#!/usr/bin/env python3
"""Regression tests for the static GoreeCloud public software portfolio.

The public project inventory is intentionally present in ``index.html`` instead of being
injected by JavaScript. This keeps the normal and no-JavaScript experiences aligned,
improves crawlability, and reduces unnecessary client-side mutation while preserving the
privacy and repository-publication boundaries of private projects.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
MAIN_JS = (ROOT / "js" / "main.js").read_text(encoding="utf-8")

PUBLIC_PROJECTS = {
    "GoreeCloud Manager": "https://github.com/GoreeCloud/goreecloud-manager",
    "GoreeCloud Calendar": "https://github.com/GoreeCloud/goreecloud-calendar",
    "GoreeCloud Monitoring": "https://github.com/GoreeCloud/goreecloud-monitor",
    "GoreeCloud Search": "https://github.com/GoreeCloud/goreecloud-search",
    "GoreeCloud Browser": "https://github.com/GoreeCloud/goreecloud-browser",
    "GoreeCloud Redirector": "https://github.com/GoreeCloud/goreecloud-redirector",
    "GoreeCloud Source Resync": "https://github.com/GoreeCloud/goreecloud-source-resync",
    "GoreeCloud Notes": "https://github.com/GoreeCloud/goreecloud-notes",
    "GoreeCloud Memos": "https://github.com/GoreeCloud/goreecloud-memos",
    "GoreeCloud Research Library": "https://github.com/GoreeCloud/goreecloud-research-library",
    "GoreeCloud Bookmarks": "https://github.com/GoreeCloud/goreecloud-bookmarks",
    "GoreeCloud Bookmarks Browser Extension": "https://github.com/GoreeCloud/goreecloud-bookmark-browser-extension",
    "GoreeCloud Feed": "https://github.com/GoreeCloud/goreecloud-rss",
    "GoreeCloud Gallery": "https://github.com/GoreeCloud/goreecloud-gallery",
    "GoreeVault Server": "https://github.com/GoreeCloud/goreevault-server",
}

PRIVATE_PROJECTS = {
    "GoreeCloud Tasks": "https://github.com/GoreeCloud/goreecloud-tasks",
    "GoreeCloud Contacts": "https://github.com/GoreeCloud/goreecloud-contacts",
    "GoreeCloud Notify": "https://github.com/GoreeCloud/goreecloud-notify",
}

EXPECTED_PROJECT_SLUGS = {
    "goreecloud-manager",
    "goreecloud-tasks",
    "goreecloud-contacts",
    "goreecloud-calendar",
    "goreecloud-notify",
    "goreecloud-monitor",
    "goreecloud-search",
    "goreecloud-browser",
    "goreecloud-redirector",
    "goreecloud-source-resync",
    "goreecloud-notes",
    "goreecloud-memos",
    "goreecloud-research-library",
    "goreecloud-bookmarks",
    "goreecloud-bookmark-browser-extension",
    "goreecloud-feed",
    "goreecloud-gallery",
    "goreevault-server",
}

PROJECT_SLUG_RE = re.compile(r'data-project="([a-z0-9-]+)"')


class ProjectPortfolioContractTests(unittest.TestCase):
    """Protect the static public project inventory and migration boundaries."""

    def test_project_inventory_is_static_explicit_and_unique(self) -> None:
        slugs = PROJECT_SLUG_RE.findall(INDEX)
        self.assertEqual(set(slugs), EXPECTED_PROJECT_SLUGS)
        self.assertEqual(len(slugs), len(set(slugs)), "Public project markers must be unique.")

        for project_name in [*PUBLIC_PROJECTS, *PRIVATE_PROJECTS]:
            with self.subTest(project=project_name):
                self.assertIn(f"<strong>{project_name}</strong>", INDEX)

    def test_public_project_links_remain_goreecloud_controlled_https_urls(self) -> None:
        for project_name, repository in PUBLIC_PROJECTS.items():
            with self.subTest(project=project_name):
                parsed = urlparse(repository)
                self.assertEqual(parsed.scheme, "https")
                self.assertEqual(parsed.hostname, "github.com")
                self.assertTrue(parsed.path.startswith("/GoreeCloud/"))
                self.assertFalse(parsed.params)
                self.assertFalse(parsed.query)
                self.assertFalse(parsed.fragment)
                self.assertIn(f'href="{repository}" target="_blank" rel="noopener noreferrer"', INDEX)

    def test_private_development_projects_do_not_publish_repository_links(self) -> None:
        for project_name, repository in PRIVATE_PROJECTS.items():
            with self.subTest(project=project_name):
                self.assertIn(project_name, INDEX)
                self.assertNotIn(repository, INDEX)

    def test_notification_and_search_replacements_are_current(self) -> None:
        self.assertIn("GoreeCloud Notify", INDEX)
        self.assertIn("has replaced ntfy", INDEX)
        self.assertIn("GoreeCloud Search", INDEX)
        self.assertIn("has replaced the direct SearXNG-facing service", INDEX)
        self.assertNotIn("ntfy remains current", INDEX)

    def test_monitor_transition_preserves_uptime_kuma_until_cutover(self) -> None:
        self.assertIn("GoreeCloud Monitoring", INDEX)
        self.assertIn("Uptime Kuma", INDEX)
        self.assertIn("remains in service until GoreeCloud Monitoring completes validation", INDEX)
        self.assertIn("replacement for Uptime Kuma", INDEX)

    def test_bookmarks_static_content_reflects_current_public_repository(self) -> None:
        self.assertIn("Maintained Linkwarden-based bookmark", INDEX)
        self.assertIn(PUBLIC_PROJECTS["GoreeCloud Bookmarks"], INDEX)
        self.assertNotIn("Specification &amp; fork planning", INDEX)

    def test_glaze_ui_repository_is_linked_from_project_overview(self) -> None:
        self.assertIn("https://github.com/GoreeCloud/glaze-ui", INDEX)
        self.assertIn("View public repository →", INDEX)

    def test_complete_repository_directory_is_discoverable(self) -> None:
        self.assertIn('href="repositories.html"', INDEX)
        self.assertIn("complete repository directory", INDEX)
        self.assertIn("all 20 current repositories", INDEX)

    def test_javascript_does_not_mutate_project_portfolio(self) -> None:
        for removed_marker in (
            "CURRENT_PUBLIC_PROJECTS",
            "createProjectCard",
            "reconcilePublicProjectPortfolio",
            "#development .development-grid",
        ):
            self.assertNotIn(removed_marker, MAIN_JS)


if __name__ == "__main__":
    unittest.main()
