# GoreeCloud Website Stability Baseline

## Current release version

The repository-defined release version is **5.24.0**.

`VERSION` is the canonical machine-readable version source. The version file and this stability record are repository metadata only and are not part of the isolated Cloudflare Pages publication artifact.

Version metadata never establishes a Stable production release by itself. A revision must satisfy the source, artifact, preview, and production acceptance requirements below.

## Current reviewed baseline

Version 5.24.0 is the GoreeCloud public-web ecosystem modernization and current-state reconciliation release.

The reviewed baseline is:

- **Glaze UI 2.0.0 Stable** is the current production design target.
- Stable promotion reference: `ff3fff4306bd53ea9c0715a7c0d64265bb038617` in `GoreeCloud/goreecloud-glaze-ui`.
- **Glaze UI 2.1 remains Candidate** and does not establish Stable consumer conformance.
- The authenticated GoreeCloud owner inventory reviewed on **2026-08-29** contains **56 repositories: 40 public, 16 private, across 13 functional groups**.
- The official production public-web portfolio contains **10 active production destinations**: Main, Suite, Projects, Design Center, Privacy Center, Security Center, Continuity Center, Roadmap, Blog, and Archive.
- The six substantive GoreeCloud platform systems are **Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity**.
- GoreeCloud Identity is authoritative for identity, authentication, authorization, accounts, devices, credentials, sessions, and delegated authority.
- GoreeCloud Mesh coordinates explicit relationships, capabilities, lifecycle context, governance, events, and evidence exchange without taking over another platform system's authority.
- The current approved Glaze UI visual identity is **Facet**. Historical Fold references remain valid only when clearly presented as history.
- `GoreeCloud/goreecloud-branding-assets` is the current shared branding and approved visual-asset authority. The retired `goreecloud-logo` repository must not be restored as an authority.
- Products without approved canonical artwork remain text-only or use explicitly neutral non-official presentation rather than fabricated official icons or logos.

## Stability definition

A GoreeCloud website revision is considered stable only when all applicable conditions are satisfied:

1. The exact source revision passes the complete repository validation workflow.
2. Repository hygiene, history, license, governance, privacy, security-reporting, Wardveil Security, observability, and browser-origin checks pass.
3. Structural accessibility and the current Glaze UI design-contract checks pass.
4. Repository-portfolio validation confirms the reviewed total/public/private/group counts, directory completeness, public/private link boundaries, and local-only browser filtering behavior.
5. Current public-runtime-status validation confirms that accepted production services, release candidates, active development projects, migration states, and replacement boundaries are not reversed or overstated.
6. The explicit allowlisted `dist/` artifact builds and validates successfully.
7. Cloudflare deployment-contract and performance-budget checks pass.
8. JavaScript syntax, static fallback, reduced-effect, high-contrast, and failure-resilience checks pass where applicable.
9. Pull-request candidates pass **exact branch-preview deployment verification** before merge.
10. The resulting `main` revision passes **exact production deployment verification** after merge.

A passing branch preview alone is not a stable release. **A merge alone is not a stable release.** Stability requires the reviewed source, isolated artifact, and deployed production bytes to agree.

## Glaze UI 2.0 production boundary

Glaze UI is the substantive GoreeCloud design-system authority, not a decorative theme.

The production websites target Glaze UI 2.0.0 Stable and use the current material hierarchy:

**Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**

The public-web mapping includes, where applicable:

- current semantic typography, spacing, shape, surface, state, and focus behavior;
- 48px minimum general interaction targets;
- responsive mobile, tablet, and desktop layouts;
- mobile safe-area handling;
- Navigation Capsule behavior or an equivalent approved Glaze navigation mapping;
- reduced-motion and reduced-transparency behavior;
- increased-contrast and forced-colors fallbacks;
- keyboard-visible focus treatment;
- no-backdrop and print fallbacks;
- locally hosted production assets and explicit browser-origin boundaries.

Importing tokens or a stylesheet alone does not establish application conformance. Application-specific behavior, accessibility, representative viewport/device behavior, and deployment acceptance remain separate requirements.

Glaze UI 2.1 Candidate work may be developed and previewed in isolation but must not be presented as current Stable production conformance until formally promoted and separately adopted.

## Public website portfolio boundary

The ten active production destinations are maintained as focused sites rather than one monolithic page:

1. `www.goreecloud.com` — main GoreeCloud public website.
2. `suite.goreecloud.com` — GoreeCloud Suite application and service directory.
3. `projects.goreecloud.com` — current project portfolio.
4. `design.goreecloud.com` — Design Center / Glaze UI.
5. `privacy.goreecloud.com` — Privacy Center / Privacy Shield.
6. `security.goreecloud.com` — Security Center / Wardveil Security.
7. `everkeep.goreecloud.com` — Continuity Center / Everkeep.
8. `roadmap.goreecloud.com` — public development roadmap.
9. `blog.goreecloud.com` — public technical writing and development context.
10. `archive.goreecloud.com` — selected historical milestones and superseded directions.

Mesh Center and Identity Center remain substantive platform-system concepts. This baseline does not invent additional production domains for them where the canonical public-web project specification does not list one.

## Repository portfolio and privacy boundary

`docs/repository-portfolio.json` is the repository-only machine-readable authority for the reviewed source inventory. It is separate from runtime-readiness evidence.

The manifest records repository names, visibility, functional groups, and public-safe roles. Private repositories may be named where their product role is intentionally public, but the public website must not publish direct private-repository URLs or private contents.

The browser does not fetch this manifest or query GitHub at runtime. Repository cards and counts are source-controlled release facts rendered before publication. Browser search/filter controls operate only over already-rendered public HTML and remain local, ephemeral, and network-independent.

Repository visibility does not determine runtime maturity.

## Current public runtime-status boundary

The website continues to distinguish source development, release candidates, migration paths, accepted production services, and Stable application releases.

Representative reviewed boundaries include:

- **GoreeCloud Memos:** accepted Stable production at its recorded accepted version.
- **GoreeCloud Notify:** release-candidate work remains distinct from any still-active transitional production notification service until controlled cutover is accepted.
- **GoreeCloud Search:** public production claims remain limited to the accepted replacement scope recorded by its project evidence.
- **GoreeCloud Monitoring:** active-development/replacement language must not imply a cutover that has not been accepted.

A public repository, successful build, green CI run, release candidate, platform identity, or deployable source tree does not automatically establish production acceptance, security protection, privacy compliance, recoverability, design conformance, or native-rebuild completion.

## Branding and visual-asset boundary

Official GoreeCloud logos, product icons, system marks, illustrations, artwork, and other visual identities must trace to an approved first-party source.

The shared branding authority is `GoreeCloud/goreecloud-branding-assets`. Deployed sites may keep origin-local byte-identical or otherwise approved publication derivatives so browser delivery does not depend on a private repository at runtime.

The website must not create initials, generic graphics, or improvised artwork and then describe those as official. Neutral text presentation is acceptable when canonical artwork has not yet been approved.

Historical visual identities may remain in the Archive or other clearly historical context when needed to preserve the project's development record.

## Privacy, security, and observability boundary

The current public websites remain privacy-preserving static browser surfaces unless a specific site explicitly documents otherwise.

The main static-publication model does not add visitor analytics, advertising, behavioral tracking, fingerprinting, session replay, remote fonts, application-owned authentication, application storage, or a public application API merely as a consequence of this design refresh.

Wardveil Security, Privacy Shield, Everkeep, GoreeCloud Identity, and GoreeCloud Mesh names do not manufacture underlying security, privacy, continuity, identity, authorization, or coordination state. Public claims require the appropriate implemented behavior and authoritative evidence.

Future dynamic features must define their own authentication, authorization, observability, audit, sensitive-data handling, retention, recovery, monitoring, and security requirements before production acceptance.

## Governance and release boundaries

This website release does not itself authorize a:

- repository visibility change;
- DNS change;
- Cloudflare project-setting change outside the reviewed deployment contract;
- application production cutover;
- network migration;
- backup or recovery-platform cutover;
- security or privacy state upgrade;
- creative-rights/publication decision.

The **final human reachable-history/contextual-disclosure review** remains separate where publication or creative-rights review is required.

Current public claims must continue to match implementation, source authority, and accepted evidence. A design modernization must not be used to make unsupported application, platform, security, privacy, continuity, identity, deployment, or production-readiness claims appear authoritative.
