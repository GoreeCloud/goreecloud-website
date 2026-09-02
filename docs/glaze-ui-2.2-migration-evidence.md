# GoreeCloud Website — Glaze UI 2.2 Migration Evidence

Status: **Implementation under review**

This record tracks the repository-local migration from Glaze UI 2.1.0 to 2.2.0. It is evidence bookkeeping, not a declaration of production acceptance.

## Canonical design-system authority

- Repository: `GoreeCloud/goreecloud-glaze-ui`
- Target: `2.2.0` Stable
- Stable release revision: `6731098b28dd0393faa878c70d989a221d714a20`
- Historical rollback baseline: `2.1.0` at `c49113eb8b93c267613fdf1bbca1f814495acad7`

## Consumer scope

The migration covers the GoreeCloud Website repository's independently deployed public surfaces:

1. Main
2. Projects
3. Roadmap
4. Blog
5. Archive

## Implemented migration controls

- Active HTML declarations target 2.2.0 directly rather than relying on a build-time version rewrite.
- Every deployment consumes a same-origin local 2.2.0 CSS layer.
- Main's isolated artifact allowlist publishes 2.2.0 and no longer publishes 2.1.0 as an active runtime asset.
- Durable reading/data surfaces use solid surfaces; Glaze is reserved for interaction/navigation/overlay semantics.
- Nested Glaze backdrop blur is disabled.
- The one-dominant-System-Panel composition budget is represented in the local consumer contract.
- 48px interaction and 56px Touch Assistance floors remain explicit.
- Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, and reduced-performance fallbacks remain explicit.
- Current public text identifies the seven Integral Platform Systems and preserves producer authority boundaries.
- Historical 1.x, 2.0, and 2.1 entries remain only where they are explicitly dated historical records or rollback context.

## Automated evidence required on the exact migration revision

The pull-request revision must pass, as applicable:

- Main source and artifact validation;
- Glaze UI 2.2 consumed-subset validation;
- accessibility structure validation;
- responsive-layout validation;
- privacy and browser-origin validation;
- security and Wardveil observability validation;
- Projects source validation and Chrome/Firefox desktop/mobile branch-preview checks;
- Roadmap validation;
- Blog validation and responsive browser checks;
- Archive validation and responsive browser checks;
- isolated artifact build and validation;
- branch-preview byte/deployment verification; and
- Main responsive browser smoke tests.

A green pull request proves only the evidence covered by those checks for the exact PR revision. It does not establish post-merge production deployment acceptance.

## Rendered acceptance profiles

Representative Glaze UI 2.2 web review profiles are:

- Mobile: 390×844
- Tablet: 820×1180
- Desktop: 1280×900
- Wide Desktop: 1600×1000

Acceptance also requires relevant keyboard, focus, 200% text/reflow, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, loading/empty/error/disabled/selected states, and focus-restoration behavior where those states or transient surfaces exist.

## Release boundary

Production Glaze UI 2.2 conformance must remain **unverified** until the merged exact revision is deployed and post-deployment validation succeeds for every required Website surface. Earlier 2.1 production acceptance is rollback/historical evidence, not 2.2 acceptance.

No GoreeCloud application, service, Platform System, security control, privacy control, or recovery state is upgraded by this UI migration alone.
