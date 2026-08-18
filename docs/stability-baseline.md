# GoreeCloud Website Stability Baseline

## Current release version

The repository-defined release version is **5.18.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only; neither is part of the isolated Cloudflare `dist/` publication allowlist. A source revision carrying this version is not considered stable merely because the version metadata exists; it must satisfy the full stability definition below.

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

## 5.18.0 scope

Version 5.18.0 turns the 28-repository directory into a more usable first-party discovery surface without changing its static authority, privacy model, inventory, repository visibility, or runtime-status boundaries. The release is a Glaze UI interaction and progressive-enhancement pass over the production-verified 5.17.0 runtime-status baseline.

The release:

- preserves all **28 repositories: 22 public and 6 private** and the existing 11 functional groups as source-controlled static HTML;
- adds first-party repository text search over repository names, descriptions, purposes, roles, and functional-group context;
- adds a functional-group selector derived from the rendered directory rather than from a second browser-side inventory;
- adds All/Public/Private visibility controls with explicit selected-state semantics;
- adds a local result-count status message, a clear no-results state, and a reset control that restores all repositories and focus to the search field;
- keeps the discovery controls entirely progressive: if JavaScript is unavailable, no incomplete search UI is shown and the complete static directory remains readable and navigable;
- keeps repository discovery entirely local and ephemeral: filter state is not written to localStorage, sessionStorage, the URL, browser history, or a network request;
- uses existing Glaze UI semantic tokens, 48-pixel comfortable control targets, rounded search/select/button geometry, visible focus treatment, light/dark theme inheritance, and restrained selected-state emphasis;
- transforms the discovery layout for Medium and Compact adaptive ranges rather than merely shrinking the desktop composition;
- removes nonessential control motion under reduced-motion preferences and provides reduced-transparency, increased-contrast, and forced-colors fallbacks;
- ensures print restores the complete repository directory even when the interactive browser view is currently filtered;
- extends `scripts/validate_repository_portfolio.py` so discovery privacy, accessibility semantics, adaptive behavior, and print/no-JavaScript resilience fail closed with the portfolio itself;
- expands `tests/test_repository_portfolio.py` with explicit local/network-independence and print-fallback regression tests;
- preserves the 5.17.0 runtime-status authority and all Memos, Notify/ntfy, Search, and Monitoring/Uptime Kuma maturity boundaries;
- preserves the 5.16.0 static homepage and repository-portfolio authority and no-runtime-GitHub-fetch boundary;
- preserves the 5.15.0 Wardveil Security reporting path, dedicated `security@goreecloud.com` contact, telemetry-free observability contract, security headers, and privacy boundary;
- preserves isolated Cloudflare `dist/` publication, exact preview/production verification, and the existing performance budgets.

## Repository discovery progressive-enhancement boundary

The repository directory remains authoritative static HTML. JavaScript does not generate repository facts, repository cards, portfolio counts, visibility states, canonical GitHub URLs, production-status claims, or functional-group membership.

The v5.18.0 enhancement operates only over already-rendered repository cards. It may hide and reveal cards and groups in response to local search/group/visibility input, but it cannot add repositories or change their source-controlled facts. Result counts are derived from the rendered cards, so the browser enhancement does not become a competing inventory authority.

Search and filter values are intentionally ephemeral. They are not persisted to browser storage, encoded into query parameters or fragments, written to browser history, or transmitted to a server. The current static site's `connect-src 'none'` browser boundary remains unchanged.

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

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

Version 5.18.0 does not change the canonical Glaze UI version. It applies the existing Glaze UI 1.0 search-field, text-input, select, button, semantic-token, target-size, selected-state, adaptive-layout, focus, motion, contrast, forced-colors, translucency-fallback, and print/resilience semantics to the repository directory. The complete static directory remains the no-JavaScript content authority.

The stable boundary explicitly preserves the existing **semantic tokens**, **adaptive ranges**, static homepage delivery, GoreeCloud Monitor transition language, privacy controls, and isolated publication model from earlier stable releases.

## Repository portfolio authority and privacy boundary

`docs/repository-portfolio.json` remains the repository-only machine-readable authority for repository names, visibility states, group membership, and derived totals. The separate `docs/public-runtime-status.json` controls reviewed public maturity claims. These records are complementary and must not be collapsed into one property: **repository visibility does not determine runtime maturity**.

Both records must remain outside the public artifact and must not contain credentials, private source contents, private hostnames, private IP addresses, internal topology, administrative endpoints, or sensitive implementation data. Private repository cards may identify an intentionally public product role but must not expose direct private repository links.

The browser must not fetch either repository metadata record or GitHub inventory at runtime. Repository counts, grouping, and runtime-status claims are source-controlled release facts validated before publication rather than collected from visitors or fetched dynamically. The v5.18.0 discovery enhancement filters only the already-rendered static cards and does not introduce another data source.

## Wardveil Security, privacy, and observability boundary

Wardveil Security by GoreeCloud remains the platform security identity and presentation layer; it does not replace technical security controls or evidence. The v5.18.0 directory enhancement does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, remote telemetry, search telemetry, or query persistence.

Current observability remains source- and deployment-bound through exact-revision CI, isolated artifact validation, exact preview and production verification, scheduled remote checks, and responsible security reporting. The site's privacy-first static architecture remains unchanged.

## Observability and future dynamic-feature boundary

The current website has no application backend, account system, authentication, authorization, state-changing form processor, application database, server-side session store, or application-owned API runtime. Adding any of those capabilities changes the observability and security model.

A future dynamic revision must not inherit the current static-site `not applicable` determinations without review. Required operational and security events, correlation identifiers, sensitive-data exclusions, retention and access rules, retry/failure behavior, monitoring integration, audit expectations, and validation evidence must be defined and tested before Stable classification.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, application production cutover, network migration, backup-platform cutover, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
