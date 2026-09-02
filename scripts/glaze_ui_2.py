"""Glaze UI 2.2 public-site normalization helpers.

The GoreeCloud website repository contains several independently deployed HTML
surfaces. This helper keeps generated artifacts on the exact current Stable Glaze
UI contract while source templates are migrated source-native. It is a compatibility
boundary, not permission to leave superseded active markup in source.
"""

from __future__ import annotations

GLAZE_VERSION = "2.2.0"
GLAZE_PROMOTION_REVISION = "6731098b28dd0393faa878c70d989a221d714a20"
GLAZE_BUNDLE = "css/glaze-ui-2.2.0.css"

FILE_MANAGER_CARD = '''<article class="service-card suite-card" data-suite-app="file-manager">
  <div class="service-art suite-art" aria-hidden="true"><span class="repo-mark">FM</span></div>
  <h3>GoreeCloud File Manager</h3>
  <p class="suite-description"><strong>Description:</strong> First-party file-management experience for local and connected GoreeCloud storage surfaces.</p>
  <p class="suite-role"><strong>Role:</strong> File-management experience across local and connected GoreeCloud storage.</p>
  <span class="badge growing">Active Development</span>
</article>'''

MAPS_CARD = '''<article class="service-card suite-card" data-suite-app="maps">
  <div class="service-art suite-art" aria-hidden="true"><span class="repo-mark">MP</span></div>
  <h3>GoreeCloud Maps</h3>
  <p class="suite-description"><strong>Description:</strong> GoreeCloud mapping experience with privacy, location, navigation, and identity boundaries kept explicit.</p>
  <p class="suite-role"><strong>Role:</strong> First-party maps, navigation, and location presentation experience.</p>
  <span class="badge growing">Active Development</span>
</article>'''

APP_STORE_CARD = '''<article class="service-card suite-card" data-suite-app="app-store">
  <div class="service-art suite-art" aria-hidden="true"><span class="repo-mark">AS</span></div>
  <h3>GoreeCloud App Store</h3>
  <p class="suite-description"><strong>Description:</strong> Official multi-user catalog for discovering GoreeCloud applications and services according to account access and entitlement.</p>
  <p class="suite-role"><strong>Role:</strong> GoreeCloud application and service discovery catalog with account and entitlement boundaries.</p>
  <span class="badge growing">Active Development</span>
</article>'''


def _insert_suite_card_after(html: str, anchor_id: str, card: str) -> str:
    """Insert a current Suite card after a rendered manifest card, idempotently."""
    card_id = card.split('data-suite-app="', 1)[1].split('"', 1)[0]
    if f'data-suite-app="{card_id}"' in html:
        return html
    marker = f'data-suite-app="{anchor_id}"'
    start = html.find(marker)
    if start < 0:
        raise ValueError(f"Suite card anchor missing: {anchor_id}")
    end = html.find("</article>", start)
    if end < 0:
        raise ValueError(f"Suite card boundary missing: {anchor_id}")
    end += len("</article>")
    return html[:end] + "\n            " + card + html[end:]


def apply_glaze_ui_2(html: str) -> str:
    """Normalize historical source fragments to the 2.2.0 artifact contract.

    Source validation separately requires deployable templates to be 2.2-native;
    these replacements exist for generated fragments and controlled rollback
    compatibility, not as the sole migration mechanism.
    """
    replacements = (
        ('name="goreecloud-glaze-ui" content="1.5.0"', 'name="goreecloud-glaze-ui" content="2.2.0"'),
        ('name="goreecloud-glaze-ui" content="2.0.0"', 'name="goreecloud-glaze-ui" content="2.2.0"'),
        ('name="goreecloud-glaze-ui" content="2.1.0"', 'name="goreecloud-glaze-ui" content="2.2.0"'),
        ('href="/css/glaze-ui-1.5.0.css" data-glaze-ui="1.5.0"', 'href="/css/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('href="/css/glaze-ui-2.0.0.css" data-glaze-ui="2.0.0"', 'href="/css/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('href="/css/glaze-ui-2.1.0.css" data-glaze-ui="2.1.0"', 'href="/css/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('href="css/glaze-ui-1.5.0.css" data-glaze-ui="1.5.0"', 'href="css/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('href="css/glaze-ui-2.0.0.css" data-glaze-ui="2.0.0"', 'href="css/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('href="css/glaze-ui-2.1.0.css" data-glaze-ui="2.1.0"', 'href="css/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('href="/assets/glaze-ui-2.1.0.css" data-glaze-ui="2.1.0"', 'href="/assets/glaze-ui-2.2.0.css" data-glaze-ui="2.2.0"'),
        ('class="site-header"', 'class="site-header glaze-material-soft"'),
        ('class="site-nav"', 'class="site-nav glaze-navigation-capsule"'),
        ('class="button primary"', 'class="button primary glaze-button"'),
        ('class="button secondary"', 'class="button secondary glaze-button"'),
        ('class="hero-card"', 'class="hero-card glaze-surface-raised"'),
        ('Glaze UI 1.5.0 is the current Stable', 'Glaze UI 2.2.0 is the current Stable'),
        ('Glaze UI 2.0.0 is the current Stable', 'Glaze UI 2.2.0 is the current Stable'),
        ('Glaze UI 2.1.0 is the current Stable', 'Glaze UI 2.2.0 is the current Stable'),
        ('Glaze UI 1.5 is the current Stable', 'Glaze UI 2.2 is the current Stable'),
        ('Glaze UI 2.0 is the current Stable', 'Glaze UI 2.2 is the current Stable'),
        ('Glaze UI 2.1 is the current Stable', 'Glaze UI 2.2 is the current Stable'),
        ('Glaze UI 1.5 Stable', 'Glaze UI 2.2 Stable'),
        ('Glaze UI 2.0 Stable', 'Glaze UI 2.2 Stable'),
        ('Glaze UI 2.1 Stable', 'Glaze UI 2.2 Stable'),
        ('Stable 1.5', 'Stable 2.2'),
        ('Stable 2.0', 'Stable 2.2'),
        ('Stable 2.1', 'Stable 2.2'),
        (
            'The public portfolio uses Glaze UI 2.1.0 Stable as its current design target; each independently deployed site must still earn exact-revision deployment acceptance.',
            'The public portfolio uses Glaze UI 2.2.0 Stable as its current design target; each independently deployed site must still earn exact-revision deployment acceptance.',
        ),
        (
            'The GoreeCloud Design Center for Glaze UI 2.1.0 Stable: interaction, material, adaptive form factors, accessibility, motion, visual language, and design-system governance.',
            'The GoreeCloud Design Center for Glaze UI 2.2.0 Stable: interaction, material, adaptive form factors, accessibility, motion, visual language, and design-system governance.',
        ),
        ('current 53-repository portfolio', 'current 57-repository portfolio'),
        ('current 56-repository portfolio', 'current 57-repository portfolio'),
        ('the five substantive platform systems', 'the seven Integral Platform Systems'),
        ('the six substantive platform systems', 'the seven Integral Platform Systems'),
        (
            'Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity remain substantive platform systems',
            'GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, GoreeCloud Mesh, and GoreeCloud Identity are the seven Integral Platform Systems',
        ),
    )
    for old, new in replacements:
        html = html.replace(old, new)

    if 'data-suite-app="drive"' in html:
        html = _insert_suite_card_after(html, "drive", FILE_MANAGER_CARD)
        html = _insert_suite_card_after(html, "location", MAPS_CARD)
        html = _insert_suite_card_after(html, "launcher", APP_STORE_CARD)
        html = html.replace(
            'Status labels describe GoreeCloud lifecycle and acceptance state, not upstream project maturity. A source repository, milestone, beta, or release-candidate label does not imply production approval unless the card explicitly states a Stable or current-service status.',
            'Status labels describe GoreeCloud lifecycle and acceptance state, not upstream project maturity. A source repository, milestone, beta, or release-candidate label does not imply production approval unless the card explicitly states a Stable or current-service status. Products without approved canonical artwork use a neutral text mark until the branding authority publishes an approved asset.',
        )
    return html
