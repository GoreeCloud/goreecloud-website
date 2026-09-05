# GoreeCloud Website — GLAZE UI V1.1 Source Alignment

## Current target

- Current applicable GoreeCloud Stable consumer target: **GLAZE UI V1.1 / 1.1.0**
- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`
- Exact Stable promotion revision used by the build: `15cc76d2bcd4065552dc31c77145b63f34d9e7b2`
- Main website source state in this branch: **targets the V1.1 consumer contract**
- New five-product website source state in this branch: **targets the V1.1 consumer contract**
- Exact rendered consumer acceptance remains pending.
- Production acceptance remains pending for this source revision.
- Website Platform Contract status remains nonconformant.

## Known immutable Stable-source defect

The immutable GLAZE UI `1.1.0` Stable source graph contains one verified import-closure defect: `css/glaze-v1.components.css` imports nonexistent `./glaze-v1.candidate.css`.

The canonical upstream remediation is being developed as a separate GLAZE V1.1 patch Release Candidate. That Release Candidate is not Stable and is not consumer-eligible, so this Website branch does not import, copy, or claim authority from the candidate.

Until a corrected immutable Stable patch release is published, `scripts/glaze_v1.py` uses a fail-closed consumer-build workaround:

1. fetch the exact immutable `1.1.0` Stable promotion revision;
2. validate the expected Stable entrypoint and inherited V1.0 import graph;
3. require the known dangling import to occur exactly once in `glaze-v1.components.css`;
4. reject any other unpinned or changed import;
5. remove only that single verified dangling directive from the generated artifact copy;
6. insert an explicit workaround marker into that generated file;
7. validate the resulting import closure before the artifact can pass.

The generated bundle is therefore not asserted to be byte-identical to the immutable Stable source. This bounded workaround is **not GLAZE consumer-conformance evidence** and does not change upstream Stable authority.

## Publication model

Browsers load GLAZE UI only from the same origin as the website. Cloudflare Pages builds do not load a floating branch, tag, or remote stylesheet in the browser.

The current candidate artifact is derived from the exact pinned Stable revision with the single documented import-closure workaround above. A corrected immutable Stable patch release must be independently re-pinned and the Website must be revalidated before this workaround can be removed or current GLAZE conformance can be claimed.

## Website scope

This branch covers the rebuilt root GoreeCloud public website surfaces and the new `sites/labs` five-product public-center source.

The legacy satellite sites in `sites/projects`, `sites/roadmap`, `sites/blog`, and `sites/archive` remain separate migration and exact-revision acceptance scope. This record must not be used to claim those independently deployed sites have earned V1.1 consumer or production acceptance from this branch.

## Consumer use

The rebuilt source uses the V1.1 structural and appearance contract:

- `html[data-glaze-version="1.1"]`
- same-origin `glaze-v1.1.0.css`
- V1.1 workspace, system overlay, system panel, capsule, shell-control, focus, and state-layer roles
- Light, Dark, and System appearance behavior through the V1.1 appearance contract
- a 48-pixel minimum shell-control target
- responsive reflow, keyboard focus, reduced-motion behavior, reduced-transparency fallbacks, and forced-colors support

Site-specific CSS is limited to public-website composition and consumes GLAZE roles and tokens rather than defining an independent GoreeCloud design system.

## Authority boundary

GLAZE UI governs design and interaction only. A V1.1 source target or generated workaround does not grant Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, GoreeCloud Identity, or GoreeCloud Manager acceptance. It also does not prove deployment, recovery, production readiness, product maturity, or Website Platform Contract conformance.

## Acceptance boundary

Automated source and artifact checks are necessary regression evidence but are not the final production gate.

The exact Website candidate still requires applicable branch-preview verification and representative human visual/interaction review, including touch targets, safe areas, appearance modes, 200% text/reflow, keyboard behavior, reduced-motion/transparency behavior, and horizontal-overflow checks.

For the new five-product destination, Cloudflare Pages project creation, custom-domain binding, DNS/TLS, indexing enablement, and exact production verification remain separate gates.

After a corrected immutable Stable GLAZE patch is published, the Website must replace this workaround with an exact re-pin and new repository-specific evidence before GLAZE migration can be considered complete.
