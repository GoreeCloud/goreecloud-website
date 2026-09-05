# GoreeCloud five-product public center

Source foundation for a combined public website covering **GoreeCloud Home Security**, **GoreeCloud Home**, **GoreeCloud AI**, **GoreeCloud Containers**, and **GoreeCloud Code**.

`labs.goreecloud.com` is a **Proposed technical website namespace**, not a new GoreeCloud product or umbrella brand. The public page uses the GoreeCloud master brand and preserves the five canonical product names.

## Cloudflare Pages contract

- Repository: `GoreeCloud/goreecloud-website`
- Root directory: `/`
- Build command: `python sites/labs/build.py`
- Build output directory: `sites/labs/dist`
- Production branch: `main` only after review and merge
- Proposed custom domain: `labs.goreecloud.com`
- Current publication state: **source prepared; production activation pending**

The site is static at browser runtime. It does not host GoreeCloud Home device control, Home Security camera processing, AI inference/runtime APIs, Containers workload execution, Code forge/provider operations, or private GoreeCloud application services.

## Production gates still required

Before this source can be represented as a production website:

1. Create or verify the dedicated Cloudflare Pages project.
2. Configure and verify the custom domain, DNS, HTTPS, and TLS state.
3. Confirm branch-preview publication matches the reviewed candidate source.
4. Complete required representative-mobile human visual review, including touch targets, safe areas, 200% text/reflow, appearance modes, and horizontal-overflow checks.
5. Confirm production deployment matches the accepted revision.
6. Only then change the site from `noindex,nofollow` / `Disallow: /` and link it as an active destination from the main website.

## GLAZE UI

The Pages build fetches the exact current Stable GLAZE UI V1.1 / 1.1.0 web CSS from canonical commit `15cc76d2bcd4065552dc31c77145b63f34d9e7b2`, validates the expected import closure and Stable markers, and republishes the CSS same-origin inside the isolated artifact. Browsers do not fetch GLAZE UI from GitHub at runtime.
