#!/usr/bin/env python3
"""Capture reviewable desktop rendering evidence from a reviewed deployment target.

The deployed desktop validator intentionally keeps its screenshots ephemeral. This helper
performs a second, read-only browser pass after validation and writes representative viewport
PNGs, Wide full-page Light/Dark PNGs, and a compact JSON manifest into
``artifacts/desktop-rendering/<target>`` so GitHub Actions can preserve them for short-lived
human review.

Only the fixed GoreeCloud branch-preview and production targets exposed by
``verify_remote_deployment.py`` are accepted. No arbitrary URL input is supported.
"""

from __future__ import annotations

import argparse
import base64
import json
from hashlib import sha256
from pathlib import Path
import shutil
import sys
import time
from typing import Any

from validate_desktop_rendering import (
    APPEARANCE_MODES,
    VIEWPORTS,
    Driver,
    WebDriverError,
    apply_appearance,
    collect_metrics,
    find_chromedriver,
    png_dimensions,
)
from verify_remote_deployment import target_url, validate_fixed_url

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "artifacts" / "desktop-rendering"
THEME_SETTLE_SECONDS = 0.4
FULL_PAGE_MIN_WIDTH = 1440
FULL_PAGE_MODES = {"light", "dark"}


def decode_png(value: str, label: str) -> tuple[bytes, int, int, str]:
    screenshot = base64.b64decode(value, validate=True)
    shot_width, shot_height = png_dimensions(screenshot)
    if len(screenshot) < 20_000:
        raise RuntimeError(f"{label}: screenshot payload is unexpectedly small.")
    return screenshot, shot_width, shot_height, sha256(screenshot).hexdigest()


def capture_viewport(
    driver: Driver,
    output_dir: Path,
    width: int,
    height: int,
    mode: str,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    label = f"{width}x{height}/{mode}"
    screenshot_value = driver.command("GET", "/screenshot")
    if not isinstance(screenshot_value, str):
        raise RuntimeError(f"{label}: browser did not return screenshot data.")

    screenshot, shot_width, shot_height, digest = decode_png(screenshot_value, label)
    filename = f"{width}x{height}-{mode}.png"
    (output_dir / filename).write_bytes(screenshot)

    hero = metrics.get("heroCard") or {}
    container = metrics.get("container") or {}
    return {
        "file": filename,
        "kind": "viewport",
        "viewport": {"width": width, "height": height},
        "appearance": mode,
        "png": {
            "width": shot_width,
            "height": shot_height,
            "bytes": len(screenshot),
            "sha256": digest,
        },
        "layout": {
            "innerWidth": metrics.get("innerWidth"),
            "clientWidth": metrics.get("clientWidth"),
            "scrollWidth": metrics.get("scrollWidth"),
            "contentMax": metrics.get("contentMax"),
            "containerWidth": container.get("width"),
            "heroWidth": hero.get("width"),
            "heroHeight": hero.get("height"),
            "serviceColumns": metrics.get("serviceColumns"),
            "developmentColumns": metrics.get("developmentColumns"),
            "socialColumns": metrics.get("socialColumns"),
        },
    }


def capture_full_page(
    driver: Driver,
    output_dir: Path,
    width: int,
    height: int,
    mode: str,
) -> dict[str, Any]:
    label = f"{width}x{height}/{mode}/full-page"
    result = driver.command(
        "POST",
        "/goog/cdp/execute",
        {
            "cmd": "Page.captureScreenshot",
            "params": {
                "format": "png",
                "fromSurface": True,
                "captureBeyondViewport": True,
            },
        },
    )
    screenshot_value = result.get("data") if isinstance(result, dict) else None
    if not isinstance(screenshot_value, str):
        raise RuntimeError(f"{label}: Chrome did not return full-page screenshot data.")

    screenshot, shot_width, shot_height, digest = decode_png(screenshot_value, label)
    if shot_height <= height + 500:
        raise RuntimeError(
            f"{label}: full-page screenshot height {shot_height}px does not exceed the "
            "viewport enough to represent the complete homepage."
        )
    filename = f"{width}x{height}-{mode}-full.png"
    (output_dir / filename).write_bytes(screenshot)
    return {
        "file": filename,
        "kind": "full-page",
        "viewport": {"width": width, "height": height},
        "appearance": mode,
        "png": {
            "width": shot_width,
            "height": shot_height,
            "bytes": len(screenshot),
            "sha256": digest,
        },
    }


def capture(
    driver: Driver,
    base_url: str,
    output_dir: Path,
    width: int,
    height: int,
    mode: str,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    driver.command(
        "POST",
        "/window/rect",
        {"width": width, "height": height, "x": 0, "y": 0},
    )
    driver.command("POST", "/url", {"url": base_url})
    apply_appearance(driver, mode)
    # Theme-sensitive controls intentionally animate between appearance modes. Wait until
    # those reviewed Glaze UI transitions settle so preserved evidence reflects the steady
    # state rather than an intermediate frame between Light and Dark values.
    time.sleep(THEME_SETTLE_SECONDS)
    metrics = collect_metrics(driver)

    viewport = capture_viewport(driver, output_dir, width, height, mode, metrics)
    full_page = None
    if width >= FULL_PAGE_MIN_WIDTH and mode in FULL_PAGE_MODES:
        full_page = capture_full_page(driver, output_dir, width, height, mode)
    return viewport, full_page


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=("branch-preview", "production"),
        required=True,
        help="Reviewed GoreeCloud deployment target to capture.",
    )
    args = parser.parse_args()

    base_url = target_url(args.target)
    validate_fixed_url(base_url)
    output_dir = EVIDENCE_ROOT / args.target
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    driver: Driver | None = None
    screenshots: list[dict[str, Any]] = []
    full_page_screenshots: list[dict[str, Any]] = []
    try:
        driver = Driver(find_chromedriver())
        for width, height, _gutter, _content_max, _hero_min_height in VIEWPORTS:
            for mode in APPEARANCE_MODES:
                viewport, full_page = capture(
                    driver, base_url, output_dir, width, height, mode
                )
                screenshots.append(viewport)
                if full_page is not None:
                    full_page_screenshots.append(full_page)
    except (RuntimeError, WebDriverError, ValueError) as error:
        print(f"Desktop render evidence capture failed: {error}")
        return 1
    finally:
        if driver is not None:
            driver.close()

    manifest = {
        "schemaVersion": 2,
        "target": args.target,
        "baseUrl": base_url,
        "themeSettleSeconds": THEME_SETTLE_SECONDS,
        "screenshots": screenshots,
        "fullPageScreenshots": full_page_screenshots,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        f"Captured {len(screenshots)} desktop viewport screenshots and "
        f"{len(full_page_screenshots)} Wide full-page screenshots for {args.target} "
        f"in {output_dir.relative_to(ROOT)} after {THEME_SETTLE_SECONDS:.1f}s theme settling."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
