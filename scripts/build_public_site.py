#!/usr/bin/env python3
"""Build an allowlisted static artifact for GoreeCloud's public website.

The source repository intentionally contains CI validators, GitHub metadata, and
repository documentation that are not part of the public website. This script
copies only the files and directories that are intended to be deployable.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

PUBLIC_FILES = (
    "404.html",
    "_headers",
    "googlea0a636fd5dafd9e0.html",
    "index.html",
    "privacy.html",
    "robots.txt",
    "security.html",
    "site.webmanifest",
    "sitemap.xml",
)

PUBLIC_DIRECTORIES = (
    ".well-known",
    "assets",
    "css",
    "js",
)


def fail(message: str) -> int:
    print(f"Public-site build failed: {message}")
    return 1


def reject_symlinks(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"Deployable source must not be a symlink: {path.relative_to(ROOT)}")
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_symlink():
                raise ValueError(f"Deployable source must not contain symlinks: {child.relative_to(ROOT)}")


def main() -> int:
    try:
        sources = [ROOT / relative for relative in (*PUBLIC_FILES, *PUBLIC_DIRECTORIES)]
        for source in sources:
            if not source.exists():
                return fail(f"required public source is missing: {source.relative_to(ROOT)}")
            reject_symlinks(source)

        if DIST.exists():
            if DIST.is_symlink():
                return fail("dist must not be a symlink")
            shutil.rmtree(DIST)
        DIST.mkdir()

        for relative in PUBLIC_FILES:
            source = ROOT / relative
            destination = DIST / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        for relative in PUBLIC_DIRECTORIES:
            shutil.copytree(ROOT / relative, DIST / relative)

    except (OSError, ValueError) as exc:
        return fail(str(exc))

    file_count = sum(1 for path in DIST.rglob("*") if path.is_file())
    total_bytes = sum(path.stat().st_size for path in DIST.rglob("*") if path.is_file())
    print(f"Built isolated public artifact: {file_count} files, {total_bytes} bytes -> dist/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
