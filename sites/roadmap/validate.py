#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for name in ("index.html", "404.html", "site.css", "site.js", "_headers"):
    if not (ROOT / name).is_file():
        raise SystemExit(f"missing roadmap site file: {name}")
html=(ROOT/"index.html").read_text(encoding="utf-8")
headers=(ROOT/"_headers").read_text(encoding="utf-8")
for needle in (
    "Public Development Roadmap",
    "Active development",
    "Near-term priorities",
    "Long-term direction",
    "dates are not promises",
    "private infrastructure or security-sensitive work is omitted",
    "Glaze UI Fold identity",
    "Drive persistent storage foundation",
    "Search, Notify, and Terminal candidates",
    "PostgreSQL",
    "RC #09",
    "50.2-rc.2",
):
    if needle not in html:
        raise SystemExit(f"required roadmap content missing: {needle}")
for needle in ("Content-Security-Policy:","frame-ancestors 'none'","Permissions-Policy:","X-Content-Type-Options: nosniff"):
    if needle not in headers:
        raise SystemExit(f"required security header missing: {needle}")
for prohibited in ("google-analytics","googletagmanager","fonts.googleapis.com","segment.com"):
    if prohibited in html.lower():
        raise SystemExit(f"prohibited runtime dependency: {prohibited}")
print("GoreeCloud roadmap public-site validation passed")
