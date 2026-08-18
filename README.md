# GoreeCloud Website

Public static website for GoreeCloud.

## Version

Current website package: **v5.18.0 — local repository discovery and adaptive directory experience**

`VERSION` is the canonical machine-readable version source. `docs/stability-baseline.md` defines the release scope and the evidence required before a revision is treated as stable. `docs/glaze-ui-conformance.md` records the website's targeted Glaze UI version and conformance state. `docs/wardveil-security-and-observability.md` defines the website-specific Wardveil Security and observability boundary. `docs/repository-portfolio.json` is the repository-only machine-readable authority for the current public/private GitHub portfolio counts and grouping. `docs/public-runtime-status.json` is the separate repository-only authority for reviewed public maturity and migration claims that must not be inferred from repository visibility.

## Role

This repository contains the public-facing GoreeCloud website. It explains GoreeCloud's purpose, public software work, representative platform technologies, current repository portfolio, and long-term direction without publishing private infrastructure details.

The browser surface is intentionally small, static, and privacy-preserving:

- static HTML;
- locally hosted CSS and JavaScript;
- locally hosted images and project artwork;
- no browser analytics, advertising, behavioral tracking, or fingerprinting;
- no third-party browser-loaded render resources or fonts;
- no third-party JavaScript framework;
- no runtime browser network clients;
- no service worker;
- no Cloudflare Pages Functions or Worker runtime.

The authoritative repository directory and homepage repository summary are static HTML. JavaScript provides appearance, mobile-navigation behavior, section highlighting, footer-year progressive behavior, and a local-only repository discovery enhancement. The complete repository directory remains available when JavaScript is unavailable. Repository search/filter terms are ephemeral: they are not stored, placed in the URL, or transmitted over the network. Repository counts, visibility, grouping, public/private boundaries, and reviewed runtime-status claims remain source-controlled static facts available to crawlers, assistive technology, and no-JavaScript users.

## Current software repository portfolio

The authenticated GoreeCloud repository inventory currently contains **28 repositories: 22 public and 6 private**. The dedicated `repositories.html` page groups those repositories into **11 functional groups** and records a concise public description, purpose, role, visibility, and production boundary for each.

Public repositories link directly to their GitHub source. GoreeCloud Tasks, GoreeCloud Contacts, GoreeCloud Notify, GoreeCloud Wardveil Security, GoreeCloud Privacy Shield, and the `goreecloud-website` deployment-source repository remain private and are identified without publishing private source contents.

The portfolio includes Glaze UI; GoreeCloud Manager; GoreeCloud Identity; GoreeVault Server; Wardveil Security; Privacy Shield; GoreeCloud Backup; GoreeCloud Network, its dashboard source and Android client; GoreeCloud DNS; GoreeCloud Research Library; GoreeCloud Notes; GoreeCloud Memos; GoreeCloud Bookmarks and its browser extension; GoreeCloud Tasks; GoreeCloud Contacts; GoreeCloud Calendar; GoreeCloud Notify; GoreeCloud Monitor; GoreeCloud Search; GoreeCloud Feed; GoreeCloud Browser; GoreeCloud Redirector; GoreeCloud Source Resync; GoreeCloud Gallery; and this website.

The public homepage intentionally presents a representative software overview instead of duplicating the exhaustive repository directory. On the directory page, first-party progressive enhancement adds text search, functional-group selection, public/private visibility controls, reset behavior, and an assistive-technology status message over the already-rendered static cards. The controls derive their options and counts from the rendered directory rather than creating a competing inventory source.

`docs/repository-portfolio.json`, `scripts/validate_repository_portfolio.py`, and `tests/test_repository_portfolio.py` fail closed when declared counts, public/private visibility, required public links, private-link boundaries, homepage summary, exhaustive directory content, local-only discovery behavior, adaptive Glaze UI presentation, or print/no-JavaScript resilience drift from the reviewed portfolio.

Public source availability does not imply production acceptance. GoreeCloud Network remains under controlled fork-to-native development while the existing NetBird environment remains the current private-network production platform. GoreeCloud Backup remains under active development while current accepted recovery systems remain authoritative. **GoreeCloud Memos v0.1.2 is accepted Stable production. GoreeCloud Search is the current GoreeCloud-facing private-search layer. GoreeCloud Notify is a release candidate and ntfy remains the current production notification service until controlled production acceptance and cutover. Uptime Kuma remains the current production availability monitor**, but it is explicitly transitional while **GoreeCloud Monitoring** completes validation and an authorized cutover.

`docs/public-runtime-status.json`, `scripts/validate_public_runtime_status.py`, and the project-portfolio regression suite protect these reviewed maturity boundaries. A public repository, green CI run, published release candidate, or deployable source tree is not treated as proof of a production cutover.

## Source license and creative-rights boundary

The website source code, repository automation, validation scripts, and technical repository documentation are licensed under the **Apache License 2.0**. The authoritative source-license identifier is **Apache-2.0**, and the top-level `LICENSE` contains the reviewed license text.

`NOTICE` records the separate creative-rights boundary. The source license does not grant unrestricted reuse of GoreeCloud trade names, logos, branding, editorial identity, or third-party marks.

`docs/public-asset-inventory.md` is the working deployable-artwork inventory and is **not a license grant**. It records publication and provenance evidence for the exact public asset set, but provenance and rights verification still requires the applicable human and legal review.

Issue #5 remains open for the remaining third-party platform-mark review, the final human repository-history/contextual review, and the explicit repository visibility/publication decision. Passing CI does not itself authorize a repository visibility change or a creative-rights decision.

## Public site structure

- `index.html` — homepage, representative software overview, static repository summary, platform information, roadmap, public story, social links, and primary search/social metadata;
- `repositories.html` — dedicated canonical directory of all current GoreeCloud GitHub repositories, progressively enhanced with local search/group/visibility filtering;
- `privacy.html` — public website privacy statement;
- `security.html` — public Wardveil Security responsible-reporting policy;
- `404.html` — custom noindex not-found experience;
- `.well-known/security.txt` — standardized public security-reporting contact;
- `site.webmanifest` — browser application identity;
- `robots.txt` and `sitemap.xml` — crawler and canonical discovery metadata;
- `_headers` — Cloudflare Pages security, privacy, indexing, and resource-policy headers;
- `assets/` — self-hosted artwork source; only explicitly approved files are deployable;
- `css/` — Glaze UI, responsive, accessibility, repository-directory, and section presentation;
- `js/theme-init.js` — early local appearance initialization;
- `js/main.js` — appearance, navigation, section-state, repository discovery, and footer-year progressive behavior.

Repository-only CI validators, GitHub metadata, release records, publication-review material, tests, development documentation, observability contracts, repository-portfolio metadata, runtime-status metadata, and version metadata remain outside the public artifact.

## Cloudflare Pages deployment

The website is deployed through Cloudflare Pages using Git integration.

Production settings:

- Production branch: `main`
- Framework preset: `None`
- Build command: `python scripts/build_public_site.py`
- Build output directory: `dist`
- Root directory: blank

`dist/` is the production boundary. The build is **exact, per-file allowlisted** rather than directory-published. Adding a file to `assets/`, `css/`, `js/`, the repository root, or another source directory does **not** make that file public. A file becomes deployable only when it is deliberately added to the public allowlist and passes the applicable privacy, security, accessibility, Glaze UI, performance, artifact, and deployment checks.

The isolated `dist/` Cloudflare Pages cutover is complete for production and branch previews. **Issue #6 is closed** and remains historical implementation context for that completed migration. Exact preview and production verification continue to prove that deployed bytes and headers match the reviewed candidate boundary.

The canonical public website is `https://www.goreecloud.com/`. The apex domain redirects permanently to the `www` hostname.

## Glaze UI 1.0 and visual identity

The website is a GoreeCloud reference implementation of **Glaze UI 1.0**. **Glaze UI is treated as a design contract**, not a decorative stylesheet.

The canonical shared design-system source is `GoreeCloud/glaze-ui`. The website records its target and conformance state in `docs/glaze-ui-conformance.md` rather than silently assuming compatibility.

The 5.18.0 candidate preserves the site's established visual identity, 5.17.0 runtime-status integrity, 5.16.0 static repository authority, 5.15.0 Wardveil integration, and earlier theme-surface corrections. The repository discovery controls use existing semantic tokens and the Glaze UI search/input/button interaction vocabulary rather than adding an external component framework. The discovery surface transforms across Compact and Medium layouts, uses 48-pixel comfortable control targets, provides explicit focus treatment and selected states, removes nonessential motion under reduced-motion preferences, has reduced-transparency/increased-contrast/forced-colors fallbacks, and restores the complete repository directory for print.

The shared foundation includes:

- semantic `--glaze-*` design tokens for canvas, surfaces, text, semantic colors, spacing, radii, target sizes, blur, shadows, focus, motion, and content widths;
- the Canvas, Solid, Raised, Glaze, and Overlay surface hierarchy;
- 44-pixel minimum and 48-pixel comfortable interactive target sizing;
- Instant 90 ms, Fast 160 ms, Standard 220 ms, and Emphasized 320 ms motion semantics;
- shared standard and emphasized easing;
- Compact (through 599 px), Medium (600–1023 px), Expanded (1024–1439 px), and Wide (1440 px+) adaptive ranges;
- System, Light, and Dark appearance modes;
- local-only explicit-theme persistence;
- selective translucency, softened depth, rounded geometry, purposeful gradients, and restrained elevation;
- semantic success, warning, and danger presentation;
- visible keyboard focus and no-JavaScript navigation resilience;
- reduced-motion, reduced-transparency, increased-contrast, forced-colors, and print behavior;
- solid-surface fallback when backdrop filtering is unavailable.

The application-specific website palette and composition remain intentional GoreeCloud personality. Glaze UI family resemblance does not require every GoreeCloud interface to use identical layouts or colors.

The automated checks are regression controls, not a claim of complete WCAG conformance. Material interface changes still warrant manual keyboard review, **screen-reader testing**, zoom/reflow inspection, color-contrast review, touch-device review, and explicit visual acceptance.

## Wardveil Security and observability

**Wardveil Security by GoreeCloud** is the platform security identity used by the public security-reporting experience. Wardveil is a security identity and presentation layer; it does not replace the underlying source validation, Cloudflare Pages configuration, security headers, policies, or application-specific controls that establish technical state.

The dedicated public reporting address is **security@goreecloud.com** and is published consistently in `security.html`, `SECURITY.md`, and `.well-known/security.txt`.

The current website is an anonymous static site with no authentication, authorization, application database, backend API, state-changing forms, administrative interface, server-side session store, or application-owned request-processing service. Those event families are therefore not applicable to the current website runtime. A future dynamic capability cannot reuse that classification: it must add privacy-conscious structured operational and security logging, sensitive-data exclusions, retention/access controls, failure behavior, and validation before Stable classification.

Current observability is source- and deployment-bound rather than visitor-tracking based. Exact-revision CI, isolated artifact validation, branch-preview verification, production verification, scheduled deployment checks, and the public security-reporting channel provide release and operational evidence without introducing client analytics or telemetry.

The website deliberately does **not** add browser error reporting, analytics, session replay, fingerprinting, or a remote telemetry exporter. Provider-side logging capability is not treated as enabled or sufficient unless separately verified and documented.

The public website does not use the phrase **Protected by Wardveil** as a blanket assurance. Any future protection-status use must be tied to an evidenced scope under the governing Wardveil standard.

## Privacy and browser boundary

Glaze UI alignment, Wardveil presentation, observability governance, static repository-directory publication, local repository discovery, and runtime-status governance do not introduce remote UI dependencies. The public website continues to use local/system typography and local artwork. It contains no analytics, trackers, ad technology, remote font delivery, remote icon delivery, runtime browser API client, form backend, account system, database, service worker, or browser storage beyond the explicit local appearance preference.

The repository discovery enhancement operates entirely over the already-rendered DOM. Search terms, selected groups, and visibility filters are not persisted to localStorage or sessionStorage, are not placed in query strings or history state, and are not sent through fetch, XMLHttpRequest, Beacon, or another network path. If JavaScript is unavailable, users receive the complete unfiltered static directory rather than an incomplete or broken search experience.

Repository portfolio and runtime-status metadata are repository-only. The browser does not fetch GitHub inventory or status metadata, and private repository URLs are not published from the directory. The implementation, public privacy statement, Wardveil/observability contract, repository-portfolio validator, and runtime-status validator are kept aligned so browser data collection, runtime networking, dynamic security-sensitive behavior, portfolio drift, or maturity-claim drift cannot be added silently without updating the documented boundary.

## Repository tooling

The production-readiness tooling is intentionally dependency-light and uses the Python standard library where practical.

Core commands and gates include:

- `python scripts/build_public_site.py` — build the exact allowlisted `dist/` artifact;
- `python scripts/validate_build_artifact.py` — prove the artifact contains only reviewed public files;
- `python scripts/validate_repository_hygiene.py` — reject current-tree sensitive file types, credential signatures, symlinks, and unsafe artifacts;
- `python scripts/validate_repository_history.py` — perform the repository-history preflight across reachable history;
- `python scripts/validate_license.py` — validate Apache-2.0 source terms and NOTICE/README boundaries;
- `python scripts/validate_accessibility.py` — enforce structural accessibility invariants across human-facing pages;
- `python scripts/validate_glaze_ui.py` — enforce the website Glaze UI 1.0 contract and conformance record;
- `python scripts/validate_browser_origin_integrity.py` — keep browser-loaded resources origin-local and reject prohibited runtime clients;
- `python scripts/validate_performance_budget.py` — keep the static public artifact within explicit payload and request ceilings;
- `python scripts/validate_public_surface.py` — validate links, canonical state, sitemap, crawler policy, and cross-page integrity;
- `python scripts/validate_deployment_contract.py` — enforce the static Cloudflare Pages architecture and headers;
- `python scripts/validate_privacy_policy.py` — keep public privacy guidance synchronized with implementation;
- `python scripts/validate_security_policy.py` — validate Wardveil public security-reporting behavior and `security.txt` freshness;
- `python scripts/validate_wardveil_observability.py` — fail closed on Wardveil identity drift, security-contact drift, observability-contract removal, prohibited browser telemetry, or runtime exporter introduction;
- `python scripts/validate_repository_portfolio.py` — fail closed on repository-count, visibility, public-link, private-link, static-homepage, directory-completeness, local-discovery privacy, adaptive/resilience behavior, and stale-inventory drift;
- `python scripts/validate_public_runtime_status.py` — fail closed on reviewed production-state, release-candidate, replacement, and migration-boundary drift;
- `python scripts/verify_remote_deployment.py` — compare deployed public bytes and live headers with the exact reviewed candidate.

Run the complete offline regression suite with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The repository-history preflight requires a **non-shallow checkout** so the complete reachable history can be examined. Sensitive-history validators report the path and classification while avoiding disclosure of the actual **matched value** when printing it would expose reusable private material.

## Isolated public artifact

Build locally with:

```bash
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
```

The public decision is the exact `PUBLIC_FILES` allowlist in `scripts/build_public_site.py`, not directory location. Files such as `README.md`, `SECURITY.md`, `.github/`, `scripts/`, `tests/`, `docs/`, `VERSION`, development records, local environment files, credentials, private keys, or unapproved artwork must never become public merely because they exist in the repository.

## Release and authorization boundary

A branch preview is evidence, not a release. A merge is evidence, not a complete stability declaration. The candidate must pass the full repository workflow and exact branch-preview verification before merge, and the resulting `main` revision must pass exact production deployment verification after merge.

The current stability contract is defined in `docs/stability-baseline.md`.

Passing CI does not itself authorize DNS changes, Cloudflare project-setting changes, repository visibility changes, public exposure of private infrastructure, production cutovers for other GoreeCloud applications, or the remaining issue #5 creative-rights/publication decision.

## Security reporting

Do not publish vulnerability details, credentials, tokens, private hostnames, private IP addresses, or other sensitive operational information in public issue or pull-request content. Use the public Wardveil Security reporting guidance at the GoreeCloud website security page or email **security@goreecloud.com**.
