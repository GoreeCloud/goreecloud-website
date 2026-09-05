from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HomepageCurrentStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "css" / "site-v1.1.css").read_text(encoding="utf-8")

    def test_rebuilt_owner_controlled_hero_is_current(self) -> None:
        self.assertIn("Your cloud should belong to you.", self.homepage)
        self.assertIn("Owner-controlled • Private by design • Built to endure", self.homepage)
        self.assertIn("Development reality:", self.homepage)
        self.assertNotIn("Expanding the platform", self.homepage)
        self.assertNotIn("Private • Self-hosted • Recoverable", self.homepage)

    def test_homepage_has_four_durable_principles(self) -> None:
        for label in ("Ownership", "Privacy", "Portability", "Recoverability"):
            with self.subTest(label=label):
                self.assertIn(f"<h3>{label}</h3>", self.homepage)
        self.assertEqual(self.homepage.count('class="card glz1-raised"'), 4)

    def test_main_homepage_is_a_clear_six_destination_front_door(self) -> None:
        self.assertEqual(self.homepage.count("destination-card"), 6)
        for destination in (
            "GoreeCloud Suite",
            "GoreeCloud Projects",
            "Home, AI &amp; Developer Systems",
            "Glaze UI",
            "Privacy Shield",
            "Wardveil Security",
        ):
            with self.subTest(destination=destination):
                self.assertIn(destination, self.homepage)
        self.assertIn("Publication pending", self.homepage)
        self.assertIn("Source: sites/labs", self.homepage)
        self.assertNotIn("https://labs.goreecloud.com/", self.homepage)

    def test_homepage_exposes_all_seven_integral_platform_systems(self) -> None:
        systems = (
            "GoreeCloud Manager",
            "Glaze UI",
            "Privacy Shield",
            "Wardveil Security",
            "Everkeep",
            "GoreeCloud Mesh",
            "GoreeCloud Identity",
        )
        for system in systems:
            with self.subTest(system=system):
                self.assertIn(f"<strong>{system}</strong>", self.homepage)
        self.assertIn("seven Integral Platform Systems", self.homepage)
        self.assertNotIn("six substantive platform systems", self.homepage)

    def test_homepage_keeps_full_portfolios_out_of_main_composition(self) -> None:
        self.assertNotIn("data-suite-app=", self.homepage)
        self.assertNotIn("data-capability=", self.homepage)
        self.assertNotIn("data-roadmap=", self.homepage)
        self.assertNotIn("website-preview-browser", self.homepage)

    def test_rebuilt_shell_uses_only_current_v11_site_layers(self) -> None:
        self.assertIn('/css/glaze-v1/glaze-v1.1.0.css', self.homepage)
        self.assertIn('/css/site-v1.1.css', self.homepage)
        self.assertIn('name="goreecloud-glaze-ui" content="1.1.0"', self.homepage)
        self.assertNotIn("homepage-v6.css", self.homepage)
        self.assertNotIn("websites.css", self.homepage)
        self.assertNotIn("glaze-ui-2.1.0", self.homepage)

    def test_responsive_source_contract_matches_rebuilt_grids(self) -> None:
        self.assertIn(".principle-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));", self.styles)
        self.assertIn(".destination-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr));", self.styles)
        self.assertIn("@media (max-width: 980px)", self.styles)
        self.assertIn(".principle-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }", self.styles)
        self.assertIn(".destination-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }", self.styles)
        self.assertIn(".principle-grid, .destination-grid, .repo-grid { grid-template-columns: 1fr; }", self.styles)


if __name__ == "__main__":
    unittest.main()
