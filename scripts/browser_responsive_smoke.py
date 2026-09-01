#!/usr/bin/env python3
"""Exercise the public GoreeCloud homepage at screenshot-relevant viewport widths."""

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
    req = Request(f"{BASE}{path}", data=body, method=method, headers={"Content-Type": "application/json; charset=utf-8"})
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
    decoded = json.loads(raw.decode("utf-8"))
    value = decoded.get("value")
    if isinstance(value, dict) and value.get("error"):
        raise BrowserError(f"WebDriver {value.get('error')} for {path}: {value.get('message', '')}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BrowserError(message)


def driver_binary() -> str:
    candidates = [
        shutil.which("chromedriver"),
        "/usr/local/share/chromedriver-linux64/chromedriver",
    ]
    for candidate in candidates:
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
        except Exception as error:  # bounded startup polling only
            last = error
        time.sleep(0.2)
    raise BrowserError(f"chromedriver did not become ready: {last}")


def create_session() -> str:
    value = request(
        "POST",
        "/session",
        {
            "capabilities": {
                "alwaysMatch": {
                    "browserName": "chrome",
                    "goog:chromeOptions": {
                        "args": [
                            "--headless=new",
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-background-networking",
                            "--disable-component-update",
                            "--disable-default-apps",
                            "--disable-extensions",
                            "--disable-sync",
                            "--metrics-recording-only",
                            "--no-first-run",
                            "--window-size=1180,900",
                        ]
                    },
                }
            }
        },
    )
    require(isinstance(value, dict), f"Unexpected Chrome session response: {value!r}")
    session_id = value.get("sessionId")
    require(isinstance(session_id, str) and bool(session_id), f"Chrome did not return a session id: {value!r}")
    return session_id


def execute(session_id: str, script: str) -> Any:
    return request("POST", f"/session/{session_id}/execute/sync", {"script": script, "args": []})


def set_viewport(session_id: str, width: int, height: int) -> None:
    request("POST", f"/session/{session_id}/window/rect", {"width": width, "height": height, "x": 0, "y": 0})


def exercise(session_id: str, url: str) -> None:
    request("POST", f"/session/{session_id}/timeouts", {"implicit": 0, "pageLoad": 15000, "script": 10000})
    request("POST", f"/session/{session_id}/url", {"url": url})

    for width, height in VIEWPORTS:
        set_viewport(session_id, width, height)
        state = execute(
            session_id,
            """
            const width=window.innerWidth;
            const header=document.querySelector('.site-header');
            const headerStyle=header?getComputedStyle(header):null;
            const hero=document.querySelector('#top');
            const heroRect=hero?.getBoundingClientRect();
            const headerRect=header?.getBoundingClientRect();
            const q=s=>document.querySelector(s);
            const columns=s=>{const el=q(s);return el?getComputedStyle(el).gridTemplateColumns:''};
            return {
              ready:document.readyState,
              width,
              scrollWidth:document.documentElement.scrollWidth,
              headerPosition:headerStyle?.position||'',
              headerBottom:headerRect?.bottom||0,
              heroTop:heroRect?.top||0,
              websiteColumns:columns('.website-grid'),
              howColumns:columns('.how-flow'),
              platformColumns:columns('.platform-grid'),
              roadmapColumns:columns('.roadmap-grid'),
              socialColumns:columns('.social-grid'),
              statColumns:columns('.repository-teaser-stats'),
              heroFont:parseFloat(getComputedStyle(q('.hero h1')).fontSize),
            };
            """,
        )
        require(isinstance(state, dict), f"Could not read responsive state at {width}px: {state!r}")
        require(state.get("ready") == "complete", f"Homepage did not finish loading at {width}px: {state}")
        require(int(state.get("scrollWidth", width + 10)) <= int(state.get("width", width)) + 1, f"Horizontal overflow at {width}px: {state}")
        require(state.get("headerPosition") not in {"fixed", "sticky"}, f"Public header overlays content at {width}px: {state}")
        require(float(state.get("heroTop", 0)) + 1 >= float(state.get("headerBottom", 0)), f"Hero begins beneath an overlapping header at {width}px: {state}")
        require(float(state.get("heroFont", 0)) >= 40, f"Hero type became too small at {width}px: {state}")

        if width <= 820:
            require(" " not in str(state.get("websiteColumns", "")).strip(), f"Website directory did not collapse to one column at {width}px: {state}")
        if width <= 600:
            for key in ("howColumns", "platformColumns", "roadmapColumns", "socialColumns", "statColumns"):
                columns = str(state.get(key, "")).strip()
                require(columns and " " not in columns, f"{key} did not collapse to one column at {width}px: {state}")

        if width <= 390:
            nav_state = execute(
                session_id,
                """
                const toggle=document.querySelector('.nav-toggle');
                if(toggle && !toggle.getAttribute('aria-expanded')?.includes('true')) toggle.click();
                const nav=document.querySelector('.site-nav');
                const links=[...document.querySelectorAll('.site-nav a')];
                const style=nav?getComputedStyle(nav):null;
                const rect=nav?.getBoundingClientRect();
                return {
                  display:style?.display||'',
                  position:style?.position||'',
                  columns:style?.gridTemplateColumns||'',
                  left:rect?.left||0,
                  right:rect?.right||0,
                  minLinkHeight:links.length?Math.min(...links.map(a=>a.getBoundingClientRect().height)):0,
                  expanded:toggle?.getAttribute('aria-expanded')||'',
                };
                """,
            )
            require(isinstance(nav_state, dict), f"Could not read mobile navigation at {width}px")
            require(nav_state.get("position") == "static", f"Mobile navigation is not in flow at {width}px: {nav_state}")
            require(float(nav_state.get("minLinkHeight", 0)) >= 47.5, f"Mobile navigation target below 48px at {width}px: {nav_state}")
            require(float(nav_state.get("left", -1)) >= -1 and float(nav_state.get("right", width + 2)) <= width + 1, f"Mobile navigation overflows viewport at {width}px: {nav_state}")
            if width <= 320:
                require(" " not in str(nav_state.get("columns", "")).strip(), f"320px navigation did not collapse to one column: {nav_state}")


def run(target: str) -> int:
    url = verify_remote_deployment.target_url(target)
    log_path: str | None = None
    process: subprocess.Popen[bytes] | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="goreecloud-main-chromedriver-", suffix=".log", delete=False) as log_file:
            log_path = log_file.name
            process = subprocess.Popen([driver_binary(), f"--port={PORT}", "--allowed-ips=127.0.0.1"], stdout=log_file, stderr=subprocess.STDOUT)
        wait_for_driver()
        last_error: Exception | None = None
        for attempt in range(2):
            session_id: str | None = None
            try:
                session_id = create_session()
                exercise(session_id, url)
                print(f"Main responsive Chrome smoke passed for {target}: {url}")
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
        print(f"Main responsive Chrome smoke failed for {target}: {url}")
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
                process.kill()
                process.wait(timeout=5)
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
