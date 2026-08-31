# GoreeCloud Website

Canonical source for the main GoreeCloud public website and the Projects, Roadmap, Blog, and Archive destinations deployed through Cloudflare Pages.

## Current baseline

- Current accepted website package: **v5.24.0**
- Current accepted production design language before this migration is deployed: **Glaze UI 2.0.0 Stable**
- Current source migration target: **Glaze UI 2.1.0 Stable**
- Glaze UI 2.1 Stable promotion reference: `c49113eb8b93c267613fdf1bbca1f814495acad7`
- Glaze UI authority: `GoreeCloud/goreecloud-glaze-ui`
- Branding and approved visual-asset authority: `GoreeCloud/goreecloud-branding-assets`
- Repository inventory reviewed on **2026-08-29**: **56 repositories — 40 public, 16 private**
- Public website portfolio: **10 active destinations**

`VERSION` is the canonical machine-readable version source for the last accepted website package. Version metadata is repository-only release metadata and does not establish deployment or production acceptance by itself.

Glaze UI 2.1.0 is the current Stable design-system contract. This migration branch adopts it at source/build level, but the public websites do not inherit production 2.1 conformance by declaration. Exact repository validation, rendered branch-preview review, authorized merge, and exact production deployment verification remain required.

## Official GoreeCloud public websites

This repository is responsible for five of the ten current destinations:

| Destination | Domain | Source |
| --- | --- | --- |
| GoreeCloud | `www.goreecloud.com` | repository root |
| Projects | `projects.goreecloud.com` | `sites/projects/` |
| Roadmap | `roadmap.goreecloud.com` | `sites/roadmap/` |
| Blog | `blog.goreecloud.com` | `sites/blog/` |
| Archive | `archive.goreecloud.com` | `sites/archive/` |

The wider ecosystem also includes GoreeCloud Suite, Design Center, Privacy Center, Security Center, and Continuity Center in their respective canonical repositories.

## Public-web principles

The browser surface is intentionally static, privacy-preserving, and evidence-scoped:

- static HTML, locally hosted CSS, JavaScript, and approved visual assets;
- no advertising, behavioral analytics, tracking, fingerprinting, or third-party browser-loaded fonts;
- no unsupported production or security claims;
- public/private GitHub repository boundaries are preserved;
- application and platform-system claims are tied to current source, project specifications, and accepted evidence;
- every deployable main-site page is normalized onto Glaze UI 2.1.0 Stable before artifact validation;
- durable content surfaces remain solid while interaction uses controlled glaze.

The six substantive GoreeCloud platform systems are Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity. Their names represent actual design, privacy, security, continuity, coordination, identity, authentication, and authorization responsibilities rather than decorative branding.

## Design and accessibility

Glaze UI is treated as a design contract, not merely a stylesheet or theme. The shared Glaze UI 2.1 web layer is the current source target for typography, spacing, materials, navigation, cards, buttons, forms, focus treatment, responsive behavior, reduced-motion and reduced-transparency preferences, forced-colors support, minimum interaction targets, mobile safe areas, and print resilience.

The core 2.1 material rule is **Content is solid. Interaction is glazed.** Durable reading surfaces use solid Surface material; navigation, transient controls, selected interactive emphasis, and deliberately live interaction surfaces may use controlled Glaze material. The web contract also carries explicit clarity/density modes, a 56px Touch Assistance floor, large-text fallbacks, and deterministic material/performance fallbacks.

Site-specific CSS may extend that layer while preserving Glaze UI hierarchy and accessibility contracts. Importing tokens alone is not considered conformance.

The automated checks are regression controls, not a claim of complete WCAG conformance. Release acceptance still requires appropriate human interaction review, representative viewport review, keyboard testing, and screen-reader testing where applicable.

## Content and repository authority

`docs/repository-portfolio.json` is the machine-readable authority for the reviewed GoreeCloud GitHub portfolio shown on the public site. It is intentionally separate from runtime or production-readiness evidence.

`docs/public-runtime-status.json` records reviewed public maturity and migration claims. Repository visibility must never be treated as evidence of production acceptance.

Approved GoreeCloud logos, product icons, system marks, artwork, and derivatives come from `GoreeCloud/goreecloud-branding-assets`. New products without an approved canonical asset use a neutral presentation until an asset is approved; the website must not invent an “official” mark.

`docs/public-asset-inventory.md` records reviewed publication and provenance facts for deployable creative assets. The inventory is not a license grant. Official artwork is required when it exists, and publication eligibility remains separate from mere repository presence.

## Source license and creative-rights boundary

The website source code, repository automation, validation scripts, and technical repository documentation are licensed under the **Apache License 2.0**. The authoritative source-license identifier is **Apache-2.0**, and the top-level `LICENSE` contains the reviewed license text.

`NOTICE` records the separate creative-rights boundary. The source license does not grant unrestricted reuse of GoreeCloud trade names, logos, branding, editorial identity, or third-party marks. `docs/public-asset-inventory.md` is not a license grant.

Issue #5 remains open as the separate human-controlled reachable-history, contextual-disclosure, creative-rights, and repository-publication decision. The final human reachable-history/contextual-disclosure review remains required where publication or creative-rights review applies. Passing CI does not itself authorize a repository visibility change, publication decision, trademark use, or release.

## Build and publication allowlist

The main public site is built as an explicit allowlisted artifact:

```bash
python scripts/build_public_site.py
```

Build output directory: `dist`.

The publication boundary is exact, per-file allowlisted. Adding a file to `assets/`, `css/`, `js/`, the repository root, or another source directory does not automatically add it to the deployable artifact. The build renders repository facts, normalizes the homepage, applies Glaze UI 2.1.0 Stable, and writes only approved paths to `dist/`.

Issue #6 is closed: the isolated `dist/` Cloudflare Pages cutover is complete. This records the deployment architecture only; it does not eliminate exact candidate and post-merge deployment verification.

## Validation

Before a revision is accepted, run the repository validators and tests used by CI. The canonical local commands include:

```bash
python scripts/validate_repository_hygiene.py
python scripts/validate_repository_history.py
python scripts/validate_license.py
python scripts/validate_public_assets.py
python scripts/validate_accessibility.py
python scripts/validate_glaze_ui.py
python -m unittest discover -s tests -p "test_*.py"
```

The repository-history preflight must run from a non-shallow checkout so reachable historical blobs are actually reviewed. Its reporting must identify a failing location or class of finding without echoing a sensitive matched value into CI output.

The broader CI contract also validates the Suite/capability manifests, governance readiness, repository portfolio, public runtime status, security reporting, Wardveil/observability boundaries, privacy statement, browser-origin integrity, application identity, public semantics, full public surface, Cloudflare deployment contract, performance budget, isolated artifact, remote verifier configuration, repository guidance, release-evidence records, JavaScript syntax, branch preview, and post-merge production deployment.

Key validators and sources include:

- `scripts/validate_repository_portfolio.py`
- `scripts/validate_public_assets.py`
- `scripts/validate_public_runtime_status.py`
- `scripts/validate_public_semantics.py`
- `scripts/validate_public_surface.py`
- `scripts/validate_accessibility.py`
- `scripts/validate_glaze_ui.py`
- `scripts/validate_browser_origin_integrity.py`
- `scripts/validate_deployment_contract.py`
- `scripts/validate_performance_budget.py`
- `scripts/validate_build_artifact.py`
- `docs/glaze-ui-conformance.md`
- `docs/glaze-ui-2.1-public-sites.md`
- `docs/glaze-ui-2.0-public-sites.md` (historical adoption record)
- `docs/stability-baseline.md`
- `docs/release-readiness-checklist.md`
- `docs/release-evidence-template.md`

## Runtime-status boundary

The website must not turn development intent into a production claim. In particular, GoreeCloud Monitor remains a separately accepted replacement path: Uptime Kuma remains the current production availability monitor until a controlled GoreeCloud Monitor cutover is accepted and documented by its authoritative project evidence.

The same principle applies to every application and platform system. Source availability, a successful build, green CI, a release-candidate label, branding, or a public website card cannot manufacture production, privacy, security, continuity, identity, or conformance state.

## Deployment and release acceptance

Cloudflare Pages deploys reviewed static artifacts. Exact accepted production revisions are recorded in the GoreeCloud Public Websites and Cloudflare Pages project specification in Google Drive.

A branch preview is evidence, not a release. Passing CI does not itself authorize merge, production deployment, a public claim upgrade, or broader product acceptance. The exact pull-request candidate must pass branch-preview verification; after merge, the exact resulting `main` revision must pass production verification. Source, isolated artifact, and deployed bytes must agree.

Glaze UI 2.0 production acceptance does not automatically transfer to 2.1. Each website must earn repository-local 2.1 acceptance for the exact deployed revision.

Deployment success does not by itself authorize broader product, privacy, security, continuity, identity, or production-readiness claims.

## Maintenance rules

When public behavior, architecture, project state, design-system conformance, branding authority, repository inventory, or deployment scope changes:

1. update the canonical source rather than adding a competing source of truth;
2. keep public claims evidence-scoped;
3. update the GoreeCloud project specification in `GoreeCloud/Projects`;
4. append the canonical website changelog in `GoreeCloud/Changelogs`;
5. verify Cloudflare Pages and GitHub status before treating the revision as accepted.

Do not restore references to the retired `goreecloud-logo` repository. The unified authority is `GoreeCloud/goreecloud-branding-assets`.
