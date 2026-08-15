# goreecloud-website

Public static website for GoreeCloud.

## Version

Current website package: **v5.8 — production-readiness hardening in progress**

## Role

This repository contains the public-facing GoreeCloud website. It describes GoreeCloud's purpose, public software work, representative platform technologies, and long-term direction without publishing private infrastructure details.

The browser surface is intentionally dependency-light:

- static HTML
- locally hosted CSS
- locally hosted JavaScript
- locally hosted images and project artwork
- no browser analytics
- no advertising
- no third-party browser-loaded render resources
- no third-party fonts
- no third-party JavaScript frameworks
- no runtime browser network clients
- no service worker
- no Cloudflare Pages Functions or Worker runtime

Repository-only material such as CI validators, GitHub metadata, contributor documentation, development artifacts, publication-review records, and unapproved local files is kept separate from the generated public deployment artifact.

## Public site structure

- `index.html` — homepage and primary search/social metadata
- `privacy.html` — public website privacy statement
- `security.html` — public security-reporting policy
- `404.html` — custom noindex Cloudflare Pages not-found experience
- `.well-known/security.txt` — standardized public security-reporting contact
- `site.webmanifest` — browser application identity
- `robots.txt` — crawler instructions
- `sitemap.xml` — canonical public sitemap
- `_headers` — Cloudflare Pages security, privacy, and resource-hint headers
- `assets/` — source location for self-hosted GoreeCloud, service, platform, and social-preview artwork; only explicitly approved files are deployable
- `css/` — core, Glaze UI, responsive, section, accessibility, and error-page styles; only explicitly approved files are deployable
- `js/theme-init.js` — early appearance initialization
- `js/main.js` — appearance, navigation, and progressive interaction behavior

## Repository tooling

Production-readiness tooling is intentionally dependency-free and uses the Python standard library where practical.

- `scripts/build_public_site.py` — creates an exact, per-file allowlisted `dist/` deployment artifact
- `scripts/validate_build_artifact.py` — proves `dist/` contains exactly the reviewed public files and no repository-only content
- `scripts/validate_repository_hygiene.py` — rejects sensitive current-tree file types, private-key material, selected reusable credential signatures, symlinks, editor artifacts, and missing local-ignore protections
- `scripts/validate_repository_history.py` — inspects complete reachable Git history for prohibited secret-file paths, key material, selected reusable credential signatures, private-network addresses, and selected private-infrastructure identifiers without printing matched values
- `scripts/validate_performance_budget.py` — enforces static payload, request-count, and image-dimension budgets
- `scripts/validate_browser_origin_integrity.py` — keeps explicitly allowlisted browser-loaded HTML/CSS/manifest resources origin-local and rejects runtime network, cookie, worker, and service-worker clients in site JavaScript
- `scripts/validate_accessibility.py` — enforces structural accessibility invariants across the homepage, Privacy, Security, and custom 404 pages
- `scripts/validate_glaze_ui.py` — enforces the shared Glaze UI design, appearance, branding, responsive, accessibility, and progressive-enhancement contract across all human-facing pages
- `scripts/validate_public_surface.py` — validates cross-page links, fragments, canonical state, crawler policy, sitemap completeness, and sitemap dates
- `scripts/validate_deployment_contract.py` — enforces the static Cloudflare Pages architecture and header contract
- `scripts/validate_site.py` — validates the homepage and core public-site invariants
- `scripts/validate_resilience.py` — validates 404 behavior, failure paths, privacy boundaries, and response-header requirements
- `scripts/validate_app_identity.py` — validates browser/site identity metadata
- `scripts/validate_public_semantics.py` — validates public, canonical, Open Graph, X/Twitter, and semantic metadata guarantees
- `scripts/validate_privacy_policy.py` — keeps the privacy statement synchronized with implementation
- `scripts/validate_security_policy.py` — validates public security-reporting behavior and security.txt freshness
- `scripts/verify_remote_deployment.py` — verifies fixed GoreeCloud preview/production HTTP surfaces, repository isolation, live browser-security headers, live security.txt freshness, and preview/production indexing headers
- `tests/test_verify_remote_deployment.py` — exercises remote-verifier security/indexing/error/redirect behavior offline with synthetic responses and mocked network access
- `tests/test_public_asset_inventory.py` — keeps the deployable artwork allowlist synchronized with its pre-publication rights inventory
- `docs/public-asset-inventory.md` — repository-only inventory separating GoreeCloud identity artwork from third-party project/platform marks while provenance, attribution, trademark, and reuse terms remain under issue #5 review
- `scripts/validate_repository_guidance.py` — validates issue/PR safety guidance and maintenance documentation
- `scripts/validate_workflow_security.py` — enforces immutable GitHub Actions references, least privilege, full-history checkout, and retention of required production gates

Generated `dist/` output, local Python bytecode, local environment files, private-key/certificate-container file types, editor artifacts, and common operating-system metadata are ignored by Git. `.gitignore` is a convenience boundary rather than a security guarantee; CI independently validates repository hygiene so a force-added sensitive file type cannot silently become acceptable source.

## Cloudflare Pages deployment

The website is deployed through Cloudflare Pages using Git integration.

The intended production settings are:

- Production branch: `main`
- Framework preset: `None`
- Build command: `python scripts/build_public_site.py`
- Build output directory: `dist`
- Root directory: blank

`dist/` is the production boundary. The build script copies only files named in its explicit public-file allowlist. Adding a file to `assets/`, `css/`, `js/`, the repository root, or another source directory does **not** make that file deployable. A new public file must be deliberately added to the build allowlist and then pass the browser-origin, artifact, privacy, security, accessibility, Glaze UI, and other applicable validation gates.

CI compares every generated file byte-for-byte with its reviewed source and rejects missing files, unexpected files, duplicate allowlist paths, symlinks, non-regular source entries, or repository-only content. This fail-closed design prevents a future debug file, source map, screenshot, temporary artifact, or unrelated source file from becoming public merely because it was placed under a historically public directory.

For the existing Cloudflare Pages project, the dashboard build command and output-directory settings must be changed deliberately before relying on this boundary in production. That external cutover and its preview verification are tracked in **issue #6**. This repository does not introduce a Wrangler configuration file because the existing Pages configuration should be inspected before source control is made authoritative for it.

The documented live routing uses `https://www.goreecloud.com/` as the final public website address. The apex `https://goreecloud.com/` redirects permanently to the `www` hostname. Canonical, Open Graph, robots, and sitemap metadata therefore use the final `www` address.

Cloudflare Pages provides deployment-aware caching, ETags, compression, and static-asset delivery. The repository deliberately avoids broad long-lived browser cache rules for ordinary versionless HTML, CSS, and JavaScript so a release cannot leave clients stuck on stale code. `/.well-known/security.txt` retains a short explicit cache policy so corrections can propagate quickly.

## Production artifact

Build locally with:

```bash
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
```

The generated artifact must contain only the intentional public surface. Files such as `README.md`, `SECURITY.md`, `.github/`, `scripts/`, `tests/`, `docs/`, `.gitignore`, local environment files, private keys, development files, and unapproved artwork are repository or local concerns and must never be copied into `dist/`.

The source tree may contain material that is intentionally not deployed. The authoritative production decision is therefore the exact `PUBLIC_FILES` allowlist in `scripts/build_public_site.py`, not directory location alone.

The site currently uses no server-side application runtime, database, form handler, service worker, or Cloudflare Pages Function. Adding any of those changes the security and deployment model and requires an intentional revision of the deployment contract, privacy statement, threat boundary, public allowlist, and validators.

## Performance budget

The static site has explicit CI budgets to prevent accidental growth from turning a small public site into a heavy application. The current gates limit individual and aggregate HTML, CSS, JavaScript, SVG, raster-image, and total public-artifact size.

Public HTML images must declare intrinsic `width` and `height` so browsers can reserve layout space before image data arrives. Homepage stylesheet and script request counts are also bounded. These checks are regression ceilings rather than targets; smaller remains preferable where readability and maintainability are preserved.

## Glaze UI and accessibility

The website is the public implementation of **Glaze UI**, GoreeCloud's shared visual and interaction language. Glaze UI is treated as a design contract rather than a decorative stylesheet.

The current implementation includes:

- System, Light, and Dark appearance modes
- operating-system appearance detection
- local-only explicit-theme persistence through `localStorage`
- early self-hosted theme initialization to reduce appearance flash
- layered and selectively translucent surfaces rather than indiscriminate glass effects
- rounded geometry, soft depth, controlled gradients, and GoreeCloud design tokens
- visible keyboard focus states
- accessible mobile navigation with current open/closed labeling
- Escape-key focus restoration
- no-JavaScript primary-navigation fallback
- reduced-motion behavior
- reduced-transparency fallback
- `prefers-contrast: more` support
- forced-colors/high-contrast support
- print/readable-paper presentation
- responsive layouts and touch targets
- semantic footer navigation
- explicit image dimensions for layout stability
- consistent GoreeCloud branding and icon use on every human-facing page, including Privacy, Security, and 404 surfaces

The Glaze UI validator requires the homepage, Privacy page, Security page, and custom 404 to retain responsive viewport metadata, dark/light color-scheme metadata, the shared Glaze foundation and polish stylesheets, early appearance initialization, GoreeCloud brand identity, keyboard skip links, a programmatically focusable main landmark, and at least one shared Glaze surface or control. It also protects the common design tokens, light/system theme behavior, focus states, layered surfaces, responsive breakpoint, reduced-transparency and reduced-motion fallbacks, increased-contrast handling, forced-colors handling, print behavior, and System/Light/Dark interaction model.

The structural accessibility validator separately checks all four human-facing HTML pages for document language, a single main landmark and h1, skip-link targeting, heading-level progression, labeled navigation landmarks, accessible names for links and buttons, valid ARIA references, image alternatives, safe focus ordering, absence of autofocus, explicit button types, and safe new-tab relationships. It also requires keyboard focus styling and a visible skip-link focus state.

These automated checks are regression controls, not a claim of complete WCAG conformance. They do not replace manual keyboard review, screen-reader testing, browser zoom/reflow inspection, color-contrast measurement, touch-device review, visual Glaze UI review, or other real assistive-technology acceptance testing before a formal accessibility-conformance claim is made.

Glaze UI is intended to remain distinctly GoreeCloud rather than copying another vendor's interface. New public surfaces should reuse the shared design system before introducing page-specific patterns, and visual polish must never override privacy, readability, accessibility, performance, or clear interaction state.

## Privacy

The public site does not intentionally use analytics, behavioral tracking, advertising, fingerprinting, third-party telemetry, or third-party browser-loaded render resources. Stylesheets, scripts, images, manifest icons, and similar browser resources must remain origin-local so Cloudflare previews and the production hostname execute the same reviewed site without silently contacting another resource host.

Browser JavaScript is intentionally non-networked: CI rejects `fetch`, XMLHttpRequest, WebSocket, EventSource, `sendBeacon`, worker/service-worker clients, `importScripts`, and `document.cookie` access unless the privacy and deployment architecture is deliberately revised first.

When a visitor explicitly chooses Light or Dark mode, the preference is stored only in the visitor's browser using the `goreecloud-theme` `localStorage` key. Returning to System mode removes the stored override. The early theme initializer restores only an explicit stored Light/Dark choice; operating-system preference behavior remains owned by the shared CSS and normal interaction script instead of being duplicated across layers.

The response policy uses `Referrer-Policy: no-referrer`. The Content Security Policy denies browser capabilities the static site does not need, including form submission, arbitrary browser connections, media loading, workers, framing, and plugin/object content. The Permissions Policy additionally denies unnecessary device/browser capabilities.

Cloudflare remains the hosting/network-delivery layer, so repository validation does not pretend to control every behavior of the delivery provider. The enforced boundary is GoreeCloud's reviewed public artifact and browser code. The remote verifier checks the deployed response headers so repository configuration and the visitor-visible HTTP surface cannot silently diverge after the Cloudflare `dist/` cutover.

See `privacy.html` for the public statement that is validated against the implementation.

## Security and repository hygiene

Do not commit passwords, API keys, tokens, `.env` files, SSH private keys, private network addresses, private hostnames, internal access details, backup destinations, recovery credentials, or private family information.

The repository-hygiene validator provides a current-tree prevention layer. It rejects tracked/source symlinks; environment and secret-bearing configuration files; common private-key and certificate-container file types; SSH private-key filenames; editor/merge artifacts; selected operating-system metadata; private-key blocks; and several high-confidence reusable token/credential signatures.

The separate repository-history preflight requires a non-shallow checkout and scans every reachable historical blob path plus text-sized historical blob content. It checks for secret-bearing filenames, reusable credential/key signatures, private-network address patterns, and selected private-infrastructure identifiers. Findings intentionally disclose only the finding class, object ID, and historical path—not the matched value. Validator files that embed infrastructure identifiers solely to detect them are exempt only from those literal self-matches; reusable-credential scanning still applies to those detector sources.

A green automated history preflight is useful publication evidence, but it is not proof that every historical or contextual disclosure is appropriate. Issue #5 therefore still requires a final human repository-history/contextual review before any public visibility change. GoreeCloud's source-control policy treats an active credential committed to Git as compromised even if the repository is private or the value is later deleted; such a real finding would require rotation/revocation and an intentional history-remediation decision rather than merely updating the latest tree.

The deployable artwork rights boundary is also repository-controlled. `docs/public-asset-inventory.md` is not a license grant: it identifies GoreeCloud-branded presentation assets separately from third-party project/platform marks and keeps provenance, attribution, trademark, copyright, and reuse terms explicitly unresolved until issue #5 is completed. CI requires the inventory to stay synchronized with the exact public asset allowlist.

The public security-reporting path is:

- `https://www.goreecloud.com/security.html`
- `https://www.goreecloud.com/.well-known/security.txt`

`SECURITY.md` provides repository-side reporting guidance. Public security documents deliberately exclude private family infrastructure, credentials, internal networks, administrative interfaces, and non-public data from authorized testing.

The `security.txt` validator requires the reporting contact, canonical URL, policy URL, language metadata, and a single timezone-aware RFC3339 `Expires` value. CI intentionally begins failing once fewer than 30 days remain before expiration, providing a renewal window before the deployed metadata becomes stale. The remote production verifier enforces the same 30-day freshness boundary against the live file, so the scheduled production smoke check becomes an advance renewal alert as well as a reachability check.

The repository remains private while the source-license/publication decision tracked in issue #5 is unresolved. Passing CI does not itself authorize a visibility, DNS, or production release change.

## Search and crawler metadata

The homepage canonical URL, Open Graph metadata, X/Twitter card metadata, social-preview URL, title, and preview alt text are validated as one contract so social/search identity cannot drift across fields.

`robots.txt` must continue to allow the public site and publish exactly the canonical `https://www.goreecloud.com/sitemap.xml` location. The sitemap must contain exactly the intentional indexable public URLs, and every entry must carry one valid, non-future `lastmod` date. A `lastmod` value should be changed only when that page receives a significant content, structured-data, or link update rather than merely because a deployment occurred.

## Validation

Run the production checks from the repository root. The history check requires a complete reachable Git history rather than a shallow clone.

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

GitHub Actions runs the same production gates on pull requests and on pushes to `main`. External Actions are pinned to immutable full commit SHAs, workflow permissions remain read-only, persisted checkout credentials are disabled, superseded runs are cancelled, and the validation workflow does not consume repository or environment secrets. Validation checkout uses `fetch-depth: 0` because publication safety depends on inspecting reachable history, not merely the current commit.

The workflow self-validator requires the full-history checkout/preflight, current-tree repository-hygiene, Glaze UI, accessibility, privacy, security, browser-origin, public-surface, artifact, performance, offline regression-test, and remote-verifier configuration gates to remain wired into CI. Removing one of those checks therefore fails the workflow-supply-chain validation rather than silently weakening production readiness.

The checks cover, among other things:

- exact per-file production allowlisting rather than directory-wide publication
- repository sensitive-file/type hygiene and selected reusable credential signatures
- reachable Git-history preflight with redacted finding output
- deployable artwork inventory synchronization for publication-rights review
- offline regression testing of remote verifier security, indexing, redirect, 404, and repository-isolation behavior
- GoreeCloud Glaze UI design-system participation across all human-facing pages
- canonical, Open Graph, X/Twitter, manifest, and application identity
- sitemap completeness, canonical consistency, valid non-future `lastmod` dates, and canonical robots sitemap discovery
- local links, assets, same-page fragments, and cross-page fragments
- origin-local rendered resources across allowlisted HTML, CSS, and the web manifest
- no runtime browser network, cookie, worker, or service-worker clients in public JavaScript
- whole-site structural accessibility including skip links, landmark labeling, accessible interactive names, ARIA target integrity, heading progression, focus order, and image alternatives
- intrinsic image dimensions and static performance budgets
- HTTPS-only external navigation references
- safe new-tab link relationships
- CSP-compatible markup with no inline script/style/event-handler exceptions
- no-JavaScript navigation and footer fallbacks
- accessibility contrast, forced-colors, reduced-motion, reduced-transparency, and print behavior
- custom nested-path 404 resilience
- public privacy/security statement consistency
- standardized security-contact metadata with an advance expiry-renewal window
- private-network and selected internal-identifier leakage checks
- static Cloudflare Pages architecture and `_headers` limits
- fixed-target remote deployment verification
- branch previews must be excluded from indexing while production must remain indexable
- GitHub contribution safety boundaries
- immutable Action dependencies and least-privilege workflow configuration

## Remote deployment verification

Before treating the Cloudflare `dist/` cutover as verified, run:

```bash
python scripts/verify_remote_deployment.py --check-config
python scripts/verify_remote_deployment.py --target branch-preview
```

Branch-preview verification requires the deployment root to publish `X-Robots-Tag: noindex`. Production verification checks the opposite boundary: the canonical production root must not publish `noindex`, because a production-only indexing header can override otherwise-correct HTML and crawler metadata.

The remote verifier also checks that repository-only paths are not publicly reachable, required public resources have the expected status/content type/identity markers, the custom nested 404 is active, `security.txt` is current and correctly cached, and the reviewed browser-security header contract reaches the live deployment.

After an authorized production release, the default-branch deployment workflow can verify production manually and also performs a scheduled production smoke check each day at 8:17 AM America/Chicago.

## Release boundary

PR validation and Cloudflare preview deployment are pre-release evidence, not authorization to publish. Before a production merge, GoreeCloud should confirm the final PR head, green CI, successful preview, the Cloudflare Pages `dist/` cutover tracked in issue #6, and the source-license/creative-rights/publication decision in issue #5—including the final human history/contextual disclosure review—while treating any DNS or visibility change as a separate explicit action.

A production-ready repository state also does not by itself establish a formal accessibility-conformance claim or complete the external Cloudflare configuration. Those require their own evidence and deliberate release decisions.