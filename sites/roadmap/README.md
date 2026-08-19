# GoreeCloud Roadmap Public Website

This directory contains the public development-roadmap site planned for `https://roadmap.goreecloud.com`.

## Cloudflare Pages contract

- Repository: `GoreeCloud/goreecloud-website`
- Production branch: `main`
- Root directory: `sites/roadmap`
- Build command: none
- Build output directory: `.`
- Planned custom domain: `roadmap.goreecloud.com`

## Public-information boundary

The roadmap is deliberately broader and less detailed than internal task trackers, project specifications, change logs, infrastructure plans, and security records. It communicates public direction without exposing private topology, operational details, sensitive remediation work, credentials, private hostnames, internal addresses, or unpublished project information.

Roadmap states describe direction and maturity, not guaranteed delivery dates. Dates and commitments must not be inferred from ordering alone.

## Validation

Run:

```bash
python3 sites/roadmap/validate.py
```

Cloudflare project connection, custom-domain activation, and DNS changes are separate production operations after source and preview acceptance.
