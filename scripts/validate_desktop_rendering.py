#!/usr/bin/env python3
"""Validate the deployed GoreeCloud desktop layout in a real headless browser.

This verifier intentionally uses only the Python standard library plus the Chrome
and ChromeDriver binaries already present on the pinned GitHub Actions Ubuntu
runner. It accepts only the reviewed GoreeCloud deployment targets exposed by
``verify_remote_deployment.py`` and never accepts an arbitrary URL.

The rendered checks supplement, but do not replace, human visual acceptance.
They fail closed on horizontal overflow, broken images, incorrect Expanded/Wide
container geometry, undersized hero artwork, incorrect Wide collection density,
missing platform-card row density, or broken reduced-motion/contrast media
fallbacks. A screenshot is also rendered for every representative viewport and
appearance mode so the browser pipeline proves that real pixels were produced.
"""

from __future__ import annotations

import argparse
import base64
from contextlib import suppress
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import socket
import struct
import subprocess
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from verify_remote_deployment import target_url, validate_fixed_url

TIMEOUT_SECONDS = 30
VIEWPORTS = (
    (1280, 900, 32, 1280, 480),
    (1600, 1000, 40, 1480, 525),
)
APPEARANCE_MODES = ("system", "light", "dark")


class WebDriverError(RuntimeError):
    """Raised when the local ChromeDriver session returns a protocol error."""


def find_chromedriver() -> str:
    candidates: list[Path] = []
    configured = os.environ.get("CHROMEWEBDRIVER")
    if configured:
        configured_path = Path(configured)
        candidates.append(
            configured_path / "chromedriver"
            if configured_path.is_dir()
            else configured_path
        )
    candidates.extend(
        Path(path)
        for path in (
            "/usr/local/share/chromedriver-linux64/chromedriver",
            "/usr/bin/chromedriver",
        )
    )

    on_path = shutil.which("chromedriver")
    if on_path:
        candidates.insert(0, Path(on_path))

    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    raise RuntimeError(
        "ChromeDriver is unavailable. The pinned GitHub Actions runner is expected "
        "to provide it as part of the reviewed browser toolchain."
    )


def reserve_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        return int(server.getsockname()[1])


class Driver:
    def __init__(self, executable: str) -> None:
        self.port = reserve_port()
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.process = subprocess.Popen(
            [executable, f"--port={self.port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.session_id: str | None = None
        self._wait_until_ready()
        self._create_session()

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        *,
        timeout: int = TIMEOUT_SECONDS,
    ) -> Any:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            self.base_url + path,
            data=data,
            headers={"Content-Type": "application/json"},
            method=method,
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except (HTTPError, URLError) as error:
            raise WebDriverError(f"ChromeDriver request failed: {method} {path}: {error}") from error

        try:
            decoded = json.loads(body)
        except json.JSONDecodeError as error:
            raise WebDriverError(
                f"ChromeDriver returned non-JSON data for {method} {path}."
            ) from error

        value = decoded.get("value")
        if isinstance(value, dict) and value.get("error"):
            raise WebDriverError(
                f"ChromeDriver error for {method} {path}: "
                f"{value.get('error')}: {value.get('message', '')}"
            )
        return value

    def _wait_until_ready(self) -> None:
        deadline = time.monotonic() + TIMEOUT_SECONDS
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                output = self.process.stdout.read() if self.process.stdout else ""
                raise RuntimeError(
                    f"ChromeDriver exited before becoming ready. Output: {output.strip()}"
                )
            try:
                status = self._request("GET", "/status", timeout=2)
                if isinstance(status, dict) and status.get("ready"):
                    return
            except (WebDriverError, TimeoutError) as error:
                last_error = error
            time.sleep(0.2)
        raise RuntimeError(f"ChromeDriver did not become ready: {last_error}")

    def _create_session(self) -> None:
        value = self._request(
            "POST",
            "/session",
            {
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": "chrome",
                        "pageLoadStrategy": "normal",
                        "goog:chromeOptions": {
                            "args": [
                                "--headless=new",
                                "--disable-gpu",
                                "--no-sandbox",
                                "--disable-dev-shm-usage",
                            ]
                        },
                    }
                }
            },
        )
        if not isinstance(value, dict) or not value.get("sessionId"):
            raise WebDriverError("ChromeDriver did not return a session id.")
        self.session_id = str(value["sessionId"])
        self.command(
            "POST",
            "/timeouts",
            {"pageLoad": 30000, "script": 10000, "implicit": 0},
        )

    def command(
        self,
        method: str,
        suffix: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        if not self.session_id:
            raise WebDriverError("ChromeDriver session is not active.")
        return self._request(
            method,
            f"/session/{self.session_id}{suffix}",
            payload,
        )

    def execute(self, script: str) -> Any:
        return self.command(
            "POST",
            "/execute/sync",
            {"script": script, "args": []},
        )

    def emulate_media(self, features: list[dict[str, str]]) -> None:
        self.command(
            "POST",
            "/goog/cdp/execute",
            {
                "cmd": "Emulation.setEmulatedMedia",
                "params": {"features": features},
            },
        )

    def close(self) -> None:
        if self.session_id:
            with suppress(Exception):
                self._request("DELETE", f"/session/{self.session_id}")
            self.session_id = None
        if self.process.poll() is None:
            self.process.terminate()
            with suppress(subprocess.TimeoutExpired):
                self.process.wait(timeout=5)
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=5)


def png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Browser screenshot is not a valid PNG payload.")
    return struct.unpack(">II", data[16:24])


def collect_metrics(driver: Driver) -> dict[str, Any]:
    return driver.execute(
        r"""
const rect = selector => {
  const element = document.querySelector(selector);
  if (!element) return null;
  const value = element.getBoundingClientRect();
  return {left:value.left, right:value.right, top:value.top, width:value.width, height:value.height};
};
const columns = selector => {
  const element = document.querySelector(selector);
  if (!element) return 0;
  const value = getComputedStyle(element).gridTemplateColumns.trim();
  return value ? value.split(/\s+/).filter(Boolean).length : 0;
};
const platformTops = Array.from(document.querySelectorAll('.platform-card'))
  .slice(0, 4)
  .map(element => element.getBoundingClientRect().top);
const failedImages = Array.from(document.images)
  .filter(image => !image.complete || image.naturalWidth <= 0)
  .map(image => image.getAttribute('src') || '<unknown>');
const root = getComputedStyle(document.documentElement);
return {
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  scrollWidth: document.documentElement.scrollWidth,
  container: rect('.hero-grid'),
  heroCard: rect('.hero-card'),
  nav: rect('.site-nav'),
  serviceColumns: columns('.service-grid'),
  developmentColumns: columns('.development-grid'),
  socialColumns: columns('.social-grid'),
  platformTopSpread: platformTops.length >= 4 ? Math.max(...platformTops) - Math.min(...platformTops) : null,
  platformCount: document.querySelectorAll('.platform-card').length,
  failedImages,
  theme: document.documentElement.getAttribute('data-theme'),
  colorScheme: root.colorScheme,
  contentMax: root.getPropertyValue('--glaze-content-max').trim()
};
"""
    )


def apply_appearance(driver: Driver, mode: str) -> None:
    driver.execute(
        f"""
if ({json.dumps(mode)} === 'system') {{
  document.documentElement.removeAttribute('data-theme');
}} else {{
  document.documentElement.setAttribute('data-theme', {json.dumps(mode)});
}}
return document.documentElement.getAttribute('data-theme');
"""
    )


def validate_viewport(
    driver: Driver,
    base_url: str,
    width: int,
    height: int,
    gutter: int,
    content_max: int,
    hero_min_height: int,
    mode: str,
    errors: list[str],
) -> None:
    driver.command(
        "POST",
        "/window/rect",
        {"width": width, "height": height, "x": 0, "y": 0},
    )
    driver.command("POST", "/url", {"url": base_url})
    apply_appearance(driver, mode)
    metrics = collect_metrics(driver)

    label = f"{width}x{height}/{mode}"
    inner_width = int(metrics.get("innerWidth") or 0)
    if inner_width < width - 16:
        errors.append(
            f"{label}: browser viewport width is unexpectedly small: {inner_width}px."
        )

    if int(metrics.get("scrollWidth") or 0) > inner_width + 1:
        errors.append(
            f"{label}: horizontal overflow detected: scrollWidth={metrics.get('scrollWidth')} "
            f"innerWidth={inner_width}."
        )

    container = metrics.get("container") or {}
    actual_container = float(container.get("width") or 0)
    expected_container = min(max(inner_width - (2 * gutter), 0), content_max)
    if abs(actual_container - expected_container) > 2.5:
        errors.append(
            f"{label}: hero/container width is {actual_container:.1f}px; expected "
            f"approximately {expected_container}px for the semantic desktop gutter contract."
        )

    expected_token = f"{content_max}px"
    if metrics.get("contentMax") != expected_token:
        errors.append(
            f"{label}: --glaze-content-max resolved to {metrics.get('contentMax')!r}; "
            f"expected {expected_token!r}."
        )

    hero_card = metrics.get("heroCard") or {}
    if float(hero_card.get("height") or 0) + 1 < hero_min_height:
        errors.append(
            f"{label}: hero card rendered at {hero_card.get('height')}px high; "
            f"expected at least {hero_min_height}px."
        )

    min_hero_width = 420 if width < 1440 else 500
    if float(hero_card.get("width") or 0) + 1 < min_hero_width:
        errors.append(
            f"{label}: hero card rendered at {hero_card.get('width')}px wide; "
            f"expected at least {min_hero_width}px."
        )

    nav = metrics.get("nav") or {}
    if float(nav.get("right") or 0) > inner_width + 1:
        errors.append(f"{label}: primary navigation extends beyond the viewport.")

    failed_images = metrics.get("failedImages") or []
    if failed_images:
        errors.append(f"{label}: broken rendered images detected: {', '.join(failed_images)}")

    if width >= 1440:
        for key, human in (
            ("serviceColumns", "service grid"),
            ("developmentColumns", "development grid"),
            ("socialColumns", "social grid"),
        ):
            if int(metrics.get(key) or 0) != 4:
                errors.append(
                    f"{label}: {human} rendered {metrics.get(key)} columns; expected 4."
                )
        if int(metrics.get("platformCount") or 0) >= 4:
            spread = metrics.get("platformTopSpread")
            if spread is None or float(spread) > 2:
                errors.append(
                    f"{label}: the first four platform cards are not aligned on one Wide row "
                    f"(top spread {spread!r}px)."
                )

    screenshot_value = driver.command("GET", "/screenshot")
    if not isinstance(screenshot_value, str):
        errors.append(f"{label}: browser did not return screenshot data.")
        return
    try:
        screenshot = base64.b64decode(screenshot_value, validate=True)
        shot_width, shot_height = png_dimensions(screenshot)
    except (ValueError, base64.binascii.Error) as error:
        errors.append(f"{label}: invalid screenshot evidence: {error}")
        return

    if shot_width < width - 16 or shot_height < 600:
        errors.append(
            f"{label}: screenshot dimensions are unexpectedly small: "
            f"{shot_width}x{shot_height}."
        )
    if len(screenshot) < 20_000:
        errors.append(
            f"{label}: screenshot payload is unexpectedly small ({len(screenshot)} bytes)."
        )

    print(
        f"Rendered {label}: viewport={inner_width}x{metrics.get('innerHeight')} "
        f"container={actual_container:.1f}px hero={float(hero_card.get('width') or 0):.1f}x"
        f"{float(hero_card.get('height') or 0):.1f}px screenshot={shot_width}x{shot_height} "
        f"sha256={sha256(screenshot).hexdigest()[:16]}"
    )


def validate_media_fallbacks(driver: Driver, errors: list[str]) -> None:
    driver.emulate_media([{"name": "prefers-reduced-motion", "value": "reduce"}])
    reduced = driver.execute(
        r"""
const link = document.querySelector('.site-nav a');
return {
  matches: matchMedia('(prefers-reduced-motion: reduce)').matches,
  scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
  transitionDuration: link ? getComputedStyle(link).transitionDuration : null
};
"""
    )
    if not reduced.get("matches"):
        errors.append("Reduced-motion emulation did not activate the expected media query.")
    if reduced.get("scrollBehavior") != "auto":
        errors.append(
            "Reduced-motion rendering did not disable smooth scrolling on the root element."
        )
    if reduced.get("transitionDuration") not in {"0s", "0s, 0s", "0s, 0s, 0s"}:
        errors.append(
            "Reduced-motion rendering did not remove navigation transition duration: "
            f"{reduced.get('transitionDuration')!r}."
        )

    driver.emulate_media([{"name": "prefers-contrast", "value": "more"}])
    contrast = driver.execute(
        r"""
const root = getComputedStyle(document.documentElement);
return {
  matches: matchMedia('(prefers-contrast: more)').matches,
  raisedShadow: root.getPropertyValue('--glaze-shadow-raised').trim()
};
"""
    )
    if not contrast.get("matches"):
        errors.append("Increased-contrast emulation did not activate the expected media query.")
    if contrast.get("raisedShadow") != "none":
        errors.append(
            "Increased-contrast rendering did not remove raised shadows as required: "
            f"{contrast.get('raisedShadow')!r}."
        )

    driver.emulate_media([])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=("branch-preview", "production"),
        required=True,
        help="Reviewed GoreeCloud deployment target to render.",
    )
    args = parser.parse_args()

    base_url = target_url(args.target)
    validate_fixed_url(base_url)
    executable = find_chromedriver()
    errors: list[str] = []
    driver: Driver | None = None

    try:
        driver = Driver(executable)
        for width, height, gutter, content_max, hero_min_height in VIEWPORTS:
            for mode in APPEARANCE_MODES:
                validate_viewport(
                    driver,
                    base_url,
                    width,
                    height,
                    gutter,
                    content_max,
                    hero_min_height,
                    mode,
                    errors,
                )
        validate_media_fallbacks(driver, errors)
    except (RuntimeError, WebDriverError) as error:
        errors.append(str(error))
    finally:
        if driver is not None:
            driver.close()

    if errors:
        print("Rendered desktop validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Rendered desktop validation passed for {args.target}: "
        "Expanded/Wide geometry, appearance modes, image loading, overflow, "
        "reduced motion, and increased contrast are healthy."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
