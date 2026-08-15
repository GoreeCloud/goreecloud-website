#!/usr/bin/env python3
"""Regression tests for the public software-portfolio enhancement contract.

The homepage retains useful static development content while ``js/main.js`` reconciles
newer public projects at runtime. These tests keep that enhancement narrow, idempotent,
and safe: project repositories must remain GoreeCloud-controlled HTTPS GitHub URLs,
external links must preserve opener isolation, and the Bookmarks reconciliation must not
regress to planning-only presentation when JavaScript is available.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
MAIN_JS = (ROOT / "js" / "main.js").read_text(encoding="utf-8")

EXPECTED_DYNAMIC_PROJECTS = {
    "GoreeVault Server": "https://github.com/GoreeCloud/goreevault-server",
    "GoreeCloud Feed": "https://github.com/GoreeCloud/goreecloud-rss",
    "GoreeCloud Gallery": "https://github.com/GoreeCloud/goreecloud-gallery",
}
BOOKMARKS_REPOSITORY = "https://github.com/GoreeCloud/goreecloud-bookmarks"

PROJECT_RE = re.compile(
    r"name:\s*'(?P<name>[^']+)'\s*,\s*"
    r"description:\s*'(?P<description>[^']+)'\s*,\s*"
    r"repository:\s*'(?P<repository>https://[^']+)'",
    re.MULTILINE,
)


class ProjectPortfolioContractTests(unittest.TestCase):
    """Protect the small JavaScript portfolio reconciliation layer."""

    def test_dynamic_project_inventory_is_explicit_and_unique(self) -> None:
        projects = PROJECT_RE.findall(MAIN_JS)
        self.assertEqual(len(projects), len(EXPECTED_DYNAMIC_PROJECTS))

        names = [name for name, _description, _repository in projects]
        self.assertEqual(len(names), len(set(names)), "Dynamic project names must be unique.")

        actual = {name: repository for name, _description, repository in projects}
        self.assertEqual(actual, EXPECTED_DYNAMIC_PROJECTS)

    def test_public_project_links_remain_goreecloud_controlled_https_urls(self) -> None:
        repositories = [*EXPECTED_DYNAMIC_PROJECTS.values(), BOOKMARKS_REPOSITORY]
        for repository in repositories:
            with self.subTest(repository=repository):
                parsed = urlparse(repository)
                self.assertEqual(parsed.scheme, "https")
                self.assertEqual(parsed.hostname, "github.com")
                self.assertTrue(parsed.path.startswith("/GoreeCloud/"))
                self.assertFalse(parsed.params)
                self.assertFalse(parsed.query)
                self.assertFalse(parsed.fragment)

    def test_generated_external_links_preserve_opener_isolation(self) -> None:
        self.assertIn("link.target = '_blank';", MAIN_JS)
        self.assertIn("link.rel = 'noopener noreferrer';", MAIN_JS)

    def test_bookmarks_reconciliation_preserves_current_public_repository(self) -> None:
        self.assertIn("'GoreeCloud Bookmarks'", MAIN_JS)
        self.assertIn(BOOKMARKS_REPOSITORY, MAIN_JS)
        self.assertIn("status?.remove();", MAIN_JS)
        self.assertIn("Maintained Linkwarden-based bookmark", MAIN_JS)

    def test_reconciliation_is_idempotent_and_scoped_to_development_grid(self) -> None:
        self.assertIn("#development .development-grid", MAIN_JS)
        self.assertIn("const existingNames = new Set(", MAIN_JS)
        self.assertIn("if (!existingNames.has(project.name))", MAIN_JS)
        self.assertEqual(MAIN_JS.count("reconcilePublicProjectPortfolio();"), 1)

    def test_static_homepage_retains_development_fallback_content(self) -> None:
        self.assertIn('id="development"', INDEX)
        self.assertIn('class="principle-grid development-grid"', INDEX)
        self.assertIn("GoreeCloud Bookmarks", INDEX)
        self.assertIn("Research Library", INDEX)
        self.assertIn("GoreeCloud Manager", INDEX)


if __name__ == "__main__":
    unittest.main()
