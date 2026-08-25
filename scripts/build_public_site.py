#!/usr/bin/env python3
"""Build the exact allowlisted static artifact for GoreeCloud's public website.

The source repository intentionally contains CI validators, GitHub metadata, and
repository documentation that are not part of the public website. Every deployable
file is named explicitly below so adding a file anywhere in the repository cannot
silently make that file public on the next Cloudflare Pages build.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

from render_repository_portfolio import load_manifest, render_public_file

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SERVICE_SECTION_FRAGMENT = ROOT / "fragments" / "services-section.html"

PUBLIC_ROOT_FILES = (
    "404.html",
    "_headers",
    "googlea0a636fd5dafd9e0.html",
    "index.html",
    "privacy.html",
    "repositories.html",
    "robots.txt",
    "security.html",
    "site.webmanifest",
    "sitemap.xml",
    ".well-known/security.txt",
)

PUBLIC_ASSET_FILES = (
    "assets/goreecloud-logo.svg",
    "assets/platform/adguard-home.svg",
    "assets/platform/caddy.svg",
    "assets/platform/debian.svg",
    "assets/platform/docker.png",
    "assets/platform/netbird.svg",
    "assets/platform/proxmox.svg",
    "assets/platform/uptime-kuma.svg",
    "assets/roadmap/frigate.svg",
    "assets/roadmap/home-assistant.png",
    "assets/services/goreecloud-memos.svg",
    "assets/social/github.ico",
    "assets/social/instagram.ico",
    "assets/social/pinterest.ico",
    "assets/social/reddit.ico",
    "assets/social/threads.ico",
    "assets/social/tiktok.ico",
    "assets/social/x.ico",
    "assets/social/youtube.ico",
    "assets/social-preview.png",
)

PUBLIC_STYLE_FILES = (
    "css/development.css",
    "css/error.css",
    "css/glaze-polish.css",
    "css/glaze.css",
    "css/how-it-works.css",
    "css/platform.css",
    "css/repositories.css",
    "css/roadmap.css",
    "css/social.css",
    "css/status.css",
    "css/style.css",
)

PUBLIC_SCRIPT_FILES = (
    "js/main.js",
    "js/public-info.js",
    "js/theme-init.js",
)

PUBLIC_FILES = (
    *PUBLIC_ROOT_FILES,
    *PUBLIC_ASSET_FILES,
    *PUBLIC_STYLE_FILES,
    *PUBLIC_SCRIPT_FILES,
)

GENERATED_HTML = {"index.html", "repositories.html"}


def fail(message: str) -> int:
    print(f"Public-site build failed: {message}")
    return 1


def reject_symlink(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"Deployable source must not be a symlink: {path.relative_to(ROOT)}")


def render_services_section(html: str) -> str:
    start = '    <section id="services" class="section">'
    next_section = '    <section id="how-it-works" class="section how-section">'
    if html.count(start) != 1 or html.count(next_section) != 1:
        raise ValueError("index.html service-section anchors are missing or ambiguous")
    fragment = SERVICE_SECTION_FRAGMENT.read_text(encoding="utf-8").rstrip()
    before, remainder = html.split(start, 1)
    _, after = remainder.split(next_section, 1)
    return f"{before}{fragment}\n\n{next_section}{after}"


def main() -> int:
    try:
        if len(PUBLIC_FILES) != len(set(PUBLIC_FILES)):
            return fail("public file allowlist contains a duplicate path")

        sources = [ROOT / relative for relative in PUBLIC_FILES]
        for source in sources:
            if not source.exists():
                return fail(f"required public source is missing: {source.relative_to(ROOT)}")
            if not source.is_file():
                return fail(f"allowlisted public source is not a regular file: {source.relative_to(ROOT)}")
            reject_symlink(source)

        if not SERVICE_SECTION_FRAGMENT.exists() or not SERVICE_SECTION_FRAGMENT.is_file():
            return fail("authoritative service-directory fragment is missing")
        reject_symlink(SERVICE_SECTION_FRAGMENT)

        manifest = load_manifest(ROOT)

        if DIST.exists():
            if DIST.is_symlink():
                return fail("dist must not be a symlink")
            shutil.rmtree(DIST)
        DIST.mkdir()

        for relative in PUBLIC_FILES:
            source = ROOT / relative
            destination = DIST / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if relative in GENERATED_HTML:
                source_text = source.read_text(encoding="utf-8")
                if relative == "index.html":
                    source_text = render_services_section(source_text)
                rendered = render_public_file(relative, source_text, manifest)
                destination.write_text(rendered, encoding="utf-8")
            else:
                shutil.copy2(source, destination)

    except (OSError, ValueError) as exc:
        return fail(str(exc))

    file_count = sum(1 for path in DIST.rglob("*") if path.is_file())
    total_bytes = sum(path.stat().st_size for path in DIST.rglob("*") if path.is_file())
    print(f"Built isolated public artifact: {file_count} files, {total_bytes} bytes -> dist/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
