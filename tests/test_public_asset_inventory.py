#!/usr/bin/env python3
"""Keep the publication/licensing inventory synchronized with deployable artwork."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_ASSET_FILES, PUBLIC_FILES  # noqa: E402

INVENTORY = ROOT / "docs" / "public-asset-inventory.md"
ASSET_PATH_RE = re.compile(r"`(assets/[A-Za-z0-9_./-]+\.(?:svg|png|jpg|jpeg|webp|gif))`")


class PublicAssetInventoryTests(unittest.TestCase):
    """Prevent deployable artwork from bypassing the pre-publication rights review."""

    def test_inventory_exists_but_is_not_deployed(self) -> None:
        self.assertTrue(INVENTORY.is_file())
        self.assertNotIn("docs/public-asset-inventory.md", PUBLIC_FILES)

    def test_inventory_matches_exact_public_asset_allowlist(self) -> None:
        text = INVENTORY.read_text(encoding="utf-8")
        documented = set(ASSET_PATH_RE.findall(text))
        expected = set(PUBLIC_ASSET_FILES)

        self.assertEqual(
            documented,
            expected,
            "Public asset inventory must exactly match PUBLIC_ASSET_FILES; review licensing/provenance whenever deployable artwork changes.",
        )

        for path in PUBLIC_ASSET_FILES:
            self.assertEqual(
                text.count(f"`{path}`"),
                1,
                f"Deployable asset must appear exactly once in the inventory table: {path}",
            )

    def test_inventory_preserves_publication_boundary_language(self) -> None:
        text = INVENTORY.read_text(encoding="utf-8")
        required = (
            "not a license grant",
            "provenance and rights verification still required",
            "source-code license must not be assumed to relicense third-party marks",
            "Issue #5 remains open",
        )
        for marker in required:
            self.assertIn(marker.lower(), text.lower())


if __name__ == "__main__":
    unittest.main()
