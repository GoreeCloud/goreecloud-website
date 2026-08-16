# GoreeCloud Website

Public static website for GoreeCloud.

## Version

Current website package: **v5.12.0 — Glaze UI 1.0 conformance alignment**

`VERSION` is the canonical machine-readable version source. `docs/stability-baseline.md` defines the release scope and the evidence required before a revision is treated as stable. `docs/glaze-ui-conformance.md` records the website's targeted Glaze UI version and conformance state.

## Role

This repository contains the public-facing GoreeCloud website. It explains GoreeCloud's purpose, public software work, representative platform technologies, and long-term direction without publishing private infrastructure details.

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

The public software portfolio is static HTML. JavaScript is limited to appearance, navigation state, section highlighting, and the footer year so the normal and no-JavaScript experiences expose the same public project information.

## Current public software portfolio

The current public portfolio includes GoreeCloud Manager, GoreeCloud Monitor, GoreeCloud Notes, GoreeCloud Memos, GoreeCloud Research Library, GoreeCloud Bookmarks, GoreeCloud Feed, GoreeCloud Gallery, and GoreeVault Server.

GoreeCloud Tasks, GoreeCloud Contacts, and GoreeCloud Notify remain represented as active private development without public repository links.

GoreeCloud Monitor is an active native monitoring project. **Uptime Kuma remains the current production availability monitor** until GoreeCloud Monitor completes parallel validation and an explicit authorized cutover.

## Source license and creative-rights boundary

The website source code, repository automation, validation scripts, and technical repository documentation are licensed under the **Apache License 2.0**. The authoritative source-license identifier is **Apache-2.0**, and the top-level `LICENSE` contains the reviewed license text.

`NOTICE` records the separate creative-rights boundary. The source license does not grant unrestricted reuse of GoreeCloud trade names, logos, branding, editorial identity, or third-party marks.

`docs/public-asset-inventory.md` is the working deployable-artwork inventory and is **not a license grant**. It records publication and provenance evidence for the exact public asset set, but provenance and rights verification still requires the applicable human and legal review.

Issue #5 remains open for the remaining third-party platform-mark review, the final human repository-history/contextual review, and the explicit repository visibility/publication decision. Passing CI does not itself authorize a repository visibility change or a creative-rights decision.

## Public site structure

- `index.html` — homepage, current static software portfolio, and primary search/social metadata;
- `privacy.html` — public website privacy statement;
- `security.html` — public security-reporting policy;
- `404.html` — custom noindex not-found experience;
- `.well-known/security.txt` — standardized public security-reporting contact;
- `site.webmanifest` — browser application identity;
- `robots.txt` and `sitemap.xml` — crawler and canonical discovery metadata;
- `_headers` — Cloudflare Pages security, privacy, indexing, and resource-policy headers;
- `assets/` — self-hosted artwork source; only explicitly approved files are deployable;
- `css/` — Glaze UI, responsive, accessibility, and section presentation;
- `js/theme-init.js` — early local appearance initialization;
- `js/main.js` — appearance, navigation, section-state, and footer-year progressive behavior.

Repository-only CI validators, GitHub metadata, release records, publication-review material, tests, development documentation, and version metadata remain outside the public artifact.

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

The 5.12.0 alignment preserves the site's established visual identity while standardizing the implementation underneath it. The shared foundation includes:

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

## Privacy and browser boundary

Glaze UI alignment does not introduce remote UI dependencies. The public website continues to use local/system typography and local artwork. It contains no analytics, trackers, ad technology, remote font delivery, remote icon delivery, runtime browser API client, form backend, account system, database, service worker, or browser storage beyond the explicit local appearance preference.

The implementation and public privacy statement are validated together so a browser capability cannot be added silently without updating the documented boundary.

## Repository tooling

The production-readiness tooling is intentionally dependency-light and uses the Python standard library where practical.

Core commands and gates include:

- `python scripts/build_public_site.py` — build the exact allowlisted `dist/` artifact;
- `python scripts/validate_build_artifact.py` — prove the artifact contains only reviewed public files;
- `python scripts/validate_repository_hygiene.py` — reject current-tree sensitive file types, credential signatures, symlinks, and unsafe artifacts;
- `python scripts/validate_repository_history.py` — perform the repository-history preflight across reachable history;
- `python scripts/validate_license.py` — validate Apache-2.0 source terms and NOTICE/README boundaries;
- `python scripts/validate_accessibility.py` — enforce structural accessibility invariants;
- `python scripts/validate_glaze_ui.py` — enforce the website Glaze UI 1.0 contract and conformance record;
- `python scripts/validate_browser_origin_integrity.py` — keep browser-loaded resources origin-local and reject prohibited runtime clients;
- `python scripts/validate_performance_budget.py` — keep the static public artifact within explicit payload and request ceilings;
- `python scripts/validate_public_surface.py` — validate links, canonical state, sitemap, crawler policy, and cross-page integrity;
- `python scripts/validate_deployment_contract.py` — enforce the static Cloudflare Pages architecture and headers;
- `python scripts/validate_privacy_policy.py` — keep public privacy guidance synchronized with implementation;
- `python scripts/validate_security_policy.py` — validate public security-reporting behavior and `security.txt` freshness;
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

Do not publish vulnerability details, credentials, tokens, private hostnames, private IP addresses, or other sensitive operational information in public issue or pull-request content. Use the public security-reporting guidance at the GoreeCloud website security page.
