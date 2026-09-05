#!/usr/bin/env python3
"""Validate GoreeCloud Website source targeting the current Stable GLAZE UI V1.1 contract."""
from pathlib import Path
import sys

from glaze_v1 import GLAZE_SOURCE_REVISION, GLAZE_VERSION, KNOWN_STABLE_WORKAROUND_MARKER

ROOT = Path(__file__).resolve().parents[1]
ROOT_PAGES = [ROOT / n for n in ("index.html", "repositories.html", "privacy.html", "security.html", "404.html")]
LABS_PAGES = [ROOT / "sites/labs/index.html", ROOT / "sites/labs/404.html"]
CONFORMANCE = ROOT / "docs/glaze-ui-conformance.md"
errors: list[str] = []

for page in [*ROOT_PAGES, *LABS_PAGES]:
    if not page.is_file():
        errors.append(f"missing V1.1 consumer page: {page.relative_to(ROOT)}")
        continue
    text = page.read_text(encoding="utf-8")
    for marker in (
        'data-glaze-version="1.1"',
        f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"',
        f'data-glaze-ui="{GLAZE_VERSION}"',
    ):
        if marker not in text:
            errors.append(f"{page.relative_to(ROOT)} missing marker: {marker}")
    for retired in (
        'content="2.1.0"',
        'data-glaze-ui="2.1.0"',
        'content="2.2.0"',
        'data-glaze-ui="2.2.0"',
    ):
        if retired in text:
            errors.append(f"{page.relative_to(ROOT)} still activates retired 2.x GLAZE source")
    if "raw.githubusercontent.com" in text:
        errors.append(f"{page.relative_to(ROOT)} must not load GLAZE remotely at browser runtime")

conformance = CONFORMANCE.read_text(encoding="utf-8") if CONFORMANCE.is_file() else ""
for marker in (
    f"GLAZE UI V1.1 / {GLAZE_VERSION}",
    GLAZE_SOURCE_REVISION,
    "consumer acceptance remains pending",
    "legacy satellite sites",
    "Known immutable Stable-source defect",
    "not GLAZE consumer-conformance evidence",
):
    if marker not in conformance:
        errors.append(f"conformance record missing: {marker}")

if KNOWN_STABLE_WORKAROUND_MARKER not in (ROOT / "scripts/glaze_v1.py").read_text(encoding="utf-8"):
    errors.append("GLAZE build helper is missing the explicit known-defect workaround marker")

if errors:
    print("GLAZE UI V1.1 source validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(
    "GLAZE UI V1.1 source target validated for the rebuilt main site and new Labs "
    "product-center source; bounded Stable import workaround and pending conformance are explicit."
)
