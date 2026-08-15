# GoreeCloud Website Public Asset Inventory

## Purpose

This repository document records the artwork that is intentionally eligible for publication by the GoreeCloud website build. It supports the source-license, creative-asset, attribution, and repository-publication review tracked in issue #5.

This inventory is **not a license grant**. The authoritative deployment list remains `PUBLIC_ASSET_FILES` in `scripts/build_public_site.py`, and CI requires every path in that list to remain represented here with the exact reviewed Git blob ID.

## Review status

Status: **Production-deployment inventory narrowed; repository-publication provenance and rights verification still required**

The public website no longer deploys third-party family-service logo artwork. Those cards use GoreeCloud Glaze UI text monograms instead. The current deployable third-party artwork is limited to the platform-foundation marks listed below.

This narrowing reduces the public creative-rights surface without claiming ownership of third-party names or marks. The source-code license must not be assumed to relicense third-party marks, and an intermediary icon-library license must not be treated as a blanket rights grant for an underlying brand.

## Integrity snapshot

Each deployable asset row records the Git blob ID of the exact file content reviewed in this inventory. CI recomputes the blob ID from the checked-out bytes and requires it to match the recorded value.

A Git blob ID is an **integrity fingerprint only**. It does not establish copyright ownership, provenance, trademark permission, or redistribution rights. When an approved asset changes, the new bytes and their legal/brand implications must be reviewed before the inventory is updated.

## GoreeCloud identity artwork

| Deployable path | Role | Publication/licensing status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `1e578573f8f753f0d51e616284546b42f67012da` |
| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; brand reuse remains outside the Apache-2.0 source grant | `5ae9000d1404239ef362f42f109e3d7de3557d38` |
| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; editorial/brand rights remain separately controlled | `64aaf437835b31a8473292487cf57366bb58c4fa` |

## Third-party platform marks still deployed

The following marks identify technologies referenced by the public Platform Foundation section. They remain third-party project/brand artwork and are not GoreeCloud-owned assets. Their use is descriptive and must not imply sponsorship, endorsement, or affiliation.

| Deployable path | Identified project/platform | Verification status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/platform/adguard-home.svg` | AdGuard Home | Upstream artwork source/terms to verify | `713ec820617ccda98427c3fa38f97a72165ca6e1` |
| `assets/platform/beszel.svg` | Beszel | Upstream artwork source/terms to verify | `a0459d16b3c5b9582eea6a637e1027fe76426be4` |
| `assets/platform/caddy.svg` | Caddy | Upstream artwork source/terms to verify | `e7c49498548a1d79228284c9de8066f31c983d8a` |
| `assets/platform/debian.svg` | Debian | Official logo/trademark policy located; exact-source/final-use review still required | `e6bd21288ffb991cab15625b0a69900a0ded5e41` |
| `assets/platform/docker.svg` | Docker | Official brand/trademark guidance located; exact-source/final-use review still required | `de7b005b813f9c3c902591a3084f138777c29b30` |
| `assets/platform/netbird.svg` | NetBird | Upstream artwork source/terms to verify | `89bb8ba27d31b24c4f1dd308e43bd09bfae76901` |
| `assets/platform/ntfy.svg` | ntfy | Upstream artwork source/terms to verify | `429dfed5bd19effcf1d420b17f8995353caad97f` |
| `assets/platform/proxmox.svg` | Proxmox | Upstream artwork source/terms to verify | `10f91a01bb4fd15c7345bbbefba00a06e84bd7ac` |
| `assets/platform/searxng.svg` | SearXNG | Upstream artwork source/terms to verify | `908330f2b0b0aa881e50e8e1013c18126b728c02` |
| `assets/platform/uptime-kuma.svg` | Uptime Kuma | Upstream artwork source/terms to verify | `8ef1dbe73ecdacf7dadd430cfe9c87af684732d0` |

## Family-service artwork boundary

Family-service cards are now rendered with GoreeCloud-owned Glaze UI monograms such as NC, IM, JF, and VW. Their service names are descriptive references to the corresponding projects. No third-party family-service logo artwork is included in the current `PUBLIC_ASSET_FILES` deployment allowlist.

Repository-only historical/reference artwork may remain outside `dist/` while issue #5 is open. Its presence in a private source repository must not be interpreted as approved public redistribution, and it must never become deployable merely because it exists under an `assets` directory.

## Deliberate boundaries

- Presence in the public deployment artifact means an asset is technically published; it does not mean GoreeCloud owns an underlying third-party mark.
- The Apache-2.0 source license applies to the approved source-code boundary and does not automatically license GoreeCloud branding or third-party marks.
- GoreeCloud identity artwork may use different reuse terms from source code.
- Third-party marks must not be described as GoreeCloud-owned artwork.
- Replacing or adding a public asset requires updating both `PUBLIC_ASSET_FILES` and this inventory in the same reviewed change.
- Changing the bytes of an existing public asset requires updating its reviewed Git blob ID and reconsidering provenance/rights status.
- Repository-only artwork remains outside the deployment artifact unless explicitly allowlisted.

## Publication gate

Issue #5 remains open. Before a public repository-visibility decision, GoreeCloud still requires the final human history/contextual disclosure review and the remaining third-party creative-rights review. The public website deployment may remain separate from source-repository publication.
