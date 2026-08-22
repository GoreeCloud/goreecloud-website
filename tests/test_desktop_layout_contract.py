#!/usr/bin/env python3
"""Regression coverage for the GoreeCloud website desktop layout contract."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLISH_PATH = ROOT / "css" / "glaze-polish.css"
CONFORMANCE_PATH = ROOT / "docs" / "glaze-ui-conformance.md"
RENDER_VALIDATOR_PATH = ROOT / "scripts" / "validate_desktop_rendering.py"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "validate.yml"


class DesktopLayoutContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.polish = POLISH_PATH.read_text(encoding="utf-8")
        cls.conformance = CONFORMANCE_PATH.read_text(encoding="utf-8")
        cls.render_validator = RENDER_VALIDATOR_PATH.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_expanded_desktop_contract_is_explicit(self) -> None:
        for marker in (
            "@media (min-width:1024px)",
            "--glaze-content-max:1280px",
            "var(--glaze-gutter-expanded)",
            "grid-template-columns:minmax(0,1.08fr) minmax(420px,.92fr)",
            ".hero-card{min-height:480px}",
        ):
            self.assertIn(marker, self.polish)

    def test_wide_desktop_contract_is_explicit(self) -> None:
        for marker in (
            "@media (min-width:1440px)",
            "--glaze-content-max:1480px",
            "var(--glaze-gutter-wide)",
            "grid-template-columns:repeat(4,minmax(0,1fr))",
            ".platform-card{flex-basis:calc((100% - 3rem)/4)}",
        ):
            self.assertIn(marker, self.polish)

    def test_real_browser_rendering_preflight_is_connected(self) -> None:
        for marker in (
            'choices=("branch-preview", "production")',
            'CHROMEWEBDRIVER',
            '"/goog/cdp/execute"',
            'prefers-reduced-motion',
            'prefers-contrast',
            '"/screenshot"',
            'horizontal overflow',
        ):
            self.assertIn(marker, self.render_validator)

        for command in (
            "python scripts/validate_desktop_rendering.py --target branch-preview",
            "python scripts/validate_desktop_rendering.py --target production",
        ):
            self.assertIn(command, self.workflow)

    def test_desktop_contract_preserves_acceptance_boundary(self) -> None:
        for marker in (
            "purpose-built desktop compositions",
            "1280 × 900",
            "1600 × 1000",
            "Manual visual acceptance",
            "requires representative Expanded and Wide manual browser review",
        ):
            self.assertIn(marker, self.conformance)


if __name__ == "__main__":
    unittest.main()
