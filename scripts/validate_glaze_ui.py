#!/usr/bin/env python3
from pathlib import Path
import sys

from glaze_ui_2 import GLAZE_PROMOTION_REVISION, GLAZE_VERSION

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "css/glaze-ui-2.2.0.css"
ROOT_PAGES = [ROOT / n for n in ("index.html", "repositories.html", "privacy.html", "security.html", "404.html")]
CHILD_PAGES = [
    ROOT / "sites/projects/index.html", ROOT / "sites/projects/404.html",
    ROOT / "sites/roadmap/index.html", ROOT / "sites/roadmap/404.html",
    ROOT / "sites/blog/index.html", ROOT / "sites/blog/404.html",
    ROOT / "sites/archive/index.html", ROOT / "sites/archive/404.html",
]
CHILD_BUNDLES = [
    ROOT / "sites/projects/assets/glaze-ui-2.2.0.css",
    ROOT / "sites/roadmap/glaze-ui-2.2.0.css",
    ROOT / "sites/blog/glaze-ui-2.2.0.css",
    ROOT / "sites/archive/glaze-ui-2.2.0.css",
]
CONFORMANCE = ROOT / "docs/glaze-ui-conformance.md"
BUILD = ROOT / "scripts/build_public_site.py"
errors = []

bundle_markers = [
    "Glaze UI 2.2.0 Stable consumer integration",
    GLAZE_PROMOTION_REVISION,
    "Solid where users read. Glazed where users interact.",
    "--glaze-touch-min: 48px",
    "--glaze-touch-assisted: 56px",
    'data-glaze-density="comfortable"',
    'data-glaze-density="compact"',
    'data-glaze-performance="reduced"',
    'data-glaze-large-text="true"',
    "prefers-reduced-motion",
    "prefers-reduced-transparency",
    "prefers-contrast: more",
    "forced-colors: active",
    "--glaze-system-panel-budget: 1",
]
for bundle in [BUNDLE, *CHILD_BUNDLES]:
    if not bundle.is_file():
        errors.append(f"Glaze UI 2.2 bundle is missing: {bundle.relative_to(ROOT)}")
        continue
    css = bundle.read_text(encoding="utf-8")
    for marker in bundle_markers:
        if marker not in css:
            errors.append(f"{bundle.relative_to(ROOT)} missing 2.2 marker: {marker}")
    if "raw.githubusercontent.com" in css or "https://" in css or "http://" in css:
        errors.append(f"{bundle.relative_to(ROOT)} must remain a same-origin/local presentation contract")


def validate_page(page: Path) -> None:
    if not page.is_file():
        errors.append(f"Deployable HTML surface is missing: {page.relative_to(ROOT)}")
        return
    text = page.read_text(encoding="utf-8")
    for marker in [
        f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"',
        f'data-glaze-ui="{GLAZE_VERSION}"',
        'glaze-canvas',
        'name="viewport"',
    ]:
        if marker not in text:
            errors.append(f"{page.relative_to(ROOT)} missing source-native 2.2 marker: {marker}")
    for stale in (
        'data-glaze-ui="1.5.0"',
        'data-glaze-ui="2.0.0"',
        'data-glaze-ui="2.1.0"',
        'goreecloud-glaze-ui" content="1.5.0"',
        'goreecloud-glaze-ui" content="2.0.0"',
        'goreecloud-glaze-ui" content="2.1.0"',
        'glaze-ui-1.5.0.css',
        'glaze-ui-2.0.0.css',
        'glaze-ui-2.1.0.css',
    ):
        if stale in text:
            errors.append(f"{page.relative_to(ROOT)} still activates superseded Glaze UI: {stale}")
    if "raw.githubusercontent.com" in text:
        errors.append(f"{page.relative_to(ROOT)} must not load remote Glaze UI at runtime")


for page in [*ROOT_PAGES, *CHILD_PAGES]:
    validate_page(page)

text = CONFORMANCE.read_text(encoding="utf-8") if CONFORMANCE.is_file() else ""
for marker in [
    "Target Glaze UI version: **2.2.0**",
    "GoreeCloud/goreecloud-glaze-ui",
    GLAZE_PROMOTION_REVISION,
    "same-origin",
    "Solid where users read. Glazed where users interact.",
    "48px general interaction floor",
    "56px Touch Assistance floor",
    "one dominant Glaze panel",
    "Rendered/production acceptance",
    "No production Glaze UI exception",
    "Source / generated / deployed agreement",
]:
    if marker not in text:
        errors.append(f"Conformance marker missing: {marker}")

build_text = BUILD.read_text(encoding="utf-8") if BUILD.is_file() else ""
if '"css/glaze-ui-2.2.0.css"' not in build_text:
    errors.append("Public build allowlist does not publish the active 2.2.0 bundle")
if '"css/glaze-ui-2.1.0.css"' in build_text:
    errors.append("Public build allowlist still publishes the superseded 2.1.0 bundle")

if errors:
    print("Glaze UI 2.2 validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print("Glaze UI 2.2.0 Stable source validation passed across Main, Projects, Roadmap, Blog, and Archive surfaces.")
