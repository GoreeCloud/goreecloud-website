#!/usr/bin/env python3
"""Protect rebuilt GLAZE V1.1 theme-aware surfaces from fallback regressions."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE_CSS = (ROOT / "css" / "site-v1.1.css").read_text(encoding="utf-8")
THEME_INIT = (ROOT / "js" / "theme-init.js").read_text(encoding="utf-8")
MAIN_JS = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


class ThemeSurfaceContractTests(unittest.TestCase):
    def test_site_composition_consumes_v11_tokens_with_safe_fallbacks(self) -> None:
        for marker in (
            "var(--glz1-line,",
            "var(--glz1-text-primary,",
            "var(--glz1-text-secondary,",
            "var(--glz1-canvas,",
            "var(--glz1-base,",
            "var(--glz1-raised,",
            "var(--glz1-glaze-blue,",
            "var(--glz1-focus,",
        ):
            self.assertIn(marker, SITE_CSS)
        self.assertNotIn("--glaze-surface", SITE_CSS)
        self.assertNotIn("--surface-glaze", SITE_CSS)

    def test_pages_declare_current_v11_appearance_contract(self) -> None:
        self.assertIn('data-glaze-version="1.1"', INDEX)
        self.assertIn('name="goreecloud-glaze-ui" content="1.1.0"', INDEX)
        self.assertIn('/css/glaze-v1/glaze-v1.1.0.css', INDEX)
        self.assertIn('name="color-scheme" content="dark light"', INDEX)

    def test_early_theme_restore_uses_v11_appearance_attribute(self) -> None:
        self.assertIn("const key = 'goreecloud-appearance';", THEME_INIT)
        self.assertIn("localStorage.getItem(key)", THEME_INIT)
        self.assertIn("root.dataset.glzAppearance = value;", THEME_INIT)
        self.assertIn("delete root.dataset.glzAppearance;", THEME_INIT)

    def test_shared_control_cycles_system_light_and_dark_without_cookie_state(self) -> None:
        self.assertIn("const modes = ['system', 'light', 'dark'];", MAIN_JS)
        self.assertIn("localStorage.removeItem(key)", MAIN_JS)
        self.assertIn("localStorage.setItem(key, mode)", MAIN_JS)
        self.assertNotIn("document.cookie", MAIN_JS)
        self.assertNotIn("document.cookie", THEME_INIT)

    def test_accessibility_effect_fallbacks_remain_present(self) -> None:
        for marker in (
            "@media (prefers-reduced-motion: reduce)",
            "@media (prefers-reduced-transparency: reduce)",
            "@media (forced-colors: active)",
        ):
            self.assertIn(marker, SITE_CSS)


if __name__ == "__main__":
    unittest.main()
