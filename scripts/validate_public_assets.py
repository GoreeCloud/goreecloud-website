#!/usr/bin/env python3
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from build_public_site import PUBLIC_ASSET_FILES, ROOT
MANIFEST = ROOT / "docs/visual-identity-sources.json"
INDEX = ROOT / "index.html"
GITHUB_REF = re.compile(r"^[0-9a-f]{40}$|^(?:main|master|dev)$")
DATE_REF = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main():
    errors = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = data.get("assets", [])
    deployed = {r["asset_path"]: r for r in records if r.get("asset_path")}
    expected = set(PUBLIC_ASSET_FILES) - {"assets/social-preview.png"}

    if set(deployed) != expected:
        errors.append(
            f"Identity manifest/deployable artwork mismatch: manifest={sorted(deployed)} expected={sorted(expected)}"
        )

    for rel, rec in deployed.items():
        p = ROOT / rel
        if not p.is_file() or p.is_symlink():
            errors.append(f"Official identity asset is not a regular file: {rel}")
            continue

        actual = sha256(p.read_bytes()).hexdigest()
        if rec.get("sha256") != actual:
            errors.append(f"Identity asset changed without provenance review: {rel}")
        if rec.get("bytes") != p.stat().st_size:
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

    index = INDEX.read_text(encoding="utf-8")
    for stale in (
        'class="service-icon"',
        "platform-native-mark",
        "social-letter",
        "neutral Glaze UI letter marks instead of third-party logo artwork",
        "assets/goreecloud-icon.png",
        "assets/favicon.svg",
    ):
        if stale in index:
            errors.append(f"Obsolete placeholder/identity marker remains: {stale}")

    for rel in expected:
        if rel != "assets/goreecloud-logo.svg" and rel not in index:
            errors.append(f"Deployable identity asset is not referenced by homepage: {rel}")
    if index.count("assets/goreecloud-logo.svg") < 3:
        errors.append("Canonical GoreeCloud logo is not used across visible website identity surfaces.")

    for rec in records:
        if rec.get("official_artwork_exists") is False and rec.get("fallback") != "text-only":
            errors.append(f"Non-art fallback must be text-only: {rec.get('id')}")

    if errors:
        print("Official visual-identity validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Official visual-identity validation passed across {len(deployed)} deployed identity assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
