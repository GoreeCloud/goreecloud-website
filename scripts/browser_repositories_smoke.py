#!/usr/bin/env python3
"""Exercise rebuilt repositories.html on the exact deployed preview.

This validates the current five-product development-focus page and shared shell.
It does not substitute for the separate human mobile visual acceptance required
for a material GoreeCloud website redesign.
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
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import verify_remote_deployment

HOST = "127.0.0.1"
PORT = 9519
BASE = f"http://{HOST}:{PORT}"
VIEWPORTS = ((1180, 900), (768, 900), (390, 844), (320, 844))
EXPECTED_REPOS = {
    "https://github.com/GoreeCloud/goreecloud-home-security",
    "https://github.com/GoreeCloud/goreecloud-home",
    "https://github.com/GoreeCloud/goreecloud-ai",
    "https://github.com/GoreeCloud/goreecloud-containers",
    "https://github.com/GoreeCloud/goreecloud-code",
}


class BrowserError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BrowserError(message)


def request(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(f"{BASE}{path}", data=body, method=method, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urlopen(req, timeout=25) as response:
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
        raise BrowserError(f"WebDriver {value.get('error')}: {value.get('message', '')}")
    return value


def chromedriver() -> str:
    for candidate in (shutil.which("chromedriver"), "/usr/local/share/chromedriver-linux64/chromedriver"):
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise BrowserError("chromedriver is unavailable on the runner")


def wait_driver() -> None:
    deadline = time.monotonic() + 15
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            status = request("GET", "/status")
            if isinstance(status, dict) and status.get("ready"):
                return
        except Exception as error:
            last = error
        time.sleep(.2)
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


def set_viewport(session_id: str, width: int, height: int) -> None:
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
        window.scrollTo(0,0); return {width:window.innerWidth,height:window.innerHeight};
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
        const header=q('.site-header');
        const hero=q('.page-hero');
        const headerRect=header?.getBoundingClientRect();
        const heroRect=hero?.getBoundingClientRect();
        const cards=[...document.querySelectorAll('.repo-card')].filter(el=>getComputedStyle(el).display!=='none');
        const cardRects=cards.map(el=>el.getBoundingClientRect());
        const links=cards.map(el=>el.href);
        const buttons=[...document.querySelectorAll('.button,.appearance-toggle,.nav-toggle,.primary-nav a')]
          .filter(el=>getComputedStyle(el).display!=='none').map(el=>el.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0);
        return {
          ready:document.readyState,
          title:document.title,
          width:window.innerWidth,
          height:window.innerHeight,
          scrollWidth:document.documentElement.scrollWidth,
          headerPosition:header?getComputedStyle(header).position:'',
          headerTop:headerRect?.top||0,
          headerBottom:headerRect?.bottom||0,
          heroTop:heroRect?.top||0,
          heroFont:parseFloat(style('.page-hero h1')?.fontSize||'0'),
          gridTracks:style('.repo-grid')?.gridTemplateColumns||'',
          cards:cards.length,
          links,
          minCardWidth:cardRects.length?Math.min(...cardRects.map(r=>r.width)):0,
          minTargetHeight:buttons.length?Math.min(...buttons.map(r=>r.height)):0,
          statusCards:document.querySelectorAll('.status-stack .card').length,
          navDisplay:style('.primary-nav')?.display||'',
          navToggleDisplay:style('.nav-toggle')?.display||'',
        };
        """,
    )
    require(isinstance(state, dict), f"Repository page state was not readable: {state!r}")
    return state


def validate_nav(session_id: str, width: int) -> None:
    nav = execute(
        session_id,
        """
        const toggle=document.querySelector('.nav-toggle');
        const el=document.querySelector('.primary-nav');
        const before=getComputedStyle(el).display;
        if(toggle && toggle.getAttribute('aria-expanded')!=='true') toggle.click();
        const style=getComputedStyle(el);
        const rect=el.getBoundingClientRect();
        const links=[...el.querySelectorAll('a')].map(a=>a.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0);
        return {
          before,
          after:style.display,
          expanded:toggle?.getAttribute('aria-expanded')||'',
          left:rect.left,
          right:rect.right,
          minHeight:links.length?Math.min(...links.map(r=>r.height)):0,
        };
        """,
    )
    require(isinstance(nav, dict), f"Repository mobile navigation state unreadable at {width}px")
    require(nav.get("before") == "none", f"Repository navigation was not initially collapsed at {width}px: {nav}")
    require(nav.get("after") in {"flex", "grid", "block"}, f"Repository navigation did not open at {width}px: {nav}")
    require(nav.get("expanded") == "true", f"Repository navigation aria-expanded did not update at {width}px: {nav}")
    require(float(nav.get("minHeight", 0)) >= 47.5, f"Repository navigation target below 48px at {width}px: {nav}")
    require(float(nav.get("left", -1)) >= -1 and float(nav.get("right", width+2)) <= width+1, f"Repository navigation overflows at {width}px: {nav}")


def exercise(session_id: str, target_url: str) -> None:
    request("POST", f"/session/{session_id}/timeouts", {"implicit": 0, "pageLoad": 15000, "script": 10000})
    request("POST", f"/session/{session_id}/url", {"url": target_url})

    for requested_width, requested_height in VIEWPORTS:
        set_viewport(session_id, requested_width, requested_height)
        state = read_state(session_id)
        width = int(state.get("width", 0))
        height = int(state.get("height", 0))
        require(abs(width-requested_width) <= 1, f"Repository CSS viewport is {width}px; expected {requested_width}px")
        require(abs(height-requested_height) <= 1, f"Repository CSS viewport height is {height}px; expected {requested_height}px")
        require(state.get("ready") == "complete", f"Repository page did not finish loading at {width}px: {state}")
        require(state.get("title") == "Repositories — GoreeCloud", f"Unexpected repository page title: {state}")
        require(int(state.get("cards", 0)) == 5, f"Repository focus page did not render exactly five product cards at {width}px: {state}")
        require(set(state.get("links") or []) == EXPECTED_REPOS, f"Repository focus links drifted at {width}px: {state}")
        require(int(state.get("statusCards", 0)) == 3, f"Repository status semantics are incomplete at {width}px: {state}")
        require(int(state.get("scrollWidth", width+2)) <= width+1, f"Repository page horizontally overflows at {width}px: {state}")
        require(state.get("headerPosition") == "sticky", f"Repository page does not use the shared sticky header at {width}px: {state}")
        require(float(state.get("headerTop", -2)) >= -1, f"Repository header begins outside viewport at {width}px: {state}")
        require(float(state.get("heroTop", 0))+1 >= float(state.get("headerBottom", 0)), f"Repository hero is obscured by header at {width}px: {state}")
        require(float(state.get("heroFont", 0)) >= 40, f"Repository hero type became too small at {width}px: {state}")

        expected_columns = 2 if width > 700 else 1
        require(track_count(str(state.get("gridTracks", ""))) == expected_columns, f"Repository grid is not {expected_columns} columns at {width}px: {state}")
        require(float(state.get("minCardWidth", 0)) >= min(width * .82, 270), f"Repository cards became unreasonably narrow at {width}px: {state}")

        if width <= 980:
            require(state.get("navToggleDisplay") != "none", f"Repository navigation toggle is hidden at {width}px: {state}")
            require(state.get("navDisplay") == "none", f"Repository collapsed navigation is unexpectedly open at {width}px: {state}")
            validate_nav(session_id, width)


def run(target: str) -> int:
    base_url = verify_remote_deployment.target_url(target)
    target_url = urljoin(base_url.rstrip("/")+"/", "repositories.html")
    process: subprocess.Popen[bytes] | None = None
    log_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="goreecloud-repositories-chromedriver-", suffix=".log", delete=False) as log:
            log_path = log.name
            process = subprocess.Popen([chromedriver(), f"--port={PORT}", "--allowed-ips=127.0.0.1"], stdout=log, stderr=subprocess.STDOUT)
        wait_driver()
        last: Exception | None = None
        for attempt in range(2):
            session_id: str | None = None
            try:
                session_id = create_session()
                exercise(session_id, target_url)
                print(f"Rebuilt repository focus Chrome smoke passed for {target}: {target_url}")
                return 0
            except Exception as error:
                last = error
                if attempt == 0:
                    print(f"Chrome session failed before repository responsive acceptance; retrying fresh: {error}")
            finally:
                if session_id:
                    try:
                        request("DELETE", f"/session/{session_id}")
                    except Exception:
                        pass
        raise BrowserError(str(last))
    except Exception as error:
        print(f"Rebuilt repository focus Chrome smoke failed for {target}: {target_url}")
        print(f"- {error}")
        if log_path:
            try:
                log_text = Path(log_path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                log_text = ""
            if log_text:
                print(log_text[-8000:])
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
