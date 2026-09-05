#!/usr/bin/env python3
"""Fail closed when current public runtime claims drift across source authorities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "docs" / "public-runtime-status.json"
SUITE_PATH = ROOT / "docs" / "suite-portfolio.json"
INDEX_PATH = ROOT / "index.html"
REPOSITORIES_PATH = ROOT / "repositories.html"
RUNTIME_AUTHORITY_DATE = "2026-08-31"
SUITE_REGISTRY_REVIEW_DATE = "2026-09-01"


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object.")
        return {}
    return value


def suite_applications(suite: dict, errors: list[str]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    groups = suite.get("groups")
    if not isinstance(groups, list):
        errors.append("suite-portfolio.json must define a groups array.")
        return result
    for group in groups:
        if not isinstance(group, dict):
            errors.append("suite-portfolio.json groups must be objects.")
            continue
        applications = group.get("applications")
        if not isinstance(applications, list):
            errors.append(f"Suite group {group.get('id')!r} must define an applications array.")
            continue
        for application in applications:
            if not isinstance(application, dict):
                errors.append(f"Suite group {group.get('id')!r} contains a non-object application.")
                continue
            app_id = application.get("id")
            if not isinstance(app_id, str) or not app_id:
                errors.append(f"Suite group {group.get('id')!r} contains an application without a valid id.")
                continue
            if app_id in result:
                errors.append(f"Duplicate Suite application id: {app_id}")
                continue
            result[app_id] = application
    return result


def main() -> int:
    errors: list[str] = []
    status = load_json(STATUS_PATH, errors)
    suite = load_json(SUITE_PATH, errors)

    if status.get("schema_version") != 2:
        errors.append("public-runtime-status.json must use schema_version 2.")
    if status.get("as_of") != RUNTIME_AUTHORITY_DATE:
        errors.append(
            "public-runtime-status.json must retain the reviewed "
            f"{RUNTIME_AUTHORITY_DATE} authority date until deliberately revalidated."
        )
    if suite.get("as_of") != SUITE_REGISTRY_REVIEW_DATE:
        errors.append(
            "suite-portfolio.json must retain the reviewed "
            f"{SUITE_REGISTRY_REVIEW_DATE} registry date until deliberately revalidated."
        )

    services = status.get("services")
    if not isinstance(services, dict):
        errors.append("public-runtime-status.json must define a services object.")
        services = {}

    apps = suite_applications(suite, errors)
    expected = {
        "goreecloud-memos": {
            "suite_id": "memos",
            "product_state": "stable-production",
            "runtime_state": "production-accepted",
            "current_service": "GoreeCloud Memos v0.1.3",
            "production_authority": "GoreeCloud Memos v0.1.3",
            "suite_status": "Stable Production v0.1.3",
            "suite_status_class": "active",
        },
        "goreecloud-notify": {
            "suite_id": "notify",
            "product_state": "release-candidate",
            "runtime_state": "pre-cutover",
            "current_service": "ntfy v2.26.3",
            "production_authority": "ntfy v2.26.3",
            "suite_status": "Release Candidate",
            "suite_status_class": "growing",
        },
        "goreecloud-search": {
            "suite_id": "search",
            "product_state": "active-development",
            "runtime_state": "transitional-production",
            "current_service": "GoreeCloud Search",
            "production_authority": "Current SearXNG-derived GoreeCloud Search runtime",
            "suite_status": "Current Service · Native Rebuild",
            "suite_status_class": "active",
        },
        "goreecloud-monitor": {
            "suite_id": "monitor",
            "product_state": "active-validation",
            "runtime_state": "pre-cutover",
            "current_service": "Uptime Kuma",
            "production_authority": "Uptime Kuma",
            "suite_status": "Active Validation",
            "suite_status_class": "growing",
        },
    }

    for slug, contract in expected.items():
        record = services.get(slug)
        if not isinstance(record, dict):
            errors.append(f"Missing public runtime status record: {slug}")
            continue
        for field in ("public_name", "public_label", "transition"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"Public runtime status {slug} must define non-empty {field}.")
        for field in ("product_state", "runtime_state", "current_service", "production_authority"):
            expected_value = contract[field]
            if record.get(field) != expected_value:
                errors.append(
                    f"Unexpected {field} for {slug}: expected {expected_value!r}, found {record.get(field)!r}."
                )

        app = apps.get(contract["suite_id"])
        if not isinstance(app, dict):
            errors.append(f"Suite portfolio is missing runtime-tracked application: {contract['suite_id']}")
            continue
        if app.get("status") != contract["suite_status"]:
            errors.append(
                f"Suite status for {contract['suite_id']} must be {contract['suite_status']!r}, found {app.get('status')!r}."
            )
        if app.get("status_class") != contract["suite_status_class"]:
            errors.append(
                f"Suite status class for {contract['suite_id']} must be {contract['suite_status_class']!r}, found {app.get('status_class')!r}."
            )

    # The rebuilt Main and focused repository page no longer duplicate the full
    # Suite/runtime directory. They must remain free of stale or over-promoted
    # runtime claims while the reviewed JSON authorities continue to be validated.
    try:
        public_text = INDEX_PATH.read_text(encoding="utf-8") + "\n" + REPOSITORIES_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read rebuilt public source: {exc}")
        public_text = ""

    stale_current_markers = (
        'data-service="memos"',
        'data-service="notify"',
        'data-service="search"',
        'data-service="monitor"',
        "GoreeCloud Memos v0.1.2",
        "GoreeCloud Notify has replaced ntfy",
        "GoreeCloud Notify replaces ntfy",
        "GoreeCloud Monitor has replaced Uptime Kuma",
        "GoreeCloud Search native implementation is Stable",
    )
    for marker in stale_current_markers:
        if marker in public_text:
            errors.append(f"Rebuilt public source contains stale or unaccepted runtime claim: {marker}")

    authority_text = STATUS_PATH.read_text(encoding="utf-8") + "\n" + SUITE_PATH.read_text(encoding="utf-8")
    for marker in (
        "GoreeCloud Memos v0.1.2",
        "GoreeCloud Notify has replaced ntfy",
        "GoreeCloud Notify replaces ntfy",
        "GoreeCloud Monitor has replaced Uptime Kuma",
        "GoreeCloud Search native implementation is Stable",
    ):
        if marker in authority_text:
            errors.append(f"Superseded or unaccepted current runtime claim remains in current-state authorities: {marker}")

    if errors:
        print("Public runtime status validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Public runtime status validation passed: reviewed runtime and Suite authorities remain pinned, and the rebuilt public front door does not duplicate or over-promote runtime state."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
