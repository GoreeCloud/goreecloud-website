#!/usr/bin/env python3
from pathlib import Path
import hashlib

SITE = Path(__file__).resolve().parent
required = [
    "index.html", "404.html", "README.md", "_headers",
    "assets/app.js", "assets/public-refresh.js", "assets/icon-refresh.js",
    "assets/styles.css", "assets/mobile-refresh.css", "assets/glaze-ui-2.1.0.css",
    "assets/goreecloud-logo.svg", "assets/glaze-ui-mark.svg", "assets/everkeep.svg",
    "assets/privacy-shield-icon.svg", "assets/wardveil-security-icon.svg",
    "assets/goreecloud-mesh-mark.svg", "assets/identity.svg",
]
for name in required:
    if not (SITE / name).is_file():
        raise SystemExit(f"missing Projects site file: {name}")

html = (SITE / "index.html").read_text(encoding="utf-8")
error_html = (SITE / "404.html").read_text(encoding="utf-8")
js = (SITE / "assets/app.js").read_text(encoding="utf-8")
refresh = (SITE / "assets/public-refresh.js").read_text(encoding="utf-8")
icons = (SITE / "assets/icon-refresh.js").read_text(encoding="utf-8")
mobile = (SITE / "assets/mobile-refresh.css").read_text(encoding="utf-8")
readme = (SITE / "README.md").read_text(encoding="utf-8")
glaze = (SITE / "assets/glaze-ui-2.1.0.css").read_text(encoding="utf-8")
headers = (SITE / "_headers").read_text(encoding="utf-8")
combined = html + js + refresh + icons + readme

for needle in ["Glaze UI 2.1", "Privacy Shield", "Wardveil Security", "Everkeep", "GoreeCloud Mesh", "GoreeCloud Identity", "GoreeCloud AI", "GoreeCloud Code", "GoreeCloud Documents", "GoreeCloud Messenger", "GoreeCloud Gateway", "GoreeCloud Quill", "GoreeCloud File Manager", "GoreeCloud Maps", "GoreeCloud App Store", "Design Center", "Privacy Center", "Security Center", "Continuity Center", "Mesh Center", "Identity Center", "Sentinel Fold", "Weave"]:
    if needle not in combined:
        raise SystemExit(f"current portfolio marker missing: {needle}")

for page_name, page in (("index", html), ("404", error_html)):
    for marker in ('name="goreecloud-glaze-ui" content="2.1.0"', 'data-glaze-ui="2.1.0"', "glaze-canvas"):
        if marker not in page:
            raise SystemExit(f"{page_name} missing Glaze UI 2.1 marker: {marker}")
    if 'data-glaze-ui="2.0.0"' in page or 'data-glaze-ui="1.5.0"' in page:
        raise SystemExit(f"{page_name} still activates superseded Glaze UI")

for marker in ["Glaze UI 2.1.0 Stable integration", "c49113eb8b93c267613fdf1bbca1f814495acad7", "Content is solid. Interaction is glazed.", "--glaze-touch-assisted:56px", "data-glaze-density=compact", "data-glaze-performance=reduced", "data-glaze-large-text=true", "prefers-reduced-motion", "prefers-reduced-transparency", "forced-colors:active"]:
    if marker not in glaze:
        raise SystemExit(f"Projects Glaze UI 2.1 marker missing: {marker}")

for current in ["GoreeCloud AI", "GoreeCloud Code", "GoreeCloud Documents", "GoreeCloud Messenger", "GoreeCloud Gateway", "GoreeCloud Quill", "GoreeCloud Mesh", "GoreeCloud File Manager", "GoreeCloud Maps", "GoreeCloud App Store"]:
    if f"name:'{current}'" not in refresh:
        raise SystemExit(f"Projects current portfolio augmentation missing: {current}")
for current_truth in ["2.1.0 current Stable", "Content is solid. Interaction is glazed", "Identity platform · active development", "Recursive resolution remains a separate responsibility"]:
    if current_truth not in refresh:
        raise SystemExit(f"current Projects truth boundary missing: {current_truth}")
for stale in ["2.0.0 current Stable", "2.1 remains Candidate", "planned permanent source-control authority"]:
    if stale in combined:
        raise SystemExit(f"superseded Projects direction remains public: {stale}")

system_blobs = {
    "assets/goreecloud-logo.svg": "082936062de7839148db89ea3ab4e86ff71341b0",
    "assets/glaze-ui-mark.svg": "7756ca8f04a588286e05e37e9a141dbea7f1965d",
    "assets/privacy-shield-icon.svg": "62b10029d4104d0235afe634c21f55d0a826a63d",
    "assets/wardveil-security-icon.svg": "fb3d643cca5477c3f8d4e03ce10a3458fd12f407",
    "assets/everkeep.svg": "5f70a483e06147193944c816291d42774a8648b2",
    "assets/goreecloud-mesh-mark.svg": "0b2c6881668ce319081390b217f6d59b4298dd4d",
    "assets/identity.svg": "dc8287e385f86767f0105c48a8f234d8440d7623",
}
for relative, expected in system_blobs.items():
    data = (SITE / relative).read_bytes()
    actual = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if actual != expected:
        raise SystemExit(f"Projects synchronized branding derivative drifted: {relative}")

for marker in ["Content-Security-Policy:", "Permissions-Policy:", "X-Content-Type-Options: nosniff"]:
    if marker not in headers:
        raise SystemExit(f"security header missing: {marker}")
if "localStorage" not in js or "data-theme-choice" not in html:
    raise SystemExit("local appearance preference contract missing")
for needle in ["min-height:44px", "overflow-x:hidden", ".card-meta{flex-wrap:wrap", "@media(max-width:380px)"]:
    if needle not in mobile:
        raise SystemExit(f"Projects mobile hardening marker missing: {needle}")
for reference in ["/assets/mobile-refresh.css?v=20260827-mobile2", "/assets/app.js?v=20260827-cache2", "/assets/public-refresh.js?v=20260830-glaze21", "/assets/icon-refresh.js?v=20260828-identities1"]:
    if reference not in html:
        raise SystemExit(f"Projects cache-busted resource reference missing: {reference}")
if "Cache-Control: public, max-age=0, must-revalidate" not in headers:
    raise SystemExit("Projects mutable assets must revalidate")

print("GoreeCloud Projects current portfolio, Glaze UI 2.1, six-system model, responsive hardening, and unified branding validation passed")
