#!/usr/bin/env python3
"""Apply the reviewed homepage platform-foundations presentation atomically."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

text = INDEX.read_text(encoding="utf-8")

old_hero = '''          <div class="hero-labels" aria-label="GoreeCloud characteristics">\n            <span class="glaze-chip">Glaze UI</span>\n            <span class="eyebrow">Privacy-first • Self-hosted • Family-owned</span>\n          </div>'''
new_hero = '''          <div class="hero-labels" aria-label="GoreeCloud platform foundations">\n            <a class="glaze-chip" href="https://design.goreecloud.com/">Glaze UI</a>\n            <a class="glaze-chip" href="https://privacy.goreecloud.com/">Privacy Shield</a>\n            <a class="glaze-chip" href="https://security.goreecloud.com/">Wardveil Security</a>\n            <span class="eyebrow">Design • Privacy • Security</span>\n          </div>'''

old_footer = '        <p class="footer-glaze">Designed with <strong>Glaze UI</strong>.</p>'
new_footer = '        <p class="footer-glaze"><strong>Glaze UI</strong> design • <strong>Privacy Shield</strong> privacy • <strong>Wardveil Security</strong> security.</p>'

if text.count(old_hero) != 1:
    raise SystemExit("Expected exactly one current homepage hero-label block.")
if text.count(old_footer) != 1:
    raise SystemExit("Expected exactly one current homepage foundation footer line.")
if "https://privacy.goreecloud.com/" in text or "https://security.goreecloud.com/" in text or "https://design.goreecloud.com/" in text:
    raise SystemExit("Homepage already contains dedicated foundation destinations; refusing ambiguous migration.")

text = text.replace(old_hero, new_hero, 1).replace(old_footer, new_footer, 1)
INDEX.write_text(text, encoding="utf-8")
print("Applied homepage platform-foundations integration.")
