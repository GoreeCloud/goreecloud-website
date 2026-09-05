#!/usr/bin/env python3
"""Validate the GoreeCloud repository registry and rebuilt public source boundary."""

from __future__ import annotations

from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "repository-portfolio.json"
INDEX = ROOT / "index.html"
DIRECTORY = ROOT / "repositories.html"

PLATFORM_SYSTEMS = (
    "GoreeCloud Manager",
    "Privacy Shield",
    "Wardveil Security",
    "Everkeep",
    "Glaze UI",
    "GoreeCloud Mesh",
    "GoreeCloud Identity",
)

FOCUS_REPOSITORIES = (
    "goreecloud-home-security",
    "goreecloud-home",
    "goreecloud-ai",
    "goreecloud-containers",
    "goreecloud-code",
)

EXPECTED_CURRENT = {
    "goreecloud-app-store",
    "goreecloud-file-manager",
    "goreecloud-maps",
    "goreecloud-index",
    "goreecloud-branding-assets",
    "goreecloud-identity",
    "goreecloud-mesh",
    "goreecloud-glaze-ui",
    *FOCUS_REPOSITORIES,
}


def validate_manifest(data: dict) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    groups = data.get("groups")
    counts = data.get("counts")
    repositories: list[dict] = []

    if data.get("schema_version") != 1:
        errors.append("Repository portfolio manifest must use schema_version 1.")

    as_of = data.get("as_of")
    try:
        reviewed_date = date.fromisoformat(as_of) if isinstance(as_of, str) else None
    except ValueError:
        reviewed_date = None
    if reviewed_date is None:
        errors.append("Repository portfolio manifest must contain a valid YYYY-MM-DD as_of date.")
    elif reviewed_date > date.today():
        errors.append(f"Repository portfolio manifest as_of date must not be in the future: {as_of}.")

    if not isinstance(groups, list) or not groups:
        errors.append("Repository portfolio manifest must contain at least one group.")
        return errors, repositories
    if not isinstance(counts, dict):
        errors.append("Repository portfolio manifest must contain declared counts.")
        return errors, repositories

    group_ids: list[str] = []
    names: list[str] = []
    visibilities: list[str] = []
    for group in groups:
        if not isinstance(group, dict):
            errors.append("Every repository portfolio group must be an object.")
            continue
        group_id = group.get("id")
        label = group.get("label")
        items = group.get("repositories")
        if not isinstance(group_id, str) or not group_id.strip():
            errors.append("Every repository portfolio group must have a non-empty id.")
        else:
            group_ids.append(group_id)
        if not isinstance(label, str) or not label.strip():
            errors.append(f"Repository portfolio group {group_id!r} must have a non-empty label.")
        if not isinstance(items, list) or not items:
            errors.append(f"Repository portfolio group {group_id!r} must contain repositories.")
            continue
        for repository in items:
            if not isinstance(repository, dict):
                errors.append(f"Repository entry in group {group_id!r} must be an object.")
                continue
            name = repository.get("name")
            visibility = repository.get("visibility")
            if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
                errors.append(f"Invalid repository name in group {group_id!r}: {name!r}.")
                continue
            if visibility not in {"public", "private"}:
                errors.append(f"Repository {name} must declare public or private visibility.")
                continue
            for field in ("description", "role"):
                value = repository.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"Repository {name} must declare a non-empty {field}.")
            names.append(name)
            visibilities.append(visibility)
            repositories.append(repository)

    for group_id in sorted(name for name, count in Counter(group_ids).items() if count > 1):
        errors.append(f"Duplicate repository portfolio group id: {group_id}.")
    for name in sorted(name for name, count in Counter(names).items() if count > 1):
        errors.append(f"Duplicate repository portfolio entry: {name}.")

    computed = {
        "total": len(names),
        "public": visibilities.count("public"),
        "private": visibilities.count("private"),
        "functional_groups": len(group_ids),
    }
    for key, actual in computed.items():
        if counts.get(key) != actual:
            errors.append(f"Repository portfolio count {key!r} must be {actual}, found {counts.get(key)!r}.")

    missing = sorted(EXPECTED_CURRENT.difference(names))
    if missing:
        errors.append("Repository portfolio is missing current repositories: " + ", ".join(missing) + ".")
    if "goreecloud-logo" in names:
        errors.append("Retired goreecloud-logo repository must not remain in the current portfolio.")

    return errors, repositories


def validate_public_source(data: dict, repositories: list[dict]) -> list[str]:
    errors: list[str] = []
    homepage = INDEX.read_text(encoding="utf-8")
    directory = DIRECTORY.read_text(encoding="utf-8")
    combined = homepage + "\n" + directory

    # The rebuild intentionally removed public repository-count snapshots. Counts
    # remain internal manifest integrity fields, not copy that goes stale on Main.
    for label in ("current repositories", "public repositories", "private repositories", "functional groups"):
        if re.search(rf"\b\d+\b[^<]{{0,24}}{re.escape(label)}", combined, re.IGNORECASE):
            errors.append(f"Rebuilt public source must not hard-code repository summary counts: {label}.")

    for retired in (
        "Expanding the platform",
        "Home Assistant",
        "Frigate",
        "repo-directory-section",
        "data-repository=",
    ):
        if retired in homepage:
            errors.append(f"Rebuilt homepage contains retired portfolio composition marker: {retired}")

    for system in PLATFORM_SYSTEMS:
        if system not in homepage:
            errors.append(f"Rebuilt homepage must name current Integral Platform System: {system}.")

    by_name = {repository["name"]: repository for repository in repositories}
    for name in FOCUS_REPOSITORIES:
        record = by_name.get(name)
        if record is None:
            continue
        if name not in directory:
            errors.append(f"Focused repository page is missing current product repository: {name}.")
        url = f"https://github.com/GoreeCloud/{name}"
        if record["visibility"] == "public" and url not in directory:
            errors.append(f"Focused public repository must link to canonical source: {name}.")
        if record["visibility"] == "private" and url in directory:
            errors.append(f"Focused private repository must not publish a direct source link: {name}.")

    # No private repository in the authoritative registry may be exposed through
    # the rebuilt Main or repository-focus page merely because it exists in source.
    for repository in repositories:
        if repository["visibility"] != "private":
            continue
        url = f"https://github.com/GoreeCloud/{repository['name']}"
        if url in combined:
            errors.append(f"Private repository direct URL leaked into public source: {repository['name']}.")

    for marker in (
        "Source should be inspectable.",
        "A repository proves source, not production.",
        "Implemented",
        "Development",
        "Planned",
    ):
        if marker not in directory:
            errors.append(f"Repository page is missing source/status boundary marker: {marker}")

    return errors


def validate(root: Path = ROOT) -> list[str]:
    try:
        data = json.loads((root / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Repository portfolio manifest cannot be read: {exc}"]

    errors, repositories = validate_manifest(data)
    if not errors:
        errors.extend(validate_public_source(data, repositories))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Repository portfolio validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Repository portfolio validation passed: authoritative registry remains internally consistent; rebuilt public source exposes no hard-coded count snapshot or private repository URL.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
