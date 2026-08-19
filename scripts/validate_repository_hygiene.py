#!/usr/bin/env python3
"""Setup-only wrapper for the v5.23 official-artwork exporter."""
from __future__ import annotations
from io import BytesIO
import zipfile
import v523_base as base

ORIGINAL_FETCH = base.fetch
ORIGINAL_WRITE_INVENTORY = base.write_inventory
ONLYOFFICE_ZIP = "https://www.onlyoffice.com/images/templates/press-downloads/logo/files/logo_symbol.zip"
STIRLING_OLD_KEY = "assets/services/stirling-pdf.png"
STIRLING_ORG_ART = "https://github.com/Stirling-Tools.png?size=192"

# The application repository references build-generated classic/modern logo files that are
# not stored at those runtime paths. Use the project's own official GitHub-organization art
# rather than a community icon or invented placeholder.
base.ASSETS[STIRLING_OLD_KEY] = (
    STIRLING_ORG_ART,
    "Stirling Tools official GitHub organization",
    "2026-08-19",
    "GitHub organization avatar",
)


def fetch_official_artwork(url: str) -> bytes:
    try:
        if url == "https://www.onlyoffice.com/favicon.ico":
            raw = ORIGINAL_FETCH(ONLYOFFICE_ZIP)
            with zipfile.ZipFile(BytesIO(raw)) as archive:
                names = [name for name in archive.namelist() if name.lower().endswith(".svg") and not name.endswith("/")]
                if not names:
                    raise RuntimeError("ONLYOFFICE official symbol archive did not contain an SVG asset")
                return archive.read(sorted(names, key=lambda n: ("symbol" not in n.lower(), len(n), n.lower()))[0])
        return ORIGINAL_FETCH(url)
    except Exception as exc:
        raise RuntimeError(f"Official artwork source failed: {url}: {exc}") from exc


def write_deployable_inventory(records):
    """The public asset table lists files only; text-only fallback records stay in the identity manifest."""
    return ORIGINAL_WRITE_INVENTORY([record for record in records if record.get("asset_path")])


base.fetch = fetch_official_artwork
base.write_inventory = write_deployable_inventory
raise SystemExit(base.main())
