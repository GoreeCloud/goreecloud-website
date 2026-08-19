#!/usr/bin/env python3
"""Setup-only wrapper for the v5.23 official-artwork exporter."""
from __future__ import annotations
from io import BytesIO
import re
import zipfile
import v523_base as base

ORIGINAL_FETCH = base.fetch
ORIGINAL_WRITE_INVENTORY = base.write_inventory
ORIGINAL_RUN_CHECKS = base.run_checks
ONLYOFFICE_ZIP = "https://www.onlyoffice.com/images/templates/press-downloads/logo/files/logo_symbol.zip"
STIRLING_OLD_KEY = "assets/services/stirling-pdf.png"
STIRLING_ORG_ART = "https://github.com/Stirling-Tools.png?size=192"

base.ASSETS[STIRLING_OLD_KEY] = (STIRLING_ORG_ART, "Stirling Tools official GitHub organization", "2026-08-19", "GitHub organization avatar")


def fetch_official_artwork(url: str) -> bytes:
    try:
        if url == "https://www.onlyoffice.com/favicon.ico":
            raw = ORIGINAL_FETCH(ONLYOFFICE_ZIP)
            with zipfile.ZipFile(BytesIO(raw)) as archive:
                names = [name for name in archive.namelist() if name.lower().endswith(".svg") and not name.endswith("/")]
                if not names: raise RuntimeError("ONLYOFFICE official symbol archive did not contain an SVG asset")
                return archive.read(sorted(names, key=lambda n: ("symbol" not in n.lower(), len(n), n.lower()))[0])
        return ORIGINAL_FETCH(url)
    except Exception as exc:
        raise RuntimeError(f"Official artwork source failed: {url}: {exc}") from exc


def write_deployable_inventory(records):
    return ORIGINAL_WRITE_INVENTORY([record for record in records if record.get("asset_path")])


def normalize_canonical_logo_contract() -> None:
    for name in ("index.html", "repositories.html", "privacy.html", "security.html", "404.html"):
        path = base.ROOT / name
        text = path.read_text(encoding="utf-8")
        text = text.replace('<link rel="icon" href="assets/goreecloud-logo.svg" type="image/png">\n', '')
        text = text.replace('<link rel="icon" type="image/png" href="assets/goreecloud-logo.svg">\n', '')
        text = text.replace('<link rel="apple-touch-icon" href="assets/goreecloud-logo.svg">', '<link rel="apple-touch-icon" href="assets/goreecloud-logo.svg" type="image/svg+xml">')
        if name == "index.html":
            text = re.sub(r'<img src="(assets/(?:services|platform|roadmap|social)/[^"]+)" alt="">', r'<img src="\1" alt="" width="52" height="52">', text)
        path.write_text(text, encoding="utf-8")

    glaze = base.ROOT / "scripts" / "validate_glaze_ui.py"
    text = glaze.read_text(encoding="utf-8")
    old = 'attrs.get("src", "").endswith("assets/goreecloud-icon.png")'
    new = 'attrs.get("src", "").endswith("assets/goreecloud-logo.svg")'
    if text.count(old) != 1: raise RuntimeError(f"Expected one legacy Glaze brand-icon contract; found {text.count(old)}")
    glaze.write_text(text.replace(old, new, 1), encoding="utf-8")

    surface = base.ROOT / "scripts" / "validate_public_surface.py"
    text = surface.read_text(encoding="utf-8")
    old_block = '''        if not any("icon" in rels and href == "assets/favicon.svg" and content_type == "image/svg+xml" for rels, href, content_type in normalized_icons):
            errors.append(f"{display} must publish the local SVG favicon.")
        if not any("icon" in rels and href == "assets/goreecloud-icon.png" and content_type == "image/png" for rels, href, content_type in normalized_icons):
            errors.append(f"{display} must publish the PNG favicon fallback.")
        if not any("apple-touch-icon" in rels and href == "assets/goreecloud-icon.png" for rels, href, _ in normalized_icons):
            errors.append(f"{display} must publish the local Apple touch icon.")
'''
    new_block = '''        if not any("icon" in rels and href == "assets/goreecloud-logo.svg" and content_type == "image/svg+xml" for rels, href, content_type in normalized_icons):
            errors.append(f"{display} must publish the canonical GoreeCloud SVG favicon.")
        if not any("apple-touch-icon" in rels and href == "assets/goreecloud-logo.svg" for rels, href, _ in normalized_icons):
            errors.append(f"{display} must publish the canonical GoreeCloud SVG Apple-touch identity.")
'''
    if text.count(old_block) != 1: raise RuntimeError(f"Expected one legacy public-surface icon block; found {text.count(old_block)}")
    surface.write_text(text.replace(old_block, new_block, 1), encoding="utf-8")


def run_checks_with_canonical_logo() -> None:
    normalize_canonical_logo_contract()
    ORIGINAL_RUN_CHECKS()

base.fetch = fetch_official_artwork
base.write_inventory = write_deployable_inventory
base.run_checks = run_checks_with_canonical_logo
raise SystemExit(base.main())
