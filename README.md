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
- every deployable page is normalized onto Glaze UI 2.0.0 Stable before artifact validation.

The six substantive GoreeCloud platform systems are Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity. Their names represent actual design, privacy, security, continuity, coordination, identity, authentication, and authorization responsibilities rather than decorative branding.

## Design and accessibility

The shared Glaze UI 2.0 web layer provides the production baseline for typography, spacing, materials, navigation, cards, buttons, forms, focus treatment, responsive behavior, reduced-motion and reduced-transparency preferences, forced-colors support, minimum interaction targets, mobile safe areas, and print resilience.

Site-specific CSS may extend that layer while preserving Glaze UI hierarchy and accessibility contracts. Importing tokens alone is not considered conformance.

## Content and repository authority

`docs/repository-portfolio.json` is the machine-readable authority for the reviewed GoreeCloud GitHub portfolio shown on the public site. It is intentionally separate from runtime or production-readiness evidence.

`docs/public-runtime-status.json` records reviewed public maturity and migration claims. Repository visibility must never be treated as evidence of production acceptance.

Approved GoreeCloud logos, product icons, system marks, artwork, and derivatives come from `GoreeCloud/goreecloud-branding-assets`. New products without an approved canonical asset use a neutral presentation until an asset is approved; the website must not invent an “official” mark.

## Build

The main public site is built as an explicit allowlisted artifact:

```bash
python3 scripts/build_public_site.py
```

The build renders repository facts, normalizes the homepage, applies Glaze UI 2.0.0 Stable, and writes the isolated deployment artifact to `dist/`.

## Validation

Before a revision is accepted, run the repository validators and tests used by CI. They cover the static deployment allowlist, content rendering, repository inventory, public/private boundaries, privacy invariants, Glaze UI conformance, navigation behavior, accessibility fallbacks, security headers, branding provenance, and Cloudflare Pages artifact expectations.

Key sources include:

- `scripts/validate_repository_portfolio.py`
- `scripts/validate_public_sites.py`
- `scripts/validate_public_invariants.py`
- `scripts/validate_asset_provenance.py`
- `docs/glaze-ui-conformance.md`
- `docs/glaze-ui-2.0-public-sites.md`
- `docs/stability-baseline.md`

## Deployment

Cloudflare Pages deploys the reviewed static artifacts. Exact production revisions are recorded in the GoreeCloud Public Websites and Cloudflare Pages project specification in Google Drive. Deployment success does not by itself authorize broader product, privacy, security, continuity, identity, or production-readiness claims.

## Maintenance rules

When public behavior, architecture, project state, design-system conformance, branding authority, repository inventory, or deployment scope changes:

1. update the canonical source rather than adding a competing source of truth;
2. keep public claims evidence-scoped;
3. update the GoreeCloud project specification in `GoreeCloud/Projects`;
4. append the canonical website changelog in `GoreeCloud/Changelogs`;
5. verify Cloudflare Pages and GitHub status before treating the revision as accepted.

Do not restore references to the retired `goreecloud-logo` repository. The unified authority is `GoreeCloud/goreecloud-branding-assets`.
