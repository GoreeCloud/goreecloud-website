#!/usr/bin/env python3
"""Validate homepage identity, search/social metadata, policy discoverability, and loading semantics."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CANONICAL_URL = "https://www.goreecloud.com/"
SOCIAL_PREVIEW_URL = "https://www.goreecloud.com/assets/social-preview.png"
EXPECTED_TITLE = "GoreeCloud — Privacy-First Personal & Family Cloud"

SOCIAL_PROFILES = {
    "https://instagram.com/goreecloud",
    "https://www.pinterest.com/goreecloud/",
    "https://www.threads.net/@goreecloud",
    "https://www.tiktok.com/@goreecloud",
    "https://x.com/GoreeCloud",
    "https://www.reddit.com/user/goreecloud/",
    "https://github.com/GoreeCloud",
}

EXPECTED_PLATFORM_MARKS = {"PX", "DE", "DK", "NB", "AG", "CA", "GN", "BZ", "UK", "GM", "GS"}
FORBIDDEN_PLATFORM_ASSET_PREFIXES = ("assets/platform/", "assets/services/")


class HomepageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta_names: dict[str, str] = {}
        self.meta_properties: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.main_attrs: dict[str, str] | None = None
        self.footer_nav_attrs: dict[str, str] | None = None
        self.footer_nav_hrefs: set[str] = set()
        self._footer_nav_depth = 0
        self._platform_link_depth = 0
        self._in_title = False
        self._capture_platform_mark = False
        self.title_parts: list[str] = []
        self.platform_images: list[dict[str, str]] = []
        self.platform_marks: list[str] = []

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        classes = set(attrs.get("class", "").split())

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            if attrs.get("name"):
                self.meta_names[attrs["name"]] = attrs.get("content", "")
            if attrs.get("property"):
                self.meta_properties[attrs["property"]] = attrs.get("content", "")
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "main" and attrs.get("id") == "main":
            self.main_attrs = attrs
        elif tag == "nav" and "footer-links" in classes:
            self.footer_nav_attrs = attrs
            self._footer_nav_depth = 1
        elif self._footer_nav_depth:
            self._footer_nav_depth += 1

        if tag == "a":
            self.anchors.append(attrs)
            if self._footer_nav_depth and attrs.get("href"):
                self.footer_nav_hrefs.add(attrs["href"])
            if "platform-logo-link" in classes:
                self._platform_link_depth = 1
        elif self._platform_link_depth:
            self._platform_link_depth += 1

        if tag == "img" and self._platform_link_depth:
            self.platform_images.append(attrs)
        if tag in {"a", "span"} and "platform-native-mark" in classes:
            self._capture_platform_mark = True

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._capture_platform_mark:
            value = data.strip()
            if value:
                self.platform_marks.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if self._capture_platform_mark and tag in {"a", "span"}:
            self._capture_platform_mark = False
        if self._footer_nav_depth:
            self._footer_nav_depth -= 1
        if self._platform_link_depth:
            self._platform_link_depth -= 1


def main() -> int:
    errors: list[str] = []
    if not INDEX.exists():
        errors.append("index.html is missing.")
        return report(errors)

    parser = HomepageParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    if parser.main_attrs is None:
        errors.append("Homepage must contain <main id=\"main\"> for the skip link target.")
    elif parser.main_attrs.get("tabindex") != "-1":
        errors.append("Homepage main skip-link target must use tabindex=\"-1\" for reliable programmatic focus.")

    if parser.title != EXPECTED_TITLE:
        errors.append(f"Homepage title must remain {EXPECTED_TITLE!r}, found {parser.title!r}.")
    if not parser.meta_names.get("description", "").strip():
        errors.append("Homepage must publish a non-empty meta description.")
    if parser.meta_names.get("robots") != "index,follow,max-image-preview:large":
        errors.append("Homepage robots metadata must remain index,follow,max-image-preview:large.")
    if parser.meta_names.get("author") != "GoreeCloud":
        errors.append("Homepage must identify GoreeCloud with meta name=\"author\".")

    canonical_links = [
        link for link in parser.links
        if "canonical" in link.get("rel", "").split()
    ]
    if len(canonical_links) != 1 or canonical_links[0].get("href") != CANONICAL_URL:
        errors.append(f"Homepage must publish exactly one canonical link to {CANONICAL_URL}.")

    expected_og = {
        "og:type": "website",
        "og:locale": "en_US",
        "og:site_name": "GoreeCloud",
        "og:title": EXPECTED_TITLE,
        "og:url": CANONICAL_URL,
        "og:image": SOCIAL_PREVIEW_URL,
        "og:image:type": "image/png",
        "og:image:width": "1200",
        "og:image:height": "630",
    }
    for key, expected in expected_og.items():
        actual = parser.meta_properties.get(key)
        if actual != expected:
            errors.append(f"Homepage {key} must be {expected!r}, found {actual!r}.")

    og_description = parser.meta_properties.get("og:description", "")
    og_image_alt = parser.meta_properties.get("og:image:alt", "")
    if not og_description.strip():
        errors.append("Homepage must publish a non-empty og:description.")
    if not og_image_alt.strip():
        errors.append("Homepage must publish non-empty og:image:alt text.")

    expected_twitter = {
        "twitter:card": "summary_large_image",
        "twitter:site": "@GoreeCloud",
        "twitter:title": EXPECTED_TITLE,
        "twitter:image": SOCIAL_PREVIEW_URL,
    }
    for key, expected in expected_twitter.items():
        actual = parser.meta_names.get(key)
        if actual != expected:
            errors.append(f"Homepage {key} must be {expected!r}, found {actual!r}.")

    if parser.meta_names.get("twitter:description") != og_description:
        errors.append("Homepage twitter:description must stay aligned with og:description.")
    if parser.meta_names.get("twitter:image:alt") != og_image_alt:
        errors.append("Homepage twitter:image:alt must stay aligned with og:image:alt.")

    apple_icons = [
        link for link in parser.links
        if "apple-touch-icon" in link.get("rel", "").split()
    ]
    if not apple_icons or apple_icons[0].get("href") != "assets/goreecloud-icon.png":
        errors.append("Homepage must publish the local GoreeCloud icon as an apple-touch-icon.")

    if parser.footer_nav_attrs is None:
        errors.append("Homepage footer links must be a semantic navigation landmark.")
    elif parser.footer_nav_attrs.get("aria-label") != "Footer navigation":
        errors.append("Homepage footer navigation must use aria-label=\"Footer navigation\".")

    for href in ("privacy.html", "security.html"):
        if href not in parser.footer_nav_hrefs:
            errors.append(f"Homepage footer must link directly to {href}.")
        if not (ROOT / href).exists():
            errors.append(f"Homepage public policy target is missing: {href}.")

    social_anchors = {
        anchor.get("href", ""): anchor
        for anchor in parser.anchors
        if anchor.get("href") in SOCIAL_PROFILES
    }
    missing_social = sorted(SOCIAL_PROFILES.difference(social_anchors))
    for href in missing_social:
        errors.append(f"Official social profile is missing from homepage: {href}")

    for href, anchor in sorted(social_anchors.items()):
        rel = set(anchor.get("rel", "").split())
        if not {"me", "noopener", "noreferrer"}.issubset(rel):
            errors.append(f"Official social profile must use rel=me noopener noreferrer: {href}")

    if parser.platform_images:
        sources = sorted({image.get("src", "(missing src)") for image in parser.platform_images})
        errors.append(f"Platform identity must use neutral Glaze UI marks instead of logo images; found: {', '.join(sources)}")
        for source in sources:
            if source.startswith(FORBIDDEN_PLATFORM_ASSET_PREFIXES):
                errors.append(f"Third-party platform/service artwork must not be browser-loaded: {source}")

    platform_marks = set(parser.platform_marks)
    if platform_marks != EXPECTED_PLATFORM_MARKS:
        missing = sorted(EXPECTED_PLATFORM_MARKS - platform_marks)
        unexpected = sorted(platform_marks - EXPECTED_PLATFORM_MARKS)
        if missing:
            errors.append(f"Expected neutral platform marks are missing: {', '.join(missing)}")
        if unexpected:
            errors.append(f"Unexpected neutral platform marks are present: {', '.join(unexpected)}")
    if len(parser.platform_marks) != len(platform_marks):
        errors.append("Neutral platform marks must not be duplicated.")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print("Public semantics validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Public semantics validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
