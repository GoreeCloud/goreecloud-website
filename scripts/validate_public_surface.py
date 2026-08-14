#!/usr/bin/env python3
"""Validate the complete public HTML surface as one linked static site.

This complements page-specific validators by crawling every intentional public HTML
page, resolving local links/assets exactly as a browser would, validating cross-page
fragments, and keeping the sitemap aligned with indexable pages.
"""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = (
    ROOT / "index.html",
    ROOT / "privacy.html",
    ROOT / "security.html",
    ROOT / "404.html",
)
INDEXABLE_PAGES = {
    ROOT / "index.html": "https://www.goreecloud.com/",
    ROOT / "privacy.html": "https://www.goreecloud.com/privacy.html",
    ROOT / "security.html": "https://www.goreecloud.com/security.html",
}
SITEMAP = ROOT / "sitemap.xml"


class PublicPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: Counter[str] = Counter()
        self.references: list[tuple[str, str, str]] = []
        self.canonical: str | None = None
        self.robots: str | None = None

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1

        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots = attrs.get("content")

        for attr_name in ("href", "src"):
            value = attrs.get(attr_name)
            if value:
                self.references.append((tag, attr_name, value))


def report(errors: list[str]) -> int:
    if errors:
        print("Public surface validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Public surface validation passed.")
    return 0


def target_for_local_reference(source: Path, path_text: str) -> Path:
    decoded = unquote(path_text)
    if decoded in {"", "/"}:
        return ROOT / "index.html"

    if decoded.startswith("/"):
        relative = decoded.lstrip("/")
    else:
        relative = str((source.parent.relative_to(ROOT) / decoded))

    candidate = (ROOT / relative).resolve()
    candidate.relative_to(ROOT.resolve())

    if decoded.endswith("/"):
        candidate = candidate / "index.html"
    return candidate


def parse_pages(errors: list[str]) -> dict[Path, PublicPageParser]:
    parsed_pages: dict[Path, PublicPageParser] = {}
    for page in PUBLIC_PAGES:
        if not page.exists():
            errors.append(f"Required public page is missing: {page.relative_to(ROOT)}")
            continue
        parser = PublicPageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed_pages[page.resolve()] = parser

        for identifier, count in sorted(parser.ids.items()):
            if count > 1:
                errors.append(f"Duplicate id in {page.relative_to(ROOT)}: {identifier}")
    return parsed_pages


def validate_references(errors: list[str], parsed_pages: dict[Path, PublicPageParser]) -> None:
    for page, parser in parsed_pages.items():
        display_page = page.relative_to(ROOT)
        for tag, attr_name, raw_value in parser.references:
            value = raw_value.strip()
            if not value:
                continue

            if value.startswith("#"):
                fragment = unquote(value[1:])
                if fragment and fragment not in parser.ids:
                    errors.append(
                        f"{display_page} {tag}[{attr_name}] references missing fragment #{fragment}."
                    )
                continue

            parsed = urlparse(value)
            if parsed.scheme or parsed.netloc or value.startswith("//"):
                continue

            try:
                target = target_for_local_reference(page, parsed.path)
            except ValueError:
                errors.append(
                    f"{display_page} {tag}[{attr_name}] escapes repository root: {value}"
                )
                continue

            if not target.exists():
                errors.append(
                    f"{display_page} {tag}[{attr_name}] references missing local resource: {value}"
                )
                continue

            if parsed.fragment:
                target_parser = parsed_pages.get(target.resolve())
                if target_parser is None and target.suffix.lower() == ".html":
                    errors.append(
                        f"{display_page} links to HTML outside the declared public surface: {value}"
                    )
                    continue
                fragment = unquote(parsed.fragment)
                if target_parser is not None and fragment not in target_parser.ids:
                    errors.append(
                        f"{display_page} links to missing fragment #{fragment} in {target.relative_to(ROOT)}."
                    )


def validate_indexing(errors: list[str], parsed_pages: dict[Path, PublicPageParser]) -> None:
    for page, expected_canonical in INDEXABLE_PAGES.items():
        parser = parsed_pages.get(page.resolve())
        if parser is None:
            continue
        if parser.canonical != expected_canonical:
            errors.append(
                f"{page.relative_to(ROOT)} canonical must be {expected_canonical!r}, found {parser.canonical!r}."
            )
        if parser.robots and "noindex" in parser.robots.lower():
            errors.append(f"Indexable public page is marked noindex: {page.relative_to(ROOT)}")

    error_parser = parsed_pages.get((ROOT / "404.html").resolve())
    if error_parser is not None:
        if not error_parser.robots or "noindex" not in error_parser.robots.lower():
            errors.append("404.html must remain noindex.")
        if error_parser.canonical:
            errors.append("404.html must not publish a canonical URL for a missing resource.")


def validate_sitemap(errors: list[str]) -> None:
    if not SITEMAP.exists():
        errors.append("sitemap.xml is missing.")
        return

    try:
        root = ElementTree.fromstring(SITEMAP.read_text(encoding="utf-8"))
    except ElementTree.ParseError as exc:
        errors.append(f"sitemap.xml is not valid XML: {exc}")
        return

    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locations = [
        (node.text or "").strip()
        for node in root.findall(f"{namespace}url/{namespace}loc")
    ]
    expected = list(INDEXABLE_PAGES.values())

    duplicates = sorted(url for url, count in Counter(locations).items() if count > 1)
    for url in duplicates:
        errors.append(f"Duplicate sitemap URL: {url}")

    missing = sorted(set(expected).difference(locations))
    extra = sorted(set(locations).difference(expected))
    for url in missing:
        errors.append(f"Indexable public page is missing from sitemap.xml: {url}")
    for url in extra:
        errors.append(f"sitemap.xml contains an unexpected public URL: {url}")


def main() -> int:
    errors: list[str] = []
    parsed_pages = parse_pages(errors)
    validate_references(errors, parsed_pages)
    validate_indexing(errors, parsed_pages)
    validate_sitemap(errors)
    return report(errors)


if __name__ == "__main__":
    sys.exit(main())
