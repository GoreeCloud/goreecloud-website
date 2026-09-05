#!/usr/bin/env python3
"""Validate the complete rebuilt Main public surface against its deployment contract.

The rebuilt root website is reviewed source, not a template that is rewritten into a
different public composition. This validator therefore crawls the exact source pages
and checks local references against the explicit deployment allowlist plus generated
same-origin GLAZE files. Repository-only/source-only files cannot satisfy public links.
"""

from __future__ import annotations

from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree
import posixpath
import sys

from build_public_site import GENERATED_GLAZE_FILES, PUBLIC_FILES, ROOT

PUBLIC_PAGE_NAMES = (
    "index.html",
    "privacy.html",
    "repositories.html",
    "security.html",
    "404.html",
)
PUBLIC_PAGES = tuple(ROOT / name for name in PUBLIC_PAGE_NAMES)
INDEXABLE_PAGES = {
    "index.html": "https://www.goreecloud.com/",
    "privacy.html": "https://www.goreecloud.com/privacy.html",
    "repositories.html": "https://www.goreecloud.com/repositories.html",
    "security.html": "https://www.goreecloud.com/security.html",
}
DEPLOYABLE_PATHS = set(PUBLIC_FILES) | set(GENERATED_GLAZE_FILES)
SITEMAP = ROOT / "sitemap.xml"
ROBOTS = ROOT / "robots.txt"
CANONICAL_SITEMAP_URL = "https://www.goreecloud.com/sitemap.xml"
SITEMAP_NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
CANONICAL_LOGO = "assets/goreecloud-logo.svg"
MANIFEST_PATH = "site.webmanifest"


class PublicPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: Counter[str] = Counter()
        self.references: list[tuple[str, str, str]] = []
        self.canonical: str | None = None
        self.robots: str | None = None
        self.meta_names: dict[str, str] = {}
        self.manifest_href: str | None = None
        self.icon_links: list[tuple[set[str], str, str]] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1

        if tag == "link":
            rels = set(attrs.get("rel", "").lower().split())
            if "canonical" in rels:
                self.canonical = attrs.get("href")
            if "manifest" in rels:
                self.manifest_href = attrs.get("href")
            if "icon" in rels:
                self.icon_links.append((rels, attrs.get("href", ""), attrs.get("type", "")))
        if tag == "meta":
            name = attrs.get("name", "").lower()
            if name:
                self.meta_names[name] = attrs.get("content", "")
            if name == "robots":
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
    print("Rebuilt public surface validation passed against the exact deployment allowlist.")
    return 0


def normalize_local_path(source_name: str, path_text: str) -> str:
    decoded = unquote(path_text)
    if decoded in {"", "/"}:
        return "index.html"
    if decoded.startswith("/"):
        relative = decoded.lstrip("/")
    else:
        base = posixpath.dirname(source_name)
        relative = posixpath.normpath(posixpath.join(base, decoded))
    if relative.startswith("../") or relative == "..":
        raise ValueError("reference escapes public root")
    if relative.endswith("/"):
        relative = f"{relative}index.html"
    return relative


def parse_pages(errors: list[str]) -> dict[str, PublicPageParser]:
    parsed_pages: dict[str, PublicPageParser] = {}
    for page in PUBLIC_PAGES:
        if not page.is_file() or page.is_symlink():
            errors.append(f"Required public page is missing or invalid: {page.relative_to(ROOT)}")
            continue
        parser = PublicPageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        relative = page.name
        parsed_pages[relative] = parser
        for identifier, count in sorted(parser.ids.items()):
            if count > 1:
                errors.append(f"Duplicate id in {relative}: {identifier}")
    return parsed_pages


def validate_references(errors: list[str], parsed_pages: dict[str, PublicPageParser]) -> None:
    for source_name, parser in parsed_pages.items():
        for tag, attr_name, raw_value in parser.references:
            value = raw_value.strip()
            if not value:
                continue
            if value.startswith("#"):
                fragment = unquote(value[1:])
                if fragment and fragment not in parser.ids:
                    errors.append(f"{source_name} {tag}[{attr_name}] references missing fragment #{fragment}.")
                continue

            parsed = urlparse(value)
            if parsed.scheme or parsed.netloc or value.startswith("//"):
                continue

            try:
                target = normalize_local_path(source_name, parsed.path)
            except ValueError:
                errors.append(f"{source_name} {tag}[{attr_name}] escapes the public root: {value}")
                continue
            if target not in DEPLOYABLE_PATHS:
                errors.append(
                    f"{source_name} {tag}[{attr_name}] references a file outside the reviewed public artifact: {value}"
                )
                continue

            if parsed.fragment and target.endswith(".html"):
                target_parser = parsed_pages.get(target)
                if target_parser is None:
                    errors.append(f"{source_name} links to HTML outside the declared Main public-page set: {value}")
                    continue
                fragment = unquote(parsed.fragment)
                if fragment not in target_parser.ids:
                    errors.append(f"{source_name} links to missing fragment #{fragment} in {target}.")


def validate_indexing(errors: list[str], parsed_pages: dict[str, PublicPageParser]) -> None:
    for page_name, expected_canonical in INDEXABLE_PAGES.items():
        parser = parsed_pages.get(page_name)
        if parser is None:
            continue
        if parser.canonical != expected_canonical:
            errors.append(f"{page_name} canonical must be {expected_canonical!r}, found {parser.canonical!r}.")
        if not parser.robots or "noindex" in parser.robots.lower():
            errors.append(f"Indexable public page must explicitly remain indexable: {page_name}")

    error_parser = parsed_pages.get("404.html")
    if error_parser is not None:
        if not error_parser.robots or "noindex" not in error_parser.robots.lower():
            errors.append("404.html must remain noindex.")
        if error_parser.canonical:
            errors.append("404.html must not publish a canonical URL for a missing resource.")


def validate_page_metadata(errors: list[str], parsed_pages: dict[str, PublicPageParser]) -> None:
    for page_name in PUBLIC_PAGE_NAMES:
        parser = parsed_pages.get(page_name)
        if parser is None:
            continue
        if parser.meta_names.get("application-name") != "GoreeCloud":
            errors.append(f"{page_name} must publish application-name=GoreeCloud.")
        if parser.meta_names.get("author") != "GoreeCloud":
            errors.append(f"{page_name} must publish author=GoreeCloud.")
        if parser.meta_names.get("goreecloud-glaze-ui") != "1.1.0":
            errors.append(f"{page_name} must publish the Website GLAZE UI source target 1.1.0.")

        manifest = (parser.manifest_href or "").lstrip("/")
        if manifest != MANIFEST_PATH:
            errors.append(f"{page_name} must link explicitly to /{MANIFEST_PATH}.")

        normalized_icons = {
            (frozenset(rels), href.lstrip("/"), content_type)
            for rels, href, content_type in parser.icon_links
        }
        if not any(
            "icon" in rels
            and href == CANONICAL_LOGO
            and content_type == "image/svg+xml"
            for rels, href, content_type in normalized_icons
        ):
            errors.append(f"{page_name} must publish the canonical GoreeCloud SVG favicon.")


def validate_sitemap(errors: list[str]) -> None:
    if not SITEMAP.exists():
        errors.append("sitemap.xml is missing.")
        return
    try:
        root = ElementTree.fromstring(SITEMAP.read_text(encoding="utf-8"))
    except ElementTree.ParseError as exc:
        errors.append(f"sitemap.xml is not valid XML: {exc}")
        return
    if root.tag != f"{SITEMAP_NAMESPACE}urlset":
        errors.append("sitemap.xml must use the standard sitemaps.org urlset namespace.")
        return

    locations: list[str] = []
    today = date.today()
    for url_node in root.findall(f"{SITEMAP_NAMESPACE}url"):
        loc_nodes = url_node.findall(f"{SITEMAP_NAMESPACE}loc")
        lastmod_nodes = url_node.findall(f"{SITEMAP_NAMESPACE}lastmod")
        if len(loc_nodes) != 1:
            errors.append(f"Each sitemap URL entry must contain exactly one <loc>; found {len(loc_nodes)}.")
            continue
        location = (loc_nodes[0].text or "").strip()
        if not location:
            errors.append("sitemap.xml contains an empty <loc> value.")
            continue
        locations.append(location)
        if len(lastmod_nodes) != 1:
            errors.append(f"Sitemap entry {location} must contain exactly one <lastmod>; found {len(lastmod_nodes)}.")
            continue
        lastmod_text = (lastmod_nodes[0].text or "").strip()
        try:
            lastmod = date.fromisoformat(lastmod_text)
        except ValueError:
            errors.append(f"Sitemap entry {location} has invalid YYYY-MM-DD lastmod: {lastmod_text!r}.")
            continue
        if lastmod > today:
            errors.append(f"Sitemap entry {location} has a future lastmod date: {lastmod_text}.")

    expected = set(INDEXABLE_PAGES.values())
    duplicates = sorted(url for url, count in Counter(locations).items() if count > 1)
    for url in duplicates:
        errors.append(f"Duplicate sitemap URL: {url}")
    for url in sorted(expected.difference(locations)):
        errors.append(f"Indexable public page is missing from sitemap.xml: {url}")
    for url in sorted(set(locations).difference(expected)):
        errors.append(f"sitemap.xml contains an unexpected Main public URL: {url}")


def validate_robots(errors: list[str]) -> None:
    if not ROBOTS.exists():
        errors.append("robots.txt is missing.")
        return
    directives = [
        line.strip()
        for line in ROBOTS.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    lowered = [line.lower() for line in directives]
    if lowered.count("user-agent: *") != 1:
        errors.append("robots.txt must contain exactly one global 'User-agent: *' directive.")
    if lowered.count("allow: /") != 1:
        errors.append("robots.txt must explicitly allow the Main public site root exactly once.")
    if any(line.startswith("disallow:") for line in lowered):
        errors.append("Main robots.txt must not block the intentionally public website with Disallow directives.")
    sitemap_directives = [line for line in directives if line.lower().startswith("sitemap:")]
    expected = f"Sitemap: {CANONICAL_SITEMAP_URL}"
    if sitemap_directives != [expected]:
        errors.append(f"robots.txt must publish exactly {expected!r}; found {sitemap_directives!r}.")


def main() -> int:
    errors: list[str] = []
    expected_public_pages = set(PUBLIC_PAGE_NAMES)
    if not expected_public_pages.issubset(DEPLOYABLE_PATHS):
        missing = sorted(expected_public_pages.difference(DEPLOYABLE_PATHS))
        errors.append("Main page set is not fully included in the deployment allowlist: " + ", ".join(missing))
    parsed_pages = parse_pages(errors)
    validate_references(errors, parsed_pages)
    validate_indexing(errors, parsed_pages)
    validate_page_metadata(errors, parsed_pages)
    validate_sitemap(errors)
    validate_robots(errors)
    return report(errors)


if __name__ == "__main__":
    sys.exit(main())
