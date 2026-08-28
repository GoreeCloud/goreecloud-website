#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re

SITE=Path(__file__).resolve().parent
ROOT=SITE.parents[1]
required=["index.html","404.html","README.md","_headers","assets/app.js","assets/public-refresh.js","assets/icon-refresh.js","assets/styles.css","assets/mobile-refresh.css","assets/goreecloud-logo.svg","assets/glaze-ui-mark.svg","assets/everkeep.svg","assets/privacy-shield-icon.svg","assets/wardveil-security-icon.svg"]
for name in required:
    if not (SITE/name).is_file(): raise SystemExit(f"missing Projects site file: {name}")
html=(SITE/"index.html").read_text(encoding="utf-8")
js=(SITE/"assets/app.js").read_text(encoding="utf-8")
refresh=(SITE/"assets/public-refresh.js").read_text(encoding="utf-8")
icons=(SITE/"assets/icon-refresh.js").read_text(encoding="utf-8")
mobile=(SITE/"assets/mobile-refresh.css").read_text(encoding="utf-8")
readme=(SITE/"README.md").read_text(encoding="utf-8")
combined=html+js+refresh+icons+readme
headers=(SITE/"_headers").read_text(encoding="utf-8")

def git_blob_sha(path: Path) -> str:
    data=path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

for needle in [
    "Suite applications","Shared foundations","Glaze UI 1.5","Privacy Shield","Wardveil Security","Everkeep","GoreeCloud Mesh",
    "GoreeCloud AI","GoreeCloud Code","GoreeCloud Documents","GoreeCloud Messenger","GoreeCloud Gateway","GoreeCloud Quill",
    "Forgejo is the initial replaceable infrastructure foundation","Design Center","Privacy Center","Security Center","Continuity Center","Mesh Center",
    "GoreeCloud Calendar","GoreeCloud Keyboard","GoreeCloud Mail","GoreeCloud Music","GoreeCloud Photos","GoreeCloud Vault Server","GoreeCloud Suite",
    "GoreeCloud Firefox Extensions","GoreeCloud Autobiography","GoreeCloud Waypoint","GoreeCloud Drive","GoreeCloud Sync","GoreeCloud Location","GoreeCloud Launcher","GoreeCloud Video",
    "Milestone 1 · persistent node CRUD","native client foundation merged",
]:
    if needle not in combined: raise SystemExit(f"current portfolio marker missing: {needle}")
if js.count("kind:'Application'") != 33: raise SystemExit("Projects base catalog must contain exactly 33 Suite applications before current portfolio augmentation")
if js.count("kind:'Foundation'") != 6: raise SystemExit("Projects base catalog must contain exactly 6 shared foundations before current portfolio augmentation")
for augmented in ["GoreeCloud AI","GoreeCloud Code","GoreeCloud Documents","GoreeCloud Messenger","GoreeCloud Gateway","GoreeCloud Quill","GoreeCloud Mesh"]:
    if f"entry.name==='{augmented}'" not in refresh: raise SystemExit(f"Projects August 27 augmentation missing: {augmented}")
for stale in ["Gitea is the planned permanent","planned permanent source-control authority","Glaze UI 1.4</strong><span>Current Stable baseline"]:
    if stale in html+refresh: raise SystemExit(f"superseded Projects direction remains public: {stale}")

branding_repo="GoreeCloud/goreecloud-branding-assets"
if f"brandingAuthority='{branding_repo}'" not in icons: raise SystemExit("Projects identity mapping must name the unified branding repository as authority")
for needle in [branding_repo,"catalog.json","synchronized publication derivatives","GoreeCloud Mesh has no approved canonical artwork","remains text-only"]:
    if needle not in readme: raise SystemExit(f"Projects branding-authority documentation missing: {needle}")

system_blobs={
    "assets/goreecloud-logo.svg":"082936062de7839148db89ea3ab4e86ff71341b0",
    "assets/glaze-ui-mark.svg":"7756ca8f04a588286e05e37e9a141dbea7f1965d",
    "assets/privacy-shield-icon.svg":"62b10029d4104d0235afe634c21f55d0a826a63d",
    "assets/wardveil-security-icon.svg":"fb3d643cca5477c3f8d4e03ce10a3458fd12f407",
    "assets/everkeep.svg":"5f70a483e06147193944c816291d42774a8648b2",
}
for relative,expected in system_blobs.items():
    actual=git_blob_sha(SITE/relative)
    if actual!=expected: raise SystemExit(f"Projects synchronized branding derivative drifted: {relative}: expected {expected}, got {actual}")

product_blobs={
    "ai.svg":"1cbe04748f50cb843eef0cbb7233e2769efa275a","backup.svg":"6e8f2bc02beb4679ed99f2db787e7dc6b4a0f28f","bookmarks.svg":"2e9947924708df10844a3a81f47585c4da6b931a",
    "browser.svg":"2a81cc68cb8c1831dfd7bec6c3d0b14e2f421f1f","calendar.svg":"369c42a204c6b130f49f37f91ec0569256a2c19e","changelogs.svg":"958878ecde32cadd3e646c606534638e4f5e01fb",
    "code.svg":"579f0416bd2839bf40e87de7751e319d80bd0bf9","contacts.svg":"22e818436ebef790333fcf56efa79d5bdfff5c88","dns.svg":"99c8e09f4e8e65bde57e671e4fd4beb1bd2fcb4a",
    "documents.svg":"58200e22b053fe17a2d80cc69e9908a3a2987a34","drive.svg":"a931ebc4e657895128adb6391eb4665c99e74c4a","feed.svg":"3464434f08f1c200621900ae86a00d04e812a5fb",
    "gallery.svg":"ff3085d705b567283dd566a3c02e667866458012","gateway.svg":"f8a94f6a6ff5dece3f93bc15531ee5845fa3db61","identity.svg":"dc8287e385f86767f0105c48a8f234d8440d7623",
    "keyboard.svg":"9dea51ca5853dc0faf41d94fbc12ee810480c472","launcher.svg":"d6768114e689058f1c911beca4050f33c96bd7c2","location.svg":"ceb93b6d814c80ece0929022eb5edcdfbc346e2d",
    "mail.svg":"6fcc489ccfc6348514755a9a052dc413ee17ccde","manager.svg":"024d82d5b5911e426216dfbd6a19d95cd6d71fc3","memos.svg":"eb9396c3a1891f6afb96849a29110c6f35e65f19",
    "messenger.svg":"01102af91a43e100c66877489b94929165ec0430","monitor.svg":"f31c9abab93f1e9e45e34e0eef411705228d1a66","music.svg":"74d7726676faf6447116153da53790e4c272e03c",
    "network.svg":"7457cd187d65887189150016b44c28af279635e5","notes.svg":"9618b85e29f89990320cc3a101f0f3bf6fffc89f","notify.svg":"1ce1239cd2319a0f96232b1562ec1f6e68d43815",
    "photos.svg":"7cce0f2f1b1fad209577a4e0294f0b767fd06b14","search.svg":"fc441c75d6cc2bd0d88a80d77b60994b34475670","sync.svg":"91e40049d146881df6befe32d836e260e2bd908c",
    "tasks.svg":"180e162c81b34a0b1dffd20031b36cbb874e2f61","terminal.svg":"fd28f49fc0dd67e2f3e31480942d555914e8fc5b","vault.svg":"c34edae0c57a6bac002fb0f940de7ae26cf1450e",
    "video.svg":"0fbffa1c5210b5da3934c4615b40d59303c0844c",
}
for filename,expected in product_blobs.items():
    path=ROOT/"assets"/"suite"/filename
    if not path.is_file(): raise SystemExit(f"missing synchronized Suite branding derivative: {path.relative_to(ROOT)}")
    actual=git_blob_sha(path)
    if actual!=expected: raise SystemExit(f"Suite branding derivative drifted from unified catalog: {filename}: expected {expected}, got {actual}")

for source in ["products/manager/app-icon.svg","products/browser/app-icon.svg","products/ai/app-icon.svg","systems/glaze-ui/glaze-ui-mark.svg","systems/everkeep/everkeep.svg","systems/wardveil-security/wardveil-security-icon.svg"]:
    if source not in icons: raise SystemExit(f"Projects canonical branding source mapping missing: {source}")
if len(re.findall(r"'goreecloud-[^']+':\['products/[^']+/app-icon\.svg','[^']+\.svg'\]",icons)) < 30:
    raise SystemExit("Projects must map established products to approved unified-catalog artwork")
for forbidden in ["projectMonogram","meshSymbol","data:image/svg+xml"]:
    if forbidden in icons: raise SystemExit(f"Projects must not fabricate branding artwork: {forbidden}")
if "'goreecloud-mesh':[null,null,'text-only-pending-approved-artwork']" not in icons:
    raise SystemExit("Projects Mesh must follow the branding catalog text-only pending-artwork state")
if 'class="text-only-system"' not in html or "Mesh Center · artwork pending approval" not in html:
    raise SystemExit("Projects Mesh foundation identity must be text-only and disclose pending artwork")
if 'class="mesh-mark"' in html or ".mesh-mark{" in mobile:
    raise SystemExit("Projects must not publish an unapproved Mesh mark")
if "article.querySelector('.project-icon')?.remove()" not in icons or "entry.icon=''" not in icons:
    raise SystemExit("Projects must remove fallback platform logos from entries without approved artwork")

for src in re.findall(r'src=["\']([^"\']+)',html):
    if src.startswith("http:") or src.startswith("https:"): raise SystemExit(f"remote static browser resource prohibited in HTML: {src}")
for directive in ["Content-Security-Policy:","Permissions-Policy:","X-Content-Type-Options: nosniff"]:
    if directive not in headers: raise SystemExit(f"security header missing: {directive}")
if "img-src 'self' https://www.goreecloud.com" not in headers: raise SystemExit("Projects CSP must allow only self plus the first-party Website publication origin for imagery")
for forbidden in ["data:","raw.githubusercontent.com","githubusercontent.com"]:
    if forbidden in headers+icons: raise SystemExit(f"Projects image provenance policy must not allow or reference: {forbidden}")
if "localStorage" not in js or "data-theme-choice" not in html: raise SystemExit("local appearance preference contract missing")
release_boundary="Public source, a successful build, active development, a release candidate, or a platform identity does not automatically establish production acceptance or protection."
if release_boundary not in html: raise SystemExit("source-versus-production boundary missing")
if "MutationObserver" in refresh: raise SystemExit("Projects refresh must update the data model without a DOM MutationObserver")
for needle in ["entry.status=update[0]","entry.role=update[1]","entry.model=update[2]","render();"]:
    if needle not in refresh: raise SystemExit(f"Projects data-model refresh contract missing: {needle}")
for needle in ["min-height:44px","overflow-x:hidden",".card-meta{flex-wrap:wrap","@media(max-width:380px)",".card-head.text-only-brand",".foundation-strip>a.text-only-system"]:
    if needle not in mobile: raise SystemExit(f"Projects mobile hardening marker missing: {needle}")
for stylesheet in ["/assets/mobile-refresh.css?v=20260827-mobile2"]:
    if stylesheet not in html: raise SystemExit(f"Projects mobile stylesheet reference missing: {stylesheet}")
for script in ["/assets/app.js?v=20260827-cache2","/assets/public-refresh.js?v=20260827-cache2","/assets/icon-refresh.js?v=20260827-icons2"]:
    if script not in html: raise SystemExit(f"Projects cache-busted script reference missing: {script}")
if "Cache-Control: public, max-age=0, must-revalidate" not in headers: raise SystemExit("Projects mutable assets must revalidate instead of remaining browser-fresh for a day")
for stale_cache in ["max-age=86400","stale-while-revalidate"]:
    if stale_cache in headers: raise SystemExit(f"Projects stale asset cache policy remains: {stale_cache}")
print("GoreeCloud Projects current portfolio and unified branding validation passed")
