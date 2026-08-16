# GoreeCloud Website Stability Baseline

## Current stable version

The repository-defined stable version is **5.12.0**.

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

## 5.12.0 scope

Version 5.12.0 advances the stable v5 foundation by aligning the website with the active **Glaze UI 1.0** design-system contract while preserving the accepted public appearance and the static-first privacy model introduced in 5.11.0.

The release:

- records the website's target Glaze UI version and conformance state in `docs/glaze-ui-conformance.md`;
- aligns the website foundation with canonical `--glaze-*` semantic tokens while retaining compatibility aliases for established section styles;
- formalizes Canvas, Solid, Raised, Glaze, and Overlay surface semantics without forcing translucency onto every component;
- standardizes Glaze UI target sizing, focus geometry, motion durations, easing, blur, shadows, radii, spacing, and semantic status colors;
- exposes the Compact, Medium, Expanded, and Wide adaptive ranges defined by Glaze UI 1.0;
- strengthens solid fallbacks when backdrop filtering is unsupported or reduced transparency is requested;
- strengthens reduced-motion behavior so nonessential animation and smooth scrolling are removed;
- updates the Glaze UI validator so semantic tokens, motion, adaptive ranges, resilience fallbacks, canonical-version targeting, and the conformance record cannot silently drift;
- retains the static homepage and current public project inventory from 5.11.0, including GoreeCloud Monitor and the explicit Uptime Kuma production-monitoring boundary;
- preserves privacy, local assets, dependency-light delivery, GoreeCloud identity, and isolated publication through Cloudflare Pages.

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

The 5.12.0 alignment intentionally does not redesign the accepted public composition. Visual acceptance is therefore preserved while the underlying design-system semantics and automated contract are strengthened.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
