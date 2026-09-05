#!/usr/bin/env python3
from __future__ import annotations

from hashlib import sha1, sha256
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

from build_public_site import (
    PUBLIC_ASSET_FILES,
    RETIRED_SOURCE_ONLY_ASSET_FILES,
    ROOT,
    SOURCE_ONLY_ASSET_FILES,
)
from render_repository_portfolio import load_suite_manifest

MANIFEST = ROOT / "docs/visual-identity-sources.json"
INDEX = ROOT / "index.html"
GITHUB_REF = re.compile(r"^[0-9a-f]{40}$|^(?:main|master|dev)$")
DATE_REF = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def git_blob_id(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return sha1(header + raw).hexdigest()


def suite_records() -> dict[str, dict]:
    records: dict[str, dict] = {}
    for group in load_suite_manifest(ROOT)["groups"]:
        for app in group["applications"]:
            path = app["icon"]
            repository = app["source_repository"]
            source_ref = app["source_ref"]
            source_path = app["source_path"]
            records[path] = {
                "asset_path": path,
                "official_artwork_exists": True,
                "git_blob": app["icon_blob"],
                "source_authority": repository,
                "source_path": source_path,
                "source_ref": source_ref,
                "source_url": f"https://raw.githubusercontent.com/{repository}/{source_ref}/{source_path}",
            }
    return records


def main() -> int:
    errors: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    legacy_records = {
        record["asset_path"]: record
        for record in data.get("assets", [])
        if record.get("asset_path")
    }
    suite = suite_records()
    collisions = sorted(set(legacy_records).intersection(suite))
    for path in collisions:
        errors.append(f"Suite artwork path collides with legacy identity record: {path}")

    all_records = {**legacy_records, **suite}
    deployed = set(PUBLIC_ASSET_FILES)
    source_only = set(SOURCE_ONLY_ASSET_FILES)
    retired = set(RETIRED_SOURCE_ONLY_ASSET_FILES)

    classifications = {
        "deployable": deployed,
        "source-only": source_only,
        "retired": retired,
    }
    names = tuple(classifications)
    for index, left_name in enumerate(names):
        for right_name in names[index + 1:]:
            overlap = sorted(classifications[left_name] & classifications[right_name])
            for rel in overlap:
                errors.append(
                    f"Identity asset is classified as both {left_name} and {right_name}: {rel}"
                )

    for label, paths in classifications.items():
        missing = sorted(paths.difference(all_records))
        for rel in missing:
            errors.append(f"{label} identity asset lacks a reviewed provenance record: {rel}")

    classified = deployed | source_only | retired
    for rel in sorted(set(all_records).difference(classified)):
        errors.append(
            f"Identity provenance record is not classified as deployable, source-only, or retired history: {rel}"
        )

    # Preserve byte/provenance integrity for every retained identity file, whether
    # it is currently deployed by Main or kept only as source/history.
    for rel in sorted(classified):
        rec = all_records.get(rel)
        if rec is None:
            continue
        path = ROOT / rel
        if not path.is_file() or path.is_symlink():
            errors.append(f"Reviewed identity asset is not a regular file: {rel}")
            continue

        raw = path.read_bytes()
        if rec.get("git_blob"):
            if rec["git_blob"] != git_blob_id(raw):
                errors.append(f"Identity asset changed without reviewed Git-blob provenance: {rel}")
        else:
            actual = sha256(raw).hexdigest()
            if rec.get("sha256") != actual:
                errors.append(f"Identity asset changed without provenance review: {rel}")
            if rec.get("bytes") != path.stat().st_size:
                errors.append(f"Identity asset byte count drifted without provenance review: {rel}")

        if not rec.get("source_authority") or not rec.get("source_url"):
            errors.append(f"Identity asset lacks source authority: {rel}")
            continue

        parsed = urlparse(rec["source_url"])
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"Identity asset source URL must be an absolute HTTPS URL: {rel}")

        source_ref = str(rec.get("source_ref", ""))
        if parsed.netloc == "raw.githubusercontent.com" and not GITHUB_REF.fullmatch(source_ref):
            errors.append(f"GitHub-hosted identity asset must record a commit or named source branch: {rel}")
        elif parsed.netloc != "raw.githubusercontent.com" and not (
            GITHUB_REF.fullmatch(source_ref) or DATE_REF.fullmatch(source_ref)
        ):
            errors.append(f"Identity asset must record a commit, named branch, or dated review ref: {rel}")

    source_index = INDEX.read_text(encoding="utf-8")

    for stale in (
        'class="service-icon"',
        "platform-native-mark",
        "social-letter",
        "neutral Glaze UI letter marks instead of third-party logo artwork",
        "assets/goreecloud-icon.png",
        "assets/favicon.svg",
    ):
        if stale in source_index:
            errors.append(f"Obsolete placeholder/identity marker remains in rebuilt homepage: {stale}")

    # The rebuilt Main website intentionally deploys only the master mark. Every
    # other reviewed identity asset must stay out of the current homepage source.
    for rel in deployed:
        if rel not in source_index:
            errors.append(f"Deployable identity asset is not represented by rebuilt homepage source: {rel}")
    for rel in source_only | retired:
        if rel in source_index:
            errors.append(f"Non-deployable identity asset appears in rebuilt homepage source: {rel}")

    if source_index.count("assets/goreecloud-logo.svg") < 3:
        errors.append("Canonical GoreeCloud logo is not used across visible website identity surfaces.")

    for rec in data.get("assets", []):
        if rec.get("official_artwork_exists") is False and rec.get("fallback") != "text-only":
            errors.append(f"Non-art fallback must be text-only: {rec.get('id')}")

    if errors:
        print("Official visual-identity validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Official visual-identity validation passed across "
        f"{len(deployed)} deployable, {len(source_only)} source-only, and "
        f"{len(retired)} retired provenance assets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
