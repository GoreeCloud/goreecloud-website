#!/usr/bin/env python3
"""Keep publication classification synchronized with deployable and retained artwork."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import (  # noqa: E402
    PUBLIC_ASSET_FILES,
    PUBLIC_FILES,
    RETIRED_SOURCE_ONLY_ASSET_FILES,
    SOURCE_ONLY_ASSET_FILES,
)

INVENTORY = ROOT / "docs" / "public-asset-inventory.md"


def inventory_section(text: str, heading: str, next_heading: str | None = None) -> str:
    start_marker = f"## {heading}"
    if start_marker not in text:
        raise AssertionError(f"Missing inventory section: {heading}")
    section = text.split(start_marker, 1)[1]
    if next_heading:
        end_marker = f"## {next_heading}"
        if end_marker not in section:
            raise AssertionError(f"Missing inventory section boundary: {next_heading}")
        section = section.split(end_marker, 1)[0]
    return section


def listed_asset_paths(text: str) -> set[str]:
    paths: set[str] = set()
    for match in re.finditer(r"^- `(?P<path>assets/[^`]+)`\s*$", text, re.MULTILINE):
        path = match.group("path")
        if path in paths:
            raise AssertionError(f"Duplicate asset path in inventory section: {path}")
        paths.add(path)
    return paths


def normalize_markdown_text(text: str) -> str:
    # Strip Markdown asterisk emphasis without corrupting underscores in canonical
    # file paths such as scripts/validate_public_assets.py.
    return text.replace("*", "").lower()


class PublicAssetInventoryTests(unittest.TestCase):
    """Prevent current or retained artwork from bypassing publication review."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = INVENTORY.read_text(encoding="utf-8")
        cls.deployable_section = inventory_section(
            cls.text,
            "Deployable artwork",
            "Source-only reviewed artwork",
        )
        cls.source_only_section = inventory_section(
            cls.text,
            "Source-only reviewed artwork",
            "Retired source-only historical/provenance artwork",
        )
        cls.retired_section = inventory_section(
            cls.text,
            "Retired source-only historical/provenance artwork",
            "Non-identity publication preview retained in source",
        )
        cls.preview_section = inventory_section(
            cls.text,
            "Non-identity publication preview retained in source",
            "Publication boundary",
        )

    def test_inventory_exists_but_is_not_deployed(self) -> None:
        self.assertTrue(INVENTORY.is_file())
        self.assertNotIn("docs/public-asset-inventory.md", PUBLIC_FILES)

    def test_inventory_matches_exact_public_asset_allowlist(self) -> None:
        documented = listed_asset_paths(self.deployable_section)
        self.assertEqual(documented, set(PUBLIC_ASSET_FILES))
        self.assertEqual(PUBLIC_ASSET_FILES, ("assets/goreecloud-logo.svg",))

    def test_source_only_inventory_matches_exact_current_source_only_set(self) -> None:
        documented = listed_asset_paths(self.source_only_section)
        expected = set(SOURCE_ONLY_ASSET_FILES)
        self.assertEqual(documented, expected)
        self.assertTrue(expected.isdisjoint(set(PUBLIC_ASSET_FILES)))
        for path in SOURCE_ONLY_ASSET_FILES:
            self.assertNotIn(path, PUBLIC_FILES)

    def test_retired_inventory_matches_exact_retired_set(self) -> None:
        documented = listed_asset_paths(self.retired_section)
        expected = set(RETIRED_SOURCE_ONLY_ASSET_FILES)
        self.assertEqual(documented, expected)
        self.assertTrue(expected.isdisjoint(set(PUBLIC_ASSET_FILES)))
        self.assertTrue(expected.isdisjoint(set(SOURCE_ONLY_ASSET_FILES)))
        for path in RETIRED_SOURCE_ONLY_ASSET_FILES:
            self.assertNotIn(path, PUBLIC_FILES)

    def test_all_classified_identity_files_exist_as_regular_source_files(self) -> None:
        for relative_path in (
            *PUBLIC_ASSET_FILES,
            *SOURCE_ONLY_ASSET_FILES,
            *RETIRED_SOURCE_ONLY_ASSET_FILES,
        ):
            with self.subTest(path=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.is_file())
                self.assertFalse(path.is_symlink())

    def test_social_preview_is_explicitly_non_identity_and_not_deployed(self) -> None:
        self.assertIn("`assets/social-preview.png`", self.preview_section)
        self.assertNotIn("assets/social-preview.png", PUBLIC_FILES)
        self.assertNotIn("assets/social-preview.png", PUBLIC_ASSET_FILES)

    def test_inventory_delegates_detailed_provenance_to_canonical_records(self) -> None:
        normalized = normalize_markdown_text(self.text)
        for marker in (
            "docs/visual-identity-sources.json",
            "suite manifest",
            "source authority",
            "source revision/path",
            "reviewed git blob",
            "scripts/validate_public_assets.py",
        ):
            self.assertIn(marker, normalized)

    def test_inventory_preserves_publication_boundary_language(self) -> None:
        text = normalize_markdown_text(self.text)
        required = (
            "not a license grant",
            "official artwork is required when it exists",
            "identity artwork must be source-traceable before deployment",
            "does not automatically license goreecloud branding or third-party marks",
            "final human reachable-history/contextual-disclosure review",
            "issue #5 remains open",
            "not part of the current public build allowlist",
            "must not be published by the current goreecloud website artifact",
            "repository presence does not make a file deployable",
            "text-only presentation rather than an invented icon",
        )
        for marker in required:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
