# GoreeCloud Website Stability Baseline

## Current release version

The repository-defined release version is **5.16.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only; neither is part of the isolated Cloudflare `dist/` publication allowlist. A source revision carrying this version is not considered stable merely because the version metadata exists; it must satisfy the full stability definition below.

## Stability definition

A GoreeCloud website revision is considered stable only when all of the following are true:

1. The exact source revision passes the complete `Validate public website` workflow.
2. Repository hygiene and reachable-history validation pass.
3. Source-license, governance-readiness, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.
4. Structural accessibility and Glaze UI design-contract checks pass.
5. Application identity, public semantics, and full public-surface checks pass.
6. Repository portfolio integrity validation confirms the reviewed total/public/private counts, functional grouping, directory completeness, private-link boundary, and static homepage summary.
7. Cloudflare deployment-contract and performance-budget checks pass.
8. The isolated `dist/` artifact builds and validates successfully.
9. Remote-verifier configuration and regression tests pass.
10. JavaScript syntax and failure-resilience checks pass.
11. Pull-request candidates pass exact branch-preview deployment verification before merge.
12. The resulting `main` revision passes exact production deployment verification after merge.

A passing branch preview alone is not a stable release. A merge alone is not a stable release. Stability requires the reviewed source, isolated artifact, and deployed production bytes to agree.

## 5.16.0 scope

Version 5.16.0 reconciles the public repository portfolio with the current GoreeCloud GitHub inventory and removes factual repository inventory from runtime JavaScript. The release is a portfolio-integrity and static-first progressive-enhancement hardening pass over the production-verified 5.15.0 Wardveil/observability baseline.

The release:

- updates the canonical public repository portfolio from the stale 20-repository view to **28 repositories: 22 public and 6 private**;
- organizes the current inventory into **11 functional groups** covering the design system; platform, identity, and security; backup and recovery; private networking and DNS; research and knowledge; bookmarks and web preservation; productivity and personal information; notifications and monitoring; search, feeds, and browser; photos and media; and web presence;
- adds current public-safe repository coverage for GoreeCloud Identity, GoreeCloud Backup, GoreeCloud Network, the Network dashboard source, the Android network client, GoreeCloud DNS, Wardveil Security, and Privacy Shield;
- distinguishes public source availability from production acceptance so maintained forks and replacement projects are not represented as migrated merely because their source repositories exist;
- preserves the current NetBird private-network production boundary while GoreeCloud Network remains under controlled development and migration review;
- preserves current accepted recovery systems while GoreeCloud Backup remains under active development and has not yet earned a production replacement claim;
- preserves Uptime Kuma as the current production availability monitor while GoreeCloud Monitoring remains the validated replacement path;
- keeps Wardveil Security as the platform-wide security and protection identity while Privacy Shield remains the GoreeCloud Browser first-party privacy/content-protection subsystem;
- adds `docs/repository-portfolio.json` as a repository-only machine-readable portfolio authority;
- adds `scripts/validate_repository_portfolio.py` and regression tests that fail closed on count drift, duplicate entries, visibility drift, missing public links, publication of private repository links, missing repository cards, stale 20/16/4 copy, loss of the static homepage repository summary, or reintroduction of JavaScript-generated inventory;
- makes `repositories.html` the exhaustive human-facing directory for all current repositories;
- makes the homepage software cards explicitly representative rather than falsely claiming to enumerate every repository;
- publishes the homepage repository summary directly in HTML so no-JavaScript users, crawlers, and assistive technologies receive the same portfolio facts;
- directly loads `css/repositories.css` from the homepage and removes repository stylesheet/inventory generation from `js/main.js`;
- preserves the 5.15.0 Wardveil Security reporting path, dedicated `security@goreecloud.com` contact, telemetry-free observability contract, security headers, and privacy boundary;
- preserves isolated Cloudflare `dist/` publication, exact preview/production verification, and fail-closed deployment validation.

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

Version 5.16.0 does not change the canonical Glaze UI version. The repository directory and homepage repository summary use the existing Glaze UI 1.0 surface, token, focus, accessibility, adaptive, reduced-motion, reduced-transparency, forced-colors, and resilience semantics. Moving repository content from JavaScript into static HTML changes the content authority and progressive-enhancement boundary, not the design-system authority.

The stable boundary explicitly preserves the existing **semantic tokens**, **adaptive ranges**, static homepage delivery, GoreeCloud Monitor transition language, privacy controls, and isolated publication model from earlier stable releases.

## Repository portfolio authority and privacy boundary

`docs/repository-portfolio.json` is repository metadata and must remain outside the generated public artifact. It records repository names, visibility states, group membership, and derived totals only. It must not become a vehicle for private URLs, source contents, credentials, private hostnames, private IP addresses, internal topology, administrative endpoints, or sensitive implementation data.

The public directory may identify private repositories at a high product-role level when that identity is already intentionally public, but private repository cards must not expose direct repository links. The validator treats publication of a private canonical GitHub repository URL as a failure.

The browser must not fetch GitHub inventory at runtime. Repository counts and grouping are source-controlled release facts and are validated before publication rather than collected from visitors or fetched dynamically.

## Observability and future dynamic-feature boundary

The current website has no application backend, account system, authentication, authorization, state-changing form processor, application database, server-side session store, or application-owned API runtime. Adding any of those capabilities changes the observability and security model.

A future dynamic revision must not inherit the current static-site `not applicable` determinations without review. Required operational and security events, correlation identifiers, sensitive-data exclusions, retention and access rules, retry/failure behavior, monitoring integration, audit expectations, and validation evidence must be defined and tested before Stable classification.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, application production cutover, network migration, backup-platform cutover, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
