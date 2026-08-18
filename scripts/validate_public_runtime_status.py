#!/usr/bin/env python3
"""Fail closed when public runtime and migration claims drift from the website status authority."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "docs" / "public-runtime-status.json"
INDEX_PATH = ROOT / "index.html"
REPOSITORIES_PATH = ROOT / "repositories.html"


def require(errors: list[str], text: str, marker: str, message: str) -> None:
    if marker not in text:
        errors.append(message)


def forbid(errors: list[str], text: str, marker: str, message: str) -> None:
    if marker in text:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Public runtime status validation failed: cannot read {STATUS_PATH.relative_to(ROOT)}: {exc}")
        return 1

    index = INDEX_PATH.read_text(encoding="utf-8")
    repositories = REPOSITORIES_PATH.read_text(encoding="utf-8")

    if status.get("schema_version") != 1:
        errors.append("public-runtime-status.json must use schema_version 1.")
    if status.get("as_of") != "2026-08-18":
        errors.append("public-runtime-status.json must retain the reviewed 2026-08-18 authority date until deliberately revalidated.")

    services = status.get("services")
    if not isinstance(services, dict):
        errors.append("public-runtime-status.json must define a services object.")
        services = {}

    expected_states = {
        "goreecloud-memos": "stable-production",
        "goreecloud-notify": "release-candidate",
        "goreecloud-search": "stable-production",
        "goreecloud-monitor": "active-development",
    }
    for slug, state in expected_states.items():
        record = services.get(slug)
        if not isinstance(record, dict):
            errors.append(f"Missing public runtime status record: {slug}")
            continue
        if record.get("state") != state:
            errors.append(f"Unexpected public runtime state for {slug}: {record.get('state')!r}")

    # Accepted production application.
    require(errors, index, '<article class="service-card" data-service="memos">', "Homepage must retain the GoreeCloud Memos service card.")
    require(errors, index, '<span class="badge active">Available Now</span>', "Accepted GoreeCloud Memos production must be presented as Available Now.")
    require(errors, index, "GoreeCloud Memos v0.1.2 is the accepted Stable production service", "Homepage project copy must identify Memos v0.1.2 as accepted Stable production.")
    forbid(errors, index, '<span class="badge growing">Stabilizing</span>', "Homepage must not regress accepted GoreeCloud Memos production to Stabilizing.")

    # Notification migration is not complete.
    require(errors, index, "ntfy remains the current production notification service", "Homepage must state that ntfy remains the current production notification service.")
    require(errors, index, "GoreeCloud Notify is a release candidate", "Homepage must present GoreeCloud Notify as a release candidate.")
    require(errors, repositories, "Release-candidate successor to ntfy; ntfy remains current production until controlled cutover.", "Repository directory must preserve the Notify migration boundary.")
    forbid(errors, index, "has replaced ntfy", "Homepage must not claim GoreeCloud Notify has replaced ntfy before production acceptance.")
    forbid(errors, index, "GoreeCloud Notify replaces ntfy", "Homepage timeline must not record an unaccepted Notify cutover.")
    forbid(errors, repositories, "Current GoreeCloud notification layer.", "Repository directory must not call GoreeCloud Notify the current notification layer before cutover.")

    # Accepted Search migration and pending Monitoring migration remain independently true.
    require(errors, index, "has replaced the direct SearXNG-facing service", "Homepage must preserve the accepted GoreeCloud Search cutover.")
    require(errors, index, "Uptime Kuma remains in service until GoreeCloud Monitoring completes validation", "Homepage must preserve the Uptime Kuma transition boundary.")
    require(errors, repositories, "Planned replacement for Uptime Kuma after controlled validation.", "Repository directory must preserve the Monitor transition boundary.")

    if errors:
        print("Public runtime status validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Public runtime status validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
