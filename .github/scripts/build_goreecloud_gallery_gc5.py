#!/usr/bin/env python3
"""Apply GoreeCloud Gallery gc.5 acceptance, Glaze UI, and readiness hardening."""

from __future__ import annotations

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

GALLERY_COMMIT = "b28299dc33821eee8d108a9880ce87876cf31443"
COMMONS_COMMIT = "acfd352df1a1852d17a5f77def8b7ad6e522a5b6"
VERSION_NAME = "1.0.0-gc.5"
VERSION_CODE = "10005"
LIGHT_TEXT = "#14213D"
DARK_TEXT = "#F5F7FC"
FAKE_WARNING = "You are using a fake version of the app"
FAKE_WARNING_SUFFIX = "download the original one from www.fossify.org. Thanks"


def fail(message: str) -> None:
    raise SystemExit(f"gc.5 patch failed: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        fail(f"expected one occurrence in {path}: {old!r}; found {count}")
    write(path, text.replace(old, new, 1))


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


def patch_noncompose_counterfeit_boundary(commons: Path) -> None:
    """Close the legacy Activity warning path missed by the earlier Compose-only fixes."""
    base_activity = commons / "commons/src/main/kotlin/org/fossify/commons/activities/BaseSimpleActivity.kt"
    replace_once(
        base_activity,
        '''        if (!packageName.startsWith("org.fossify.", true)) {
            if ((0..50).random() == 10 || baseConfig.appRunCount % 100 == 0) {
                showModdedAppWarning()
            }
        }
''',
        '''        if (!packageName.startsWith("org.fossify.", true) &&
            !packageName.startsWith("com.goreecloud.", true)
        ) {
            if ((0..50).random() == 10 || baseConfig.appRunCount % 100 == 0) {
                showModdedAppWarning()
            }
        }
''',
    )

    # This Commons checkout is included only to build GoreeCloud Gallery. Remove the legacy
    # upstream counterfeit dialog implementation entirely so it cannot reappear through a
    # secondary call site or a future refactor within this pinned source baseline.
    activity = commons / "commons/src/main/kotlin/org/fossify/commons/extensions/Activity.kt"
    text = read(activity)
    pattern = re.compile(
        r'''fun BaseSimpleActivity\.showModdedAppWarning\(\) \{\n.*?\n\}\n\nfun Activity\.checkAppSideloading''',
        re.S,
    )
    replacement = '''fun BaseSimpleActivity.showModdedAppWarning() {
    // GoreeCloud maintained fork: upstream counterfeit-build promotion is intentionally disabled.
}

fun Activity.checkAppSideloading'''
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        fail("could not remove legacy non-Compose counterfeit dialog")
    write(activity, text)


def patch_popup_theme_selection(commons: Path) -> None:
    styling = commons / "commons/src/main/kotlin/org/fossify/commons/extensions/Context-styling.kt"
    replace_once(
        styling,
        '''fun Context.getPopupMenuTheme(): Int {
    return if (isDynamicTheme()) {
        if (isSystemInDarkMode()) {
            R.style.AppTheme_YouPopupMenuStyle
        } else {
            R.style.AppTheme_YouPopupMenuStyle_Light
        }
    } else if (isWhiteTheme()) {
        R.style.AppTheme_PopupMenuLightStyle
    } else {
        R.style.AppTheme_PopupMenuDarkStyle
    }
}
''',
        '''fun Context.getPopupMenuTheme(): Int {
    if (packageName.startsWith("com.goreecloud.", true)) {
        // Glaze light surfaces are intentionally off-white, so isWhiteTheme() is not a safe
        // light/dark discriminator for GoreeCloud. Choose popup contrast from the actual surface.
        return if (getProperBackgroundColor().getContrastColor() == Color.WHITE) {
            R.style.AppTheme_PopupMenuDarkStyle
        } else {
            R.style.AppTheme_PopupMenuLightStyle
        }
    }

    return if (isDynamicTheme()) {
        if (isSystemInDarkMode()) {
            R.style.AppTheme_YouPopupMenuStyle
        } else {
            R.style.AppTheme_YouPopupMenuStyle_Light
        }
    } else if (isWhiteTheme()) {
        R.style.AppTheme_PopupMenuLightStyle
    } else {
        R.style.AppTheme_PopupMenuDarkStyle
    }
}
''',
    )

    styles = commons / "commons/src/main/res/values/styles.xml"
    replace_once(
        styles,
        '''    <style name="AppTheme.PopupMenuDarkStyle" parent="ThemeOverlay.AppCompat.Dark">
        <item name="android:popupMenuStyle">@style/AppTheme.PopupMenuDark</item>
    </style>
''',
        f'''    <style name="AppTheme.PopupMenuDarkStyle" parent="ThemeOverlay.AppCompat.Dark">
        <item name="android:popupMenuStyle">@style/AppTheme.PopupMenuDark</item>
        <item name="popupMenuStyle">@style/AppTheme.PopupMenuDark</item>
        <item name="android:textColorPrimary">{DARK_TEXT}</item>
        <item name="android:textColorSecondary">{DARK_TEXT}</item>
        <item name="android:textColor">{DARK_TEXT}</item>
    </style>
''',
    )
    replace_once(
        styles,
        '''    <style name="AppTheme.PopupMenuLightStyle" parent="ThemeOverlay.AppCompat.Light">
        <item name="android:popupMenuStyle">@style/AppTheme.PopupMenuLight</item>
    </style>
''',
        f'''    <style name="AppTheme.PopupMenuLightStyle" parent="ThemeOverlay.AppCompat.Light">
        <item name="android:popupMenuStyle">@style/AppTheme.PopupMenuLight</item>
        <item name="popupMenuStyle">@style/AppTheme.PopupMenuLight</item>
        <item name="android:textColorPrimary">{LIGHT_TEXT}</item>
        <item name="android:textColorSecondary">{LIGHT_TEXT}</item>
        <item name="android:textColor">{LIGHT_TEXT}</item>
    </style>
''',
    )


def patch_rounded_thumbnail_defaults(gallery: Path) -> None:
    config = gallery / "app/src/main/kotlin/org/fossify/gallery/helpers/Config.kt"
    replace_once(
        config,
        '''    var folderStyle: Int
        get() = prefs.getInt(FOLDER_THUMBNAIL_STYLE, FOLDER_STYLE_SQUARE)
        set(folderStyle) = prefs.edit().putInt(FOLDER_THUMBNAIL_STYLE, folderStyle).apply()
''',
        '''    var folderStyle: Int
        get() = prefs.getInt(FOLDER_THUMBNAIL_STYLE, FOLDER_STYLE_ROUNDED_CORNERS)
        set(folderStyle) = prefs.edit().putInt(FOLDER_THUMBNAIL_STYLE, folderStyle).apply()
''',
    )
    replace_once(
        config,
        '''    var fileRoundedCorners: Boolean
        get() = prefs.getBoolean(FILE_ROUNDED_CORNERS, false)
        set(fileRoundedCorners) = prefs.edit().putBoolean(FILE_ROUNDED_CORNERS, fileRoundedCorners).apply()
''',
        '''    var fileRoundedCorners: Boolean
        get() = prefs.getBoolean(FILE_ROUNDED_CORNERS, true)
        set(fileRoundedCorners) = prefs.edit().putBoolean(FILE_ROUNDED_CORNERS, fileRoundedCorners).apply()
''',
    )


def patch_notice(gallery: Path) -> None:
    notice = f"""GoreeCloud Gallery {VERSION_NAME}

GoreeCloud Gallery is a GoreeCloud-maintained Android gallery fork based on Fossify Gallery
1.13.1 and Fossify Commons 6.1.5. It remains offline-first and adds no analytics,
advertising, cloud account, remote API, or Internet permission.

gc.5 is a real-device acceptance and release-readiness hardening pass. It closes the legacy
non-Compose counterfeit-build warning path that remained reachable in gc.4, preserves the
existing Compose-side GoreeCloud boundary, and removes the legacy warning implementation
from the Commons source included in this APK. Popup menus now select light or dark Glaze
styling from the actual GoreeCloud surface contrast rather than Fossify's pure-white theme test,
with explicit readable menu text colors. Folder thumbnails and media thumbnails now default
to rounded corners while preserving a user's explicit later choice. The accepted gc.4 rounded
Settings-card treatment and dialog geometry remain in place.

The build pipeline validates the exact pinned upstream revisions, source transformations,
Android compilation, unit tests, Android lint, package identity, offline permission boundary,
all packaged DEX files for the removed counterfeit warning, licensing files, and SHA-256 output.

Upstream copyright, source history, GNU GPL licensing, and third-party notices remain
applicable. GoreeCloud rebranding does not remove those obligations.
"""
    write(gallery / "GOREECLOUD-NOTICE.md", notice)
    write(gallery / "app/src/main/assets/goreecloud_notice.txt", notice)


def validate_no_counterfeit_runtime(commons: Path) -> None:
    runtime_root = commons / "commons/src/main"
    offenders: list[Path] = []
    for path in runtime_root.rglob("*"):
        if path.is_file() and path.suffix in {".kt", ".java", ".xml"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if FAKE_WARNING in text or FAKE_WARNING_SUFFIX in text:
                offenders.append(path)
    if offenders:
        joined = ", ".join(str(path.relative_to(commons)) for path in offenders)
        fail(f"upstream counterfeit warning remains in runtime sources: {joined}")


def validate(gallery: Path, commons: Path) -> None:
    props = read(gallery / "gradle.properties")
    config = read(gallery / "app/src/main/kotlin/org/fossify/gallery/helpers/Config.kt")
    base_activity = read(commons / "commons/src/main/kotlin/org/fossify/commons/activities/BaseSimpleActivity.kt")
    activity = read(commons / "commons/src/main/kotlin/org/fossify/commons/extensions/Activity.kt")
    styling = read(commons / "commons/src/main/kotlin/org/fossify/commons/extensions/Context-styling.kt")
    styles = read(commons / "commons/src/main/res/values/styles.xml")

    checks = [
        (f"VERSION_NAME={VERSION_NAME}", props),
        (f"VERSION_CODE={VERSION_CODE}", props),
        ('!packageName.startsWith("com.goreecloud.", true)', base_activity),
        ('upstream counterfeit-build promotion is intentionally disabled', activity),
        ('packageName.startsWith("com.goreecloud.", true)', styling),
        ('getProperBackgroundColor().getContrastColor() == Color.WHITE', styling),
        ('R.style.AppTheme_PopupMenuLightStyle', styling),
        ('R.style.AppTheme_PopupMenuDarkStyle', styling),
        (f'<item name="android:textColorPrimary">{LIGHT_TEXT}</item>', styles),
        (f'<item name="android:textColorPrimary">{DARK_TEXT}</item>', styles),
        ('prefs.getInt(FOLDER_THUMBNAIL_STYLE, FOLDER_STYLE_ROUNDED_CORNERS)', config),
        ('prefs.getBoolean(FILE_ROUNDED_CORNERS, true)', config),
    ]
    for needle, haystack in checks:
        if needle not in haystack:
            fail(f"validation missing {needle!r}")

    validate_no_counterfeit_runtime(commons)

    for xml_file in (
        commons / "commons/src/main/res/values/styles.xml",
        commons / "commons/src/main/res/drawable/top_popup_menu_bg_light.xml",
        commons / "commons/src/main/res/drawable/top_popup_menu_bg_dark.xml",
        gallery / "app/src/main/res/layout/activity_settings.xml",
    ):
        try:
            ET.parse(xml_file)
        except ET.ParseError as exc:
            fail(f"invalid XML in {xml_file}: {exc}")


def main() -> None:
    if len(sys.argv) != 3:
        fail("usage: build_goreecloud_gallery_gc5.py <gallery-root> <commons-root>")
    gallery = Path(sys.argv[1]).resolve()
    commons = Path(sys.argv[2]).resolve()
    verify_checkout(gallery, GALLERY_COMMIT, "Gallery")
    verify_checkout(commons, COMMONS_COMMIT, "Commons")
    patch_version(gallery)
    patch_noncompose_counterfeit_boundary(commons)
    patch_popup_theme_selection(commons)
    patch_rounded_thumbnail_defaults(gallery)
    patch_notice(gallery)
    validate(gallery, commons)
    print(f"Applied GoreeCloud Gallery {VERSION_NAME} acceptance and readiness hardening")


if __name__ == "__main__":
    main()
