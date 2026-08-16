#!/usr/bin/env python3
"""Validate the GoreeCloud public site's Glaze UI 1.0 design contract.

This is a structural regression gate for the shared GoreeCloud design system. It
checks that every human-facing page participates in the same theme, branding,
responsive, accessibility, privacy, and progressive-enhancement foundation while
also proving the repository records an explicit Glaze UI version/conformance state.
It does not replace visual review in real browsers or assistive technologies.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HUMAN_PAGES = (
    ROOT / "index.html",
    ROOT / "privacy.html",
    ROOT / "security.html",
    ROOT / "404.html",
)
GLAZE = ROOT / "css" / "glaze.css"
POLISH = ROOT / "css" / "glaze-polish.css"
THEME_INIT = ROOT / "js" / "theme-init.js"
MAIN_JS = ROOT / "js" / "main.js"
CONFORMANCE = ROOT / "docs" / "glaze-ui-conformance.md"
TARGET_GLAZE_UI_VERSION = "1.0.0"
GLAZE_COMPONENT_CLASSES = {
    "button",
    "glaze-chip",
    "glaze-callout",
    "hero-card",
    "service-card",
    "platform-card",
    "roadmap-card",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.theme_colors: set[str] = set()
        self.has_color_scheme_meta = False
        self.has_viewport = False
        self.has_brand = False
        self.has_brand_icon = False
        self.has_skip_link = False
        self.has_main = False
        self.main_tabindex: str | None = None
        self.has_glaze_component = False

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        classes = set(attrs.get("class", "").split())

        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        if tag == "meta" and attrs.get("name") == "color-scheme":
            self.has_color_scheme_meta = True
        if tag == "meta" and attrs.get("name") == "theme-color":
            scheme = attrs.get("data-theme-color")
            if scheme:
                self.theme_colors.add(scheme)
        if tag == "link" and "stylesheet" in attrs.get("rel", "").split():
            href = attrs.get("href")
            if href:
                self.stylesheets.append(href.lstrip("/"))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"].lstrip("/"))
        if tag == "a" and "brand" in classes:
            self.has_brand = True
        if tag == "img" and "brand-logo" in classes and attrs.get("src", "").endswith("assets/goreecloud-icon.png"):
            self.has_brand_icon = True
        if tag == "a" and "skip-link" in classes and attrs.get("href") == "#main":
            self.has_skip_link = True
        if tag == "main" and attrs.get("id") == "main":
            self.has_main = True
            self.main_tabindex = attrs.get("tabindex")
        if classes.intersection(GLAZE_COMPONENT_CLASSES):
            self.has_glaze_component = True


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_pages(errors: list[str]) -> None:
    for page in HUMAN_PAGES:
        if not page.exists():
            fail(errors, f"Human-facing Glaze UI page is missing: {page.name}")
            continue

        text = page.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(text)

        if not parser.has_viewport:
            fail(errors, f"{page.name} must retain responsive viewport metadata.")
        if not parser.has_color_scheme_meta:
            fail(errors, f"{page.name} must declare dark/light color-scheme support.")
        if parser.theme_colors != {"dark", "light"}:
            fail(errors, f"{page.name} must publish both dark and light theme-color metadata.")
        if "css/glaze.css" not in parser.stylesheets:
            fail(errors, f"{page.name} must load the Glaze UI foundation stylesheet.")
        if "css/glaze-polish.css" not in parser.stylesheets:
            fail(errors, f"{page.name} must load the Glaze UI polish/accessibility stylesheet.")
        if parser.stylesheets.index("css/glaze.css") > parser.stylesheets.index("css/glaze-polish.css"):
            fail(errors, f"{page.name} must load glaze.css before glaze-polish.css.")
        if "js/theme-init.js" not in parser.scripts:
            fail(errors, f"{page.name} must load the early local Glaze UI appearance initializer.")
        if not parser.has_brand or not parser.has_brand_icon:
            fail(errors, f"{page.name} must retain GoreeCloud brand identity and controlled icon artwork.")
        if not parser.has_skip_link:
            fail(errors, f"{page.name} must retain the keyboard skip link to #main.")
        if not parser.has_main or parser.main_tabindex != "-1":
            fail(errors, f"{page.name} main landmark must remain programmatically focusable with tabindex=-1.")
        if not parser.has_glaze_component:
            fail(errors, f"{page.name} must retain at least one Glaze UI surface or control marker.")

        theme_pos = text.find("js/theme-init.js")
        first_style_pos = text.find('rel="stylesheet"')
        if theme_pos < 0 or first_style_pos < 0 or theme_pos > first_style_pos:
            fail(errors, f"{page.name} must initialize stored/system appearance before stylesheets load.")


def require_markers(path: Path, markers: tuple[str, ...], errors: list[str]) -> str:
    if not path.exists():
        fail(errors, f"Required Glaze UI source is missing: {path.relative_to(ROOT)}")
        return ""
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            fail(errors, f"{path.relative_to(ROOT)} is missing required Glaze UI contract marker: {marker}")
    return text


def validate_semantic_tokens(errors: list[str]) -> None:
    glaze = require_markers(
        GLAZE,
        (
            "--glaze-canvas:",
            "--glaze-canvas-accent:",
            "--glaze-surface:",
            "--glaze-surface-strong:",
            "--glaze-surface-muted:",
            "--glaze-text:",
            "--glaze-muted:",
            "--glaze-line:",
            "--glaze-accent:",
            "--glaze-accent-2:",
            "--glaze-success:",
            "--glaze-warning:",
            "--glaze-danger:",
            "--glaze-radius-control:",
            "--glaze-target-min: 44px",
            "--glaze-target-comfortable: 48px",
            "--glaze-blur:",
            "--glaze-shadow-raised:",
            "--glaze-motion-instant: 90ms",
            "--glaze-motion-fast: 160ms",
            "--glaze-motion-standard: 220ms",
            "--glaze-motion-emphasized: 320ms",
            "--glaze-ease-standard:",
            "--glaze-ease-emphasized:",
            "--glaze-focus-width:",
            "--glaze-content-max:",
            "--glaze-reading-max:",
        ),
        errors,
    )

    if glaze and glaze.count("--glaze-motion-") < 4:
        fail(errors, "css/glaze.css must retain all four Glaze UI motion-duration roles.")


def validate_surface_and_adaptive_contract(errors: list[str]) -> None:
    require_markers(
        GLAZE,
        (
            ".glaze-surface-solid",
            ".glaze-surface-raised",
            ".glaze-surface {",
            ".glaze-overlay",
            "@media (max-width: 599px)",
            "@media (min-width: 600px) and (max-width: 1023px)",
            "@media (min-width: 1024px) and (max-width: 1439px)",
            "@media (min-width: 1440px)",
            ".glaze-adaptive-hide-compact",
            ".glaze-adaptive-hide-medium",
            ".glaze-adaptive-hide-expanded",
            ".glaze-adaptive-hide-wide",
        ),
        errors,
    )


def validate_accessibility_resilience(errors: list[str]) -> None:
    require_markers(
        GLAZE,
        (
            ':root[data-theme="light"]',
            "@media (prefers-color-scheme: light)",
            ":where(a, button):focus-visible",
            "@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))",
            "@media (prefers-reduced-transparency: reduce)",
            "@media (prefers-reduced-motion: reduce)",
            "animation-duration: .01ms !important",
            "transition-duration: .01ms !important",
        ),
        errors,
    )
    require_markers(
        POLISH,
        (
            "var(--glaze-motion-fast)",
            "var(--glaze-ease-standard)",
            "@media (prefers-contrast: more)",
            "@media (forced-colors: active)",
            "@media print",
            'html:not([data-js="true"]) .site-nav',
            ":where(a, button):focus-visible",
        ),
        errors,
    )


def validate_conformance_record(errors: list[str]) -> None:
    text = require_markers(
        CONFORMANCE,
        (
            f"Target Glaze UI version: **{TARGET_GLAZE_UI_VERSION}**",
            "Canonical design-system repository: `GoreeCloud/glaze-ui`",
            "Canvas, Solid, Raised, Glaze, and Overlay",
            "Compact: through 599 CSS pixels",
            "Medium: 600 through 1023 CSS pixels",
            "Expanded: 1024 through 1439 CSS pixels",
            "Wide: 1440 CSS pixels and above",
            "Instant: 90 ms",
            "Fast: 160 ms",
            "Standard: 220 ms",
            "Emphasized: 320 ms",
            "Visual acceptance: **Preserved**",
            "No production Glaze UI exception is recorded",
        ),
        errors,
    )
    if text and "must remain outside the isolated Cloudflare `dist/` artifact" not in text:
        fail(errors, "Glaze UI conformance metadata must explicitly remain outside the public artifact.")


def validate_interaction(errors: list[str]) -> None:
    require_markers(
        THEME_INIT,
        (
            "goreecloud-theme",
            "localStorage.getItem",
            "localStorage.removeItem",
            "root.dataset.theme",
        ),
        errors,
    )
    require_markers(
        MAIN_JS,
        (
            "THEME_MODES = ['system', 'light', 'dark']",
            "prefers-color-scheme: light",
            "themeToggle.hidden = false",
            "localStorage.setItem",
            "localStorage.removeItem",
            "root.dataset.js = 'true'",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_pages(errors)
    validate_semantic_tokens(errors)
    validate_surface_and_adaptive_contract(errors)
    validate_accessibility_resilience(errors)
    validate_conformance_record(errors)
    validate_interaction(errors)

    if errors:
        print("Glaze UI validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Glaze UI {TARGET_GLAZE_UI_VERSION} validation passed across "
        f"{len(HUMAN_PAGES)} human-facing pages with recorded conformance."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
