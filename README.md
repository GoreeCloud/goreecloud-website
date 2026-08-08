# goreecloud-website

Public static website for GoreeCloud.com.

## Version

Current website package: **v3**

## Structure

- `index.html` — main public website
- `css/style.css` — responsive site styling
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

## v3 changes

- Canonical URL standardized on `https://www.goreecloud.com/`.
- Open Graph and X/Twitter preview URLs standardized on the `www` production hostname.
- `robots.txt` and `sitemap.xml` standardized on the `www` production hostname.
- Added Cloudflare Pages `_headers` with a restrictive Content Security Policy and baseline browser security headers.
- HSTS is enabled for the host serving the Pages site without `includeSubDomains` or preload.

If Cloudflare Web Analytics, Turnstile, externally hosted fonts, or other third-party browser resources are added later, review and update the Content Security Policy before deployment.
