#!/usr/bin/env python3
"""Validate rebuilt homepage identity, canonical metadata, and public navigation semantics."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CANONICAL_URL = "https://www.goreecloud.com/"
EXPECTED_TITLE = "GoreeCloud — Owner-Controlled Computing"
CANONICAL_LOGO = "/assets/goreecloud-logo.svg"
REQUIRED_PUBLIC_DESTINATIONS = {
    "https://suite.goreecloud.com/",
    "https://projects.goreecloud.com/",
    "https://design.goreecloud.com/",
    "https://privacy.goreecloud.com/",
    "https://security.goreecloud.com/",
}
REQUIRED_POLICY_LINKS = {"/privacy.html", "/security.html"}
RETIRED_COMPOSITION = {
    "Expanding the platform",
    "Home Assistant",
    "Frigate",
    "platform-logo-link",
    "platform-native-mark",
    "assets/platform/proxmox.svg",
    "assets/platform/docker.png",
    "assets/platform/netbird.svg",
    "assets/platform/adguard-home.svg",
    "assets/platform/caddy.svg",
    "assets/platform/uptime-kuma.svg",
}


class HomepageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta_names: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.main_attrs: dict[str, str] | None = None
        self.navs: list[dict[str, str]] = []
        self._in_title = False
        self.title_parts: list[str] = []

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and attrs.get("name"):
            self.meta_names[attrs["name"]] = attrs.get("content", "")
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "a":
            self.anchors.append(attrs)
        elif tag == "img":
            self.images.append(attrs)
        elif tag == "main" and attrs.get("id") == "main":
            self.main_attrs = attrs
        elif tag == "nav":
            self.navs.append(attrs)

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False


def main() -> int:
    errors: list[str] = []
    if not INDEX.exists():
        return report(["index.html is missing."])

    source = INDEX.read_text(encoding="utf-8")
    parser = HomepageParser()
    parser.feed(source)

    if parser.main_attrs is None:
        errors.append("Homepage must contain <main id=\"main\"> for the skip link target.")
    elif parser.main_attrs.get("tabindex") != "-1":
        errors.append("Homepage main skip-link target must use tabindex=\"-1\" for reliable programmatic focus.")

    if parser.title != EXPECTED_TITLE:
        errors.append(f"Homepage title must be {EXPECTED_TITLE!r}, found {parser.title!r}.")
    if not parser.meta_names.get("description", "").strip():
        errors.append("Homepage must publish a non-empty meta description.")
    if parser.meta_names.get("robots") != "index,follow,max-image-preview:large":
        errors.append("Homepage robots metadata must remain index,follow,max-image-preview:large.")
    if parser.meta_names.get("author") != "GoreeCloud":
        errors.append("Homepage must identify GoreeCloud with meta name=\"author\".")
    if parser.meta_names.get("application-name") != "GoreeCloud":
        errors.append("Homepage must publish application-name=GoreeCloud.")
    if parser.meta_names.get("goreecloud-glaze-ui") != "1.1.0":
        errors.append("Homepage must identify the current Website GLAZE UI source target as 1.1.0.")

    canonical_links = [link for link in parser.links if "canonical" in link.get("rel", "").split()]
    if len(canonical_links) != 1 or canonical_links[0].get("href") != CANONICAL_URL:
        errors.append(f"Homepage must publish exactly one canonical link to {CANONICAL_URL}.")

    icon_links = [link for link in parser.links if "icon" in link.get("rel", "").split()]
    canonical_icons = [link for link in icon_links if link.get("href") == CANONICAL_LOGO]
    if len(canonical_icons) != 1 or canonical_icons[0].get("type") != "image/svg+xml":
        errors.append("Homepage must explicitly publish the canonical GoreeCloud SVG icon.")

    hrefs = {anchor.get("href", "") for anchor in parser.anchors}
    for href in sorted(REQUIRED_PUBLIC_DESTINATIONS):
        if href not in hrefs:
            errors.append(f"Homepage is missing official public destination: {href}")
    for href in sorted(REQUIRED_POLICY_LINKS):
        if href not in hrefs:
            errors.append(f"Homepage must directly expose policy link: {href}")
        if not (ROOT / href.lstrip("/")).exists():
            errors.append(f"Homepage public policy target is missing: {href}")

    if not any(nav.get("aria-label") == "Primary" for nav in parser.navs):
        errors.append("Homepage must retain a labeled Primary navigation landmark.")
    if not any(nav.get("aria-label") == "Footer" for nav in parser.navs):
        errors.append("Homepage must retain a labeled Footer navigation landmark.")

    logo_sources = [image.get("src", "") for image in parser.images]
    if logo_sources.count(CANONICAL_LOGO) < 3:
        errors.append("Homepage must use the canonical GoreeCloud master mark across header, hero, and footer identity surfaces.")
    unexpected_images = sorted(set(logo_sources) - {CANONICAL_LOGO})
    if unexpected_images:
        errors.append("Rebuilt homepage must not reintroduce noncanonical product/platform artwork: " + ", ".join(unexpected_images))

    for marker in sorted(RETIRED_COMPOSITION):
        if marker in source:
            errors.append(f"Retired homepage composition marker returned: {marker}")

    if "Publication pending" not in source or "Source: sites/labs" not in source:
        errors.append("Homepage must keep the new combined product center explicitly publication-pending until its domain is verified.")
    if "labs.goreecloud.com" in hrefs:
        errors.append("Homepage must not link to the proposed Labs hostname before its public-domain activation is verified.")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print("Public semantics validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Public semantics validation passed: rebuilt canonical identity, policies, official destinations, and publication boundaries are intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
