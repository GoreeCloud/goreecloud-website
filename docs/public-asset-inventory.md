# GoreeCloud Public Asset Inventory

This inventory records the publication classification of artwork retained by `GoreeCloud/goreecloud-website`. It is **not a license grant**. Official artwork is required when it exists, and identity artwork must be source-traceable before deployment. The source-code license does not automatically license GoreeCloud branding or third-party marks. Third-party trademarks and artwork remain the property of their respective owners; use is referential and does not imply sponsorship, endorsement, or affiliation.

The canonical detailed provenance records are intentionally not duplicated here. `docs/visual-identity-sources.json` and the Suite manifest retain the applicable **Source authority**, **Source revision/path**, and **Reviewed Git blob** evidence, and `scripts/validate_public_assets.py` checks those records against the current retained file bytes. This document controls publication classification only.

Final human reachable-history/contextual-disclosure review remains required for source-publication decisions, and **Issue #5 remains open** until that separate review is resolved. Passing validation does not replace the explicit repository visibility/publication decision.

## Deployable artwork

Only artwork listed here may enter the rebuilt Main Cloudflare Pages artifact, and it must also appear in the exact build allowlist. Repository presence does not make a file deployable.

- `assets/goreecloud-logo.svg`

The approved GoreeCloud master mark is the rebuilt Main website's only deployable identity artwork. Products without approved canonical artwork use text-only presentation rather than an invented icon.

## Source-only reviewed artwork

The following reviewed assets remain in repository source for provenance, migration/history, or separately governed GoreeCloud surfaces. They are **not part of the current public build allowlist** and must not be published by the rebuilt Main website artifact.

- `assets/platform/adguard-home.svg`
- `assets/platform/caddy.svg`
- `assets/platform/debian.svg`
- `assets/platform/docker.png`
- `assets/platform/netbird.svg`
- `assets/platform/proxmox.svg`
- `assets/platform/uptime-kuma.svg`
- `assets/roadmap/frigate.svg`
- `assets/roadmap/home-assistant.png`
- `assets/suite/ai.svg`
- `assets/suite/app-store.svg`
- `assets/suite/backup.svg`
- `assets/suite/bookmarks.svg`
- `assets/suite/browser.svg`
- `assets/suite/calendar.svg`
- `assets/suite/changelogs.svg`
- `assets/suite/code.svg`
- `assets/suite/contacts.svg`
- `assets/suite/dns.svg`
- `assets/suite/documents.svg`
- `assets/suite/drive.svg`
- `assets/suite/feed.svg`
- `assets/suite/file-manager.svg`
- `assets/suite/gallery.svg`
- `assets/suite/gateway.svg`
- `assets/suite/identity.svg`
- `assets/suite/index.svg`
- `assets/suite/keyboard.svg`
- `assets/suite/launcher.svg`
- `assets/suite/location.svg`
- `assets/suite/mail.svg`
- `assets/suite/manager.svg`
- `assets/suite/maps.svg`
- `assets/suite/memos.svg`
- `assets/suite/messenger.svg`
- `assets/suite/monitor.svg`
- `assets/suite/music.svg`
- `assets/suite/network.svg`
- `assets/suite/notes.svg`
- `assets/suite/notify.svg`
- `assets/suite/photos.svg`
- `assets/suite/search.svg`
- `assets/suite/sync.svg`
- `assets/suite/tasks.svg`
- `assets/suite/terminal.svg`
- `assets/suite/vault.svg`
- `assets/suite/video.svg`
- `assets/social/github.ico`
- `assets/social/instagram.ico`
- `assets/social/pinterest.ico`
- `assets/social/reddit.ico`
- `assets/social/threads.ico`
- `assets/social/tiktok.ico`
- `assets/social/x.ico`
- `assets/social/youtube.ico`

These files may remain valid evidence or assets for another independently governed surface, but that does not authorize Main to publish them. Their presence in source is not a statement that every associated product, service, or third party is currently integrated, production-ready, or endorsed.

## Retired source-only historical/provenance artwork

The following older upstream-service marks are retained solely for historical traceability, migration context, attribution/provenance review, and repository-history continuity. Historical repository presence does not authorize artwork use. They are not GoreeCloud-native product identities, are not part of the current public build allowlist, and **must not be published by the current GoreeCloud website artifact**.

- `assets/services/actual-budget.png`
- `assets/services/audiobookshelf.svg`
- `assets/services/element.svg`
- `assets/services/immich.svg`
- `assets/services/jellyfin.svg`
- `assets/services/matrix.svg`
- `assets/services/navidrome.png`
- `assets/services/nextcloud.svg`
- `assets/services/onlyoffice.ico`
- `assets/services/paperless-ngx.svg`
- `assets/services/stirling-pdf.png`
- `assets/services/vaultwarden.svg`

## Non-identity publication preview retained in source

`assets/social-preview.png` is retained as historical/publication-preview source material. It is not canonical GoreeCloud identity artwork and is not included in the rebuilt Main artifact. Its presence in the repository does not restore the retired social-card composition or authorize deployment.

## Publication boundary

A change from source-only or retired to deployable requires an explicit change to the build allowlist and this classification record, applicable provenance review, current branding authority, and all required publication/rights review. A build script, HTML reference, or passing test cannot silently promote an asset into the public artifact.
