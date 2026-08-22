#!/usr/bin/env python3
from pathlib import Path
import re

SITE=Path(__file__).resolve().parent
required=["index.html","404.html","_headers","assets/app.js","assets/styles.css","assets/goreecloud-logo.svg","assets/glaze-ui-mark.svg","assets/privacy-shield-icon.svg","assets/wardveil-security-icon.svg"]
for name in required:
    if not (SITE/name).is_file(): raise SystemExit(f"missing Projects site file: {name}")
html=(SITE/"index.html").read_text(encoding="utf-8")
js=(SITE/"assets/app.js").read_text(encoding="utf-8")
headers=(SITE/"_headers").read_text(encoding="utf-8")
for needle in ["Suite applications","Shared foundations","Glaze UI 1.4","Privacy Shield","Wardveil Security","Everkeep","GoreeCloud Calendar","GoreeCloud Keyboard","GoreeCloud Mail","GoreeCloud Music","GoreeCloud Photos","GoreeCloud Vault Server","GoreeCloud Suite","GoreeCloud Firefox Extensions","GoreeCloud Autobiography","GoreeCloud Waypoint"]:
    if needle not in html+js: raise SystemExit(f"current portfolio marker missing: {needle}")
if js.count("kind:'Application'") != 28: raise SystemExit("Projects catalog must contain exactly 28 Suite applications")
if js.count("kind:'Foundation'") != 6: raise SystemExit("Projects catalog must contain exactly 6 shared foundations")
for icon in ["/assets/goreecloud-logo.svg","/assets/glaze-ui-mark.svg","/assets/privacy-shield-icon.svg","/assets/wardveil-security-icon.svg"]:
    if icon not in html+js: raise SystemExit(f"approved identity artwork is not used: {icon}")
for src in re.findall(r'src=["\']([^"\']+)',html):
    if src.startswith("http:") or src.startswith("https:"): raise SystemExit(f"remote browser resource prohibited: {src}")
for directive in ["Content-Security-Policy:","Permissions-Policy:","X-Content-Type-Options: nosniff"]:
    if directive not in headers: raise SystemExit(f"security header missing: {directive}")
if "localStorage" not in js or "data-theme-choice" not in html: raise SystemExit("local appearance preference contract missing")
if "Repository visibility and development status are shown independently from production acceptance" not in html: raise SystemExit("source-versus-production boundary missing")
print("GoreeCloud Projects current portfolio validation passed")
