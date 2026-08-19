#!/usr/bin/env python3
"""Setup-only wrapper for the v5.23 official-artwork exporter."""
from __future__ import annotations
from io import BytesIO
import zipfile
import v523_base as base

ORIGINAL_FETCH = base.fetch
ONLYOFFICE_ZIP = "https://www.onlyoffice.com/images/templates/press-downloads/logo/files/logo_symbol.zip"
STIRLING_OLD = "https://raw.githubusercontent.com/Stirling-Tools/Stirling-PDF/ec3de16c0862c01190bf45896bae87e9f0e10ca7/frontend/editor/public/modern-logo/logo192.png"
STIRLING_OFFICIAL = "https://raw.githubusercontent.com/Stirling-Tools/Stirling-PDF/ec3de16c0862c01190bf45896bae87e9f0e10ca7/app/core/src/main/resources/static/modern-logo/logo192.png"


def fetch_official_artwork(url: str) -> bytes:
    try:
        if url == "https://www.onlyoffice.com/favicon.ico":
            raw = ORIGINAL_FETCH(ONLYOFFICE_ZIP)
            with zipfile.ZipFile(BytesIO(raw)) as archive:
                names = [name for name in archive.namelist() if name.lower().endswith(".svg") and not name.endswith("/")]
                if not names:
                    raise RuntimeError("ONLYOFFICE official symbol archive did not contain an SVG asset")
                return archive.read(sorted(names, key=lambda n: ("symbol" not in n.lower(), len(n), n.lower()))[0])
        if url == STIRLING_OLD:
            return ORIGINAL_FETCH(STIRLING_OFFICIAL)
        return ORIGINAL_FETCH(url)
    except Exception as exc:
        raise RuntimeError(f"Official artwork source failed: {url}: {exc}") from exc


base.fetch = fetch_official_artwork
raise SystemExit(base.main())
