from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MobileNavigationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.styles = (ROOT / "css" / "site-v1.1.css").read_text(encoding="utf-8")
        cls.script = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_mobile_navigation_is_hidden_until_opened(self) -> None:
        self.assertIn(".primary-nav { grid-column: 1 / -1; justify-self: stretch; display: none;", self.styles)
        self.assertIn(".primary-nav.is-open { display: flex; }", self.styles)
        self.assertIn(".nav-toggle { display: inline-flex;", self.styles)

    def test_mobile_navigation_and_shell_keep_48px_targets(self) -> None:
        self.assertIn(".primary-nav a { display: inline-flex; min-height: 48px;", self.styles)
        self.assertIn("min-width: 48px; min-height: 48px;", self.styles)
        self.assertIn(".site-footer nav a { min-height: 48px;", self.styles)

    def test_navigation_uses_accessible_expanded_state_and_control_target(self) -> None:
        self.assertIn('aria-expanded="false"', self.index)
        self.assertIn('aria-controls="primary-nav"', self.index)
        self.assertIn("navButton.setAttribute('aria-expanded', String(!open));", self.script)
        self.assertIn("nav.classList.toggle('is-open', !open);", self.script)

    def test_navigation_closes_after_selecting_a_link(self) -> None:
        self.assertIn("if (event.target.closest('a'))", self.script)
        self.assertIn("navButton.setAttribute('aria-expanded', 'false');", self.script)
        self.assertIn("nav.classList.remove('is-open');", self.script)

    def test_narrow_actions_and_grids_collapse_for_touch_readability(self) -> None:
        self.assertIn("@media (max-width: 700px)", self.styles)
        self.assertIn(".principle-grid, .destination-grid, .repo-grid { grid-template-columns: 1fr; }", self.styles)
        self.assertIn("@media (max-width: 440px) { .actions { flex-direction: column; } .button { width: 100%; }", self.styles)


if __name__ == "__main__":
    unittest.main()
