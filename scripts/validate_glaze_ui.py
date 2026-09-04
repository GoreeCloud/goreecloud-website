#!/usr/bin/env python3
from pathlib import Path
import sys

from glaze_ui_2 import GLAZE_ACTIVATION_VERSION, GLAZE_PROMOTION_REVISION, GLAZE_VERSION

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "css/glaze-v1.1.0.css"
ROOT_PAGES = [ROOT / n for n in ("index.html", "repositories.html", "privacy.html", "security.html", "404.html")]
CHILD_PAGES = [
    ROOT / "sites/projects/index.html", ROOT / "sites/projects/404.html",
    ROOT / "sites/roadmap/index.html", ROOT / "sites/roadmap/404.html",
    ROOT / "sites/blog/index.html", ROOT / "sites/blog/404.html",
    ROOT / "sites/archive/index.html", ROOT / "sites/archive/404.html",
]
CHILD_BUNDLES = [
    ROOT / "sites/projects/assets/glaze-v1.1.0.css",
    ROOT / "sites/roadmap/glaze-v1.1.0.css",
    ROOT / "sites/blog/glaze-v1.1.0.css",
    ROOT / "sites/archive/glaze-v1.1.0.css",
]
CONFORMANCE = ROOT / "docs/glaze-ui-conformance.md"
errors = []

bundle_markers = [
    "GLAZE UI V1.1 / 1.1.0 Stable consumer integration",
    GLAZE_PROMOTION_REVISION,
    "--glz1-canvas:",
    "--glz11-deep-teal:",
    "--glz11-soft-aqua:",
    "--glz11-soft-amber:",
    "--glz1-target-shell: 48px",
    "--glz1-target-assisted: 56px",
    'data-glaze-version="1.1"',
    "prefers-reduced-motion",
    "prefers-reduced-transparency",
    "prefers-contrast: more",
    "forced-colors: active",
]
for bundle in [BUNDLE, *CHILD_BUNDLES]:
    if not bundle.is_file():
        errors.append(f"GLAZE UI V1.1 bundle is missing: {bundle.relative_to(ROOT)}")
        continue
    css = bundle.read_text(encoding="utf-8")
    for marker in bundle_markers:
        if marker not in css:
            errors.append(f"{bundle.relative_to(ROOT)} missing V1.1 marker: {marker}")


def validate_page(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    for marker in [
        f'data-glaze-version="{GLAZE_ACTIVATION_VERSION}"',
        f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"',
        f'data-glaze-ui="{GLAZE_VERSION}"',
        'glaze-v1.1.0.css',
        'name="viewport"',
    ]:
        if marker not in text:
            errors.append(f"{page.relative_to(ROOT)} missing source-native V1.1 marker: {marker}")
    for stale in (
        'data-glaze-ui="1.5.0"',
        'data-glaze-ui="2.0.0"',
        'data-glaze-ui="2.1.0"',
        'data-glaze-ui="2.2.0"',
        'goreecloud-glaze-ui" content="1.5.0"',
        'goreecloud-glaze-ui" content="2.0.0"',
        'goreecloud-glaze-ui" content="2.1.0"',
        'goreecloud-glaze-ui" content="2.2.0"',
    ):
        if stale in text:
            errors.append(f"{page.relative_to(ROOT)} still activates a superseded Glaze UI contract: {stale}")
    if "raw.githubusercontent.com" in text:
        errors.append(f"{page.relative_to(ROOT)} must not load remote Glaze UI at runtime")


for page in [*ROOT_PAGES, *CHILD_PAGES]:
    validate_page(page)

text = CONFORMANCE.read_text(encoding="utf-8") if CONFORMANCE.is_file() else ""
for marker in [
    "Target GLAZE UI version: **V1.1 / 1.1.0**",
    "GoreeCloud/goreecloud-glaze-ui",
    GLAZE_PROMOTION_REVISION,
    "same-origin",
    "48px",
    "56px",
    "Rendered/production acceptance",
    "No production GLAZE UI exception",
]:
    if marker not in text:
        errors.append(f"Conformance marker missing: {marker}")

if errors:
    print("GLAZE UI V1.1 validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print("GLAZE UI V1.1 / 1.1.0 Stable source validation passed across Main, Projects, Roadmap, Blog, and Archive HTML surfaces.")
