#!/usr/bin/env python3
"""Regression coverage for rebuilt Main, focused repository page, and source inventory separation."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
REPOSITORIES = [repo for group in MANIFEST["groups"] for repo in group["repositories"]]
PUBLIC_REPOSITORIES = {repo["name"] for repo in REPOSITORIES if repo["visibility"] == "public"}
PRIVATE_REPOSITORIES = {repo["name"] for repo in REPOSITORIES if repo["visibility"] == "private"}
PUBLIC_HOME = (ROOT / "index.html").read_text(encoding="utf-8")
PUBLIC_DIRECTORY = (ROOT / "repositories.html").read_text(encoding="utf-8")
MAIN_JS = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")

FOCUS = {
    "goreecloud-home-security",
    "goreecloud-home",
    "goreecloud-ai",
    "goreecloud-containers",
    "goreecloud-code",
}


class ProjectPortfolioContractTests(unittest.TestCase):
    def test_main_is_front_door_not_duplicate_project_or_repository_directory(self) -> None:
        self.assertEqual(PUBLIC_HOME.count("destination-card"), 6)
        self.assertNotIn('data-project=', PUBLIC_HOME)
        self.assertNotIn('data-suite-app=', PUBLIC_HOME)
        self.assertNotIn('data-capability=', PUBLIC_HOME)
        self.assertNotIn('data-repository=', PUBLIC_HOME)
        self.assertIn('href="https://suite.goreecloud.com/"', PUBLIC_HOME)
        self.assertIn('href="https://projects.goreecloud.com/"', PUBLIC_HOME)
        self.assertIn("Home, AI &amp; Developer Systems", PUBLIC_HOME)
        self.assertIn("Publication pending", PUBLIC_HOME)

    def test_manifest_is_current_verified_inventory(self) -> None:
        self.assertEqual(MANIFEST["as_of"], "2026-09-05")
        self.assertEqual(MANIFEST["counts"], {
            "total": 68,
            "public": 65,
            "private": 3,
            "functional_groups": 15,
        })
        names = {repo["name"] for repo in REPOSITORIES}
        for current in (
            "goreecloud-glaze-ui",
            "goreecloud-identity",
            "goreecloud-mesh",
            "goreecloud-app-store",
            "goreecloud-file-manager",
            "goreecloud-maps",
            "goreecloud-index",
            "goreecloud-branding-assets",
            "goreecloud-vault-server",
            *sorted(FOCUS),
        ):
            self.assertIn(current, names)
        for retired_or_wrong in ("glaze-ui", "goreecloud-logo", "goreevault-server"):
            self.assertNotIn(retired_or_wrong, names)

    def test_public_repository_page_is_exact_five_product_focus_not_full_inventory(self) -> None:
        self.assertEqual(PUBLIC_DIRECTORY.count('class="repo-card glz1-system-overlay glz1-state-layer"'), 5)
        for name in FOCUS:
            self.assertIn(f"https://github.com/GoreeCloud/{name}", PUBLIC_DIRECTORY)
        self.assertNotRegex(PUBLIC_DIRECTORY, r"\b68\b[^<]{0,24}repositories")
        non_focus_public = sorted(PUBLIC_REPOSITORIES - FOCUS)
        self.assertTrue(non_focus_public)
        self.assertNotIn(f"https://github.com/GoreeCloud/{non_focus_public[0]}", PUBLIC_DIRECTORY)

    def test_private_repositories_do_not_publish_direct_source_links(self) -> None:
        combined = PUBLIC_HOME + "\n" + PUBLIC_DIRECTORY
        self.assertEqual(len(PRIVATE_REPOSITORIES), 3)
        for name in PRIVATE_REPOSITORIES:
            with self.subTest(private=name):
                self.assertNotIn(f"https://github.com/GoreeCloud/{name}", combined)

    def test_current_design_and_platform_truth_is_visible_without_stale_marketing(self) -> None:
        for marker in (
            "Your cloud should belong to you.",
            "seven Integral Platform Systems",
            "GoreeCloud Manager",
            "GoreeCloud Identity",
            "GoreeCloud Mesh",
        ):
            self.assertIn(marker, PUBLIC_HOME)
        self.assertIn("GoreeCloud/goreecloud-branding-assets", README)
        self.assertIn("GLAZE UI V1.1 / 1.1.0", README)
        self.assertNotIn("Glaze UI 2.1.0 Stable", PUBLIC_HOME)
        self.assertNotIn("current 57-repository portfolio", PUBLIC_HOME)
        self.assertNotIn("six substantive platform systems", PUBLIC_HOME)

    def test_javascript_does_not_generate_repository_or_editorial_facts(self) -> None:
        for removed_marker in (
            "CURRENT_PUBLIC_PROJECTS",
            "createProjectCard",
            "reconcilePublicProjectPortfolio",
            "repositorySection.innerHTML",
            "current-platform-update",
            "native-application-update",
            "fetch(",
        ):
            self.assertNotIn(removed_marker, MAIN_JS)


if __name__ == "__main__":
    unittest.main()
