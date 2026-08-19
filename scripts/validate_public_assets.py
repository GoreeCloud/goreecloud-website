#!/usr/bin/env python3
"""Fail closed on GoreeCloud website public creative-asset boundaries."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_ASSET_FILES  # noqa: E402

EXPECTED_ASSETS = (
    "assets/favicon.svg",
    "assets/goreecloud-icon.png",
    "assets/social-preview.png",
)
FORBIDDEN_PREFIXES = ("assets/platform/", "assets/services/")
FORBIDDEN_CURRENT_TREE_DIRS = (ROOT / "assets" / "platform", ROOT / "assets" / "services")
EXPECTED_PLATFORM_MARKS = {"PX", "DE", "DK", "NB", "AG", "CA", "GN", "BZ", "UK", "GM", "GS"}


class PlatformParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_platform = False
        self.platform_depth = 0
        self.third_party_images: list[str] = []
        self.marks: list[str] = []
        self._capture_mark = False

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "section" and attrs.get("id") == "platform":
            self.in_platform = True
            self.platform_depth = 1
            return
        if self.in_platform and tag == "section":
            self.platform_depth += 1
        if not self.in_platform:
            return
        if tag == "img":
            src = attrs.get("src", "")
            if src.startswith(FORBIDDEN_PREFIXES):
                self.third_party_images.append(src)
        classes = set(attrs.get("class", "").split())
        if tag in {"a", "span"} and "platform-native-mark" in classes:
            self._capture_mark = True

    def handle_endtag(self, tag: str) -> None:
        if self._capture_mark and tag in {"a", "span"}:
            self._capture_mark = False
        if self.in_platform and tag == "section":
            self.platform_depth -= 1
            if self.platform_depth <= 0:
                self.in_platform = False

    def handle_data(self, data: str) -> None:
        if self.in_platform and self._capture_mark:
            value = data.strip()
            if value:
                self.marks.append(value)


def main() -> int:
    errors: list[str] = []
    if tuple(PUBLIC_ASSET_FILES) != EXPECTED_ASSETS:
        errors.append(f"PUBLIC_ASSET_FILES must remain exactly {EXPECTED_ASSETS!r}; found {tuple(PUBLIC_ASSET_FILES)!r}.")

    for path in PUBLIC_ASSET_FILES:
        if path.startswith(FORBIDDEN_PREFIXES):
            errors.append(f"Third-party artwork must not be deployable: {path}")

    for directory in FORBIDDEN_CURRENT_TREE_DIRS:
        if directory.exists():
            errors.append(f"Retired third-party artwork directory must be absent from the current tree: {directory.relative_to(ROOT)}")

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = PlatformParser()
    parser.feed(index)
    if parser.third_party_images:
        errors.append(f"Platform section still references third-party artwork: {sorted(parser.third_party_images)!r}")
    if set(parser.marks) != EXPECTED_PLATFORM_MARKS:
        errors.append(f"Platform neutral marks drifted: expected {sorted(EXPECTED_PLATFORM_MARKS)!r}, found {sorted(set(parser.marks))!r}.")

    inventory = (ROOT / "docs/public-asset-inventory.md").read_text(encoding="utf-8")
    for marker in (
        "third-party artwork removed from the public artifact and current source tree",
        "No current-tree path under `assets/platform/` or `assets/services/` remains",
        "final human reachable-history/contextual-disclosure review",
    ):
        if marker not in inventory:
            errors.append(f"Public asset inventory is missing required boundary text: {marker!r}")

    if errors:
        print("Public creative-asset validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Public creative-asset validation passed: only GoreeCloud-owned artwork remains deployable and retired third-party artwork is absent from the current tree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
