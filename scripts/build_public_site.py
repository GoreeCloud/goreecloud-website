#!/usr/bin/env python3
"""Build the exact allowlisted Cloudflare Pages artifact for www.goreecloud.com.

The rebuilt Main website publishes only reviewed files named by PUBLIC_FILES.
Legacy/current identity assets that remain in source for provenance, historical,
or independently deployed surfaces are classified explicitly and cannot enter the
Main artifact merely because they remain in the repository.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import sys

from glaze_v1 import FILES as GLAZE_FILES, install_glaze

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

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

# The rebuilt Main surface uses the approved GoreeCloud master mark as its only
# deployable identity artwork. Product-specific artwork is not fabricated.
PUBLIC_ASSET_FILES = (
    "assets/goreecloud-logo.svg",
)

# These reviewed identity assets remain in repository source for provenance,
# historical records, or other independently governed website/source surfaces.
# They are deliberately excluded from the rebuilt Main Cloudflare artifact.
SOURCE_ONLY_ASSET_FILES = (
    "assets/platform/adguard-home.svg",
    "assets/platform/caddy.svg",
    "assets/platform/debian.svg",
    "assets/platform/docker.png",
    "assets/platform/netbird.svg",
    "assets/platform/proxmox.svg",
    "assets/platform/uptime-kuma.svg",
    "assets/roadmap/frigate.svg",
    "assets/roadmap/home-assistant.png",
    "assets/suite/ai.svg",
    "assets/suite/app-store.svg",
    "assets/suite/backup.svg",
    "assets/suite/bookmarks.svg",
    "assets/suite/browser.svg",
    "assets/suite/calendar.svg",
    "assets/suite/changelogs.svg",
    "assets/suite/code.svg",
    "assets/suite/contacts.svg",
    "assets/suite/dns.svg",
    "assets/suite/documents.svg",
    "assets/suite/drive.svg",
    "assets/suite/feed.svg",
    "assets/suite/file-manager.svg",
    "assets/suite/gallery.svg",
    "assets/suite/gateway.svg",
    "assets/suite/identity.svg",
    "assets/suite/index.svg",
    "assets/suite/keyboard.svg",
    "assets/suite/launcher.svg",
    "assets/suite/location.svg",
    "assets/suite/mail.svg",
    "assets/suite/manager.svg",
    "assets/suite/maps.svg",
    "assets/suite/memos.svg",
    "assets/suite/messenger.svg",
    "assets/suite/monitor.svg",
    "assets/suite/music.svg",
    "assets/suite/network.svg",
    "assets/suite/notes.svg",
    "assets/suite/notify.svg",
    "assets/suite/photos.svg",
    "assets/suite/search.svg",
    "assets/suite/sync.svg",
    "assets/suite/tasks.svg",
    "assets/suite/terminal.svg",
    "assets/suite/vault.svg",
    "assets/suite/video.svg",
    "assets/social/github.ico",
    "assets/social/instagram.ico",
    "assets/social/pinterest.ico",
    "assets/social/reddit.ico",
    "assets/social/threads.ico",
    "assets/social/tiktok.ico",
    "assets/social/x.ico",
    "assets/social/youtube.ico",
)

# Older upstream-service marks are retained only as reviewed historical source.
# They must not be reintroduced into current GoreeCloud-native public identity.
RETIRED_SOURCE_ONLY_ASSET_FILES = (
    "assets/services/actual-budget.png",
    "assets/services/audiobookshelf.svg",
    "assets/services/element.svg",
    "assets/services/immich.svg",
    "assets/services/jellyfin.svg",
    "assets/services/matrix.svg",
    "assets/services/navidrome.png",
    "assets/services/nextcloud.svg",
    "assets/services/onlyoffice.ico",
    "assets/services/paperless-ngx.svg",
    "assets/services/stirling-pdf.png",
    "assets/services/vaultwarden.svg",
)

PUBLIC_STYLE_FILES = ("css/site-v1.1.css",)
PUBLIC_SCRIPT_FILES = ("js/main.js", "js/theme-init.js")

PUBLIC_FILES = (
    *PUBLIC_ROOT_FILES,
    *PUBLIC_ASSET_FILES,
    *PUBLIC_STYLE_FILES,
    *PUBLIC_SCRIPT_FILES,
)
GENERATED_GLAZE_FILES = tuple(f"css/glaze-v1/{name}" for name in GLAZE_FILES)


def fail(message: str) -> int:
    print(f"Public-site build failed: {message}")
    return 1


def main() -> int:
    try:
        if len(PUBLIC_FILES) != len(set(PUBLIC_FILES)):
            return fail("public file allowlist contains duplicates")

        categories = {
            "deployable": set(PUBLIC_ASSET_FILES),
            "source-only": set(SOURCE_ONLY_ASSET_FILES),
            "retired": set(RETIRED_SOURCE_ONLY_ASSET_FILES),
        }
        names = tuple(categories)
        for index, left_name in enumerate(names):
            for right_name in names[index + 1:]:
                overlap = sorted(categories[left_name] & categories[right_name])
                if overlap:
                    return fail(
                        f"asset classification overlap between {left_name} and {right_name}: "
                        + ", ".join(overlap)
                    )

        for relative in (*SOURCE_ONLY_ASSET_FILES, *RETIRED_SOURCE_ONLY_ASSET_FILES):
            path = ROOT / relative
            if not path.is_file() or path.is_symlink():
                return fail(f"classified source-only identity asset is invalid: {relative}")

        for relative in PUBLIC_FILES:
            source = ROOT / relative
            if not source.is_file() or source.is_symlink():
                return fail(f"invalid allowlisted public source: {relative}")

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

    files = [path for path in DIST.rglob("*") if path.is_file()]
    print(f"Built isolated public artifact: {len(files)} files -> dist/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
