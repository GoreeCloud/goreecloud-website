# GoreeCloud Website Stability Baseline

## Current stable version

The repository-defined stable version is **5.13.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only; neither is part of the isolated Cloudflare `dist/` publication allowlist.

## Stability definition

A GoreeCloud website revision is considered stable only when all of the following are true:

1. The exact source revision passes the complete `Validate public website` workflow.
2. Repository hygiene and reachable-history validation pass.
3. Source-license, governance-readiness, privacy, security-reporting, and browser-origin checks pass.
4. Structural accessibility and Glaze UI design-contract checks pass.
5. Application identity, public semantics, and full public-surface checks pass.
6. Cloudflare deployment-contract and performance-budget checks pass.
7. The isolated `dist/` artifact builds and validates successfully.
8. Remote-verifier configuration and regression tests pass.
9. JavaScript syntax and failure-resilience checks pass.
10. Pull-request candidates pass exact branch-preview deployment verification before merge.
11. The resulting `main` revision passes exact production deployment verification after merge.

A passing branch preview alone is not a stable release. A merge alone is not a stable release. Stability requires the reviewed source, isolated artifact, and deployed production bytes to agree.

## 5.13.0 scope

Version 5.13.0 extends the stable Glaze UI 1.0 website foundation with a dedicated GitHub repository directory synchronized to the current authenticated GoreeCloud software portfolio.

The release:

- adds `repositories.html` as a canonical, indexable public directory for the current GoreeCloud repository portfolio;
- represents all 20 current GoreeCloud repositories and preserves the verified boundary of 16 public repositories and 4 private repositories;
- groups repositories by functional role so design-system, platform, security, knowledge, productivity, monitoring, browser, media, and web-presence responsibilities remain understandable;
- publishes direct GitHub links only for repositories that are currently public and identifies private repositories without exposing private source contents;
- adds a Glaze UI repository-directory presentation layer with responsive layouts, reduced-motion behavior, reduced-transparency fallback, and forced-colors support;
- adds repository discovery to the website navigation and homepage progressive-enhancement surface;
- adds the repository directory to the sitemap and exact public-file allowlist;
- expands full-public-surface validation to include the repository directory and its canonical URL;
- expands accessibility and Glaze UI structural validation so the new page is held to the same public-interface contract as the other human-facing pages;
- preserves the static-first privacy boundary, local assets, dependency-light delivery, security headers, isolated Cloudflare Pages publication model, and exact deployed-byte verification.

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

The 5.13.0 repository directory uses the existing Glaze UI 1.0 foundation rather than changing the canonical design system. Its new cards, repository status treatments, responsive composition, and resilience fallbacks remain application-specific website implementation details subject to the shared Glaze UI contract.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
