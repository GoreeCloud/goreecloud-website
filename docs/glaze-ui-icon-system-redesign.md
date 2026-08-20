# Glaze UI Icon System Redesign

## Purpose

Replace generic project-card artwork with purpose-built GoreeCloud identity assets while keeping Glaze UI as the canonical owner of the visual system.

## Canonical Source

Official Glaze UI, Privacy Shield, Wardveil Security, and GoreeCloud application identity artwork is maintained in:

- `GoreeCloud/glaze-ui`

The website must not become the source of truth for Glaze UI identity artwork.

## Website Consumption Model

The Projects site consumes canonical SVG assets from the public `glaze-ui` repository. Application cards derive their symbol URL from the repository slug, while shared foundations use their dedicated canonical paths.

Current canonical namespaces:

- `branding/icons/glaze-ui/`
- `branding/identities/privacy-shield/`
- `branding/identities/wardveil-security/`
- `branding/applications/<repository>/`

The site keeps only its own GoreeCloud website fallback logo locally.

## Reliability

Project artwork loading includes a local fallback to `goreecloud-logo.svg` if a canonical asset cannot be loaded. The Projects site Content Security Policy explicitly permits image delivery from `raw.githubusercontent.com` while keeping other resource classes restricted.

## Adoption Goal

Every Projects card should display a distinct official identity asset instead of reusing the generic GoreeCloud mark. Canonical artwork changes should be made in `GoreeCloud/glaze-ui`, then consumed automatically by the Projects site from the Glaze UI main branch.
