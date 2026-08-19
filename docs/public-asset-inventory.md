# GoreeCloud Website Public Asset Inventory

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
