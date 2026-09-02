# GoreeCloud Website — Glaze UI 2.2.0 Conformance

## Conformance record

- Target Glaze UI version: **2.2.0**
- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`
- Stable release revision used for this migration: `6731098b28dd0393faa878c70d989a221d714a20`
- Historical rollback baseline: **2.1.0** at `c49113eb8b93c267613fdf1bbca1f814495acad7`
- Migration classification: **2.1.0 → 2.2.0 additive semantic refinement with explicit consumer work**
- Conformance state: **Migration implementation in review; production eligibility remains false until repository-local source, rendered, accessibility, and deployment evidence is complete.**
- Rendered/production acceptance: **Separate mandatory gate. Preview and production evidence must pass on the exact migration revision before this record may be upgraded.**

## Scope

This record covers the Main, Projects, Roadmap, Blog, and Archive public surfaces. Each deployment uses a same-origin Glaze UI 2.2.0 consumed-subset layer so design-system availability does not depend on another GoreeCloud domain at runtime.

The Main deployment uses the isolated build pipeline. Projects, Roadmap, Blog, and Archive are independently deployed Cloudflare Pages surfaces and therefore require their own source-native 2.2.0 asset and exact-revision rendered/deployment acceptance.

## 2.2 System Shell and material mapping

The public Website does not claim to implement every Glaze UI 2.2 system component. It consumes the subset its public information surfaces require.

- Website document/canvas → **Workspace / Application reading surface**.
- Durable content cards, project records, status records, policies, timelines, repository data, and hero information → **solid Surface / raised Surface**.
- Persistent site navigation → **Soft Glaze interaction chrome**.
- Transient interactive overlays, if used → **System Overlay / Glaze**.
- A dominant transient panel, if introduced → **System Panel**, subject to the one-dominant-panel budget.
- Security/privacy/recovery-critical certainty surfaces, if introduced → **Critical System**, solid and evidence-backed.

The governing 2.2 material principle is **Solid where users read. Glazed where users interact.** Historical class names do not authorize a reading surface to remain translucent.

## System Glaze budget

Ordinary composition allows at most **one dominant Glaze panel** plus **one to three small floating Glaze controls**. Nested backdrop blur is prohibited. Universal Search and Control Center are not implemented by this public website and therefore are not claimed as consumed 2.2 components.

## Interaction, accessibility, and resilience

The consumed contract preserves:

- a **48px general interaction floor**;
- a **56px Touch Assistance floor**;
- visible keyboard focus;
- semantic disabled and error states;
- 200% text/reflow expectations;
- responsive phone, tablet, desktop, and wide-desktop composition;
- Reduced Motion behavior;
- Reduced Transparency with solid fallbacks;
- Increased Contrast;
- Forced Colors;
- large-text compact-density protection;
- effects-free/reduced-performance fallbacks;
- same task semantics when optical effects are removed; and
- safe-area-aware compact layouts.

Rendered acceptance must exercise at least the Glaze reference profiles 390×844, 820×1180, 1280×900, and 1600×1000, plus keyboard navigation, 200% text, reduced-motion, reduced-transparency, increased-contrast/forced-colors behavior, and important loading/empty/error/focus states that exist on the site.

## Privacy and supply-chain boundary

The design-system layer is served same-origin. It adds no analytics, advertising, trackers, remote fonts, remote icons, CDN UI dependencies, browser-storage requirement, or cross-domain stylesheet dependency.

The production bundle is repository-local and tied to the exact Glaze UI 2.2.0 Stable release revision recorded above. Candidate-named Glaze UI files are not production aliases.

## Authority boundary

Glaze UI controls presentation and interaction only. A visual badge, shield, privacy label, backup indicator, account affordance, Manager card, or Mesh relationship must never manufacture underlying platform state.

GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, GoreeCloud Mesh, and GoreeCloud Identity retain their distinct authority boundaries. Public presentation cannot upgrade an application or Platform System from unverified to implemented, accepted, conformant, recoverable, secure, private, authenticated, authorized, connected, or Stable.

## Source / generated / deployed agreement

Build-time normalization remains as a controlled compatibility and rendering boundary, but it is **not the sole conformance mechanism**. Active source templates are required to declare 2.2.0 directly; generated artifacts must carry the same 2.2.0 contract; deployed previews and production must match the validated artifact.

Glaze UI 2.1.0 may remain in repository history or explicitly labeled rollback material, but it must not be active in current deployable HTML or the public build allowlist after migration acceptance.

## Evidence and release boundary

Source validation and successful CI are necessary but not sufficient. Production eligibility remains false until exact-revision evidence exists for:

1. source-native 2.2.0 declarations across all deployable surfaces;
2. consumed-subset contract validation;
3. responsive rendered acceptance;
4. accessibility acceptance;
5. browser/runtime resilience acceptance;
6. exact branch-preview deployment verification; and
7. exact production deployment verification after merge.

No production Glaze UI exception is recorded for these Website surfaces. Missing mandatory evidence remains an explicit blocker rather than being inferred from prior 2.1 acceptance.
