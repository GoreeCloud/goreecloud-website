from __future__ import annotations

import copy
from datetime import date, timedelta
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_repository_portfolio as portfolio


class RepositoryPortfolioTests(unittest.TestCase):
    def test_current_repository_portfolio_passes(self) -> None:
        self.assertEqual(portfolio.validate(ROOT), [])

    def test_duplicate_repository_is_rejected(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(data)
        mutated["groups"][0]["repositories"].append(copy.deepcopy(mutated["groups"][0]["repositories"][0]))
        errors, _ = portfolio.validate_manifest(mutated)
        self.assertTrue(any("Duplicate repository portfolio entry" in error for error in errors))

    def test_declared_counts_are_derived_from_entries(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(data)
        mutated["counts"]["total"] = 999
        errors, _ = portfolio.validate_manifest(mutated)
        self.assertTrue(any("count 'total'" in error for error in errors))

    def test_manifest_review_date_must_be_valid_and_not_future(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(data)
        mutated["as_of"] = (date.today() + timedelta(days=1)).isoformat()
        errors, _ = portfolio.validate_manifest(mutated)
        self.assertTrue(any("must not be in the future" in error for error in errors))

    def test_current_inventory_matches_verified_snapshot(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        self.assertEqual(data["as_of"], "2026-09-05")
        self.assertEqual(data["counts"], {"total": 68, "public": 65, "private": 3, "functional_groups": 15})

    def test_public_source_has_no_repository_search_runtime_or_count_snapshot(self) -> None:
        directory = (ROOT / "repositories.html").read_text(encoding="utf-8")
        main_js = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
        combined = directory + "\n" + main_js
        for marker in ("repo-search", "repository-search", "data-repository=", "fetch("):
            self.assertNotIn(marker, combined)
        for label in ("current repositories", "public repositories", "private repositories", "functional groups"):
            import re
            self.assertIsNone(re.search(rf"\b\d+\b[^<]{{0,24}}{re.escape(label)}", directory, re.IGNORECASE))

    def test_five_focus_repositories_remain_present_in_manifest_and_public_page(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        names = {repository["name"] for group in data["groups"] for repository in group["repositories"]}
        directory = (ROOT / "repositories.html").read_text(encoding="utf-8")
        for name in portfolio.FOCUS_REPOSITORIES:
            self.assertIn(name, names)
            self.assertIn(name, directory)

    def test_private_repository_urls_do_not_leak_into_rebuilt_public_source(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        repositories = [repository for group in data["groups"] for repository in group["repositories"]]
        combined = (ROOT / "index.html").read_text(encoding="utf-8") + (ROOT / "repositories.html").read_text(encoding="utf-8")
        for repository in repositories:
            if repository["visibility"] == "private":
                self.assertNotIn(f"https://github.com/GoreeCloud/{repository['name']}", combined)


if __name__ == "__main__":
    unittest.main()
