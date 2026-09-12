# Glaze UI 2.2 — GoreeCloud public websites

Status: migration implementation and per-site acceptance in progress.

## Release baseline

- Target: **Glaze UI 2.2.0 Stable**.
- Canonical release: `GoreeCloud/goreecloud-glaze-ui` tag `v2.2.0`.
- Stable release commit: `6731098b28dd0393faa878c70d989a221d714a20`.
- Rollback baseline: Glaze UI 2.1.0 Stable until each destination independently re-earns 2.2 production acceptance.
- Delivery policy: same-origin assets for every independently deployed public website; no third-party runtime UI dependency.

## Official public-web inventory

| Destination | Source authority | 2.2 migration rule |
| --- | --- | --- |
| Main Website | `goreecloud-website` | Preserve platform-first hierarchy and privacy-first messaging. |
| Projects | `goreecloud-website/sites/projects` | Preserve repository/project discovery and status semantics. |
| Roadmap | `goreecloud-website/sites/roadmap` | Keep planned vs active-development claims explicit. |
| Blog | `goreecloud-website/sites/blog` | Preserve editorial hierarchy and readable long-form surfaces. |
| Archive | `goreecloud-website/sites/archive` | Preserve archival purpose and historical-context cues. |
| Suite | `goreecloud-suite` | Keep application discovery primary; use approved app identities. |
| Design Center | `goreecloud-glaze-ui/website` | It is the reference consumer and must remain aligned with the released 2.2 contract. |
| Privacy Center | `goreecloud-privacy-shield/website` | Use only approved Privacy Shield identity assets. |
| Security Center | `goreecloud-wardveil-security/website` | Use the approved Wardveil/Sentinel Fold identity; source and committed build output must agree. |
| Continuity Center | `goreecloud-everkeep/website` | Use approved Everkeep identity and continuity/recovery semantics. |
| Identity Center | `goreecloud-identity` | First-party source surface; publication/custom-domain acceptance remains a separate deployment gate. |

A product repository is not automatically a public website. Application consoles and product UIs remain outside this public-site inventory unless their repository/deployment configuration explicitly declares an independent public web destination.

## 2.2 web contract

The public sites retain their existing information architecture but standardize the interaction layer around the 2.2 contract:

- 48 px normal and 56 px assisted touch/reachability targets.
- Logical block/inline sizing and safe-area-aware mobile padding.
- A single dominant translucent Glaze surface per composition; ordinary cards remain solid surfaces.
- Standard 2.2 surface radii, elevation restraint, focus visibility, state motion, and deep-dark behavior.
- Responsive navigation that remains keyboard- and touch-operable without viewport clipping.
- Reduced-motion and reduced-transparency behavior with no critical information encoded in motion or translucency.
- High-contrast and forced-colors fallbacks.
- No branding-by-status: product identity and semantic state remain separate.
- Approved logos and product artwork only; candidates and historical marks are not promoted into production.

## Content and asset review

For every destination, migration review must cover:

1. Product/service naming, maturity labels, descriptions, contact information, canonical URLs, social metadata, robots/sitemap entries, and cross-site links.
2. Approved logo/icon/artwork provenance and stale or duplicated assets.
3. Broken local references, missing assets, dead external links, and obsolete third-party product references.
4. Duplicate or contradictory copy across the portfolio.
5. Desktop, tablet, small-mobile, large-text, RTL, keyboard, touch, reduced-motion, reduced-transparency, contrast, and forced-colors behavior.

## Acceptance rule

A source migration does **not** by itself constitute production acceptance. Each independently deployed destination must be validated on the exact revision that is published, including its committed/generated output when applicable. Production status is only advanced after the existing release-evidence and remote-deployment gates pass for that destination.
