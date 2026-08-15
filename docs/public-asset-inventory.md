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

## GoreeCloud identity artwork

These files are GoreeCloud-branded identity/presentation assets in the repository. Their final copyright holder and reuse terms must be confirmed as part of issue #5 before repository publication.

| Deployable path | Role | Publication/licensing status |
| --- | --- | --- |
| `assets/favicon.svg` | GoreeCloud browser/site mark | GoreeCloud identity asset; final ownership/reuse notice pending issue #5 |
| `assets/goreecloud-icon.png` | GoreeCloud application/site icon | GoreeCloud identity asset; final ownership/reuse notice pending issue #5 |
| `assets/social-preview.png` | GoreeCloud Open Graph/X social preview | GoreeCloud presentation asset; final ownership/reuse notice pending issue #5 |

## Third-party platform/project marks

The following files identify software or platforms referenced by the public GoreeCloud site. They should be treated as third-party project/brand artwork until their exact source, license, attribution, and trademark usage requirements are verified.

The repository filename and displayed project identity are sufficient to establish the intended subject, but they do **not** establish provenance or redistribution rights. Do not infer an asset license from the software project's code license.

| Deployable path | Identified project/platform | Verification status |
| --- | --- | --- |
| `assets/platform/adguard-home.svg` | AdGuard Home | Upstream artwork source/terms to verify |
| `assets/platform/beszel.svg` | Beszel | Upstream artwork source/terms to verify |
| `assets/platform/caddy.svg` | Caddy | Upstream artwork source/terms to verify |
| `assets/platform/debian.svg` | Debian | Upstream artwork source/terms to verify |
| `assets/platform/docker.svg` | Docker | Upstream artwork source/terms to verify |
| `assets/platform/netbird.svg` | NetBird | Upstream artwork source/terms to verify |
| `assets/platform/ntfy.svg` | ntfy | Upstream artwork source/terms to verify |
| `assets/platform/proxmox.svg` | Proxmox | Upstream artwork source/terms to verify |
| `assets/platform/searxng.svg` | SearXNG | Upstream artwork source/terms to verify |
| `assets/platform/uptime-kuma.svg` | Uptime Kuma | Upstream artwork source/terms to verify |
| `assets/services/audiobookshelf.svg` | Audiobookshelf | Upstream artwork source/terms to verify |
| `assets/services/element.svg` | Element | Upstream artwork source/terms to verify |
| `assets/services/immich.svg` | Immich | Upstream artwork source/terms to verify |
| `assets/services/jellyfin.svg` | Jellyfin | Upstream artwork source/terms to verify |
| `assets/services/navidrome.svg` | Navidrome | Upstream artwork source/terms to verify |
| `assets/services/nextcloud.svg` | Nextcloud | Upstream artwork source/terms to verify |
| `assets/services/paperless-ngx.svg` | Paperless-ngx | Upstream artwork source/terms to verify |
| `assets/services/vaultwarden.svg` | Vaultwarden | Upstream artwork source/terms to verify |

## Deliberate boundaries

- Presence in the public deployment artifact means an asset is technically published by the website; it does not mean GoreeCloud owns the underlying third-party mark.
- The eventual HTML/CSS/JavaScript/Python source license must be evaluated separately from creative-content and trademark rights.
- GoreeCloud identity artwork may use different reuse terms from source code if that is the approved project-specific decision.
- Third-party marks must not be described as GoreeCloud-owned artwork.
- A third-party software project's open-source license must not be treated as automatic permission to redistribute its logo under that same license.
- Replacing or adding a public asset requires updating both `PUBLIC_ASSET_FILES` and this inventory in the same reviewed change.
- Repository-only design experiments, source material, or unused artwork remain outside the deployment artifact unless explicitly allowlisted.

## Publication gate

This inventory intentionally leaves provenance and rights fields unresolved where the repository does not currently establish them. Issue #5 remains open until the actual source-license, creative-asset terms, copyright notice, history review, and repository-visibility decisions are completed.
