#!/usr/bin/env python3
"""Enforce conservative performance budgets for the static public website."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

from build_public_site import PUBLIC_DIRECTORIES, PUBLIC_FILES, ROOT

KIB = 1024
HTML_FILE_BUDGET = 64 * KIB
HTML_TOTAL_BUDGET = 96 * KIB
CSS_FILE_BUDGET = 24 * KIB
CSS_TOTAL_BUDGET = 64 * KIB
JS_FILE_BUDGET = 16 * KIB
JS_TOTAL_BUDGET = 24 * KIB
SVG_FILE_BUDGET = 24 * KIB
SVG_TOTAL_BUDGET = 128 * KIB
RASTER_FILE_BUDGET = 256 * KIB
RASTER_TOTAL_BUDGET = 256 * KIB
PUBLIC_ARTIFACT_BUDGET = 512 * KIB
MAX_HOMEPAGE_STYLESHEETS = 10
MAX_HOMEPAGE_SCRIPTS = 3

PUBLIC_HTML = (
    ROOT / "index.html",
    ROOT / "privacy.html",
    ROOT / "security.html",
    ROOT / "404.html",
)


class PerformanceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images_without_dimensions: list[str] = []
        self.stylesheet_count = 0
        self.script_count = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {name: value or "" for name, value in attrs_list}
        if tag == "img":
            if not attrs.get("width") or not attrs.get("height"):
                self.images_without_dimensions.append(attrs.get("src", "(missing src)"))
        elif tag == "link" and "stylesheet" in attrs.get("rel", "").split():
            self.stylesheet_count += 1
        elif tag == "script" and attrs.get("src"):
            self.script_count += 1


def public_files() -> list[Path]:
    paths = [ROOT / relative for relative in PUBLIC_FILES]
    for relative in PUBLIC_DIRECTORIES:
        paths.extend(path for path in (ROOT / relative).rglob("*") if path.is_file())
    return paths


def enforce_individual(errors: list[str], files: list[Path], budget: int, label: str) -> None:
    for path in files:
        size = path.stat().st_size
        if size > budget:
            errors.append(
                f"{label} exceeds {budget // KIB} KiB budget: {path.relative_to(ROOT)} is {size / KIB:.1f} KiB."
            )


def enforce_total(errors: list[str], files: list[Path], budget: int, label: str) -> None:
    size = sum(path.stat().st_size for path in files)
    if size > budget:
        errors.append(f"{label} exceeds {budget // KIB} KiB total budget: {size / KIB:.1f} KiB.")


def main() -> int:
    errors: list[str] = []
    deployable = public_files()

    html_files = [path for path in deployable if path.suffix.lower() == ".html"]
    css_files = [path for path in deployable if path.suffix.lower() == ".css"]
    js_files = [path for path in deployable if path.suffix.lower() == ".js"]
    svg_files = [path for path in deployable if path.suffix.lower() == ".svg"]
    raster_files = [path for path in deployable if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}]

    enforce_individual(errors, html_files, HTML_FILE_BUDGET, "HTML file")
    enforce_total(errors, html_files, HTML_TOTAL_BUDGET, "HTML")
    enforce_individual(errors, css_files, CSS_FILE_BUDGET, "CSS file")
    enforce_total(errors, css_files, CSS_TOTAL_BUDGET, "CSS")
    enforce_individual(errors, js_files, JS_FILE_BUDGET, "JavaScript file")
    enforce_total(errors, js_files, JS_TOTAL_BUDGET, "JavaScript")
    enforce_individual(errors, svg_files, SVG_FILE_BUDGET, "SVG file")
    enforce_total(errors, svg_files, SVG_TOTAL_BUDGET, "SVG")
    enforce_individual(errors, raster_files, RASTER_FILE_BUDGET, "Raster image")
    enforce_total(errors, raster_files, RASTER_TOTAL_BUDGET, "Raster images")

    total_size = sum(path.stat().st_size for path in deployable)
    if total_size > PUBLIC_ARTIFACT_BUDGET:
        errors.append(
            f"Public static artifact exceeds {PUBLIC_ARTIFACT_BUDGET // KIB} KiB source budget: "
            f"{total_size / KIB:.1f} KiB."
        )

    for path in PUBLIC_HTML:
        parser = PerformanceHTMLParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for src in parser.images_without_dimensions:
            errors.append(
                f"Image must declare width and height to reserve layout space in {path.relative_to(ROOT)}: {src}"
            )

        if path.name == "index.html":
            if parser.stylesheet_count > MAX_HOMEPAGE_STYLESHEETS:
                errors.append(
                    f"Homepage stylesheet request count exceeds {MAX_HOMEPAGE_STYLESHEETS}: "
                    f"found {parser.stylesheet_count}."
                )
            if parser.script_count > MAX_HOMEPAGE_SCRIPTS:
                errors.append(
                    f"Homepage script request count exceeds {MAX_HOMEPAGE_SCRIPTS}: found {parser.script_count}."
                )

    if errors:
        print("Performance budget validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Performance budget validation passed: public source artifact is {total_size / KIB:.1f} KiB.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
