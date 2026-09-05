#!/usr/bin/env python3
"""Fetch the exact current Stable GLAZE UI V1.1 web bundle for same-origin publication."""
from __future__ import annotations

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import re

GLAZE_VERSION = "1.1.0"
GLAZE_SOURCE_REVISION = "15cc76d2bcd4065552dc31c77145b63f34d9e7b2"
BASE_URL = f"https://raw.githubusercontent.com/GoreeCloud/goreecloud-glaze-ui/{GLAZE_SOURCE_REVISION}/css"
FILES = (
    "glaze-v1.1.0.css",
    "glaze-v1.0.0.css",
    "glaze-v1.foundation.css",
    "glaze-v1.components.css",
    "glaze-v1.components.adaptive.css",
    "glaze-v1.components.runtime.css",
    "glaze-v1.structure.css",
    "glaze-v1.overlay.css",
    "glaze-v1.advanced.css",
    "glaze-v1.visual-refinement.css",
    "glaze-v1.optical-reachability.css",
    "glaze-v1.1.css",
    "glaze-v1.1-appearance.css",
)


def _imports(text: str) -> set[str]:
    return set(re.findall(r'@import\s+url\(["\']\./([^"\']+)["\']\)', text))


def validate_bundle(bundle: dict[str, str]) -> None:
    missing = sorted(set(FILES) - set(bundle))
    if missing:
        raise ValueError("GLAZE V1.1 bundle is incomplete: " + ", ".join(missing))

    entry = bundle["glaze-v1.1.0.css"]
    if "official Stable web entrypoint" not in entry:
        raise ValueError("GLAZE V1.1 Stable entrypoint marker is missing")
    expected_entry = {"glaze-v1.0.0.css", "glaze-v1.1.css", "glaze-v1.1-appearance.css"}
    if _imports(entry) != expected_entry:
        raise ValueError("GLAZE V1.1 Stable entrypoint import closure changed unexpectedly")

    v10 = bundle["glaze-v1.0.0.css"]
    expected_v10 = {
        "glaze-v1.foundation.css", "glaze-v1.components.css", "glaze-v1.components.adaptive.css",
        "glaze-v1.components.runtime.css", "glaze-v1.structure.css", "glaze-v1.overlay.css",
        "glaze-v1.advanced.css", "glaze-v1.visual-refinement.css", "glaze-v1.optical-reachability.css",
    }
    if _imports(v10) != expected_v10:
        raise ValueError("GLAZE V1.0 inherited import closure changed unexpectedly")

    v11 = bundle["glaze-v1.1.css"]
    if "GLAZE UI V1.1" not in v11 or 'html[data-glaze-version="1.1"]' not in v11:
        raise ValueError("GLAZE V1.1 optical layer markers are missing")

    appearance = bundle["glaze-v1.1-appearance.css"]
    for marker in ('data-glz-appearance="light"', 'data-glz-appearance="dark"', 'forced-colors: active'):
        if marker not in appearance:
            raise ValueError(f"GLAZE V1.1 appearance marker is missing: {marker}")

    for name, text in bundle.items():
        if not text.strip():
            raise ValueError(f"Downloaded GLAZE source is empty: {name}")
        if "raw.githubusercontent.com" in text or "https://" in text or "http://" in text:
            raise ValueError(f"GLAZE runtime CSS must not introduce remote resources: {name}")
        unexpected = _imports(text) - set(FILES)
        if unexpected:
            raise ValueError(f"GLAZE CSS imports an unpinned file from {name}: {sorted(unexpected)}")


def fetch_bundle(timeout: float = 20.0) -> dict[str, str]:
    bundle: dict[str, str] = {}
    for name in FILES:
        request = Request(f"{BASE_URL}/{name}", headers={"User-Agent": "GoreeCloud-Website-Build/1.1"})
        try:
            with urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    raise ValueError(f"Unexpected HTTP status for {name}: {response.status}")
                raw = response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            raise ValueError(f"Unable to fetch pinned GLAZE source {name}: {exc}") from exc
        try:
            bundle[name] = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Pinned GLAZE source is not UTF-8: {name}") from exc
    validate_bundle(bundle)
    return bundle


def install_glaze(destination: Path) -> tuple[Path, ...]:
    bundle = fetch_bundle()
    destination.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        raise ValueError("GLAZE destination must not be a symlink")
    written: list[Path] = []
    for name in FILES:
        path = destination / name
        path.write_text(bundle[name], encoding="utf-8")
        written.append(path)
    return tuple(written)
