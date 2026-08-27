#!/usr/bin/env python3
from pathlib import Path
import re

SITE=Path(__file__).resolve().parent
required=["index.html","404.html","_headers","assets/app.js","assets/public-refresh.js","assets/icon-refresh.js","assets/styles.css","assets/mobile-refresh.css","assets/goreecloud-logo.svg","assets/glaze-ui-mark.svg","assets/everkeep.svg","assets/privacy-shield-icon.svg","assets/wardveil-security-icon.svg"]
for name in required:
    if not (SITE/name).is_file(): raise SystemExit(f"missing Projects site file: {name}")
html=(SITE/"index.html").read_text(encoding="utf-8")
js=(SITE/"assets/app.js").read_text(encoding="utf-8")
refresh=(SITE/"assets/public-refresh.js").read_text(encoding="utf-8")
icons=(SITE/"assets/icon-refresh.js").read_text(encoding="utf-8")
mobile=(SITE/"assets/mobile-refresh.css").read_text(encoding="utf-8")
combined=html+js+refresh+icons
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
for icon in ["/assets/goreecloud-logo.svg","/assets/glaze-ui-mark.svg","/assets/everkeep.svg","/assets/privacy-shield-icon.svg","/assets/wardveil-security-icon.svg"]:
    if icon not in combined: raise SystemExit(f"approved identity artwork is not used: {icon}")
facet=(SITE/"assets/glaze-ui-mark.svg").read_text(encoding="utf-8")
if 'viewBox="0 0 64 64"' not in facet or "Three interlocking translucent interface facets" not in facet:
    raise SystemExit("Projects Glaze UI artwork must use the current Facet identity")
everkeep=(SITE/"assets/everkeep.svg").read_text(encoding="utf-8")
if "fixed preserved keystone" not in everkeep or 'viewBox="0 0 64 64"' not in everkeep:
    raise SystemExit("Projects Everkeep artwork must use the repository-owned keystone identity")
if '<a href="https://everkeep.goreecloud.com/"><img src="/assets/goreecloud-logo.svg"' in html:
    raise SystemExit("Everkeep must not use the GoreeCloud platform logo")
if '<strong>GoreeCloud Mesh</strong>' in html and 'class="mesh-mark"' not in html:
    raise SystemExit("Mesh must use a distinct coordination mark rather than the GoreeCloud platform logo")
for src in re.findall(r'src=["\']([^"\']+)',html):
    if src.startswith("http:") or src.startswith("https:"): raise SystemExit(f"remote static browser resource prohibited: {src}")
for directive in ["Content-Security-Policy:","Permissions-Policy:","X-Content-Type-Options: nosniff"]:
    if directive not in headers: raise SystemExit(f"security header missing: {directive}")
if "img-src 'self' data: https://www.goreecloud.com" not in headers:
    raise SystemExit("Projects CSP must allow only the canonical first-party Website origin for remote Suite artwork")
if "raw.githubusercontent.com" in headers+icons or "githubusercontent.com" in headers+icons:
    raise SystemExit("Projects must not make visitor browsers fetch repository artwork from GitHub")
if "localStorage" not in js or "data-theme-choice" not in html: raise SystemExit("local appearance preference contract missing")
release_boundary="Public source, a successful build, active development, a release candidate, or a platform identity does not automatically establish production acceptance or protection."
if release_boundary not in html: raise SystemExit("source-versus-production boundary missing")
if "MutationObserver" in refresh:
    raise SystemExit("Projects refresh must update the data model without a DOM MutationObserver")
for needle in ["entry.status=update[0]","entry.role=update[1]","entry.model=update[2]","render();"]:
    if needle not in refresh:
        raise SystemExit(f"Projects data-model refresh contract missing: {needle}")
for needle in ["canonicalSuiteIconBase='https://www.goreecloud.com/assets/suite/'","'goreecloud-manager':'manager.svg'","'goreecloud-browser':'browser.svg'","'goreecloud-ai':'ai.svg'","'goreecloud-code':'code.svg'","'goreecloud-gateway':'gateway.svg'","entry.repo==='goreecloud-everkeep'","entry.repo==='goreecloud-mesh'","projectMonogram(entry.name)"]:
    if needle not in icons:
        raise SystemExit(f"Projects repository identity mapping missing: {needle}")
if icons.count("canonicalSuiteIconBase") < 2 or len(re.findall(r"'goreecloud-[^']+':'[^']+\.svg'",icons)) < 30:
    raise SystemExit("Projects must map the established application portfolio to canonical per-product artwork")
for needle in ["min-height:44px","overflow-x:hidden",".card-meta{flex-wrap:wrap","@media(max-width:380px)",".mesh-mark{"]:
    if needle not in mobile:
        raise SystemExit(f"Projects mobile hardening marker missing: {needle}")
for stylesheet in ["/assets/mobile-refresh.css?v=20260827-mobile1"]:
    if stylesheet not in html:
        raise SystemExit(f"Projects mobile stylesheet reference missing: {stylesheet}")
for script in ["/assets/app.js?v=20260827-cache2","/assets/public-refresh.js?v=20260827-cache2","/assets/icon-refresh.js?v=20260827-icons1"]:
    if script not in html:
        raise SystemExit(f"Projects cache-busted script reference missing: {script}")
if "Cache-Control: public, max-age=0, must-revalidate" not in headers:
    raise SystemExit("Projects mutable assets must revalidate instead of remaining browser-fresh for a day")
for stale_cache in ["max-age=86400","stale-while-revalidate"]:
    if stale_cache in headers:
        raise SystemExit(f"Projects stale asset cache policy remains: {stale_cache}")
print("GoreeCloud Projects current portfolio validation passed")
