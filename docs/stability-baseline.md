# GoreeCloud Website Stability Baseline

## Current stable version

The repository-defined stable version is **5.11.0**.

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

## 5.11.0 scope

Version 5.11.0 advances the stable v5 foundation with a current, static-first public software portfolio and monitoring-transition clarity:

- adds GoreeCloud Monitor to the public software portfolio as an active native development project;
- keeps Uptime Kuma explicitly identified as the current production availability monitor until GoreeCloud Monitor completes parallel validation and an authorized cutover;
- moves the current public project inventory into the static homepage so the same project information remains available without JavaScript;
- removes the now-unnecessary JavaScript portfolio-injection layer, reducing client-side complexity and improving progressive-resilience, accessibility, search visibility, and maintainability;
- reconciles GoreeCloud Bookmarks with its current public maintained-fork status rather than the older planning-only fallback;
- synchronizes repository guidance with the canonical SemVer release metadata and the completed isolated `dist/` Cloudflare Pages cutover;
- extends regression coverage so current public project identities, repository links, static fallback behavior, release metadata, Glaze UI, privacy, and isolated publication remain protected together.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
