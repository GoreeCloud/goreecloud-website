#!/usr/bin/env python3
"""Keep the publication/licensing inventory synchronized with deployable artwork."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_ASSET_FILES, PUBLIC_FILES  # noqa: E402

INVENTORY = ROOT / "docs" / "public-asset-inventory.md"
ASSET_PATH_RE = re.compile(r"`(assets/[A-Za-z0-9_./-]+\.(?:svg|png|jpg|jpeg|webp|gif))`")
BLOB_ID_RE = re.compile(r"[0-9a-f]{40,64}")


def inventory_rows(text: str) -> dict[str, str]:
    """Return deployable asset paths mapped to their reviewed Git blob IDs."""
    rows: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or "`assets/" not in line:
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue

        path_cell = cells[0]
        blob_cell = cells[-1]
        if not (path_cell.startswith("`assets/") and path_cell.endswith("`")):
            continue
        if not (blob_cell.startswith("`") and blob_cell.endswith("`")):
            continue

        path = path_cell[1:-1]
        blob_id = blob_cell[1:-1]
        if BLOB_ID_RE.fullmatch(blob_id):
            if path in rows:
                raise AssertionError(f"Duplicate deployable asset row in inventory: {path}")
            rows[path] = blob_id
    return rows


def git_blob_id(path: Path) -> str:
    """Compute the repository-format Git blob ID for the checked-out file bytes."""
    result = subprocess.run(
        ("git", "hash-object", str(path)),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "unknown git hash-object failure"
        raise AssertionError(f"Could not compute Git blob ID for {path.relative_to(ROOT)}: {message}")

    blob_id = result.stdout.strip()
    if not BLOB_ID_RE.fullmatch(blob_id):
        raise AssertionError(f"Unexpected Git blob ID for {path.relative_to(ROOT)}: {blob_id!r}")
    return blob_id


def normalize_markdown_text(text: str) -> str:
    """Normalize lightweight Markdown emphasis before semantic wording checks."""
    return re.sub(r"[*_]", "", text).lower()


class PublicAssetInventoryTests(unittest.TestCase):
    """Prevent deployable artwork from bypassing the pre-publication rights review."""

    def test_inventory_exists_but_is_not_deployed(self) -> None:
        self.assertTrue(INVENTORY.is_file())
        self.assertNotIn("docs/public-asset-inventory.md", PUBLIC_FILES)

    def test_inventory_matches_exact_public_asset_allowlist(self) -> None:
        text = INVENTORY.read_text(encoding="utf-8")
        documented = set(ASSET_PATH_RE.findall(text))
        expected = set(PUBLIC_ASSET_FILES)

        self.assertEqual(
            documented,
            expected,
            "Public asset inventory must exactly match PUBLIC_ASSET_FILES; review licensing/provenance whenever deployable artwork changes.",
        )

        for path in PUBLIC_ASSET_FILES:
            self.assertEqual(
                text.count(f"`{path}`"),
                1,
                f"Deployable asset must appear exactly once in the inventory table: {path}",
            )

    def test_reviewed_blob_ids_match_current_asset_bytes(self) -> None:
        text = INVENTORY.read_text(encoding="utf-8")
        reviewed = inventory_rows(text)
        expected = set(PUBLIC_ASSET_FILES)

        self.assertEqual(
            set(reviewed),
            expected,
            "Every deployable asset must have exactly one reviewed Git blob ID in the inventory.",
        )

        for relative_path in PUBLIC_ASSET_FILES:
            actual = git_blob_id(ROOT / relative_path)
            self.assertEqual(
                reviewed[relative_path],
                actual,
                (
                    f"Deployable asset bytes changed without updating the rights/provenance inventory: {relative_path}. "
                    "Review the new artwork and update its recorded Git blob ID in the same change."
                ),
            )

    def test_inventory_preserves_publication_boundary_language(self) -> None:
        text = normalize_markdown_text(INVENTORY.read_text(encoding="utf-8"))
        required = (
            "not a license grant",
            "provenance and rights verification still required",
            "source-code license must not be assumed to relicense third-party marks",
            "integrity fingerprint only",
            "does not establish copyright ownership",
            "issue #5 remains open",
        )
        for marker in required:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
