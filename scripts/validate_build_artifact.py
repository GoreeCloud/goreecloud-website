#!/usr/bin/env python3
"""Validate the exact www.goreecloud.com deployment artifact."""
from __future__ import annotations

from pathlib import Path
import sys

from build_public_site import DIST, GENERATED_GLAZE_FILES, PUBLIC_FILES, ROOT
from glaze_v1 import FILES as GLAZE_FILES, validate_bundle

FORBIDDEN_TOP_LEVEL = {".git", ".github", "README.md", "SECURITY.md", "docs", "scripts", "sites"}


def main() -> int:
    errors: list[str] = []
    if not DIST.is_dir() or DIST.is_symlink():
        errors.append("dist/ is missing or invalid")
    if errors:
        print("Build artifact validation failed:\n  - " + "\n  - ".join(errors))
        return 1

    actual = {str(path.relative_to(DIST)) for path in DIST.rglob("*") if path.is_file()}
    expected = set(PUBLIC_FILES) | set(GENERATED_GLAZE_FILES)
    for path in sorted(expected - actual): errors.append(f"missing artifact file: {path}")
    for path in sorted(actual - expected): errors.append(f"unexpected artifact file: {path}")

    for relative in PUBLIC_FILES:
        source, built = ROOT / relative, DIST / relative
        if built.is_file() and source.read_bytes() != built.read_bytes():
            errors.append(f"copied artifact differs from reviewed source: {relative}")

    bundle: dict[str, str] = {}
    for name in GLAZE_FILES:
        path = DIST / "css" / "glaze-v1" / name
        if path.is_file(): bundle[name] = path.read_text(encoding="utf-8")
    try:
        validate_bundle(bundle)
    except ValueError as exc:
        errors.append(str(exc))

    top = {Path(path).parts[0] for path in actual if Path(path).parts}
    for forbidden in sorted(top & FORBIDDEN_TOP_LEVEL): errors.append(f"repository-only content leaked into artifact: {forbidden}")

    for page in ("index.html", "repositories.html", "privacy.html", "security.html", "404.html"):
        text = (DIST / page).read_text(encoding="utf-8")
        for marker in ('data-glaze-version="1.1"', 'name="goreecloud-glaze-ui" content="1.1.0"', 'data-glaze-ui="1.1.0"'):
            if marker not in text: errors.append(f"{page} missing GLAZE V1.1 marker: {marker}")
        if "glaze-ui-2.1.0.css" in text or "Expanding the platform" in text:
            errors.append(f"{page} contains retired website content")

    if errors:
        print("Build artifact validation failed:")
        for error in errors: print(f"  - {error}")
        return 1
    print(f"Build artifact validation passed: {len(actual)} files; GLAZE V1.1 is published same-origin from the pinned Stable revision.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
