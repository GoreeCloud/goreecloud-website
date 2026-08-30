# GoreeCloud Website

Canonical source for the main GoreeCloud public website and the Projects, Roadmap, Blog, and Archive destinations deployed through Cloudflare Pages.

## Current baseline

- Website package: **v5.24.0**
- Production design language: **Glaze UI 2.0.0 Stable**
- Glaze UI authority: `GoreeCloud/goreecloud-glaze-ui`
- Branding and approved visual-asset authority: `GoreeCloud/goreecloud-branding-assets`
- Repository inventory reviewed on **2026-08-29**: **56 repositories — 40 public, 16 private**
- Public website portfolio: **10 active destinations**

Glaze UI 2.1 remains a Candidate and is not used as a Stable production-conformance target by this repository.

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
- every deployable main-site page is normalized onto Glaze UI 2.0.0 Stable before artifact validation.

The six substantive GoreeCloud platform systems are Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity. Their names represent actual design, privacy, security, continuity, coordination, identity, authentication, and authorization responsibilities rather than decorative branding.

## Design and accessibility

The shared Glaze UI 2.0 web layer provides the production baseline for typography, spacing, materials, navigation, cards, buttons, forms, focus treatment, responsive behavior, reduced-motion and reduced-transparency preferences, forced-colors support, minimum interaction targets, mobile safe areas, and print resilience.

Site-specific CSS may extend that layer while preserving Glaze UI hierarchy and accessibility contracts. Importing tokens alone is not considered conformance.

## Content and repository authority

`docs/repository-portfolio.json` is the machine-readable authority for the reviewed GoreeCloud GitHub portfolio shown on the public site. It is intentionally separate from runtime or production-readiness evidence.

`docs/public-runtime-status.json` records reviewed public maturity and migration claims. Repository visibility must never be treated as evidence of production acceptance.

Approved GoreeCloud logos, product icons, system marks, artwork, and derivatives come from `GoreeCloud/goreecloud-branding-assets`. New products without an approved canonical asset use a neutral presentation until an asset is approved; the website must not invent an “official” mark.

## Source license and creative-rights boundary

The website source code, repository automation, validation scripts, and technical repository documentation are licensed under the **Apache License 2.0**. The authoritative source-license identifier is **Apache-2.0**, and the top-level `LICENSE` contains the reviewed license text.

`NOTICE` records the separate creative-rights boundary. The source license does not grant unrestricted reuse of GoreeCloud trade names, logos, branding, editorial identity, or third-party marks. `docs/public-asset-inventory.md` records reviewed deployable-artwork provenance and is not itself a license grant.

Issue #5 remains open as the separate human-controlled reachable-history, contextual-disclosure, creative-rights, and repository-publication decision. Passing CI validates technical boundaries and reviewed bytes; it does not grant trademark rights or authorize a repository visibility change.

## Build

The main public site is built as an explicit allowlisted artifact:

```bash
python3 scripts/build_public_site.py
```

The build renders repository facts, normalizes the homepage, applies Glaze UI 2.0.0 Stable, and writes the isolated deployment artifact to `dist/`.

## Validation

Before a revision is accepted, run the repository validators and tests used by CI. They cover the static deployment allowlist, content rendering, repository inventory, public/private boundaries, privacy invariants, Glaze UI conformance, navigation behavior, accessibility fallbacks, security headers, branding provenance, and Cloudflare Pages artifact expectations.

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
- `docs/glaze-ui-2.0-public-sites.md`
- `docs/stability-baseline.md`

Run the complete offline regression suite with:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Deployment

Cloudflare Pages deploys reviewed static artifacts. Exact accepted production revisions are recorded in the GoreeCloud Public Websites and Cloudflare Pages project specification in Google Drive. A branch preview is evidence, not a release, and a merge alone is not a stable release; exact preview and post-merge production verification remain required by the stability baseline.

Deployment success does not by itself authorize broader product, privacy, security, continuity, identity, or production-readiness claims.

## Maintenance rules

When public behavior, architecture, project state, design-system conformance, branding authority, repository inventory, or deployment scope changes:

1. update the canonical source rather than adding a competing source of truth;
2. keep public claims evidence-scoped;
3. update the GoreeCloud project specification in `GoreeCloud/Projects`;
4. append the canonical website changelog in `GoreeCloud/Changelogs`;
5. verify Cloudflare Pages and GitHub status before treating the revision as accepted.

Do not restore references to the retired `goreecloud-logo` repository. The unified authority is `GoreeCloud/goreecloud-branding-assets`.
