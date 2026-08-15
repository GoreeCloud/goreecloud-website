# GoreeCloud Website Stability Baseline

## Current stable version

The repository-defined stable version is **5.10.0**.

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

## 5.10.0 scope

Version 5.10.0 consolidates the production-hardening work completed after the v5.9 baseline:

- current public GoreeCloud software-portfolio reconciliation;
- corrected Cloudflare Pages pull-request preview targeting;
- fail-closed exact-candidate deployment verification;
- maintainable deployment-verifier structure;
- dedicated regression coverage for branch-preview resolution and hostname safety;
- dedicated regression coverage for the public software-portfolio progressive-enhancement contract;
- continued dependency-free static publication, no analytics or tracking, strict security headers, Glaze UI validation, accessibility validation, and isolated `dist/` publication.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
