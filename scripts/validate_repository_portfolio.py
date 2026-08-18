#!/usr/bin/env python3
"""Validate the public GoreeCloud repository portfolio against its repository-only manifest."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "repository-portfolio.json"
DIRECTORY = ROOT / "repositories.html"
HOMEPAGE = ROOT / "index.html"
MAIN_JS = ROOT / "js" / "main.js"
REPOSITORY_CSS = ROOT / "css" / "repositories.css"


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    groups = data.get("groups")
    counts = data.get("counts")
    if data.get("schema_version") != 1:
        errors.append("Repository portfolio manifest must use schema_version 1.")
    if not isinstance(groups, list) or not groups:
        errors.append("Repository portfolio manifest must contain at least one group.")
        return errors
    if not isinstance(counts, dict):
        errors.append("Repository portfolio manifest must contain declared counts.")
        return errors

    names: list[str] = []
    visibilities: list[str] = []
    group_ids: list[str] = []
    for group in groups:
        if not isinstance(group, dict):
            errors.append("Every repository portfolio group must be an object.")
            continue
        group_id = group.get("id")
        label = group.get("label")
        repositories = group.get("repositories")
        if not isinstance(group_id, str) or not group_id:
            errors.append("Every repository portfolio group must have a non-empty id.")
        else:
            group_ids.append(group_id)
        if not isinstance(label, str) or not label:
            errors.append(f"Repository portfolio group {group_id!r} must have a non-empty label.")
        if not isinstance(repositories, list) or not repositories:
            errors.append(f"Repository portfolio group {group_id!r} must contain repositories.")
            continue
        for repository in repositories:
            if not isinstance(repository, dict):
                errors.append(f"Repository entry in group {group_id!r} must be an object.")
                continue
            name = repository.get("name")
            visibility = repository.get("visibility")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", name):
                errors.append(f"Invalid repository name in group {group_id!r}: {name!r}.")
                continue
            if visibility not in {"public", "private"}:
                errors.append(f"Repository {name} must declare public or private visibility.")
                continue
            names.append(name)
            visibilities.append(visibility)

    duplicate_groups = sorted(name for name, count in Counter(group_ids).items() if count > 1)
    duplicate_repositories = sorted(name for name, count in Counter(names).items() if count > 1)
    for group_id in duplicate_groups:
        errors.append(f"Duplicate repository portfolio group id: {group_id}.")
    for name in duplicate_repositories:
        errors.append(f"Duplicate repository portfolio entry: {name}.")

    computed = {
        "total": len(names),
        "public": visibilities.count("public"),
        "private": visibilities.count("private"),
        "functional_groups": len(group_ids),
    }
    for key, actual in computed.items():
        if counts.get(key) != actual:
            errors.append(
                f"Repository portfolio count {key!r} must be {actual}, found {counts.get(key)!r}."
            )

    return errors


def validate_discovery_enhancement(main_js: str, repository_css: str) -> list[str]:
    """Validate the local-only progressive repository discovery controls."""
    errors: list[str] = []
    required_js_markers = (
        "const repositoryDirectory = document.querySelector('.repo-directory-section');",
        "tools.className = 'repo-tools';",
        "searchInput.type = 'search';",
        "searchInput.autocomplete = 'off';",
        "groupSelect",
        "Repository visibility",
        "status.setAttribute('role', 'status');",
        "status.setAttribute('aria-live', 'polite');",
        "card.hidden = !matches;",
        "group.hidden = visibleInGroup === 0;",
        "directoryHeading.insertAdjacentElement('afterend', tools);",
        "not stored, added to the URL, or sent anywhere",
        "repositoryCards.length",
        "searchInput.focus();",
    )
    for marker in required_js_markers:
        if marker not in main_js:
            errors.append(f"Repository discovery enhancement is missing required behavior: {marker}")

    if "const repositoryDirectory =" in main_js:
        filter_source = main_js.split("const repositoryDirectory =", 1)[1]
        prohibited_filter_behavior = (
            "localStorage",
            "sessionStorage",
            "URLSearchParams",
            "history.pushState",
            "history.replaceState",
            "fetch(",
            "XMLHttpRequest",
            "sendBeacon",
        )
        for marker in prohibited_filter_behavior:
            if marker in filter_source:
                errors.append(
                    "Repository search/filter controls must remain local, ephemeral, and network-independent: "
                    f"{marker}"
                )

    required_css_markers = (
        ".repo-tools {",
        "min-height: var(--glaze-target-comfortable);",
        ".repo-filter-button[aria-pressed=\"true\"]",
        "@media (max-width: 1023px)",
        "@media (max-width: 599px)",
        "@media (prefers-reduced-motion: reduce)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (prefers-contrast: more)",
        "@media (forced-colors: active)",
        "@media print",
        ".repo-card[hidden], .repo-group[hidden] { display: block !important; }",
    )
    for marker in required_css_markers:
        if marker not in repository_css:
            errors.append(f"Repository discovery presentation is missing required Glaze UI behavior: {marker}")

    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "docs" / "repository-portfolio.json"
    directory_path = root / "repositories.html"
    homepage_path = root / "index.html"
    main_js_path = root / "js" / "main.js"
    repository_css_path = root / "css" / "repositories.css"

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Repository portfolio manifest cannot be read: {exc}"]

    errors.extend(validate_manifest(data))
    if errors:
        return errors

    directory = directory_path.read_text(encoding="utf-8")
    homepage = homepage_path.read_text(encoding="utf-8")
    main_js = main_js_path.read_text(encoding="utf-8")
    repository_css = repository_css_path.read_text(encoding="utf-8")
    counts = data["counts"]

    summary_markers = (
        (counts["total"], "current repositories"),
        (counts["public"], "public repositories"),
        (counts["private"], "private repositories"),
    )
    for count, label in summary_markers:
        marker = f"<strong>{count}</strong><span>{label}</span>"
        if marker not in directory:
            errors.append(f"Repository directory summary is missing current {label}: {count}.")
        if marker not in homepage:
            errors.append(f"Homepage repository summary is missing current {label}: {count}.")

    group_marker = f"<strong>{counts['functional_groups']}</strong><span>functional groups</span>"
    if group_marker not in homepage:
        errors.append(
            "Homepage repository summary is missing the current functional-group count: "
            f"{counts['functional_groups']}."
        )

    if '<section id="repositories" class="section repository-teaser">' not in homepage:
        errors.append("Homepage must publish the repository summary as static HTML.")
    if 'href="css/repositories.css"' not in homepage:
        errors.append("Homepage must load repository presentation directly for its static repository summary.")
    if 'href="repositories.html">Repositories</a>' not in homepage:
        errors.append("Homepage navigation must include a static repository-directory link.")
    if "all 28 current repositories" not in homepage:
        errors.append("Homepage software overview must identify the current 28-repository directory.")

    prohibited_runtime_inventory = (
        "repositorySection.innerHTML",
        "GoreeCloud currently maintains 20 repositories",
        "<strong>20</strong><span>current repositories</span>",
    )
    for marker in prohibited_runtime_inventory:
        if marker in main_js:
            errors.append(f"Repository inventory must not be generated from JavaScript: {marker}")

    repositories: list[tuple[str, str]] = []
    for group in data["groups"]:
        for repository in group["repositories"]:
            repositories.append((repository["name"], repository["visibility"]))

    for name, visibility in repositories:
        heading = f"<h4>{name}</h4>"
        occurrences = directory.count(heading)
        if occurrences != 1:
            errors.append(
                f"Repository directory must contain exactly one card for {name}; found {occurrences}."
            )
            continue

        card_pattern = re.compile(
            r'<article class="repo-card(?: [^"]*)?">(?P<body>.*?)</article>', re.DOTALL
        )
        card_body = None
        for match in card_pattern.finditer(directory):
            if heading in match.group("body"):
                card_body = match.group("body")
                break
        if card_body is None:
            errors.append(f"Repository {name} is not contained in a valid repo-card article.")
            continue

        visibility_marker = f'<span class="repo-visibility {visibility}">{visibility.title()}</span>'
        if visibility_marker not in card_body:
            errors.append(f"Repository {name} must display {visibility} visibility.")

        public_url = f'https://github.com/GoreeCloud/{name}'
        if visibility == "public":
            if public_url not in card_body:
                errors.append(f"Public repository {name} must link to its canonical GitHub URL.")
        elif public_url in card_body:
            errors.append(f"Private repository {name} must not publish a direct repository link.")

    stale_counts = (
        "<strong>20</strong><span>current repositories</span>",
        "<strong>16</strong><span>public repositories</span>",
        "<strong>4</strong><span>private repositories</span>",
        "all 20 current repositories",
    )
    for marker in stale_counts:
        if marker in directory or marker in homepage or marker in main_js:
            errors.append(f"Stale repository portfolio count must not remain public: {marker}")

    errors.extend(validate_discovery_enhancement(main_js, repository_css))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Repository portfolio validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Repository portfolio validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
