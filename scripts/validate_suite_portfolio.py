#!/usr/bin/env python3
"""Validate the reviewed GoreeCloud Suite manifest and rendered homepage section."""

from __future__ import annotations

from hashlib import sha1
from pathlib import Path
import re
import sys

from render_repository_portfolio import load_manifest, load_suite_manifest, render_public_file

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REF = re.compile(r"^[0-9a-f]{40}$|^(?:main|master)$")
STATUS_CLASSES = {"active", "growing", "planned"}
REQUIRED_FIELDS = {
    "id",
    "name",
    "description",
    "role",
    "status",
    "status_class",
    "icon",
    "icon_blob",
    "source_repository",
    "source_path",
    "source_ref",
}
LEGACY_CARD_IDS = {
    "nextcloud",
    "immich",
    "jellyfin",
    "navidrome",
    "audiobookshelf",
    "paperless",
    "vaultwarden",
    "element",
    "onlyoffice",
    "stirling-pdf",
    "actual-budget",
}


def blob_id(raw: bytes) -> str:
    return sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def main() -> int:
    errors: list[str] = []
    manifest = load_suite_manifest(ROOT)
    if manifest.get("schema_version") != 1:
        errors.append("Suite manifest schema_version must be 1.")
    if manifest.get("section_title") != "GoreeCloud Suite":
        errors.append("Suite section title must be 'GoreeCloud Suite'.")
    if not str(manifest.get("section_description", "")).strip():
        errors.append("Suite section description must be non-empty.")

    groups = manifest.get("groups")
    if not isinstance(groups, list) or not groups:
        errors.append("Suite manifest must contain application groups.")
        groups = []

    ids: set[str] = set()
    names: set[str] = set()
    icons: set[str] = set()
    applications: list[dict] = []

    for group in groups:
        if not str(group.get("id", "")).strip() or not str(group.get("label", "")).strip():
            errors.append("Every Suite group must have a non-empty id and label.")
        apps = group.get("applications")
        if not isinstance(apps, list) or not apps:
            errors.append(f"Suite group has no applications: {group.get('id')!r}")
            continue
        applications.extend(apps)

    if len(applications) != 34:
        errors.append(f"Suite manifest must contain exactly 34 current applications/services; found {len(applications)}.")

    for app in applications:
        missing = sorted(field for field in REQUIRED_FIELDS if not str(app.get(field, "")).strip())
        if missing:
            errors.append(f"Suite application {app.get('id')!r} is missing fields: {', '.join(missing)}")
            continue

        app_id = app["id"]
        if app_id in ids:
            errors.append(f"Duplicate Suite application id: {app_id}")
        ids.add(app_id)

        name = app["name"]
        if name in names:
            errors.append(f"Duplicate Suite application name: {name}")
        names.add(name)

        icon = app["icon"]
        if icon in icons:
            errors.append(f"Duplicate Suite icon path: {icon}")
        icons.add(icon)
        if not icon.startswith("assets/suite/") or not icon.endswith(".svg"):
            errors.append(f"Suite icon must use assets/suite/*.svg: {icon}")
        else:
            path = ROOT / icon
            if not path.is_file() or path.is_symlink():
                errors.append(f"Suite icon is missing or invalid: {icon}")
            elif blob_id(path.read_bytes()) != app["icon_blob"]:
                errors.append(f"Suite icon bytes do not match reviewed repository-owned artwork: {icon}")

        if app["status_class"] not in STATUS_CLASSES:
            errors.append(f"Unsupported Suite status class for {app_id}: {app['status_class']}")
        if not app["source_repository"].startswith("GoreeCloud/"):
            errors.append(f"Suite source repository must be first-party GoreeCloud: {app_id}")
        if not REF.fullmatch(app["source_ref"]):
            errors.append(f"Suite source ref must be an immutable commit or reviewed main/master branch: {app_id}")

    if "quill" in ids or "GoreeCloud Quill" in names:
        errors.append("Quill is a GoreeCloud Keyboard capability family and must not be listed as a standalone Suite application.")

    source = INDEX.read_text(encoding="utf-8")
    rendered = render_public_file("index.html", source, load_manifest(ROOT))
    if "Personal &amp; family services" in rendered or "Personal & family services" in rendered:
        errors.append("Rendered homepage still contains the replaced Personal & Family Services heading.")
    if '<p class="eyebrow">GoreeCloud Suite</p>' not in rendered:
        errors.append("Rendered homepage is missing the GoreeCloud Suite heading.")
    if '<a href="#services">Suite</a>' not in rendered:
        errors.append("Rendered homepage navigation does not identify the section as Suite.")

    for legacy_id in sorted(LEGACY_CARD_IDS):
        if f'data-service="{legacy_id}"' in rendered:
            errors.append(f"Legacy service card remains in rendered GoreeCloud Suite section: {legacy_id}")

    for app in applications:
        marker = f'data-suite-app="{app["id"]}"'
        if rendered.count(marker) != 1:
            errors.append(f"Rendered homepage must contain exactly one Suite card for {app['id']}.")
        if app["icon"] not in rendered:
            errors.append(f"Rendered homepage does not use the reviewed Suite icon for {app['id']}.")
        if f'<strong>Description:</strong> {app["description"]}' not in rendered:
            errors.append(f"Rendered homepage description drifted for {app['id']}.")
        if f'<strong>Role:</strong> {app["role"]}' not in rendered:
            errors.append(f"Rendered homepage role drifted for {app['id']}.")
        if f'>{app["status"]}</span>' not in rendered:
            errors.append(f"Rendered homepage status drifted for {app['id']}.")

    if errors:
        print("GoreeCloud Suite validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"GoreeCloud Suite validation passed: {len(applications)} applications across {len(groups)} groups.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
