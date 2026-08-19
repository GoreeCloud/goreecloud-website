#!/usr/bin/env python3
"""Setup-only wrapper for the v5.23 official-artwork exporter."""
from __future__ import annotations
from io import BytesIO
import zipfile
import v523_base as base

ORIGINAL_FETCH = base.fetch
ONLYOFFICE_ZIP = "https://www.onlyoffice.com/images/templates/press-downloads/logo/files/logo_symbol.zip"


def fetch_with_onlyoffice(url: str) -> bytes:
    if url == "https://www.onlyoffice.com/favicon.ico":
        raw = ORIGINAL_FETCH(ONLYOFFICE_ZIP)
        with zipfile.ZipFile(BytesIO(raw)) as archive:
            names = [name for name in archive.namelist() if name.lower().endswith(".svg") and not name.endswith("/")]
            if not names:
                raise SystemExit("ONLYOFFICE official symbol archive did not contain an SVG asset.")
            return archive.read(sorted(names, key=lambda n: ("symbol" not in n.lower(), len(n), n.lower()))[0])
    return ORIGINAL_FETCH(url)


base.fetch = fetch_with_onlyoffice
raise SystemExit(base.main())
