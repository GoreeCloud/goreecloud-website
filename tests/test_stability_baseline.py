#!/usr/bin/env python3
"""Regression coverage for GoreeCloud website stable-version metadata."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_FILES  # noqa: E402
from glaze_ui_2 import GLAZE_PROMOTION_REVISION, GLAZE_VERSION  # noqa: E402

VERSION_PATH = ROOT / "VERSION"
BASELINE_PATH = ROOT / "docs" / "stability-baseline.md"
GLAZE_CONFORMANCE_PATH = ROOT / "docs" / "glaze-ui-conformance.md"
README_PATH = ROOT / "README.md"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class StabilityBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.version = VERSION_PATH.read_text(encoding="utf-8").strip()
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.glaze_conformance = GLAZE_CONFORMANCE_PATH.read_text(encoding="utf-8")
        cls.readme = README_PATH.read_text(encoding="utf-8")

    def test_version_is_current_strict_semver(self) -> None:
        self.assertRegex(self.version, SEMVER_RE)
        self.assertEqual(self.version, "5.24.0")

    def test_baseline_names_canonical_version(self) -> None:
        self.assertIn(f"**{self.version}**", self.baseline)
        self.assertIn("`VERSION` is the canonical machine-readable version source", self.baseline)

    def test_readme_tracks_current_release_state(self) -> None:
        self.assertIn(f"Website package: **v{self.version}**", self.readme)
        self.assertIn("Glaze UI 2.0.0 Stable", self.readme)
        self.assertIn("56 repositories — 40 public, 16 private", self.readme)
        self.assertIn("10 active destinations", self.readme)
        self.assertIn("GoreeCloud/goreecloud-branding-assets", self.readme)

    def test_stability_requires_exact_preview_and_production_verification(self) -> None:
        self.assertIn("exact branch-preview deployment verification", self.baseline)
        self.assertIn("exact production deployment verification", self.baseline)
        self.assertIn("A merge alone is not a stable release", self.baseline)

    def test_stability_records_current_portfolio_and_platform_systems(self) -> None:
        for marker in (
            "56 repositories: 40 public, 16 private, across 13 functional groups",
            "10 active production destinations",
            "GoreeCloud Identity",
            "Identity Center",
            "Glaze UI 2.1 remains Candidate",
            "Facet",
        ):
            self.assertIn(marker, self.baseline)

    def test_stability_rejects_obsolete_current_state(self) -> None:
        for stale in (
            "30 repository / 23 public / 7 private",
            "Glaze UI 1.1.0 using the exact canonical source revision",
            "current Stable production target for GoreeCloud-controlled user-facing applications.\n\nGlaze UI 1.5.0",
            "goreecloud-logo` repository artwork source",
        ):
            self.assertNotIn(stale, self.baseline)

    def test_stability_preserves_governance_boundaries(self) -> None:
        for marker in (
            "repository visibility change",
            "DNS change",
            "creative-rights/publication decision",
            "final human reachable-history/contextual-disclosure review",
        ):
            self.assertIn(marker, self.baseline)

    def test_version_metadata_is_repository_only(self) -> None:
        self.assertNotIn("VERSION", PUBLIC_FILES)
        self.assertNotIn("docs/stability-baseline.md", PUBLIC_FILES)
        self.assertNotIn("docs/glaze-ui-conformance.md", PUBLIC_FILES)

    def test_scope_preserves_static_privacy_and_current_glaze_boundaries(self) -> None:
        for marker in (
            "Glaze UI 2.0.0 Stable",
            "Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze",
            "48px minimum general interaction targets",
            "reduced-motion and reduced-transparency",
            "privacy-preserving static browser surfaces",
            "isolated Cloudflare Pages publication artifact",
        ):
            self.assertIn(marker, self.baseline)

    def test_glaze_conformance_records_current_target(self) -> None:
        for marker in (
            f"Target Glaze UI version: **{GLAZE_VERSION}**",
            GLAZE_PROMOTION_REVISION,
            "GoreeCloud/goreecloud-glaze-ui",
            "Glaze UI 2.0.0 Stable web contract prepared",
            "same-origin Glaze UI 2.0.0 web layer",
            "48px interaction targets",
            "Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze",
            "Reduced-motion behavior",
            "Reduced-transparency preferences",
            "No production Glaze UI exception is recorded",
        ):
            self.assertIn(marker, self.glaze_conformance)


if __name__ == "__main__":
    unittest.main()
