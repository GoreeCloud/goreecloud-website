#!/usr/bin/env python3
"""Validate the rebuilt dependency-minimal GoreeCloud public website source."""
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys
from build_public_site import GENERATED_GLAZE_FILES, PUBLIC_FILES, ROOT

PAGES = ("index.html", "repositories.html", "privacy.html", "security.html", "404.html")
REQUIRED_HEADERS = ("Content-Security-Policy:", "Referrer-Policy: no-referrer", "X-Content-Type-Options: nosniff", "X-Frame-Options: DENY", "Cross-Origin-Opener-Policy: same-origin", "Origin-Agent-Cluster: ?1", "Strict-Transport-Security:")
FORBIDDEN_COPY = ("Expanding the platform", "Home Assistant", "<h3>Frigate</h3>", "Glaze UI 2.1.0", "Glaze UI 2.2.0", "57 repositories", "40 public repositories", "17 private repositories")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.ids=Counter(); self.h1=0; self.lang=None; self.title_depth=0; self.title_parts=[]; self.local_refs=set(); self.inline_scripts=0; self.inline_styles=0; self.inline_handlers=[]; self.blank_errors=[]; self.images_without_alt=[]; self.insecure=[]; self.canonical=None; self.description=None
    @property
    def title(self): return "".join(self.title_parts).strip()
    def handle_starttag(self, tag, attrs_list):
        attrs={k:(v or "") for k,v in attrs_list}
        if tag=="html": self.lang=attrs.get("lang")
        if tag=="h1": self.h1+=1
        if tag=="title": self.title_depth+=1
        if attrs.get("id"): self.ids[attrs["id"]]+=1
        if tag=="meta" and attrs.get("name")=="description": self.description=attrs.get("content")
        if tag=="link" and attrs.get("rel")=="canonical": self.canonical=attrs.get("href")
        if tag=="script" and not attrs.get("src"): self.inline_scripts+=1
        if tag=="style": self.inline_styles+=1
        if tag=="img" and "alt" not in attrs: self.images_without_alt.append(attrs.get("src","(missing)"))
        for name in attrs:
            if name.lower().startswith("on"): self.inline_handlers.append(f"<{tag} {name}>")
        if attrs.get("target")=="_blank":
            rel=set(attrs.get("rel","").split())
            if not {"noopener","noreferrer"}.issubset(rel): self.blank_errors.append(attrs.get("href",""))
        for attr in ("href","src"):
            value=attrs.get(attr,"")
            if not value or value.startswith(("#","mailto:")): continue
            parsed=urlparse(value)
            if parsed.scheme:
                if parsed.scheme=="http": self.insecure.append(value)
                continue
            if value.startswith("//"): self.insecure.append(value); continue
            self.local_refs.add(parsed.path)
    def handle_endtag(self, tag):
        if tag=="title" and self.title_depth: self.title_depth-=1
    def handle_data(self, data):
        if self.title_depth: self.title_parts.append(data)

def main():
    errors=[]; generated={"/"+p for p in GENERATED_GLAZE_FILES}; allowlisted={"/"+p for p in PUBLIC_FILES}
    for page_name in PAGES:
        text=(ROOT/page_name).read_text(encoding="utf-8"); parser=Parser(); parser.feed(text)
        if parser.lang!="en": errors.append(f"{page_name}: html lang must be en")
        if parser.h1!=1: errors.append(f"{page_name}: expected one h1, found {parser.h1}")
        if not parser.title: errors.append(f"{page_name}: title is empty")
        if not parser.description: errors.append(f"{page_name}: description is empty")
        if not parser.canonical or not parser.canonical.startswith("https://www.goreecloud.com/"): errors.append(f"{page_name}: canonical must use www.goreecloud.com")
        duplicates=[n for n,c in parser.ids.items() if c>1]
        if duplicates: errors.append(f"{page_name}: duplicate ids: {duplicates}")
        if parser.inline_scripts or parser.inline_styles or parser.inline_handlers: errors.append(f"{page_name}: inline executable/style content violates self-only CSP")
        if parser.images_without_alt: errors.append(f"{page_name}: image missing alt: {parser.images_without_alt}")
        if parser.blank_errors: errors.append(f"{page_name}: target=_blank links need noopener noreferrer")
        if parser.insecure: errors.append(f"{page_name}: insecure external references: {parser.insecure}")
        for ref in parser.local_refs:
            if ref=="/": continue
            if ref not in allowlisted and ref not in generated: errors.append(f"{page_name}: local reference is outside reviewed artifact: {ref}")
        for forbidden in FORBIDDEN_COPY:
            if forbidden in text: errors.append(f"{page_name}: retired copy returned: {forbidden}")
        for marker in ('data-glaze-version="1.1"','name="goreecloud-glaze-ui" content="1.1.0"','/css/site-v1.1.css'):
            if marker not in text: errors.append(f"{page_name}: missing current site marker: {marker}")
    index=(ROOT/"index.html").read_text(encoding="utf-8")
    for marker in ("Your cloud should belong to you.","Home, AI &amp; Developer Systems","Publication pending","sites/labs","Systems are replaceable. Durable information is not."):
        if marker not in index: errors.append(f"homepage missing rebuilt information architecture marker: {marker}")
    repos=(ROOT/"repositories.html").read_text(encoding="utf-8")
    for product in ("GoreeCloud Home Security","GoreeCloud Home","GoreeCloud AI","GoreeCloud Containers","GoreeCloud Code"):
        if product not in repos: errors.append(f"repositories page missing current focus product: {product}")
    if re.search(r"\b\d+\s+(?:current\s+)?repositories\b",repos,re.I): errors.append("repositories page must not hard-code an organization repository count")
    headers=(ROOT/"_headers").read_text(encoding="utf-8")
    for marker in REQUIRED_HEADERS:
        if marker not in headers: errors.append(f"_headers missing security marker: {marker}")
    if "</css/site-v1.1.css>" not in headers: errors.append("_headers must preload the rebuilt site stylesheet")
    if "glaze-ui-2.1.0" in headers: errors.append("_headers still references retired GLAZE 2.1 asset")
    manifest=json.loads((ROOT/"site.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("name")!="GoreeCloud": errors.append("web manifest must preserve GoreeCloud master brand")
    if manifest.get("start_url")!="/": errors.append("web manifest start_url must be /")
    main_js=(ROOT/"js/main.js").read_text(encoding="utf-8"); theme_js=(ROOT/"js/theme-init.js").read_text(encoding="utf-8")
    for marker in ("system","light","dark"):
        if marker not in main_js: errors.append(f"appearance control missing mode: {marker}")
    if "root.dataset.js = 'true'" not in theme_js: errors.append("theme init must mark JS readiness before first paint")
    if errors:
        print("Website validation failed:"); [print(f"  - {e}") for e in errors]; return 1
    print("Website source validation passed for the rebuilt GoreeCloud main public surface."); return 0

if __name__=="__main__": sys.exit(main())
