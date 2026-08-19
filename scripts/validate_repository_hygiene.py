#!/usr/bin/env python3
"""Setup-only v5.21 migration/export bridge.

This file is intentionally temporary and is never eligible for the release tree. It applies the
already-preflighted migration in the CI workspace, packs the exact final changed files into one
compressed base64 bundle, and intentionally stops the setup workflow immediately afterward so
the export log remains compact enough for deterministic materialization through GitHub's
blob/tree API. The real release tree inherits the normal hygiene validator from main.
"""

from __future__ import annotations

from base64 import b64encode
from io import BytesIO
from pathlib import Path
import subprocess
import sys
import tarfile

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


def emit_bundle() -> None:
    buffer = BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz", compresslevel=9) as archive:
        for relative in FINAL_FILES:
            path = ROOT / relative
            if not path.is_file():
                raise SystemExit(f"Expected final changed file is missing: {relative}")
            archive.add(path, arcname=relative, recursive=False)
        deletion_bytes = ("\n".join(DELETIONS) + "\n").encode("utf-8")
        info = tarfile.TarInfo("V521_DELETIONS.txt")
        info.size = len(deletion_bytes)
        info.mode = 0o644
        archive.addfile(info, BytesIO(deletion_bytes))

    encoded = b64encode(buffer.getvalue()).decode("ascii")
    print(f"V521_TARGZ_BASE64 {encoded}")
    print(f"V521_TARGZ_BYTES {len(buffer.getvalue())}")


def main() -> int:
    apply_once()
    emit_bundle()
    print("V521_EXPORT_COMPLETE: intentional setup-only stop after exact bundle emission.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
