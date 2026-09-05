#!/usr/bin/env python3
"""Verify GoreeCloud public deployments against the reviewed rebuilt artifact.

The verifier supports only GoreeCloud-controlled production and Cloudflare Pages
preview hosts. It compares every fetchable file in the explicit Main artifact,
including the generated same-origin GLAZE V1.1 bundle, against the exact reviewed
candidate bytes. It also checks security headers, preview indexing protection,
404 behavior, repository isolation, and the RFC 9116 security.txt contract.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from hashlib import sha256
import os
import re
import ssl
import sys
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

from build_public_site import GENERATED_GLAZE_FILES, PUBLIC_FILES, ROOT
from glaze_v1 import fetch_bundle

PRODUCTION_URL = "https://www.goreecloud.com"
PAGES_DOMAIN = "goreecloud-website.pages.dev"
DEFAULT_BRANCH_PREVIEW_URL = (
    "https://agent-rebuild-public-site-v1.goreecloud-website.pages.dev"
)
TARGETS = {
    "branch-preview": DEFAULT_BRANCH_PREVIEW_URL,
    "production": PRODUCTION_URL,
}
ALLOWED_HOSTS = {
    "www.goreecloud.com",
    "goreecloud.com",
}
BRANCH_NAME_RE = re.compile(r"[^a-z0-9-]+")

PUBLIC_CHECKS = {
    "/": (200, "Your cloud should belong to you.", "text/html"),
    "/repositories.html": (200, "Repositories", "text/html"),
    "/privacy.html": (200, "Privacy starts with collecting less.", "text/html"),
    "/security.html": (200, "Report security issues responsibly.", "text/html"),
    "/robots.txt": (
        200,
        "Sitemap: https://www.goreecloud.com/sitemap.xml",
        "text/plain",
    ),
    "/sitemap.xml": (200, "https://www.goreecloud.com/", "xml"),
    "/site.webmanifest": (200, '"name": "GoreeCloud"', "json"),
    "/.well-known/security.txt": (
        200,
        "Canonical: https://www.goreecloud.com/.well-known/security.txt",
        "text/plain",
    ),
    "/css/site-v1.1.css": (200, "GLAZE UI V1.1 / 1.1.0", "text/css"),
    "/css/glaze-v1/glaze-v1.1.0.css": (200, "official Stable web entrypoint", "text/css"),
    "/js/main.js": (200, "goreecloud-appearance", "javascript"),
    "/assets/goreecloud-logo.svg": (200, None, "image/svg+xml"),
}

REPOSITORY_ONLY_PATHS = (
    "/README.md",
    "/SECURITY.md",
    "/scripts/validate_site.py",
    "/.github/workflows/validate.yml",
    "/sites/labs/README.md",
)
MISSING_PATH = "/__goreecloud-deployment-smoke__/missing/nested/path"
MAX_BODY_BYTES = 1_048_576
TIMEOUT_SECONDS = 15
SECURITY_TXT_RENEWAL_BUFFER = timedelta(days=30)
EXPECTED_SECURITY_CONTACT = "mailto:security@goreecloud.com"
EXPECTED_SECURITY_CANONICAL = "https://www.goreecloud.com/.well-known/security.txt"
EXPECTED_SECURITY_POLICY = "https://www.goreecloud.com/security.html"

# Cloudflare consumes _headers as deployment configuration instead of serving it.
# Every other static allowlist entry plus every generated GLAZE file is verified.
NON_FETCHABLE_PUBLIC_FILES = frozenset({"_headers"})
ARTIFACT_FILES = tuple((*PUBLIC_FILES, *GENERATED_GLAZE_FILES))
REMOTE_INTEGRITY_FILES = tuple(
    relative for relative in ARTIFACT_FILES if relative not in NON_FETCHABLE_PUBLIC_FILES
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


def normalize_branch_preview_label(branch: str) -> str:
    """Convert a Git branch name into Cloudflare Pages' bounded preview label."""
    label = BRANCH_NAME_RE.sub(
        "-",
        branch.strip().lower().replace("/", "-"),
    ).strip("-")
    label = re.sub(r"-+", "-", label)
    if not label:
        raise ValueError("Branch preview name resolves to an empty Cloudflare label.")
    return label[:28].rstrip("-")


def branch_preview_url(branch: str | None = None) -> str:
    """Resolve the current PR preview, with a reviewed non-CI fallback."""
    branch_name = branch or os.environ.get("GITHUB_HEAD_REF")
    if not branch_name:
        return DEFAULT_BRANCH_PREVIEW_URL
    label = normalize_branch_preview_label(branch_name)
    return f"https://{label}.{PAGES_DOMAIN}"


def target_url(target: str) -> str:
    if target == "branch-preview":
        return branch_preview_url()
    return TARGETS[target]


def host_is_allowed(hostname: str | None) -> bool:
    if not hostname:
        return False
    return hostname in ALLOWED_HOSTS or hostname.endswith(f".{PAGES_DOMAIN}")


def validate_fixed_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Only HTTPS targets are permitted: {url}")
    if not host_is_allowed(parsed.hostname):
        raise ValueError(f"Host is outside the GoreeCloud verifier allowlist: {url}")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError(
            "Target must not contain credentials, query parameters, or fragments: "
            f"{url}"
        )


class AllowlistedRedirectHandler(HTTPRedirectHandler):
    """Reject unsafe redirect destinations before urllib follows them."""

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
            "User-Agent": "GoreeCloud-Deployment-Verifier/1.1",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
        },
        method="GET",
    )
    opener = build_opener(
        AllowlistedRedirectHandler(),
        HTTPSHandler(context=ssl.create_default_context()),
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
    if not relative or relative.startswith("/") or ".." in relative.split("/"):
        raise ValueError(f"Public integrity path must be repository-relative: {relative!r}")
    return "/" if relative == "index.html" else f"/{relative}"


@lru_cache(maxsize=1)
def generated_glaze_candidate() -> dict[str, str]:
    """Fetch and validate the exact generated GLAZE bytes once per verifier run."""
    return fetch_bundle()


def candidate_bytes(relative: str) -> bytes:
    """Return the exact bytes the rebuilt Main artifact publishes for one file."""
    if relative in PUBLIC_FILES:
        source = ROOT / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Candidate integrity source is unavailable or unsafe: {relative}")
        return source.read_bytes()

    if relative in GENERATED_GLAZE_FILES:
        name = relative.removeprefix("css/glaze-v1/")
        try:
            return generated_glaze_candidate()[name].encode("utf-8")
        except KeyError as error:
            raise ValueError(f"Generated GLAZE candidate is missing: {name}") from error

    raise ValueError(f"Candidate integrity path is outside the reviewed artifact: {relative}")


def verify_candidate_content_integrity(base_url: str, errors: list[str]) -> None:
    for relative in REMOTE_INTEGRITY_FILES:
        try:
            expected = candidate_bytes(relative)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue
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
            errors.append(
                f"Candidate content mismatch for {path}: expected SHA-256 "
                f"{sha256(expected).hexdigest()}, deployed SHA-256 "
                f"{sha256(response.body).hexdigest()}."
            )


def verify_public_surface(base_url: str, errors: list[str]) -> None:
    for path, (expected_status, marker, expected_type) in PUBLIC_CHECKS.items():
        try:
            response = fetch(build_url(base_url, path))
        except RuntimeError as error:
            errors.append(str(error))
            continue
        if response.status != expected_status:
            errors.append(f"{path} returned HTTP {response.status}; expected {expected_status}.")
            continue
        if not host_is_allowed(urlparse(response.final_url).hostname):
            errors.append(f"{path} redirected outside the GoreeCloud host allowlist: {response.final_url}")
        actual_type = response.headers.get("content-type", "")
        if not content_type_matches(actual_type, expected_type):
            errors.append(
                f"{path} returned Content-Type {actual_type!r}; expected {expected_type!r}."
            )
        if marker:
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
        errors.append(f"Cannot validate root response headers because / returned HTTP {response.status}.")
        return
    for header, markers in REQUIRED_HEADERS.items():
        value = response.headers.get(header)
        if value is None:
            errors.append(f"Root response is missing required header: {header}")
            continue
        lower_value = value.lower()
        for marker in markers:
            if marker.lower() not in lower_value:
                errors.append(f"Root response header {header} is missing required value: {marker}")


def verify_indexing_header(target: str, base_url: str, errors: list[str]) -> None:
    try:
        response = fetch(build_url(base_url, "/"))
    except RuntimeError as error:
        errors.append(str(error))
        return
    tokens = {
        token.strip()
        for token in response.headers.get("x-robots-tag", "").lower().replace(";", ",").split(",")
        if token.strip()
    }
    if target == "branch-preview" and "noindex" not in tokens:
        errors.append("Branch preview is missing the expected X-Robots-Tag: noindex protection.")
    if target == "production" and "noindex" in tokens:
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
    for marker in ("Page Not Found — GoreeCloud", "This page isn’t here.", "noindex,follow"):
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
        errors.append(f"/.well-known/security.txt returned HTTP {response.status}; expected 200.")
        return
    if "max-age=3600" not in response.headers.get("cache-control", "").lower():
        errors.append("/.well-known/security.txt is missing the intended one-hour Cache-Control policy.")
    fields = parse_security_txt(response.body.decode("utf-8", errors="replace"))
    contacts = fields.get("contact", [])
    if not contacts or contacts[0] != EXPECTED_SECURITY_CONTACT:
        errors.append("Deployed security.txt does not publish the expected primary security contact.")
    if EXPECTED_SECURITY_CANONICAL not in fields.get("canonical", []):
        errors.append("Deployed security.txt does not publish the expected canonical URL.")
    if EXPECTED_SECURITY_POLICY not in fields.get("policy", []):
        errors.append("Deployed security.txt does not publish the expected security policy URL.")
    expires_values = fields.get("expires", [])
    if len(expires_values) != 1:
        errors.append(
            f"Deployed security.txt must contain exactly one Expires field, found {len(expires_values)}."
        )
        return
    expires = parse_rfc3339(expires_values[0])
    if expires is None:
        errors.append("Deployed security.txt Expires is not a valid timezone-aware RFC3339 timestamp.")
    elif expires - datetime.now(timezone.utc) <= SECURITY_TXT_RENEWAL_BUFFER:
        errors.append("Deployed security.txt expires within 30 days and must be renewed before it becomes stale.")


def verify_production_redirect(errors: list[str]) -> None:
    try:
        response = fetch("https://goreecloud.com/")
    except RuntimeError as error:
        errors.append(str(error))
        return
    if response.status != 200:
        errors.append(f"Apex production URL resolved to HTTP {response.status}; expected final HTTP 200.")
    if urlparse(response.final_url).hostname != "www.goreecloud.com":
        errors.append(f"Apex production URL did not resolve to the canonical www host: {response.final_url}")


def check_configuration() -> int:
    errors: list[str] = []
    if set(TARGETS) != {"branch-preview", "production"}:
        errors.append("Verifier target set must remain exactly branch-preview and production.")
    for name in TARGETS:
        try:
            validate_fixed_url(target_url(name))
        except ValueError as error:
            errors.append(f"Invalid fixed target {name}: {error}")
    if not host_is_allowed(f"preview.{PAGES_DOMAIN}"):
        errors.append("Cloudflare Pages preview host pattern is missing from the verifier allowlist.")
    if NON_FETCHABLE_PUBLIC_FILES != frozenset({"_headers"}):
        errors.append("Remote integrity exclusion set must remain exactly the Cloudflare _headers control file.")
    if set(PUBLIC_FILES) & set(GENERATED_GLAZE_FILES):
        errors.append("Generated GLAZE files must remain disjoint from copied source allowlist entries.")
    if set(REMOTE_INTEGRITY_FILES) != set(ARTIFACT_FILES) - NON_FETCHABLE_PUBLIC_FILES:
        errors.append("Remote integrity file set has drifted from the rebuilt public artifact contract.")
    if not set(GENERATED_GLAZE_FILES).issubset(REMOTE_INTEGRITY_FILES):
        errors.append("Generated GLAZE files must remain within the remotely verified artifact set.")
    if errors:
        print("Remote deployment verifier configuration failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Remote deployment verifier configuration passed for the rebuilt Main artifact.")
    return 0


def verify(target: str) -> int:
    base_url = target_url(target)
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
