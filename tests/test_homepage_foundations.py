from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CONTRACT = ROOT / "docs" / "homepage-foundations-integration.md"


class HomepageFoundationsContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = INDEX.read_text(encoding="utf-8")
        self.contract = CONTRACT.read_text(encoding="utf-8")

    def test_homepage_exposes_current_public_authority_destinations(self) -> None:
        expected = {
            "Glaze UI": "https://design.goreecloud.com/",
            "Privacy Shield": "https://privacy.goreecloud.com/",
            "Wardveil Security": "https://security.goreecloud.com/",
        }
        for label, url in expected.items():
            with self.subTest(label=label):
                self.assertIn(f'href="{url}"', self.index)
                self.assertIn(f"<h3>{label}</h3>", self.index)

    def test_homepage_keeps_seven_integral_systems_explicit_and_scoped(self) -> None:
        expected = {
            "GoreeCloud Manager": "Management and operational visibility",
            "Glaze UI": "Design and interaction",
            "Privacy Shield": "Privacy and data use",
            "Wardveil Security": "Security and trust",
            "Everkeep": "Continuity and recovery",
            "GoreeCloud Mesh": "Coordination and capability exchange",
            "GoreeCloud Identity": "Identity and authentication",
        }
        for system, role in expected.items():
            with self.subTest(system=system):
                self.assertIn(f"<strong>{system}</strong><span>{role}</span>", self.index)
        self.assertIn("seven Integral Platform Systems", self.index)
        self.assertIn("A product does not gain conformance merely because it displays a logo or names an integration.", self.index)

    def test_homepage_keeps_authority_out_of_hero_marketing_claims(self) -> None:
        hero = self.index.split('</section>', 1)[0]
        self.assertIn("Development reality:", hero)
        self.assertNotIn("Protected by Wardveil", hero)
        self.assertNotIn("Privacy Shield accepted", hero)
        self.assertNotIn("GLAZE-conformant", hero)

    def test_historical_contract_still_preserves_core_authority_separation(self) -> None:
        self.assertIn("design and interaction authority", self.contract)
        self.assertIn("privacy and privacy-control identity", self.contract)
        self.assertIn("security and protection identity", self.contract)
        self.assertIn("must not imply that Privacy Shield and Wardveil are the same authority", self.contract)
        self.assertIn("blanket Wardveil protection assurance", self.contract)
        self.assertIn("unverified Privacy Shield enforcement runtime", self.contract)


if __name__ == "__main__":
    unittest.main()
