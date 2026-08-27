from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from normalize_homepage import normalize_homepage  # noqa: E402
from render_repository_portfolio import load_manifest, render_public_file  # noqa: E402


class HomepageCurrentStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        rendered = render_public_file("index.html", source, load_manifest(ROOT))
        cls.homepage = normalize_homepage(rendered)

    def test_hero_is_focused_without_platform_system_duplication(self) -> None:
        hero = self.homepage.split("<h1>", 1)[0]
        self.assertIn("Private • Self-hosted • Recoverable", hero)
        for label in (
            "Glaze UI",
            "Privacy Shield",
            "Wardveil Security",
            "Everkeep",
            "GoreeCloud Mesh",
            "GoreeCloud Identity",
        ):
            with self.subTest(label=label):
                self.assertNotIn(label, hero)
        self.assertNotIn('<section class="band" aria-label="Core principles">', self.homepage)

    def test_main_homepage_is_a_website_hub(self) -> None:
        self.assertEqual(self.homepage.count('id="websites"'), 1)
        for domain in (
            "goreecloud.com",
            "suite.goreecloud.com",
            "projects.goreecloud.com",
            "design.goreecloud.com",
            "privacy.goreecloud.com",
            "security.goreecloud.com",
            "roadmap.goreecloud.com",
            "blog.goreecloud.com",
            "archive.goreecloud.com",
        ):
            with self.subTest(domain=domain):
                self.assertIn(domain, self.homepage)
        self.assertEqual(self.homepage.count('class="service-card website-card"'), 9)
        self.assertEqual(self.homepage.count('class="website-preview '), 9)
        self.assertIn('<a href="#websites">Websites</a>', self.homepage)
        self.assertIn('<a href="https://suite.goreecloud.com/">Suite</a>', self.homepage)
        self.assertIn('css/websites.css', self.homepage)
        self.assertIn('css/homepage-v6.css', self.homepage)

    def test_suite_and_capability_cards_moved_off_main_homepage(self) -> None:
        self.assertNotIn('data-suite-app=', self.homepage)
        self.assertNotIn('data-capability=', self.homepage)
        self.assertNotIn('<p class="eyebrow">GoreeCloud Suite</p>', self.homepage)
        self.assertNotIn('<p class="eyebrow">Umbrella Capabilities</p>', self.homepage)

    def test_goreecloud_ai_replaces_retired_front_ends_in_roadmap(self) -> None:
        self.assertIn('data-roadmap="goreecloud-ai"', self.homepage)
        self.assertIn('<h3>GoreeCloud AI</h3>', self.homepage)
        self.assertIn('src="assets/suite/ai.svg"', self.homepage)
        self.assertNotIn("Open WebUI", self.homepage)
        self.assertNotIn("AnythingLLM", self.homepage)
        self.assertIn("Ollama local model runtime", self.homepage)
        self.assertIn("Controlled web research through GoreeCloud Search", self.homepage)


if __name__ == "__main__":
    unittest.main()
