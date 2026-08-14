# goreecloud-website

Public static website for GoreeCloud.

## Version

Current website package: **v5.5 — production-readiness hardening in progress**

## Role

This repository contains the public-facing GoreeCloud website. It describes GoreeCloud's purpose, public software work, representative platform technologies, and long-term direction without publishing private infrastructure details.

The browser surface is intentionally dependency-light:

- static HTML
- locally hosted CSS
- locally hosted JavaScript
- locally hosted images and project artwork
- no browser analytics
- no advertising
- no third-party fonts
- no third-party JavaScript frameworks
- no service worker
- no Cloudflare Pages Functions or Worker runtime

Repository-only material such as CI validators, GitHub metadata, and contributor documentation is kept separate from the generated public deployment artifact.

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
- `assets/` — self-hosted GoreeCloud, service, platform, and social-preview artwork
- `css/` — core, Glaze UI, responsive, section, accessibility, and error-page styles
- `js/theme-init.js` — early appearance initialization
- `js/main.js` — appearance, navigation, and progressive interaction behavior

## Repository tooling

Production-readiness tooling is intentionally dependency-free and uses the Python standard library where practical.

- `scripts/build_public_site.py` — creates an allowlisted `dist/` deployment artifact
- `scripts/validate_build_artifact.py` — proves `dist/` contains exactly the reviewed public files and no repository-only content
- `scripts/validate_performance_budget.py` — enforces static payload, request-count, and image-dimension budgets
- `scripts/validate_public_surface.py` — validates cross-page links, fragments, canonical state, and sitemap completeness
- `scripts/validate_deployment_contract.py` — enforces the static Cloudflare Pages architecture and header contract
- `scripts/validate_site.py` — validates the homepage and core public-site invariants
- `scripts/validate_resilience.py` — validates 404 behavior, failure paths, privacy boundaries, and response-header requirements
- `scripts/validate_app_identity.py` — validates browser/site identity metadata
- `scripts/validate_public_semantics.py` — validates public metadata and semantic guarantees
- `scripts/validate_privacy_policy.py` — keeps the privacy statement synchronized with implementation
- `scripts/validate_security_policy.py` — validates public security-reporting behavior
- `scripts/validate_repository_guidance.py` — validates issue/PR safety guidance
- `scripts/validate_workflow_security.py` — enforces immutable GitHub Actions references and least privilege

Generated `dist/` output and local Python bytecode are ignored by Git.

## Cloudflare Pages deployment

The website is deployed through Cloudflare Pages using Git integration.

The intended production settings are:

- Production branch: `main`
- Framework preset: `None`
- Build command: `python scripts/build_public_site.py`
- Build output directory: `dist`
- Root directory: blank

`dist/` is the production boundary. The build script copies only the explicitly allowlisted public pages, metadata, headers, JavaScript, CSS, and artwork into that directory. CI then compares every generated file byte-for-byte with its reviewed source and rejects missing files, unexpected files, symlinks, or repository-only content.

For an existing Cloudflare Pages project, the dashboard build command and output-directory settings must be changed deliberately before relying on this boundary in production. This repository does not introduce a Wrangler configuration file because Cloudflare recommends verifying or downloading the existing Pages configuration before making a Wrangler file the source of truth for an established project.

The documented live routing uses `https://www.goreecloud.com/` as the final public website address. The apex `https://goreecloud.com/` redirects permanently to the `www` hostname. Canonical, Open Graph, robots, and sitemap metadata therefore use the final `www` address.

Cloudflare Pages provides deployment-aware caching, ETags, compression, and static-asset delivery. The repository deliberately avoids broad long-lived browser cache rules for ordinary versionless HTML, CSS, and JavaScript so a release cannot leave clients stuck on stale code. `/.well-known/security.txt` retains a short explicit cache policy so corrections can propagate quickly.

## Production artifact

Build locally with:

```bash
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
```

The generated artifact must contain only the intentional public surface. Files such as `README.md`, `SECURITY.md`, `.github/`, `scripts/`, and `.gitignore` are repository concerns and must never be copied into `dist/`.

The site currently uses no server-side application runtime, database, form handler, service worker, or Cloudflare Pages Function. Adding any of those changes the security and deployment model and requires an intentional revision of the deployment contract and validators.

## Performance budget

The static site has explicit CI budgets to prevent accidental growth from turning a small public site into a heavy application. The current gates limit individual and aggregate HTML, CSS, JavaScript, SVG, raster-image, and total public-artifact size.

Public HTML images must declare intrinsic `width` and `height` so browsers can reserve layout space before image data arrives. Homepage stylesheet and script request counts are also bounded. These checks are regression ceilings rather than targets; smaller remains preferable where readability and maintainability are preserved.

## Glaze UI and accessibility

The website is the public implementation of **Glaze UI**, GoreeCloud's shared visual and interaction language.

The current implementation includes:

- System, Light, and Dark appearance modes
- operating-system appearance detection
- local-only explicit-theme persistence through `localStorage`
- early self-hosted theme initialization to reduce appearance flash
- layered and selectively translucent surfaces
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

Glaze UI is intended to remain distinctly GoreeCloud rather than copying another vendor's interface.

## Privacy

The public site does not intentionally use analytics, behavioral tracking, advertising, fingerprinting, third-party telemetry, third-party fonts, or third-party browser scripts.

When a visitor explicitly chooses Light or Dark mode, the preference is stored only in the visitor's browser using the `goreecloud-theme` `localStorage` key. Returning to System mode removes the stored override.

The response policy uses `Referrer-Policy: no-referrer`. The Content Security Policy denies browser capabilities the static site does not need, including form submission, arbitrary browser connections, media loading, workers, framing, and plugin/object content.

See `privacy.html` for the public statement that is validated against the implementation.

## Security

Do not commit passwords, API keys, tokens, `.env` files, SSH private keys, private network addresses, private hostnames, internal access details, backup destinations, recovery credentials, or private family information.

The public security-reporting path is:

- `https://www.goreecloud.com/security.html`
- `https://www.goreecloud.com/.well-known/security.txt`

`SECURITY.md` provides repository-side reporting guidance. Public security documents deliberately exclude private family infrastructure, credentials, internal networks, administrative interfaces, and non-public data from authorized testing.

The repository remains private while the source-license/publication decision tracked in issue #5 is unresolved. Passing CI does not itself authorize a visibility, DNS, or production release change.

## Validation

Run the production checks from the repository root:

```bash
python scripts/validate_workflow_security.py
python scripts/validate_security_policy.py
python scripts/validate_privacy_policy.py
python scripts/validate_app_identity.py
python scripts/validate_public_semantics.py
python scripts/validate_public_surface.py
python scripts/validate_deployment_contract.py
python scripts/validate_performance_budget.py
python scripts/build_public_site.py
python scripts/validate_build_artifact.py
python scripts/validate_repository_guidance.py
python scripts/validate_site.py
python scripts/validate_resilience.py
node --check js/theme-init.js
node --check js/main.js
```

GitHub Actions runs the same production gates on pull requests and on pushes to `main`. External Actions are pinned to immutable full commit SHAs, workflow permissions remain read-only, persisted checkout credentials are disabled, superseded runs are cancelled, and the validation workflow does not consume repository or environment secrets.

The checks cover, among other things:

- canonical, Open Graph, manifest, and application identity
- sitemap completeness and canonical consistency
- local links, assets, same-page fragments, and cross-page fragments
- document language, headings, duplicate IDs, and image alternatives
- intrinsic image dimensions and static performance budgets
- HTTPS-only external web references
- safe new-tab link relationships
- CSP-compatible markup with no inline script/style/event-handler exceptions
- no-JavaScript navigation and footer fallbacks
- accessibility contrast, forced-colors, reduced-motion, and print behavior
- custom nested-path 404 resilience
- public privacy/security statement consistency
- standardized and non-expired security-contact metadata
- private-network and selected internal-identifier leakage checks
- static Cloudflare Pages architecture and `_headers` limits
- isolated, allowlisted production-artifact generation
- GitHub contribution safety boundaries
- immutable Action dependencies and least-privilege workflow configuration

## Release boundary

PR validation and Cloudflare preview deployment are pre-release evidence, not authorization to publish. Before a production merge, GoreeCloud should confirm the final PR head, green CI, successful preview, intended Cloudflare Pages build settings, source-license/publication decision, and any DNS or visibility changes separately.
