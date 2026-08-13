# goreecloud-website

Public static website for GoreeCloud.

## Version

Current website package: **v5.1 — Glaze UI interaction polish**

## Role

This repository contains the public-facing GoreeCloud website. It describes GoreeCloud's purpose, public software work, representative platform technologies, and long-term direction without publishing private infrastructure details.

The site is intentionally dependency-light:

- static HTML
- locally hosted CSS
- locally hosted JavaScript
- locally hosted images and project artwork
- no browser analytics
- no advertising
- no third-party fonts
- no third-party JavaScript frameworks

## Structure

- `index.html` — public single-page website and search/social metadata
- `css/style.css` — core responsive site styling
- `css/glaze.css` — Glaze UI design tokens, light/dark themes, layered surfaces, accessibility refinements, and compatibility overrides
- `css/glaze-polish.css` — progressive Glaze UI interaction polish for section-aware navigation and appearance controls
- `css/status.css` — Family Services product artwork mapping
- `css/how-it-works.css` — How GoreeCloud Works section
- `css/platform.css` — Platform Foundation section
- `css/roadmap.css` — roadmap section
- `css/development.css` — software project section
- `css/social.css` — social-follow layout
- `js/main.js` — appearance modes, active-section navigation, mobile navigation, and footer year
- `scripts/validate_site.py` — dependency-free repository validation
- `.github/workflows/validate.yml` — pull-request and main-branch validation
- `assets/goreecloud-icon.png` — GoreeCloud artwork
- `assets/services/` — locally hosted Family Services project logos
- `assets/platform/` — locally hosted platform technology logos
- `assets/social-preview.png` — Open Graph/social preview
- `robots.txt` — crawler instructions
- `sitemap.xml` — sitemap
- `_headers` — Cloudflare Pages security headers

## Deployment

The repository is deployed through Cloudflare Pages.

Recommended settings:

- Production branch: `main`
- Framework preset: `None`
- Build command: `exit 0`
- Build output directory: `/`
- Root directory: blank

The documented live routing uses `https://www.goreecloud.com/` as the final public website address. The apex `https://goreecloud.com/` redirects permanently to the `www` hostname. Canonical, Open Graph, robots, and sitemap metadata therefore use the final `www` address.

## Glaze UI

The website is the public implementation of **Glaze UI**, GoreeCloud's shared visual and interaction language.

The website implementation includes:

- shared design tokens
- System, Light, and Dark appearance modes
- operating-system appearance detection
- local-only explicit-theme persistence through `localStorage`
- a System mode that returns control to the operating-system preference
- layered and selectively translucent surfaces
- restrained depth and rounded geometry
- section-aware primary navigation with `aria-current` state
- visible keyboard focus states
- reduced-motion support
- reduced-transparency fallback
- responsive navigation and touch targets
- no external browser dependencies

The v5.1 interaction layer is loaded progressively from `css/glaze-polish.css` by the already self-hosted `js/main.js`. The baseline site remains usable when JavaScript is unavailable.

Glaze UI is intended to remain distinctly GoreeCloud rather than copying another vendor's interface.

## Privacy

The website does not intentionally use:

- analytics
- behavioral tracking
- advertising
- third-party telemetry
- fingerprinting
- third-party browser scripts

When a visitor explicitly chooses Light or Dark mode, that preference is stored only in the visitor's browser using `localStorage` and is not transmitted by the site. Returning to System mode removes the stored override.

## Security

This repository is public-website source only.

Do not commit:

- passwords
- API keys
- tokens
- `.env` files
- SSH private keys
- private IP addresses
- private hostnames
- internal NetBird details
- backup destinations or recovery credentials
- private family information
- internal infrastructure documentation

Cloudflare Pages response headers enforce a restrictive Content Security Policy and disable browser capabilities that the static site does not need.

## Validation

Run:

```bash
python scripts/validate_site.py
node --check js/main.js
```

The dependency-free validator checks, among other things:

- canonical and Open Graph URL consistency
- document language, title, description, and single-`h1` structure
- duplicate element IDs
- local asset references
- in-page fragment targets
- image `alt` attributes
- safe `target="_blank"` links
- absence of inline scripts, inline style blocks, and inline event handlers that conflict with the self-only CSP
- self-hosted browser code dependencies
- Glaze UI polish and three-mode appearance-control wiring
- simple CSS brace integrity
- common private-network address leakage
- selected private infrastructure identifiers
- robots/sitemap canonical consistency

GitHub Actions runs the same checks on pull requests and on pushes to `main`.

## v5.1 changes

- Expanded the appearance control from a two-state Light/Dark switch into a three-mode System → Light → Dark cycle.
- Returning to System mode removes the browser-stored theme override and resumes the operating-system preference.
- Added clearer accessible labels and a distinct System-mode control state.
- Added section-aware primary navigation that applies `aria-current="location"` as visitors move through the page.
- Added restrained Glaze UI active-navigation treatment for desktop and mobile layouts.
- Hardened mobile navigation so crossing into the desktop breakpoint closes any open mobile menu state.
- Throttled scroll-driven active-navigation updates with `requestAnimationFrame` and passive scroll handling.
- Expanded reduced-motion behavior so smooth scrolling and the new interaction transitions are removed when requested by the visitor.
- Strengthened the dependency-free validator with document-structure, duplicate-ID, image-alternative-text, CSP-compatible markup, Glaze interaction-wiring, and CSS-integrity checks.
- Kept all new browser resources self-hosted and retained the no-analytics/no-third-party-runtime posture.

## v5.0 changes

- Applied the first Glaze UI website foundation with system-aware light and dark themes.
- Added a persistent, accessible appearance switch without introducing external dependencies.
- Added Glaze UI layered surfaces, refined depth, updated focus behavior, improved mobile controls, and reduced-transparency handling.
- Replaced fragile position-based Family Services logo selectors with explicit `data-service` selectors.
- Replaced the obsolete Trilium Family Services card with GoreeCloud Notes and identified it as a release-candidate GoreeCloud-maintained Memos fork.
- Expanded public software coverage to Research Library, GoreeCloud Manager, GoreeCloud Notes, GoreeCloud Tasks, GoreeCloud Contacts, and GoreeCloud Bookmarks.
- Added a public Glaze UI design-system callout and an August 12, 2026 software/design milestone.
- Corrected canonical, Open Graph, robots, and sitemap identity to `https://www.goreecloud.com/`, matching the documented production redirect.
- Added dependency-free validation and GitHub Actions CI.
- Strengthened Cloudflare Pages security headers while preserving the site's self-contained browser model.
- Kept analytics, telemetry, third-party fonts, and third-party browser scripts absent by default.
