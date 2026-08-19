# GoreeCloud Website Public Asset Inventory

## Purpose

This repository document records the artwork that is intentionally eligible for publication by the GoreeCloud website build. It supports the source-license, creative-asset, and repository-publication review tracked in issue #5.

This inventory is **not a license grant**. The authoritative deployment list remains `PUBLIC_ASSET_FILES` in `scripts/build_public_site.py`, and CI requires the deployable artwork boundary to remain GoreeCloud-owned and explicitly allowlisted.

## Review status

Status: **Deployable artwork reduced to GoreeCloud-owned identity and presentation assets; third-party artwork removed from the public artifact**

Version 5.21.0 removes the remaining third-party platform logo files from the `dist/` allowlist and replaces the homepage platform-logo presentation with neutral Glaze UI letter marks. Technology names and outbound links remain for descriptive identification, but the browser no longer downloads or displays third-party project logo artwork from this repository.

This change removes the remaining deployable third-party-artwork provenance/trademark review from the website publication surface. It does **not** declare third-party names or marks to be GoreeCloud property, does not alter the Apache-2.0 source-license boundary, and does not by itself authorize publishing the private repository or its history.

## GoreeCloud identity artwork

| Deployable path | Role | Publication/licensing status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `1e578573f8f753f0d51e616284546b42f67012da` |
| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `5ae9000d1404239ef362f42f109e3d7de3557d38` |
| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; editorial/brand rights remain separately controlled | `64aaf437835b31a8473292487cf57366bb58c4fa` |

## Third-party artwork publication boundary

No path under `assets/platform/` or `assets/services/` is included in the current `PUBLIC_ASSET_FILES` allowlist. The homepage uses text/letter marks for platform technologies and family services instead of third-party logos.

Third-party SVG files may remain in the private repository as historical or reference material while issue #5 remains open. Repository presence does not make those files deployable, approved for redistribution, or covered by the Apache-2.0 source grant. The isolated `dist/` build is the publication boundary.

## Integrity and regression controls

- `scripts/build_public_site.py` explicitly allowlists only the three GoreeCloud-owned public artwork files above.
- `scripts/validate_public_assets.py` rejects any deployable `assets/platform/` or `assets/services/` path and rejects third-party artwork references from the homepage platform surface.
- `tests/test_public_asset_boundary.py` protects the exact artwork allowlist and neutral-mark contract.
- `scripts/validate_build_artifact.py` proves that only allowlisted files enter the isolated `dist/` artifact.
- `scripts/verify_remote_deployment.py` compares deployed bytes against the exact reviewed source/artifact after merge.

## Deliberate boundaries

- Technology and project names remain descriptive references to their respective projects.
- Official outbound project links remain links; they do not load third-party render resources into the GoreeCloud page.
- The Apache-2.0 source license applies to the approved source-code boundary and does not automatically license GoreeCloud branding or third-party marks.
- GoreeCloud identity artwork may use different reuse terms from source code.
- Adding any new public artwork requires updating `PUBLIC_ASSET_FILES`, this inventory, and the creative-asset validator in the same reviewed change.
- Repository-only historical/reference artwork remains outside the deployment artifact unless explicitly reviewed and allowlisted.

## Publication gate

Issue #5 remains open only for the final human reachable-history/contextual-disclosure review and the explicit repository visibility/publication decision. A successful CI run or this reduction of the public artwork surface does not authorize a repository visibility change.
