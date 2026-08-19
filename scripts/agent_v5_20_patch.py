#!/usr/bin/env python3
"""Temporary branch-only helper for exact v5.20 whole-file edits.

This helper is deleted by the patch commit and must never reach main.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match for {old!r}, found {count}")
    write(path, text.replace(old, new, 1))


def insert_before_once(path: str, marker: str, addition: str) -> None:
    text = read(path)
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one insertion marker {marker!r}, found {count}")
    write(path, text.replace(marker, addition + marker, 1))


manifest_links = '''  <link rel="manifest" href="site.webmanifest">\n  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">\n  <link rel="icon" href="assets/goreecloud-icon.png" type="image/png">'''
for path in ("index.html", "repositories.html", "privacy.html", "security.html"):
    replace_once(
        path,
        '  <link rel="icon" href="assets/goreecloud-icon.png" type="image/png">',
        manifest_links,
    )

replace_once(
    "404.html",
    '  <link rel="icon" href="/assets/goreecloud-icon.png" type="image/png">',
    '  <link rel="manifest" href="/site.webmanifest">\n  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">\n  <link rel="icon" href="/assets/goreecloud-icon.png" type="image/png">',
)

for path in ("privacy.html", "security.html"):
    text = read(path)
    for stylesheet in (
        "css/status.css",
        "css/how-it-works.css",
        "css/platform.css",
        "css/roadmap.css",
        "css/development.css",
        "css/social.css",
    ):
        line = f'  <link rel="stylesheet" href="{stylesheet}">\n'
        if text.count(line) != 1:
            raise SystemExit(f"{path}: expected unused stylesheet once: {stylesheet}")
        text = text.replace(line, "", 1)
    write(path, text)

old_repo_social = '''  <meta property="og:type" content="website">\n  <meta property="og:site_name" content="GoreeCloud">\n  <meta property="og:title" content="GitHub Repositories — GoreeCloud">\n  <meta property="og:description" content="The current GoreeCloud software repository portfolio, organized by product and platform role.">\n  <meta property="og:url" content="https://www.goreecloud.com/repositories.html">\n  <meta property="og:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="GitHub Repositories — GoreeCloud">\n  <meta name="twitter:description" content="Explore GoreeCloud's current software repository portfolio.">\n  <meta name="twitter:image" content="https://www.goreecloud.com/assets/social-preview.png">'''
repo_social = '''  <meta property="og:type" content="website">\n  <meta property="og:locale" content="en_US">\n  <meta property="og:site_name" content="GoreeCloud">\n  <meta property="og:title" content="GitHub Repositories — GoreeCloud">\n  <meta property="og:description" content="The current GoreeCloud software repository portfolio, organized by product and platform role.">\n  <meta property="og:url" content="https://www.goreecloud.com/repositories.html">\n  <meta property="og:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta property="og:image:type" content="image/png">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="GoreeCloud software repository portfolio.">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:site" content="@GoreeCloud">\n  <meta name="twitter:title" content="GitHub Repositories — GoreeCloud">\n  <meta name="twitter:description" content="Explore GoreeCloud's current software repository portfolio.">\n  <meta name="twitter:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta name="twitter:image:alt" content="GoreeCloud software repository portfolio.">'''
replace_once("repositories.html", old_repo_social, repo_social)

privacy_social = '''\n  <meta property="og:type" content="website">\n  <meta property="og:locale" content="en_US">\n  <meta property="og:site_name" content="GoreeCloud">\n  <meta property="og:title" content="Privacy — GoreeCloud">\n  <meta property="og:description" content="Privacy statement for the public GoreeCloud website, including browser storage, tracking, hosting, referrer behavior, external links, and contact boundaries.">\n  <meta property="og:url" content="https://www.goreecloud.com/privacy.html">\n  <meta property="og:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta property="og:image:type" content="image/png">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="GoreeCloud public website privacy statement.">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:site" content="@GoreeCloud">\n  <meta name="twitter:title" content="Privacy — GoreeCloud">\n  <meta name="twitter:description" content="Privacy practices and browser-side data boundaries for the public GoreeCloud website.">\n  <meta name="twitter:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta name="twitter:image:alt" content="GoreeCloud public website privacy statement.">\n'''
insert_before_once("privacy.html", "</head>", privacy_social)

security_social = '''\n  <meta property="og:type" content="website">\n  <meta property="og:locale" content="en_US">\n  <meta property="og:site_name" content="GoreeCloud">\n  <meta property="og:title" content="Wardveil Security Reporting — GoreeCloud">\n  <meta property="og:description" content="Responsible security-reporting guidance for public GoreeCloud web properties and publicly available GoreeCloud software.">\n  <meta property="og:url" content="https://www.goreecloud.com/security.html">\n  <meta property="og:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta property="og:image:type" content="image/png">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="Wardveil Security by GoreeCloud responsible security reporting.">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:site" content="@GoreeCloud">\n  <meta name="twitter:title" content="Wardveil Security Reporting — GoreeCloud">\n  <meta name="twitter:description" content="Responsible security-reporting guidance for public-facing GoreeCloud properties and software.">\n  <meta name="twitter:image" content="https://www.goreecloud.com/assets/social-preview.png">\n  <meta name="twitter:image:alt" content="Wardveil Security by GoreeCloud responsible security reporting.">\n'''
insert_before_once("security.html", "</head>", security_social)

for path in ("index.html", "repositories.html"):
    text = read(path)
    replacements = (
        ("<strong>28</strong><span>current repositories</span>", "<strong>30</strong><span>current repositories</span>"),
        ("<strong>22</strong><span>public repositories</span>", "<strong>23</strong><span>public repositories</span>"),
        ("<strong>6</strong><span>private repositories</span>", "<strong>7</strong><span>private repositories</span>"),
    )
    for old, new in replacements:
        if text.count(old) != 1:
            raise SystemExit(f"{path}: expected summary marker once: {old}")
        text = text.replace(old, new, 1)
    write(path, text)

replace_once("index.html", "all 28 current repositories", "all 30 current repositories")
replace_once("index.html", "GoreeCloud currently maintains 28 repositories", "GoreeCloud currently maintains 30 repositories")
replace_once(
    "index.html",
    "spanning Glaze UI, platform administration, identity, credentials, Wardveil Security, Privacy Shield, backup, private networking, DNS, productivity, research, browser integrations, monitoring, search, feeds, media, and the public website.",
    "spanning Glaze UI, platform administration, identity, credentials, Wardveil Security, Privacy Shield, backup, private networking, DNS, productivity, private input, historical change management, research, browser integrations, monitoring, search, feeds, media, and the public website.",
)

replace_once(
    "repositories.html",
    '<div class="repo-group-heading"><span>07</span><div><p class="eyebrow">Productivity &amp; personal information</p><h3>Private everyday applications</h3></div></div>',
    '<div class="repo-group-heading"><span>07</span><div><p class="eyebrow">Productivity, input &amp; personal information</p><h3>Private everyday applications and on-device input</h3></div></div>',
)
keyboard_card = '''            <article class="repo-card"><div class="repo-card-top"><span class="repo-mark">KB</span><span class="repo-visibility public">Public</span></div><h4>goreecloud-keyboard</h4><p>GoreeCloud-maintained Android keyboard project based on CleverKeys.</p><dl><div><dt>Purpose</dt><dd>Develop private on-device text input with swipe typing, dictionaries, clipboard productivity, and GoreeCloud-specific workflows.</dd></div><div><dt>Role</dt><dd>Android input method and productivity client under active development.</dd></div></dl><a href="https://github.com/GoreeCloud/goreecloud-keyboard" target="_blank" rel="noopener noreferrer">View repository →</a></article>\n'''
group_08_marker = '        <div class="repo-group">\n          <div class="repo-group-heading"><span>08</span><div><p class="eyebrow">Notifications &amp; monitoring</p><h3>Know when something changes or fails</h3></div></div>'
repo_text = read("repositories.html")
boundary = "          </div>\n        </div>\n\n" + group_08_marker
if repo_text.count(boundary) != 1:
    raise SystemExit("repositories.html: group 07/08 boundary not unique")
repo_text = repo_text.replace(boundary, keyboard_card + boundary, 1)
write("repositories.html", repo_text)
replace_once(
    "repositories.html",
    '<div class="repo-group-heading"><span>08</span><div><p class="eyebrow">Notifications &amp; monitoring</p><h3>Know when something changes or fails</h3></div></div>',
    '<div class="repo-group-heading"><span>08</span><div><p class="eyebrow">Operations, notifications &amp; monitoring</p><h3>Preserve operational history and know when something changes or fails</h3></div></div>',
)
changelog_card = '''            <article class="repo-card"><div class="repo-card-top"><span class="repo-mark">CH</span><span class="repo-visibility private">Private</span></div><h4>goreecloud-changelogs</h4><p>Native GoreeCloud historical change-ledger application in active development.</p><dl><div><dt>Purpose</dt><dd>Build searchable, append-only GoreeCloud change history across web, API, import/export, and future mobile workflows.</dd></div><div><dt>Role</dt><dd>Historical change-management platform; production migration and acceptance remain pending.</dd></div></dl><span class="repo-private-note">Private development repository • migration pending</span></article>\n'''
insert_before_once(
    "repositories.html",
    '            <article class="repo-card"><div class="repo-card-top"><span class="repo-mark">NF</span>',
    changelog_card,
)

manifest_path = ROOT / "site.webmanifest"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["shortcuts"] = [
    {"name": "Repositories", "short_name": "Repositories", "url": "/repositories.html"},
    {"name": "Privacy", "short_name": "Privacy", "url": "/privacy.html"},
    {"name": "Security", "short_name": "Security", "url": "/security.html"},
]
manifest["prefer_related_applications"] = False
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

perf_path = "scripts/validate_performance_budget.py"
replace_once(
    perf_path,
    "MAX_HOMEPAGE_STYLESHEETS = 10\nMAX_HOMEPAGE_SCRIPTS = 3",
    '''MAX_STYLESHEETS_BY_PAGE = {\n    "index.html": 10,\n    "repositories.html": 4,\n    "privacy.html": 3,\n    "security.html": 3,\n    "404.html": 4,\n}\nMAX_SCRIPTS_BY_PAGE = {\n    "index.html": 2,\n    "repositories.html": 2,\n    "privacy.html": 1,\n    "security.html": 1,\n    "404.html": 1,\n}''',
)
replace_once(
    perf_path,
    '''        if path.name == "index.html":\n            if parser.stylesheet_count > MAX_HOMEPAGE_STYLESHEETS:\n                errors.append(\n                    f"Homepage stylesheet request count exceeds {MAX_HOMEPAGE_STYLESHEETS}: "\n                    f"found {parser.stylesheet_count}."\n                )\n            if parser.script_count > MAX_HOMEPAGE_SCRIPTS:\n                errors.append(\n                    f"Homepage script request count exceeds {MAX_HOMEPAGE_SCRIPTS}: found {parser.script_count}."\n                )''',
    '''        stylesheet_limit = MAX_STYLESHEETS_BY_PAGE[path.name]\n        script_limit = MAX_SCRIPTS_BY_PAGE[path.name]\n        if parser.stylesheet_count > stylesheet_limit:\n            errors.append(\n                f"{path.name} stylesheet request count exceeds {stylesheet_limit}: "\n                f"found {parser.stylesheet_count}."\n            )\n        if parser.script_count > script_limit:\n            errors.append(\n                f"{path.name} script request count exceeds {script_limit}: found {parser.script_count}."\n            )''',
)

surface_path = "scripts/validate_public_surface.py"
replace_once(
    surface_path,
    'CANONICAL_SITEMAP_URL = "https://www.goreecloud.com/sitemap.xml"\nSITEMAP_NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"',
    'CANONICAL_SITEMAP_URL = "https://www.goreecloud.com/sitemap.xml"\nSOCIAL_IMAGE_URL = "https://www.goreecloud.com/assets/social-preview.png"\nSITEMAP_NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"',
)
replace_once(
    surface_path,
    '''        self.canonical: str | None = None\n        self.robots: str | None = None''',
    '''        self.canonical: str | None = None\n        self.robots: str | None = None\n        self.meta_names: dict[str, str] = {}\n        self.meta_properties: dict[str, str] = {}\n        self.manifest_href: str | None = None\n        self.icon_links: list[tuple[set[str], str, str]] = []''',
)
replace_once(
    surface_path,
    '''        if tag == "link" and "canonical" in attrs.get("rel", "").split():\n            self.canonical = attrs.get("href")\n        if tag == "meta" and attrs.get("name", "").lower() == "robots":\n            self.robots = attrs.get("content")''',
    '''        if tag == "link":\n            rels = set(attrs.get("rel", "").lower().split())\n            if "canonical" in rels:\n                self.canonical = attrs.get("href")\n            if "manifest" in rels:\n                self.manifest_href = attrs.get("href")\n            if rels.intersection({"icon", "apple-touch-icon"}):\n                self.icon_links.append((rels, attrs.get("href", ""), attrs.get("type", "")))\n        if tag == "meta":\n            name = attrs.get("name", "").lower()\n            prop = attrs.get("property", "").lower()\n            if name:\n                self.meta_names[name] = attrs.get("content", "")\n            if prop:\n                self.meta_properties[prop] = attrs.get("content", "")\n            if name == "robots":\n                self.robots = attrs.get("content")''',
)
metadata_function = r'''

def validate_page_metadata(errors: list[str], parsed_pages: dict[Path, PublicPageParser]) -> None:
    for page in PUBLIC_PAGES:
        parser = parsed_pages.get(page.resolve())
        if parser is None:
            continue
        display = page.relative_to(ROOT)
        manifest_href = (parser.manifest_href or "").lstrip("/")
        if manifest_href != "site.webmanifest":
            errors.append(f"{display} must link to the local site.webmanifest.")
        normalized_icons = {
            (frozenset(rels), href.lstrip("/"), content_type)
            for rels, href, content_type in parser.icon_links
        }
        if not any("icon" in rels and href == "assets/favicon.svg" and content_type == "image/svg+xml" for rels, href, content_type in normalized_icons):
            errors.append(f"{display} must publish the local SVG favicon.")
        if not any("icon" in rels and href == "assets/goreecloud-icon.png" and content_type == "image/png" for rels, href, content_type in normalized_icons):
            errors.append(f"{display} must publish the PNG favicon fallback.")
        if not any("apple-touch-icon" in rels and href == "assets/goreecloud-icon.png" for rels, href, _ in normalized_icons):
            errors.append(f"{display} must publish the local Apple touch icon.")

    for page, canonical in INDEXABLE_PAGES.items():
        parser = parsed_pages.get(page.resolve())
        if parser is None:
            continue
        display = page.relative_to(ROOT)
        expected_properties = {
            "og:type": "website",
            "og:locale": "en_US",
            "og:site_name": "GoreeCloud",
            "og:url": canonical,
            "og:image": SOCIAL_IMAGE_URL,
            "og:image:type": "image/png",
            "og:image:width": "1200",
            "og:image:height": "630",
        }
        for key, expected in expected_properties.items():
            if parser.meta_properties.get(key) != expected:
                errors.append(f"{display} metadata {key} must be {expected!r}.")
        for key in ("og:title", "og:description", "og:image:alt"):
            if not parser.meta_properties.get(key, "").strip():
                errors.append(f"{display} must publish non-empty {key} metadata.")
        expected_names = {
            "twitter:card": "summary_large_image",
            "twitter:site": "@GoreeCloud",
            "twitter:image": SOCIAL_IMAGE_URL,
        }
        for key, expected in expected_names.items():
            if parser.meta_names.get(key) != expected:
                errors.append(f"{display} metadata {key} must be {expected!r}.")
        for key in ("twitter:title", "twitter:description", "twitter:image:alt"):
            if not parser.meta_names.get(key, "").strip():
                errors.append(f"{display} must publish non-empty {key} metadata.")
'''
insert_before_once(surface_path, "\ndef validate_sitemap(errors: list[str]) -> None:", metadata_function)
replace_once(
    surface_path,
    "    validate_indexing(errors, parsed_pages)\n    validate_sitemap(errors)",
    "    validate_indexing(errors, parsed_pages)\n    validate_page_metadata(errors, parsed_pages)\n    validate_sitemap(errors)",
)

replace_once(
    "tests/test_repository_portfolio.py",
    "import copy\nimport json",
    "import copy\nfrom datetime import date, timedelta\nimport json",
)
extra_tests = '''\n    def test_manifest_review_date_must_be_valid_and_not_future(self) -> None:\n        data = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))\n        mutated = copy.deepcopy(data)\n        mutated["as_of"] = (date.today() + timedelta(days=1)).isoformat()\n        errors = portfolio.validate_manifest(mutated)\n        self.assertTrue(any("must not be in the future" in error for error in errors))\n\n    def test_rendered_summary_rejects_stale_counts(self) -> None:\n        counts = json.loads((ROOT / "docs" / "repository-portfolio.json").read_text(encoding="utf-8"))["counts"]\n        stale = '<strong>28</strong><span>current repositories</span>'\n        errors = portfolio.validate_summary_counts(stale, counts, "Test")\n        self.assertTrue(any("stale current repositories" in error for error in errors))\n'''
insert_before_once("tests/test_repository_portfolio.py", '\n\nif __name__ == "__main__":', extra_tests)
replace_once(
    "tests/test_project_portfolio_contract.py",
    'self.assertIn("all 28 current repositories", INDEX)',
    'self.assertIn("all 30 current repositories", INDEX)',
)

write("VERSION", "5.20.0\n")
replace_once(
    "README.md",
    "Current website package: **v5.19.0 — Glaze UI 1.1 exact-version conformance and safe-area semantics**",
    "Current website package: **v5.20.0 — repository portfolio reconciliation, metadata hardening, and ancillary-page request optimization**",
)
replace_once(
    "README.md",
    "The authenticated GoreeCloud repository inventory currently contains **28 repositories: 22 public and 6 private**.",
    "The authenticated GoreeCloud repository inventory currently contains **30 repositories: 23 public and 7 private**.",
)
replace_once(
    "README.md",
    "GoreeCloud Tasks, GoreeCloud Contacts, GoreeCloud Notify, GoreeCloud Wardveil Security, GoreeCloud Privacy Shield, and the `goreecloud-website` deployment-source repository remain private",
    "GoreeCloud Tasks, GoreeCloud Contacts, GoreeCloud Notify, GoreeCloud Changelogs, GoreeCloud Wardveil Security, GoreeCloud Privacy Shield, and the `goreecloud-website` deployment-source repository remain private",
)
replace_once("README.md", "GoreeCloud Gallery; and this website.", "GoreeCloud Gallery; GoreeCloud Keyboard; GoreeCloud Changelogs; and this website.")
replace_once(
    "README.md",
    "The 5.19.0 candidate preserves the site's established visual identity, 5.18.0 local repository discovery, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections.",
    "The 5.20.0 candidate preserves the site's established visual identity and exact Glaze UI 1.1 contract, plus the 5.18.0 local repository discovery, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections.",
)
insert_before_once(
    "README.md",
    "\nPublic source availability does not imply production acceptance.",
    "\nThe v5.20.0 release also links the already-deployed local web manifest and dual SVG/PNG favicon identity from every human-facing page, completes Open Graph/Twitter metadata across every indexable page, and enforces page-specific stylesheet/script request ceilings. Privacy and security pages now load only the shared styles they actually use. These are static presentation and delivery improvements; they do not add browser telemetry, a service worker, a backend, or new network requests.\n",
)
replace_once(
    "README.md",
    "The v5.19.0 Glaze UI alignment does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
    "The v5.20.0 portfolio and metadata release does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
)

baseline = read("docs/stability-baseline.md")
baseline = baseline.replace("The repository-defined release version is **5.19.0**.", "The repository-defined release version is **5.20.0**.", 1)
scope_pattern = re.compile(r"## 5\.19\.0 scope\n.*?(?=\n## Glaze UI 1\.1 stable-release boundary)", re.DOTALL)
scope = '''## 5.20.0 scope

Version 5.20.0 reconciles the public repository portfolio with the authenticated GoreeCloud GitHub inventory and strengthens browser metadata and request-efficiency controls while preserving the production-verified Glaze UI 1.1, privacy, security, runtime-status, and isolated-publication boundaries.

The release:

- records **30 current repositories: 23 public and 7 private**, while preserving 11 functional groups;
- adds the public `goreecloud-keyboard` repository to the productivity/input group without implying production acceptance;
- adds the private `goreecloud-changelogs` repository to the operations group with its production migration and acceptance boundary stated explicitly;
- advances the repository manifest review date to August 19, 2026 and validates that the review date is valid and not future-dated;
- removes the hard-coded 28-repository validator assumption and makes rendered count/overview checks derive from the repository manifest, including rejection of conflicting stale counts;
- links the local `site.webmanifest`, SVG favicon, PNG fallback, and Apple touch icon consistently from all five human-facing public pages;
- completes page-specific Open Graph and Twitter metadata across every indexable page and validates canonical social URL/image identity;
- adds local manifest shortcuts for repositories, privacy, and security without introducing a service worker or remote dependency;
- reduces the Privacy and Security pages from nine stylesheet requests to the three shared Glaze UI/style layers they actually use;
- replaces the homepage-only request ceiling with page-specific stylesheet and script ceilings for every human-facing page;
- preserves the existing HTML, CSS, JavaScript, image, and 512 KiB total artifact budgets without increasing any ceiling;
- preserves the exact Glaze UI 1.1.0 conformance pin at `5c8320de4f770614a3e2bcf9de2a27f7fcfd920c`;
- preserves the v5.18.0 local repository discovery controls and their local-only, ephemeral, no-network/no-storage behavior;
- preserves the v5.17.0 Memos, Notify/ntfy, Search, and Monitoring/Uptime Kuma runtime-status boundaries;
- preserves Wardveil Security reporting, `security@goreecloud.com`, the self-only browser-origin model, `connect-src 'none'`, and telemetry-free operation;
- preserves the exact allowlisted Cloudflare `dist/` publication model and exact branch-preview/production deployment verification requirement.
'''
baseline, count = scope_pattern.subn(scope.rstrip(), baseline, count=1)
if count != 1:
    raise SystemExit(f"docs/stability-baseline.md: expected one v5.19 scope block, found {count}")
baseline = baseline.replace(
    "The v5.19.0 Glaze UI alignment does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
    "The v5.20.0 portfolio and metadata release does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
    1,
)
write("docs/stability-baseline.md", baseline)

for temporary in (
    ".github/workflows/agent-v5-20-patch.yml",
    ".github/workflows/agent-v5-20-pr-patch.yml",
    "scripts/agent_v5_20_patch.py",
):
    candidate = ROOT / temporary
    if candidate.exists():
        candidate.unlink()
