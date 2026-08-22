# GoreeCloud Website — Glaze UI Conformance

## Conformance record

- Target Glaze UI version: **1.1.0**
- Canonical design-system repository: `GoreeCloud/glaze-ui`
- Canonical reference revision reviewed for this alignment: `5c8320de4f770614a3e2bcf9de2a27f7fcfd920c`
- Website package introducing this recorded alignment: **5.19.0**
- Conformance state: **Aligned — version-specific semantic mapping and automated structural contract enforced; existing visual identity preserved**
- Visual acceptance: **Preserved** — the 1.1 adoption is a compatible semantic expansion. It retains the accepted website composition and product character while adding version-specific semantics and safe-area behavior.

## Purpose

This record documents how the GoreeCloud public website targets the active Glaze UI 1.1 design-system contract. It is repository metadata only and must remain outside the isolated Cloudflare `dist/` artifact.

Glaze UI 1.4.0 is now the current canonical Stable design-system baseline, with Glaze UI 1.3.0 retained as a supported older Stable target. That platform promotion does not automatically migrate this website: the website remains intentionally pinned to its reviewed 1.1.0 consumer contract until a separate controlled application-level migration, validation, and visual-acceptance process is completed.

The website is a reference implementation with its own public-site personality. Alignment means using the shared Glaze UI semantics without replacing the website's established colors, content hierarchy, or recognizable composition with a generic reference-demo appearance.

## Glaze UI 1.1 adoption

Glaze UI 1.1 is a compatible expansion of the 1.0 foundation. The website adopts the applicable 1.1 additions while preserving the existing surface hierarchy, adaptive ranges, motion vocabulary, privacy boundary, accessibility fallbacks, and product personality.

The website-specific 1.1 mapping includes:

- `on-accent` for primary action text;
- `info` and semantic scrim roles for future information and overlay states;
- shared hover, pressed, focus, and selected state-layer opacity semantics;
- 16, 20, 24, and 32 CSS-pixel icon-size roles;
- compact and comfortable control-padding roles while preserving the 44 CSS-pixel minimum target;
- Compact, Medium, Expanded, and Wide gutter roles;
- safe-area inset handling for persistent site chrome;
- exact version and canonical-source revision evidence in this conformance record.

The current public website has no modal dialog or destructive workflow, so the semantic scrim role is defined for compatibility but has no active modal consumer. Loading, destructive, and authenticated form states remain not applicable to the current anonymous static-site architecture.

## Semantic token alignment

`css/glaze.css` continues to define and consume the shared Glaze UI semantic roles for:

- canvas and canvas accent;
- solid, raised, glaze, and overlay surfaces;
- primary and secondary accents;
- semantic success, warning, and danger colors;
- border/line treatment;
- text and muted text;
- spacing and corner radii;
- minimum and comfortable target sizes;
- blur and elevation shadows;
- focus width and offset;
- content and reading widths;
- Instant, Fast, Standard, and Emphasized motion durations;
- standard and emphasized easing.

`css/glaze-polish.css` supplies the compatible 1.1 semantic extension for on-accent, info, scrim, state-layer, icon-size, density, adaptive-gutter, and safe-area behavior while retaining the existing website palette. Legacy website variables remain compatibility aliases where existing section styles consume them. New shared behavior should prefer the `--glaze-*` semantic roles.

## Surface hierarchy

The website recognizes the five Glaze UI surface levels: **Canvas, Solid, Raised, Glaze, and Overlay**.

1. Canvas — atmospheric page background and restrained GoreeCloud gradients.
2. Solid — readability-first opaque or near-opaque surfaces.
3. Raised — solid surfaces with restrained elevation.
4. Glaze — selectively translucent surfaces with blur and saturation.
5. Overlay — strongest separation for attention-priority layers.

The public website does not require every component to be translucent. Existing cards and navigation surfaces retain selective Glaze treatment, and all translucent surfaces retain readable solid fallbacks.

## Interaction and state contract

The website uses the shared Glaze UI target-size, focus, transition, motion, and state semantics for buttons, navigation controls, appearance controls, cards, chips, links, and status presentation. Relevant interactive controls preserve hover, pressed, focus-visible, current/selected, and disabled-safe behavior where applicable.

Primary actions explicitly consume the 1.1 on-accent role. Existing product-specific navigation and control feedback remains a documented website mapping to the shared 1.1 state-layer semantics rather than being replaced by generic reference-component styling.

The website does not currently contain authenticated forms, dialogs, destructive actions, loading workflows, or user-data editing. Those component states remain not applicable to the current anonymous static-site architecture.

## Adaptive layout and safe-area contract

The stylesheet exposes and validates the four Glaze UI adaptive ranges:

- Compact: through 599 CSS pixels.
- Medium: 600 through 1023 CSS pixels.
- Expanded: 1024 through 1439 CSS pixels.
- Wide: 1440 CSS pixels and above.

Product-specific responsive behavior may continue to use narrower component breakpoints when that improves readability or navigation ergonomics, but the Glaze UI adaptive ranges remain the shared layout vocabulary and conformance boundary.

The 1.1 mapping also records Compact, Medium, Expanded, and Wide gutter roles. Persistent site chrome accounts for `safe-area-inset-left` and `safe-area-inset-right` so display cutouts do not require hard-coded device assumptions.

### Desktop composition refinement

The homepage now treats Expanded and Wide desktop ranges as purpose-built desktop compositions rather than merely centering the smaller-layout presentation inside a larger viewport.

At Expanded widths, the content canvas grows to a 1280 CSS-pixel maximum with 32-pixel semantic desktop gutters. The hero uses a wider two-column composition, its visual surface receives more physical presence, and section spacing increases so the layout uses the available desktop workspace without becoming edge-to-edge.

At Wide widths, the content canvas grows to a 1480 CSS-pixel maximum with 40-pixel semantic gutters. The hero typography and visual surface scale up without becoming full-width; service, development, and social collections use four balanced columns; and platform cards retain readable four-column density.

This desktop refinement does not remove Compact or Medium behavior and does not infer a TV interface from width. It is specifically a pointer/keyboard-friendly public website composition for representative 1280 × 900 and 1600 × 1000 desktop acceptance ranges. Manual visual acceptance should confirm that the wider composition improves density and hierarchy without creating overly long reading lines, clipped navigation, inaccessible focus order, or excessive card width.

### Rendered desktop preflight

`scripts/validate_desktop_rendering.py` adds a real-browser preflight on the exact deployed Cloudflare Pages candidate after byte-for-byte deployment verification succeeds. It uses the Chrome and ChromeDriver toolchain supplied by the explicitly pinned `ubuntu-24.04` GitHub Actions runner and does not add a runtime browser library, npm package, remote rendering service, analytics dependency, or public artifact file.

For both 1280 × 900 and 1600 × 1000, the preflight renders System, Light, and Dark appearance modes and checks the semantic desktop gutter/container relationship, hero minimum geometry, horizontal overflow, primary-navigation containment, image loading, and Wide four-column collection density. It also exercises reduced-motion and increased-contrast media fallbacks and requires each representative browser render to produce a valid nontrivial PNG screenshot payload. The screenshot bytes remain ephemeral CI evidence and are not published as public website assets.

The rendered preflight strengthens the candidate gate but does not replace human judgment. Manual visual acceptance remains required for hierarchy, aesthetic balance, reading comfort, keyboard-navigation feel, zoom/reflow behavior, and the subjective quality of System/Light/Dark presentation before the desktop refinement is treated as newly accepted production visual evidence.

## Motion contract

The website retains the Glaze UI motion vocabulary:

- Instant: 90 ms.
- Fast: 160 ms.
- Standard: 220 ms.
- Emphasized: 320 ms.

Motion remains restrained and functional. Reduced-motion mode removes nonessential motion and disables smooth scrolling rather than merely speeding animation up.

## Accessibility and resilience

The website retains:

- semantic page landmarks and keyboard skip links;
- visible focus indicators;
- practical 44–48 CSS-pixel target sizing;
- responsive and touch-aware navigation;
- safe-area-aware persistent chrome;
- reduced-motion behavior;
- reduced-transparency behavior;
- unsupported-backdrop-filter solid fallbacks;
- increased-contrast handling;
- forced-colors handling;
- print/readable-paper behavior;
- no-JavaScript primary-content and navigation resilience;
- local/system typography and local artwork.

Automated checks remain regression controls rather than a formal WCAG-conformance claim. Manual keyboard, screen-reader, zoom/reflow, contrast, touch-device, safe-area/device, and visual acceptance review remain appropriate for material interface changes.

## Privacy contract

Glaze UI alignment introduces no analytics, advertising, trackers, fingerprinting, remote fonts, remote icon delivery, remote UI framework, runtime browser API client, service worker, or third-party rendering dependency. Explicit theme preference remains local to the browser.

## Stable-release gate

`scripts/validate_glaze_ui.py` enforces this record together with the public page foundation. A stable website release must retain the exact target Glaze UI version and reference revision, applicable 1.1 semantic mapping, surface hierarchy, standardized motion, adaptive ranges, safe-area behavior, accessibility/resilience fallbacks, privacy-preserving dependency model, and GoreeCloud identity.

Passing automated Glaze UI validation does not replace visual acceptance. For this compatible 5.19.0 alignment, existing visual acceptance is carried forward because the ordinary-viewport public composition and product identity are intentionally preserved while the implementation contract is strengthened underneath it.

The desktop composition refinement is an additional candidate-level layout improvement and requires representative Expanded and Wide manual browser review before it should be described as newly accepted production visual evidence.

## Exceptions

No production Glaze UI exception is recorded for the current website package.
