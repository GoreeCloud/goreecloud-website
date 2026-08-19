#!/usr/bin/env python3
"""Setup-only v5.21 migration/export bridge.

This file is intentionally temporary and is never eligible for the release tree. During a
normal read-only PR workflow it applies the guarded v5.21 migration to the runner workspace,
restores the historical creative-rights wording still required by repository-governance tests,
and emits the exact final changed files as base64 so they can be materialized with GitHub's
blob/tree API. The final release tree inherits the real hygiene validator from main.
"""

from __future__ import annotations

from base64 import b64encode
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
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


def apply_once() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version == "5.20.0":
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "apply_v521_native_platform_marks.py")],
            cwd=ROOT,
            check=True,
        )
        normalize_generated_markers()
        preserve_governance_history_language()
    elif version != "5.21.0":
        raise SystemExit(f"Unexpected VERSION during v5.21 setup export: {version!r}")


def emit_blobs() -> None:
    print("V521_BUNDLE_BEGIN")
    for relative in FINAL_FILES:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"Expected final changed file is missing: {relative}")
        encoded = b64encode(path.read_bytes()).decode("ascii")
        print(f"V521_BLOB {relative} {encoded}")
    print("V521_DELETE assets/platform/adguard-home.svg")
    print("V521_DELETE assets/platform/beszel.svg")
    print("V521_DELETE assets/platform/caddy.svg")
    print("V521_DELETE assets/platform/debian.svg")
    print("V521_DELETE assets/platform/docker.svg")
    print("V521_DELETE assets/platform/netbird.svg")
    print("V521_DELETE assets/platform/ntfy.svg")
    print("V521_DELETE assets/platform/proxmox.svg")
    print("V521_DELETE assets/platform/searxng.svg")
    print("V521_DELETE assets/platform/uptime-kuma.svg")
    print("V521_BUNDLE_END")


def main() -> int:
    apply_once()
    emit_blobs()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
