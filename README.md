# goreecloud-website

Public static website for GoreeCloud.

## Version

Current website package: **v5.5 — Navigation accessibility and print resilience**

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
- `css/glaze-polish.css` — Glaze UI interaction states, progressive-enhancement fallbacks, increased-contrast/forced-colors support, and print presentation
- `css/status.css` — Family Services product artwork mapping
- `css/how-it-works.css` — How GoreeCloud Works section
- `css/platform.css` — Platform Foundation section
- `css/roadmap.css` — roadmap section
- `css/development.css` — software project section
- `css/social.css` — social-follow layout
- `js/theme-init.js` — early appearance initialization before stylesheet paint
- `js/main.js` — appearance modes, active-section navigation, accessible mobile-navigation state, and footer-year enhancement
- `scripts/validate_site.py` — dependency-free repository validation
- `.github/workflows/validate.yml` — pull-request and main-branch validation
- `.well-known/security.txt` — standardized public security-reporting contact and expiration metadata
- `assets/goreecloud-icon.png` — GoreeCloud artwork
- `assets/services/` — locally hosted Family Services project logos
- `assets/platform/` — locally hosted platform technology logos
- `assets/social-preview.png` — Open Graph/social preview
- `robots.txt` — crawler instructions
- `sitemap.xml` — sitemap
- `_headers` — Cloudflare Pages security and privacy headers

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
- an early self-hosted appearance initializer that applies explicit Light/Dark preferences before stylesheets paint
- a System mode that returns control to the operating-system preference
- browser theme-color synchronization with explicit appearance choices
- layered and selectively translucent surfaces
- restrained depth and rounded geometry
- section-aware primary navigation with `aria-current` state
- mobile navigation whose accessible control label reflects whether the menu is open or closed
- visible keyboard focus states
- reduced-motion support
- reduced-transparency fallback
- increased-contrast support through `prefers-contrast: more`
- forced-colors support for operating-system high-contrast modes
- print/readable-paper presentation that removes interactive chrome and translucent effects
- responsive navigation and touch targets
- a mobile navigation fallback that remains usable when JavaScript is unavailable
- no external browser dependencies

The Glaze UI polish layer is linked directly from `index.html` so visual behavior is not dependent on JavaScript loading. The appearance control remains hidden until the interaction script is active, while mobile primary navigation remains directly accessible when JavaScript is unavailable.

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

Cloudflare Pages sends `Referrer-Policy: no-referrer`, so GoreeCloud does not intentionally disclose the current GoreeCloud page URL through the browser's HTTP `Referer` header when a visitor follows an outbound link.

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

Cloudflare Pages response headers enforce a restrictive Content Security Policy, isolate the site into its own origin agent cluster where supported, and disable browser capabilities that the static site does not need.

The standardized public security-reporting contact is published at `https://www.goreecloud.com/.well-known/security.txt`. That file contains only public contact and metadata, is intentionally short-cached, and is validated so an expired or malformed security-contact record cannot be merged unnoticed.

## Validation

Run:

```bash
python scripts/validate_site.py
node --check js/theme-init.js
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
- explicit HTTPS for external web references
- absence of inline scripts, inline style blocks, and inline event handlers that conflict with the self-only CSP
- self-hosted browser code dependencies
- direct loading of the Glaze UI polish stylesheet
- early appearance initialization before stylesheet loading
- System/Light/Dark appearance-control wiring
- hidden-until-active appearance control behavior
- accessible open/closed mobile-navigation labeling
- no-JavaScript mobile-navigation fallback wiring
- no-JavaScript footer-year fallback
- increased-contrast, forced-colors, and print Glaze UI fallbacks
- current public Notes repository and Notify project markers
- rejection of the obsolete Memos-as-primary-Notes description
- public ownership-independence purpose marker
- standardized security-contact fields and expiration
- privacy/security header requirements, including no-referrer and origin-agent clustering
- simple CSS brace integrity
- common private-network address leakage
- selected private infrastructure identifiers
- robots/sitemap canonical consistency and sitemap modification metadata

GitHub Actions runs the repository validation and JavaScript syntax checks on pull requests and on pushes to `main`.

## v5.5 changes

- Improved the mobile navigation control so its accessible text changes between `Open navigation` and `Close navigation` as the menu state changes, while preserving `aria-expanded` and Escape-key focus restoration.
- Added a print/readable-paper Glaze UI mode that removes interactive chrome, decorative hero artwork, translucency, and shadows while preserving the site's core content and hierarchy.
- Added validator coverage for the dynamic mobile-navigation accessible label and print stylesheet.
- Added validation that rejects accidental `http://` and protocol-relative external web references so public outbound links remain explicitly HTTPS.
- Kept the site dependency-free, tracker-free, and compatible with the existing no-JavaScript navigation fallback.

## v5.4 changes

- Added explicit `prefers-contrast: more` Glaze UI behavior that strengthens borders, focus indication, muted-text contrast, and surface separation while removing translucency-dependent effects.
- Added a `forced-colors: active` fallback so cards, controls, state badges, and active navigation remain legible in operating-system high-contrast modes.
- Added `/.well-known/security.txt` with the public GoreeCloud security-reporting contact, canonical URL, preferred language, and an explicit expiration date.
- Added a short cache policy for the security-contact file so corrections can propagate promptly.
- Changed the site-wide referrer policy from `strict-origin-when-cross-origin` to `no-referrer` to better match GoreeCloud's privacy-first posture.
- Added `Origin-Agent-Cluster: ?1` as an additional browser isolation signal where supported.
- Expanded repository validation to enforce the accessibility media queries, security-contact metadata and expiration, privacy headers, origin-agent clustering, and security.txt cache policy.

## v5.3 changes

- Reconciled the public GoreeCloud Notes description with the native application direction and linked the authoritative public `GoreeCloud/goreecloud-notes` repository.
- Preserved the Memos release candidate in public wording as a transitional migration source rather than presenting the maintained fork as the long-term Notes product.
- Added GoreeCloud Notify to the public software portfolio while clearly preserving ntfy as the current notification service until controlled migration gates are complete.
- Expanded the software-development explanation to reflect GoreeCloud Ownership Independence: core applications move toward native GoreeCloud software or maintained forks when that adds durable control, without needlessly forking sustainable foundational dependencies.
- Added an explicit public-purpose statement explaining that GoreeCloud is not a commercial cloud product and is documented to demonstrate what individuals and families can own and operate for themselves.
- Added an August 14, 2026 timeline milestone for the expansion of native GoreeCloud software ownership.
- Strengthened validation so future edits cannot silently restore the obsolete Memos-primary Notes wording or omit the current Notes/Notify/public-purpose markers.
- Updated the sitemap modification date for this public-content refresh.

## v5.2 changes

- Moved the Glaze UI polish stylesheet from JavaScript injection to a direct `index.html` stylesheet link so visual polish does not depend on the interaction script.
- Added `js/theme-init.js`, a small self-hosted early initializer that restores explicit Light/Dark preference before CSS is painted, reducing appearance flash without adding inline script exceptions to the Content Security Policy.
- Synchronized browser theme-color metadata with explicit Light/Dark appearance choices while preserving operating-system-aware colors in System mode.
- Added a progressive mobile-navigation fallback: when JavaScript is unavailable, primary navigation remains visible rather than being trapped behind an inert menu button.
- Hid the appearance button until JavaScript is active so visitors never receive a nonfunctional theme control.
- Added a static `2026` footer-year fallback while preserving automatic year updates when JavaScript is available.
- Added `application-name`, Open Graph locale, and Twitter image-alt metadata.
- Added homepage `lastmod` metadata to the sitemap.
- Expanded repository validation to enforce the early-theme, direct-stylesheet, no-JavaScript navigation, footer fallback, and sitemap requirements.

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
