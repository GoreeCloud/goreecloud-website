#!/usr/bin/env python3
"""Regression coverage for the rebuilt GoreeCloud repository focus page."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "repositories.html"
MANIFEST = ROOT / "docs" / "repository-portfolio.json"
PORTFOLIO = json.loads(MANIFEST.read_text(encoding="utf-8"))
EXPECTED_FOCUS = {
    "GoreeCloud Home Security": "https://github.com/GoreeCloud/goreecloud-home-security",
    "GoreeCloud Home": "https://github.com/GoreeCloud/goreecloud-home",
    "GoreeCloud AI": "https://github.com/GoreeCloud/goreecloud-ai",
    "GoreeCloud Containers": "https://github.com/GoreeCloud/goreecloud-containers",
    "GoreeCloud Code": "https://github.com/GoreeCloud/goreecloud-code",
}


class DirectoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.stylesheets: set[str] = set()
        self.scripts: set[str] = set()
        self.canonical = ""
        self.has_viewport = False
        self.has_color_scheme = False
        self.has_skip_link = False
        self.has_main = False
        self.main_tabindex = ""
        self.repo_links: dict[str, str] = {}
        self.status_labels: list[str] = []
        self._repo_depth = 0
        self._repo_href = ""
        self._h3_depth = 0
        self._h3_text: list[str] = []
        self._strong_depth = 0
        self._strong_text: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        classes = set(attrs.get("class", "").split())
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "link" and "stylesheet" in attrs.get("rel", "").split():
            self.stylesheets.add(attrs.get("href", ""))
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href", "")
        if tag == "script" and attrs.get("src"):
            self.scripts.add(attrs["src"])
        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        if tag == "meta" and attrs.get("name") == "color-scheme":
            self.has_color_scheme = True
        if tag == "a" and "skip-link" in classes and attrs.get("href") == "#main":
            self.has_skip_link = True
        if tag == "main" and attrs.get("id") == "main":
            self.has_main = True
            self.main_tabindex = attrs.get("tabindex", "")
        if tag == "a" and "repo-card" in classes:
            self._repo_depth = 1
            self._repo_href = attrs.get("href", "")
        elif self._repo_depth:
            self._repo_depth += 1
        if tag == "h3" and self._repo_depth:
            self._h3_depth = 1
            self._h3_text = []
        elif self._h3_depth:
            self._h3_depth += 1
        if tag == "strong" and not self._repo_depth:
            self._strong_depth = 1
            self._strong_text = []
        elif self._strong_depth:
            self._strong_depth += 1

    def handle_data(self, data: str) -> None:
        if self._h3_depth:
            self._h3_text.append(data)
        if self._strong_depth:
            self._strong_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._h3_depth:
            self._h3_depth -= 1
            if tag == "h3" and self._h3_depth == 0:
                name = "".join(self._h3_text).strip()
                if name:
                    self.repo_links[name] = self._repo_href
                self._h3_text = []
        if self._strong_depth:
            self._strong_depth -= 1
            if tag == "strong" and self._strong_depth == 0:
                value = "".join(self._strong_text).strip()
                if value in {"Implemented", "Development", "Planned"}:
                    self.status_labels.append(value)
                self._strong_text = []
        if self._repo_depth:
            self._repo_depth -= 1
            if tag == "a" and self._repo_depth == 0:
                self._repo_href = ""


class RepositoryDirectoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = PAGE.read_text(encoding="utf-8")
        cls.parser = DirectoryParser()
        cls.parser.feed(cls.source)

    def test_focus_page_has_canonical_public_identity(self) -> None:
        self.assertEqual(self.parser.canonical, "https://www.goreecloud.com/repositories.html")
        self.assertTrue(self.parser.has_viewport)
        self.assertTrue(self.parser.has_color_scheme)

    def test_focus_page_uses_rebuilt_shared_v11_shell(self) -> None:
        self.assertEqual(
            self.parser.stylesheets,
            {"/css/glaze-v1/glaze-v1.1.0.css", "/css/site-v1.1.css"},
        )
        self.assertEqual(self.parser.scripts, {"/js/theme-init.js", "/js/main.js"})
        self.assertNotIn("css/repositories.css", self.source)
        self.assertNotIn("glaze-ui-2.1.0", self.source)

    def test_focus_page_preserves_accessible_page_shell(self) -> None:
        self.assertTrue(self.parser.has_skip_link)
        self.assertTrue(self.parser.has_main)
        self.assertEqual(self.parser.main_tabindex, "-1")
        self.assertIn("main", self.parser.ids)

    def test_focus_page_matches_exact_five_current_product_repositories(self) -> None:
        self.assertEqual(self.parser.repo_links, EXPECTED_FOCUS)
        self.assertEqual(len(self.parser.repo_links), 5)

    def test_focus_page_explains_status_semantics_without_claiming_full_inventory(self) -> None:
        self.assertEqual(self.parser.status_labels, ["Implemented", "Development", "Planned"])
        self.assertNotRegex(self.source, r"\b\d+\s+(?:current\s+)?repositories\b")
        self.assertIn("A repository proves source, not production.", self.source)

    def test_full_repository_manifest_remains_separate_authoritative_inventory(self) -> None:
        repositories = [repository for group in PORTFOLIO["groups"] for repository in group["repositories"]]
        self.assertEqual(len(repositories), PORTFOLIO["counts"]["total"])
        names = {repository["name"] for repository in repositories}
        for repo_url in EXPECTED_FOCUS.values():
            self.assertIn(repo_url.rsplit("/", 1)[-1], names)


if __name__ == "__main__":
    unittest.main()
