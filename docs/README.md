# GoreeCloud Website Repository Documentation

## Purpose

This directory contains repository-only operational, governance, release, and publication-review records for the GoreeCloud public website.

These files support release readiness, validation evidence, source-publication review, stability tracking, and long-term maintenance. They are not browser-facing website content and **must remain outside the generated `dist/` artifact**.

The public website itself remains defined by the exact `PUBLIC_FILES` allowlist in `scripts/build_public_site.py`.

## Documentation map

### `governance-readiness.md`

**Role:** GoreeCloud mandatory software/service baseline applicability record.

Use this record to map the website's anonymous static architecture to GoreeCloud multi-user, security, privacy, accessibility, and Glaze UI requirements. The multi-user gate is Not Applicable only while the website has no authentication, accounts, profiles, private workspace, or user-owned application data.

Authority boundary:

- applies only to the current anonymous static architecture;
- expires if identity or private-data features are introduced;
- does not waive security, privacy, Glaze UI, accessibility, deployment, or release requirements;
- is validated by `scripts/validate_governance_readiness.py`.

### `public-asset-inventory.md`

**Role:** Pre-publication artwork rights/provenance working inventory.

Use this record to identify every deployable artwork path and its reviewed file identity while issue #5 remains unresolved. It separates GoreeCloud identity/presentation assets from third-party project/platform marks and records provenance or brand-policy evidence where verified.

Authority boundary:

- authoritative working inventory for deployable artwork review;
- must match `PUBLIC_ASSET_FILES` exactly;
- Git blob IDs are integrity fingerprints, not copyright/trademark/redistribution-rights evidence;
- does not grant a license or resolve issue #5 by itself.

### `stability-baseline.md`

**Role:** Current repository-defined stable-version contract.

Use this record with the top-level `VERSION` file to define the current SemVer release, the scope of that version, the evidence required for stability, and the actions that remain outside release authorization.

Authority boundary:

- `VERSION` is the machine-readable version source;
- the baseline must describe the same version;
- stability requires exact source validation plus exact branch-preview and production verification;
- version metadata does not authorize repository visibility, DNS, Cloudflare configuration, or creative-rights decisions.

### `release-readiness-checklist.md`

**Role:** Canonical reusable release-readiness procedure.

Use this checklist to determine what must be verified before an authorized website release. It covers exact-candidate freeze, automated validation, Glaze UI visual acceptance, accessibility, resilience, privacy/origin behavior, issue #5, the already-completed issue #6 Cloudflare isolated-artifact prerequisite, explicit authorization, and post-release verification.

Authority boundary:

- controls the reusable release acceptance process;
- should remain procedural rather than becoming a running history log;
- passing every checklist item does not create authorization that was not explicitly granted;
- material checklist changes require repository review and CI validation.

### `release-evidence-template.md`

**Role:** Template for one-candidate historical validation evidence.

Create a working copy when a release candidate reaches formal manual acceptance. A completed record documents what was actually reviewed for one exact 40-character Git commit SHA, including automation, Glaze UI/accessibility acceptance, issue #5 disposition, Cloudflare isolated-artifact status, exceptions, authorization, and post-release results.

Use the repository generator rather than manually inventing a filename or editing the canonical template:

```bash
python scripts/create_release_evidence.py --commit <40-character-lowercase-git-sha>
```

The generator uses the Central-Time date, the approved lowercase/ISO/hyphen technical filename pattern, the canonical template, and **non-overwriting creation**. It binds the working record to the supplied SHA while leaving acceptance checkboxes unchecked. It does not fetch evidence, validate the candidate, authorize release, or infer readiness.

After a working record is edited, validate its structural and privacy boundaries with:

```bash
python scripts/validate_release_evidence.py
```

The validator checks candidate/filename/SHA binding, Central-Time 12-hour record metadata, private-network and selected secret patterns, final-disposition consistency, and fail-closed authorization structure. It **does not decide whether the underlying human review was substantively correct**.

Record-state lifecycle:

- keep `Record state` as `Working — not accepted` while no final candidate disposition is selected;
- when exactly one final disposition is selected, update `Record state` to the matching canonical value: `Accepted`, `Blocked`, `Rejected`, or `Superseded`;
- an `Accepted` record must retain required acceptance/gate evidence and record at least one explicitly authorized action with the authorizing person/role and authorization date/time;
- a generated record, structurally valid record, or green validation result does not itself authorize an action.

Authority boundary:

- a completed record is historical evidence, not current policy;
- evidence from one candidate must not be silently carried forward to another SHA;
- rejected, blocked, and superseded records retain their real disposition when they have historical value;
- sensitive supporting material belongs in an approved protected system rather than a repository evidence record.

Generated record location:

`docs/release-evidence/YYYY-MM-DD-<short-commit>-release-evidence.md`

Before issue #5 is resolved, review whether a completed record is appropriate for eventual repository publication before committing it.

## Authority relationships

In shorthand: **governance = mandatory-baseline applicability; inventory = publication/rights working record; stability = current stable-version contract; checklist = reusable procedure; evidence template = historical candidate record**.

The repository uses these records together without treating them as interchangeable:

1. `scripts/build_public_site.py` controls the exact technical public deployment file set.
2. `docs/governance-readiness.md` controls website-specific applicability of the mandatory multi-user/security/Glaze UI baseline.
3. `scripts/validate_governance_readiness.py` verifies that applicability still matches the architecture and CI gates.
4. `docs/public-asset-inventory.md` controls the working deployable-artwork rights/provenance review.
5. `VERSION` and `docs/stability-baseline.md` identify the current stable release contract.
6. `docs/release-readiness-checklist.md` controls the reusable manual release procedure.
7. `docs/release-evidence-template.md` defines candidate-specific historical evidence structure.
8. `scripts/create_release_evidence.py` safely instantiates a working candidate record but has no authority to validate or accept it.
9. `scripts/validate_release_evidence.py` validates evidence-record structure and selected privacy/safety invariants but not substantive release acceptance.
10. GitHub Actions and repository validators provide machine-generated validation evidence for the exact candidate they run against.
11. Issue #5 remains the open source-publication/creative-rights/visibility decision gate.
12. Issue #6 records the completed Cloudflare `dist/` isolated-publication cutover and is historical implementation context rather than a pending gate.
13. **Explicit human authorization remains required** for merge, repository visibility, DNS/routing, Cloudflare configuration changes, and production release actions.

A successful CI run, checksum, Git blob ID, preview deployment, generated record, structurally valid evidence record, or completed evidence record must not be presented as proving a different property or authorizing a different action.

## Privacy and publication boundary

Repository documentation must remain safe for the repository's approved visibility model.

**Do not record:**

- credentials, tokens, or private keys;
- private IP addresses or private hostnames;
- sensitive infrastructure diagrams or internal-only service URLs;
- raw logs containing unnecessary operational detail;
- private account identifiers or private GoreeCloud information not required for the record's purpose.

Use public-safe evidence identifiers and concise conclusions where possible. Retain sensitive evidence only in the approved protected system that owns it.

## Maintenance

When adding a permanent repository document, first determine whether an existing record already owns the subject. Prefer extending an authoritative record or adding a clear cross-reference over creating a competing source of truth.

If a new document is justified:

- define its Role and Purpose;
- state its authority boundary;
- identify related records;
- keep public/private information separated;
- add validation where silent drift would create material risk;
- keep it outside `dist/` unless deliberately approved as browser-facing content.

This index describes the repository documentation structure. It does not replace GoreeCloud-wide policies, standards, requirements, rules, or instructions.
