# GoreeCloud Website Stability Baseline

## Current release version

The repository-defined release version is **5.21.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only; neither is part of the isolated Cloudflare `dist/` publication allowlist. A source revision carrying this version is not considered stable merely because version metadata exists; it must satisfy the full stability definition below.

## Stability definition

A GoreeCloud website revision is considered stable only when all of the following are true:

1. The exact source revision passes the complete `Validate public website` workflow.
2. Repository hygiene and reachable-history validation pass.
3. Source-license, governance-readiness, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.
4. Structural accessibility and Glaze UI design-contract checks pass.
5. Application identity, public semantics, and full public-surface checks pass.
6. Repository portfolio integrity validation confirms the reviewed total/public/private counts, functional grouping, directory completeness, private-link boundary, static homepage summary, and local-only repository discovery behavior.
7. Public runtime status integrity validation confirms that accepted production services, release candidates, active development projects, and controlled migration boundaries are not reversed or overstated by the public website.
8. Cloudflare deployment-contract and performance-budget checks pass.
9. The isolated `dist/` artifact builds and validates successfully.
10. Remote-verifier configuration and regression tests pass.
11. JavaScript syntax and failure-resilience checks pass.
12. Pull-request candidates pass exact branch-preview deployment verification before merge.
13. The resulting `main` revision passes exact production deployment verification after merge.

A passing branch preview alone is not a stable release. A merge alone is not a stable release. Stability requires the reviewed source, isolated artifact, and deployed production bytes to agree.

## 5.21.0 scope

Version 5.21.0 removes third-party artwork from the deployable website artifact and hardens the platform-identity boundary while preserving the production-verified v5.20 repository portfolio, metadata, Glaze UI 1.1, privacy, security, runtime-status, and isolated-publication contracts.

The release:

- removes all ten `assets/platform/*.svg` paths from `PUBLIC_ASSET_FILES`, leaving only the GoreeCloud favicon, application icon, and social preview as deployable artwork;
- replaces visible Proxmox, Debian, Docker, NetBird, AdGuard Home, Caddy, Beszel, and Uptime Kuma logos with neutral Glaze UI letter marks while preserving descriptive names and official outbound project links;
- simplifies GoreeCloud Monitor and Search platform marks to the same single-frame Glaze UI mark pattern;
- retains historical/reference third-party SVG files only in the private repository and outside `dist/`;
- adds `scripts/validate_public_assets.py` and `tests/test_public_asset_boundary.py` so third-party artwork cannot silently re-enter the deployed allowlist or homepage platform surface;
- adds the creative-asset validator to the exact-head CI workflow before governance/deployment acceptance;
- updates `docs/public-asset-inventory.md` so the remaining issue #5 gate is the final human reachable-history/contextual-disclosure review and explicit repository publication decision, not deployable third-party logo provenance;
- reduces public file count and artifact bytes without raising any HTML, CSS, JavaScript, image, request, or total-artifact ceiling;
- preserves the authenticated **30 repository / 23 public / 7 private / 11 group** portfolio authority from v5.20.0;
- preserves the exact Glaze UI 1.1.0 conformance pin at `5c8320de4f770614a3e2bcf9de2a27f7fcfd920c`;
- preserves the Memos, Notify/ntfy, Search, and Monitoring/Uptime Kuma runtime-status boundaries;
- preserves Wardveil Security reporting, `security@goreecloud.com`, the self-only browser-origin model, `connect-src 'none'`, and telemetry-free operation;
- preserves the exact allowlisted Cloudflare `dist/` publication model and exact branch-preview/production deployment verification requirement.

## Glaze UI 1.1 stable-release boundary

Glaze UI is a design contract and visual-identity requirement. The website now targets Glaze UI 1.1.0 using the exact canonical source revision recorded above rather than assuming compatibility with an unversioned latest design-system state.

The 1.1 adoption is intentionally compatible. It preserves the Glaze UI 1.0 foundation while expanding the website's semantic vocabulary for richer reusable state, density, icon, gutter, safe-area, and overlay behavior. Existing product-specific colors, layouts, imagery, composition, and information architecture remain valid GoreeCloud personality.

The website maps the new semantic roles through `css/glaze-polish.css` and records the mapping in `docs/glaze-ui-conformance.md`. Existing website-specific interaction feedback remains an approved product mapping to the shared state-layer contract rather than being replaced by generic reference-component styling.

Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, touch-device review, or safe-area/device review when a material interface change warrants those checks. The ordinary-viewport visual composition is preserved by this release.

The stable boundary explicitly preserves the existing **semantic tokens**, **adaptive ranges**, static homepage delivery, GoreeCloud Monitor transition language, privacy controls, and isolated publication model from earlier stable releases.

## Repository discovery progressive-enhancement boundary

The repository directory remains authoritative static HTML. JavaScript does not generate repository facts, repository cards, portfolio counts, visibility states, canonical GitHub URLs, production-status claims, or functional-group membership.

The v5.18.0 enhancement remains in force: it operates only over already-rendered repository cards and may hide or reveal cards and groups in response to local search/group/visibility input. Search and filter values are ephemeral and are not persisted to browser storage, encoded into query parameters or fragments, written to browser history, or transmitted to a server. The current static site's `connect-src 'none'` browser boundary remains unchanged.

If JavaScript fails or is disabled, the directory continues to expose every repository. If CSS translucency is unavailable or disabled, discovery controls remain readable on solid surfaces. If reduced motion, increased contrast, or forced colors are requested, the control states remain understandable. Print output deliberately ignores active browser filtering and restores the full directory.

## Runtime-status authority and migration boundary

`docs/public-runtime-status.json` is repository metadata and remains outside the generated public artifact. It records only the public-safe maturity state necessary to prevent the website from confusing source development with production deployment.

The reviewed authority continues to distinguish four representative states:

- **GoreeCloud Memos:** accepted Stable production at v0.1.2;
- **GoreeCloud Notify:** release candidate; ntfy remains current production pending controlled acceptance and cutover;
- **GoreeCloud Search:** accepted production replacement for the direct SearXNG-facing search service;
- **GoreeCloud Monitoring:** active development/replacement path; Uptime Kuma remains current production availability monitoring.

A repository becoming public, a CI run becoming green, a release candidate being published, or a source tree becoming deployable does not by itself change production state. Production replacement claims require the applicable target-environment, recovery, monitoring, manual acceptance, controlled cutover, and rollback evidence owned by that product.

The runtime-status validator is intentionally narrow. It protects reviewed public claims but does not become a competing authoritative application specification. When an application's authoritative project record changes after a real accepted cutover or rollback, this website authority must be deliberately revalidated and updated in the same release that changes the public claim.

## Repository portfolio authority and privacy boundary

`docs/repository-portfolio.json` remains the repository-only machine-readable authority for repository names, visibility states, group membership, and derived totals. The separate `docs/public-runtime-status.json` controls reviewed public maturity claims. These records are complementary and must not be collapsed into one property: **repository visibility does not determine runtime maturity**.

Both records must remain outside the public artifact and must not contain credentials, private source contents, private hostnames, private IP addresses, internal topology, administrative endpoints, or sensitive implementation data. Private repository cards may identify an intentionally public product role but must not expose direct private repository links.

The browser must not fetch either repository metadata record or GitHub inventory at runtime. Repository counts, grouping, and runtime-status claims are source-controlled release facts validated before publication rather than collected from visitors or fetched dynamically.

## Wardveil Security, privacy, and observability boundary

Wardveil Security by GoreeCloud remains the platform security identity and presentation layer; it does not replace technical security controls or evidence. The v5.21.0 platform-identity release does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.

Current observability remains source- and deployment-bound through exact-revision CI, isolated artifact validation, exact preview and production verification, scheduled remote checks, and responsible security reporting. The site's privacy-first static architecture remains unchanged.

## Observability and future dynamic-feature boundary

The current website has no application backend, account system, authentication, authorization, state-changing form processor, application database, server-side session store, or application-owned API runtime. Adding any of those capabilities changes the observability and security model.

A future dynamic revision must not inherit the current static-site `not applicable` determinations without review. Required operational and security events, correlation identifiers, sensitive-data exclusions, retention and access rules, retry/failure behavior, monitoring integration, audit expectations, and validation evidence must be defined and tested before Stable classification.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, application production cutover, network migration, backup-platform cutover, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. The public artifact no longer deploys third-party logo artwork, but the final human reachable-history/contextual-disclosure review and explicit publication decision are not bypassed by a successful stable release.
