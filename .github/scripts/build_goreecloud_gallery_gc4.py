#!/usr/bin/env python3
"""Apply GoreeCloud Gallery gc.4 Glaze UI surface refinements after gc.3."""

from __future__ import annotations

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

GALLERY_COMMIT = "b28299dc33821eee8d108a9880ce87876cf31443"
COMMONS_COMMIT = "acfd352df1a1852d17a5f77def8b7ad6e522a5b6"
VERSION_NAME = "1.0.0-gc.4"
VERSION_CODE = "10004"


def fail(message: str) -> None:
    raise SystemExit(f"gc.4 patch failed: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def verify_checkout(root: Path, expected: str, label: str) -> None:
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != expected:
        fail(f"{label} checkout is {actual}, expected {expected}")


def patch_version(gallery: Path) -> None:
    props = gallery / "gradle.properties"
    text = read(props)
    text, name_count = re.subn(
        r"^VERSION_NAME=.*$", f"VERSION_NAME={VERSION_NAME}", text, count=1, flags=re.M
    )
    text, code_count = re.subn(
        r"^VERSION_CODE=.*$", f"VERSION_CODE={VERSION_CODE}", text, count=1, flags=re.M
    )
    if name_count != 1 or code_count != 1:
        fail("could not advance Gallery version metadata")
    write(props, text)


def add_glaze_settings_card(gallery: Path) -> None:
    drawable = """<?xml version="1.0" encoding="utf-8"?>
<ripple xmlns:android="http://schemas.android.com/apk/res/android"
    android:color="#185865F2">
    <item>
        <shape android:shape="rectangle">
            <solid android:color="@color/glaze_surface" />
            <corners android:radius="16dp" />
            <stroke android:width="1dp" android:color="#185865F2" />
        </shape>
    </item>
    <item android:id="@android:id/mask">
        <shape android:shape="rectangle">
            <solid android:color="#FFFFFFFF" />
            <corners android:radius="16dp" />
        </shape>
    </item>
</ripple>
"""
    write(gallery / "app/src/main/res/drawable/glaze_settings_row_background.xml", drawable)


def patch_settings_rows(gallery: Path) -> None:
    settings = gallery / "app/src/main/res/layout/activity_settings.xml"
    text = read(settings)

    # The upstream screen is a flat edge-to-edge preference list. Keep the information
    # hierarchy and behavior, but give interactive rows Glaze UI spacing, surfaces and depth.
    pattern = re.compile(
        r'(?P<head><(?:RelativeLayout|androidx\.constraintlayout\.widget\.ConstraintLayout)\n'
        r'\s+android:id="@\+id/settings_[^"]+_holder"\n'
        r'\s+style="@style/SettingsHolder[^"]+")'
    )

    def add_card(match: re.Match[str]) -> str:
        return match.group("head") + "\n" + (
            '                android:layout_marginStart="12dp"\n'
            '                android:layout_marginTop="3dp"\n'
            '                android:layout_marginEnd="12dp"\n'
            '                android:layout_marginBottom="3dp"\n'
            '                android:background="@drawable/glaze_settings_row_background"\n'
            '                android:elevation="1dp"'
        )

    text, count = pattern.subn(add_card, text)
    if count < 20:
        fail(f"expected at least 20 Settings rows to receive Glaze cards, found {count}")

    scroll_anchor = '        android:fillViewport="true"\n        android:scrollbars="none"'
    scroll_replacement = (
        '        android:fillViewport="true"\n'
        '        android:clipToPadding="false"\n'
        '        android:paddingBottom="20dp"\n'
        '        android:scrollbars="none"'
    )
    if scroll_anchor not in text:
        fail("Settings NestedScrollView shape changed")
    text = text.replace(scroll_anchor, scroll_replacement, 1)
    write(settings, text)


def patch_customization_rows(commons: Path) -> None:
    customization = commons / "commons/src/main/res/layout/activity_customization.xml"
    text = read(customization)

    for holder_id in ("customization_theme_holder", "customization_font_holder"):
        pattern = re.compile(
            rf'(?P<head><RelativeLayout\n\s+android:id="@\+id/{holder_id}"\n'
            r'\s+style="@style/SettingsHolderTextViewStyle")'
        )
        replacement = (
            r'\g<head>\n'
            '                android:layout_marginStart="12dp"\n'
            '                android:layout_marginEnd="12dp"\n'
            '                android:layout_marginBottom="4dp"\n'
            '                android:background="@drawable/glaze_settings_row_background"\n'
            '                android:elevation="1dp"'
        )
        text, count = pattern.subn(replacement, text, count=1)
        if count != 1:
            fail(f"could not Glaze-style {holder_id}")

    scroll_anchor = '        android:fillViewport="true"\n        android:scrollbars="none"'
    scroll_replacement = (
        '        android:fillViewport="true"\n'
        '        android:clipToPadding="false"\n'
        '        android:paddingBottom="20dp"\n'
        '        android:scrollbars="none"'
    )
    if scroll_anchor not in text:
        fail("Customization NestedScrollView shape changed")
    text = text.replace(scroll_anchor, scroll_replacement, 1)
    write(customization, text)


def patch_popup_surfaces(commons: Path) -> None:
    light = commons / "commons/src/main/res/drawable/top_popup_menu_bg_light.xml"
    dark = commons / "commons/src/main/res/drawable/top_popup_menu_bg_dark.xml"

    light_xml = """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <shape android:shape="rectangle">
            <solid android:color="#F7F8FC" />
            <corners android:radius="20dp" />
            <stroke android:width="1dp" android:color="#1F5865F2" />
            <padding android:left="4dp" android:top="10dp" android:right="4dp" android:bottom="10dp" />
        </shape>
    </item>
</layer-list>
"""
    dark_xml = """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <shape android:shape="rectangle">
            <solid android:color="#171C29" />
            <corners android:radius="20dp" />
            <stroke android:width="1dp" android:color="#338995FF" />
            <padding android:left="4dp" android:top="10dp" android:right="4dp" android:bottom="10dp" />
        </shape>
    </item>
</layer-list>
"""
    write(light, light_xml)
    write(dark, dark_xml)


def patch_notice(gallery: Path) -> None:
    notice = f"""GoreeCloud Gallery {VERSION_NAME}\n\nGoreeCloud Gallery is a GoreeCloud-maintained Android gallery fork based on Fossify Gallery\n1.13.1 and Fossify Commons 6.1.5. It remains offline-first and adds no analytics,\nadvertising, cloud account, remote API, or Internet permission.\n\ngc.4 is the first post-gc.3 Glaze UI acceptance refinement. Real-device gc.3 testing confirmed\nthat the counterfeit-build dialog is gone, launcher-color identity leakage is gone, and the\nSettings/customization app-bar correction works. gc.4 preserves those fixes while converting\ninteractive Settings and Appearance rows from a flat edge-to-edge list into softly elevated,\nrounded Glaze surfaces with intentional spacing. The top overflow popup is also moved from\nthe upstream 8dp Material panel to a 20dp rounded GoreeCloud surface with restrained border\ndepth. No Gallery feature behavior or media-storage behavior is intentionally changed.\n\nUpstream copyright, source history, GNU GPL licensing, and third-party notices remain\napplicable. GoreeCloud rebranding does not remove those obligations.\n"""
    write(gallery / "GOREECLOUD-NOTICE.md", notice)
    write(gallery / "app/src/main/assets/goreecloud_notice.txt", notice)


def validate(gallery: Path, commons: Path) -> None:
    props = read(gallery / "gradle.properties")
    settings = read(gallery / "app/src/main/res/layout/activity_settings.xml")
    customization = read(commons / "commons/src/main/res/layout/activity_customization.xml")
    popup_light = read(commons / "commons/src/main/res/drawable/top_popup_menu_bg_light.xml")
    popup_dark = read(commons / "commons/src/main/res/drawable/top_popup_menu_bg_dark.xml")

    checks = [
        (f"VERSION_NAME={VERSION_NAME}", props),
        (f"VERSION_CODE={VERSION_CODE}", props),
        ('@drawable/glaze_settings_row_background', settings),
        ('android:elevation="1dp"', settings),
        ('@drawable/glaze_settings_row_background', customization),
        ('android:radius="20dp"', popup_light),
        ('android:radius="20dp"', popup_dark),
        ('#F7F8FC', popup_light),
        ('#171C29', popup_dark),
    ]
    for needle, haystack in checks:
        if needle not in haystack:
            fail(f"validation missing {needle!r}")

    if settings.count('@drawable/glaze_settings_row_background') < 20:
        fail("too few Settings rows received Glaze card treatment")

    # Validate every XML resource directly changed or created by gc.4.
    for xml_file in (
        gallery / "app/src/main/res/drawable/glaze_settings_row_background.xml",
        gallery / "app/src/main/res/layout/activity_settings.xml",
        commons / "commons/src/main/res/layout/activity_customization.xml",
        commons / "commons/src/main/res/drawable/top_popup_menu_bg_light.xml",
        commons / "commons/src/main/res/drawable/top_popup_menu_bg_dark.xml",
    ):
        try:
            ET.parse(xml_file)
        except ET.ParseError as exc:
            fail(f"invalid XML in {xml_file}: {exc}")


def main() -> None:
    if len(sys.argv) != 3:
        fail("usage: build_goreecloud_gallery_gc4.py <gallery-root> <commons-root>")
    gallery = Path(sys.argv[1]).resolve()
    commons = Path(sys.argv[2]).resolve()
    verify_checkout(gallery, GALLERY_COMMIT, "Gallery")
    verify_checkout(commons, COMMONS_COMMIT, "Commons")
    patch_version(gallery)
    add_glaze_settings_card(gallery)
    patch_settings_rows(gallery)
    patch_customization_rows(commons)
    patch_popup_surfaces(commons)
    patch_notice(gallery)
    validate(gallery, commons)
    print(f"Applied GoreeCloud Gallery {VERSION_NAME} Glaze UI refinements")


if __name__ == "__main__":
    main()
