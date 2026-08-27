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

    def test_hero_platform_identities_are_unique_and_complete(self) -> None:
        self.assertEqual(self.homepage.count('>Everkeep</span>'), 1)
        self.assertEqual(self.homepage.count('>GoreeCloud Mesh</span>'), 1)
        self.assertEqual(self.homepage.count('>GoreeCloud Identity</span>'), 1)
        self.assertIn(
            "Design • Privacy • Security • Resilience • Coordination • Identity",
            self.homepage,
        )

    def test_goreecloud_ai_replaces_retired_front_ends_in_roadmap(self) -> None:
        self.assertIn('data-roadmap="goreecloud-ai"', self.homepage)
        self.assertIn('<h3>GoreeCloud AI</h3>', self.homepage)
        self.assertIn('src="assets/suite/ai.svg"', self.homepage)
        self.assertNotIn("Open WebUI", self.homepage)
        self.assertNotIn("AnythingLLM", self.homepage)
        self.assertIn("Ollama local model runtime", self.homepage)
        self.assertIn("Controlled web research through GoreeCloud Search", self.homepage)

    def test_suite_uses_manifest_owned_icons(self) -> None:
        self.assertIn('data-suite-app="ai"', self.homepage)
        self.assertIn('data-suite-app="browser"', self.homepage)
        self.assertIn('data-suite-app="music"', self.homepage)
        self.assertNotIn("goreecloud-artwork-pending.svg", self.homepage)


if __name__ == "__main__":
    unittest.main()
