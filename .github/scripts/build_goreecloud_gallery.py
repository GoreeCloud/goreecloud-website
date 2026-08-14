#!/usr/bin/env python3
"""Apply the GoreeCloud Gallery gc.1 patchset to Fossify Gallery 1.13.1.

This script intentionally keeps the upstream Kotlin namespace intact while giving the
installable application a GoreeCloud package identity. It performs only deterministic,
reviewable source transformations and fails closed when the expected upstream source
shape is not present.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

EXPECTED_UPSTREAM_COMMIT = "b28299dc33821eee8d108a9880ce87876cf31443"
APP_ID = "com.goreecloud.gallery"
APP_NAME = "GoreeCloud Gallery"
VERSION_NAME = "1.0.0-gc.1"
VERSION_CODE = "10001"
GLAZE_PRIMARY = "#5865F2"
GLAZE_ACCENT = "#8B5CF6"


def fail(message: str) -> None:
    raise SystemExit(f"goreecloud-gallery patch failed: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing expected file: {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        fail(f"expected exactly one occurrence in {path}: {old!r}; found {count}")
    write(path, text.replace(old, new, 1))


def replace_regex_once(path: Path, pattern: str, replacement: str) -> None:
    text = read(path)
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        fail(f"expected regex once in {path}: {pattern!r}; found {count}")
    write(path, updated)


def verify_upstream(root: Path) -> None:
    commit = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if commit != EXPECTED_UPSTREAM_COMMIT:
        fail(f"unexpected upstream commit {commit}; expected {EXPECTED_UPSTREAM_COMMIT}")

    license_text = read(root / "LICENSE")
    if "GNU GENERAL PUBLIC LICENSE" not in license_text or "Version 3" not in license_text:
        fail("upstream GPL-3.0 license was not found as expected")


def patch_build_identity(root: Path) -> None:
    gradle = root / "app/build.gradle.kts"
    replace_once(
        gradle,
        'applicationId = project.property("APP_ID").toString()',
        f'applicationId = "{APP_ID}"',
    )
    replace_once(
        gradle,
        'applicationIdSuffix = ".debug"',
        '// GoreeCloud: keep the debug build on the production package ID for direct APK installation.',
    )

    props = root / "gradle.properties"
    text = read(props)
    text, n1 = re.subn(r"^VERSION_NAME=.*$", f"VERSION_NAME={VERSION_NAME}", text, count=1, flags=re.MULTILINE)
    text, n2 = re.subn(r"^VERSION_CODE=.*$", f"VERSION_CODE={VERSION_CODE}", text, count=1, flags=re.MULTILINE)
    if n1 != 1 or n2 != 1:
        fail("could not update version metadata")
    # APP_ID remains org.fossify.gallery on purpose: it is the Kotlin/Android resource namespace.
    write(props, text)


def patch_branding(root: Path) -> None:
    donottranslate = root / "app/src/main/res/values/donottranslate.xml"
    replace_once(donottranslate, "<string name=\"app_name\">Fossify Gallery</string>", f"<string name=\"app_name\">{APP_NAME}</string>")
    replace_once(donottranslate, "<string name=\"package_name\">org.fossify.gallery</string>", f"<string name=\"package_name\">{APP_ID}</string>")

    # App launcher name and brand references are normalized across translations without
    # altering the surrounding translated prose.
    for strings in (root / "app/src/main/res").glob("values*/strings.xml"):
        text = read(strings)
        text = text.replace("Fossify Gallery", APP_NAME)
        text = re.sub(
            r'(<string name="app_launcher_name"[^>]*>).*?(</string>)',
            rf"\1{APP_NAME}\2",
            text,
            count=1,
        )
        write(strings, text)

    debug_strings = root / "app/src/debug/res/values/strings.xml"
    if debug_strings.exists():
        text = read(debug_strings).replace("Fossify Gallery", APP_NAME)
        text = re.sub(
            r'(<string name="app_launcher_name"[^>]*>).*?(</string>)',
            rf"\1{APP_NAME}\2",
            text,
            count=1,
        )
        write(debug_strings, text)

    manifest = root / "app/src/main/AndroidManifest.xml"
    text = read(manifest)
    text = text.replace('<package android:name="org.fossify.gallery.debug" />', f'<package android:name="{APP_ID}" />')
    text = text.replace('<package android:name="org.fossify.gallery" />', f'<package android:name="{APP_ID}" />')
    text = text.replace('android:allowBackup="true"', 'android:allowBackup="false"')
    text = text.replace('android:icon="@mipmap/ic_launcher"', 'android:icon="@drawable/ic_goreecloud_gallery"')
    text = text.replace('android:roundIcon="@mipmap/ic_launcher"', 'android:roundIcon="@drawable/ic_goreecloud_gallery"')
    write(manifest, text)


def patch_glaze_theme(root: Path) -> None:
    colors = root / "app/src/main/res/values/colors.xml"
    text = read(colors)
    insert = f"""
    <!-- GoreeCloud Glaze UI palette -->
    <color name="glaze_background">#F5F7FC</color>
    <color name="glaze_surface">#F2FFFFFF</color>
    <color name="glaze_primary">{GLAZE_PRIMARY}</color>
    <color name="glaze_accent">{GLAZE_ACCENT}</color>
    <color name="glaze_status_bar">#E8F5F7FC</color>
    <color name="glaze_navigation_bar">#F2F5F7FC</color>
"""
    if "</resources>" not in text:
        fail("colors.xml has no closing resources tag")
    write(colors, text.replace("</resources>", insert + "</resources>"))

    night_colors = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="glaze_background">#10131C</color>
    <color name="glaze_surface">#E61A1F2B</color>
    <color name="glaze_primary">#8995FF</color>
    <color name="glaze_accent">#AD8BFF</color>
    <color name="glaze_status_bar">#E810131C</color>
    <color name="glaze_navigation_bar">#F210131C</color>
</resources>
"""
    write(root / "app/src/main/res/values-night/glaze_colors.xml", night_colors)

    styles = root / "app/src/main/res/values/styles.xml"
    text = read(styles)
    text = text.replace(
        '<style name="AppTheme" parent="AppTheme.Base" />',
        '''<style name="AppTheme" parent="AppTheme.Base">
        <item name="android:windowBackground">@drawable/glaze_window_background</item>
        <item name="android:statusBarColor">@color/glaze_status_bar</item>
        <item name="android:navigationBarColor">@color/glaze_navigation_bar</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:windowLightNavigationBar">true</item>
    </style>''',
    )
    text = text.replace(
        '<item name="android:background">@android:color/transparent</item>',
        '<item name="android:background">@drawable/glaze_bottom_sheet_background</item>',
    )
    write(styles, text)

    night_styles = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="AppTheme.Base">
        <item name="android:windowBackground">@drawable/glaze_window_background</item>
        <item name="android:statusBarColor">@color/glaze_status_bar</item>
        <item name="android:navigationBarColor">@color/glaze_navigation_bar</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:windowLightNavigationBar">false</item>
    </style>
</resources>
"""
    write(root / "app/src/main/res/values-night/glaze_styles.xml", night_styles)

    window_bg = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient
        android:angle="315"
        android:startColor="@color/glaze_background"
        android:centerColor="@color/glaze_surface"
        android:endColor="@color/glaze_background" />
</shape>
"""
    write(root / "app/src/main/res/drawable/glaze_window_background.xml", window_bg)

    bottom_sheet = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <corners android:topLeftRadius="28dp" android:topRightRadius="28dp" />
    <solid android:color="@color/glaze_surface" />
    <stroke android:width="1dp" android:color="#245865F2" />
    <padding android:left="4dp" android:top="4dp" android:right="4dp" android:bottom="8dp" />
</shape>
"""
    write(root / "app/src/main/res/drawable/glaze_bottom_sheet_background.xml", bottom_sheet)

    icon = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#10131C" android:pathData="M22,8h64a14,14 0,0 1,14 14v64a14,14 0,0 1,-14 14H22A14,14 0,0 1,8 86V22A14,14 0,0 1,22 8z" />
    <path android:fillColor="#5865F2" android:pathData="M20,70L39,48l13,15 9,-10 27,29H20z" />
    <path android:fillColor="#8B5CF6" android:pathData="M20,74L39,53l13,15 9,-10 22,24H20z" />
    <path android:fillColor="#F5F7FC" android:pathData="M75,27a9,9 0,1 1,-18 0a9,9 0,1 1,18 0" />
    <path android:fillColor="#CCFFFFFF" android:pathData="M24,18h37a4,4 0,0 1,4 4v2a4,4 0,0 1,-4 4H24a4,4 0,0 1,-4 -4v-2a4,4 0,0 1,4 -4z" />
</vector>
"""
    write(root / "app/src/main/res/drawable/ic_goreecloud_gallery.xml", icon)


def patch_first_run_palette(root: Path) -> None:
    app = root / "app/src/main/kotlin/org/fossify/gallery/App.kt"
    text = read(app)
    text = text.replace(
        "package org.fossify.gallery\n\n",
        "package org.fossify.gallery\n\nimport android.graphics.Color\n",
        1,
    )
    text = text.replace(
        "import org.fossify.commons.FossifyApp\n",
        "import org.fossify.commons.FossifyApp\nimport org.fossify.gallery.helpers.Config\n",
        1,
    )
    needle = "        Reprint.initialize(this)\n"
    if needle not in text:
        fail("could not find App.onCreate initialization point")
    replacement = f'''        val glazeDefaults = getSharedPreferences("goreecloud_glaze", MODE_PRIVATE)
        if (!glazeDefaults.getBoolean("palette_applied", false)) {{
            Config.newInstance(this).apply {{
                primaryColor = Color.parseColor("{GLAZE_PRIMARY}")
                accentColor = Color.parseColor("{GLAZE_ACCENT}")
                customPrimaryColor = Color.parseColor("{GLAZE_PRIMARY}")
                customAccentColor = Color.parseColor("{GLAZE_ACCENT}")
            }}
            glazeDefaults.edit().putBoolean("palette_applied", true).apply()
        }}

        Reprint.initialize(this)
'''
    write(app, text.replace(needle, replacement, 1))


def add_notices(root: Path) -> None:
    notice = f"""GoreeCloud Gallery {VERSION_NAME}

GoreeCloud Gallery is a GoreeCloud-maintained Android gallery build based on Fossify
Gallery 1.13.1 (upstream commit {EXPECTED_UPSTREAM_COMMIT}).

The application is designed for offline-first local photo and video management. The build
patch does not add analytics, advertising, cloud accounts, remote APIs, or an Internet
permission. GoreeCloud-specific presentation changes apply the Glaze UI direction through
GoreeCloud branding, a dedicated application identity, a Glaze accent palette, layered
light/dark surfaces, rounded bottom-sheet treatment, and GoreeCloud iconography.

Upstream copyright, source history, and GNU GPL v3 licensing remain applicable and are not
removed by this build. See the upstream LICENSE file and source project for the complete
license and corresponding source baseline.
"""
    write(root / "GOREECLOUD-NOTICE.md", notice)
    assets = root / "app/src/main/assets"
    assets.mkdir(parents=True, exist_ok=True)
    write(assets / "goreecloud_notice.txt", notice)


def validate_patch(root: Path) -> None:
    gradle = read(root / "app/build.gradle.kts")
    manifest = read(root / "app/src/main/AndroidManifest.xml")
    strings = read(root / "app/src/main/res/values/strings.xml")
    donottranslate = read(root / "app/src/main/res/values/donottranslate.xml")

    required = [
        (f'applicationId = "{APP_ID}"', gradle),
        (APP_NAME, strings),
        (APP_NAME, donottranslate),
        (f'<string name="package_name">{APP_ID}</string>', donottranslate),
        ('android:allowBackup="false"', manifest),
        ('@drawable/ic_goreecloud_gallery', manifest),
    ]
    for needle, haystack in required:
        if needle not in haystack:
            fail(f"post-patch validation missing {needle!r}")

    if "android.permission.INTERNET" in manifest:
        fail("Internet permission unexpectedly present in main manifest")
    if "Fossify Gallery" in strings or "Fossify Gallery" in donottranslate:
        fail("primary English branding still contains Fossify Gallery")

    # Validate every generated XML file is at least well-formed.
    import xml.etree.ElementTree as ET
    for xml_file in [
        root / "app/src/main/res/values/colors.xml",
        root / "app/src/main/res/values/styles.xml",
        root / "app/src/main/res/values-night/glaze_colors.xml",
        root / "app/src/main/res/values-night/glaze_styles.xml",
        root / "app/src/main/res/drawable/glaze_window_background.xml",
        root / "app/src/main/res/drawable/glaze_bottom_sheet_background.xml",
        root / "app/src/main/res/drawable/ic_goreecloud_gallery.xml",
    ]:
        ET.parse(xml_file)

    print(f"Patched {APP_NAME} {VERSION_NAME} from Fossify Gallery 1.13.1")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: build_goreecloud_gallery.py <Fossify Gallery checkout>")
    root = Path(sys.argv[1]).resolve()
    verify_upstream(root)
    patch_build_identity(root)
    patch_branding(root)
    patch_glaze_theme(root)
    patch_first_run_palette(root)
    add_notices(root)
    validate_patch(root)


if __name__ == "__main__":
    main()
