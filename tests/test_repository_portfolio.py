from __future__ import annotations

import copy
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
        mutated["groups"][0]["repositories"].append(
            copy.deepcopy(mutated["groups"][0]["repositories"][0])
        )
        errors = portfolio.validate_manifest(mutated)
        self.assertTrue(any("Duplicate repository portfolio entry" in error for error in errors))

    def test_declared_counts_are_derived_from_entries(self) -> None:
        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
        mutated = copy.deepcopy(data)
        mutated["counts"]["total"] = 999
        errors = portfolio.validate_manifest(mutated)
        self.assertTrue(any("count 'total'" in error for error in errors))

    def test_repository_discovery_controls_remain_local_and_ephemeral(self) -> None:
        main_js = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
        repository_css = (ROOT / "css" / "repositories.css").read_text(encoding="utf-8")
        self.assertEqual(portfolio.validate_discovery_enhancement(main_js, repository_css), [])

        mutated = main_js + "\n// simulated regression\nfetch('/repository-search?q=test');\n"
        errors = portfolio.validate_discovery_enhancement(mutated, repository_css)
        self.assertTrue(any("local, ephemeral, and network-independent" in error for error in errors))

    def test_repository_discovery_keeps_adaptive_and_print_fallbacks(self) -> None:
        main_js = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
        repository_css = (ROOT / "css" / "repositories.css").read_text(encoding="utf-8")
        mutated = repository_css.replace("@media print", "@media screen")
        errors = portfolio.validate_discovery_enhancement(main_js, mutated)
        self.assertTrue(any("@media print" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
