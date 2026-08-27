#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVISION = "2c5078410d022eba683c8e029bc3cafe773df0b7"
BUNDLE = ROOT / "css/glaze-ui-1.5.0.css"
PAGES = [ROOT / n for n in ("index.html","repositories.html","privacy.html","security.html","404.html")]
CONFORMANCE = ROOT / "docs/glaze-ui-conformance.md"
LAYERS = ['glaze.css', 'glaze.controls.css', 'glaze.expressive.css', 'glaze.formfactors.css', 'glaze.accessibility.css', 'glaze.color.css', 'glaze.motion.css', 'glaze.materials.css', 'glaze.layout.css', 'glaze.states.css']
errors = []

if not BUNDLE.is_file(): errors.append("Stable 1.5 bundle is missing")
else:
    css = BUNDLE.read_text(encoding="utf-8")
    for marker in ["Glaze UI 1.5.0 Stable", REVISION, "GoreeCloud public-site 1.5 integration", "prefers-reduced-motion", "backdrop-filter"]:
        if marker not in css: errors.append(f"Stable bundle marker missing: {marker}")
    for layer in LAYERS:
        if f"===== {layer} =====" not in css: errors.append(f"Stable layer missing: {layer}")

for page in PAGES:
    text = page.read_text(encoding="utf-8")
    for marker in ['name="goreecloud-glaze-ui" content="1.5.0"', 'data-glaze-ui="1.5.0"', 'glaze-canvas', 'name="viewport"', 'name="color-scheme"']:
        if marker not in text: errors.append(f"{page.name} missing 1.5 page marker: {marker}")
    if "http://raw.githubusercontent.com" in text or "https://raw.githubusercontent.com" in text:
        errors.append(f"{page.name} must not load remote Glaze UI at runtime")

text = CONFORMANCE.read_text(encoding="utf-8") if CONFORMANCE.is_file() else ""
for marker in ["Target Glaze UI version: **1.5.0**", "GoreeCloud/goreecloud-glaze-ui", REVISION, "same-origin", "Candidate wearable", "No production Glaze UI exception"]:
    if marker not in text: errors.append(f"Conformance marker missing: {marker}")

if errors:
    print("Glaze UI 1.5 validation failed:")
    for error in errors: print(f"  - {error}")
    sys.exit(1)
print("Glaze UI 1.5.0 Stable validation passed across the five goreecloud-website public surfaces.")
