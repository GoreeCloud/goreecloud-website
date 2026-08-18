# GoreeCloud Website Stability Baseline

## Current stable version

The repository-defined stable version is **5.15.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only; neither is part of the isolated Cloudflare `dist/` publication allowlist.

## Stability definition

A GoreeCloud website revision is considered stable only when all of the following are true:

1. The exact source revision passes the complete `Validate public website` workflow.
2. Repository hygiene and reachable-history validation pass.
3. Source-license, governance-readiness, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.
4. Structural accessibility and Glaze UI design-contract checks pass.
5. Application identity, public semantics, and full public-surface checks pass.
6. Cloudflare deployment-contract and performance-budget checks pass.
7. The isolated `dist/` artifact builds and validates successfully.
8. Remote-verifier configuration and regression tests pass.
9. JavaScript syntax and failure-resilience checks pass.
10. Pull-request candidates pass exact branch-preview deployment verification before merge.
11. The resulting `main` revision passes exact production deployment verification after merge.

A passing branch preview alone is not a stable release. A merge alone is not a stable release. Stability requires the reviewed source, isolated artifact, and deployed production bytes to agree.

## 5.15.0 scope

Version 5.15.0 integrates Wardveil Security by GoreeCloud into the public security-reporting experience, moves vulnerability reports to the dedicated `security@goreecloud.com` role address, and establishes a fail-closed observability contract appropriate to the website's anonymous static architecture.

The release:

- presents Wardveil Security by GoreeCloud on the public security-reporting surface using existing Glaze UI 1.0 semantics rather than creating a separate security visual system;
- preserves Wardveil as a security identity and presentation layer while keeping source validation, browser security headers, Cloudflare Pages publication, policies, and application-specific safeguards authoritative for their respective technical states;
- deliberately avoids a blanket `Protected by Wardveil` assurance on the public website;
- routes public vulnerability reports through `security@goreecloud.com` and synchronizes `security.html`, `SECURITY.md`, and `.well-known/security.txt` around the dedicated security role address;
- adds `docs/wardveil-security-and-observability.md` as the repository contract for Wardveil presentation, operational evidence, privacy boundaries, error handling, future dynamic-feature logging requirements, and Stable-release gating;
- adds a fail-closed Wardveil/observability validator and makes that validator part of the exact-revision CI workflow;
- defines current observability through exact-revision CI, repository/history checks, isolated artifact validation, branch-preview verification, production verification, scheduled remote verification, and responsible security reporting rather than visitor tracking;
- explicitly rejects client analytics, session replay, fingerprinting, browser telemetry exporters, and runtime browser network clients as observability shortcuts;
- records authentication, authorization, application-database, administrator-action, and server-side request-correlation event families as not applicable to the current anonymous static runtime, while requiring any future dynamic backend capability to add structured privacy-conscious logging and audit evidence before Stable classification;
- refuses to assume that provider-level logs are enabled, retained, exported, or sufficient merely because a hosting provider may support logging;
- preserves the static homepage and static-first privacy boundary;
- preserves GoreeCloud Monitor as the repository identity for the native monitoring project while public product language uses GoreeCloud Monitoring for the replacement path;
- preserves the Glaze UI 1.0 design contract, including semantic tokens and adaptive ranges;
- preserves privacy, local assets, accessibility and resilience requirements, isolated publication through Cloudflare Pages, and exact deployment verification.

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

Version 5.15.0 does not change the canonical Glaze UI version. Wardveil-facing public website content consumes the established Glaze UI surface, token, focus, accessibility, adaptive, and resilience semantics. Wardveil remains a security identity rather than a competing design system.

## Observability and future dynamic-feature boundary

The current website has no application backend, account system, authentication, authorization, state-changing form processor, application database, server-side session store, or application-owned API runtime. Adding any of those capabilities changes the observability and security model.

A future dynamic revision must not inherit the current static-site `not applicable` determinations without review. Required operational and security events, correlation identifiers, sensitive-data exclusions, retention and access rules, retry/failure behavior, monitoring integration, audit expectations, and validation evidence must be defined and tested before Stable classification.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, application production cutover, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
