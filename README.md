# goreecloud-website

Public static website for GoreeCloud.com.

## Version

Current website package: **v4**

## Structure

- `index.html` — main public website
- `css/style.css` — responsive site styling and GoreeCloud brand identity
- `css/status.css` — current-service status hierarchy and availability emphasis
- `js/main.js` — mobile navigation and footer year
- `assets/logo.svg` — GoreeCloud brand mark
- `assets/social-preview.png` — Open Graph/social sharing preview image
- `robots.txt` — search crawler instructions
- `sitemap.xml` — basic sitemap
- `_headers` — Cloudflare Pages security headers

## Deployment

This repository is deployed through Cloudflare Pages.

Recommended Cloudflare Pages settings:

- Production branch: `main`
- Framework preset: `None`
- Build command: `exit 0`
- Build output directory: `/`
- Root directory: blank

Any commit pushed to `main` should trigger a new production deployment.

The preferred public and canonical hostname is `https://goreecloud.com/`. The `www` hostname should permanently redirect to the apex hostname at the Cloudflare zone level.

## Security

This repository is for public website content only.

Do not commit:

- passwords
- API keys
- tokens
- `.env` files
- SSH private keys
- private IP addresses
- internal hostnames that are not intentionally public
- NetBird configuration
- internal infrastructure documentation
- backup destinations or recovery credentials
- personal or family private information

## v4 changes

- Applied the GoreeCloud deep-navy, cobalt-blue, and cyan brand palette throughout the public website.
- Reworked the homepage visual hierarchy, hero presentation, cards, timeline, social section, contact section, and responsive behavior without introducing external browser dependencies.
- Reworked the SVG brand mark around cloud infrastructure, server blocks, and circuit-style networking.
- Standardized the preferred public identity and search metadata on the apex `https://goreecloud.com/` hostname.
- Added a concise "GoreeCloud today" service-status summary and moved available/in-development services ahead of planned services.
- Added visual emphasis for services that are available now or actively in development.
- Preserved public service descriptions, availability labels, social links, and the Cloudflare Pages security model.
- Added Escape-key handling to the mobile navigation so the menu can be closed from the keyboard and focus is returned to the menu button.
- Kept all page styling and scripting self-contained so the restrictive Content Security Policy remains compatible.

## v3 changes

- The site previously standardized canonical and social-preview URLs on the `www` hostname; v4 now uses the apex hostname as the preferred public identity.
- Added Cloudflare Pages `_headers` with a restrictive Content Security Policy and baseline browser security headers.
- HSTS is enabled for the host serving the Pages site without `includeSubDomains` or preload.

If Cloudflare Web Analytics, Turnstile, externally hosted fonts, or other third-party browser resources are added later, review and update the Content Security Policy before deployment.
