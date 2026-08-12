#!/usr/bin/env python3
"""Validate the dependency-free GoreeCloud public website.

The checks intentionally use only the Python standard library so GitHub Actions can
validate the repository without downloading third-party packages.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CANONICAL = "https://www.goreecloud.com/"
PRIVATE_PATTERNS = (
    re.compile(r"\b10(?:\.\d{1,3}){3}\b"),
    re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2}\b"),
)
SENSITIVE_TERMS = ("goreecloud-vps-01", ".netbird.selfhosted")


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.local_refs: set[str] = set()
        self.fragment_refs: set[str] = set()
        self.external_blank_errors: list[str] = []
        self.canonical: str | None = None
        self.og_url: str | None = None
        self.script_sources: list[str] = []
        self.stylesheet_sources: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if attrs.get("id"):
            self.ids.add(attrs["id"])

        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("property") == "og:url":
            self.og_url = attrs.get("content")

        if tag == "script" and attrs.get("src"):
            self.script_sources.append(attrs["src"])
        if tag == "link" and "stylesheet" in attrs.get("rel", "").split() and attrs.get("href"):
            self.stylesheet_sources.append(attrs["href"])

        for attr in ("href", "src"):
            value = attrs.get(attr, "")
            if not value:
                continue
            if value.startswith("#"):
                self.fragment_refs.add(value[1:])
                continue
            parsed = urlparse(value)
            if parsed.scheme or value.startswith("//"):
                continue
            self.local_refs.add(parsed.path)

        if attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.external_blank_errors.append(attrs.get("href", "(missing href)"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    html = INDEX.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)

    if parser.canonical != CANONICAL:
        fail(errors, f"Canonical URL must be {CANONICAL!r}, found {parser.canonical!r}.")
    if parser.og_url != CANONICAL:
        fail(errors, f"Open Graph URL must be {CANONICAL!r}, found {parser.og_url!r}.")

    missing_fragments = sorted(ref for ref in parser.fragment_refs if ref and ref not in parser.ids)
    for fragment in missing_fragments:
        fail(errors, f"Missing in-page target for #{fragment}.")

    for reference in sorted(parser.local_refs):
        target = (ROOT / reference).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(errors, f"Local reference escapes repository root: {reference}")
            continue
        if not target.exists():
            fail(errors, f"Missing local asset referenced by index.html: {reference}")

    for href in parser.external_blank_errors:
        fail(errors, f'target="_blank" link must include rel="noopener noreferrer": {href}')

    for src in parser.script_sources + parser.stylesheet_sources:
        if urlparse(src).scheme or src.startswith("//"):
            fail(errors, f"Browser code dependency must be self-hosted, found external resource: {src}")

    public_text_files = [
        INDEX,
        ROOT / "README.md",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / "_headers",
    ]
    public_text_files.extend((ROOT / "css").glob("*.css"))
    public_text_files.extend((ROOT / "js").glob("*.js"))

    for path in public_text_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in PRIVATE_PATTERNS:
            match = pattern.search(text)
            if match:
                fail(errors, f"Private-range IP address found in {path.relative_to(ROOT)}: {match.group(0)}")
        lower_text = text.lower()
        for term in SENSITIVE_TERMS:
            if term.lower() in lower_text:
                fail(errors, f"Private infrastructure identifier found in {path.relative_to(ROOT)}: {term}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {CANONICAL}sitemap.xml" not in robots:
        fail(errors, "robots.txt sitemap URL does not match the canonical www hostname.")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"<loc>{CANONICAL}</loc>" not in sitemap:
        fail(errors, "sitemap.xml does not contain the canonical www homepage URL.")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Website validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
