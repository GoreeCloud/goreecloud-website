"""Install the Glaze UI 2.2 normalization at the public HTML render boundary.

This module is imported by the isolated site builder before any caller captures
``render_repository_portfolio.render_public_file``. That keeps build artifact
validation and remote deployment verification on the same exact 2.2.0 Stable
representation. Source templates are validated separately and must not rely on
this render patch as their only migration mechanism.
"""

from __future__ import annotations

import render_repository_portfolio as portfolio

from glaze_ui_2 import apply_glaze_ui_2

_PATCH_FLAG = "_goreecloud_glaze_ui_2_render_patch"

if not getattr(portfolio, _PATCH_FLAG, False):
    _base_render_public_file = portfolio.render_public_file

    def render_public_file(relative: str, source: str, manifest: dict) -> str:
        return apply_glaze_ui_2(_base_render_public_file(relative, source, manifest))

    portfolio.render_public_file = render_public_file
    setattr(portfolio, _PATCH_FLAG, True)
