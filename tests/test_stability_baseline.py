#!/usr/bin/env python3
"""Regression coverage for GoreeCloud Website accepted-vs-candidate stability metadata."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_FILES  # noqa: E402
from glaze_v1 import GLAZE_SOURCE_REVISION, GLAZE_VERSION  # noqa: E402

VERSION_PATH = ROOT / "VERSION"
BASELINE_PATH = ROOT / "docs" / "stability-baseline.md"
GLAZE_CONFORMANCE_PATH = ROOT / "docs" / "glaze-ui-conformance.md"
README_PATH = ROOT / "README.md"
PORTFOLIO_PATH = ROOT / "docs" / "repository-portfolio.json"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class StabilityBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.version = VERSION_PATH.read_text(encoding="utf-8").strip()
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.glaze_conformance = GLAZE_CONFORMANCE_PATH.read_text(encoding="utf-8")
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.portfolio = json.loads(PORTFOLIO_PATH.read_text(encoding="utf-8"))

    def test_version_remains_strict_semver_and_not_implicitly_promoted(self) -> None:
        self.assertRegex(self.version, SEMVER_RE)
        self.assertEqual(self.version, "5.24.0")
        self.assertIn("accepted website package remains **5.24.0**", self.baseline)
        self.assertIn("not an accepted replacement for 5.24.0", self.baseline)

    def test_readme_identifies_current_branch_as_development(self) -> None:
        self.assertIn("## Current development state", self.readme)
        self.assertIn("This repository is in **Development**", self.readme)
        self.assertIn("GLAZE UI V1.1 / 1.1.0", self.readme)
        self.assertIn(GLAZE_SOURCE_REVISION, self.readme)
        self.assertIn("temporary, bounded consumer-build workaround", self.readme)
        self.assertIn("does **not** make the Website GLAZE-conformant", self.readme)

    def test_stability_baseline_uses_current_v11_candidate_target(self) -> None:
        self.assertIn(f"GLAZE UI V1.1 / {GLAZE_VERSION}", self.baseline)
        self.assertIn(GLAZE_SOURCE_REVISION, self.baseline)
        self.assertIn("known import-closure defect", self.baseline)
        self.assertIn("not GLAZE consumer-conformance evidence", self.baseline)
        self.assertIn("Glaze UI 2.x website-adoption records remain historical evidence only", self.baseline)

    def test_stability_records_current_verified_repository_inventory(self) -> None:
        counts = self.portfolio["counts"]
        self.assertEqual(counts, {"total": 68, "public": 65, "private": 3, "functional_groups": 15})
        for marker in (
            "**68 repositories total**",
            "**65 public**",
            "**3 private**",
            "**15 functional groups**",
        ):
            self.assertIn(marker, self.baseline)
        self.assertNotIn("57 repositories: 40 public, 17 private", self.baseline)

    def test_stability_records_all_seven_integral_platform_systems(self) -> None:
        for marker in (
            "GoreeCloud Manager",
            "Glaze UI",
            "Privacy Shield",
            "Wardveil Security",
            "Everkeep",
            "GoreeCloud Mesh",
            "GoreeCloud Identity",
        ):
            self.assertIn(marker, self.baseline)
        self.assertNotIn("The six substantive GoreeCloud platform systems", self.baseline)

    def test_stability_requires_exact_preview_human_and_production_verification(self) -> None:
        for marker in (
            "branch-preview deployment verification",
            "representative human mobile visual/interaction review",
            "Automated Chrome evidence does not replace this gate",
            "production deployment verification",
            "A merge alone is not a stable release",
        ):
            self.assertIn(marker, self.baseline)

    def test_stability_preserves_publication_and_cloudflare_boundaries(self) -> None:
        for marker in (
            "labs.goreecloud.com",
            "proposed technical website namespace",
            "noindex,nofollow",
            "repository visibility change",
            "DNS change",
            "creative-rights/publication decision",
            "merge or production release",
        ):
            self.assertIn(marker, self.baseline)

    def test_version_and_candidate_records_remain_repository_only(self) -> None:
        self.assertNotIn("VERSION", PUBLIC_FILES)
        self.assertNotIn("docs/stability-baseline.md", PUBLIC_FILES)
        self.assertNotIn("docs/glaze-ui-conformance.md", PUBLIC_FILES)
        self.assertNotIn("docs/repository-portfolio.json", PUBLIC_FILES)

    def test_glaze_conformance_matches_baseline_and_pending_state(self) -> None:
        for marker in (
            f"GLAZE UI V1.1 / {GLAZE_VERSION}",
            GLAZE_SOURCE_REVISION,
            "Known immutable Stable-source defect",
            "not GLAZE consumer-conformance evidence",
            "Exact rendered consumer acceptance remains pending",
            "Production acceptance remains pending",
            "48-pixel minimum shell-control target",
            "legacy satellite sites",
        ):
            self.assertIn(marker, self.glaze_conformance)


if __name__ == "__main__":
    unittest.main()
