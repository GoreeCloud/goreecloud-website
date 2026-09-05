#!/usr/bin/env python3
"""Build the exact allowlisted Cloudflare Pages artifact for www.goreecloud.com."""
from __future__ import annotations

from pathlib import Path
import shutil
import sys

from glaze_v1 import FILES as GLAZE_FILES, install_glaze

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC_FILES = (
    "404.html", "_headers", "googlea0a636fd5dafd9e0.html", "index.html", "privacy.html",
    "repositories.html", "robots.txt", "security.html", "site.webmanifest", "sitemap.xml",
    ".well-known/security.txt", "assets/goreecloud-logo.svg", "css/site-v1.1.css",
    "js/main.js", "js/theme-init.js",
)
GENERATED_GLAZE_FILES = tuple(f"css/glaze-v1/{name}" for name in GLAZE_FILES)


def fail(message: str) -> int:
    print(f"Public-site build failed: {message}")
    return 1


def main() -> int:
    try:
        if len(PUBLIC_FILES) != len(set(PUBLIC_FILES)):
            return fail("public file allowlist contains duplicates")
        sources = [ROOT / relative for relative in PUBLIC_FILES]
        for source in sources:
            if not source.is_file() or source.is_symlink():
                return fail(f"invalid allowlisted public source: {source.relative_to(ROOT)}")
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
        install_glaze(DIST / "css" / "glaze-v1")
    except (OSError, ValueError) as exc:
        return fail(str(exc))
    files = [p for p in DIST.rglob("*") if p.is_file()]
    print(f"Built isolated public artifact: {len(files)} files -> dist/")
    return 0

if __name__ == "__main__":
    sys.exit(main())
