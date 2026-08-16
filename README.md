# goreecloud-website

Public static website for GoreeCloud.

## Version

Current website package: **v5.11.0 — static-first portfolio and monitoring transition**

`VERSION` is the canonical machine-readable version source. `docs/stability-baseline.md` records the release scope, stability definition, and release boundaries for the current website revision.

## Role

This repository contains the public-facing GoreeCloud website. It explains GoreeCloud's purpose, public software work, representative platform technologies, and long-term direction without publishing private infrastructure details.

The browser surface is deliberately small and privacy-preserving:

- static HTML;
- locally hosted CSS and JavaScript;
- locally hosted images and project artwork;
- no browser analytics, advertising, behavioral tracking, or fingerprinting;
- no third-party browser-loaded render resources or fonts;
- no third-party JavaScript framework;
- no runtime browser network clients;
- no service worker;
- no Cloudflare Pages Functions or Worker runtime.

The public software portfolio is static HTML. JavaScript is limited to appearance, navigation state, section highlighting, and the footer year so the no-JavaScript and normal experiences expose the same project information.

## Current public software portfolio

Public repository links are shown only for projects that are currently published. The current public portfolio includes GoreeCloud Manager, GoreeCloud Monitor, GoreeCloud Notes, GoreeCloud Memos, GoreeCloud Research Library, GoreeCloud Bookmarks, GoreeCloud Feed, GoreeCloud Gallery, and GoreeVault Server.

GoreeCloud Tasks, GoreeCloud Contacts, and GoreeCloud Notify remain represented as active private development without public repository links. GoreeCloud Monitor is in active development; **Uptime Kuma remains the current production availability monitor until GoreeCloud Monitor completes parallel validation and an explicit cutover**.

## Source license and creative-rights boundary

The website source code, repository automation, validation scripts, and technical repository documentation are licensed under the **Apache License 2.0**. The authoritative source-license identifier is **Apache-2.0**, and the top-level `LICENSE` contains the reviewed license text.

`NOTICE` records the separate creative-rights boundary. The source license does not grant unrestricted reuse of GoreeCloud trade names, logos, branding, editorial identity, or third-party marks.

`docs/public-asset-inventory.md` is the working deployable-artwork inventory and is **not a license grant**. Issue #5 remains open for the remaining third-party platform-mark review, the final human repository-history/contextual review, and the explicit repository-publication/visibility decision. Passing CI does not itself authorize a repository visibility change, DNS change, creative-rights decision, or other publication action.

## Public site structure

- `index.html` — homepage, current static software portfolio, and primary search/social metadata;
- `privacy.html` — public website privacy statement;
- `security.html` — public security-reporting policy;
- `404.html` — custom noindex not-found experience;
- `.well-known/security.txt` — standardized security-reporting contact;
- `site.webmanifest` — browser application identity;
- `robots.txt` and `sitemap.xml` — crawler and canonical discovery metadata;
- `_headers` — Cloudflare Pages security, privacy, and indexing headers;
- `assets/` — self-hosted artwork source; only explicitly approved files are deployable;
- `css/` — Glaze UI and responsive presentation;
- `js/theme-init.js` — early appearance initialization;
- `js/main.js` — appearance, navigation, section-state, and footer-year progressive behavior.

Repository-only CI validators, GitHub metadata, release records, publication-review material, tests, and development documentation remain outside the public artifact.

## Cloudflare Pages deployment

The website is deployed through Cloudflare Pages using Git integration.

The production settings are:

- Production branch: `main`
- Framework preset: `None`
- Build command: `python scripts/build_public_site.py`
- Build output directory: `dist`
- Root directory: blank

`dist/` is the production boundary. The build is **exact, per-file allowlisted** rather than directory-published. Adding a file to `assets/`, `css/`, `js/`, the repository root, or any other source directory does not make that file public. A file becomes deployable only when it is intentionally added to the public allowlist and passes the applicable privacy, security, accessibility, Glaze UI, performance, artifact, and deployment checks.

The isolated `dist/` Cloudflare Pages cutover is complete for production and branch previews. Issue #6 is closed and remains historical implementation context for that completed migration. Exact preview and production verification continue to prove that the deployed bytes and headers match the reviewed candidate boundary.

The live canonical website is `https://www.goreecloud.com/`; the apex domain redirects permanently to the `www` hostname.

## Glaze UI and accessibility

The website is the public implementation of **Glaze UI**, GoreeCloud's shared visual and interaction language. **Glaze UI is treated as a design contract**, not a decorative layer.

The current implementation includes System, Light, and Dark appearance modes, operating-system appearance detection, local-only explicit-theme persistence, layered surfaces, rounded geometry, responsive layouts, visible keyboard focus, mobile navigation, reduced-motion and reduced-transparency behavior, increased-contrast and forced-colors support, print behavior, touch-friendly controls, and consistent GoreeCloud branding across human-facing pages.

The automated checks are regression controls, not a claim of complete WCAG conformance. Formal accessibility acceptance still requires manual keyboard review, screen-reader testing, zoom/reflow inspection, color-contrast review, touch-device review, and visual Glaze UI acceptance where appropriate.

## Privacy and browser boundary

The browser JavaScript remains non-networked. CI rejects browser networking, cookie, worker, and service-worker APIs unless the privacy and deployment architecture is deliberately revised first.

When a visitor explicitly chooses Light or Dark mode, the site stores only the `goreecloud-theme` preference in local browser storage. Returning to System mode removes the override. No account, profile, analytics identifier, or server-side visitor record is created by the site.

The deployed response policy uses a restrictive Content Security Policy, `Referrer-Policy: no-referrer`, and a Permissions Policy that denies browser capabilities the static site does not need.

## Security and repository hygiene

Do not commit passwords, API keys, tokens, `.env` files, SSH private keys, private network addresses, private hostnames, internal administrative details, backup destinations, recovery credentials, or private family information.

The current-tree hygiene validator rejects selected secret-bearing file types, private-key material, reusable credential signatures, symlinks, editor artifacts, and other inappropriate repository content.

The separate **repository-history preflight** requires a **non-shallow checkout** and scans every reachable historical blob path plus eligible text content for prohibited secret paths, private-key material, selected reusable credential signatures, private-network address patterns, and selected internal identifiers. Findings disclose only the finding class, object identifier, and historical path—not the matched value.

A green automated history scan is useful evidence but is not a substitute for the final human repository-history/contextual review required by issue #5.

## Repository tooling

Production-readiness tooling is dependency-light and primarily uses the Python standard library:

- `scripts/build_public_site.py` — builds the isolated `dist/` artifact from an explicit allowlist;
- `scripts/validate_build_artifact.py` — proves the generated artifact contains exactly the reviewed public files;
- `scripts/validate_repository_hygiene.py` — current-tree sensitive-content and repository-hygiene checks;
- `scripts/validate_repository_history.py` — reachable-history publication-safety preflight;
- `scripts/validate_license.py` — Apache-2.0 and NOTICE-boundary validation;
- `scripts/validate_governance_readiness.py` — governance applicability and readiness boundaries;
- `scripts/validate_accessibility.py` — structural accessibility regression controls;
- `scripts/validate_glaze_ui.py` — Glaze UI design-contract validation;
- `scripts/validate_browser_origin_integrity.py` — origin-local browser-resource and non-networked-JavaScript enforcement;
- `scripts/validate_public_surface.py` — links, fragments, crawler policy, sitemap, and canonical-surface checks;
- `scripts/validate_deployment_contract.py` — Cloudflare static-publication contract;
- `scripts/validate_performance_budget.py` — public payload and request-count budgets;
- `scripts/verify_remote_deployment.py` — exact preview/production HTTP and artifact verification;
- `scripts/validate_repository_guidance.py` — repository safety and maintenance guidance validation;
- `scripts/validate_release_evidence.py` — release-evidence record validation;
- `tests/test_project_portfolio_contract.py` — static project-inventory, repository-link, no-JavaScript, and monitoring-transition regression coverage;
- `tests/test_stability_baseline.py` — version, stability-contract, guidance synchronization, and release-boundary regression coverage.

## Validation

Run the production checks from the repository root. The reachable-history check requires a complete Git history.

```bash
python scripts/validate_workflow_security.py
python scripts/validate_repository_hygiene.py
python scripts/validate_repository_history.py
python scripts/validate_license.py
python scripts/validate_governance_readiness.py
python scripts/validate_security_policy.py
python scripts/validate_privacy_policy.py
python scripts/validate_browser_origin_integrity.py
python scripts/validate_accessibility.py
python scripts/validate_glaze_ui.py
python scripts/validate_app_identity.py
python scripts/validate_public_semantics.py
python scripts/validate_public_surface.py
python scripts/validate_deployment_contract.py
python scripts/validate_performance_budget.py
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
python scripts/verify_remote_deployment.py --check-config
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate_repository_guidance.py
python scripts/validate_release_evidence.py
python scripts/validate_site.py
python scripts/validate_resilience.py
node --check js/theme-init.js
node --check js/main.js
```

GitHub Actions runs these gates on pull requests and pushes to `main`. External Actions are pinned to immutable revisions, workflow permissions remain read-only, persisted checkout credentials are disabled, and validation uses full reachable history where required.

Pull requests additionally verify the exact Cloudflare branch-preview candidate. Pushes to `main` verify the exact production deployment. A passing branch preview alone is not a stable release, and a merge alone is not a stable release.

## Release boundary

PR validation and Cloudflare preview deployment are pre-release evidence, not authorization to publish. Before a production merge, confirm the exact intended candidate, green CI, successful exact branch-preview verification, current release/version documentation, and the applicable issue #5 publication-rights boundary. After merge, exact production verification must also succeed.

Issue #6 documents the already-completed isolated-artifact Cloudflare cutover; it is no longer a pending release prerequisite. Repository visibility, DNS, Cloudflare project-setting changes, and creative-rights/publication decisions remain separate explicit actions.

Passing CI does not itself authorize a merge, repository visibility change, DNS change, or other production/publication action. A production-ready repository state also does not establish formal accessibility conformance or complete the remaining issue #5 publication-rights and visibility review.
