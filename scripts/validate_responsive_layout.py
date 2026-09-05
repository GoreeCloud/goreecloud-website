#!/usr/bin/env python3
"""Fail closed if the public-site responsive composition regresses.

This is intentionally a source contract, not a claim of rendered visual acceptance.
Real-browser preview checks remain separate where configured. The purpose of this
gate is to preserve explicit mobile/tablet composition and interaction floors while
allowing the rebuilt Main and Repository pages to share one V1.1 consumer layer.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(source: str, marker: str, label: str, errors: list[str]) -> None:
    if marker not in source:
        errors.append(f"Missing responsive contract: {label}")


def validate() -> list[str]:
    errors: list[str] = []

    # Rebuilt Main, Repositories, Privacy, Security, and 404 share one responsive
    # source contract rather than the retired homepage-v6/websites/repositories CSS.
    site = text("css/site-v1.1.css")
    for marker, label in (
        ("body { margin: 0; min-width: 320px;", "Rebuilt root pages retain a defined narrow layout floor"),
        ("min-width: 48px; min-height: 48px;", "Header controls preserve the 48px interaction floor"),
        ("@media (max-width: 980px)", "Shared tablet breakpoint exists"),
        ("@media (max-width: 700px)", "Shared phone breakpoint exists"),
        ("@media (max-width: 440px)", "Shared narrow-phone breakpoint exists"),
        (".primary-nav.is-open { display: flex; }", "Mobile navigation is explicit open-state interaction"),
        (".nav-toggle { display: inline-flex;", "Navigation control appears at compact widths"),
        (".hero-grid, .split-section, .architecture-grid { grid-template-columns: 1fr; }", "Complex root layouts collapse to one column on tablets"),
        (".principle-grid, .destination-grid, .repo-grid { grid-template-columns: 1fr; }", "Dense cards collapse to one column on phones"),
        (".system-list > div { flex-direction: column;", "Platform-system rows recompose for phone width"),
        (".footer-grid { grid-template-columns: 1fr; }", "Footer becomes one column on phones"),
        (".actions { flex-direction: column; }", "Narrow-phone action groups stack"),
        (".button { width: 100%; }", "Narrow-phone actions use the available width"),
        ("@media (prefers-reduced-motion: reduce)", "Reduced-motion source fallback exists"),
        ("@media (prefers-reduced-transparency: reduce)", "Reduced-transparency source fallback exists"),
        ("@media (forced-colors: active)", "Forced-colors source fallback exists"),
    ):
        require(site, marker, label, errors)

    projects = text("sites/projects/assets/mobile-refresh.css")
    for marker, label in (
        ("body.glaze-canvas .topbar{position:relative", "Projects header stays in document flow"),
        ("@media(max-width:820px)", "Projects tablet breakpoint exists"),
        ("@media(max-width:580px)", "Projects phone breakpoint exists"),
        (".foundation-strip,.grid{grid-template-columns:1fr}", "Projects foundation and directory grids collapse on phones"),
        ("@media(max-width:390px){.topbar nav{grid-template-columns:1fr}", "Projects navigation becomes one column on narrow phones"),
    ):
        require(projects, marker, label, errors)

    blog = text("sites/blog/style.css")
    for marker, label in (
        ("body.glaze-canvas .top{position:relative", "Blog header stays in document flow"),
        ("@media(max-width:1060px){.card{grid-column:span 6}", "Blog uses an intermediate two-column layout"),
        ("@media(max-width:760px)", "Blog phone breakpoint exists"),
        (".card,.featured{grid-column:1/-1", "Blog cards become single-column on phones"),
        ("@media(max-width:420px){.top nav{grid-template-columns:1fr}", "Blog navigation becomes one column on narrow phones"),
    ):
        require(blog, marker, label, errors)

    roadmap = text("sites/roadmap/site.css")
    for marker, label in (
        ("body.glaze-canvas .site-header{position:relative", "Roadmap header stays in document flow"),
        ("@media(max-width:700px)", "Roadmap phone breakpoint exists"),
        (".cards{grid-template-columns:1fr}", "Roadmap cards become single-column on phones"),
        ("@media(max-width:420px){.nav nav{grid-template-columns:1fr}", "Roadmap navigation becomes one column on narrow phones"),
    ):
        require(roadmap, marker, label, errors)

    archive = text("sites/archive/style.css")
    for marker, label in (
        ("body.glaze-canvas .top{position:relative", "Archive header stays in document flow"),
        ("@media(max-width:760px)", "Archive phone breakpoint exists"),
        ("@media(max-width:430px){.top nav{grid-template-columns:1fr}", "Archive navigation becomes one column on narrow phones"),
        (".timeline{margin-left:0;padding-left:0;border-left:0}", "Archive timeline simplifies on narrow phones"),
    ):
        require(archive, marker, label, errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Responsive layout validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Responsive layout source contract passed for rebuilt root pages plus Projects, Blog, Roadmap, and Archive.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
