#!/usr/bin/env python3
"""Apply the one-time GoreeCloud Website v5.22 current-tree publication cleanup."""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    platform_dir = ROOT / "assets" / "platform"
    services_dir = ROOT / "assets" / "services"
    platform_files = sorted(platform_dir.glob("*.svg"))
    service_files = sorted(services_dir.glob("*.svg"))
    if len(platform_files) != 10:
        raise RuntimeError(f"Expected exactly 10 platform SVGs, found {len(platform_files)}")
    if len(service_files) != 8:
        raise RuntimeError(f"Expected exactly 8 service SVGs, found {len(service_files)}")
    for path in platform_files + service_files:
        path.unlink()
    platform_dir.rmdir()
    services_dir.rmdir()

    readme = read("README.md")
    readme = replace_once(
        readme,
        "Current website package: **v5.21.0 — third-party artwork elimination and platform identity hardening**",
        "Current website package: **v5.22.0 — current-tree third-party artwork removal and publication-surface hardening**",
        "README version",
    )
    readme = replace_once(
        readme,
        "The v5.21.0 release removes all third-party platform/service artwork from the deployable `dist/` allowlist. The platform foundation now uses neutral Glaze UI letter marks while retaining descriptive technology names and official outbound links. A dedicated validator and regression suite reject any future `assets/platform/` or `assets/services/` publication without an explicit reviewed boundary change. This reduces payload, browser asset requests, and creative-rights exposure without adding telemetry, remote resources, a service worker, or a backend.",
        "The v5.22.0 release removes the 18 now-unused third-party SVG files under `assets/platform/` and `assets/services/` from the current repository tree. v5.21.0 had already removed those files from the deployable `dist/` allowlist and replaced visible project logos with neutral Glaze UI letter marks; v5.22.0 now makes current source match that public-artwork boundary and fails closed if either third-party artwork directory reappears. Prior reachable Git history may still contain historical copies, so issue #5 remains a separate human history/context/publication gate. The browser experience and deployable artifact remain otherwise unchanged.",
        "README v5.22 scope",
    )
    readme = replace_once(
        readme,
        "Issue #5 remains open for the final human reachable-history/contextual-disclosure review and the explicit repository visibility/publication decision. The v5.21.0 public artifact no longer contains third-party logo artwork, but passing CI still does not authorize a repository visibility change or a creative-rights/publication decision.",
        "Issue #5 remains open for the final human reachable-history/contextual-disclosure review and the explicit repository visibility/publication decision. The v5.22.0 current tree and public artifact no longer contain third-party logo artwork, but prior reachable history may still contain historical copies; passing CI still does not authorize a repository visibility change or a creative-rights/publication decision.",
        "README issue #5 boundary",
    )
    readme = replace_once(readme, "The 5.21.0 candidate preserves", "The 5.22.0 candidate preserves", "README Glaze release marker")
    readme = replace_once(
        readme,
        "`python scripts/validate_public_assets.py` — reject third-party artwork from the deployable allowlist and homepage platform surface;",
        "`python scripts/validate_public_assets.py` — reject third-party artwork from the deployable allowlist, homepage platform surface, and current-tree platform/service asset directories;",
        "README validator description",
    )
    write("README.md", readme)

    baseline = read("docs/stability-baseline.md")
    baseline = replace_once(baseline, "The repository-defined release version is **5.21.0**.", "The repository-defined release version is **5.22.0**.", "baseline version")
    new_scope = '''## 5.22.0 scope

Version 5.22.0 removes obsolete third-party artwork from the current repository tree and hardens the source-publication boundary while preserving the production-verified v5.21 public artifact, Glaze UI 1.1, privacy, security, repository/runtime-status, and isolated-publication contracts.

The release:

- deletes the ten unused `assets/platform/*.svg` files and eight unused `assets/services/*.svg` files from the current source tree;
- preserves the v5.21.0 neutral Glaze UI letter-mark presentation and official descriptive outbound project links;
- leaves `PUBLIC_ASSET_FILES` unchanged at exactly the three GoreeCloud-owned favicon/icon/social-preview assets;
- strengthens `scripts/validate_public_assets.py` so `assets/platform/` and `assets/services/` must remain absent from the current tree as well as absent from the deployable allowlist and homepage render surface;
- strengthens `tests/test_public_asset_boundary.py` with current-tree directory-absence regression coverage;
- updates `docs/public-asset-inventory.md` to distinguish the clean current tree from prior reachable Git history, which remains subject to final human contextual review;
- keeps issue #5 open because deleting current-tree files does not rewrite reachable history and does not authorize a repository visibility change;
- leaves the browser-facing `dist/` artifact byte-equivalent to v5.21.0 because the deleted SVGs were already non-deployable;
- preserves the authenticated **30 repository / 23 public / 7 private / 11 group** portfolio authority;
- preserves the exact Glaze UI 1.1.0 conformance pin at `5c8320de4f770614a3e2bcf9de2a27f7fcfd920c`;
- preserves the Memos, Notify/ntfy, Search, and Monitoring/Uptime Kuma runtime-status boundaries;
- preserves Wardveil Security reporting, `security@goreecloud.com`, the self-only browser-origin model, `connect-src 'none'`, and telemetry-free operation;
- preserves the exact allowlisted Cloudflare `dist/` publication model and exact branch-preview/production deployment verification requirement.

'''
    pattern = re.compile(r"## 5\.21\.0 scope\n.*?(?=## Glaze UI 1\.1 stable-release boundary)", re.DOTALL)
    baseline, count = pattern.subn(new_scope, baseline, count=1)
    if count != 1:
        raise RuntimeError(f"baseline scope: expected one section, replaced {count}")
    baseline = replace_once(
        baseline,
        "The v5.21.0 platform-identity release does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
        "The v5.22.0 current-tree publication cleanup does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.",
        "baseline Wardveil release marker",
    )
    write("docs/stability-baseline.md", baseline)

    inventory = '''# GoreeCloud Website Public Asset Inventory

## Purpose

This repository document records the artwork that is intentionally eligible for publication by the GoreeCloud website build. It supports the source-license, creative-asset, and repository-publication review tracked in issue #5.

This inventory is **not a license grant**. The authoritative deployment list remains `PUBLIC_ASSET_FILES` in `scripts/build_public_site.py`, and CI requires the deployable artwork boundary to remain GoreeCloud-owned and explicitly allowlisted.

## Review status

Status: **Deployable and current-tree artwork reduced to GoreeCloud-owned identity and presentation assets; third-party artwork removed from the public artifact and current source tree**

Version 5.21.0 removed third-party platform artwork from `dist` and replaced visible project logos with neutral Glaze UI letter marks. Version 5.22.0 completes the current-tree cleanup by deleting the ten obsolete `assets/platform/*.svg` files and eight obsolete `assets/services/*.svg` files from the current source revision.

This removes third-party logo artwork from both the deployable artifact and current repository tree. It does **not** rewrite prior reachable Git history, declare third-party names or marks to be GoreeCloud property, alter the Apache-2.0 source-license boundary, or authorize publishing the private repository or its history.

## GoreeCloud identity artwork

| Deployable path | Role | Publication/licensing status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `1e578573f8f753f0d51e616284546b42f67012da` |
| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `5ae9000d1404239ef362f42f109e3d7de3557d38` |
| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; editorial/brand rights remain separately controlled | `64aaf437835b31a8473292487cf57366bb58c4fa` |

## Third-party artwork publication boundary

No current-tree path under `assets/platform/` or `assets/services/` remains. Neither directory is part of the current source revision, and no path under either prefix is included in `PUBLIC_ASSET_FILES`. The homepage uses text/letter marks for platform technologies and family services instead of third-party logos.

Prior reachable Git history may still contain historical copies of retired third-party SVG files. Historical repository presence does not make those files deployable, approved for redistribution, or covered by the Apache-2.0 source grant. The final human reachable-history/contextual-disclosure review remains required before any repository publication decision.

## Integrity and regression controls

- `scripts/build_public_site.py` explicitly allowlists only the three GoreeCloud-owned public artwork files above.
- `scripts/validate_public_assets.py` rejects any deployable `assets/platform/` or `assets/services/` path, rejects third-party artwork references from the homepage platform surface, and fails if either retired directory exists in the current tree.
- `tests/test_public_asset_boundary.py` protects the exact artwork allowlist, neutral-mark contract, and current-tree directory absence.
- `tests/test_public_asset_inventory.py` binds the three deployable GoreeCloud artwork files to their reviewed Git blob IDs and preserves the publication boundary language.
- `scripts/validate_build_artifact.py` proves that only allowlisted files enter the isolated `dist/` artifact.
- `scripts/verify_remote_deployment.py` compares deployed bytes against the exact reviewed source/artifact after merge.

## Deliberate boundaries

- Technology and project names remain descriptive references to their respective projects.
- Official outbound project links remain links; they do not load third-party render resources into the GoreeCloud page.
- The Apache-2.0 source license applies to the approved source-code boundary and does not automatically license GoreeCloud branding or third-party marks.
- GoreeCloud identity artwork may use different reuse terms from source code.
- Adding any new public artwork requires updating `PUBLIC_ASSET_FILES`, this inventory, and the creative-asset validator in the same reviewed change.
- Reintroducing `assets/platform/` or `assets/services/` in the current tree requires an explicit publication-boundary review rather than being treated as harmless reference material.
- Historical objects in reachable Git history remain a separate human source-publication review concern even when absent from the current tree and `dist/`.

## Publication gate

Issue #5 remains open only for the final human reachable-history/contextual-disclosure review and the explicit repository visibility/publication decision. A successful CI run, current-tree cleanup, or stable production deployment does not authorize a repository visibility change.
'''
    write("docs/public-asset-inventory.md", inventory)

    validator = read("scripts/validate_public_assets.py")
    validator = replace_once(
        validator,
        'FORBIDDEN_PREFIXES = ("assets/platform/", "assets/services/")\n',
        'FORBIDDEN_PREFIXES = ("assets/platform/", "assets/services/")\nFORBIDDEN_CURRENT_TREE_DIRS = (ROOT / "assets" / "platform", ROOT / "assets" / "services")\n',
        "validator current-tree constants",
    )
    validator = replace_once(
        validator,
        '    for path in PUBLIC_ASSET_FILES:\n        if path.startswith(FORBIDDEN_PREFIXES):\n            errors.append(f"Third-party artwork must not be deployable: {path}")\n\n',
        '    for path in PUBLIC_ASSET_FILES:\n        if path.startswith(FORBIDDEN_PREFIXES):\n            errors.append(f"Third-party artwork must not be deployable: {path}")\n\n    for directory in FORBIDDEN_CURRENT_TREE_DIRS:\n        if directory.exists():\n            errors.append(f"Retired third-party artwork directory must be absent from the current tree: {directory.relative_to(ROOT)}")\n\n',
        "validator current-tree check",
    )
    validator = replace_once(
        validator,
        '        "third-party artwork removed from the public artifact",\n        "No path under `assets/platform/` or `assets/services/` is included",\n',
        '        "third-party artwork removed from the public artifact and current source tree",\n        "No current-tree path under `assets/platform/` or `assets/services/` remains",\n',
        "validator inventory markers",
    )
    validator = replace_once(
        validator,
        '    print("Public creative-asset validation passed: only GoreeCloud-owned artwork is deployable.")',
        '    print("Public creative-asset validation passed: only GoreeCloud-owned artwork remains deployable and retired third-party artwork is absent from the current tree.")',
        "validator success message",
    )
    write("scripts/validate_public_assets.py", validator)

    tests = read("tests/test_public_asset_boundary.py")
    tests = replace_once(
        tests,
        '    def test_third_party_asset_directories_are_not_deployable(self) -> None:\n        self.assertFalse(any(path.startswith("assets/platform/") for path in PUBLIC_ASSET_FILES))\n        self.assertFalse(any(path.startswith("assets/services/") for path in PUBLIC_ASSET_FILES))\n\n',
        '    def test_third_party_asset_directories_are_not_deployable(self) -> None:\n        self.assertFalse(any(path.startswith("assets/platform/") for path in PUBLIC_ASSET_FILES))\n        self.assertFalse(any(path.startswith("assets/services/") for path in PUBLIC_ASSET_FILES))\n\n    def test_retired_third_party_asset_directories_are_absent_from_current_tree(self) -> None:\n        self.assertFalse((ROOT / "assets" / "platform").exists())\n        self.assertFalse((ROOT / "assets" / "services").exists())\n\n',
        "asset boundary current-tree test",
    )
    write("tests/test_public_asset_boundary.py", tests)

    write("VERSION", "5.22.0\n")
    print("Applied GoreeCloud Website v5.22.0 current-tree publication cleanup.")


if __name__ == "__main__":
    main()
