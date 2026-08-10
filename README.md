# goreecloud-website

Public static website for GoreeCloud.com.

## Version

Current website package: **v4**

## Structure

- `index.html` — main public website
- `css/style.css` — responsive site styling and GoreeCloud brand identity
- `css/status.css` — locally hosted Family Services project logos/icons
- `css/how-it-works.css` — public How GoreeCloud Works section styling
- `css/platform.css` — public Platform Foundation section styling
- `css/social.css` — responsive layout overrides for the public Follow section
- `js/main.js` — mobile navigation and footer year
- `assets/goreecloud-icon.png` — official GoreeCloud artwork used in the header, hero, footer, and favicon
- `assets/services/` — locally hosted Family Services project logos/icons
- `assets/platform/` — locally hosted platform technology logos/icons for Proxmox, Debian, Docker, NetBird, AdGuard Home, Caddy, ntfy, Beszel, Uptime Kuma, and SearXNG
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

The source canonical, Open Graph, robots, and sitemap identity uses `https://goreecloud.com/` as the preferred public address. The previously configured external routing still redirects the apex domain to `https://www.goreecloud.com/`; a Cloudflare-side `www`-to-apex redirect was intentionally not added during the v4 work. Treat this as a known source-versus-routing inconsistency until the external redirect design is explicitly changed.

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
- Standardized the preferred source identity and search metadata on the apex `https://goreecloud.com/` hostname while preserving the separately managed external routing state.
- Added locally hosted project logos/icons for the Family Services cards, including Nextcloud, Immich, Jellyfin, Navidrome, Audiobookshelf, Paperless-ngx, Vaultwarden, Trilium, and Element.
- Added a public "How GoreeCloud Works" section that explains private access, self-hosted applications, storage and data, security and isolation, and backup and recovery at a high level without exposing private infrastructure details.
- Added and expanded a public "Platform Foundation" section featuring Proxmox VE, Debian 13, Docker, NetBird, AdGuard Home, Caddy, ntfy, Beszel, Uptime Kuma, and SearXNG with locally hosted technology logos/icons, role descriptions, and clear Active versus Planned Local status labeling.
- The Platform Foundation section distinguishes the current active Debian 13, Docker, NetBird, DNS, HTTPS, monitoring, notification, and private-search foundation from the planned locally owned Proxmox virtualization platform and does not publish private hostnames, addresses, ports, or administrative configuration.
- Added a public "Software & Development" section that explains GoreeCloud's three software approaches: use mature open-source applications, maintain forks when justified, and develop original GoreeCloud software only when a purpose-built application provides meaningful value.
- Identified GoreeCloud Research Library as the first maintained upstream fork and linked its public `GoreeCloud/linkding` repository while preserving Linkding attribution in the public description.
- Added the official GoreeCloud GitHub profile to the Follow section alongside Instagram, Pinterest, Threads, TikTok, X, and Reddit.
- Restored the official GoreeCloud artwork for the website brand treatment.
- Preserved public service descriptions, availability labels, social links, and the Cloudflare Pages security model.
- Added Escape-key handling to the mobile navigation so the menu can be closed from the keyboard and focus is returned to the menu button.
- Kept all page styling, scripting, service/platform assets, and technology-logo assets self-contained so the restrictive Content Security Policy remains compatible.

## v3 changes

- The site previously standardized canonical and social-preview URLs on the `www` hostname; v4 source metadata now uses the apex hostname as the preferred public identity.
- Added Cloudflare Pages `_headers` with a restrictive Content Security Policy and baseline browser security headers.
- HSTS is enabled for the host serving the Pages site without `includeSubDomains` or preload.

If Cloudflare Web Analytics, Turnstile, externally hosted fonts, or other third-party browser resources are added later, review and update the Content Security Policy before deployment.
