# GoreeCloud Website Repository Documentation

## Purpose

This directory contains repository-only operational and governance records for the GoreeCloud public website.

These files support release readiness, source-publication review, validation evidence, and long-term maintenance. They are not part of the browser-facing website and must remain outside the generated `dist/` artifact.

The public website itself remains defined by the exact `PUBLIC_FILES` allowlist in `scripts/build_public_site.py`.

## Documentation map

### `governance-readiness.md`

**Role:** GoreeCloud mandatory software/service baseline applicability record.

Use this record to map the website's current anonymous static architecture to the GoreeCloud multi-user, security, and Glaze UI production-readiness requirements. It documents why the multi-user gate is Not Applicable to the current no-account/no-private-workspace website while keeping security and Glaze UI fully applicable.

Authority boundary:

- applies only to the current static anonymous website architecture;
- the multi-user Not Applicable determination expires if authentication, accounts, profiles, private state, or other user identity/data boundaries are introduced;
- does not waive security, privacy, Glaze UI, accessibility, deployment, or release requirements;
- is machine-checked by `scripts/validate_governance_readiness.py` and must change when the architecture changes.

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

Create a working copy when a release candidate reaches formal manual acceptance. A completed record documents what was actually reviewed for one exact 40-character Git commit SHA, including automation, Glaze UI/accessibility acceptance, issue #5/#6 disposition, exceptions, authorization, and post-release results.

Use the repository generator rather than manually inventing a filename or editing the canonical template:

```bash
python scripts/create_release_evidence.py --commit <40-character-lowercase-git-sha>
```

The generator uses the Central-Time date, the approved lowercase/ISO/hyphen technical filename pattern, the canonical template, and non-overwriting creation. It binds the working record to the supplied SHA while leaving every acceptance checkbox unchecked. It does not fetch evidence, validate the candidate, authorize release, or infer readiness.

After a working record is edited, validate its structural and privacy boundaries with:

```bash
python scripts/validate_release_evidence.py
```

The validator checks candidate/filename/SHA binding, Central-Time 12-hour record metadata, private-network and selected secret patterns, final-disposition consistency, and fail-closed authorization structure. It does not decide whether the underlying human review was substantively correct.

Record-state lifecycle:

- keep `Record state` as `Working — not accepted` while no final candidate disposition is selected;
- when exactly one final disposition is selected, update `Record state` to the matching canonical value: `Accepted`, `Blocked`, `Rejected`, or `Superseded`;
- an `Accepted` record must retain the required acceptance/gate checkboxes and record at least one explicitly authorized action with the authorizing person/role and authorization date/time;
- a generated record, a structurally valid record, or a green validation result does not itself authorize any action.

Authority boundary:

- a completed record is historical evidence, not current policy;
- evidence from one candidate must not be silently carried forward to another SHA;
- rejected, blocked, and superseded records should retain their real disposition when they have historical value;
- sensitive supporting material belongs in an appropriate protected system rather than being pasted into a repository evidence record.

Generated record location:

`docs/release-evidence/YYYY-MM-DD-<short-commit>-release-evidence.md`

Before issue #5 is resolved, review whether a completed record is appropriate for eventual repository publication before committing it.

## Authority relationships

In shorthand: **governance = mandatory-baseline applicability; inventory = publication/rights working record; checklist = reusable procedure; evidence template = historical candidate record**.

The repository uses these records together without treating them as interchangeable:

1. `scripts/build_public_site.py` controls the exact technical public deployment file set.
2. `docs/governance-readiness.md` controls the website-specific applicability mapping for the mandatory multi-user/security/Glaze UI baseline.
3. `scripts/validate_governance_readiness.py` verifies that the documented applicability still matches the static architecture and required CI gates.
4. `docs/public-asset-inventory.md` controls the working deployable-artwork rights/provenance review record.
5. `docs/release-readiness-checklist.md` controls the reusable manual release procedure.
6. `docs/release-evidence-template.md` defines the structure of candidate-specific historical evidence.
7. `scripts/create_release_evidence.py` safely instantiates a working candidate record but has no authority to validate or accept it.
8. `scripts/validate_release_evidence.py` validates record structure, candidate binding, disposition consistency, and selected privacy/safety invariants but does not determine substantive release acceptance.
9. GitHub Actions and repository validators provide machine-generated validation evidence for the exact candidate they run against.
10. Issues #5 and #6 remain the tracked decision/external-operation gates for source publication/creative rights and Cloudflare `dist/` publication respectively.
11. Explicit human authorization remains required for merge, repository visibility, DNS/routing, Cloudflare configuration, and production release actions.

A successful CI run, checksum, Git blob ID, preview deployment, generated record, structurally valid evidence record, or completed evidence record must not be presented as proving a different property or authorizing a different action.

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
