#!/usr/bin/env python3
"""Validate failure resilience for the rebuilt GoreeCloud public site."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

from build_public_site import GENERATED_GLAZE_FILES, PUBLIC_FILES, ROOT

ERROR_PAGE = ROOT / "404.html"
HEADERS = ROOT / "_headers"
REQUIRED_STYLESHEETS = {
    "/css/glaze-v1/glaze-v1.1.0.css",
    "/css/site-v1.1.css",
}
REQUIRED_SCRIPTS = {"/js/theme-init.js", "/js/main.js"}
EARLY_HINT = (
    "Link: </css/glaze-v1/glaze-v1.1.0.css>; rel=preload; as=style, "
    "</css/site-v1.1.css>; rel=preload; as=style"
)
REQUIRED_STATIC_HEADERS = (
    "form-action 'none'",
    "connect-src 'none'",
    "media-src 'none'",
    "worker-src 'none'",
    "X-DNS-Prefetch-Control: off",
)
PRIVATE_PATTERNS = (
    re.compile(r"\b10(?:\.\d{1,3}){3}\b"),
    re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2}\b"),
)
SENSITIVE_TERMS = ("goreecloud-vps-01", ".netbird.selfhosted")


class ErrorPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.robots: str | None = None
        self.canonical: str | None = None
        self.ids: Counter[str] = Counter()
        self.fragment_refs: set[str] = set()
        self.local_refs: set[str] = set()
        self.stylesheets: set[str] = set()
        self.scripts: set[str] = set()
        self.images_missing_alt: list[str] = []
        self.insecure_refs: list[str] = []
        self.blank_errors: list[str] = []
        self.inline_scripts = 0
        self.inline_styles = 0
        self.inline_handlers: list[str] = []
        self.h1_count = 0
        self.main_attrs: dict[str, str] | None = None
        self.title_parts: list[str] = []
        self._in_title = False

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "main" and attrs.get("id") == "main":
            self.main_attrs = attrs
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots = attrs.get("content")
        if tag == "link":
            rels = set(attrs.get("rel", "").split())
            if "canonical" in rels:
                self.canonical = attrs.get("href")
            if "stylesheet" in rels and attrs.get("href"):
                self.stylesheets.add(attrs["href"])
        if tag == "script":
            if attrs.get("src"):
                self.scripts.add(attrs["src"])
            else:
                self.inline_scripts += 1
        if tag == "style":
            self.inline_styles += 1
        if tag == "img" and "alt" not in attrs:
            self.images_missing_alt.append(attrs.get("src", "(missing src)"))
        for name in attrs:
            if name.lower().startswith("on"):
                self.inline_handlers.append(f"<{tag} {name}=...>")
        if attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.blank_errors.append(attrs.get("href", "(missing href)"))
        for attr in ("href", "src"):
            value = attrs.get(attr, "")
            if not value:
                continue
            if value.startswith("#"):
                self.fragment_refs.add(value[1:])
                continue
            parsed = urlparse(value)
            if parsed.scheme:
                if parsed.scheme == "http":
                    self.insecure_refs.append(value)
                continue
            if value.startswith("//"):
                self.insecure_refs.append(value)
                continue
            self.local_refs.add(parsed.path)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)


def validate_error_page(errors: list[str]) -> None:
    if not ERROR_PAGE.is_file():
        errors.append("Custom Cloudflare Pages not-found document is missing: 404.html")
        return

    html = ERROR_PAGE.read_text(encoding="utf-8")
    parser = ErrorPageParser()
    parser.feed(html)
    if parser.lang != "en":
        errors.append(f"404.html root language must be 'en', found {parser.lang!r}.")
    if parser.title != "Page Not Found — GoreeCloud":
        errors.append(f"404.html has unexpected title: {parser.title!r}.")
    if parser.robots != "noindex,follow":
        errors.append(f"404.html robots metadata must be 'noindex,follow', found {parser.robots!r}.")
    if parser.canonical:
        errors.append("404.html must not publish a canonical URL for a missing resource.")
    if parser.h1_count != 1:
        errors.append(f"404.html must contain exactly one h1, found {parser.h1_count}.")
    if parser.main_attrs is None or parser.main_attrs.get("tabindex") != "-1":
        errors.append("404.html main skip-link target must use id='main' and tabindex='-1'.")
    if "main" not in parser.fragment_refs:
        errors.append("404.html must include a skip link targeting #main.")
    for identifier, count in parser.ids.items():
        if count > 1:
            errors.append(f"Duplicate id found in 404.html: {identifier}")
    for fragment in parser.fragment_refs:
        if fragment and fragment not in parser.ids:
            errors.append(f"404.html references a missing in-page target: #{fragment}")
    if parser.inline_scripts or parser.inline_styles or parser.inline_handlers:
        errors.append("404.html must remain compatible with the self-only CSP and contain no inline executable/style hooks.")
    for image in parser.images_missing_alt:
        errors.append(f"404.html image must include alt text: {image}")
    for reference in parser.insecure_refs:
        errors.append(f"404.html external web references must use explicit HTTPS: {reference}")
    for href in parser.blank_errors:
        errors.append(f'404.html target="_blank" link must include rel="noopener noreferrer": {href}')

    missing_styles = sorted(REQUIRED_STYLESHEETS - parser.stylesheets)
    for stylesheet in missing_styles:
        errors.append(f"404.html must load rebuilt shared-shell stylesheet: {stylesheet}")
    missing_scripts = sorted(REQUIRED_SCRIPTS - parser.scripts)
    for script in missing_scripts:
        errors.append(f"404.html must load rebuilt shared-shell script: {script}")

    allowlisted = {"/" + relative for relative in PUBLIC_FILES}
    generated = {"/" + relative for relative in GENERATED_GLAZE_FILES}
    for reference in sorted(parser.local_refs):
        if reference in {"", "/"}:
            continue
        if not reference.startswith("/"):
            errors.append(
                "404.html local references must be origin-rooted so nested missing URLs render correctly: "
                f"{reference}"
            )
            continue
        if reference not in allowlisted and reference not in generated:
            errors.append(f"404.html local reference is outside the reviewed deployment artifact: {reference}")

    for pattern in PRIVATE_PATTERNS:
        match = pattern.search(html)
        if match:
            errors.append(f"Private-range IP address found in public 404 page: {match.group(0)}")
    lower = html.lower()
    for term in SENSITIVE_TERMS:
        if term.lower() in lower:
            errors.append(f"Private infrastructure identifier found in public 404 page: {term}")


def validate_headers(errors: list[str]) -> None:
    if not HEADERS.is_file():
        errors.append("Cloudflare Pages _headers file is missing.")
        return
    headers = HEADERS.read_text(encoding="utf-8")
    if f"/\n  {EARLY_HINT}" not in headers:
        errors.append("Homepage must preload both rebuilt critical stylesheets through the root Cloudflare Pages Link rule.")
    for marker in REQUIRED_STATIC_HEADERS:
        if marker not in headers:
            errors.append(f"Static-site security hardening is missing from _headers: {marker}")
    if "Access-Control-Allow-Origin: *" in headers:
        errors.append("The public static site must not introduce blanket cross-origin resource access.")


def main() -> int:
    errors: list[str] = []
    validate_error_page(errors)
    validate_headers(errors)
    if errors:
        print("Website resilience validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Website resilience validation passed for the rebuilt shared shell and nested 404 boundary.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
