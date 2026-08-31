# Glaze UI 2.1.0 public-site adoption

- Stable source target: **2.1.0**
- Canonical repository: `GoreeCloud/goreecloud-glaze-ui`
- Stable promotion reference: `c49113eb8b93c267613fdf1bbca1f814495acad7`
- Surfaces in this repository: Main, Projects, Roadmap, Blog, Archive
- Wider official portfolio: Main, Suite, Projects, Design Center, Privacy Center, Security Center, Continuity Center, Roadmap, Blog, Archive
- Delivery: same-origin CSS per independently deployed Cloudflare Pages surface
- Runtime third-party UI dependencies: none
- Acceptance state: **source migration candidate; rendered preview and production acceptance remain separate gates**

## Glaze UI 2.1 mapping

The public-web integration follows the current Stable rule: **Content is solid. Interaction is glazed.** Durable reading surfaces such as cards, repository summaries, policies, timelines, status content, project entries, and article content use solid Surface material. Navigation, selected interactive emphasis, transient controls, and deliberately live interaction surfaces may use controlled Glaze material.

The web layer retains the Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze hierarchy while adding the current 2.1 interaction and resilience contract: explicit clarity and density modes, 48px general target floors, a 56px Touch Assistance floor, large-text fallback behavior, deterministic material/performance fallbacks, focus-visible treatment, reduced-motion and reduced-transparency handling, increased-contrast support, forced-colors support, safe-area behavior, and non-backdrop fallbacks.

## Information architecture and branding

The migration preserves each site's purpose and content hierarchy. It does not collapse the five repository-owned public destinations into one page or make Design Center, Privacy Center, Security Center, Continuity Center, Mesh Center, or Identity Center interchangeable concepts.

Official logos, product icons, system marks, illustrations, and artwork continue to come from approved GoreeCloud authorities. Facet remains the current Glaze UI identity. Historical Fold material is valid only when clearly presented as history. Products without approved canonical artwork keep neutral presentation rather than receiving fabricated official marks.

## Authority and truth boundaries

Glaze UI controls presentation and interaction. It does not create or upgrade application maturity, Privacy Shield protection, Wardveil Security protection, Everkeep recoverability, GoreeCloud Mesh coordination state, GoreeCloud Identity state, deployment acceptance, or production readiness.

The Archive may retain dated 1.x and 2.0 statements where they accurately describe a historical state. Historical CSS may also remain in source control for rollback or compatibility evidence. Neither is an active public-site dependency once the 2.1 deployment is accepted.

## Acceptance boundary

Source conformance and rendered deployment acceptance are separate. A site is not used as proof of production-rendered Glaze UI 2.1 conformance until the exact reviewed revision passes its repository-local validators, Cloudflare Pages branch-preview verification where applicable, human visual/accessibility review, merge authorization, and exact post-merge production verification.

Glaze UI 2.0.0 remains the immediately preceding historical Stable baseline. Existing 2.0 consumer acceptance does not automatically transfer to 2.1.
