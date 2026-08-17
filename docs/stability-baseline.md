# GoreeCloud Website Stability Baseline

## Current stable version

The repository-defined stable version is **5.14.0**.

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

## 5.14.0 scope

Version 5.14.0 reconciles the public website with the current GoreeCloud software replacement paths, completes the homepage project overview, and corrects mixed light/dark Glaze UI surfaces discovered during production review.

The release:

- presents GoreeCloud Notify as the GoreeCloud-facing notification layer replacing direct ntfy presentation;
- presents GoreeCloud Search as the GoreeCloud-facing private-search layer replacing direct SearXNG presentation;
- keeps Uptime Kuma explicitly transitional while GoreeCloud Monitoring completes validation and an authorized cutover;
- updates local-AI public language to use GoreeCloud Search rather than direct SearXNG service branding;
- expands the homepage Projects overview to include the current Calendar, Search, Browser, Redirector, Source Resync, and Bookmarks browser-extension repositories;
- preserves the authoritative 20-repository directory and verified boundary of 16 public repositories and 4 private repositories;
- replaces dark fallback values in repository and platform surfaces with canonical Glaze UI semantic tokens so explicit and system light themes remain consistently light while dark mode remains separately intentional;
- adds regression coverage for replacement-state language, complete homepage project inventory, theme-aware surfaces, and the exact remaining third-party platform-logo set;
- preserves the static-first privacy boundary, local assets, accessibility and resilience requirements, isolated Cloudflare Pages publication, and exact deployment verification contract established by earlier stable releases.

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

Version 5.14.0 does not change the canonical Glaze UI version. It corrects website implementation drift by using the canonical semantic canvas, surface, text, border, status, shadow, focus, and motion tokens instead of dark-only fallback values in theme-aware components.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, application production cutover, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
