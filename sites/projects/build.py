#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import os
import shutil
import urllib.request

SOURCE = Path(__file__).resolve().parent
DIST = SOURCE / "dist"
LOCK = json.loads((SOURCE / "glaze.lock.json").read_text(encoding="utf-8"))

if LOCK.get("product") != "GLAZE UI V1.1" or LOCK.get("version") != "1.1.0":
    raise SystemExit("Projects Glaze lock must target GLAZE UI V1.1 / 1.1.0")
if LOCK.get("release_commit") != "15cc76d2bcd4065552dc31c77145b63f34d9e7b2":
    raise SystemExit("Projects Glaze lock release commit drifted")
if LOCK.get("entrypoint") != "css/glaze-v1.1.0.css":
    raise SystemExit("Projects Glaze lock entrypoint drifted")

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data, usedforsecurity=False).hexdigest()

def read_glaze(path: str, expected: str) -> bytes:
    local_root = os.environ.get("GLAZE_UI_SOURCE")
    if local_root:
        data = (Path(local_root) / path).read_bytes()
    else:
        url = f"https://raw.githubusercontent.com/{LOCK['repository']}/{LOCK['release_commit']}/{path}"
        request = urllib.request.Request(url, headers={"User-Agent":"GoreeCloud-Projects-Build/1"})
        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read()
    actual = git_blob_sha(data)
    if actual != expected:
        raise SystemExit(f"Glaze integrity mismatch for {path}: {actual} != {expected}")
    return data

if DIST.exists():
    shutil.rmtree(DIST)
(DIST / "assets" / "glaze").mkdir(parents=True)

for name in ("index.html", "404.html", "_headers", "robots.txt", "sitemap.xml"):
    source = SOURCE / name
    if source.is_file():
        shutil.copy2(source, DIST / name)

for asset in sorted((SOURCE / "assets").iterdir()):
    if asset.name.startswith("glaze-ui-") and asset.suffix == ".css":
        continue
    target = DIST / "assets" / asset.name
    if asset.is_dir():
        shutil.copytree(asset, target)
    elif asset.is_file() and not asset.is_symlink():
        shutil.copy2(asset, target)
    else:
        raise SystemExit(f"unsafe Projects asset: {asset.name}")

for upstream_path, expected in LOCK["files"].items():
    (DIST / "assets" / "glaze" / Path(upstream_path).name).write_bytes(read_glaze(upstream_path, expected))

print(f"Built Projects public artifact with immutable GLAZE UI V1.1 / 1.1.0 source at {DIST}")
