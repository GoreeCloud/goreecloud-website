# GoreeCloud Website Repository Documentation

## Purpose

This directory contains repository-only operational and governance records for the GoreeCloud public website.

These files support release readiness, source-publication review, validation evidence, and long-term maintenance. They are not part of the browser-facing website and must remain outside the generated `dist/` artifact.

The public website itself remains defined by the exact `PUBLIC_FILES` allowlist in `scripts/build_public_site.py`.

## Documentation map

### `public-asset-inventory.md`

**Role:** Pre-publication artwork rights/provenance working inventory.

Use this record to identify every deployable artwork path and the exact reviewed file content while issue #5 remains unresolved. It separates GoreeCloud identity/presentation assets from third-party project/platform marks and records provenance or brand-policy evidence where verified.

Authority boundary:

- authoritative working inventory for deployable artwork review;
- must match `PUBLIC_ASSET_FILES` exactly;
- Git blob IDs are integrity fingerprints, not copyright/trademark/redistribution-rights evidence;
- does not grant a license or resolve issue #5 by itself.

### `release-readiness-checklist.md`

**Role:** Canonical reusable release-readiness procedure.

Use this checklist to determine what must be verified before an authorized website release. It covers exact-candidate freeze, automated validation, Glaze UI visual acceptance, accessibility, resilience, privacy/origin behavior, issue #5, issue #6, explicit authorization, and post-release verification.

Authority boundary:

- controls the reusable release acceptance process;
- should remain stable and procedural rather than becoming a running history log;
- passing every checklist item does not create authorization that was not explicitly granted;
- material checklist changes require repository review and CI validation.

### `release-evidence-template.md`

**Role:** Template for one-candidate historical validation evidence.

Copy this template when a release candidate reaches formal manual acceptance. A completed record documents what was actually reviewed for one exact 40-character Git commit SHA, including automation, Glaze UI/accessibility acceptance, issue #5/#6 disposition, exceptions, authorization, and post-release results.

Authority boundary:

- a completed record is historical evidence, not current policy;
- evidence from one candidate must not be silently carried forward to another SHA;
- rejected, blocked, and superseded records should retain their real disposition when they have historical value;
- sensitive supporting material belongs in an appropriate protected system rather than being pasted into a repository evidence record.

Recommended completed-record location after the source-publication model is approved:

`docs/release-evidence/YYYY-MM-DD-<short-commit>-release-evidence.md`

Before issue #5 is resolved, review whether a completed record is appropriate for eventual repository publication before committing it.

## Authority relationships

The repository uses these records together without treating them as interchangeable:

1. `scripts/build_public_site.py` controls the exact technical public deployment file set.
2. `docs/public-asset-inventory.md` controls the working deployable-artwork rights/provenance review record.
3. `docs/release-readiness-checklist.md` controls the reusable manual release procedure.
4. `docs/release-evidence-template.md` defines the structure of candidate-specific historical evidence.
5. GitHub Actions and repository validators provide machine-generated validation evidence for the exact candidate they run against.
6. Issues #5 and #6 remain the tracked decision/external-operation gates for source publication/creative rights and Cloudflare `dist/` publication respectively.
7. Explicit human authorization remains required for merge, repository visibility, DNS/routing, Cloudflare configuration, and production release actions.

A successful CI run, checksum, Git blob ID, preview deployment, or completed evidence record must not be presented as proving a different property or authorizing a different action.

## Privacy and publication boundary

Repository documentation must remain safe for the repository's approved visibility model.

Do not record:

- credentials, tokens, or private keys;
- private IP addresses or private hostnames;
- sensitive infrastructure diagrams or internal-only service URLs;
- raw logs containing unnecessary operational detail;
- private account identifiers or other sensitive GoreeCloud information not required for the record's purpose.

Use public-safe evidence identifiers and concise conclusions where possible. Retain sensitive evidence only in the approved protected system that owns it.

## Maintenance

When adding a new permanent repository document, first determine whether an existing record already owns that subject. Prefer extending an authoritative record or adding a clear cross-reference over creating a competing source of truth.

If a new document is justified:

- define its Role and Purpose;
- state its authority boundary;
- identify related records;
- keep public/private information separated;
- add validation where silent drift would create material risk;
- keep it outside `dist/` unless it is deliberately approved as browser-facing content.

This index describes the repository documentation structure. It does not replace GoreeCloud-wide policies, standards, requirements, rules, or instructions.