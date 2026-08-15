# GoreeCloud Website Public Asset Inventory

## Purpose

This repository document records the artwork that is intentionally eligible for publication by the GoreeCloud website build. It supports the source-license, creative-asset, attribution, and repository-publication decision tracked in issue #5.

This inventory is **not a license grant** and does not select the website source-code license. It exists so source code, GoreeCloud-owned identity material, written content, and third-party product/project marks are not accidentally treated as one undifferentiated licensing category.

The authoritative deployment list remains `PUBLIC_ASSET_FILES` in `scripts/build_public_site.py`. CI requires every path in that list to remain represented here.

## Review status

Status: **Pre-publication inventory — provenance and rights verification still required**

Before this repository is made public or its creative assets are represented as reusable under a repository-wide license:

1. confirm the original source and applicable license/usage terms for every third-party mark;
2. confirm the copyright holder and intended reuse terms for GoreeCloud identity artwork and the social preview;
3. decide whether written website content and GoreeCloud branding use the source-code license or a separate copyright/license notice;
4. preserve any required attribution, trademark notice, or upstream license text;
5. complete the repository-history sensitive-information review required by issue #5;
6. only then add the approved top-level `LICENSE` and any useful notice/attribution file.

A source-code license must not be assumed to relicense third-party marks or branding.

## Integrity snapshot

Each deployable asset row records the Git blob ID of the exact file content reviewed in this inventory. CI recomputes the blob ID from the checked-out bytes and requires it to match the recorded value.

This content binding closes an important review gap: replacing an artwork file in place while retaining the same path now requires an intentional inventory update. The blob ID is an integrity fingerprint only. It does **not** establish copyright ownership, provenance, trademark permission, or redistribution rights, and it must not be presented as rights evidence.

When an approved asset changes legitimately, update the asset and its recorded blob ID in the same reviewed change, then re-evaluate any provenance, attribution, trademark, or licensing implications of the new bytes.

## GoreeCloud identity artwork

These files are GoreeCloud-branded identity/presentation assets in the repository. Their final copyright holder and reuse terms must be confirmed as part of issue #5 before repository publication.

| Deployable path | Role | Publication/licensing status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; final ownership/reuse notice pending issue #5 | `1e578573f8f753f0d51e616284546b42f67012da` |
| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; final ownership/reuse notice pending issue #5 | `5ae9000d1404239ef362f42f109e3d7de3557d38` |
| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; final ownership/reuse notice pending issue #5 | `64aaf437835b31a8473292487cf57366bb58c4fa` |

## Third-party platform/project marks

The following files identify software or platforms referenced by the public GoreeCloud site. They should be treated as third-party project/brand artwork until their exact source, license, attribution, and trademark usage requirements are verified.

The repository filename and displayed project identity are sufficient to establish the intended subject, but they do **not** establish provenance or redistribution rights. Do not infer an asset license from the software project's code license.

| Deployable path | Identified project/platform | Verification status | Reviewed Git blob ID |
| --- | --- | --- | --- |
| `assets/platform/adguard-home.svg` | AdGuard Home | Upstream artwork source/terms to verify | `713ec820617ccda98427c3fa38f97a72165ca6e1` |
| `assets/platform/beszel.svg` | Beszel | Upstream artwork source/terms to verify | `a0459d16b3c5b9582eea6a637e1027fe76426be4` |
| `assets/platform/caddy.svg` | Caddy | Upstream artwork source/terms to verify | `e7c49498548a1d79228284c9de8066f31c983d8a` |
| `assets/platform/debian.svg` | Debian | Official logo/trademark policy located; Simple Icons intermediary-source evidence located; final exact-source/compliance review still required | `e6bd21288ffb991cab15625b0a69900a0ded5e41` |
| `assets/platform/docker.svg` | Docker | Official brand/trademark guidance located; Simple Icons intermediary-source evidence located; final exact-source/permission/compliance review still required | `de7b005b813f9c3c902591a3084f138777c29b30` |
| `assets/platform/netbird.svg` | NetBird | Upstream artwork source/terms to verify | `89bb8ba27d31b24c4f1dd308e43bd09bfae76901` |
| `assets/platform/ntfy.svg` | ntfy | Upstream artwork source/terms to verify | `429dfed5bd19effcf1d420b17f8995353caad97f` |
| `assets/platform/proxmox.svg` | Proxmox | Upstream artwork source/terms to verify | `10f91a01bb4fd15c7345bbbefba00a06e84bd7ac` |
| `assets/platform/searxng.svg` | SearXNG | Upstream artwork source/terms to verify | `908330f2b0b0aa881e50e8e1013c18126b728c02` |
| `assets/platform/uptime-kuma.svg` | Uptime Kuma | Upstream artwork source/terms to verify | `8ef1dbe73ecdacf7dadd430cfe9c87af684732d0` |
| `assets/services/audiobookshelf.svg` | Audiobookshelf | Upstream artwork source/terms to verify | `917e42e00103f1f285d208302a6b5a50bff7cd37` |
| `assets/services/element.svg` | Element | Upstream artwork source/terms to verify | `54a91b72f803034ee1e7c71fb68e2d2a2c84349e` |
| `assets/services/immich.svg` | Immich | Upstream artwork source/terms to verify | `08e60a45bb98462eeaa22800a8fd7bbe174fe0b2` |
| `assets/services/jellyfin.svg` | Jellyfin | Upstream artwork source/terms to verify | `d4d7f01724b132f3f36a22d4727dc88953677e6a` |
| `assets/services/navidrome.svg` | Navidrome | Upstream artwork source/terms to verify | `1ec9541621a037829c6e6336b3d92a5541fd70b2` |
| `assets/services/nextcloud.svg` | Nextcloud | Upstream artwork source/terms to verify | `853346e1d6013387eb2768bbd5774b86c7fc32d0` |
| `assets/services/paperless-ngx.svg` | Paperless-ngx | Upstream artwork source/terms to verify | `8db3273947738f0b80644ccb706b54459a5745a5` |
| `assets/services/vaultwarden.svg` | Vaultwarden | Upstream artwork source/terms to verify | `bb241d516206c45bfaffe5f023caaeb7d6dcc2a4` |

## Verified upstream policy evidence

This section records official policy material found during the pre-publication review. It deliberately distinguishes an upstream policy from proof that GoreeCloud's current local SVG is the upstream-approved file.

### Debian

Official sources reviewed:

- Debian logo page: https://www.debian.org/logos/
- Debian trademark policy: https://www.debian.org/trademark

The Debian Project publishes an "open use" logo and states that this logo is copyright Software in the Public Interest, Inc. and is released under LGPL-3.0-or-later or, at the user's option, CC BY-SA 3.0. Debian also publishes separate trademark-use conditions, including attribution/disclaimer guidance and restrictions intended to avoid false affiliation or endorsement.

This establishes an official policy path for using a Debian logo, but the final GoreeCloud attribution/disclaimer treatment has not yet been implemented. Keep the Debian row unresolved until the exact-source and final presentation checks are complete.

### Docker

Official sources reviewed:

- Docker brand/media resources: https://www.docker.com/company/newsroom/media-resources/
- Docker trademark guidelines: https://www.docker.com/legal/trademark-guidelines/

Docker publishes an approved logo kit and detailed logo/trademark rules. The current guidelines distinguish permitted referential use from logo-mark use, require avoidance of implied sponsorship/affiliation, specify approved logo presentation, and provide trademark-notice requirements. The guidelines also state that logo/design use is more constrained than ordinary word-mark reference.

This establishes the governing official policy material, but it does **not** establish that the current local Docker SVG came from Docker's approved logo kit or that GoreeCloud's specific presentation satisfies every applicable condition. Keep the Docker row unresolved until exact source provenance and final use/notice compliance are verified.

## Intermediary-source evidence

The current Debian and Docker SVGs use the same 24×24 path geometry and titles as the corresponding Simple Icons assets checked on August 15, 2026. GoreeCloud's local copies are reformatted and add explicit brand-color fills, while the Simple Icons files are normalized monochrome SVGs. This is strong evidence that these two local assets were derived from Simple Icons or from the same normalized icon geometry; it is **not** proof of the original acquisition event or a substitute for the underlying brand owner's terms.

Simple Icons references reviewed:

- Debian icon: https://github.com/simple-icons/simple-icons/blob/develop/icons/debian.svg
- Docker icon: https://github.com/simple-icons/simple-icons/blob/develop/icons/docker.svg
- Simple Icons disclaimer: https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md

Simple Icons' repository is distributed under CC0-1.0, but its own disclaimer expressly cautions that this does **not** mean every included brand icon is CC0. It directs users to individual icon license data, source URLs, and brand guidelines where available. Therefore GoreeCloud must continue to treat Simple Icons as an intermediary artwork source, not as a blanket rights-clearing layer for third-party marks.

## Deliberate boundaries

- Presence in the public deployment artifact means an asset is technically published by the website; it does not mean GoreeCloud owns the underlying third-party mark.
- The eventual HTML/CSS/JavaScript/Python source license must be evaluated separately from creative-content and trademark rights.
- GoreeCloud identity artwork may use different reuse terms from source code if that is the approved project-specific decision.
- Third-party marks must not be described as GoreeCloud-owned artwork.
- A third-party software project's open-source license must not be treated as automatic permission to redistribute its logo under that same license.
- Replacing or adding a public asset requires updating both `PUBLIC_ASSET_FILES` and this inventory in the same reviewed change.
- Changing the bytes of an existing public asset requires updating its reviewed Git blob ID here and reconsidering its provenance/rights status even when the filename is unchanged.
- Official trademark/brand guidance is evidence about permitted conditions; it is not proof that a local artwork file came from the approved upstream source.
- An intermediary icon library's repository license must not be treated as a blanket license for all underlying third-party brand marks.
- Repository-only design experiments, source material, or unused artwork remain outside the deployment artifact unless explicitly allowlisted.

## Publication gate

This inventory intentionally leaves provenance and rights fields unresolved where the repository does not currently establish them. Issue #5 remains open until the actual source-license, creative-asset terms, copyright notice, history review, and repository-visibility decisions are completed.
