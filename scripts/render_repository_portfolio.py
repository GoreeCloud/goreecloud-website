#!/usr/bin/env python3
"""Render reviewed GoreeCloud public portfolio data into deployable HTML."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "repository-portfolio.json"
SUITE_MANIFEST = ROOT / "docs" / "suite-portfolio.json"

SUMMARY_PATTERNS = {
    "total": re.compile(r"<strong>\d+</strong><span>current repositories</span>"),
    "public": re.compile(r"<strong>\d+</strong><span>public repositories</span>"),
    "private": re.compile(r"<strong>\d+</strong><span>private repositories</span>"),
    "functional_groups": re.compile(r"<strong>\d+</strong><span>functional groups</span>"),
}

DIRECTORY_GROUP_BLOCK = re.compile(
    r'(?P<indent>\s*)<div class="repo-group">.*?(?=\n      </div>\n    </section>)',
    re.DOTALL,
)
DIRECTORY_SUMMARY = re.compile(
    r'<aside class="repo-summary" aria-label="Repository summary">.*?</aside>',
    re.DOTALL,
)
HOMEPAGE_TEASER = re.compile(
    r'<p>GoreeCloud currently maintains \d+ repositories spanning.*?</p>',
    re.DOTALL,
)
SUITE_SECTION = re.compile(
    r'    <section id="services" class="section">.*?(?=\n    <section id="how-it-works")',
    re.DOTALL,
)
PLATFORM_SECTION = re.compile(
    r'\n    <section id="platform" class="section platform-section">.*?(?=\n    <section id="development")',
    re.DOTALL,
)
PLATFORM_NAVIGATION = re.compile(
    r'\s*<a href="(?:index\.html)?#platform">Platform</a>',
)


def load_manifest(root: Path = ROOT) -> dict:
    return json.loads((root / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))


def load_suite_manifest(root: Path = ROOT) -> dict:
    return json.loads((root / "docs" / "suite-portfolio.json").read_text(encoding="utf-8"))


def _mark(name: str) -> str:
    if name == "GoreeCloud":
        return "GC"
    base = name.removeprefix("goreecloud-")
    parts = [part for part in re.split(r"[-_]", base) if part]
    if len(parts) == 1:
        return parts[0][:2].upper()
    return "".join(part[0] for part in parts[:3]).upper()


def _card(repository: dict) -> str:
    name = repository["name"]
    visibility = repository["visibility"]
    description = escape(repository["description"])
    role = escape(repository["role"])
    featured = " featured" if name in {"glaze-ui", "goreecloud-manager", "goreecloud-drive"} else ""
    link = (
        f'<a href="https://github.com/GoreeCloud/{escape(name)}" target="_blank" '
        'rel="noopener noreferrer">View repository →</a>'
        if visibility == "public"
        else '<span class="repo-private-note">Private GoreeCloud repository</span>'
    )
    return (
        f'<article class="repo-card{featured}">'
        f'<div class="repo-card-top"><span class="repo-mark">{_mark(name)}</span>'
        f'<span class="repo-visibility {visibility}">{visibility.title()}</span></div>'
        f'<h4>{escape(name)}</h4><p>{description}</p>'
        f'<p class="repo-role"><strong>Role:</strong> {role}</p>{link}</article>'
    )


def _groups(manifest: dict) -> str:
    rendered: list[str] = []
    for number, group in enumerate(manifest["groups"], start=1):
        label = escape(group["label"])
        cards = "\n".join(f"            {_card(repo)}" for repo in group["repositories"])
        rendered.append(
            "        <div class=\"repo-group\">\n"
            f"          <div class=\"repo-group-heading\"><span>{number:02d}</span>"
            f"<div><p class=\"eyebrow\">{label}</p><h3>{label}</h3></div></div>\n"
            "          <div class=\"repo-grid\">\n"
            f"{cards}\n"
            "          </div>\n"
            "        </div>"
        )
    rendered.append(
        '        <div class="repo-footnote glaze-callout"><div>'
        '<span class="glaze-chip">Portfolio principle</span>'
        '<h3>Everything GoreeCloud builds belongs in source control.</h3></div>'
        '<p>Repository visibility does not determine runtime maturity. A public listing does not '
        'by itself establish release, deployment, production acceptance, or Stable status; each '
        "project's specification and release evidence remain authoritative.</p></div>"
    )
    return "\n\n".join(rendered) + "\n"


def _suite_card(application: dict) -> str:
    return (
        f'<article class="service-card suite-card" data-suite-app="{escape(application["id"])}">\n'
        f'  <div class="service-art suite-art" aria-hidden="true"><img src="{escape(application["icon"])}" alt="" width="52" height="52"></div>\n'
        f'  <h3>{escape(application["name"])}</h3>\n'
        f'  <p class="suite-description"><strong>Description:</strong> {escape(application["description"])}</p>\n'
        f'  <p class="suite-role"><strong>Role:</strong> {escape(application["role"])}</p>\n'
        f'  <span class="badge {escape(application["status_class"])}">{escape(application["status"])}</span>\n'
        '</article>'
    )


def _suite_section(manifest: dict) -> str:
    groups: list[str] = []
    for group in manifest["groups"]:
        group_id = f'suite-group-{escape(group["id"])}'
        cards = "\n".join(f"            {_suite_card(app)}" for app in group["applications"])
        groups.append(
            f'        <section class="suite-group" aria-labelledby="{group_id}">\n'
            f'          <div class="suite-group-heading"><p class="eyebrow">{escape(group["label"])}</p><h3 id="{group_id}">{escape(group["label"])}</h3></div>\n'
            '          <div class="service-grid suite-grid">\n'
            f'{cards}\n'
            '          </div>\n'
            '        </section>'
        )

    return (
        '    <section id="services" class="section suite-section">\n'
        '      <div class="container">\n'
        '        <div class="section-heading suite-heading">\n'
        f'          <p class="eyebrow">{escape(manifest["section_title"])}</p>\n'
        '          <h2>First-party applications for the complete GoreeCloud experience.</h2>\n'
        f'          <p>{escape(manifest["section_description"])}</p>\n'
        '        </div>\n\n'
        + "\n\n".join(groups)
        + '\n\n        <p class="status-note suite-note">Status labels describe GoreeCloud lifecycle and acceptance state, not upstream project maturity. A source repository, milestone, beta, or release-candidate label does not imply production approval unless the card explicitly states a Stable or current-service status.</p>\n'
        '      </div>\n'
        '    </section>\n'
    )


def _remove_platform_navigation(source: str) -> str:
    return PLATFORM_NAVIGATION.sub("", source)


def render_repository_directory(source: str, manifest: dict) -> str:
    counts = manifest["counts"]
    summary = (
        '<aside class="repo-summary" aria-label="Repository summary">'
        f'<div><strong>{counts["total"]}</strong><span>current repositories</span></div>'
        f'<div><strong>{counts["public"]}</strong><span>public repositories</span></div>'
        f'<div><strong>{counts["private"]}</strong><span>private repositories</span></div>'
        '<p>Historical redirect names are not counted separately.</p></aside>'
    )
    source, summary_replacements = DIRECTORY_SUMMARY.subn(summary, source, count=1)
    if summary_replacements != 1:
        raise ValueError("repository directory summary template could not be resolved")

    source, group_replacements = DIRECTORY_GROUP_BLOCK.subn(_groups(manifest), source, count=1)
    if group_replacements != 1:
        raise ValueError("repository directory group template could not be resolved")
    return _remove_platform_navigation(source)


def render_homepage(source: str, manifest: dict, suite_manifest: dict | None = None) -> str:
    counts = manifest["counts"]
    suite_manifest = suite_manifest or load_suite_manifest(ROOT)
    rendered = source

    rendered, suite_replacements = SUITE_SECTION.subn(_suite_section(suite_manifest), rendered, count=1)
    if suite_replacements != 1:
        raise ValueError("homepage GoreeCloud Suite template could not be resolved")
    rendered = rendered.replace('<a href="#services">Services</a>', '<a href="#services">Suite</a>')

    rendered, platform_replacements = PLATFORM_SECTION.subn("", rendered, count=1)
    if platform_replacements != 1:
        raise ValueError("homepage Platform Foundation section could not be resolved")
    rendered = _remove_platform_navigation(rendered)
    rendered = rendered.replace('  <link rel="stylesheet" href="css/platform.css">\n', '')

    rendered = re.sub(
        r"all \d+ current repositories",
        f'all {counts["total"]} current repositories',
        rendered,
    )
    rendered = re.sub(
        r"GoreeCloud currently maintains \d+ repositories",
        f'GoreeCloud currently maintains {counts["total"]} repositories',
        rendered,
    )
    current_teaser = (
        f'<p>GoreeCloud currently maintains {counts["total"]} repositories across first-party '
        'applications, maintained forks, shared platform foundations, design, identity, security, '
        'privacy, resilience, networking, storage, media, productivity, developer tooling, and '
        'public-presence work. The dedicated directory explains each repository at a public-safe '
        'level while preserving private source and lifecycle boundaries.</p>'
    )
    rendered, teaser_replacements = HOMEPAGE_TEASER.subn(current_teaser, rendered, count=1)
    if teaser_replacements != 1:
        raise ValueError("homepage repository teaser template could not be resolved")

    labels = {
        "total": "current repositories",
        "public": "public repositories",
        "private": "private repositories",
        "functional_groups": "functional groups",
    }
    for key, pattern in SUMMARY_PATTERNS.items():
        rendered, replacement_count = pattern.subn(
            f'<strong>{counts[key]}</strong><span>{labels[key]}</span>',
            rendered,
            count=1,
        )
        if replacement_count != 1:
            raise ValueError(f"homepage repository summary marker could not be resolved: {key}")
    return rendered


def render_public_file(relative: str, source: str, manifest: dict) -> str:
    if relative == "index.html":
        return render_homepage(source, manifest)
    if relative == "repositories.html":
        return render_repository_directory(source, manifest)
    if relative.endswith(".html"):
        return _remove_platform_navigation(source)
    return source
