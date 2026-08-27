# GoreeCloud Website — Glaze UI Conformance

## Conformance record

- Target Glaze UI version: **1.5.0**
- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`
- Canonical reference revision reviewed for this alignment: `e8f68770540d00499b5613a00310ac7002a674fd`
- Alignment date: **2026-08-27**
- Conformance state: **Current-Stable migration implemented — semantic, material, layout, state, accessibility, and structural regression gates are enforced**
- Visual acceptance: **Pending user review** — the migration intentionally changes the public composition and must not be described as visually approved until the revised branch preview is reviewed.
- Verified branch preview: `https://agent-glaze-1-5-revamp-0827.goreecloud-website.pages.dev`
- Verified candidate revision: `cd75aa2f624f555c1e17f7fcfc604eda20220b5b`
- Verification workflow: `Validate public website` run **#503**

## Purpose

This record documents how the GoreeCloud public website targets the current Stable Glaze UI 1.5 design-system contract. It is repository metadata only and must remain outside the isolated Cloudflare `dist/` artifact.

The website retains its GoreeCloud product identity while consuming the shared Glaze UI material, layout, motion, state, adaptive-color, accessibility, and form-factor principles. Glaze UI is the governing interface architecture, not a decorative theme.

## Glaze UI 1.5 adoption

Glaze UI 1.5 is the current Stable baseline. The website migration applies the 1.5 contracts that are relevant to this static public web surface:

- adaptive layout gutters and content measures;
- selective material hierarchy and depth roles;
- functional glass only where bounded translucency improves navigation context;
- Solid/Raised ordinary content surfaces;
- shared hover, pressed, focus, selected, and semantic-state roles;
- current motion duration and easing vocabulary;
- safe-area-aware persistent chrome;
- reduced-motion, reduced-transparency, increased-contrast, forced-colors, print, and no-JavaScript resilience;
- local/system typography and local controlled artwork;
- responsive Desktop, Tablet, and Mobile web behavior within the Stable supported scope.

The website does not contain authenticated editing, destructive actions, modal workflows, or user-data forms. Those interaction states are not active consumers on this anonymous static surface.

## Material hierarchy

The website follows the current Stable hierarchy: **Canvas → Solid → Raised → Functional Glass → Overlay**.

1. Canvas — atmospheric page background and restrained GoreeCloud color fields.
2. Solid — readability-first content surfaces.
3. Raised — cards and grouped content that need hierarchy or separation.
4. Functional Glass — bounded persistent navigation where background context is useful.
5. Overlay — reserved for attention-priority layers; no ordinary homepage content uses Overlay by default.

Clear Glass is not used as a universal content treatment. Ordinary website cards explicitly disable backdrop blur and use Solid/Raised material treatment. The persistent navigation surface is the principal Functional Glass consumer and falls back to Solid when backdrop filtering is unavailable or reduced transparency is requested.

## Layout and density

The website maps the Glaze UI 1.5 layout system to these active roles:

- Compact gutter: 16 CSS pixels.
- Medium gutter: 24 CSS pixels.
- Expanded gutter: 32 CSS pixels.
- Wide gutter: 48 CSS pixels.
- Standard content measure: 1200 CSS pixels.
- Wide content measure: 1600 CSS pixels when a future surface explicitly needs it.
- Prose measure: 72ch.
- Form measure: 720 CSS pixels.
- Default density: comfortable.

The homepage uses semantic spacing rather than fixed card heights. Its story presentation is a chronological rail with flexible milestone surfaces so date labels, content height, and ongoing state remain aligned instead of being forced into an equal-height four-column card matrix.

## Adaptive layout and form-factor contract

The shared adaptive ranges remain:

- Compact: through 599 CSS pixels.
- Medium: 600 through 1023 CSS pixels.
- Expanded: 1024 through 1439 CSS pixels.
- Wide: 1440 CSS pixels and above.

The website may use additional content-specific breakpoints where readability or navigation ergonomics require them. Those component breakpoints do not redefine the shared Glaze UI form-factor or adaptive-range vocabulary.

Persistent site chrome accounts for `safe-area-inset-left` and `safe-area-inset-right`. The public website is pointer/keyboard capable on desktop and remains touch-capable and reflow-safe on smaller web surfaces.

## Motion and state contract

The website retains the Stable motion vocabulary:

- Instant: 90 ms.
- Fast: 160 ms.
- Standard: 220 ms.
- Emphasized: 320 ms.

Motion is restrained to state change, focus, navigation, and small elevation feedback. Reduced-motion mode disables nonessential transforms and smooth scrolling.

State-layer semantics are defined for hover, pressed, focus, and selected presentation. Semantic status colors remain evidence-bound to the underlying producer state; Glaze UI only presents supplied state and does not invent platform evidence.

## Homepage composition

The Glaze UI 1.5 homepage revamp establishes these product-specific decisions:

- one focused hero without platform-system identity-chip duplication;
- a Raised hero identity surface rather than universal glass;
- a compact ten-destination website directory without browser mockups or duplicated labels;
- restrained Raised cards with consistent corner, spacing, and motion roles;
- a true chronological GoreeCloud story rail with an explicit Ongoing state and Archive handoff;
- stronger section rhythm and semantic spacing across platform, repository, roadmap, about, social, and contact content;
- bounded Functional Glass navigation with Solid fallbacks.

These choices are website-specific compositions built from Glaze UI semantics; they are not new competing design-system primitives.

## Accessibility and resilience

The website retains:

- semantic page landmarks and keyboard skip links;
- visible focus indicators;
- practical 44–48 CSS-pixel target sizing;
- responsive and touch-aware navigation;
- safe-area-aware persistent chrome;
- reduced-motion behavior;
- reduced-transparency behavior;
- unsupported-backdrop-filter Solid fallbacks;
- increased-contrast handling;
- forced-colors handling;
- print/readable-paper behavior;
- no-JavaScript primary-content and navigation resilience;
- local/system typography and local artwork.

Automated checks are regression controls, not a formal WCAG-conformance claim. Material interface changes still warrant manual keyboard, assistive-technology, zoom/reflow, contrast, touch, and visual review.

## Privacy contract

Glaze UI 1.5 alignment introduces no analytics, advertising, trackers, fingerprinting, remote fonts, remote icon delivery, remote UI framework, runtime browser API client, service worker, or third-party rendering dependency. Explicit appearance preference remains local to the browser.

## Stable-release gate

`scripts/validate_glaze_ui.py` enforces this record together with the public page foundation. The validator binds the website to Glaze UI 1.5.0, the canonical `GoreeCloud/goreecloud-glaze-ui` repository, the reviewed reference revision, material/layout/state markers, adaptive ranges, motion semantics, accessibility/resilience fallbacks, privacy-preserving dependency boundaries, and GoreeCloud identity.

Passing automated validation and exact branch-preview verification do not substitute for visual acceptance. The candidate may be structurally current-Stable while visual acceptance remains pending explicit review. Production release classification also requires the post-merge exact production deployment verification defined by the website stability contract.

## Exceptions

No production Glaze UI exception is recorded for the current website implementation.
