# GoreeCloud Website — GLAZE UI V1.1 Source Alignment

## Current target

- Current GoreeCloud Stable consumer target: **GLAZE UI V1.1 / 1.1.0**
- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`
- Exact Stable promotion revision used by the build: `15cc76d2bcd4065552dc31c77145b63f34d9e7b2`
- Main website source state in this branch: **migrated to the V1.1 consumer contract**
- New five-product website source state in this branch: **targets the V1.1 consumer contract**
- Exact rendered consumer acceptance remains pending.
- Production acceptance remains pending for this new source revision.

## Publication model

Browsers load GLAZE UI only from the same origin as the website. The Cloudflare Pages build fetches the exact immutable Stable promotion revision, validates the expected Stable entrypoint and import closure, and republishes those CSS files inside the isolated public artifact.

The browser does not follow `main`, a floating tag, or a remote stylesheet URL at runtime. A future GLAZE release therefore cannot silently change an already reviewed website candidate.

## Website scope

This branch migrates the root GoreeCloud public website surfaces and the new `sites/labs` five-product website source. The legacy satellite sites in `sites/projects`, `sites/roadmap`, `sites/blog`, and `sites/archive` remain separate migration and exact-revision acceptance scope. This record must not be used to claim those independently deployed sites have already earned V1.1 consumer or production acceptance.

## Consumer use

The rebuilt site uses the V1.1 structural and appearance contract directly:

- `html[data-glaze-version="1.1"]`
- same-origin `glaze-v1.1.0.css`
- V1.1 workspace, system overlay, system panel, capsule, shell-control, focus, and state-layer roles
- Light, Dark, and System appearance behavior through the V1.1 appearance contract
- a 48-pixel minimum shell-control target
- responsive reflow, keyboard focus, reduced-motion behavior, reduced-transparency fallbacks, and forced-colors support

Site-specific CSS is limited to public-website composition and consumes GLAZE roles/tokens rather than defining an independent design system.

## Authority boundary

GLAZE UI governs design and interaction. A V1.1 source target does not grant Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, GoreeCloud Identity, or GoreeCloud Manager acceptance. It also does not prove deployment, recovery, production readiness, or product maturity.

## Acceptance boundary

Automated source and artifact checks are necessary regression evidence but are not the final production gate. The exact candidate still requires applicable branch-preview verification and required human representative-mobile review, including touch targets, safe areas, appearance modes, 200% text/reflow, keyboard behavior, and horizontal-overflow checks. After merge, the exact production revision must be verified independently.
