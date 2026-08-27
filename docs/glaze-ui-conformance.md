# GoreeCloud Website — Glaze UI 1.5.0 Conformance

## Conformance record

- Target Glaze UI version: **1.5.0**
- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`
- Canonical reference revision reviewed for this alignment: `2c5078410d022eba683c8e029bc3cafe773df0b7`
- Conformance state: **Aligned — Stable 1.5 web contract vendored across all independently deployed GoreeCloud website surfaces in this repository**

## Scope

This record covers the Main, Projects, Roadmap, Blog, and Archive public surfaces. Each deployment carries a same-origin copy of the Stable 1.5 web bundle so design-system availability does not depend on another GoreeCloud domain at runtime.

## Stable 1.5 web layers

The production bundle follows the Design Center order: core, controls, expressive components, form factors, accessibility, adaptive semantic color, motion, materials, layout/density, and interaction states. Candidate wearable and Glaze Motion promotion layers are excluded from this production adoption.

## Surface and interaction mapping

The sites use Glaze UI semantic canvas, Solid/Raised/Glaze/Overlay materials, adaptive color, 44px minimum targets, current focus semantics, restrained hover/press motion, current corner and spacing roles, and responsive Mobile/Tablet/Desktop/TV vocabulary while retaining each site's information architecture and product identity.

## Accessibility and resilience

Reduced-motion behavior removes nonessential animation and transitions. Focus-visible treatment remains explicit. Translucent header treatment has a solid fallback when backdrop filters are unavailable. Existing page-level no-JavaScript and theme behavior remains intact.

## Privacy boundary

The design-system bundle is vendored at build/source time and served same-origin. It adds no analytics, advertising, trackers, remote fonts, runtime UI framework, or cross-domain stylesheet dependency.

## Release boundary

Glaze UI 1.6 Candidate and wearable Candidate work are not production inputs. Public presentation cannot upgrade application, Privacy Shield, Wardveil Security, Everkeep, or Mesh evidence state.

## Exceptions

No production Glaze UI exception is recorded for these website surfaces.
