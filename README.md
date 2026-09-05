# GoreeCloud Website

Canonical source for the GoreeCloud public website surfaces maintained in `GoreeCloud/goreecloud-website` and published through Cloudflare Pages.

## Current development direction

This branch rebuilds the main website from the ground up and adds a new combined public product-center source for:

- GoreeCloud Home Security
- GoreeCloud Home
- GoreeCloud AI
- GoreeCloud Containers
- GoreeCloud Code

The five-product website does **not** create a new umbrella product. It uses the GoreeCloud master brand, preserves each product's canonical name, and keeps implementation, Development, planned, and production states distinct.

The source target is **GLAZE UI V1.1 / 1.1.0**, the current Stable GoreeCloud consumer baseline. The exact Stable promotion revision consumed by builds is `15cc76d2bcd4065552dc31c77145b63f34d9e7b2` from `GoreeCloud/goreecloud-glaze-ui`. Exact Website consumer acceptance and production acceptance remain separate gates.

## Main website

The main `www.goreecloud.com` source is the repository root. The rebuild intentionally removes the former **“Expanding the platform”** roadmap composition and the associated Home Assistant/Frigate-centered public framing.

The new information architecture centers on:

- GoreeCloud ownership, privacy, portability, and recoverability principles;
- clear links into specialized official public sites;
- the six substantive platform systems relevant to product integration;
- source and evidence boundaries instead of hard-coded GitHub inventory counts;
- a publication-pending entry for the new five-product public center until its domain is actually active and verified.

## Five-product public center

Source root: `sites/labs/`

Proposed technical website namespace: `labs.goreecloud.com`.

That hostname is a proposed website namespace only. It is not represented as active DNS, an active Cloudflare Pages custom domain, or a new product identity until those states are verified.

Cloudflare Pages contract:

```text
Repository: GoreeCloud/goreecloud-website
Root directory: /
Build command: python sites/labs/build.py
Build output: sites/labs/dist
Production branch: main after review and merge
Proposed custom domain: labs.goreecloud.com
```

The site remains `noindex,nofollow` and its `robots.txt` disallows indexing until Pages activation, DNS/TLS verification, human mobile review, and production acceptance are complete.

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

The repository does not silently rewrite reviewed HTML into a different public composition. Instead, `scripts/build_public_site.py` copies an explicit allowlist of reviewed source files into `dist/`.

At build time, `scripts/glaze_v1.py` fetches the exact immutable GLAZE UI Stable promotion revision, validates its expected Stable markers and import closure, and writes those files to `dist/css/glaze-v1/` for same-origin publication.

```bash
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
```

The new five-product website follows the same model:

```bash
python sites/labs/build.py
python sites/labs/validate.py
```

## Branding authority

Canonical visual-asset authority is `GoreeCloud/goreecloud-branding-assets`.

The branding catalog currently has approved product artwork for some, but not all, of the five products in the new center. The center therefore uses text-led product identity instead of fabricating icons for products whose canonical artwork is not approved. The GoreeCloud master mark remains the site-level identity.

## Status and evidence

Public copy must remain tied to authoritative project specifications, current source, tests, and deployment evidence. A draft pull request, green CI run, successful build, brand treatment, or public page does not manufacture Stable or production-ready state.

The rebuilt product center follows this rule explicitly by separating **Implemented foundation** from **Still gated** for every product.

## Security and privacy

The public artifact is explicit and allowlisted. Repository-only files do not become deployable merely because they exist in the repository.

The site uses restrictive Cloudflare Pages headers for CSP, browser permissions, referrer handling, framing, cross-origin behavior, HSTS, and content-type handling. Privacy-minded source design does not itself establish Privacy Shield acceptance, and repository/browser security controls do not themselves establish Wardveil Security acceptance.

## Validation and acceptance

CI remains a regression and evidence mechanism, not automatic production authorization. A material website redesign still requires applicable exact-revision preview verification and human representative-mobile review before production completion can be claimed. After merge, production deployment must be independently verified against the accepted revision.

The new `sites/labs` source intentionally does not add a remote-production verifier before a Cloudflare Pages project and custom domain actually exist. Adding such a verifier before the service exists would create a false deployment assumption rather than useful evidence.

## Source license and creative-rights boundary

Repository source code and automation remain governed by the repository's Apache-2.0 source license and existing `NOTICE` boundary. GoreeCloud branding and third-party marks remain subject to their separate rights and authority records.
