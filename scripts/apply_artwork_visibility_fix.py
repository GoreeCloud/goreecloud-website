#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")

service_targets = {
'''          <article class="service-card" data-service="notes">\n            <p class="service-kicker">Notes &amp; Knowledge</p>''': '''          <article class="service-card" data-service="notes">\n            <div class="service-art service-art-goreecloud" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></div>\n            <p class="service-kicker">Notes &amp; Knowledge</p>''',
'''          <article class="service-card" data-service="memos">\n            <p class="service-kicker">Quick Capture</p>''': '''          <article class="service-card" data-service="memos">\n            <div class="service-art service-art-goreecloud" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></div>\n            <p class="service-kicker">Quick Capture</p>''',
'''          <article class="service-card" data-service="tasks">\n            <p class="service-kicker">Tasks &amp; Projects</p>''': '''          <article class="service-card" data-service="tasks">\n            <div class="service-art service-art-goreecloud" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></div>\n            <p class="service-kicker">Tasks &amp; Projects</p>''',
'''          <article class="service-card" data-service="contacts">\n            <p class="service-kicker">Contacts &amp; Address Book</p>''': '''          <article class="service-card" data-service="contacts">\n            <div class="service-art service-art-goreecloud" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></div>\n            <p class="service-kicker">Contacts &amp; Address Book</p>''',
}
for old, new in service_targets.items():
    if text.count(old) != 1:
        raise SystemExit(f"expected one service target: {old[:70]}")
    text = text.replace(old, new, 1)

platform_targets = {
'''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-state planned">Release Candidate</span>\n            </div>\n            <p class="platform-kicker">Notifications</p>''': '''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-logo-link platform-logo-static" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></span>\n              <span class="platform-state planned">Release Candidate</span>\n            </div>\n            <p class="platform-kicker">Notifications</p>''',
'''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-state active">Active</span>\n            </div>\n            <p class="platform-kicker">Resource Monitoring</p>''': '''          <article class="platform-card">\n            <div class="platform-card-head">\n              <a class="platform-logo-link" href="https://github.com/henrygd/beszel" target="_blank" rel="noopener noreferrer" aria-label="Beszel official repository"><img src="assets/platform/beszel.svg" alt="" width="52" height="52"></a>\n              <span class="platform-state active">Active</span>\n            </div>\n            <p class="platform-kicker">Resource Monitoring</p>''',
'''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-state planned">Replacement</span>\n            </div>\n            <p class="platform-kicker">GoreeCloud Availability</p>''': '''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-logo-link platform-logo-static" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></span>\n              <span class="platform-state planned">Replacement</span>\n            </div>\n            <p class="platform-kicker">GoreeCloud Availability</p>''',
'''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-state active">Active</span>\n            </div>\n            <p class="platform-kicker">Private Search</p>''': '''          <article class="platform-card">\n            <div class="platform-card-head">\n              <span class="platform-logo-link platform-logo-static" aria-hidden="true"><img src="assets/goreecloud-logo.svg" alt="" width="52" height="52"></span>\n              <span class="platform-state active">Active</span>\n            </div>\n            <p class="platform-kicker">Private Search</p>''',
}
for old, new in platform_targets.items():
    if text.count(old) != 1:
        raise SystemExit(f"expected one platform target: {old[:70]}")
    text = text.replace(old, new, 1)
index.write_text(text, encoding="utf-8")

platform_css = ROOT / "css/platform.css"
css = platform_css.read_text(encoding="utf-8")
addon = '''\n.platform-logo-link img {\n  display: block;\n  max-width: 46px;\n  max-height: 46px;\n  width: auto;\n  height: auto;\n  object-fit: contain;\n}\n.platform-logo-static { cursor: default; }\n.platform-logo-static img,\n.service-art-goreecloud img { width: 38px; height: 38px; }\n.platform-logo-link img[src$="docker.png"] { transform: scale(1.45); }\n.platform-logo-link img[src$="proxmox.svg"] { transform: scale(1.18); }\n.platform-logo-link img[src$="caddy.svg"] { transform: scale(1.12); }\n'''
if addon.strip() not in css:
    css += addon
platform_css.write_text(css, encoding="utf-8")

build = ROOT / "scripts/build_public_site.py"
b = build.read_text(encoding="utf-8")
needle = '    "assets/platform/adguard-home.svg",\n'
if '    "assets/platform/beszel.svg",\n' not in b:
    if b.count(needle) != 1: raise SystemExit('build allowlist anchor drift')
    b = b.replace(needle, needle + '    "assets/platform/beszel.svg",\n', 1)
build.write_text(b, encoding="utf-8")

manifest_path = ROOT / "docs/visual-identity-sources.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
if not any(a.get("asset_path") == "assets/platform/beszel.svg" for a in manifest["assets"]):
    manifest["assets"].append({
      "asset_path": "assets/platform/beszel.svg",
      "bytes": 1405,
      "official_artwork_exists": True,
      "sha256": "5ff54970100e1ffca4c169987e588997ebbde754b3c0a8824a8b52317b7c420a",
      "source_authority": "selfhst/icons — Beszel artwork referenced by the Beszel maintainer",
      "source_path": "svg/beszel.svg",
      "source_ref": "948e3aa28d3110ee23957473a85431650e10e778",
      "source_url": "https://raw.githubusercontent.com/selfhst/icons/948e3aa28d3110ee23957473a85431650e10e778/svg/beszel.svg"
    })
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

(ROOT / "tests/test_homepage_artwork_visibility.py").write_text('''from pathlib import Path\nimport unittest\n\nROOT = Path(__file__).resolve().parents[1]\nINDEX = (ROOT / "index.html").read_text(encoding="utf-8")\n\nclass HomepageArtworkVisibilityTests(unittest.TestCase):\n    def test_native_service_cards_have_suite_artwork(self):\n        for service in ("notes", "memos", "tasks", "contacts"):\n            block = INDEX.split(f'data-service="{service}"', 1)[1].split("</article>", 1)[0]\n            self.assertIn('assets/goreecloud-logo.svg', block)\n    def test_native_platform_cards_have_suite_artwork(self):\n        for label in ("GoreeCloud Notify", "GoreeCloud Monitoring", "GoreeCloud Search"):\n            before = INDEX.split(f'<h3>{label}</h3>', 1)[0][-900:]\n            self.assertIn('assets/goreecloud-logo.svg', before)\n    def test_beszel_has_reviewed_artwork(self):\n        block = INDEX.split('<h3>Beszel</h3>', 1)[0][-900:]\n        self.assertIn('assets/platform/beszel.svg', block)\n\nif __name__ == "__main__": unittest.main()\n''', encoding="utf-8")
print('Artwork visibility migration applied.')
