#!/usr/bin/env python3
"""Validate homepage identity, policy discoverability, and loading semantics."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

SOCIAL_PROFILES = {
    "https://instagram.com/goreecloud",
    "https://www.pinterest.com/goreecloud/",
    "https://www.threads.net/@goreecloud",
    "https://www.tiktok.com/@goreecloud",
    "https://x.com/GoreeCloud",
    "https://www.reddit.com/user/goreecloud/",
    "https://github.com/GoreeCloud",
}


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
        self.platform_images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        classes = set(attrs.get("class", "").split())

        if tag == "meta":
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

    def handle_endtag(self, tag: str) -> None:
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

    if parser.meta_names.get("author") != "GoreeCloud":
        errors.append("Homepage must identify GoreeCloud with meta name=\"author\".")
    if parser.meta_names.get("twitter:site") != "@GoreeCloud":
        errors.append("Homepage must identify the official @GoreeCloud account with twitter:site metadata.")
    if parser.meta_properties.get("og:image:type") != "image/png":
        errors.append("Homepage Open Graph image type must remain image/png.")

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

    if len(parser.platform_images) != 10:
        errors.append(f"Expected 10 below-fold platform logo images, found {len(parser.platform_images)}.")
    for image in parser.platform_images:
        src = image.get("src", "(missing src)")
        if image.get("loading") != "lazy":
            errors.append(f"Below-fold platform image must use loading=\"lazy\": {src}")
        if image.get("decoding") != "async":
            errors.append(f"Below-fold platform image must use decoding=\"async\": {src}")

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
