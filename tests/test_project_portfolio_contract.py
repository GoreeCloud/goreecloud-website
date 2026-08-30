#!/usr/bin/env python3
"""Regression coverage for the current public GoreeCloud portfolio surfaces.

The main homepage is a ten-site ecosystem hub. The exhaustive source portfolio lives
in the manifest-rendered repository directory, while product-specific directory
content belongs on Projects and Suite rather than being duplicated on the main page.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from normalize_homepage import normalize_homepage  # noqa: E402
from render_repository_portfolio import render_public_file, render_repository_directory  # noqa: E402

MANIFEST = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
REPOSITORIES = [repo for group in MANIFEST["groups"] for repo in group["repositories"]]
PUBLIC_REPOSITORIES = {repo["name"] for repo in REPOSITORIES if repo["visibility"] == "public"}
PRIVATE_REPOSITORIES = {repo["name"] for repo in REPOSITORIES if repo["visibility"] == "private"}

SOURCE_HOME = (ROOT / "index.html").read_text(encoding="utf-8")
INTERMEDIATE_HOME = render_public_file("index.html", SOURCE_HOME, MANIFEST)
PUBLIC_HOME = normalize_homepage(INTERMEDIATE_HOME)
PUBLIC_DIRECTORY = render_repository_directory((ROOT / "repositories.html").read_text(encoding="utf-8"), MANIFEST)
MAIN_JS = (ROOT / "js" / "main.js").read_text(encoding="utf-8")


class ProjectPortfolioContractTests(unittest.TestCase):
    def test_final_homepage_is_ecosystem_hub_not_duplicate_project_directory(self) -> None:
        self.assertEqual(PUBLIC_HOME.count('id="websites"'), 1)
        self.assertEqual(PUBLIC_HOME.count('class="service-card website-card '), 10)
        self.assertNotIn('id="development"', PUBLIC_HOME)
        self.assertNotIn('data-project=', PUBLIC_HOME)
        self.assertNotIn('data-suite-app=', PUBLIC_HOME)
        self.assertNotIn('data-capability=', PUBLIC_HOME)
        self.assertIn('href="https://suite.goreecloud.com/"', PUBLIC_HOME)
        self.assertIn('href="https://projects.goreecloud.com/"', PUBLIC_HOME)

    def test_manifest_is_current_reviewed_inventory(self) -> None:
        self.assertEqual(MANIFEST["counts"], {
            "total": 56,
            "public": 40,
            "private": 16,
            "functional_groups": 13,
        })
        names = {repo["name"] for repo in REPOSITORIES}
        for current in (
            "goreecloud-glaze-ui",
            "goreecloud-identity",
            "goreecloud-mesh",
            "goreecloud-app-store",
            "goreecloud-file-manager",
            "goreecloud-maps",
            "goreecloud-branding-assets",
            "goreecloud-vault-server",
        ):
            self.assertIn(current, names)
        for retired_or_wrong in ("glaze-ui", "goreecloud-logo", "goreevault-server"):
            self.assertNotIn(retired_or_wrong, names)

    def test_repository_directory_contains_every_current_repository_once(self) -> None:
        for repository in REPOSITORIES:
            name = repository["name"]
            with self.subTest(repository=name):
                self.assertEqual(PUBLIC_DIRECTORY.count(f"<h4>{name}</h4>"), 1)
        self.assertIn("56</strong><span>current repositories", PUBLIC_DIRECTORY)
        self.assertIn("40</strong><span>public repositories", PUBLIC_DIRECTORY)
        self.assertIn("16</strong><span>private repositories", PUBLIC_DIRECTORY)

    def test_repository_links_preserve_visibility_boundary(self) -> None:
        for name in PUBLIC_REPOSITORIES:
            with self.subTest(public=name):
                self.assertIn(f"https://github.com/GoreeCloud/{name}", PUBLIC_DIRECTORY)
        for name in PRIVATE_REPOSITORIES:
            with self.subTest(private=name):
                self.assertNotIn(f"https://github.com/GoreeCloud/{name}", PUBLIC_DIRECTORY)

    def test_current_design_and_platform_truth_is_visible_in_final_homepage(self) -> None:
        for marker in (
            "current 56-repository portfolio",
            "Glaze UI 2.0.0 Stable",
            "Glaze UI 2.1 remains Candidate",
            "six substantive platform systems",
            "GoreeCloud Identity",
            "GoreeCloud Mesh",
            "GoreeCloud/goreecloud-branding-assets",
        ):
            if marker == "GoreeCloud/goreecloud-branding-assets":
                # Branding authority is repository metadata, not a browser-facing URL.
                self.assertIn(marker, (ROOT / "README.md").read_text(encoding="utf-8"))
            else:
                self.assertIn(marker, PUBLIC_HOME)

    def test_javascript_does_not_generate_repository_or_editorial_facts(self) -> None:
        for removed_marker in (
            "CURRENT_PUBLIC_PROJECTS",
            "createProjectCard",
            "reconcilePublicProjectPortfolio",
            "repositorySection.innerHTML",
            "current-platform-update",
            "native-application-update",
        ):
            self.assertNotIn(removed_marker, MAIN_JS)


if __name__ == "__main__":
    unittest.main()
