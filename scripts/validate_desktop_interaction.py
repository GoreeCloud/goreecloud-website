#!/usr/bin/env python3
"""Validate deployed keyboard navigation and zoom-equivalent reflow behavior.

This verifier complements ``validate_desktop_rendering.py``. It exercises the exact
reviewed GoreeCloud deployment in the same dependency-free Chrome/ChromeDriver
browser harness, using real W3C WebDriver key actions instead of JavaScript focus
simulation.

The checks cover objective portions of the remaining desktop acceptance boundary:
keyboard focus order, skip-link operation, compact navigation keyboard operation,
and horizontal reflow at CSS viewport widths equivalent to 400% zoom from the
representative 1280- and 1600-pixel desktop acceptance widths. Human review is
still required for subjective focus feel, reading comfort, visual hierarchy, and
screen-reader experience.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from validate_desktop_rendering import Driver, WebDriverError, find_chromedriver
from verify_remote_deployment import target_url, validate_fixed_url

TAB = "\ue004"
ENTER = "\ue007"
DESKTOP_VIEWPORTS = ((1280, 900), (1600, 1000))
REFLOW_VIEWPORTS = (
    (320, 900, "1280px at 400% zoom"),
    (400, 1000, "1600px at 400% zoom"),
)


def press_key(driver: Driver, key: str) -> None:
    """Send one real keyboard key through the W3C WebDriver actions endpoint."""

    driver.command(
        "POST",
        "/actions",
        {
            "actions": [
                {
                    "type": "key",
                    "id": "keyboard",
                    "actions": [
                        {"type": "keyDown", "value": key},
                        {"type": "keyUp", "value": key},
                    ],
                }
            ]
        },
    )
    driver.command("DELETE", "/actions")


def active_element(driver: Driver) -> dict[str, Any]:
    return driver.execute(
        r"""
const element = document.activeElement;
if (!element) return {};
const rect = element.getBoundingClientRect();
return {
  tag: element.tagName.toLowerCase(),
  id: element.id || '',
  className: typeof element.className === 'string' ? element.className : '',
  href: element.getAttribute('href') || '',
  ariaExpanded: element.getAttribute('aria-expanded'),
  width: rect.width,
  height: rect.height,
  top: rect.top,
  bottom: rect.bottom,
  display: getComputedStyle(element).display,
  visibility: getComputedStyle(element).visibility,
  hash: location.hash
};
"""
    )


def reset_page(driver: Driver, base_url: str, width: int, height: int) -> None:
    driver.command(
        "POST",
        "/window/rect",
        {"width": width, "height": height, "x": 0, "y": 0},
    )
    driver.command("POST", "/url", {"url": base_url})
    driver.execute(
        "window.scrollTo(0, 0); if (document.activeElement) document.activeElement.blur(); return true;"
    )


def focus_identity(snapshot: dict[str, Any]) -> str:
    return "|".join(
        (
            str(snapshot.get("tag") or ""),
            str(snapshot.get("id") or ""),
            str(snapshot.get("className") or ""),
            str(snapshot.get("href") or ""),
        )
    )


def validate_desktop_keyboard(
    driver: Driver,
    base_url: str,
    width: int,
    height: int,
    errors: list[str],
) -> None:
    label = f"{width}x{height}/keyboard"
    reset_page(driver, base_url, width, height)

    press_key(driver, TAB)
    first = active_element(driver)
    if "skip-link" not in str(first.get("className") or ""):
        errors.append(
            f"{label}: first keyboard focus target is not the skip link: {focus_identity(first)!r}."
        )
    if float(first.get("width") or 0) <= 0 or float(first.get("height") or 0) <= 0:
        errors.append(f"{label}: skip link is not visibly rendered when focused.")
    if float(first.get("top") or -9999) < -1:
        errors.append(
            f"{label}: focused skip link remains outside the viewport at top={first.get('top')!r}."
        )

    press_key(driver, ENTER)
    skip_result = active_element(driver)
    if skip_result.get("hash") != "#main":
        errors.append(
            f"{label}: activating the skip link did not navigate to #main; hash={skip_result.get('hash')!r}."
        )

    reset_page(driver, base_url, width, height)
    snapshots: list[dict[str, Any]] = []
    for _ in range(18):
        press_key(driver, TAB)
        snapshot = active_element(driver)
        snapshots.append(snapshot)
        if float(snapshot.get("width") or 0) <= 0 or float(snapshot.get("height") or 0) <= 0:
            errors.append(
                f"{label}: keyboard focus reached a zero-size target: {focus_identity(snapshot)!r}."
            )
            break
        if snapshot.get("display") == "none" or snapshot.get("visibility") == "hidden":
            errors.append(
                f"{label}: keyboard focus reached a hidden target: {focus_identity(snapshot)!r}."
            )
            break

    identities = [focus_identity(item) for item in snapshots]
    unique = {identity for identity in identities if identity.strip("|")}
    if len(unique) < 10:
        errors.append(
            f"{label}: keyboard traversal reached only {len(unique)} unique targets in 18 Tab presses."
        )

    if not any("brand" in str(item.get("className") or "") for item in snapshots):
        errors.append(f"{label}: keyboard traversal did not reach the GoreeCloud brand link.")

    nav_hrefs = {
        "#services",
        "#platform",
        "#development",
        "#roadmap",
        "#about",
        "#follow",
        "#contact",
    }
    if not any(str(item.get("href") or "") in nav_hrefs for item in snapshots):
        errors.append(f"{label}: keyboard traversal did not reach primary navigation links.")
    if not any("button" in str(item.get("className") or "").split() for item in snapshots):
        errors.append(f"{label}: keyboard traversal did not reach a hero action button/link.")

    print(
        f"Keyboard {label}: skip-link passed; "
        f"{len(unique)} unique focus targets sampled without hidden/zero-size focus."
    )


def reflow_metrics(driver: Driver) -> dict[str, Any]:
    return driver.execute(
        r"""
const rect = selector => {
  const element = document.querySelector(selector);
  if (!element) return null;
  const value = element.getBoundingClientRect();
  return {left:value.left, right:value.right, width:value.width, height:value.height};
};
const gridColumns = selector => {
  const element = document.querySelector(selector);
  if (!element) return 0;
  const value = getComputedStyle(element).gridTemplateColumns.trim();
  return value ? value.split(/\s+/).filter(Boolean).length : 0;
};
const navToggle = document.querySelector('.nav-toggle');
const siteNav = document.querySelector('.site-nav');
return {
  innerWidth: window.innerWidth,
  clientWidth: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth,
  heroColumns: gridColumns('.hero-grid'),
  heroCard: rect('.hero-card'),
  contactCard: rect('.contact-card'),
  navToggleDisplay: navToggle ? getComputedStyle(navToggle).display : null,
  navToggleRect: rect('.nav-toggle'),
  siteNavDisplay: siteNav ? getComputedStyle(siteNav).display : null,
  siteNavExpanded: navToggle ? navToggle.getAttribute('aria-expanded') : null,
  widestButton: Math.max(0, ...Array.from(document.querySelectorAll('.button')).map(element => element.getBoundingClientRect().width))
};
"""
    )


def validate_reflow(
    driver: Driver,
    base_url: str,
    width: int,
    height: int,
    equivalent: str,
    errors: list[str],
) -> None:
    label = f"{width}x{height}/reflow ({equivalent})"
    reset_page(driver, base_url, width, height)
    metrics = reflow_metrics(driver)
    client_width = int(metrics.get("clientWidth") or 0)
    scroll_width = int(metrics.get("scrollWidth") or 0)

    if client_width <= 0:
        errors.append(f"{label}: browser client width is invalid: {client_width}px.")
        return
    if scroll_width > client_width + 1:
        errors.append(
            f"{label}: horizontal overflow detected: scrollWidth={scroll_width}, clientWidth={client_width}."
        )
    if int(metrics.get("heroColumns") or 0) != 1:
        errors.append(
            f"{label}: hero did not reflow to one column; rendered {metrics.get('heroColumns')} columns."
        )
    if metrics.get("navToggleDisplay") == "none":
        errors.append(f"{label}: compact navigation toggle is not visible.")
    if metrics.get("siteNavDisplay") != "none":
        errors.append(
            f"{label}: compact navigation should start collapsed; display={metrics.get('siteNavDisplay')!r}."
        )

    for key, human in (("heroCard", "hero card"), ("contactCard", "contact card")):
        rect = metrics.get(key) or {}
        if float(rect.get("right") or 0) > client_width + 1 or float(rect.get("left") or 0) < -1:
            errors.append(
                f"{label}: {human} extends beyond the reflow viewport: {json.dumps(rect, sort_keys=True)}."
            )
    if float(metrics.get("widestButton") or 0) > client_width + 1:
        errors.append(
            f"{label}: an action button is wider than the reflow viewport ({metrics.get('widestButton')}px)."
        )

    driver.execute(
        "window.scrollTo(0, 0); if (document.activeElement) document.activeElement.blur(); return true;"
    )
    toggle_found = False
    for _ in range(8):
        press_key(driver, TAB)
        snapshot = active_element(driver)
        if "nav-toggle" in str(snapshot.get("className") or ""):
            toggle_found = True
            break
    if not toggle_found:
        errors.append(f"{label}: Tab traversal did not reach the compact navigation toggle.")
    else:
        press_key(driver, ENTER)
        expanded = reflow_metrics(driver)
        if expanded.get("siteNavExpanded") != "true":
            errors.append(
                f"{label}: Enter did not set nav toggle aria-expanded=true; "
                f"value={expanded.get('siteNavExpanded')!r}."
            )
        if expanded.get("siteNavDisplay") == "none":
            errors.append(f"{label}: Enter did not reveal the compact navigation.")
        press_key(driver, TAB)
        next_target = driver.execute(
            "return Boolean(document.activeElement && document.activeElement.closest('#site-nav'));"
        )
        if next_target is not True:
            errors.append(
                f"{label}: keyboard focus did not move into the revealed primary navigation after the toggle."
            )

    print(
        f"Reflow {label}: clientWidth={client_width}px scrollWidth={scroll_width}px; "
        "single-column hero and keyboard-operable compact navigation checked."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=("branch-preview", "production"),
        required=True,
        help="Reviewed GoreeCloud deployment target to exercise.",
    )
    args = parser.parse_args()

    base_url = target_url(args.target)
    validate_fixed_url(base_url)
    executable = find_chromedriver()
    errors: list[str] = []
    driver: Driver | None = None

    try:
        driver = Driver(executable)
        for width, height in DESKTOP_VIEWPORTS:
            validate_desktop_keyboard(driver, base_url, width, height, errors)
        for width, height, equivalent in REFLOW_VIEWPORTS:
            validate_reflow(driver, base_url, width, height, equivalent, errors)
    except (RuntimeError, WebDriverError) as error:
        errors.append(str(error))
    finally:
        if driver is not None:
            driver.close()

    if errors:
        print("Desktop interaction/reflow validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Desktop interaction/reflow validation passed for {args.target}: "
        "real keyboard traversal, skip-link behavior, compact-nav keyboard operation, "
        "and 400%-zoom-equivalent reflow are healthy."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
