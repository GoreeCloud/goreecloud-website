# GoreeCloud Website — Glaze UI Conformance

## Conformance record

- Target Glaze UI version: **1.0.0**
- Canonical design-system repository: `GoreeCloud/glaze-ui`
- Canonical reference revision reviewed for this alignment: `d6e446fd8ef251259d16368d50aad90d9287a774`
- Website package introducing this recorded alignment: **5.12.0**
- Conformance state: **Aligned — automated structural contract enforced; existing visual identity preserved**
- Visual acceptance: **Preserved** — this alignment intentionally retains the accepted GoreeCloud website composition and visual character while standardizing its underlying Glaze UI semantics.

## Purpose

This record documents how the GoreeCloud public website targets the active Glaze UI 1.0 design-system contract. It is repository metadata only and must remain outside the isolated Cloudflare `dist/` artifact.

The website is a reference implementation with its own public-site personality. Alignment therefore means using the shared Glaze UI semantics without replacing the website's established colors, content hierarchy, or recognizable composition with a generic reference-demo appearance.

## Semantic token alignment

`css/glaze.css` defines and consumes the shared Glaze UI semantic roles for:

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

Legacy website variables remain as compatibility aliases where existing section styles still consume them. New shared behavior should prefer the `--glaze-*` semantic roles.

## Surface hierarchy

The website recognizes the five Glaze UI surface levels:

1. Canvas — atmospheric page background and restrained GoreeCloud gradients.
2. Solid — readability-first opaque or near-opaque surfaces.
3. Raised — solid surfaces with restrained elevation.
4. Glaze — selectively translucent surfaces with blur and saturation.
5. Overlay — strongest separation for attention-priority layers.

The public website does not require every component to be translucent. Existing cards and navigation surfaces retain selective Glaze treatment, and all translucent surfaces retain readable solid fallbacks.

## Interaction and state contract

The website uses the shared Glaze UI target-size, focus, transition, and motion semantics for buttons, navigation controls, appearance controls, cards, chips, links, and status presentation. Relevant interactive controls preserve hover, pressed, focus-visible, current/selected, and disabled-safe behavior where applicable.

The website does not currently contain authenticated forms, dialogs, destructive actions, loading workflows, or user-data editing. Those component states remain not applicable to the current anonymous static-site architecture.

## Adaptive layout contract

The stylesheet exposes and validates the four Glaze UI adaptive ranges:

- Compact: through 599 CSS pixels.
- Medium: 600 through 1023 CSS pixels.
- Expanded: 1024 through 1439 CSS pixels.
- Wide: 1440 CSS pixels and above.

Product-specific responsive behavior may continue to use narrower component breakpoints when that improves readability or navigation ergonomics, but the Glaze UI adaptive ranges remain the shared layout vocabulary and conformance boundary.

## Motion contract

The website defines the Glaze UI 1.0 motion vocabulary:

- Instant: 90 ms.
- Fast: 160 ms.
- Standard: 220 ms.
- Emphasized: 320 ms.

Motion remains restrained and functional. Reduced-motion mode removes nonessential motion and disables smooth scrolling rather than merely speeding animation up.

## Accessibility and resilience

The website retains:

- semantic page landmarks and keyboard skip links;
- visible focus indicators;
- practical 44–48 pixel target sizing;
- responsive and touch-aware navigation;
- reduced-motion behavior;
- reduced-transparency behavior;
- unsupported-backdrop-filter solid fallbacks;
- increased-contrast handling;
- forced-colors handling;
- print/readable-paper behavior;
- no-JavaScript primary-content and navigation resilience;
- local/system typography and local artwork.

Automated checks remain regression controls rather than a formal WCAG-conformance claim. Manual keyboard, screen-reader, zoom/reflow, contrast, touch-device, and visual acceptance review remain appropriate for material interface changes.

## Privacy contract

Glaze UI alignment introduces no analytics, advertising, trackers, fingerprinting, remote fonts, remote icon delivery, remote UI framework, runtime browser API client, service worker, or third-party rendering dependency. Explicit theme preference remains local to the browser.

## Stable-release gate

`scripts/validate_glaze_ui.py` enforces this record together with the public page foundation. A stable website release must retain the target Glaze UI version, semantic tokens, surface hierarchy, standardized motion, adaptive ranges, accessibility/resilience fallbacks, privacy-preserving dependency model, and GoreeCloud identity.

Passing automated Glaze UI validation does not replace visual acceptance. For this 5.12.0 alignment, visual acceptance is carried forward because the public composition and product identity are intentionally preserved while the implementation contract is strengthened underneath it.

## Exceptions

No production Glaze UI exception is recorded for the current website package.
