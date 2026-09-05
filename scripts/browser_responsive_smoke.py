#!/usr/bin/env python3
"""Exercise the rebuilt public GoreeCloud homepage at representative CSS viewports.

This is automated browser evidence, not human visual acceptance. The Website
standard still requires representative-mobile human review before production
completion of this material redesign.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import verify_remote_deployment

HOST = "127.0.0.1"
PORT = 9517
BASE = f"http://{HOST}:{PORT}"
HTTP_TIMEOUT = 25
STARTUP_TIMEOUT = 15
VIEWPORTS = ((1180, 900), (768, 900), (390, 844), (320, 844))


class BrowserError(RuntimeError):
    pass


def request(method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = HTTP_TIMEOUT) -> Any:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        f"{BASE}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise BrowserError(f"WebDriver HTTP {error.code} for {path}: {detail}") from error
    except (URLError, TimeoutError) as error:
        raise BrowserError(f"WebDriver request failed for {path}: {error}") from error
    if not raw:
        return None
    value = json.loads(raw.decode("utf-8")).get("value")
    if isinstance(value, dict) and value.get("error"):
        raise BrowserError(f"WebDriver {value.get('error')} for {path}: {value.get('message', '')}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BrowserError(message)


def chromedriver() -> str:
    for candidate in (shutil.which("chromedriver"), "/usr/local/share/chromedriver-linux64/chromedriver"):
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise BrowserError("chromedriver is unavailable on the runner")


def wait_for_driver() -> None:
    deadline = time.monotonic() + STARTUP_TIMEOUT
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            status = request("GET", "/status")
            if isinstance(status, dict) and status.get("ready"):
                return
        except Exception as error:
            last = error
        time.sleep(0.2)
    raise BrowserError(f"chromedriver did not become ready: {last}")


def create_session() -> str:
    value = request(
        "POST",
        "/session",
        {"capabilities": {"alwaysMatch": {
            "browserName": "chrome",
            "goog:chromeOptions": {"args": [
                "--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
                "--disable-background-networking", "--disable-component-update",
                "--disable-default-apps", "--disable-extensions", "--disable-sync",
                "--metrics-recording-only", "--no-first-run", "--window-size=1180,900",
            ]},
        }}},
    )
    require(isinstance(value, dict), f"Unexpected Chrome session response: {value!r}")
    session_id = value.get("sessionId")
    require(isinstance(session_id, str) and bool(session_id), "Chrome did not return a session id")
    return session_id


def execute(session_id: str, script: str) -> Any:
    return request("POST", f"/session/{session_id}/execute/sync", {"script": script, "args": []})


def set_css_viewport(session_id: str, width: int, height: int) -> None:
    mobile = width <= 390
    request(
        "POST",
        f"/session/{session_id}/goog/cdp/execute",
        {"cmd": "Emulation.setDeviceMetricsOverride", "params": {
            "width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile,
        }},
    )
    request(
        "POST",
        f"/session/{session_id}/goog/cdp/execute",
        {"cmd": "Emulation.setTouchEmulationEnabled", "params": {"enabled": mobile, "maxTouchPoints": 5}},
    )
    execute(
        session_id,
        """
        const toggle=document.querySelector('.nav-toggle');
        if(toggle?.getAttribute('aria-expanded')==='true') toggle.click();
        window.scrollTo(0,0);
        return {width:window.innerWidth,height:window.innerHeight};
        """,
    )


def track_count(value: str) -> int:
    return len([part for part in value.split() if part and part != "none"])


def read_state(session_id: str) -> dict[str, Any]:
    state = execute(
        session_id,
        """
        const q=s=>document.querySelector(s);
        const style=s=>{const el=q(s);return el?getComputedStyle(el):null};
        const rect=s=>q(s)?.getBoundingClientRect()||null;
        const headerRect=rect('.site-header');
        const heroRect=rect('.hero-home');
        const targetRects=[...document.querySelectorAll('.appearance-toggle,.nav-toggle,.primary-nav a,.button')]
          .filter(el=>getComputedStyle(el).display!=='none')
          .map(el=>el.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0);
        return {
          ready:document.readyState,
          title:document.title,
          width:window.innerWidth,
          height:window.innerHeight,
          scrollWidth:document.documentElement.scrollWidth,
          headerPosition:style('.site-header')?.position||'',
          headerTop:headerRect?.top||0,
          headerBottom:headerRect?.bottom||0,
          heroTop:heroRect?.top||0,
          heroFont:parseFloat(style('.hero-copy h1')?.fontSize||'0'),
          heroTracks:style('.hero-grid')?.gridTemplateColumns||'',
          principleTracks:style('.principle-grid')?.gridTemplateColumns||'',
          destinationTracks:style('.destination-grid')?.gridTemplateColumns||'',
          splitTracks:style('.split-section')?.gridTemplateColumns||'',
          architectureTracks:style('.architecture-grid')?.gridTemplateColumns||'',
          navDisplay:style('.primary-nav')?.display||'',
          navToggleDisplay:style('.nav-toggle')?.display||'',
          minTargetHeight:targetRects.length?Math.min(...targetRects.map(r=>r.height)):0,
          systems:[...document.querySelectorAll('.system-list strong')].map(el=>el.textContent.trim()),
          destinations:document.querySelectorAll('.destination-card').length,
          principles:document.querySelectorAll('.principle-grid .card').length,
        };
        """,
    )
    require(isinstance(state, dict), f"Could not read rebuilt homepage state: {state!r}")
    return state


def validate_navigation(session_id: str, width: int) -> None:
    nav = execute(
        session_id,
        """
        const toggle=document.querySelector('.nav-toggle');
        const primary=document.querySelector('.primary-nav');
        const before=getComputedStyle(primary).display;
        if(toggle && toggle.getAttribute('aria-expanded')!=='true') toggle.click();
        const style=getComputedStyle(primary);
        const rect=primary.getBoundingClientRect();
        const links=[...primary.querySelectorAll('a')].map(a=>a.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0);
        return {
          before,
          after:style.display,
          expanded:toggle?.getAttribute('aria-expanded')||'',
          left:rect.left,
          right:rect.right,
          minLinkHeight:links.length?Math.min(...links.map(r=>r.height)):0,
          toggleHeight:toggle?.getBoundingClientRect().height||0,
        };
        """,
    )
    require(isinstance(nav, dict), f"Could not read mobile navigation at {width}px")
    require(nav.get("before") == "none", f"Mobile navigation was not closed initially at {width}px: {nav}")
    require(nav.get("after") in {"flex", "block", "grid"}, f"Mobile navigation did not become visible at {width}px: {nav}")
    require(nav.get("expanded") == "true", f"Mobile navigation aria-expanded did not update at {width}px: {nav}")
    require(float(nav.get("minLinkHeight", 0)) >= 47.5, f"Mobile navigation target below 48px at {width}px: {nav}")
    require(float(nav.get("toggleHeight", 0)) >= 47.5, f"Mobile navigation toggle below 48px at {width}px: {nav}")
    require(float(nav.get("left", -1)) >= -1 and float(nav.get("right", width+2)) <= width+1, f"Mobile navigation overflows at {width}px: {nav}")


def validate_appearance_cycle(session_id: str) -> None:
    state = execute(
        session_id,
        """
        localStorage.removeItem('goreecloud-appearance');
        delete document.documentElement.dataset.glzAppearance;
        const button=document.querySelector('.appearance-toggle');
        const values=[];
        for(let i=0;i<3;i++){
          button.click();
          values.push({
            appearance:document.documentElement.dataset.glzAppearance||'system',
            stored:localStorage.getItem('goreecloud-appearance'),
            label:button.textContent.trim(),
          });
        }
        return values;
        """,
    )
    require(isinstance(state, list) and len(state) == 3, f"Appearance cycle was unreadable: {state}")
    require(state[0].get("appearance") == "light" and state[0].get("stored") == "light", f"Light appearance did not persist correctly: {state}")
    require(state[1].get("appearance") == "dark" and state[1].get("stored") == "dark", f"Dark appearance did not persist correctly: {state}")
    require(state[2].get("appearance") == "system" and state[2].get("stored") is None, f"System appearance did not clear persistence: {state}")


def exercise(session_id: str, url: str) -> None:
    request("POST", f"/session/{session_id}/timeouts", {"implicit": 0, "pageLoad": 15000, "script": 10000})
    request("POST", f"/session/{session_id}/url", {"url": url})
    validate_appearance_cycle(session_id)

    for requested_width, requested_height in VIEWPORTS:
        set_css_viewport(session_id, requested_width, requested_height)
        state = read_state(session_id)
        width = int(state.get("width", 0))
        height = int(state.get("height", 0))
        require(abs(width-requested_width) <= 1, f"Chrome CSS viewport is {width}px; expected {requested_width}px: {state}")
        require(abs(height-requested_height) <= 1, f"Chrome CSS viewport height is {height}px; expected {requested_height}px: {state}")
        require(state.get("ready") == "complete", f"Homepage did not finish loading at {width}px: {state}")
        require(state.get("title") == "GoreeCloud — Owner-Controlled Computing", f"Unexpected homepage title: {state}")
        require(int(state.get("scrollWidth", width+10)) <= width+1, f"Horizontal overflow at {width}px: {state}")
        require(state.get("headerPosition") == "sticky", f"Shared header is not the intended sticky shell at {width}px: {state}")
        require(float(state.get("headerTop", -2)) >= -1, f"Sticky header begins outside the viewport at {width}px: {state}")
        require(float(state.get("heroTop", 0))+1 >= float(state.get("headerBottom", 0)), f"Hero is obscured by the sticky header at {width}px: {state}")
        require(float(state.get("heroFont", 0)) >= 40, f"Hero type became too small at {width}px: {state}")
        require(int(state.get("destinations", 0)) == 6, f"Expected six public destination cards at {width}px: {state}")
        require(int(state.get("principles", 0)) == 4, f"Expected four platform principles at {width}px: {state}")
        require(len(state.get("systems") or []) == 7 and "GoreeCloud Manager" in (state.get("systems") or []), f"Seven Integral Platform Systems are not rendered at {width}px: {state}")

        desktop = width > 980
        compact = width <= 700
        require(track_count(str(state.get("heroTracks", ""))) == (2 if desktop else 1), f"Hero grid is wrong at {width}px: {state}")
        require(track_count(str(state.get("splitTracks", ""))) == (2 if desktop else 1), f"Platform-system split is wrong at {width}px: {state}")
        require(track_count(str(state.get("architectureTracks", ""))) == (2 if desktop else 1), f"Architecture grid is wrong at {width}px: {state}")
        expected_principles = 4 if desktop else (1 if compact else 2)
        expected_destinations = 3 if desktop else (1 if compact else 2)
        require(track_count(str(state.get("principleTracks", ""))) == expected_principles, f"Principle grid is not {expected_principles} columns at {width}px: {state}")
        require(track_count(str(state.get("destinationTracks", ""))) == expected_destinations, f"Destination grid is not {expected_destinations} columns at {width}px: {state}")

        if width <= 980:
            require(state.get("navToggleDisplay") != "none", f"Mobile/tablet navigation toggle is hidden at {width}px: {state}")
            require(state.get("navDisplay") == "none", f"Collapsed navigation is unexpectedly open at {width}px: {state}")
            validate_navigation(session_id, width)


def run(target: str) -> int:
    url = verify_remote_deployment.target_url(target)
    process: subprocess.Popen[bytes] | None = None
    log_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="goreecloud-main-chromedriver-", suffix=".log", delete=False) as log_file:
            log_path = log_file.name
            process = subprocess.Popen([chromedriver(), f"--port={PORT}", "--allowed-ips=127.0.0.1"], stdout=log_file, stderr=subprocess.STDOUT)
        wait_for_driver()
        last_error: Exception | None = None
        for attempt in range(2):
            session_id: str | None = None
            try:
                session_id = create_session()
                exercise(session_id, url)
                print(f"Rebuilt Main responsive Chrome smoke passed for {target}: {url}")
                return 0
            except Exception as error:
                last_error = error
                if attempt == 0:
                    print(f"Chrome session failed before responsive acceptance; retrying with a fresh session: {error}")
            finally:
                if session_id:
                    try:
                        request("DELETE", f"/session/{session_id}")
                    except Exception:
                        pass
        raise BrowserError(str(last_error))
    except Exception as error:
        print(f"Rebuilt Main responsive Chrome smoke failed for {target}: {url}")
        print(f"- {error}")
        if log_path:
            try:
                text = Path(log_path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            if text:
                print(text[-8000:])
        return 1
    finally:
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait(timeout=5)
        if log_path:
            try:
                Path(log_path).unlink()
            except OSError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=("branch-preview", "production"), required=True)
    args = parser.parse_args()
    return run(args.target)


if __name__ == "__main__":
    raise SystemExit(main())
