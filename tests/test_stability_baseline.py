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

VERSION_PATH = ROOT / "VERSION"
BASELINE_PATH = ROOT / "docs" / "stability-baseline.md"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class StabilityBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.version = VERSION_PATH.read_text(encoding="utf-8").strip()
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")

    def test_version_is_strict_semver(self) -> None:
        self.assertRegex(self.version, SEMVER_RE)

    def test_baseline_names_canonical_version(self) -> None:
        self.assertIn(f"**{self.version}**", self.baseline)
        self.assertIn("`VERSION` is the canonical machine-readable version source", self.baseline)

    def test_stability_requires_exact_preview_and_production_verification(self) -> None:
        self.assertIn("exact branch-preview deployment verification", self.baseline)
        self.assertIn("exact production deployment verification", self.baseline)
        self.assertIn("A merge alone is not a stable release", self.baseline)

    def test_stability_preserves_governance_boundaries(self) -> None:
        for marker in (
            "repository visibility change",
            "DNS change",
            "creative-rights/publication decision",
            "Third-party platform-mark review",
        ):
            self.assertIn(marker, self.baseline)

    def test_version_metadata_is_repository_only(self) -> None:
        self.assertNotIn("VERSION", PUBLIC_FILES)
        self.assertNotIn("docs/stability-baseline.md", PUBLIC_FILES)

    def test_stable_scope_keeps_glaze_privacy_and_isolated_publication(self) -> None:
        for marker in (
            "Glaze UI validation",
            "no analytics or tracking",
            "isolated `dist/` publication",
        ):
            self.assertIn(marker, self.baseline)


if __name__ == "__main__":
    unittest.main()
