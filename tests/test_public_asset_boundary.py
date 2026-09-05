#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import (  # noqa: E402
    PUBLIC_ASSET_FILES,
    RETIRED_SOURCE_ONLY_ASSET_FILES,
    SOURCE_ONLY_ASSET_FILES,
)


class OfficialArtworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "docs/visual-identity-sources.json").read_text(encoding="utf-8"))

    def test_placeholders_are_removed(self):
        for marker in (
            'class="service-icon"',
            "platform-native-mark",
            "social-letter",
            "neutral Glaze UI letter marks instead of third-party logo artwork",
        ):
            self.assertNotIn(marker, self.index)

    def test_canonical_goreecloud_logo_is_visible_and_is_only_deployable_identity_artwork(self):
        self.assertEqual(PUBLIC_ASSET_FILES, ("assets/goreecloud-logo.svg",))
        self.assertGreaterEqual(self.index.count("assets/goreecloud-logo.svg"), 3)

    def test_only_text_fallback_when_artwork_missing(self):
        for record in self.manifest["assets"]:
            if record.get("official_artwork_exists") is False:
                self.assertEqual(record.get("fallback"), "text-only")

    def test_source_only_and_retired_identity_artwork_stays_out_of_rebuilt_main(self):
        for path in (*SOURCE_ONLY_ASSET_FILES, *RETIRED_SOURCE_ONLY_ASSET_FILES):
            with self.subTest(path=path):
                self.assertNotIn(path, self.index)

    def test_retired_social_card_composition_does_not_return(self):
        for name in ("instagram", "pinterest", "threads", "tiktok", "youtube", "x", "reddit", "github"):
            self.assertNotIn(f"assets/social/{name}.ico", self.index)
        self.assertNotIn("social-preview.png", self.index)


if __name__ == "__main__":
    unittest.main()
