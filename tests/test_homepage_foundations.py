from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CONTRACT = ROOT / "docs" / "homepage-foundations-integration.md"


class HomepageFoundationsContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = INDEX.read_text(encoding="utf-8")
        self.contract = CONTRACT.read_text(encoding="utf-8")

    def test_homepage_exposes_all_three_foundations(self) -> None:
        expected = {
            "Glaze UI": "https://design.goreecloud.com/",
            "Privacy Shield": "https://privacy.goreecloud.com/",
            "Wardveil Security": "https://security.goreecloud.com/",
        }
        for label, url in expected.items():
            with self.subTest(label=label):
                self.assertIn(f'href="{url}"', self.index)
                self.assertIn(f'>{label}</a>', self.index)

    def test_homepage_keeps_scopes_separate(self) -> None:
        self.assertIn('aria-label="GoreeCloud platform foundations"', self.index)
        self.assertIn('Design • Privacy • Security', self.index)
        self.assertIn('<strong>Glaze UI</strong> design', self.index)
        self.assertIn('<strong>Privacy Shield</strong> privacy', self.index)
        self.assertIn('<strong>Wardveil Security</strong> security', self.index)

    def test_contract_preserves_authority_boundaries(self) -> None:
        self.assertIn("design and interaction authority", self.contract)
        self.assertIn("privacy and privacy-control identity", self.contract)
        self.assertIn("security and protection identity", self.contract)
        self.assertIn("must not imply that Privacy Shield and Wardveil are the same authority", self.contract)
        self.assertIn("must not imply", self.contract)
        self.assertIn("blanket Wardveil protection assurance", self.contract)
        self.assertIn("unverified Privacy Shield enforcement runtime", self.contract)


if __name__ == "__main__":
    unittest.main()
