# goreecloud-website

Public static website for GoreeCloud.com.

## Structure

- `index.html` — main public website
- `css/style.css` — responsive site styling
- `js/main.js` — mobile navigation and footer year
- `assets/favicon.svg` — site favicon
- `robots.txt` — search crawler instructions
- `sitemap.xml` — basic sitemap

## Deployment

This repository is intended for Cloudflare Pages.

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
