#!/usr/bin/env python3
"""Render repository-portfolio public HTML from reviewed build-time public facts."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "repository-portfolio.json"

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

MEMOS_SERVICE_SOURCE = (
    'A lightweight GoreeCloud quick-note capture application for fast, focused notes when a full '
    'knowledge workspace is unnecessary. GoreeCloud Memos v0.1.2 is the accepted Stable production service.'
)
MEMOS_SERVICE_PUBLIC = (
    'A lightweight GoreeCloud quick-note capture application for fast, focused notes when a full '
    'knowledge workspace is unnecessary. GoreeCloud Memos v0.1.3 is the accepted Stable production '
    'web/server release while newer client acceptance work continues separately.'
)
MEMOS_PROJECT_SOURCE = (
    'Maintained lightweight quick-note capture application for fast, focused note entry when a full '
    'knowledge workspace is unnecessary. GoreeCloud Memos v0.1.2 is the accepted Stable production service.'
)
MEMOS_PROJECT_PUBLIC = (
    'Maintained lightweight quick-note capture application for fast, focused note entry. GoreeCloud '
    'Memos v0.1.3 is the accepted Stable production web/server release; newer native-client acceptance '
    'remains separate.'
)
FOOTER_PLATFORM_SOURCE = (
    '<p class="footer-glaze"><strong>Glaze UI</strong> design • <strong>Privacy Shield</strong> privacy • '
    '<strong>Wardveil Security</strong> security.</p>'
)
FOOTER_PLATFORM_PUBLIC = (
    '<p class="footer-glaze"><strong>Glaze UI</strong> design • <strong>Privacy Shield</strong> privacy • '
    '<strong>Wardveil Security</strong> security • <strong>Everkeep</strong> resilience &amp; preservation.</p>'
)


def load_manifest(root: Path = ROOT) -> dict:
    return json.loads((root / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))


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
    return source


def _replace_once(rendered: str, old: str, new: str, marker: str) -> str:
    if rendered.count(old) != 1:
        raise ValueError(f"homepage public-fact marker could not be resolved exactly once: {marker}")
    return rendered.replace(old, new, 1)


def render_homepage(source: str, manifest: dict) -> str:
    counts = manifest["counts"]
    rendered = source

    rendered = _replace_once(
        rendered,
        MEMOS_SERVICE_SOURCE,
        MEMOS_SERVICE_PUBLIC,
        "Memos service status",
    )
    rendered = _replace_once(
        rendered,
        '<span class="badge active">Available Now</span>\n          </article>\n\n          <article class="service-card" data-service="element">',
        '<span class="badge active">Stable 0.1.3</span>\n          </article>\n\n          <article class="service-card" data-service="element">',
        "Memos service badge",
    )
    rendered = _replace_once(
        rendered,
        MEMOS_PROJECT_SOURCE,
        MEMOS_PROJECT_PUBLIC,
        "Memos project status",
    )
    rendered = _replace_once(
        rendered,
        '<small>Stable production v0.1.2</small>',
        '<small>Stable production web/server v0.1.3</small>',
        "Memos project lifecycle",
    )
    rendered = _replace_once(
        rendered,
        FOOTER_PLATFORM_SOURCE,
        FOOTER_PLATFORM_PUBLIC,
        "platform footer",
    )

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
    return source
