"""Glaze UI 2.0 public-site normalization helpers.

The main GoreeCloud site has several deployable HTML templates. This helper keeps
all of them on the same Stable Glaze UI contract without requiring duplicated
version wiring in generated and hand-authored pages. It also corrects legacy
content that remains in source templates before the isolated public artifact is
validated and deployed.
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
        ('Glaze UI 1.5 Stable', 'Glaze UI 2.0 Stable'),
        ('Stable 1.5', 'Stable 2.0'),
        ('current 53-repository portfolio', 'current 56-repository portfolio'),
        ('the five substantive platform systems', 'the six substantive platform systems'),
        (
            'Glaze UI, Privacy Shield, Wardveil Security, Everkeep, and GoreeCloud Mesh remain substantive platform systems',
            'Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity remain substantive platform systems',
        ),
    )
    for old, new in replacements:
        html = html.replace(old, new)
    return html
