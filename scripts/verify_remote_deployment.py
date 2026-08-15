#!/usr/bin/env python3
"""Verify the public GoreeCloud deployment after a Cloudflare Pages cutover.

The verifier intentionally supports only fixed GoreeCloud targets. It is safe to
invoke from a manual GitHub Actions workflow because arbitrary URLs are never
accepted, redirects are checked before they are followed, and every network
request stays within the declared GoreeCloud hosts.

Remote acceptance also compares every fetchable allowlisted public file against
the exact local candidate bytes. This connects the repository's reviewed public
artifact to the deployed HTTP surface without publishing a private repository
commit identifier to website visitors.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import ssl
import sys
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

from build_public_site import PUBLIC_FILES, ROOT

TARGETS = {
    "branch-preview": "https://agent-glaze-ui-interaction-p.goreecloud-website.pages.dev",
    "production": "https://www.goreecloud.com",
}
ALLOWED_HOSTS = {
    "agent-glaze-ui-interaction-p.goreecloud-website.pages.dev",
    "www.goreecloud.com",
    "goreecloud.com",
}
PUBLIC_CHECKS = {
    "/": (200, "<title>GoreeCloud", "text/html"),
    "/privacy.html": (200, "<h1>Privacy at GoreeCloud</h1>", "text/html"),
    "/security.html": (200, "<h1>Responsible security reporting</h1>", "text/html"),
    "/robots.txt": (200, "Sitemap: https://www.goreecloud.com/sitemap.xml", "text/plain"),
    "/sitemap.xml": (200, "https://www.goreecloud.com/", "xml"),
    "/site.webmanifest": (200, '"name": "GoreeCloud"', "json"),
    "/.well-known/security.txt": (
        200,
        "Canonical: https://www.goreecloud.com/.well-known/security.txt",
        "text/plain",
    ),
    "/css/style.css": (200, ":root", "text/css"),
    "/js/main.js": (200, "document", "javascript"),
    "/assets/goreecloud-icon.png": (200, None, "image/png"),
}
REPOSITORY_ONLY_PATHS = (
    "/README.md",
    "/SECURITY.md",
    "/scripts/validate_site.py",
    "/.github/workflows/validate.yml",
)
MISSING_PATH = "/__goreecloud-deployment-smoke__/missing/nested/path"
MAX_BODY_BYTES = 1_048_576
TIMEOUT_SECONDS = 15
SECURITY_TXT_RENEWAL_BUFFER = timedelta(days=30)
EXPECTED_SECURITY_CONTACT = "mailto:goreecloud@gmail.com"
EXPECTED_SECURITY_CANONICAL = "https://www.goreecloud.com/.well-known/security.txt"
EXPECTED_SECURITY_POLICY = "https://www.goreecloud.com/security.html"

# Cloudflare consumes _headers as deployment configuration rather than exposing it
# as a public resource. Every other allowlisted source file should be fetchable and
# byte-identical to the candidate being verified.
NON_FETCHABLE_PUBLIC_FILES = frozenset({"_headers"})
REMOTE_INTEGRITY_FILES = tuple(
    relative for relative in PUBLIC_FILES if relative not in NON_FETCHABLE_PUBLIC_FILES
)

REQUIRED_HEADERS = {
    "content-security-policy": (
        "default-src 'self'",
        "base-uri 'self'",
        "object-src 'none'",
        "frame-ancestors 'none'",
        "form-action 'none'",
        "script-src 'self'",
        "style-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'none'",
        "media-src 'none'",
        "manifest-src 'self'",
        "worker-src 'none'",
        "upgrade-insecure-requests",
    ),
    "permissions-policy": (
        "accelerometer=()",
        "camera=()",
        "display-capture=()",
        "geolocation=()",
        "microphone=()",
        "payment=()",
        "usb=()",
    ),
    "referrer-policy": ("no-referrer",),
    "x-content-type-options": ("nosniff",),
    "x-frame-options": ("DENY",),
    "x-permitted-cross-domain-policies": ("none",),
    "x-dns-prefetch-control": ("off",),
    "cross-origin-opener-policy": ("same-origin",),
    "origin-agent-cluster": ("?1",),
    "strict-transport-security": ("max-age=31536000",),
}


@dataclass(frozen=True)
class Response:
    status: int
    final_url: str
    headers: Mapping[str, str]
    body: bytes


def validate_fixed_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Only HTTPS targets are permitted: {url}")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host is outside the GoreeCloud verifier allowlist: {url}")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError(
            f"Target must not contain credentials, query parameters, or fragments: {url}"
        )


class AllowlistedRedirectHandler(HTTPRedirectHandler):
    """Reject redirect destinations before urllib can make the next request."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            validate_fixed_url(newurl)
        except ValueError as error:
            raise URLError(f"Redirect target rejected: {error}") from error
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def build_url(base_url: str, path: str) -> str:
    if not path.startswith("/"):
        raise ValueError(f"Verifier paths must be origin-rooted: {path}")
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    validate_fixed_url(url)
    return url


def fetch(url: str) -> Response:
    validate_fixed_url(url)
    request = Request(
        url,
        headers={
            "User-Agent": "GoreeCloud-Deployment-Verifier/1.0",
            "Accept": "*/*",
            # Exact candidate-byte validation must not depend on transfer encoding.
            "Accept-Encoding": "identity",
        },
        method="GET",
    )
    context = ssl.create_default_context()
    opener = build_opener(
        AllowlistedRedirectHandler(),
        HTTPSHandler(context=context),
    )
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read(MAX_BODY_BYTES + 1)
            if len(body) > MAX_BODY_BYTES:
                raise RuntimeError(f"Response exceeded {MAX_BODY_BYTES} bytes: {url}")
            return Response(
                status=response.status,
                final_url=response.geturl(),
                headers={key.lower(): value for key, value in response.headers.items()},
                body=body,
            )
    except HTTPError as error:
        body = error.read(MAX_BODY_BYTES + 1)
        if len(body) > MAX_BODY_BYTES:
            raise RuntimeError(f"Error response exceeded {MAX_BODY_BYTES} bytes: {url}") from error
        return Response(
            status=error.code,
            final_url=error.geturl(),
            headers={key.lower(): value for key, value in error.headers.items()},
            body=body,
        )
    except URLError as error:
        raise RuntimeError(f"Network request failed for {url}: {error.reason}") from error


def content_type_matches(actual: str, expected: str) -> bool:
    media_type = actual.split(";", 1)[0].strip().lower()
    if expected == "xml":
        return media_type in {"application/xml", "text/xml"} or media_type.endswith("+xml")
    if expected == "json":
        return media_type in {"application/json", "application/manifest+json"} or media_type.endswith("+json")
    if expected == "javascript":
        return media_type in {"application/javascript", "text/javascript"}
    return media_type == expected


def parse_security_txt(text: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields.setdefault(key.strip().lower(), []).append(value.strip())
    return fields


def parse_rfc3339(value: str) -> datetime | None:
    normalized = value[:-1] + "+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def remote_path_for_public_file(relative: str) -> str:
    """Map one reviewed public source path to its deployed fetch path."""

    if not relative or relative.startswith("/"):
        raise ValueError(f"Public integrity path must be repository-relative: {relative!r}")
    if ".." in relative.split("/"):
        raise ValueError(f"Public integrity path must not traverse directories: {relative!r}")
    if relative == "index.html":
        return "/"
    return f"/{relative}"


def verify_candidate_content_integrity(base_url: str, errors: list[str]) -> None:
    """Prove the deployed public resources match this exact repository candidate."""

    for relative in REMOTE_INTEGRITY_FILES:
        source = ROOT / relative
        if source.is_symlink() or not source.is_file():
            errors.append(f"Candidate integrity source is unavailable or unsafe: {relative}")
            continue

        expected = source.read_bytes()
        path = remote_path_for_public_file(relative)
        try:
            response = fetch(build_url(base_url, path))
        except RuntimeError as error:
            errors.append(str(error))
            continue

        if response.status != 200:
            errors.append(
                f"Candidate integrity resource {path} returned HTTP {response.status}; expected 200."
            )
            continue

        if response.body != expected:
            expected_digest = sha256(expected).hexdigest()
            actual_digest = sha256(response.body).hexdigest()
            errors.append(
                f"Candidate content mismatch for {path}: expected SHA-256 "
                f"{expected_digest}, deployed SHA-256 {actual_digest}."
            )


def verify_public_surface(base_url: str, errors: list[str]) -> None:
    for path, (expected_status, marker, expected_type) in PUBLIC_CHECKS.items():
        url = build_url(base_url, path)
        try:
            response = fetch(url)
        except RuntimeError as error:
            errors.append(str(error))
            continue

        if response.status != expected_status:
            errors.append(f"{path} returned HTTP {response.status}; expected {expected_status}.")
            continue

        final_host = urlparse(response.final_url).hostname
        if final_host not in ALLOWED_HOSTS:
            errors.append(
                f"{path} redirected outside the GoreeCloud host allowlist: {response.final_url}"
            )

        actual_type = response.headers.get("content-type", "")
        if not content_type_matches(actual_type, expected_type):
            errors.append(
                f"{path} returned Content-Type {actual_type!r}; expected {expected_type!r}."
            )

        if marker is not None:
            text = response.body.decode("utf-8", errors="replace")
            if marker not in text:
                errors.append(f"{path} is missing expected deployment marker: {marker}")


def verify_headers(base_url: str, errors: list[str]) -> None:
    try:
        response = fetch(build_url(base_url, "/"))
    except RuntimeError as error:
        errors.append(str(error))
        return

    if response.status != 200:
        errors.append(
            f"Cannot validate root response headers because / returned HTTP {response.status}."
        )
        return

    for header, markers in REQUIRED_HEADERS.items():
        value = response.headers.get(header)
        if value is None:
            errors.append(f"Root response is missing required header: {header}")
            continue
        lower_value = value.lower()
        for marker in markers:
            if marker.lower() not in lower_value:
                errors.append(
                    f"Root response header {header} is missing required value: {marker}"
                )


def verify_indexing_header(target: str, base_url: str, errors: list[str]) -> None:
    try:
        response = fetch(build_url(base_url, "/"))
    except RuntimeError as error:
        errors.append(str(error))
        return

    x_robots = response.headers.get("x-robots-tag", "").lower()
    has_noindex = "noindex" in {
        token.strip()
        for token in x_robots.replace(";", ",").split(",")
        if token.strip()
    }

    if target == "branch-preview" and not has_noindex:
        errors.append(
            "Branch preview is missing the expected X-Robots-Tag: noindex protection."
        )
    if target == "production" and has_noindex:
        errors.append(
            "Production root unexpectedly publishes X-Robots-Tag: noindex and would be excluded from search indexing."
        )


def verify_not_found_behavior(base_url: str, errors: list[str]) -> None:
    try:
        response = fetch(build_url(base_url, MISSING_PATH))
    except RuntimeError as error:
        errors.append(str(error))
        return

    if response.status != 404:
        errors.append(f"Nested missing path returned HTTP {response.status}; expected 404.")
        return

    text = response.body.decode("utf-8", errors="replace")
    for marker in (
        "Page Not Found — GoreeCloud",
        "This page isn’t here.",
        "noindex,follow",
    ):
        if marker not in text:
            errors.append(f"Nested 404 response is missing expected marker: {marker}")


def verify_repository_isolation(base_url: str, errors: list[str]) -> None:
    for path in REPOSITORY_ONLY_PATHS:
        try:
            response = fetch(build_url(base_url, path))
        except RuntimeError as error:
            errors.append(str(error))
            continue
        if response.status != 404:
            errors.append(
                f"Repository-only path {path} returned HTTP {response.status}; expected 404 from the isolated dist artifact."
            )


def verify_security_txt(base_url: str, errors: list[str]) -> None:
    try:
        response = fetch(build_url(base_url, "/.well-known/security.txt"))
    except RuntimeError as error:
        errors.append(str(error))
        return

    if response.status != 200:
        errors.append(
            f"/.well-known/security.txt returned HTTP {response.status}; expected 200."
        )
        return

    cache_control = response.headers.get("cache-control", "").lower()
    if "max-age=3600" not in cache_control:
        errors.append(
            "/.well-known/security.txt is missing the intended one-hour Cache-Control policy."
        )

    text = response.body.decode("utf-8", errors="replace")
    fields = parse_security_txt(text)

    contacts = fields.get("contact", [])
    if not contacts or contacts[0] != EXPECTED_SECURITY_CONTACT:
        errors.append(
            "Deployed security.txt does not publish the expected primary security contact."
        )

    if EXPECTED_SECURITY_CANONICAL not in fields.get("canonical", []):
        errors.append("Deployed security.txt does not publish the expected canonical URL.")

    if EXPECTED_SECURITY_POLICY not in fields.get("policy", []):
        errors.append("Deployed security.txt does not publish the expected security policy URL.")

    expires_values = fields.get("expires", [])
    if len(expires_values) != 1:
        errors.append(
            f"Deployed security.txt must contain exactly one Expires field, found {len(expires_values)}."
        )
    else:
        expires = parse_rfc3339(expires_values[0])
        if expires is None:
            errors.append(
                "Deployed security.txt Expires is not a valid timezone-aware RFC3339 timestamp."
            )
        elif expires - datetime.now(timezone.utc) <= SECURITY_TXT_RENEWAL_BUFFER:
            errors.append(
                "Deployed security.txt expires within 30 days and must be renewed before it becomes stale."
            )


def verify_production_redirect(errors: list[str]) -> None:
    try:
        response = fetch("https://goreecloud.com/")
    except RuntimeError as error:
        errors.append(str(error))
        return
    if response.status != 200:
        errors.append(
            f"Apex production URL resolved to HTTP {response.status}; expected final HTTP 200."
        )
    if urlparse(response.final_url).hostname != "www.goreecloud.com":
        errors.append(
            f"Apex production URL did not resolve to the canonical www host: {response.final_url}"
        )


def check_configuration() -> int:
    errors: list[str] = []

    if set(TARGETS) != {"branch-preview", "production"}:
        errors.append("Verifier target set must remain exactly branch-preview and production.")

    for name, url in TARGETS.items():
        try:
            validate_fixed_url(url)
        except ValueError as error:
            errors.append(f"Invalid fixed target {name}: {error}")

    if "www.goreecloud.com" not in ALLOWED_HOSTS or "goreecloud.com" not in ALLOWED_HOSTS:
        errors.append("Canonical production hosts are missing from the verifier allowlist.")
    if not any(
        host.endswith(".goreecloud-website.pages.dev") for host in ALLOWED_HOSTS
    ):
        errors.append("Cloudflare branch-preview host is missing from the verifier allowlist.")

    if NON_FETCHABLE_PUBLIC_FILES != frozenset({"_headers"}):
        errors.append("Remote integrity exclusion set must remain exactly the Cloudflare _headers control file.")
    if set(REMOTE_INTEGRITY_FILES) != set(PUBLIC_FILES) - NON_FETCHABLE_PUBLIC_FILES:
        errors.append("Remote integrity file set has drifted from the reviewed public artifact allowlist.")

    integrity_paths: list[str] = []
    for relative in REMOTE_INTEGRITY_FILES:
        try:
            integrity_paths.append(remote_path_for_public_file(relative))
        except ValueError as error:
            errors.append(str(error))

    for path in (*PUBLIC_CHECKS, *REPOSITORY_ONLY_PATHS, *integrity_paths, MISSING_PATH):
        if not path.startswith("/") or ".." in path:
            errors.append(f"Unsafe verifier path configured: {path}")

    required_header_names = {
        "content-security-policy",
        "permissions-policy",
        "referrer-policy",
        "x-content-type-options",
        "x-frame-options",
        "x-permitted-cross-domain-policies",
        "x-dns-prefetch-control",
        "cross-origin-opener-policy",
        "origin-agent-cluster",
        "strict-transport-security",
    }
    if set(REQUIRED_HEADERS) != required_header_names:
        errors.append(
            "Remote verifier required-header set has drifted from the reviewed deployment contract."
        )

    if SECURITY_TXT_RENEWAL_BUFFER != timedelta(days=30):
        errors.append(
            "Remote verifier must preserve the 30-day security.txt renewal warning window."
        )

    if errors:
        print("Remote deployment verifier configuration failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Remote deployment verifier configuration passed.")
    return 0


def verify(target: str) -> int:
    base_url = TARGETS[target]
    errors: list[str] = []

    verify_candidate_content_integrity(base_url, errors)
    verify_public_surface(base_url, errors)
    verify_headers(base_url, errors)
    verify_indexing_header(target, base_url, errors)
    verify_not_found_behavior(base_url, errors)
    verify_repository_isolation(base_url, errors)
    verify_security_txt(base_url, errors)
    if target == "production":
        verify_production_redirect(errors)

    if errors:
        print(f"Remote deployment verification failed for {target} ({base_url}):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Remote deployment verification passed for {target}: {base_url}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check-config",
        action="store_true",
        help="Validate verifier configuration without network access.",
    )
    group.add_argument(
        "--target",
        choices=tuple(TARGETS),
        help="Verify one fixed GoreeCloud deployment target.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check_config:
        return check_configuration()
    return verify(args.target)


if __name__ == "__main__":
    sys.exit(main())
