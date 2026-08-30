#!/usr/bin/env python3
from pathlib import Path
import sys

from glaze_ui_2 import GLAZE_PROMOTION_REVISION, GLAZE_VERSION, apply_glaze_ui_2

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "css/glaze-ui-2.0.0.css"
ROOT_PAGES = [ROOT / n for n in ("index.html","repositories.html","privacy.html","security.html","404.html")]
CHILD_PAGES = [
    ROOT / "sites/projects/index.html", ROOT / "sites/projects/404.html",
    ROOT / "sites/roadmap/index.html", ROOT / "sites/roadmap/404.html",
    ROOT / "sites/blog/index.html", ROOT / "sites/blog/404.html",
    ROOT / "sites/archive/index.html", ROOT / "sites/archive/404.html",
]
CHILD_BUNDLES = [
    ROOT / "sites/projects/assets/glaze-ui-2.0.0.css",
    ROOT / "sites/roadmap/glaze-ui-2.0.0.css",
    ROOT / "sites/blog/glaze-ui-2.0.0.css",
    ROOT / "sites/archive/glaze-ui-2.0.0.css",
]
CONFORMANCE = ROOT / "docs/glaze-ui-conformance.md"
errors = []

for bundle in [BUNDLE, *CHILD_BUNDLES]:
    if not bundle.is_file():
        errors.append(f"Glaze UI 2.0 bundle is missing: {bundle.relative_to(ROOT)}")
        continue
    css = bundle.read_text(encoding="utf-8")
    for marker in ["Glaze UI 2.0.0 Stable integration", GLAZE_PROMOTION_REVISION, "prefers-reduced-motion", "prefers-reduced-transparency", "forced-colors"]:
        if marker not in css: errors.append(f"{bundle.relative_to(ROOT)} missing 2.0 marker: {marker}")

for page in ROOT_PAGES:
    text = apply_glaze_ui_2(page.read_text(encoding="utf-8"))
    for marker in [f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"', f'data-glaze-ui="{GLAZE_VERSION}"', 'glaze-canvas', 'name="viewport"']:
        if marker not in text: errors.append(f"{page.name} missing normalized 2.0 marker: {marker}")
    if 'data-glaze-ui="1.5.0"' in text: errors.append(f"{page.name} still activates Glaze UI 1.5 after normalization")
    if "raw.githubusercontent.com" in text: errors.append(f"{page.name} must not load remote Glaze UI at runtime")

for page in CHILD_PAGES:
    text = page.read_text(encoding="utf-8")
    for marker in [f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"', f'data-glaze-ui="{GLAZE_VERSION}"', 'glaze-canvas', 'name="viewport"']:
        if marker not in text: errors.append(f"{page.relative_to(ROOT)} missing 2.0 marker: {marker}")
    if 'data-glaze-ui="1.5.0"' in text: errors.append(f"{page.relative_to(ROOT)} still activates Glaze UI 1.5")
    if "raw.githubusercontent.com" in text: errors.append(f"{page.relative_to(ROOT)} must not load remote Glaze UI at runtime")

text = CONFORMANCE.read_text(encoding="utf-8") if CONFORMANCE.is_file() else ""
for marker in ["Target Glaze UI version: **2.0.0**", "GoreeCloud/goreecloud-glaze-ui", GLAZE_PROMOTION_REVISION, "same-origin", "48px", "Rendered/production acceptance", "No production Glaze UI exception"]:
    if marker not in text: errors.append(f"Conformance marker missing: {marker}")

if errors:
    print("Glaze UI 2.0 validation failed:")
    for error in errors: print(f"  - {error}")
    sys.exit(1)
print("Glaze UI 2.0.0 Stable source validation passed across Main, Projects, Roadmap, Blog, and Archive surfaces.")