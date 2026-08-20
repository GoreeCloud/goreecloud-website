#!/usr/bin/env python3
from pathlib import Path
import re

SITE=Path(__file__).resolve().parent
required=["index.html","404.html","_headers","assets/app.js","assets/styles.css","assets/goreecloud-logo.svg"]
for name in required:
    if not (SITE/name).is_file(): raise SystemExit(f"missing Projects site file: {name}")
html=(SITE/"index.html").read_text(encoding="utf-8")
js=(SITE/"assets/app.js").read_text(encoding="utf-8")
headers=(SITE/"_headers").read_text(encoding="utf-8")
for needle in ["22","Suite applications","3","Shared foundations","Glaze UI 1.3","Privacy Shield","Wardveil Security","GoreeCloud Calendar","GoreeCloud Keyboard"]:
    if needle not in html+js: raise SystemExit(f"current portfolio marker missing: {needle}")
if js.count("kind:'Application'") != 22: raise SystemExit("Projects catalog must contain exactly 22 Suite applications")
if js.count("kind:'Foundation'") != 3: raise SystemExit("Projects catalog must contain exactly 3 shared foundations")
for marker in [
    "https://raw.githubusercontent.com/GoreeCloud/glaze-ui/main/branding",
    "/icons/glaze-ui/glaze-ui-symbol.svg",
    "/identities/privacy-shield/symbol.svg",
    "/identities/wardveil-security/emblem.svg",
    "/applications/${entry.repo}/symbol.svg",
    "/assets/goreecloud-logo.svg",
]:
    if marker not in html+js: raise SystemExit(f"canonical identity artwork contract missing: {marker}")
for obsolete in ["/assets/glaze-ui-mark.svg","/assets/privacy-shield-icon.svg","/assets/wardveil-security-icon.svg"]:
    if obsolete in html+js: raise SystemExit(f"obsolete website-owned identity artwork still referenced: {obsolete}")
for src in re.findall(r'src=["\']([^"\']+)',html):
    if src.startswith("http:") or src.startswith("https:"): raise SystemExit(f"remote static HTML resource prohibited: {src}")
for directive in ["Content-Security-Policy:","Permissions-Policy:","X-Content-Type-Options: nosniff"]:
    if directive not in headers: raise SystemExit(f"security header missing: {directive}")
if "img-src 'self' data: https://raw.githubusercontent.com" not in headers:
    raise SystemExit("Projects CSP must allow only the canonical external artwork image source")
if "localStorage" not in js or "data-theme-choice" not in html: raise SystemExit("local appearance preference contract missing")
if "Repository visibility and development status are shown independently from production acceptance" not in html: raise SystemExit("source-versus-production boundary missing")
print("GoreeCloud Projects current portfolio validation passed")
