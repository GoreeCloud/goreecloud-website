# GoreeCloud Website Stability Baseline

## Current release version

The repository-defined release version is **5.17.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only; neither is part of the isolated Cloudflare `dist/` publication allowlist. A source revision carrying this version is not considered stable merely because the version metadata exists; it must satisfy the full stability definition below.

## Stability definition

A GoreeCloud website revision is considered stable only when all of the following are true:

1. The exact source revision passes the complete `Validate public website` workflow.
2. Repository hygiene and reachable-history validation pass.
3. Source-license, governance-readiness, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.
4. Structural accessibility and Glaze UI design-contract checks pass.
5. Application identity, public semantics, and full public-surface checks pass.
6. Repository portfolio integrity validation confirms the reviewed total/public/private counts, functional grouping, directory completeness, private-link boundary, and static homepage summary.
7. Public runtime status integrity validation confirms that accepted production services, release candidates, active development projects, and controlled migration boundaries are not reversed or overstated by the public website.
8. Cloudflare deployment-contract and performance-budget checks pass.
9. The isolated `dist/` artifact builds and validates successfully.
10. Remote-verifier configuration and regression tests pass.
11. JavaScript syntax and failure-resilience checks pass.
12. Pull-request candidates pass exact branch-preview deployment verification before merge.
13. The resulting `main` revision passes exact production deployment verification after merge.

A passing branch preview alone is not a stable release. A merge alone is not a stable release. Stability requires the reviewed source, isolated artifact, and deployed production bytes to agree.

## 5.17.0 scope

Version 5.17.0 corrects public runtime-status drift discovered after the production-verified 5.16.0 repository-portfolio release. The release establishes a repository-only runtime-status authority and a fail-closed validation gate so source maturity, repository visibility, deployment maturity, and production replacement claims remain separate properties.

The release:

- corrects GoreeCloud Notify from an inaccurate active/replaced-ntfy presentation to its authoritative **Release Candidate** state;
- explicitly preserves **ntfy as the current production notification service** until GoreeCloud Notify completes target backup/restore, monitoring and independent outage alerting, runtime/private-publication validation, manual browser/OS acceptance, controlled migration, and tested rollback;
- removes the inaccurate historical/public statement that GoreeCloud Notify had already replaced ntfy;
- preserves GoreeCloud Notify's private repository and release-candidate source maturity without treating either source validation or repository existence as production acceptance;
- corrects GoreeCloud Memos from the stale **Stabilizing** presentation to **Available Now**, reflecting the accepted Stable v0.1.2 production service;
- preserves the accepted GoreeCloud Search cutover: GoreeCloud Search has replaced the direct SearXNG-facing search service;
- preserves the GoreeCloud Monitor transition boundary: Uptime Kuma remains the current production availability monitor while GoreeCloud Monitoring remains the controlled replacement path;
- updates `index.html` consistently across service cards, platform cards, representative project cards, platform transition notes, and historical timeline text;
- updates `repositories.html` so the Notify and Memos repository roles reflect their actual deployment maturity without publishing private source links;
- adds `docs/public-runtime-status.json` as a repository-only public-status authority for the reviewed Memos, Notify, Search, and Monitoring transition states;
- adds `scripts/validate_public_runtime_status.py` to fail closed on status reversal, premature replacement claims, loss of accepted production claims, or migration-boundary drift;
- adds a named `Validate public runtime status integrity` CI step and binds that command into `scripts/validate_workflow_security.py` so the gate cannot be silently removed;
- corrects the existing project-portfolio regression tests that previously enforced the wrong Notify replacement claim and adds explicit Memos production regression coverage;
- preserves the 5.16.0 static homepage and repository-portfolio authority, 28/22/6 repository inventory, and no-runtime-GitHub-fetch boundary;
- preserves the 5.15.0 Wardveil Security reporting path, dedicated `security@goreecloud.com` contact, telemetry-free observability contract, security headers, and privacy boundary;
- preserves isolated Cloudflare `dist/` publication, exact preview/production verification, and fail-closed deployment validation.

## Runtime-status authority and migration boundary

`docs/public-runtime-status.json` is repository metadata and remains outside the generated public artifact. It records only the public-safe maturity state necessary to prevent the website from confusing source development with production deployment.

The reviewed 5.17.0 authority distinguishes four representative states:

- **GoreeCloud Memos:** accepted Stable production at v0.1.2;
- **GoreeCloud Notify:** release candidate; ntfy remains current production pending controlled acceptance and cutover;
- **GoreeCloud Search:** accepted production replacement for the direct SearXNG-facing search service;
- **GoreeCloud Monitoring:** active development/replacement path; Uptime Kuma remains current production availability monitoring.

A repository becoming public, a CI run becoming green, a release candidate being published, or a source tree becoming deployable does not by itself change production state. Production replacement claims require the applicable target-environment, recovery, monitoring, manual acceptance, controlled cutover, and rollback evidence owned by that product.

The runtime-status validator is intentionally narrow. It protects reviewed public claims but does not become a competing authoritative application specification. When an application's authoritative project record changes after a real accepted cutover or rollback, this website authority must be deliberately revalidated and updated in the same release that changes the public claim.

## Glaze UI stable-release boundary

Glaze UI is a design contract and a visual identity requirement. Automated conformance checks are necessary regression evidence, but they do not replace visual acceptance, manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, or touch-device review when a material interface change warrants those checks.

Version 5.17.0 does not change the canonical Glaze UI version or introduce a new page composition. The runtime-status corrections use existing Glaze UI 1.0 badges, platform states, cards, typography, semantic tokens, adaptive ranges, focus behavior, and resilience semantics. The static homepage remains the public authority for its rendered copy; this release changes factual status content and fail-closed governance rather than the design-system authority.

The stable boundary explicitly preserves the existing **semantic tokens**, **adaptive ranges**, static homepage delivery, GoreeCloud Monitor transition language, privacy controls, and isolated publication model from earlier stable releases.

## Repository portfolio authority and privacy boundary

`docs/repository-portfolio.json` remains the repository-only machine-readable authority for repository names, visibility states, group membership, and derived totals. The separate `docs/public-runtime-status.json` controls reviewed public maturity claims. These records are complementary and must not be collapsed into one property: **repository visibility does not determine runtime maturity**.

Both records must remain outside the public artifact and must not contain credentials, private source contents, private hostnames, private IP addresses, internal topology, administrative endpoints, or sensitive implementation data. Private repository cards may identify an intentionally public product role but must not expose direct private repository links.

The browser must not fetch either repository metadata record or GitHub inventory at runtime. Repository counts, grouping, and runtime-status claims are source-controlled release facts validated before publication rather than collected from visitors or fetched dynamically.

## Wardveil Security, privacy, and observability boundary

Wardveil Security by GoreeCloud remains the platform security identity and presentation layer; it does not replace technical security controls or evidence. The v5.17.0 status correction does not add authentication, authorization, a backend API, application storage, visitor analytics, browser error export, session replay, fingerprinting, or remote telemetry.

Current observability remains source- and deployment-bound through exact-revision CI, isolated artifact validation, exact preview and production verification, scheduled remote checks, and responsible security reporting. The site's privacy-first static architecture remains unchanged.

## Observability and future dynamic-feature boundary

The current website has no application backend, account system, authentication, authorization, state-changing form processor, application database, server-side session store, or application-owned API runtime. Adding any of those capabilities changes the observability and security model.

A future dynamic revision must not inherit the current static-site `not applicable` determinations without review. Required operational and security events, correlation identifiers, sensitive-data exclusions, retention and access rules, retry/failure behavior, monitoring integration, audit expectations, and validation evidence must be defined and tested before Stable classification.

## Release boundaries

Stable-version metadata does **not** authorize a repository visibility change, DNS change, Cloudflare project-setting change, application production cutover, network migration, backup-platform cutover, or creative-rights/publication decision. Those remain separate controlled actions.

The open creative-rights and source-publication review remains authoritative for repository visibility decisions. Third-party platform-mark review is not bypassed by a successful stable release.
