#!/usr/bin/env python3
"""Apply the one-time GoreeCloud Website v5.21 native platform-mark migration.

This helper is intentionally temporary and is removed by the branch-only patch workflow
in the same commit that applies the release changes.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match in {path.relative_to(ROOT)}; found {count}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_once(path: Path, pattern: str, replacement: str, *, flags: int = 0) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"Expected exactly one regex match in {path.relative_to(ROOT)}; found {count}: {pattern[:100]!r}")
    path.write_text(updated, encoding="utf-8")


def patch_index() -> None:
    path = ROOT / "index.html"
    logo_marks = {
        "assets/platform/proxmox.svg": "PX",
        "assets/platform/debian.svg": "DE",
        "assets/platform/docker.svg": "DK",
        "assets/platform/netbird.svg": "NB",
        "assets/platform/adguard-home.svg": "AH",
        "assets/platform/caddy.svg": "CY",
        "assets/platform/beszel.svg": "BZ",
        "assets/platform/uptime-kuma.svg": "UK",
    }
    text = path.read_text(encoding="utf-8")
    for asset, mark in logo_marks.items():
        pattern = re.compile(
            r'(?P<indent>\s*)<a class="platform-logo-link(?: netbird)?" href="(?P<href>[^"]+)" target="_blank" rel="noopener noreferrer" aria-label="(?P<label>[^"]+)">\s*'
            + r'<img src="' + re.escape(asset) + r'"[^>]*>\s*</a>'
        )
        replacement = (
            r'\g<indent><a class="platform-mark" href="\g<href>" target="_blank" '
            r'rel="noopener noreferrer" aria-label="\g<label>">' + mark + r'</a>'
        )
        text, count = pattern.subn(replacement, text, count=1)
        if count != 1:
            raise SystemExit(f"Expected exactly one homepage platform logo for {asset}; found {count}.")

    native_links = {
        "https://github.com/GoreeCloud/goreecloud-monitor": ("GoreeCloud Monitor public repository", "GM"),
        "https://github.com/GoreeCloud/goreecloud-search": ("GoreeCloud Search public repository", "GS"),
    }
    for href, (label, mark) in native_links.items():
        pattern = re.compile(
            r'(?P<indent>\s*)<a class="platform-logo-link" href="' + re.escape(href) +
            r'" target="_blank" rel="noopener noreferrer" aria-label="' + re.escape(label) +
            r'">\s*<span class="platform-native-mark" aria-hidden="true">' + mark + r'</span>\s*</a>'
        )
        replacement = (
            r'\g<indent><a class="platform-mark" href="' + href + r'" target="_blank" '
            r'rel="noopener noreferrer" aria-label="' + label + r'">' + mark + r'</a>'
        )
        text, count = pattern.subn(replacement, text, count=1)
        if count != 1:
            raise SystemExit(f"Expected exactly one native platform link for {href}; found {count}.")

    old_notify = '<span class="platform-native-mark" aria-hidden="true">GN</span>'
    if text.count(old_notify) != 1:
        raise SystemExit(f"Expected exactly one GoreeCloud Notify platform mark; found {text.count(old_notify)}.")
    text = text.replace(old_notify, '<span class="platform-mark" aria-hidden="true">GN</span>', 1)

    old_legal = '<p class="platform-legal">Third-party logos identify their respective technologies and remain the property of their respective owners. This is a representative public foundation, not a complete infrastructure inventory.</p>'
    new_legal = '<p class="platform-legal">Technology names identify the referenced open-source projects. GoreeCloud uses native Glaze UI text marks in this section instead of redistributing third-party logo artwork. This is a representative public foundation, not a complete infrastructure inventory.</p>'
    if text.count(old_legal) != 1:
        raise SystemExit("Expected the v5.20 platform legal note exactly once.")
    text = text.replace(old_legal, new_legal, 1)

    if "assets/platform/" in text:
        raise SystemExit("Homepage still references third-party platform artwork after migration.")
    if "platform-logo-link" in text or "platform-native-mark" in text:
        raise SystemExit("Homepage still contains legacy platform-mark classes after migration.")
    if text.count('class="platform-mark"') != 11:
        raise SystemExit(f"Expected 11 unified platform marks; found {text.count('class=\"platform-mark\"')}.")

    path.write_text(text, encoding="utf-8")


def patch_platform_css() -> None:
    path = ROOT / "css" / "platform.css"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\.platform-logo-link,\n\.platform-native-mark \{.*?\.platform-logo-link\.netbird img \{\n  width: 42px;\n  height: auto;\n\}\n",
        re.DOTALL,
    )
    replacement = """.platform-mark {
  width: 58px;
  height: 58px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  border: 1px solid color-mix(in srgb, var(--blue) 20%, var(--border));
  border-radius: 15px;
  background: color-mix(in srgb, var(--glaze-surface-strong) 72%, transparent);
  color: var(--cyan);
  font-size: .8rem;
  font-weight: 900;
  letter-spacing: .06em;
  text-decoration: none;
}

a.platform-mark:hover,
a.platform-mark:focus-visible {
  border-color: color-mix(in srgb, var(--cyan) 40%, var(--border));
  background: var(--glaze-surface-strong);
  color: var(--text);
}
"""
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Expected one legacy platform-mark CSS block; found {count}.")
    text = text.replace("  .platform-logo-link,\n  .platform-native-mark,\n", "  .platform-mark,\n")
    if "platform-logo-link" in text or "platform-native-mark" in text:
        raise SystemExit("Legacy platform-mark CSS selectors remain after migration.")
    path.write_text(text, encoding="utf-8")


def patch_build_allowlist() -> None:
    path = ROOT / "scripts" / "build_public_site.py"
    text = path.read_text(encoding="utf-8")
    start = text.index("PUBLIC_ASSET_FILES = (\n")
    end = text.index(")\n\n# Glaze UI and page-specific presentation layers.", start) + 2
    replacement = """PUBLIC_ASSET_FILES = (
    "assets/favicon.svg",
    "assets/goreecloud-icon.png",
    "assets/social-preview.png",
)
"""
    text = text[:start] + replacement + text[end:]
    if "assets/platform/" in text:
        raise SystemExit("Build allowlist still contains third-party platform artwork.")
    path.write_text(text, encoding="utf-8")


def write_public_asset_validator() -> None:
    path = ROOT / "scripts" / "validate_public_assets.py"
    path.write_text('''#!/usr/bin/env python3
"""Validate the GoreeCloud website public-artwork rights and integrity boundary."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from build_public_site import PUBLIC_ASSET_FILES, ROOT

EXPECTED_PUBLIC_ASSETS = (
    "assets/favicon.svg",
    "assets/goreecloud-icon.png",
    "assets/social-preview.png",
)
EXPECTED_BLOBS = {
    "assets/favicon.svg": "1e578573f8f753f0d51e616284546b42f67012da",
    "assets/goreecloud-icon.png": "5ae9000d1404239ef362f42f109e3d7de3557d38",
    "assets/social-preview.png": "64aaf437835b31a8473292487cf57366bb58c4fa",
}
INVENTORY = ROOT / "docs" / "public-asset-inventory.md"
INDEX = ROOT / "index.html"
PLATFORM_DIR = ROOT / "assets" / "platform"


def git_blob_id(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def validate() -> list[str]:
    errors: list[str] = []
    if tuple(PUBLIC_ASSET_FILES) != EXPECTED_PUBLIC_ASSETS:
        errors.append(
            "Public artwork allowlist must contain exactly the three reviewed GoreeCloud identity assets; "
            f"found {tuple(PUBLIC_ASSET_FILES)!r}."
        )

    for relative, expected_blob in EXPECTED_BLOBS.items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"Reviewed GoreeCloud public asset must be a regular file: {relative}")
            continue
        actual_blob = git_blob_id(path)
        if actual_blob != expected_blob:
            errors.append(
                f"Reviewed GoreeCloud public asset changed without inventory review: {relative}; "
                f"expected Git blob {expected_blob}, found {actual_blob}."
            )

    if PLATFORM_DIR.exists():
        current_platform_files = sorted(
            str(path.relative_to(ROOT))
            for path in PLATFORM_DIR.rglob("*")
            if path.is_file() or path.is_symlink()
        )
        if current_platform_files:
            errors.append(
                "Third-party platform artwork must not remain in the current website tree after v5.21: "
                + ", ".join(current_platform_files)
            )

    index = INDEX.read_text(encoding="utf-8")
    for stale in ("assets/platform/", "platform-logo-link", "platform-native-mark", "Third-party logos identify"):
        if stale in index:
            errors.append(f"Homepage retains obsolete third-party platform-artwork marker: {stale}")
    if index.count('class="platform-mark"') != 11:
        errors.append(
            "Homepage must expose exactly 11 unified Glaze UI platform marks; "
            f"found {index.count('class=\"platform-mark\"')}."
        )

    if not INVENTORY.is_file() or INVENTORY.is_symlink():
        errors.append("docs/public-asset-inventory.md must remain a regular repository file.")
    else:
        inventory = INVENTORY.read_text(encoding="utf-8")
        for relative, expected_blob in EXPECTED_BLOBS.items():
            marker = f"`{relative}`"
            if inventory.count(marker) != 1:
                errors.append(f"Public asset inventory must contain exactly one row for {relative}.")
            if expected_blob not in inventory:
                errors.append(f"Public asset inventory is missing reviewed Git blob {expected_blob} for {relative}.")
        if "assets/platform/" in inventory:
            errors.append("Public asset inventory must not list assets/platform/* as deployable current-tree artwork.")
        for marker in (
            "Third-party deployable logo artwork: **None**",
            "native Glaze UI text marks",
            "historical commits may still contain prior third-party artwork blobs",
            "Issue #5 remains open",
        ):
            if marker not in inventory:
                errors.append(f"Public asset inventory is missing v5.21 rights-boundary marker: {marker}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Public asset rights-boundary validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Public asset rights-boundary validation passed: three GoreeCloud identity assets; no third-party deployable logo artwork.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")


def write_public_asset_tests() -> None:
    path = ROOT / "tests" / "test_public_assets.py"
    path.write_text('''#!/usr/bin/env python3
"""Regression coverage for the GoreeCloud website public-artwork boundary."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_ASSET_FILES  # noqa: E402


class PublicAssetBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.inventory = (ROOT / "docs" / "public-asset-inventory.md").read_text(encoding="utf-8")

    def test_public_artwork_allowlist_is_first_party_only(self) -> None:
        self.assertEqual(
            tuple(PUBLIC_ASSET_FILES),
            (
                "assets/favicon.svg",
                "assets/goreecloud-icon.png",
                "assets/social-preview.png",
            ),
        )

    def test_current_tree_has_no_platform_logo_files(self) -> None:
        platform_dir = ROOT / "assets" / "platform"
        files = [] if not platform_dir.exists() else [path for path in platform_dir.rglob("*") if path.is_file() or path.is_symlink()]
        self.assertEqual(files, [])

    def test_homepage_uses_unified_native_platform_marks(self) -> None:
        self.assertEqual(self.index.count('class="platform-mark"'), 11)
        for stale in ("assets/platform/", "platform-logo-link", "platform-native-mark", "Third-party logos identify"):
            self.assertNotIn(stale, self.index)
        for mark in (">PX</a>", ">DE</a>", ">DK</a>", ">NB</a>", ">AH</a>", ">CY</a>", ">BZ</a>", ">UK</a>", ">GM</a>", ">GS</a>", ">GN</span>"):
            self.assertIn(mark, self.index)

    def test_technology_links_are_preserved(self) -> None:
        for href in (
            "https://www.proxmox.com",
            "https://www.debian.org/",
            "https://www.docker.com/",
            "https://netbird.io/",
            "https://adguard.com/adguard-home/overview.html",
            "https://caddyserver.com/",
            "https://github.com/henrygd/beszel",
            "https://github.com/louislam/uptime-kuma",
            "https://github.com/GoreeCloud/goreecloud-monitor",
            "https://github.com/GoreeCloud/goreecloud-search",
        ):
            self.assertIn(f'href="{href}"', self.index)

    def test_inventory_records_zero_third_party_deployable_logos(self) -> None:
        self.assertIn("Third-party deployable logo artwork: **None**", self.inventory)
        self.assertNotIn("assets/platform/", self.inventory)
        self.assertIn("historical commits may still contain prior third-party artwork blobs", self.inventory)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")


def write_asset_inventory() -> None:
    path = ROOT / "docs" / "public-asset-inventory.md"
    path.write_text('''# GoreeCloud Website Public Asset Inventory

## Purpose

This repository document records the artwork intentionally eligible for publication by the GoreeCloud website build. It supports the source-license, creative-rights, attribution, and repository-publication review tracked in issue #5.

This inventory is **not a license grant**. The authoritative deployment list remains `PUBLIC_ASSET_FILES` in `scripts/build_public_site.py`, and CI content-binds the reviewed GoreeCloud identity assets to the exact Git blob IDs below.

## Review status

Status: **Production deployment contains GoreeCloud-owned identity artwork only**

Third-party deployable logo artwork: **None**.

Version 5.21 removes the remaining third-party platform logos from the deployable artifact and from the current source tree. The Platform Foundation section now uses native Glaze UI text marks while retaining descriptive technology names and outbound links to the referenced projects. This reduces payload, removes the current-tree third-party artwork redistribution surface, and avoids treating descriptive technology references as GoreeCloud-owned branding.

Historical commits may still contain prior third-party artwork blobs. Their presence in reachable repository history is one reason issue #5 remains open for final human history/contextual review and an explicit repository-visibility/publication decision. A clean current tree does not by itself authorize publishing historical repository contents.

## Integrity snapshot

A Git blob ID is an **integrity fingerprint only**. It does not establish copyright ownership or grant reuse rights. CI recomputes the exact blob ID of every currently deployable artwork file and requires it to match this reviewed inventory.

## GoreeCloud identity artwork

| Deployable path | Role | Publication/licensing status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `1e578573f8f753f0d51e616284546b42f67012da` |
| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `5ae9000d1404239ef362f42f109e3d7de3557d38` |
| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; editorial/brand rights remain separately controlled | `64aaf437835b31a8473292487cf57366bb58c4fa` |

## Platform Foundation presentation boundary

The Platform Foundation section names third-party technologies descriptively and may link to their official websites or repositories, but it does not redistribute their logo artwork. Each platform card uses a short GoreeCloud-rendered Glaze UI text mark such as PX, DE, DK, NB, AH, CY, BZ, or UK.

The text marks are presentation primitives, not replacement third-party logos and not claims of ownership over the referenced project names. They exist to provide a consistent first-party visual treatment without adding remote icon dependencies or redistributing external artwork.

## Family-service artwork boundary

Family-service cards likewise use GoreeCloud Glaze UI monograms such as NC, IM, JF, and VW. Service and technology names remain descriptive references. No third-party family-service logo artwork is included in the public deployment allowlist.

## Deliberate boundaries

- The Apache-2.0 source license applies to the approved source-code boundary and does not automatically license GoreeCloud branding or third-party names and marks.
- GoreeCloud identity artwork may use different reuse terms from source code.
- Adding or replacing deployable artwork requires deliberate review of `PUBLIC_ASSET_FILES`, this inventory, and `scripts/validate_public_assets.py`.
- Changing the bytes of a reviewed GoreeCloud identity asset requires updating its reviewed Git blob ID only after the new artwork and reuse boundary are approved.
- Current descriptive links to third-party technologies do not require redistributing those projects' artwork.
- Repository history is a separate publication surface from the current public website artifact.

## Publication gate

Issue #5 remains open. The deployable third-party platform-mark review has been eliminated by removing those files from the public artifact and current source tree, but GoreeCloud still requires a final human review of reachable repository history and contextual disclosures plus an explicit repository visibility/publication decision before any source-repository visibility change.
''', encoding="utf-8")


def patch_readme() -> None:
    path = ROOT / "README.md"
    replacements = (
        (
            "Current website package: **v5.20.0 — repository portfolio reconciliation, metadata hardening, and ancillary-page request optimization**",
            "Current website package: **v5.21.0 — first-party platform marks, public-artwork minimization, and creative-rights hardening**",
        ),
        (
            "- locally hosted images and project artwork;",
            "- locally hosted GoreeCloud identity artwork and first-party Glaze UI text marks;",
        ),
        (
            "The v5.20.0 release also links the already-deployed local web manifest and dual SVG/PNG favicon identity from every human-facing page, completes Open Graph/Twitter metadata for the public repository directory, and enforces page-specific stylesheet/script request ceilings. Privacy and security pages now load only the shared styles they actually use. These are static presentation and delivery improvements; they do not add browser telemetry, a service worker, a backend, or new network requests.",
            "The v5.20.0 release linked the local web manifest and dual SVG/PNG favicon identity from every human-facing page, completed Open Graph/Twitter metadata for the public repository directory, and established page-specific stylesheet/script request ceilings. Version 5.21.0 further removes all remaining third-party platform-logo files from the public artifact and current source tree, replaces them with native Glaze UI text marks, and adds a content-bound public-asset rights validator. These are static presentation, governance, and delivery improvements; they do not add browser telemetry, a service worker, a backend, or new network requests.",
        ),
        (
            "`docs/public-asset-inventory.md` is the working deployable-artwork inventory and is **not a license grant**. It records publication and provenance evidence for the exact public asset set, but provenance and rights verification still requires the applicable human and legal review.\n\nIssue #5 remains open for the remaining third-party platform-mark review, the final human repository-history/contextual review, and the explicit repository visibility/publication decision. Passing CI does not itself authorize a repository visibility change or a creative-rights decision.",
            "`docs/public-asset-inventory.md` is the working deployable-artwork inventory and is **not a license grant**. Version 5.21.0 narrows the deployable artwork set to exactly three GoreeCloud identity assets and removes third-party platform-logo files from the current source tree. `scripts/validate_public_assets.py` content-binds those reviewed assets and rejects a silent return of the former platform artwork boundary.\n\nIssue #5 remains open for the final human repository-history/contextual review and the explicit repository visibility/publication decision. The former deployable third-party platform-mark review is no longer a current-tree/public-artifact gate because those logo files are not published or retained in the current tree. Historical commits remain a separate review surface, and passing CI does not itself authorize a repository visibility change or creative-rights decision.",
        ),
        (
            "- `assets/` — self-hosted artwork source; only explicitly approved files are deployable;",
            "- `assets/` — GoreeCloud-owned public identity artwork; third-party platform logos are not part of the current tree or deployable artifact;",
        ),
        (
            "The 5.20.0 candidate preserves the site's established visual identity and exact Glaze UI 1.1 contract, plus the 5.18.0 local repository discovery, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections. The 1.1 adoption is a compatible semantic expansion, not a visual redesign.",
            "The 5.21.0 candidate preserves the site's established visual identity and exact Glaze UI 1.1 contract while normalizing the Platform Foundation cards onto the same first-party monogram vocabulary already used by family services. It also preserves the 5.20.0 repository/metadata improvements, 5.18.0 local repository discovery, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections. The platform-mark change removes external artwork rather than redesigning the information architecture.",
        ),
        (
            "- `python scripts/validate_license.py` — validate Apache-2.0 source terms and NOTICE/README boundaries;",
            "- `python scripts/validate_license.py` — validate Apache-2.0 source terms and NOTICE/README boundaries;\n- `python scripts/validate_public_assets.py` — content-bind the three reviewed GoreeCloud public identity assets, reject current-tree platform-logo artwork, and keep the public asset inventory synchronized;",
        ),
    )
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if text.count(old) != 1:
            raise SystemExit(f"README patch marker mismatch: expected one occurrence of {old[:90]!r}, found {text.count(old)}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


def patch_stability_baseline() -> None:
    path = ROOT / "docs" / "stability-baseline.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("The repository-defined release version is **5.20.0**.", "The repository-defined release version is **5.21.0**.", 1)
    text = text.replace(
        "3. Source-license, governance-readiness, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.",
        "3. Source-license, public-asset rights-boundary, governance-readiness, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.",
        1,
    )
    scope_start = text.index("## 5.20.0 scope")
    scope_end = text.index("## Glaze UI 1.1 stable-release boundary", scope_start)
    new_scope = '''## 5.21.0 scope

Version 5.21.0 eliminates the website's remaining deployable third-party platform-logo artwork, unifies Platform Foundation cards on native Glaze UI text marks, and adds a fail-closed public-artwork integrity gate while preserving the v5.20 repository/metadata improvements and all production privacy, security, runtime-status, Glaze UI, performance, and isolated-publication boundaries.

The release:

- reduces deployable artwork from 13 files to exactly **3 GoreeCloud identity assets**: the SVG favicon, PNG application/site icon, and social-preview image;
- removes all ten former `assets/platform/*.svg` logo files from the current source tree rather than merely excluding them from `dist/`;
- replaces third-party platform logos with 11 unified first-party Glaze UI text marks across the Platform Foundation cards, including GoreeCloud Notify, Monitor, and Search;
- preserves outbound links to the referenced technology websites/repositories and keeps technology names descriptive rather than presenting the text marks as third-party logos;
- removes obsolete platform-image CSS and normalizes clickable/non-clickable marks onto one `platform-mark` component treatment;
- adds `scripts/validate_public_assets.py` and dedicated regression tests that content-bind the three reviewed GoreeCloud identity assets, reject `assets/platform/*` current-tree/public-artifact drift, and keep `docs/public-asset-inventory.md` synchronized;
- records that historical commits may still contain prior third-party artwork blobs and therefore does **not** treat the current-tree cleanup as authorization to publish repository history;
- advances issue #5 by eliminating the deployable/current-tree third-party platform-mark review while preserving the final human history/contextual review and explicit repository visibility/publication decision as separate gates;
- preserves the existing HTML, CSS, JavaScript, image, and 512 KiB total artifact budgets without increasing any ceiling;
- preserves the exact Glaze UI 1.1.0 conformance pin at `5c8320de4f770614a3e2bcf9de2a27f7fcfd920c`;
- preserves the authenticated **30 repositories / 23 public / 7 private / 11 functional groups** authority and local-only repository discovery behavior from v5.20 and v5.18;
- preserves the v5.17 Memos, Notify/ntfy, Search, and Monitoring/Uptime Kuma runtime-status boundaries;
- preserves Wardveil Security reporting, `security@goreecloud.com`, the self-only browser-origin model, `connect-src 'none'`, and telemetry-free operation;
- preserves the exact allowlisted Cloudflare `dist/` publication model and exact branch-preview/production deployment verification requirement.

'''
    text = text[:scope_start] + new_scope + text[scope_end:]
    text = text.replace(
        "Wardveil Security by GoreeCloud remains the platform security identity and presentation layer; it does not replace technical security controls or evidence. The v5.20.0 portfolio and metadata release does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
        "Wardveil Security by GoreeCloud remains the platform security identity and presentation layer; it does not replace technical security controls or evidence. The v5.21.0 public-artwork minimization release does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
        1,
    )
    text = text.replace(
        "The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.",
        "The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party deployable platform marks: **None**. The current-tree/public-artifact logo review was eliminated in v5.21 by removing those files, but historical repository content still requires final human contextual review before any visibility decision.",
        1,
    )
    path.write_text(text, encoding="utf-8")


def patch_tests_and_workflow() -> None:
    stability = ROOT / "tests" / "test_stability_baseline.py"
    text = stability.read_text(encoding="utf-8")
    old = '            "Third-party platform-mark review",\n'
    new = '            "Third-party deployable platform marks: **None**",\n'
    if text.count(old) != 1:
        raise SystemExit("Expected one legacy third-party platform-mark stability test marker.")
    stability.write_text(text.replace(old, new, 1), encoding="utf-8")

    workflow = ROOT / ".github" / "workflows" / "validate.yml"
    text = workflow.read_text(encoding="utf-8")
    marker = "      - name: Validate source license\n        run: python scripts/validate_license.py\n"
    insertion = marker + "\n      - name: Validate public asset rights boundary\n        run: python scripts/validate_public_assets.py\n"
    if text.count(marker) != 1:
        raise SystemExit("Expected one Validate source license workflow step.")
    if "Validate public asset rights boundary" in text:
        raise SystemExit("Public asset rights-boundary workflow step already exists unexpectedly.")
    workflow.write_text(text.replace(marker, insertion, 1), encoding="utf-8")


def patch_version() -> None:
    path = ROOT / "VERSION"
    if path.read_text(encoding="utf-8") != "5.20.0\n":
        raise SystemExit("Expected exact v5.20.0 VERSION baseline.")
    path.write_text("5.21.0\n", encoding="utf-8")


def delete_platform_assets() -> None:
    assets = (
        "adguard-home.svg",
        "beszel.svg",
        "caddy.svg",
        "debian.svg",
        "docker.svg",
        "netbird.svg",
        "ntfy.svg",
        "proxmox.svg",
        "searxng.svg",
        "uptime-kuma.svg",
    )
    for name in assets:
        path = ROOT / "assets" / "platform" / name
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"Expected regular legacy platform asset before removal: {path.relative_to(ROOT)}")
        path.unlink()


def main() -> None:
    patch_index()
    patch_platform_css()
    patch_build_allowlist()
    write_public_asset_validator()
    write_public_asset_tests()
    write_asset_inventory()
    patch_readme()
    patch_stability_baseline()
    patch_tests_and_workflow()
    patch_version()
    delete_platform_assets()
    print("Applied guarded GoreeCloud Website v5.21 native platform-mark migration.")


if __name__ == "__main__":
    main()
