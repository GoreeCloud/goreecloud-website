#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re

SITE = Path(__file__).resolve().parent
ROOT = SITE.parents[1]

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
# app.js is the intentionally stable base catalog. public-refresh.js applies
# current direction before the final portfolio render; stale-current checks
# therefore target the actual current-facing HTML/refresh/documentation layer.
active_direction = html + refresh + readme


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


for needle in [
    "Suite applications", "Shared foundations", "Glaze UI 2.1", "Privacy Shield",
    "Wardveil Security", "Everkeep", "GoreeCloud Mesh", "GoreeCloud Identity",
    "GoreeCloud AI", "GoreeCloud Code", "GoreeCloud Documents", "GoreeCloud Messenger",
    "GoreeCloud Gateway", "GoreeCloud Quill", "GoreeCloud File Manager", "GoreeCloud Maps",
    "GoreeCloud App Store", "Design Center", "Privacy Center", "Security Center",
    "Continuity Center", "Mesh Center", "Identity Center", "Sentinel Fold", "Weave",
]:
    if needle not in combined:
        raise SystemExit(f"current portfolio marker missing: {needle}")

for page_name, page in (("index", html), ("404", error_html)):
    for marker in (
        'name="goreecloud-glaze-ui" content="2.1.0"',
        'data-glaze-ui="2.1.0"',
        "glaze-canvas",
    ):
        if marker not in page:
            raise SystemExit(f"{page_name} missing Glaze UI 2.1 marker: {marker}")
    for stale in ('data-glaze-ui="1.5.0"', 'data-glaze-ui="2.0.0"'):
        if stale in page:
            raise SystemExit(f"{page_name} still activates superseded Glaze UI: {stale}")

for marker in (
    "Glaze UI 2.1.0 Stable integration",
    "c49113eb8b93c267613fdf1bbca1f814495acad7",
    "Content is solid. Interaction is glazed.",
    "--glaze-touch-min:48px",
    "--glaze-touch-assisted:56px",
    "data-glaze-density=compact",
    "data-glaze-performance=reduced",
    "data-glaze-large-text=true",
    "prefers-reduced-motion",
    "prefers-reduced-transparency",
    "forced-colors:active",
):
    if marker not in glaze:
        raise SystemExit(f"Projects Glaze UI 2.1 web-layer marker missing: {marker}")

# Base catalog remains intentionally stable; current additions and status
# corrections are applied by public-refresh.js before the final public render.
if js.count("kind:'Application'") != 33:
    raise SystemExit("Projects base catalog must contain exactly 33 Suite applications before current portfolio augmentation")
if js.count("kind:'Foundation'") != 6:
    raise SystemExit("Projects base catalog must contain exactly 6 shared foundations before current portfolio augmentation")
for current in [
    "GoreeCloud AI", "GoreeCloud Code", "GoreeCloud Documents", "GoreeCloud Messenger",
    "GoreeCloud Gateway", "GoreeCloud Quill", "GoreeCloud Mesh", "GoreeCloud File Manager",
    "GoreeCloud Maps", "GoreeCloud App Store",
]:
    if f"name:'{current}'" not in refresh:
        raise SystemExit(f"Projects current portfolio augmentation missing: {current}")

for stale in [
    "Gitea is the planned permanent",
    "planned permanent source-control authority",
    "1.5.0 current Stable",
    "2.0.0 current Stable",
    "2.1 remains Candidate",
    "Glaze UI 1.4</strong><span>Current Stable baseline",
    "Glaze UI 1.5</strong><span>Current Stable baseline",
    "Glaze UI 2.0</strong><span>Current Stable baseline",
    "Mesh Center · artwork pending approval",
    "GoreeCloud Mesh has no approved canonical artwork",
    "text-only-pending-approved-artwork",
    "recursive resolution, authoritative DNS",
]:
    if stale in active_direction:
        raise SystemExit(f"superseded Projects direction remains public: {stale}")

for required_truth in [
    "2.1.0 current Stable",
    "Identity platform · active development",
    "Recursive resolution remains a separate responsibility",
]:
    if required_truth not in refresh:
        raise SystemExit(f"current Projects truth boundary missing: {required_truth}")

branding_repo = "GoreeCloud/goreecloud-branding-assets"
if f"brandingAuthority='{branding_repo}'" not in icons:
    raise SystemExit("Projects identity mapping must name the unified branding repository as authority")
for needle in [branding_repo, "catalog.json", "synchronized publication derivatives", "Sentinel Fold", "Weave"]:
    if needle not in readme:
        raise SystemExit(f"Projects branding-authority documentation missing: {needle}")

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
    actual = git_blob_sha(SITE / relative)
    if actual != expected:
        raise SystemExit(f"Projects synchronized branding derivative drifted: {relative}: expected {expected}, got {actual}")

for source in [
    "products/manager/app-icon.svg", "products/browser/app-icon.svg", "products/ai/app-icon.svg",
    "systems/glaze-ui/glaze-ui-mark.svg", "systems/everkeep/everkeep.svg",
    "systems/wardveil-security/wardveil-security-icon.svg",
    "systems/goreecloud-mesh/goreecloud-mesh-mark.svg",
]:
    if source not in icons:
        raise SystemExit(f"Projects canonical branding source mapping missing: {source}")
if len(re.findall(r"'goreecloud-[^']+':\['products/[^']+/app-icon\.svg','[^']+\.svg'\]", icons)) < 30:
    raise SystemExit("Projects must map established products to approved unified-catalog artwork")
for forbidden in ["projectMonogram", "meshSymbol", "data:image/svg+xml"]:
    if forbidden in icons:
        raise SystemExit(f"Projects must not fabricate branding artwork: {forbidden}")

if '<img src="/assets/goreecloud-mesh-mark.svg"' not in html or "Mesh Center · Weave" not in html:
    raise SystemExit("Projects Mesh foundation identity must publish the approved Weave mark")
if "Security Center · Sentinel Fold" not in html:
    raise SystemExit("Projects Wardveil foundation identity must identify Sentinel Fold")
if '<img src="/assets/identity.svg"' not in html or "Identity Center" not in html:
    raise SystemExit("Projects must present GoreeCloud Identity as a substantive platform system using approved origin-local artwork")
if "article.querySelector('.project-icon')?.remove()" not in icons or "entry.icon=''" not in icons:
    raise SystemExit("Projects must remove fallback platform logos from entries without approved artwork")

for src in re.findall(r'src=["\']([^"\']+)', html):
    if src.startswith(("http:", "https:")):
        raise SystemExit(f"remote static browser resource prohibited in HTML: {src}")
for directive in ["Content-Security-Policy:", "Permissions-Policy:", "X-Content-Type-Options: nosniff"]:
    if directive not in headers:
        raise SystemExit(f"security header missing: {directive}")
if "img-src 'self' https://www.goreecloud.com" not in headers:
    raise SystemExit("Projects CSP must allow only self plus the first-party Website publication origin for imagery")
for forbidden in ["data:", "raw.githubusercontent.com", "githubusercontent.com"]:
    if forbidden in headers + icons:
        raise SystemExit(f"Projects image provenance policy must not allow or reference: {forbidden}")

if "localStorage" not in js or "data-theme-choice" not in html:
    raise SystemExit("local appearance preference contract missing")
release_boundary = "Public source, a successful build, active development, a release candidate, or a platform identity does not automatically establish production acceptance or protection."
if release_boundary not in html:
    raise SystemExit("source-versus-production boundary missing")
if "MutationObserver" in refresh:
    raise SystemExit("Projects refresh must update the data model without a DOM MutationObserver")
for needle in ["entry.status=update[0]", "entry.role=update[1]", "entry.model=update[2]", "render();"]:
    if needle not in refresh:
        raise SystemExit(f"Projects data-model refresh contract missing: {needle}")
for needle in ["min-height:48px", "overflow-x:hidden", ".card-meta{flex-wrap:wrap", "@media(max-width:380px)"]:
    if needle not in mobile:
        raise SystemExit(f"Projects mobile hardening marker missing: {needle}")

for stylesheet in ["/assets/mobile-refresh.css?v=20260827-mobile2", "/assets/glaze-ui-2.1.0.css"]:
    if stylesheet not in html:
        raise SystemExit(f"Projects stylesheet reference missing: {stylesheet}")
for script in [
    "/assets/app.js?v=20260827-cache2",
    "/assets/public-refresh.js?v=20260830-glaze21",
    "/assets/icon-refresh.js?v=20260828-identities1",
]:
    if script not in html:
        raise SystemExit(f"Projects cache-busted script reference missing: {script}")
if "Cache-Control: public, max-age=0, must-revalidate" not in headers:
    raise SystemExit("Projects mutable assets must revalidate instead of remaining browser-fresh for a day")
for stale_cache in ["max-age=86400", "stale-while-revalidate"]:
    if stale_cache in headers:
        raise SystemExit(f"Projects stale asset cache policy remains: {stale_cache}")

print("GoreeCloud Projects current portfolio, Glaze UI 2.1, six-system model, responsive hardening, and unified branding validation passed")
