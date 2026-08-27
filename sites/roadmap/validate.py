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
    "August 27, 2026",
    "Active development",
    "Near-term priorities",
    "Long-term direction",
    "dates are not promises",
    "private infrastructure or security-sensitive work is omitted",
    "53-repository source inventory",
    "GoreeCloud Code",
    "Forgejo is the initial replaceable infrastructure foundation",
    "GoreeCloud AI",
    "GoreeCloud Documents",
    "GoreeCloud Messenger",
    "GoreeCloud Gateway",
    "GoreeCloud Quill",
    "GoreeCloud Mesh",
    "Design Center",
    "Privacy Center",
    "Security Center",
    "Continuity Center",
    "Mesh Center",
    "Glaze UI 1.5.0",
    "Glaze UI Fold identity",
    "Drive persistent storage foundation",
    "Search, Notify, and Terminal candidates",
    "PostgreSQL",
):
    if needle not in html:
        raise SystemExit(f"required roadmap content missing: {needle}")
for stale in (
    "Gitea is the selected permanent authoritative source-control",
    "Complete Gitea independence",
    "Glaze UI 1.4 is the current Stable production target",
):
    if stale in html:
        raise SystemExit(f"superseded roadmap direction remains public: {stale}")
for needle in ("Content-Security-Policy:","frame-ancestors 'none'","Permissions-Policy:","X-Content-Type-Options: nosniff"):
    if needle not in headers:
        raise SystemExit(f"required security header missing: {needle}")
for prohibited in ("google-analytics","googletagmanager","fonts.googleapis.com","segment.com"):
    if prohibited in html.lower():
        raise SystemExit(f"prohibited runtime dependency: {prohibited}")
print("GoreeCloud roadmap public-site validation passed")