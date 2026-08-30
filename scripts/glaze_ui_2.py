"""Glaze UI 2.0 public-site normalization helpers.

The main GoreeCloud site has several deployable HTML templates. This helper keeps
all of them on the same Stable Glaze UI contract without requiring duplicated
version wiring in generated and hand-authored pages.
"""

from __future__ import annotations

GLAZE_VERSION = "2.0.0"
GLAZE_PROMOTION_REVISION = "ff3fff4306bd53ea9c0715a7c0d64265bb038617"
GLAZE_BUNDLE = "css/glaze-ui-2.0.0.css"


def apply_glaze_ui_2(html: str) -> str:
    replacements = (
        ('name="goreecloud-glaze-ui" content="1.5.0"', 'name="goreecloud-glaze-ui" content="2.0.0"'),
        ('href="/css/glaze-ui-1.5.0.css" data-glaze-ui="1.5.0"', 'href="/css/glaze-ui-2.0.0.css" data-glaze-ui="2.0.0"'),
        ('href="css/glaze-ui-1.5.0.css" data-glaze-ui="1.5.0"', 'href="css/glaze-ui-2.0.0.css" data-glaze-ui="2.0.0"'),
        ('class="site-header"', 'class="site-header glaze-material-soft"'),
        ('class="site-nav"', 'class="site-nav glaze-navigation-capsule"'),
        ('class="button primary"', 'class="button primary glaze-button"'),
        ('class="button secondary"', 'class="button secondary glaze-button"'),
        ('class="hero-card"', 'class="hero-card glaze-material"'),
        ('class="repo-summary"', 'class="repo-summary glaze-material"'),
        ('Glaze UI 1.5.0 is the current Stable', 'Glaze UI 2.0.0 is the current Stable'),
        ('Glaze UI 1.5 is the current Stable', 'Glaze UI 2.0 is the current Stable'),
        ('Stable 1.5', 'Stable 2.0'),
    )
    for old, new in replacements:
        html = html.replace(old, new)
    return html
