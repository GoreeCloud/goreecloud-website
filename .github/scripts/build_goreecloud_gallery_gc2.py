#!/usr/bin/env python3
"""Apply GoreeCloud Gallery gc.2 corrections after the gc.1 patchset."""

from __future__ import annotations

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

GALLERY_COMMIT = "b28299dc33821eee8d108a9880ce87876cf31443"
COMMONS_COMMIT = "acfd352df1a1852d17a5f77def8b7ad6e522a5b6"
APP_ID = "com.goreecloud.gallery"
VERSION_NAME = "1.0.0-gc.2"
VERSION_CODE = "10002"
PRIMARY = "#5865F2"
ACCENT = "#8B5CF6"
LIGHT_BG = "#F7F8FC"
LIGHT_SURFACE = "#EEF1FB"
LIGHT_TEXT = "#14213D"
DARK_BG = "#10131C"
DARK_SURFACE = "#171C29"
DARK_TEXT = "#F5F7FC"
DARK_PRIMARY = "#8995FF"
DARK_ACCENT = "#AD8BFF"


def fail(msg: str) -> None:
    raise SystemExit(f"gc.2 patch failed: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = read(path)
    if text.count(old) != 1:
        fail(f"expected one occurrence in {path}: {old!r}")
    write(path, text.replace(old, new, 1))


def verify_checkout(root: Path, expected: str, name: str) -> None:
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if actual != expected:
        fail(f"{name} checkout is {actual}, expected {expected}")


def patch_version(gallery: Path) -> None:
    props = gallery / "gradle.properties"
    text = read(props)
    text, n1 = re.subn(r"^VERSION_NAME=.*$", f"VERSION_NAME={VERSION_NAME}", text, count=1, flags=re.M)
    text, n2 = re.subn(r"^VERSION_CODE=.*$", f"VERSION_CODE={VERSION_CODE}", text, count=1, flags=re.M)
    if n1 != 1 or n2 != 1:
        fail("could not advance version metadata")
    write(props, text)


def patch_composite_build(gallery: Path) -> None:
    settings = gallery / "settings.gradle.kts"
    text = read(settings)
    marker = 'include(":app")'
    if marker not in text:
        fail("Gallery settings.gradle.kts shape changed")
    block = '''include(":app")

// GoreeCloud gc.2: build the exact Fossify Commons 6.1.5 source locally so
// legitimate fork-specific behavior and Glaze UI overrides are transparent.
includeBuild("../upstream-commons") {
    dependencySubstitution {
        substitute(module("org.fossify:commons")).using(project(":commons"))
    }
}
'''
    write(settings, text.replace(marker, block, 1))


def patch_gallery_identity(gallery: Path) -> None:
    manifest = gallery / "app/src/main/AndroidManifest.xml"
    text = read(manifest)
    text, count = re.subn(r'@mipmap/ic_launcher[^"\s]*', '@drawable/ic_goreecloud_gallery', text)
    if count < 2:
        fail("expected launcher icon aliases in Gallery manifest")
    write(manifest, text)

    foss_bools = gallery / "app/src/foss/res/values/bools.xml"
    replace_once(foss_bools, '<bool name="show_donate_in_about">true</bool>', '<bool name="show_donate_in_about">false</bool>')


def patch_gallery_palette(gallery: Path) -> None:
    app = gallery / "app/src/main/kotlin/org/fossify/gallery/App.kt"
    old = f'''        val glazeDefaults = getSharedPreferences("goreecloud_glaze", MODE_PRIVATE)
        if (!glazeDefaults.getBoolean("palette_applied", false)) {{
            Config.newInstance(this).apply {{
                primaryColor = Color.parseColor("{PRIMARY}")
                accentColor = Color.parseColor("{ACCENT}")
                customPrimaryColor = Color.parseColor("{PRIMARY}")
                customAccentColor = Color.parseColor("{ACCENT}")
            }}
            glazeDefaults.edit().putBoolean("palette_applied", true).apply()
        }}
'''
    new = f'''        val glazeDefaults = getSharedPreferences("goreecloud_glaze", MODE_PRIVATE)
        if (glazeDefaults.getInt("palette_version", 0) < 2) {{
            Config.newInstance(this).apply {{
                isSystemThemeEnabled = true
                isGlobalThemeEnabled = false
                primaryColor = Color.parseColor("{PRIMARY}")
                accentColor = Color.parseColor("{ACCENT}")
                backgroundColor = Color.parseColor("{LIGHT_BG}")
                textColor = Color.parseColor("{LIGHT_TEXT}")
                appIconColor = Color.parseColor("{PRIMARY}")
                lastIconColor = Color.parseColor("{PRIMARY}")
                customPrimaryColor = Color.parseColor("{PRIMARY}")
                customAccentColor = Color.parseColor("{ACCENT}")
                customBackgroundColor = Color.parseColor("{LIGHT_BG}")
                customTextColor = Color.parseColor("{LIGHT_TEXT}")
                customAppIconColor = Color.parseColor("{PRIMARY}")
            }}
            glazeDefaults.edit().putInt("palette_version", 2).remove("palette_applied").apply()
        }}
'''
    replace_once(app, old, new)


def patch_gallery_resources(gallery: Path) -> None:
    colors = gallery / "app/src/main/res/values/colors.xml"
    text = read(colors)
    additions = f'''
    <!-- GoreeCloud gc.2 overrides for inherited Fossify Commons resources. -->
    <color name="color_primary">{PRIMARY}</color>
    <color name="color_primary_dark">{DARK_PRIMARY}</color>
    <color name="color_accent">{ACCENT}</color>
    <color name="default_primary_color">{PRIMARY}</color>
    <color name="default_accent_color">{ACCENT}</color>
    <color name="default_app_icon_color">{PRIMARY}</color>
    <color name="default_background_color">{LIGHT_BG}</color>
    <color name="default_text_color">{LIGHT_TEXT}</color>
    <color name="glaze_surface_strong">{LIGHT_SURFACE}</color>
'''
    if "</resources>" not in text:
        fail("Gallery colors.xml has no closing resources tag")
    write(colors, text.replace("</resources>", additions + "</resources>", 1))

    night = gallery / "app/src/main/res/values-night/glaze_colors.xml"
    text = read(night)
    additions = f'''
    <color name="color_primary">{DARK_PRIMARY}</color>
    <color name="color_primary_dark">{DARK_PRIMARY}</color>
    <color name="color_accent">{DARK_ACCENT}</color>
    <color name="default_primary_color">{DARK_PRIMARY}</color>
    <color name="default_accent_color">{DARK_ACCENT}</color>
    <color name="default_app_icon_color">{PRIMARY}</color>
    <color name="default_background_color">{DARK_BG}</color>
    <color name="default_text_color">{DARK_TEXT}</color>
    <color name="glaze_surface_strong">{DARK_SURFACE}</color>
'''
    write(night, text.replace("</resources>", additions + "</resources>", 1))


def patch_commons_fake_check(commons: Path) -> None:
    activity = commons / "commons/src/main/kotlin/org/fossify/commons/compose/extensions/ActivityExtensions.kt"
    old = '''    if (!packageName.startsWith("org.fossify.", true)) {
        if ((0..50).random() == 10 || baseConfig.appRunCount % 100 == 0) {
            showConfirmationDialog()
        }
    }
'''
    new = '''    if (!packageName.startsWith("org.fossify.", true) &&
        !packageName.startsWith("com.goreecloud.", true)
    ) {
        if ((0..50).random() == 10 || baseConfig.appRunCount % 100 == 0) {
            showConfirmationDialog()
        }
    }
'''
    replace_once(activity, old, new)


def patch_commons_system_glaze(commons: Path) -> None:
    base = commons / "commons/src/main/kotlin/org/fossify/commons/helpers/BaseConfig.kt"
    text = read(base)
    text = text.replace("import android.content.res.Configuration\n", "import android.content.res.Configuration\nimport android.graphics.Color\n", 1)
    anchor = '''    companion object {
        fun newInstance(context: Context) = BaseConfig(context)
    }
'''
    helpers = '''    companion object {
        fun newInstance(context: Context) = BaseConfig(context)
    }

    private fun useGoreeCloudSystemTheme(): Boolean =
        context.packageName.startsWith("com.goreecloud.", ignoreCase = true) &&
            prefs.getBoolean(IS_SYSTEM_THEME_ENABLED, isSPlus())

    private fun isGoreeCloudDarkTheme(): Boolean =
        context.resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK == Configuration.UI_MODE_NIGHT_YES
'''
    if anchor not in text:
        fail("Commons BaseConfig class shape changed")
    text = text.replace(anchor, helpers, 1)

    replacements = {
        'get() = prefs.getInt(TEXT_COLOR, ContextCompat.getColor(context, R.color.default_text_color))':
            f'get() = if (useGoreeCloudSystemTheme()) Color.parseColor(if (isGoreeCloudDarkTheme()) "{DARK_TEXT}" else "{LIGHT_TEXT}") else prefs.getInt(TEXT_COLOR, ContextCompat.getColor(context, R.color.default_text_color))',
        'get() = prefs.getInt(BACKGROUND_COLOR, ContextCompat.getColor(context, R.color.default_background_color))':
            f'get() = if (useGoreeCloudSystemTheme()) Color.parseColor(if (isGoreeCloudDarkTheme()) "{DARK_BG}" else "{LIGHT_BG}") else prefs.getInt(BACKGROUND_COLOR, ContextCompat.getColor(context, R.color.default_background_color))',
        'get() = prefs.getInt(PRIMARY_COLOR, ContextCompat.getColor(context, R.color.default_primary_color))':
            f'get() = if (useGoreeCloudSystemTheme()) Color.parseColor(if (isGoreeCloudDarkTheme()) "{DARK_PRIMARY}" else "{PRIMARY}") else prefs.getInt(PRIMARY_COLOR, ContextCompat.getColor(context, R.color.default_primary_color))',
        'get() = prefs.getInt(ACCENT_COLOR, ContextCompat.getColor(context, R.color.default_accent_color))':
            f'get() = if (useGoreeCloudSystemTheme()) Color.parseColor(if (isGoreeCloudDarkTheme()) "{DARK_ACCENT}" else "{ACCENT}") else prefs.getInt(ACCENT_COLOR, ContextCompat.getColor(context, R.color.default_accent_color))',
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            fail(f"Commons BaseConfig expected one getter: {old}")
        text = text.replace(old, new, 1)
    write(base, text)

    styling = commons / "commons/src/main/kotlin/org/fossify/commons/extensions/Context-styling.kt"
    replace_once(
        styling,
        'fun Context.isDynamicTheme() = isSPlus() && baseConfig.isSystemThemeEnabled',
        'fun Context.isDynamicTheme() = isSPlus() && baseConfig.isSystemThemeEnabled && !packageName.startsWith("com.goreecloud.", true)',
    )

    dynamic = commons / "commons/src/main/kotlin/org/fossify/commons/compose/theme/DynamicTheme.kt"
    replace_once(dynamic, "                else -> md_green_900", "                else -> Color(primaryColorInt)")


def patch_commons_glaze_geometry(commons: Path) -> None:
    shapes = commons / "commons/src/main/kotlin/org/fossify/commons/compose/theme/Shapes.kt"
    text = read(shapes)
    old = '''val Shapes = Shapes(
    extraSmall = RoundedCornerShape(16.dp), //used by dropdown menu in M3
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(24.dp),
)'''
    new = '''val Shapes = Shapes(
    extraSmall = RoundedCornerShape(22.dp), // GoreeCloud Glaze dropdown/menu geometry
    small = RoundedCornerShape(14.dp),
    medium = RoundedCornerShape(18.dp),
    large = RoundedCornerShape(24.dp),
    extraLarge = RoundedCornerShape(30.dp),
)'''
    if old not in text:
        fail("Commons Shapes.kt shape changed")
    write(shapes, text.replace(old, new, 1))

    dialogs = commons / "commons/src/main/kotlin/org/fossify/commons/compose/alert_dialog/AlertDialogsExtensions.kt"
    text = read(dialogs)
    text = text.replace("val dialogElevation = 0.dp", "val dialogElevation = 8.dp", 1)
    old = '''fun Modifier.dialogBorder(): Modifier =
    when (LocalTheme.current) {
        is Theme.BlackAndWhite -> this.border(1.dp, light_grey_stroke, dialogShape)
        else -> this
    }
'''
    new = '''fun Modifier.dialogBorder(): Modifier =
    when {
        LocalContext.current.packageName.startsWith("com.goreecloud.", true) ->
            this.border(1.dp, Color(0x335865F2), dialogShape)
        LocalTheme.current is Theme.BlackAndWhite -> this.border(1.dp, light_grey_stroke, dialogShape)
        else -> this
    }
'''
    if old not in text:
        fail("Commons dialog border shape changed")
    write(dialogs, text.replace(old, new, 1))


def patch_notice(gallery: Path) -> None:
    notice = f'''GoreeCloud Gallery {VERSION_NAME}

GoreeCloud Gallery is a GoreeCloud-maintained Android gallery fork based on Fossify Gallery
1.13.1 and its Fossify Commons 6.1.5 dependency. The application remains offline-first and
does not add analytics, advertising, cloud accounts, remote APIs, or an Internet permission.

gc.2 corrects the maintained-fork identity boundary found during real-device acceptance:
legitimate com.goreecloud packages no longer trigger the Fossify counterfeit warning, every
launcher alias uses GoreeCloud iconography, the inherited Material-green fallback is removed,
and System appearance now follows Android light/dark mode using GoreeCloud Glaze colors.
Glaze UI geometry is also applied more deeply to menus and dialogs.

Upstream copyright, source history, GNU GPL licensing, and third-party notices remain
applicable. GoreeCloud rebranding does not remove those obligations.
'''
    write(gallery / "GOREECLOUD-NOTICE.md", notice)
    write(gallery / "app/src/main/assets/goreecloud_notice.txt", notice)


def validate(gallery: Path, commons: Path) -> None:
    manifest = read(gallery / "app/src/main/AndroidManifest.xml")
    props = read(gallery / "gradle.properties")
    settings = read(gallery / "settings.gradle.kts")
    app = read(gallery / "app/src/main/kotlin/org/fossify/gallery/App.kt")
    fake = read(commons / "commons/src/main/kotlin/org/fossify/commons/compose/extensions/ActivityExtensions.kt")
    dynamic = read(commons / "commons/src/main/kotlin/org/fossify/commons/compose/theme/DynamicTheme.kt")
    styling = read(commons / "commons/src/main/kotlin/org/fossify/commons/extensions/Context-styling.kt")
    shapes = read(commons / "commons/src/main/kotlin/org/fossify/commons/compose/theme/Shapes.kt")

    required = [
        (f"VERSION_NAME={VERSION_NAME}", props),
        (f"VERSION_CODE={VERSION_CODE}", props),
        ('includeBuild("../upstream-commons")', settings),
        ('@drawable/ic_goreecloud_gallery', manifest),
        ('palette_version", 0) < 2', app),
        ('!packageName.startsWith("com.goreecloud.", true)', fake),
        ('else -> Color(primaryColorInt)', dynamic),
        ('!packageName.startsWith("com.goreecloud.", true)', styling),
        ('extraLarge = RoundedCornerShape(30.dp)', shapes),
    ]
    for needle, haystack in required:
        if needle not in haystack:
            fail(f"validation missing {needle!r}")
    if '@mipmap/ic_launcher' in manifest:
        fail("an upstream launcher icon remains in the manifest")
    if "android.permission.INTERNET" in manifest:
        fail("Internet permission unexpectedly present")

    for path in [
        gallery / "app/src/main/res/values/colors.xml",
        gallery / "app/src/main/res/values-night/glaze_colors.xml",
        gallery / "app/src/main/res/drawable/ic_goreecloud_gallery.xml",
    ]:
        ET.parse(path)

    print(f"Applied GoreeCloud Gallery {VERSION_NAME} real-device acceptance corrections")


def main() -> None:
    if len(sys.argv) != 3:
        fail("usage: build_goreecloud_gallery_gc2.py <Gallery checkout> <Commons checkout>")
    gallery = Path(sys.argv[1]).resolve()
    commons = Path(sys.argv[2]).resolve()
    verify_checkout(gallery, GALLERY_COMMIT, "Gallery")
    verify_checkout(commons, COMMONS_COMMIT, "Commons")
    patch_version(gallery)
    patch_composite_build(gallery)
    patch_gallery_identity(gallery)
    patch_gallery_palette(gallery)
    patch_gallery_resources(gallery)
    patch_commons_fake_check(commons)
    patch_commons_system_glaze(commons)
    patch_commons_glaze_geometry(commons)
    patch_notice(gallery)
    validate(gallery, commons)


if __name__ == "__main__":
    main()
