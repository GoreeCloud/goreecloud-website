#!/usr/bin/env python3
"""Setup-only v5.23 official-artwork migration/export bridge.

This temporary file runs only on the setup branch. It downloads identity artwork from
first-party project/platform sources, patches the website to use those local copies,
validates the transformed workspace, and emits an exact compressed bundle for atomic
release-tree construction. This file must never enter the release tree.
"""
from __future__ import annotations

from base64 import b64encode
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

ASSETS = {
    "assets/goreecloud-logo.svg": ("https://raw.githubusercontent.com/GoreeCloud/goreecloud-logo/c766a4299196f8c80ed3f6de70ee8b74eb5818d9/official/goreecloud-logo.svg", "GoreeCloud/goreecloud-logo", "c766a4299196f8c80ed3f6de70ee8b74eb5818d9", "official/goreecloud-logo.svg"),
    "assets/services/nextcloud.svg": ("https://raw.githubusercontent.com/nextcloud/server/master/core/img/logo/logo.svg", "nextcloud/server", "master", "core/img/logo/logo.svg"),
    "assets/services/immich.svg": ("https://raw.githubusercontent.com/immich-app/immich/main/design/immich-logo.svg", "immich-app/immich", "main", "design/immich-logo.svg"),
    "assets/services/jellyfin.svg": ("https://raw.githubusercontent.com/jellyfin/jellyfin-ux/master/logos/SVG/jellyfin-icon--color-on-light.svg", "jellyfin/jellyfin-ux", "master", "logos/SVG/jellyfin-icon--color-on-light.svg"),
    "assets/services/navidrome.png": ("https://raw.githubusercontent.com/navidrome/navidrome/master/ui/public/android-chrome-192x192.png", "navidrome/navidrome", "master", "ui/public/android-chrome-192x192.png"),
    "assets/services/audiobookshelf.svg": ("https://raw.githubusercontent.com/advplyr/audiobookshelf/master/client/static/icon.svg", "advplyr/audiobookshelf", "master", "client/static/icon.svg"),
    "assets/services/paperless-ngx.svg": ("https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/dev/docs/assets/logo_leaf.svg", "paperless-ngx/paperless-ngx", "dev", "docs/assets/logo_leaf.svg"),
    "assets/services/vaultwarden.svg": ("https://raw.githubusercontent.com/dani-garcia/vaultwarden/0cefa4cca7c9f2a5579dd290f78193b543818c51/resources/vaultwarden-logo.svg", "dani-garcia/vaultwarden", "0cefa4cca7c9f2a5579dd290f78193b543818c51", "resources/vaultwarden-logo.svg"),
    "assets/services/element.svg": ("https://raw.githubusercontent.com/element-hq/element-web/d8e18abdf90c917d38fc1c8021e32e5e5782ec91/apps/web/res/themes/element/img/logos/element-logo.svg", "element-hq/element-web", "d8e18abdf90c917d38fc1c8021e32e5e5782ec91", "apps/web/res/themes/element/img/logos/element-logo.svg"),
    "assets/services/matrix.svg": ("https://raw.githubusercontent.com/matrix-org/matrix.org/afca85178d131d3d85a33da34d64cbae88697a77/static/images/matrix-logo-white.svg", "matrix-org/matrix.org", "afca85178d131d3d85a33da34d64cbae88697a77", "static/images/matrix-logo-white.svg"),
    "assets/services/onlyoffice.ico": ("https://www.onlyoffice.com/favicon.ico", "ONLYOFFICE official website", "2026-08-19", "/favicon.ico"),
    "assets/services/stirling-pdf.png": ("https://raw.githubusercontent.com/Stirling-Tools/Stirling-PDF/ec3de16c0862c01190bf45896bae87e9f0e10ca7/frontend/editor/public/modern-logo/logo192.png", "Stirling-Tools/Stirling-PDF", "ec3de16c0862c01190bf45896bae87e9f0e10ca7", "frontend/editor/public/modern-logo/logo192.png"),
    "assets/services/actual-budget.png": ("https://raw.githubusercontent.com/actualbudget/actual/master/packages/desktop-client/public/android-chrome-192x192.png", "actualbudget/actual", "master", "packages/desktop-client/public/android-chrome-192x192.png"),
    "assets/platform/proxmox.svg": ("https://www.proxmox.com/images/proxmox/logos/mediakit-proxmox-server-solutions-logos-light.svg", "Proxmox official media kit", "2026-08-19", "mediakit-proxmox-server-solutions-logos-light.svg"),
    "assets/platform/debian.svg": ("https://www.debian.org/logos/openlogo-nd.svg", "Debian official logo page", "2026-08-19", "logos/openlogo-nd.svg"),
    "assets/platform/docker.png": ("https://www.docker.com/app/uploads/2026/02/Docker_Mark_660x400.png", "Docker official brand site", "2026-08-19", "Docker_Mark_660x400.png"),
    "assets/platform/netbird.svg": ("https://raw.githubusercontent.com/netbirdio/netbird/9efa3c6579fe5b193fa72b8e717a0bfac014d0f0/proxy/web/src/assets/netbird.svg", "netbirdio/netbird", "9efa3c6579fe5b193fa72b8e717a0bfac014d0f0", "proxy/web/src/assets/netbird.svg"),
    "assets/platform/adguard-home.svg": ("https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/5c113ec4c565a8911f4531b3701a9013e066c433/client_v2/public/assets/favicon.svg", "AdguardTeam/AdGuardHome", "5c113ec4c565a8911f4531b3701a9013e066c433", "client_v2/public/assets/favicon.svg"),
    "assets/platform/caddy.svg": ("https://raw.githubusercontent.com/caddyserver/website/15ac087cfd9c21a53b2ddfa10359fdc63d5ec9b6/src/old/resources/images/caddy-logo.svg", "caddyserver/website", "15ac087cfd9c21a53b2ddfa10359fdc63d5ec9b6", "src/old/resources/images/caddy-logo.svg"),
    "assets/platform/uptime-kuma.svg": ("https://raw.githubusercontent.com/louislam/uptime-kuma/master/public/icon.svg", "louislam/uptime-kuma", "master", "public/icon.svg"),
    "assets/roadmap/home-assistant.png": ("https://raw.githubusercontent.com/home-assistant/home-assistant.io/6947d83903e932fb3d757b439e34814af2a23b42/source/images/favicon-192x192.png", "home-assistant/home-assistant.io", "6947d83903e932fb3d757b439e34814af2a23b42", "source/images/favicon-192x192.png"),
    "assets/roadmap/frigate.svg": ("https://raw.githubusercontent.com/blakeblackshear/frigate/036bae4ea96f23e564622a3d19c1558254122b2b/web/images/branding/favicon.svg", "blakeblackshear/frigate", "036bae4ea96f23e564622a3d19c1558254122b2b", "web/images/branding/favicon.svg"),
    "assets/social/instagram.ico": ("https://www.instagram.com/favicon.ico", "Instagram official website", "2026-08-19", "/favicon.ico"),
    "assets/social/pinterest.ico": ("https://www.pinterest.com/favicon.ico", "Pinterest official website", "2026-08-19", "/favicon.ico"),
    "assets/social/threads.ico": ("https://www.threads.net/favicon.ico", "Threads official website", "2026-08-19", "/favicon.ico"),
    "assets/social/tiktok.ico": ("https://www.tiktok.com/favicon.ico", "TikTok official website", "2026-08-19", "/favicon.ico"),
    "assets/social/youtube.ico": ("https://www.youtube.com/favicon.ico", "YouTube official website", "2026-08-19", "/favicon.ico"),
    "assets/social/x.ico": ("https://x.com/favicon.ico", "X official website", "2026-08-19", "/favicon.ico"),
    "assets/social/reddit.ico": ("https://www.reddit.com/favicon.ico", "Reddit official website", "2026-08-19", "/favicon.ico"),
    "assets/social/github.ico": ("https://github.com/favicon.ico", "GitHub official website", "2026-08-19", "/favicon.ico"),
}

SERVICE_ART = {
    "nextcloud": ["assets/services/nextcloud.svg"], "immich": ["assets/services/immich.svg"],
    "jellyfin": ["assets/services/jellyfin.svg"], "navidrome": ["assets/services/navidrome.png"],
    "audiobookshelf": ["assets/services/audiobookshelf.svg"], "paperless": ["assets/services/paperless-ngx.svg"],
    "vaultwarden": ["assets/services/vaultwarden.svg"], "element": ["assets/services/element.svg", "assets/services/matrix.svg"],
    "onlyoffice": ["assets/services/onlyoffice.ico"], "stirling-pdf": ["assets/services/stirling-pdf.png"],
    "actual-budget": ["assets/services/actual-budget.png"],
}
TEXT_ONLY_SERVICES = {"notes", "memos", "tasks", "contacts"}


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "GoreeCloud-Website-v5.23/1.0", "Accept": "*/*"})
    with urlopen(req, timeout=30) as response:
        data = response.read()
    if not data:
        raise SystemExit(f"Official artwork download was empty: {url}")
    return data


def write_assets() -> list[dict[str, object]]:
    records = []
    for relative, (url, authority, ref, source_path) in ASSETS.items():
        data = fetch(url)
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append({
            "asset_path": relative, "official_artwork_exists": True, "source_authority": authority,
            "source_ref": ref, "source_path": source_path, "source_url": url,
            "sha256": sha256(data).hexdigest(), "bytes": len(data),
        })
    return records


def patch_service_cards(text: str) -> str:
    for service, paths in SERVICE_ART.items():
        pattern = re.compile(rf'(<article class="service-card" data-service="{re.escape(service)}">\s*)<div class="service-icon" aria-hidden="true">.*?</div>', re.S)
        if len(paths) == 1:
            art = f'<div class="service-art" aria-hidden="true"><img src="{paths[0]}" alt=""></div>'
        else:
            art = '<div class="service-art service-art-pair" aria-hidden="true">' + ''.join(f'<img src="{p}" alt="">' for p in paths) + '</div>'
        text, count = pattern.subn(r'\1' + art, text, count=1)
        if count != 1: raise SystemExit(f"Expected one service placeholder for {service}; found {count}")
    for service in TEXT_ONLY_SERVICES:
        pattern = re.compile(rf'(<article class="service-card" data-service="{re.escape(service)}">\s*)<div class="service-icon" aria-hidden="true">.*?</div>\s*', re.S)
        text, count = pattern.subn(r'\1', text, count=1)
        if count != 1: raise SystemExit(f"Expected one text-only service placeholder for {service}; found {count}")
    return text


def replace_platform(text: str, token: str, path: str | None) -> str:
    if path:
        replacement = rf'\1<a class="platform-logo-link" \2><img src="{path}" alt=""></a>'
        pattern = re.compile(rf'(<div class="platform-card-head">\s*)<a class="platform-logo-link platform-native-mark" ([^>]+)>{re.escape(token)}</a>')
    else:
        replacement = r'\1'
        pattern = re.compile(rf'(<div class="platform-card-head">\s*)(?:<a class="platform-logo-link platform-native-mark" [^>]+>{re.escape(token)}</a>|<span class="platform-native-mark" aria-hidden="true">{re.escape(token)}</span>)\s*')
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1: raise SystemExit(f"Expected one platform placeholder {token}; found {count}")
    return text


def patch_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace('assets/favicon.svg', 'assets/goreecloud-logo.svg').replace('assets/goreecloud-icon.png', 'assets/goreecloud-logo.svg')
    text = patch_service_cards(text)
    for token, art in (("PX","assets/platform/proxmox.svg"),("DE","assets/platform/debian.svg"),("DK","assets/platform/docker.png"),("NB","assets/platform/netbird.svg"),("AG","assets/platform/adguard-home.svg"),("CA","assets/platform/caddy.svg"),("BZ",None),("UK","assets/platform/uptime-kuma.svg"),("GN",None),("GM",None),("GS",None)):
        text = replace_platform(text, token, art)
    roadmap = {"HA":"assets/roadmap/home-assistant.png", "FR":"assets/roadmap/frigate.svg"}
    for token, art in roadmap.items():
        pattern = re.compile(rf'<span class="roadmap-icon" aria-hidden="true">{token}</span>')
        text, count = pattern.subn(f'<span class="roadmap-icon roadmap-art" aria-hidden="true"><img src="{art}" alt=""></span>', text, count=1)
        if count != 1: raise SystemExit(f"Expected one roadmap placeholder {token}; found {count}")
    text = re.sub(r'<span class="roadmap-icon" aria-hidden="true">AI</span>\s*', '', text, count=1)
    socials = {"Instagram":"instagram.ico","Pinterest":"pinterest.ico","Threads":"threads.ico","TikTok":"tiktok.ico","YouTube":"youtube.ico","X":"x.ico","Reddit":"reddit.ico","GitHub":"github.ico"}
    for label, filename in socials.items():
        card = re.compile(rf'(<a class="social-card(?: github-card)?"[^>]+aria-label="GoreeCloud on {re.escape(label)}">\s*)<span class="social-icon[^\"]*" aria-hidden="true">.*?</span>', re.S)
        repl = rf'\1<span class="social-icon" aria-hidden="true"><img src="assets/social/{filename}" alt=""></span>'
        text, count = card.subn(repl, text, count=1)
        if count != 1: raise SystemExit(f"Expected one social placeholder for {label}; found {count}")
    old = 'Technology names identify their respective projects; outbound links lead to official project sites or repositories. GoreeCloud uses neutral Glaze UI letter marks instead of third-party logo artwork. This is a representative public foundation, not a complete infrastructure inventory.'
    new = 'Product and platform marks identify the referenced projects and services. Trademarks and artwork remain the property of their respective owners; their appearance here is referential and does not imply sponsorship, endorsement, or affiliation. This is a representative public foundation, not a complete infrastructure inventory.'
    if old not in text: raise SystemExit("Expected v5.22 platform artwork note was not found")
    text = text.replace(old, new, 1)
    for stale in ('class="service-icon"', 'platform-native-mark', 'social-letter'):
        if stale in text: raise SystemExit(f"Placeholder marker remains in homepage: {stale}")
    path.write_text(text, encoding="utf-8")


def patch_css() -> None:
    style = ROOT / "css/style.css"
    text = style.read_text(encoding="utf-8")
    start = text.index('.service-icon {')
    end = text.index('\n.service-kicker', start)
    text = text[:start] + '''.service-art {\n  width: 52px;\n  height: 52px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  gap: .28rem;\n  padding: 7px;\n  border-radius: 13px;\n  background: rgba(7,17,31,.78);\n  border: 1px solid rgba(0,194,255,.18);\n}\n.service-art img { max-width: 100%; max-height: 100%; object-fit: contain; }\n.service-art-pair img { max-width: 48%; max-height: 85%; }\n''' + text[end:]
    text = text.replace('.social-icon svg { width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 1.7; }', '.social-icon img { width: 25px; height: 25px; object-fit: contain; }')
    style.write_text(text, encoding="utf-8")

    platform = ROOT / "css/platform.css"
    p = platform.read_text(encoding="utf-8")
    p = re.sub(r'\.platform-logo-link,\n\.platform-native-mark \{', '.platform-logo-link {', p, count=1)
    p = re.sub(r'\.platform-native-mark \{.*?\}\n\n', '', p, count=1, flags=re.S)
    p = p.replace('.platform-logo-link img {', '.platform-logo-link img {')
    p = p.replace('  .platform-logo-link,\n  .platform-native-mark,\n', '  .platform-logo-link,\n')
    platform.write_text(p, encoding="utf-8")

    roadmap = ROOT / "css/roadmap.css"
    r = roadmap.read_text(encoding="utf-8")
    r += '\n.roadmap-art img { max-width: 30px; max-height: 30px; object-fit: contain; }\n'
    roadmap.write_text(r, encoding="utf-8")


def patch_manifest() -> None:
    path = ROOT / "site.webmanifest"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["icons"] = [{"src":"/assets/goreecloud-logo.svg","sizes":"any","type":"image/svg+xml","purpose":"any"}]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def patch_other_pages() -> None:
    for name in ("404.html","privacy.html","security.html","repositories.html"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8").replace('assets/favicon.svg','assets/goreecloud-logo.svg').replace('assets/goreecloud-icon.png','assets/goreecloud-logo.svg')
        path.write_text(text, encoding="utf-8")


def write_identity_manifest(records: list[dict[str, object]]) -> None:
    records += [
      {"id": n, "official_artwork_exists": False, "fallback": "text-only", "reason": "No approved canonical artwork was found in the authoritative GoreeCloud repository during the v5.23 review."}
      for n in ("goreecloud-notes","goreecloud-memos","goreecloud-tasks","goreecloud-contacts","goreecloud-notify","goreecloud-monitor","goreecloud-search","local-ai")
    ]
    data = {"schema_version":1,"reviewed":"2026-08-19","policy":"Official icon, logo, or artwork is required when it exists; text-only is the only allowed fallback when approved official artwork does not exist.","assets":records}
    out = ROOT / "docs/visual-identity-sources.json"
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def update_build(records: list[dict[str, object]]) -> None:
    path = ROOT / "scripts/build_public_site.py"
    text = path.read_text(encoding="utf-8")
    assets = sorted(str(r["asset_path"]) for r in records if r.get("asset_path")) + ["assets/social-preview.png"]
    block = 'PUBLIC_ASSET_FILES = (\n' + ''.join(f'    "{a}",\n' for a in assets) + ')'
    text = re.sub(r'PUBLIC_ASSET_FILES = \(.*?\)', block, text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")


def write_validator() -> None:
    path = ROOT / "scripts/validate_public_assets.py"
    path.write_text('''#!/usr/bin/env python3\nfrom __future__ import annotations\nfrom hashlib import sha256\nimport json\nfrom pathlib import Path\nimport sys\nfrom build_public_site import PUBLIC_ASSET_FILES, ROOT\nMANIFEST=ROOT/"docs/visual-identity-sources.json"\nINDEX=ROOT/"index.html"\n\ndef main():\n    errors=[]\n    data=json.loads(MANIFEST.read_text(encoding="utf-8"))\n    records=data.get("assets",[])\n    deployed={r["asset_path"]:r for r in records if r.get("asset_path")}\n    expected=set(PUBLIC_ASSET_FILES)-{"assets/social-preview.png"}\n    if set(deployed)!=expected: errors.append(f"Identity manifest/deployable artwork mismatch: manifest={sorted(deployed)} expected={sorted(expected)}")\n    for rel, rec in deployed.items():\n        p=ROOT/rel\n        if not p.is_file() or p.is_symlink(): errors.append(f"Official identity asset is not a regular file: {rel}"); continue\n        actual=sha256(p.read_bytes()).hexdigest()\n        if rec.get("sha256")!=actual: errors.append(f"Identity asset changed without provenance review: {rel}")\n        if not rec.get("source_authority") or not rec.get("source_url"): errors.append(f"Identity asset lacks source authority: {rel}")\n    index=INDEX.read_text(encoding="utf-8")\n    for stale in ('class="service-icon"','platform-native-mark','social-letter','neutral Glaze UI letter marks instead of third-party logo artwork','assets/goreecloud-icon.png','assets/favicon.svg'):\n        if stale in index: errors.append(f"Obsolete placeholder/identity marker remains: {stale}")\n    for rel in expected:\n        if rel != 'assets/goreecloud-logo.svg' and rel not in index: errors.append(f"Deployable identity asset is not referenced by homepage: {rel}")\n    if index.count('assets/goreecloud-logo.svg') < 3: errors.append('Canonical GoreeCloud logo is not used across visible website identity surfaces.')\n    for rec in records:\n        if rec.get('official_artwork_exists') is False and rec.get('fallback')!='text-only': errors.append(f"Non-art fallback must be text-only: {rec.get('id')}")\n    if errors:\n        print('Official visual-identity validation failed:', file=sys.stderr)\n        for e in errors: print(f'- {e}', file=sys.stderr)\n        return 1\n    print(f'Official visual-identity validation passed across {len(deployed)} deployed identity assets.')\n    return 0\nif __name__=='__main__': raise SystemExit(main())\n''', encoding="utf-8")


def write_tests() -> None:
    (ROOT/"tests/test_public_asset_boundary.py").write_text('''#!/usr/bin/env python3\nfrom pathlib import Path\nimport json, unittest\nROOT=Path(__file__).resolve().parents[1]\nclass OfficialArtworkTests(unittest.TestCase):\n  @classmethod\n  def setUpClass(cls):\n    cls.index=(ROOT/'index.html').read_text(encoding='utf-8')\n    cls.manifest=json.loads((ROOT/'docs/visual-identity-sources.json').read_text(encoding='utf-8'))\n  def test_placeholders_are_removed(self):\n    for marker in ('class="service-icon"','platform-native-mark','social-letter','neutral Glaze UI letter marks instead of third-party logo artwork'):\n      self.assertNotIn(marker,self.index)\n  def test_canonical_goreecloud_logo_is_visible(self):\n    self.assertGreaterEqual(self.index.count('assets/goreecloud-logo.svg'),3)\n  def test_only_text_fallback_when_artwork_missing(self):\n    for r in self.manifest['assets']:\n      if r.get('official_artwork_exists') is False: self.assertEqual(r.get('fallback'),'text-only')\n  def test_social_cards_use_local_official_identity_files(self):\n    for name in ('instagram','pinterest','threads','tiktok','youtube','x','reddit','github'):\n      self.assertIn(f'assets/social/{name}.ico',self.index)\nif __name__=='__main__': unittest.main()\n''', encoding="utf-8")
    inv = ROOT/"tests/test_public_asset_inventory.py"
    t=inv.read_text(encoding="utf-8")
    t=t.replace('third-party artwork removed from the public artifact','official artwork is required when it exists')
    t=t.replace('repository presence does not make those files deployable','identity artwork must be source-traceable before deployment')
    inv.write_text(t, encoding="utf-8")


def write_inventory(records: list[dict[str, object]]) -> None:
    rows=[]
    for r in sorted(records,key=lambda x:str(x.get('asset_path',''))):
        rel=str(r['asset_path']); blob=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
        rows.append(f"| `{rel}` | {r['source_authority']} | {r['source_ref']} · {r['source_path']} | `{blob}` |")
    social_blob=subprocess.check_output(['git','hash-object',str(ROOT/'assets/social-preview.png')],cwd=ROOT,text=True).strip()
    rows.append(f"| `assets/social-preview.png` | GoreeCloud website | Existing reviewed social preview | `{social_blob}` |")
    text='''# GoreeCloud Public Asset Inventory\n\nThis inventory records every deployable website artwork file. It is not a license grant. Official artwork is required when it exists, and identity artwork must be source-traceable before deployment. The source-code license does not automatically license GoreeCloud branding or third-party marks. Third-party trademarks and artwork remain the property of their respective owners; use is referential and does not imply sponsorship, endorsement, or affiliation. Final human reachable-history/contextual-disclosure review remains required for source-publication decisions, and Issue #5 remains open until that separate review is resolved.\n\n| Deployable asset | Source authority | Source revision/path | Reviewed Git blob |\n| --- | --- | --- | --- |\n'''+"\n".join(rows)+'''\n\nThe current deployable asset boundary is intentionally explicit and fail-closed. Historical repository presence does not authorize artwork use; current deployment requires a matching source record and reviewed bytes.\n'''
    (ROOT/"docs/public-asset-inventory.md").write_text(text,encoding="utf-8")


def patch_docs() -> None:
    (ROOT/"VERSION").write_text("5.23.0\n",encoding="utf-8")
    for rel in ("README.md","docs/stability-baseline.md"):
        p=ROOT/rel; t=p.read_text(encoding="utf-8").replace('5.22.0','5.23.0').replace('v5.22.0','v5.23.0')
        note='\n\n## v5.23 official visual identity\n\nThe website uses official project, service, platform, and social-media artwork when a canonical identity exists. GoreeCloud website branding is sourced from `GoreeCloud/goreecloud-logo` and `official/goreecloud-logo.svg`. Placeholder initials and generic monograms are not production identity. If an approved official artwork asset does not exist, the public surface remains text-only rather than inventing a replacement. All deployed identity assets are local static copies with source authority and integrity recorded in `docs/visual-identity-sources.json`.\n'
        if '## v5.23 official visual identity' not in t: t += note
        p.write_text(t,encoding="utf-8")


def run_checks() -> None:
    commands=[
      ['python','scripts/validate_public_assets.py'],['python','scripts/validate_accessibility.py'],['python','scripts/validate_glaze_ui.py'],
      ['python','scripts/validate_public_surface.py'],['python','scripts/validate_performance_budget.py'],['python','scripts/build_public_site.py'],
      ['python','scripts/validate_build_artifact.py'],['python','-m','unittest','discover','-s','tests','-p','test_*.py'],['python','scripts/validate_site.py']]
    for cmd in commands: subprocess.run(cmd,cwd=ROOT,check=True)


def emit_bundle() -> None:
    changed=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).splitlines()
    paths=[]
    for line in changed:
        rel=line[3:]
        if rel=='scripts/validate_repository_hygiene.py': continue
        p=ROOT/rel
        if p.exists() and p.is_file(): paths.append(rel)
    with tempfile.NamedTemporaryFile(suffix='.tar.gz',delete=False) as tmp: out=Path(tmp.name)
    with tarfile.open(out,'w:gz',compresslevel=9) as tf:
        for rel in sorted(set(paths)): tf.add(ROOT/rel,arcname=rel)
    data=out.read_bytes(); out.unlink(missing_ok=True)
    print('V523_TARGZ_BASE64 '+b64encode(data).decode('ascii'))
    print(f'V523_TARGZ_BYTES {len(data)}')
    print('V523_EXPORT_COMPLETE')


def main() -> int:
    if (ROOT/'VERSION').read_text(encoding='utf-8').strip()!='5.22.0': raise SystemExit('Setup bridge requires exact v5.22.0 source baseline.')
    records=write_assets(); patch_index(); patch_css(); patch_manifest(); patch_other_pages(); write_identity_manifest(records); update_build(records); write_validator(); write_tests(); write_inventory(records); patch_docs();
    (ROOT/'assets/favicon.svg').unlink(missing_ok=True); (ROOT/'assets/goreecloud-icon.png').unlink(missing_ok=True)
    run_checks(); emit_bundle();
    return 1
if __name__=='__main__': raise SystemExit(main())
