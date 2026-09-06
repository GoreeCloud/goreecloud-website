# GoreeCloud Labs — Identity Asset Authority

This transitional Labs source must follow the same product-artwork authority as the canonical package in `GoreeCloud/goreecloud-static-websites` until Cloudflare Pages is cut over and this legacy source is retired.

## Authority

Canonical branding authority: `GoreeCloud/goreecloud-branding-assets`.

A product card may render a logo, icon, mark, favicon derivative, or other identity artwork only when that asset has an approved canonical source in the branding authority or an explicitly governed approved derivative. Website-local initials, acronyms, text pills, generic symbols, upstream product logos, placeholders, and provisional artwork are not substitutes.

## Approved exact-source artwork

| Product | Canonical branding source | Required Git blob | Transitional Labs copy |
| --- | --- | --- | --- |
| GoreeCloud AI | `products/ai/app-icon.svg` | `1cbe04748f50cb843eef0cbb7233e2769efa275a` | `assets/products/ai.svg` |
| GoreeCloud Code | `products/code/app-icon.svg` | `579f0416bd2839bf40e87de7751e319d80bd0bf9` | `assets/products/code.svg` |

The GoreeCloud master logo remains exact canonical blob `082936062de7839148db89ea3ab4e86ff71341b0` from the repository root asset.

## Artwork approval blockers

The following products do not currently have approved canonical product artwork in the branding authority and therefore must render **no surrogate identity artwork** on Labs until approval is recorded:

- GoreeCloud Home
- GoreeCloud Home Security
- GoreeCloud Containers
- GoreeCloud Boot

Approval is tracked in `GoreeCloud/goreecloud-branding-assets#16`.

Until that authority gate closes, the canonical product names remain visible, but the former `Home`, `Security`, `OCI`, and `Boot` text badges are intentionally suppressed. This is a conformance boundary, not an invitation to invent local graphics.

## Retirement boundary

`GoreeCloud/goreecloud-website` is not the long-term static-site authority. These exact-source safeguards are maintained here only so the currently connected Labs Cloudflare deployment does not regress while the canonical `sites/labs` package is validated, cut over, production-verified, and the legacy source is retired.
