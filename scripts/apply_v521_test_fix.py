#!/usr/bin/env python3
"""Update the existing public-asset inventory regression contract for v5.21."""

from pathlib import Path

path = Path(__file__).resolve().parents[1] / "tests" / "test_public_asset_inventory.py"
text = path.read_text(encoding="utf-8")
old = '''        required = (\n            "not a license grant",\n            "provenance and rights verification still required",\n            "source-code license must not be assumed to relicense third-party marks",\n            "integrity fingerprint only",\n            "does not establish copyright ownership",\n            "issue #5 remains open",\n        )'''
new = '''        required = (\n            "not a license grant",\n            "third-party artwork removed from the public artifact",\n            "repository presence does not make those files deployable",\n            "does not automatically license goreecloud branding or third-party marks",\n            "final human reachable-history/contextual-disclosure review",\n            "issue #5 remains open",\n        )'''
if text.count(old) != 1:
    raise SystemExit(f"expected one legacy publication-boundary tuple, found {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Updated existing public-asset inventory regression contract for v5.21.")
