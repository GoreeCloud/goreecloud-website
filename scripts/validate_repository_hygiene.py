#!/usr/bin/env python3
"""Setup-only v5.21 migration and artifact-staging bridge.

This temporary script runs only on the non-mergeable setup PR. It applies the guarded v5.21
migration inside the read-only Actions workspace, restores the exact intended final validation
workflow, stages only the final changed files plus the ten-file deletion manifest for a private
workflow artifact, and returns success so the remaining normal validators can inspect the same
transformed workspace. This script itself is never eligible for the release tree.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPORT_ROOT = ROOT / "v521-export"
FINAL_FILES = (
    ".github/workflows/validate.yml",
    "README.md",
    "VERSION",
    "css/platform.css",
    "docs/public-asset-inventory.md",
    "docs/stability-baseline.md",
    "index.html",
    "scripts/build_public_site.py",
    "scripts/validate_public_assets.py",
    "tests/test_public_assets.py",
    "tests/test_stability_baseline.py",
)
DELETIONS = (
    "assets/platform/adguard-home.svg",
    "assets/platform/beszel.svg",
    "assets/platform/caddy.svg",
    "assets/platform/debian.svg",
    "assets/platform/docker.svg",
    "assets/platform/netbird.svg",
    "assets/platform/ntfy.svg",
    "assets/platform/proxmox.svg",
    "assets/platform/searxng.svg",
    "assets/platform/uptime-kuma.svg",
)


def normalize_generated_markers() -> None:
    old = "historical commits may still contain prior third-party artwork blobs"
    new = "Historical commits may still contain prior third-party artwork blobs"
    for relative in ("scripts/validate_public_assets.py", "tests/test_public_assets.py"):
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit(f"Expected one generated marker in {relative}; found {text.count(old)}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")


def preserve_governance_history_language() -> None:
    path = ROOT / "docs" / "public-asset-inventory.md"
    text = path.read_text(encoding="utf-8")
    marker = "## Publication gate\n"
    if marker not in text:
        raise SystemExit("Public asset inventory publication gate marker is missing.")
    historical = """## Historical third-party artwork note

Provenance and rights verification still required for any future artwork addition and for final historical-repository publication review. The source-code license must not be assumed to relicense third-party marks.

Simple Icons disclaimer: an earlier website state used third-party platform artwork obtained through an intermediary icon library. Those SVG logo files are no longer part of the current source tree or deployable public artifact. This historical note records provenance context only and does not grant reuse rights.

"""
    if "Simple Icons disclaimer" not in text:
        text = text.replace(marker, historical + marker, 1)
    path.write_text(text, encoding="utf-8")


def restore_final_validation_workflow() -> None:
    result = subprocess.run(
        ["git", "show", "origin/main:.github/workflows/validate.yml"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    source = result.stdout
    marker = "      - name: Validate source license\n        run: python scripts/validate_license.py\n"
    insertion = marker + "\n      - name: Validate public asset rights boundary\n        run: python scripts/validate_public_assets.py\n"
    if source.count(marker) != 1:
        raise SystemExit(f"Expected one source-license workflow marker in origin/main; found {source.count(marker)}")
    if "Validate public asset rights boundary" in source:
        final = source
    else:
        final = source.replace(marker, insertion, 1)
    (ROOT / ".github/workflows/validate.yml").write_text(final, encoding="utf-8")


def apply_once() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "5.20.0":
        raise SystemExit(f"Expected exact v5.20.0 setup baseline; found {version!r}")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "apply_v521_native_platform_marks.py")],
        cwd=ROOT,
        check=True,
    )
    normalize_generated_markers()
    preserve_governance_history_language()
    restore_final_validation_workflow()


def stage_artifact() -> None:
    if EXPORT_ROOT.exists():
        shutil.rmtree(EXPORT_ROOT)
    files_root = EXPORT_ROOT / "files"
    for relative in FINAL_FILES:
        source = ROOT / relative
        if not source.is_file() or source.is_symlink():
            raise SystemExit(f"Expected final changed regular file is missing: {relative}")
        target = files_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (EXPORT_ROOT / "V521_DELETIONS.txt").write_text("\n".join(DELETIONS) + "\n", encoding="utf-8")


def main() -> int:
    apply_once()
    stage_artifact()
    print("Setup-only v5.21 transform staged for private artifact upload; continuing normal validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
