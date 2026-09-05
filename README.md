# GoreeCloud Website

Canonical source for the GoreeCloud public website surfaces maintained in `GoreeCloud/goreecloud-website` and published through Cloudflare Pages.

## Current development state

This repository is in **Development**. The current rebuild branch replaces the main public website composition and adds a combined public product-center source for:

- GoreeCloud Home Security
- GoreeCloud Home
- GoreeCloud AI
- GoreeCloud Containers
- GoreeCloud Code

The five-product site does **not** create a new umbrella product. It uses the GoreeCloud master brand, preserves each product's canonical identity, and keeps implemented, Development, planned, and production states distinct.

The current applicable Stable design-system target is **GLAZE UI V1.1 / 1.1.0**. Website builds remain pinned to exact Stable promotion revision `15cc76d2bcd4065552dc31c77145b63f34d9e7b2` in `GoreeCloud/goreecloud-glaze-ui`.

That immutable `1.1.0` source has one known import-closure defect: `css/glaze-v1.components.css` imports nonexistent `./glaze-v1.candidate.css`. The Website build detects that exact defect and removes only that single dangling import from the generated same-origin artifact. Any other import-graph drift fails the build. This is a temporary, bounded consumer-build workaround; it does **not** make the Website GLAZE-conformant or change the upstream Stable release. A corrected GLAZE V1.1 patch is still a Release Candidate and is not consumed until a corrected immutable Stable release is published and independently re-pinned and validated.

## Main website

The main `www.goreecloud.com` source is the repository root. The rebuild removes the former **“Expanding the platform”** composition and the associated Home Assistant/Frigate-centered roadmap framing.

The new information architecture centers on:

- GoreeCloud ownership, privacy, portability, and recoverability;
- clear navigation to specialized official public destinations;
- evidence-scoped platform-system relationships;
- source and deployment truth instead of hard-coded repository-count snapshots;
- a publication-pending entry for the new five-product center until its Cloudflare Pages and domain state are actually verified.

The rebuilt root public surfaces are:

- `index.html`
- `repositories.html`
- `privacy.html`
- `security.html`
- `404.html`

## Five-product public center

Source root: `sites/labs/`

Proposed technical website namespace: `labs.goreecloud.com`.

That hostname is a proposed website namespace only. It is not represented as active DNS, an active Cloudflare Pages custom domain, or a production-accepted public destination until those states are verified.

Cloudflare Pages contract:

```text
Repository: GoreeCloud/goreecloud-website
Root directory: /
Build command: python sites/labs/build.py
Build output: sites/labs/dist
Production branch: main after review and merge
Proposed custom domain: labs.goreecloud.com
```

The site remains `noindex,nofollow` and its `robots.txt` disallows indexing until the Pages project, custom-domain binding, DNS/TLS, representative-mobile human review, and exact production acceptance are complete.

## Public runtime boundary

These are static public information sites. Cloudflare Pages does not become the runtime for private GoreeCloud applications or services. Home device control, camera processing, AI inference/runtime APIs, container execution, source-control provider operations, private APIs, and other application workloads remain on their own authorized GoreeCloud infrastructure.

The browser runtime is intentionally minimal:

- static HTML;
- same-origin CSS and JavaScript;
- approved GoreeCloud master-brand artwork;
- no advertising or behavioral analytics code;
- no third-party runtime JavaScript;
- no external runtime fonts;
- no remote GLAZE stylesheet dependency in the browser.

## GLAZE UI build boundary

`scripts/build_public_site.py` copies an explicit allowlist of reviewed source files into `dist/`. It does not silently rewrite the reviewed page composition.

`scripts/glaze_v1.py` fetches only the immutable GLAZE UI V1.1 Stable promotion revision. Before generating the public artifact it:

1. validates the Stable entrypoint and inherited import structure;
2. requires the known `glaze-v1.candidate.css` dangling import to occur exactly once in `glaze-v1.components.css`;
3. rejects any additional or changed unpinned import;
4. removes only that verified dangling directive from the generated copy;
5. marks the generated CSS with an explicit workaround comment;
6. validates the resulting same-origin import closure before publication.

This workaround is a candidate-build compatibility measure only. Exact Website consumer acceptance remains pending, and a corrected immutable Stable GLAZE release must replace the workaround before GLAZE conformance or production completion can be claimed.

Main-site build and artifact validation:

```bash
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
```

Five-product site build and validation:

```bash
python sites/labs/build.py
python sites/labs/validate.py
```

## Branding authority

Canonical visual-asset authority is `GoreeCloud/goreecloud-branding-assets`.

Approved canonical artwork is used when it exists. Products without an approved canonical product asset use text-led identity during Development rather than fabricated, emoji, generic, or upstream substitute marks. Missing required canonical artwork remains a production visual-acceptance blocker.

## Platform-system boundary

The repository evaluates GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, GLAZE UI, GoreeCloud Mesh, and GoreeCloud Identity according to `goreecloud.platform.yaml`.

A public presentation, version marker, security header, privacy-minded static implementation, or successful build does not independently establish producer-system acceptance. The Platform Contract remains intentionally nonconformant while required integrations and evidence are incomplete.

## Security and privacy

The public artifact is explicit and allowlisted. Repository-only files do not become deployable merely because they exist in the repository.

The website uses restrictive Cloudflare Pages headers for content security policy, browser permissions, framing, referrer handling, cross-origin behavior, HSTS, and content-type handling. Repository-local privacy and browser-security controls do not independently establish Privacy Shield or Wardveil Security acceptance.

## Validation and acceptance

CI is an evidence and regression mechanism, not automatic production authorization.

A material website redesign still requires, as applicable:

- exact-head repository validation;
- exact branch-preview deployment verification;
- representative mobile, tablet, and desktop visual/interaction review;
- keyboard and accessibility review;
- light/dark/system and accessibility fallback checks;
- Cloudflare Pages project and custom-domain verification for new destinations;
- DNS and TLS verification;
- exact post-merge production deployment verification.

The `sites/labs` source intentionally does not claim a remote production verifier before its Cloudflare Pages project and custom domain actually exist.

## Source license and creative-rights boundary

The website source code, repository automation, validation scripts, and technical repository documentation are licensed under the **Apache License 2.0**. The authoritative source-license identifier is **Apache-2.0**, and the top-level `LICENSE` contains the reviewed license text.

`NOTICE` records the separate creative-rights boundary. The source license does not grant unrestricted reuse of GoreeCloud trade names, logos, branding, editorial identity, or third-party marks.

Issue #5 remains open as the separate human-controlled reachable-history, contextual-disclosure, creative-rights, and repository-publication decision. Passing CI does not itself authorize a repository visibility change, publication decision, trademark use, or release.
