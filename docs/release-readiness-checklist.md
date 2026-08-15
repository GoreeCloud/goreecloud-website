# GoreeCloud Website Release Readiness Checklist

## Purpose

This repository-only checklist defines the minimum evidence required before the GoreeCloud public website is treated as ready for an authorized production release.

It complements automated CI. It does **not** replace the project-specific licensing/publication decision in issue #5, the external Cloudflare `dist/` cutover in issue #6, or human Glaze UI/accessibility acceptance.

Passing every automated check is necessary production evidence, but **passing CI does not itself authorize a merge, repository visibility change, DNS change, Cloudflare configuration change, or production release**.

## Recording convention

When recording manual evidence, use Central Time (`America/Chicago`) and the 12-hour time format. Record the exact Git commit SHA being reviewed so evidence cannot be silently carried forward to a different release candidate.

Recommended evidence header:

- Review date and time:
- Exact candidate commit:
- Pull request:
- Reviewer:
- Desktop browser/OS:
- Mobile browser/device:
- Assistive technology used, if applicable:
- Cloudflare preview URL reviewed:

## 1. Candidate freeze

Before final acceptance:

- [ ] Identify the exact intended release-candidate commit SHA.
- [ ] Confirm PR #3 (or its successor release PR) targets `main` and is not merged accidentally.
- [ ] Confirm there are no unintended unreviewed commits after the selected candidate.
- [ ] Confirm the public artifact still comes only from `PUBLIC_FILES` in `scripts/build_public_site.py`.
- [ ] Confirm repository-only `docs/`, `tests/`, `scripts/`, `.github/`, `README.md`, `SECURITY.md`, and local/development material remain outside `dist/`.

If the candidate SHA changes after manual acceptance begins, rerun the checks affected by the change and record the new exact SHA.

## 2. Automated production gates

Run from the repository root on the exact candidate:

```bash
python scripts/validate_workflow_security.py
python scripts/validate_repository_hygiene.py
python scripts/validate_repository_history.py
python scripts/validate_security_policy.py
python scripts/validate_privacy_policy.py
python scripts/validate_browser_origin_integrity.py
python scripts/validate_accessibility.py
python scripts/validate_glaze_ui.py
python scripts/validate_app_identity.py
python scripts/validate_public_semantics.py
python scripts/validate_public_surface.py
python scripts/validate_deployment_contract.py
python scripts/validate_performance_budget.py
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
python scripts/verify_remote_deployment.py --check-config
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate_repository_guidance.py
python scripts/validate_site.py
python scripts/validate_resilience.py
node --check js/theme-init.js
node --check js/main.js
```

Required evidence:

- [ ] GitHub Actions is green on the exact candidate SHA.
- [ ] Current-tree repository hygiene passes.
- [ ] Full reachable-history automated preflight passes from a non-shallow checkout.
- [ ] Every deployable public asset path is present in the rights/provenance inventory.
- [ ] Every deployable public asset byte sequence matches its reviewed Git blob ID in the inventory.
- [ ] The isolated `dist/` artifact contains exactly the expected allowlisted files.
- [ ] Performance budgets pass without waiver.
- [ ] Remote-verifier configuration and dependency-free regression tests pass.

Automated history and rights checks are prevention/evidence controls, not substitutes for the human publication review required by issue #5.

## 3. Glaze UI visual and interaction acceptance

Review the homepage, Privacy page, Security page, and custom 404 experience. Glaze UI must remain recognizably GoreeCloud while preserving readability, accessibility, privacy, and performance.

### Appearance modes

- [ ] System mode follows the operating-system light/dark preference.
- [ ] Light mode is visually complete and has no dark-only surfaces or unreadable tokens.
- [ ] Dark mode is visually complete and has no light-only surfaces or unreadable tokens.
- [ ] Explicit Light/Dark preference persists locally between reloads.
- [ ] Returning to System removes the explicit override and restores system-controlled behavior.
- [ ] Early theme initialization does not produce an obvious incorrect-theme flash.

### Glaze surfaces and hierarchy

- [ ] Layered surfaces, translucency, borders, shadows, radii, gradients, and spacing follow the shared Glaze UI language.
- [ ] Translucency is selective rather than applied indiscriminately.
- [ ] Primary headings, body text, metadata, cards, actions, and navigation retain clear hierarchy.
- [ ] GoreeCloud branding is consistent across all human-facing pages.
- [ ] Third-party platform/service marks remain supporting content and are not visually presented as GoreeCloud-owned brands.

### Responsive behavior

- [ ] Desktop layout is stable at common wide viewport sizes.
- [ ] Tablet/narrow desktop layouts retain clear hierarchy without horizontal scrolling.
- [ ] Mobile layout remains usable at approximately 320 CSS pixels wide.
- [ ] Navigation opens/closes correctly and does not trap content behind an overlay.
- [ ] Interactive controls have practical touch targets and spacing.
- [ ] Images retain correct proportions and do not cause layout shifts from missing intrinsic dimensions.

## 4. Accessibility acceptance

Automated structural checks are not a formal WCAG conformance claim. Perform human acceptance on the exact candidate.

### Keyboard

- [ ] All meaningful interactive elements are reachable using only the keyboard.
- [ ] The skip link appears when focused and moves focus to the main content.
- [ ] Focus indication remains clearly visible on links, buttons, navigation controls, and theme controls.
- [ ] Focus order follows the visual/logical reading order.
- [ ] Mobile navigation can be opened, used, and closed with the keyboard.
- [ ] Escape closes the mobile navigation where expected and restores useful focus.
- [ ] No keyboard trap is present.

### Zoom and reflow

- [ ] Content remains usable at 200% browser zoom.
- [ ] Critical content and controls remain usable at 400% zoom/reflow where the browser supports it.
- [ ] Text is not clipped or hidden by fixed-height containers.
- [ ] Horizontal scrolling is not required for ordinary page content at narrow/reflowed widths.

### User preferences

- [ ] `prefers-reduced-motion` removes or substantially reduces nonessential motion.
- [ ] Reduced-transparency behavior preserves legibility without relying on glass effects.
- [ ] Increased-contrast mode remains readable.
- [ ] Forced-colors/high-contrast mode preserves meaningful controls, boundaries, and focus.

### Screen reader / semantic review

- [ ] Page title and primary heading accurately identify each page.
- [ ] Main, navigation, and footer landmarks are understandable.
- [ ] Heading levels form a useful document outline.
- [ ] Links and controls have meaningful accessible names out of context.
- [ ] Decorative images do not create noise; informative images have appropriate alternatives.
- [ ] Theme and navigation controls announce useful state/name changes.
- [ ] Custom 404 content clearly communicates that the requested page was not found.

## 5. Progressive enhancement and resilience

- [ ] With JavaScript disabled, primary navigation remains available.
- [ ] With JavaScript disabled, the footer remains useful and the copyright year has a sensible fallback.
- [ ] Theme controls are not shown in a misleading nonfunctional state when JavaScript is unavailable.
- [ ] A nested unknown path shows the custom GoreeCloud 404 experience and returns HTTP 404 after the Cloudflare deployment boundary is verified.
- [ ] Print preview produces a readable document without decorative Glaze effects obscuring content.

## 6. Privacy and browser-origin review

- [ ] No analytics, advertising, fingerprinting, or third-party telemetry has been introduced.
- [ ] Browser-loaded render resources remain first-party/origin-local.
- [ ] Public JavaScript remains non-networked unless the architecture, privacy statement, threat boundary, and validators have been intentionally revised.
- [ ] Theme persistence remains local browser storage only.
- [ ] External links are user-selected destinations rather than hidden render/runtime dependencies.
- [ ] The privacy statement still accurately describes repository-controlled behavior and distinguishes Cloudflare's hosting/network layer.

## 7. Source publication and creative-rights gate — issue #5

Do not make the repository public or represent the source as open source until issue #5 is explicitly resolved.

Required before any repository visibility change:

- [ ] Exact source-code license selected deliberately for this repository.
- [ ] Approved top-level `LICENSE` uses authoritative license text.
- [ ] GoreeCloud written-content and branding/artwork reuse boundary is documented.
- [ ] Copyright holder/notice treatment is documented.
- [ ] Third-party artwork provenance, applicable logo/trademark terms, and required attribution/notices are reviewed.
- [ ] `docs/public-asset-inventory.md` reflects the exact deployable artwork paths and reviewed bytes.
- [ ] Final human repository-history and contextual disclosure review is complete.
- [ ] Repository visibility decision is explicitly recorded.

An upstream software license, an intermediary icon-library license, or a successful automated scan must not be treated as a blanket rights grant for third-party logos.

## 8. Cloudflare isolated-artifact gate — issue #6

The repository-side build is not enough. Cloudflare must actually publish the isolated `dist/` artifact.

Required Pages settings:

- Production branch: `main`
- Framework preset: `None`
- Build command: `python scripts/build_public_site.py`
- Build output directory: `dist`
- Root directory: blank

After those settings are deliberately applied and a new branch preview is built:

```bash
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
python scripts/verify_remote_deployment.py --target branch-preview
```

Acceptance:

- [ ] Fresh post-cutover branch preview deploys successfully.
- [ ] Branch-preview verifier exits successfully.
- [ ] Preview publishes `X-Robots-Tag: noindex`.
- [ ] Required security/privacy headers reach the deployed HTTP surface.
- [ ] Repository-only paths return 404.
- [ ] `security.txt` identity, cache policy, and expiry checks pass.
- [ ] Nested custom 404 behavior passes.

A preview produced before the `dist/` configuration change does not satisfy issue #6.

## 9. Release authorization

Only after sections 1–8 are satisfied or an explicitly documented exception has been approved:

- [ ] Confirm the final exact SHA again.
- [ ] Confirm final CI is green.
- [ ] Confirm final preview evidence corresponds to that exact SHA.
- [ ] Confirm issue #5 is resolved before any repository-publication action.
- [ ] Confirm issue #6 is resolved before treating `dist/` isolation as externally enforced.
- [ ] Obtain explicit authorization for merge/production release.
- [ ] Treat repository visibility, DNS, and production routing as separate explicit changes rather than implied consequences of a merge.

## 10. Post-release verification

After an authorized production release:

```bash
python scripts/verify_remote_deployment.py --target production
```

Confirm:

- [ ] Canonical production content is reachable at `https://www.goreecloud.com/`.
- [ ] Apex routing resolves permanently to the canonical `www` host as intended.
- [ ] Production does **not** publish `X-Robots-Tag: noindex`.
- [ ] Required public resources return expected status, MIME type, and identifying content.
- [ ] Repository-only paths remain unavailable.
- [ ] Security/privacy headers match the reviewed contract.
- [ ] `security.txt` remains valid and has more than the required freshness window remaining.
- [ ] Custom nested-path 404 behavior remains correct.
- [ ] Light, Dark, and System appearance modes still behave correctly on the production origin.

Record any production-only discrepancy as a release defect rather than normalizing it into the repository documentation.

## Release boundary

This checklist is intentionally fail-closed. An unchecked licensing/publication requirement, an unverified Cloudflare `dist/` boundary, a red automated production gate, or a material manual Glaze UI/accessibility defect means the release candidate is not yet fully accepted.

The checklist itself is repository-only documentation and must never be copied into the public `dist/` artifact.
