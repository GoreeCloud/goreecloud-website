#!/usr/bin/env python3
from pathlib import Path
import re

SITE=Path(__file__).resolve().parent
required=["index.html","404.html","_headers","assets/app.js","assets/public-refresh.js","assets/styles.css","assets/goreecloud-logo.svg","assets/glaze-ui-mark.svg","assets/privacy-shield-icon.svg","assets/wardveil-security-icon.svg"]
for name in required:
    if not (SITE/name).is_file(): raise SystemExit(f"missing Projects site file: {name}")
html=(SITE/"index.html").read_text(encoding="utf-8")
js=(SITE/"assets/app.js").read_text(encoding="utf-8")
refresh=(SITE/"assets/public-refresh.js").read_text(encoding="utf-8")
combined=html+js+refresh
headers=(SITE/"_headers").read_text(encoding="utf-8")
for needle in [
    "Suite applications",
    "Shared foundations",
    "Glaze UI 1.5",
    "Privacy Shield",
    "Wardveil Security",
    "Everkeep",
    "GoreeCloud Mesh",
    "GoreeCloud AI",
    "GoreeCloud Code",
    "GoreeCloud Documents",
    "GoreeCloud Messenger",
    "GoreeCloud Gateway",
    "GoreeCloud Quill",
    "Forgejo is the initial replaceable infrastructure foundation",
    "Design Center",
    "Privacy Center",
    "Security Center",
    "Continuity Center",
    "Mesh Center",
    "GoreeCloud Calendar",
    "GoreeCloud Keyboard",
    "GoreeCloud Mail",
    "GoreeCloud Music",
    "GoreeCloud Photos",
    "GoreeCloud Vault Server",
    "GoreeCloud Suite",
    "GoreeCloud Firefox Extensions",
    "GoreeCloud Autobiography",
    "GoreeCloud Waypoint",
    "GoreeCloud Drive",
    "GoreeCloud Sync",
    "GoreeCloud Location",
    "GoreeCloud Launcher",
    "GoreeCloud Video",
    "Milestone 1 · persistent node CRUD",
    "native client foundation merged",
    "Fold identity approved",
]:
    if needle not in combined: raise SystemExit(f"current portfolio marker missing: {needle}")
if js.count("kind:'Application'") != 33: raise SystemExit("Projects base catalog must contain exactly 33 Suite applications before current portfolio augmentation")
if js.count("kind:'Foundation'") != 6: raise SystemExit("Projects base catalog must contain exactly 6 shared foundations before current portfolio augmentation")
for augmented in ["GoreeCloud AI","GoreeCloud Code","GoreeCloud Documents","GoreeCloud Messenger","GoreeCloud Gateway","GoreeCloud Quill","GoreeCloud Mesh"]:
    if f"entry.name==='{augmented}'" not in refresh:
        raise SystemExit(f"Projects August 27 augmentation missing: {augmented}")
for stale in [
    "Gitea is the planned permanent",
    "planned permanent source-control authority",
    "Glaze UI 1.4</strong><span>Current Stable baseline",
]:
    if stale in html+refresh:
        raise SystemExit(f"superseded Projects direction remains public: {stale}")
for icon in ["/assets/goreecloud-logo.svg","/assets/glaze-ui-mark.svg","/assets/privacy-shield-icon.svg","/assets/wardveil-security-icon.svg"]:
    if icon not in combined: raise SystemExit(f"approved identity artwork is not used: {icon}")
fold=(SITE/"assets/glaze-ui-mark.svg").read_text(encoding="utf-8")
if "Official Glaze UI Fold mark" not in fold or 'viewBox="0 0 512 512"' not in fold:
    raise SystemExit("Projects Glaze UI artwork must use the approved Fold identity")
for src in re.findall(r'src=["\']([^"\']+)',html):
    if src.startswith("http:") or src.startswith("https:"): raise SystemExit(f"remote browser resource prohibited: {src}")
for directive in ["Content-Security-Policy:","Permissions-Policy:","X-Content-Type-Options: nosniff"]:
    if directive not in headers: raise SystemExit(f"security header missing: {directive}")
if "localStorage" not in js or "data-theme-choice" not in html: raise SystemExit("local appearance preference contract missing")
release_boundary="Public source, a successful build, active development, a release candidate, or a platform identity does not automatically establish production acceptance or protection."
if release_boundary not in html: raise SystemExit("source-versus-production boundary missing")
if "observe(projectGrid,{childList:true,subtree:true})" in refresh:
    raise SystemExit("Projects refresh must not observe its own descendant text mutations")
if "observe(projectGrid,{childList:true})" not in refresh:
    raise SystemExit("Projects refresh must observe only direct card-list replacement")
print("GoreeCloud Projects current portfolio validation passed")
