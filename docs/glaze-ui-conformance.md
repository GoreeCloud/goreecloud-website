# GoreeCloud Website — Glaze UI 2.0.0 Conformance

## Conformance record

- Target Glaze UI version: **2.0.0**
- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`
- Stable promotion reference used for this alignment: `ff3fff4306bd53ea9c0715a7c0d64265bb038617`
- Conformance state: **Source-aligned — Glaze UI 2.0.0 Stable web contract prepared across all independently deployed GoreeCloud website surfaces in this repository**
- Rendered/production acceptance: **Separate gate; preview and production evidence must pass before the deployment is used as proof of portfolio-wide rendered conformance.**

## Scope

This record covers the Main, Projects, Roadmap, Blog, and Archive public surfaces. Each deployment carries a same-origin Glaze UI 2.0.0 web layer so design-system availability does not depend on another GoreeCloud domain at runtime.

The Main deployment uses the isolated build pipeline to normalize all deployable HTML onto the current Stable contract. Projects, Roadmap, Blog, and Archive carry their own same-origin 2.0.0 asset because they are independently deployed Cloudflare Pages surfaces.

## Glaze UI 2.0 web contract

The current production target follows the 2.0 model: Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze. The public sites exercise the web-relevant material and interaction subset without claiming platform features they do not implement.

The migration adds Soft Glaze navigation/header treatment, Glaze material surfaces for cards and summaries, Navigation Capsule semantics, minimum 48px interaction targets, current focus behavior, connected press/hover transformation, adaptive appearance compatibility, and controlled material transparency.

## Accessibility and resilience

Reduced-motion behavior removes nonessential transformation and transition. Reduced-transparency preferences receive solid material fallbacks. Focus-visible treatment remains explicit. Increased-contrast and forced-colors modes preserve borders and meaning. Browsers without backdrop-filter support receive opaque material surfaces.

## Privacy boundary

The design-system layer is served same-origin. It adds no analytics, advertising, trackers, remote fonts, runtime UI framework, or cross-domain stylesheet dependency.

## Authority boundary

Glaze UI controls presentation and interaction only. Public presentation cannot upgrade application, Privacy Shield, Wardveil Security, Everkeep, Mesh, or GoreeCloud Identity implementation/evidence state.

## Release boundary

Glaze UI 2.0.0 is the current Stable production target. Glaze UI 1.x is historical and must not remain an active production dependency on these public surfaces.

## Exceptions

No production Glaze UI exception is recorded for these website surfaces.