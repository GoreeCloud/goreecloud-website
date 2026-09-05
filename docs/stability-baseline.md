# GoreeCloud Website Stability Baseline

## Accepted production package versus current rebuild candidate

The repository-defined accepted website package remains **5.24.0** until a newer exact revision completes all applicable preview, human-review, merge, deployment, and production-verification gates.

`VERSION` remains the canonical machine-readable package-version source. It is repository-only metadata and is not copied into the isolated Cloudflare Pages artifact. A version value, branch, pull request, green workflow, or merge does not independently establish production acceptance.

The rebuild in the current development branch is **not an accepted replacement for 5.24.0**. It is a Development candidate and must remain distinguishable from the accepted production package until the required gates are complete.

## Current candidate design-system target

The current applicable GoreeCloud Stable consumer target for this Website candidate is **GLAZE UI V1.1 / 1.1.0**.

- Canonical design-system repository: `GoreeCloud/goreecloud-glaze-ui`.
- Exact Stable promotion revision: `15cc76d2bcd4065552dc31c77145b63f34d9e7b2`.
- Official Stable web entrypoint: `css/glaze-v1.1.0.css`.
- The immutable `1.1.0` source has one known import-closure defect: `glaze-v1.components.css` imports nonexistent `glaze-v1.candidate.css`.
- The Website build uses only the documented fail-closed workaround recorded in `docs/glaze-ui-conformance.md`: prove that exact pinned dependency is HTTP 404, require the dangling directive exactly once, remove only that directive from the generated artifact copy, mark the generated file, and validate the post-workaround import closure.
- The workaround is **not GLAZE consumer-conformance evidence**. Website GLAZE acceptance remains pending until a corrected immutable Stable patch is published, independently re-pinned, and accepted for the exact Website revision.

Earlier Glaze UI 2.x website-adoption records remain historical evidence only. They do not override the current applicable V1.1 target and must not be used to make the current rebuild appear conformant or accepted.

## Current reviewed repository inventory

`docs/repository-portfolio.json` is the repository-only machine-readable inventory authority for this Website candidate.

The authenticated GoreeCloud inventory reconciled on **2026-09-05** contains:

- **68 repositories total**;
- **65 public**;
- **3 private**;
- **15 functional groups**.

This inventory is source/discovery evidence, not runtime-readiness evidence. Repository visibility does not determine application maturity, deployment state, production acceptance, security protection, or platform conformance.

The rebuilt public `repositories.html` intentionally does **not** reproduce the full organization inventory or publish a numeric repository count. It is a focused Development source page for GoreeCloud Home Security, GoreeCloud Home, GoreeCloud AI, GoreeCloud Containers, and GoreeCloud Code. The full inventory remains repository-only authority.

## Integral Platform Systems

Current GoreeCloud governance requires evaluation of all seven Integral Platform Systems where applicable:

1. **GoreeCloud Manager** — management and operational visibility.
2. **Glaze UI** — design and interaction.
3. **Privacy Shield** — privacy and data use.
4. **Wardveil Security** — security and trust.
5. **Everkeep** — continuity and recovery.
6. **GoreeCloud Mesh** — coordination and capability exchange.
7. **GoreeCloud Identity** — identity and authentication.

Naming or displaying one of these systems does not manufacture its implementation or acceptance state. Each system remains authoritative only for the state it actually controls and evidences.

## Rebuilt Main public-surface boundary

The current candidate rebuilds the root GoreeCloud public site around owner-controlled computing, privacy, portability, recoverability, specialized official destinations, evidence-scoped platform relationships, and current Development truth.

The former **“Expanding the platform”** composition and Home Assistant/Frigate-centered roadmap framing are intentionally removed from Main.

The root public artifact is an explicit static allowlist containing the reviewed HTML, headers/crawler files, manifest, master GoreeCloud logo, local composition CSS/JavaScript, and the generated same-origin pinned GLAZE V1.1 CSS set. Repository-only records, scripts, tasks, release evidence, source-only artwork, and `sites/labs` source are not copied into Main's `dist/` artifact.

The browser boundary remains intentionally minimal: no advertising, behavioral analytics, third-party runtime JavaScript, remote fonts, browser API client, service worker, or application authentication is introduced by this rebuild.

## Five-product public-center boundary

`sites/labs/` is the combined public-information source for GoreeCloud Home Security, GoreeCloud Home, GoreeCloud AI, GoreeCloud Containers, and GoreeCloud Code. It does not create a new umbrella product identity.

`labs.goreecloud.com` is a **proposed technical website namespace**, not a verified active destination. The site remains `noindex,nofollow` with crawler blocking until its dedicated Cloudflare Pages project, custom-domain binding, DNS/TLS, representative-mobile human review, and exact production deployment are verified.

Source preparation is not Cloudflare project creation, DNS activation, production publication, or product-runtime acceptance.

## Specialized public-site boundary

Suite, Projects, Design, Privacy, Security, Continuity, Roadmap, Blog, Archive, Identity, and other separately deployed public surfaces retain their own revision, migration, and production-acceptance evidence.

This Main rebuild must not be used to inherit V1.1 acceptance for a separately deployed satellite site. Legacy satellite-site Glaze versions remain historical/current-to-that-site evidence until each consumer is explicitly migrated and accepted under its own applicable gates.

## Stability definition

A GoreeCloud Website revision is considered accepted/stable only when all applicable conditions are satisfied for the exact candidate and resulting production revision:

1. The exact source revision passes the complete repository validation workflow.
2. Repository hygiene, reachable-history, license, creative-asset, governance, privacy, security-reporting, Wardveil, observability, and browser-origin checks pass.
3. Structural accessibility and the applicable GLAZE source/design checks pass without converting a source target into a conformance claim.
4. Repository-portfolio and public-runtime-status checks preserve current source/status truth.
5. The explicit allowlisted `dist/` artifact builds and validates successfully, including the exact generated same-origin GLAZE file set.
6. Cloudflare deployment-contract, request-count/payload, resilience, JavaScript syntax, and remote-verifier tests pass.
7. The exact pull-request candidate passes branch-preview deployment verification.
8. Automated browser checks pass for representative desktop, tablet, and phone viewports without horizontal overflow, obscured content, or target-size regressions.
9. Required **representative human mobile visual/interaction review** is completed for the exact material redesign. Automated Chrome evidence does not replace this gate.
10. Required source-publication, creative-rights, and authorization decisions are resolved separately where applicable.
11. After merge, the exact resulting `main` revision passes production deployment verification and required production browser checks.

A passing branch preview alone is not a stable release. **A merge alone is not a stable release.** Stability requires reviewed source, artifact, human acceptance where required, authorization, and deployed production evidence to agree.

## Interaction and accessibility baseline

The candidate preserves, at minimum:

- 48px minimum shared navigation and shell-control targets;
- responsive mobile/tablet/desktop reflow;
- no horizontal page overflow at representative narrow widths;
- a skip link and programmatically focusable `main` target;
- keyboard-visible focus treatment;
- System, Light, and Dark appearance behavior;
- reduced-motion behavior;
- reduced-transparency fallbacks;
- forced-colors support;
- safe text/reflow behavior and required human review at representative mobile sizes.

These checks are regression evidence, not a formal WCAG conformance claim.

## Branding and creative-rights boundary

`GoreeCloud/goreecloud-branding-assets` remains the canonical shared visual-asset authority. Approved artwork is used when it exists. Products without approved canonical artwork remain text-led rather than receiving invented, emoji, generic, or upstream substitute marks.

Repository presence is not a license grant. Third-party marks and historical artwork remain subject to their own rights and publication context. The final human reachable-history/contextual-disclosure review remains separate where required.

## Governance and release boundaries

This Website candidate does not itself authorize a:

- repository visibility change;
- DNS change;
- Cloudflare project or custom-domain activation outside the reviewed deployment contract;
- application production cutover;
- security, privacy, identity, continuity, or platform-conformance upgrade;
- creative-rights/publication decision;
- merge or production release.

Current public claims must continue to match implementation, source authority, and accepted evidence. Unknown, pending, candidate, proposed, Development, and historical states must remain distinguishable from implemented and production-accepted state.
