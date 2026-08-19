#!/usr/bin/env python3
"""Regression tests for the GoreeCloud public creative-asset boundary."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_ASSET_FILES  # noqa: E402


class PublicAssetBoundaryTests(unittest.TestCase):
    def test_only_goreecloud_owned_artwork_is_deployable(self) -> None:
        self.assertEqual(
            tuple(PUBLIC_ASSET_FILES),
            ("assets/favicon.svg", "assets/goreecloud-icon.png", "assets/social-preview.png"),
        )

    def test_third_party_asset_directories_are_not_deployable(self) -> None:
        self.assertFalse(any(path.startswith("assets/platform/") for path in PUBLIC_ASSET_FILES))
        self.assertFalse(any(path.startswith("assets/services/") for path in PUBLIC_ASSET_FILES))

    def test_retired_third_party_asset_directories_are_absent_from_current_tree(self) -> None:
        self.assertFalse((ROOT / "assets" / "platform").exists())
        self.assertFalse((ROOT / "assets" / "services").exists())

    def test_homepage_does_not_reference_third_party_artwork(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("assets/platform/", index)
        self.assertNotIn("assets/services/", index)
        self.assertIn("neutral Glaze UI letter marks instead of third-party logo artwork", index)


if __name__ == "__main__":
    unittest.main()
