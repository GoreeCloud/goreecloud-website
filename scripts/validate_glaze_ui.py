#!/usr/bin/env python3
from pathlib import Path
import sys

from glaze_ui_2 import GLAZE_PROMOTION_REVISION, GLAZE_VERSION, apply_glaze_ui_2

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "css/glaze-ui-2.1.0.css"
# Privacy, Security, and the error page are now source-native Glaze UI 2.1.
# Main and Repositories still pass through the compatibility normalizer while
# their larger canonical templates are being replaced without changing the
# accepted generated public hierarchy.
SOURCE_NATIVE_ROOT_PAGES = [ROOT / n for n in ("privacy.html", "security.html", "404.html")]
COMPAT_ROOT_PAGES = [ROOT / n for n in ("index.html", "repositories.html")]
CHILD_PAGES = [
    ROOT / "sites/projects/index.html", ROOT / "sites/projects/404.html",
    ROOT / "sites/roadmap/index.html", ROOT / "sites/roadmap/404.html",
    ROOT / "sites/blog/index.html", ROOT / "sites/blog/404.html",
    ROOT / "sites/archive/index.html", ROOT / "sites/archive/404.html",
]
CHILD_BUNDLES = [
    ROOT / "sites/projects/assets/glaze-ui-2.1.0.css",
    ROOT / "sites/roadmap/glaze-ui-2.1.0.css",
    ROOT / "sites/blog/glaze-ui-2.1.0.css",
    ROOT / "sites/archive/glaze-ui-2.1.0.css",
]
CONFORMANCE = ROOT / "docs/glaze-ui-conformance.md"
errors = []

bundle_markers = [
    "Glaze UI 2.1.0 Stable integration",
    GLAZE_PROMOTION_REVISION,
    "Content is solid. Interaction is glazed.",
    "--glaze-touch-min:48px",
    "--glaze-touch-assisted:56px",
    "data-glaze-density=comfortable",
    "data-glaze-density=compact",
    "data-glaze-performance=reduced",
    "data-glaze-large-text=true",
    "prefers-reduced-motion",
    "prefers-reduced-transparency",
    "forced-colors:active",
]
for bundle in [BUNDLE, *CHILD_BUNDLES]:
    if not bundle.is_file():
        errors.append(f"Glaze UI 2.1 bundle is missing: {bundle.relative_to(ROOT)}")
        continue
    css = bundle.read_text(encoding="utf-8")
    for marker in bundle_markers:
        if marker not in css:
            errors.append(f"{bundle.relative_to(ROOT)} missing 2.1 marker: {marker}")


def validate_page(page: Path, text: str, *, normalized: bool) -> None:
    mode = "normalized" if normalized else "source-native"
    for marker in [
        f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"',
        f'data-glaze-ui="{GLAZE_VERSION}"',
        'glaze-canvas',
        'name="viewport"',
    ]:
        if marker not in text:
            errors.append(f"{page.relative_to(ROOT)} missing {mode} 2.1 marker: {marker}")
    for stale in ('data-glaze-ui="1.5.0"', 'data-glaze-ui="2.0.0"'):
        if stale in text:
            errors.append(f"{page.relative_to(ROOT)} still activates a superseded Glaze UI bundle in {mode} form: {stale}")
    if "raw.githubusercontent.com" in text:
        errors.append(f"{page.relative_to(ROOT)} must not load remote Glaze UI at runtime")


for page in SOURCE_NATIVE_ROOT_PAGES:
    validate_page(page, page.read_text(encoding="utf-8"), normalized=False)

for page in COMPAT_ROOT_PAGES:
    validate_page(page, apply_glaze_ui_2(page.read_text(encoding="utf-8")), normalized=True)

for page in CHILD_PAGES:
    validate_page(page, page.read_text(encoding="utf-8"), normalized=False)

text = CONFORMANCE.read_text(encoding="utf-8") if CONFORMANCE.is_file() else ""
for marker in [
    "Target Glaze UI version: **2.1.0**",
    "GoreeCloud/goreecloud-glaze-ui",
    GLAZE_PROMOTION_REVISION,
    "same-origin",
    "Content is solid. Interaction is glazed.",
    "48px general interaction floor",
    "56px Touch Assistance floor",
    "Rendered/production acceptance",
    "No production Glaze UI exception",
]:
    if marker not in text:
        errors.append(f"Conformance marker missing: {marker}")

if errors:
    print("Glaze UI 2.1 validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print(
    "Glaze UI 2.1.0 Stable validation passed: Privacy, Security, 404, Projects, Roadmap, Blog, and Archive are source-native; Main and Repositories remain compatibility-normalized pending canonical-template replacement."
)
