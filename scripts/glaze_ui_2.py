"""GLAZE UI V1.1 public-site normalization helpers.

The public Website family has multiple independently deployable HTML templates.
This helper keeps generated Main artifacts on the current Stable GLAZE UI V1.1
contract while preserving current product facts and repository-local build rules.
"""

from __future__ import annotations

import re

GLAZE_VERSION = "1.1.0"
GLAZE_ACTIVATION_VERSION = "1.1"
GLAZE_PROMOTION_REVISION = "15cc76d2bcd4065552dc31c77145b63f34d9e7b2"
GLAZE_BUNDLE = "css/glaze-v1.1.0.css"

FILE_MANAGER_CARD = '''<article class="service-card suite-card glz11-card" data-suite-app="file-manager">
  <div class="service-art suite-art" aria-hidden="true"><span class="repo-mark">FM</span></div>
  <h3>GoreeCloud File Manager</h3>
  <p class="suite-description"><strong>Description:</strong> First-party file-management experience for local and connected GoreeCloud storage surfaces.</p>
  <p class="suite-role"><strong>Role:</strong> File-management experience across local and connected GoreeCloud storage.</p>
  <span class="badge growing">Active Development</span>
</article>'''

MAPS_CARD = '''<article class="service-card suite-card glz11-card" data-suite-app="maps">
  <div class="service-art suite-art" aria-hidden="true"><span class="repo-mark">MP</span></div>
  <h3>GoreeCloud Maps</h3>
  <p class="suite-description"><strong>Description:</strong> GoreeCloud mapping experience with privacy, location, navigation, and identity boundaries kept explicit.</p>
  <p class="suite-role"><strong>Role:</strong> First-party maps, navigation, and location presentation experience.</p>
  <span class="badge growing">Active Development</span>
</article>'''

APP_STORE_CARD = '''<article class="service-card suite-card glz11-card" data-suite-app="app-store">
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


def _activate_glaze_v11(html: str) -> str:
    """Make one HTML document source-native to the current Stable web contract."""
    html = re.sub(
        r'(<html\b)(?![^>]*\bdata-glaze-version=)([^>]*)>',
        rf'\1 data-glaze-version="{GLAZE_ACTIVATION_VERSION}"\2>',
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r'data-glaze-version="[^"]+"',
        f'data-glaze-version="{GLAZE_ACTIVATION_VERSION}"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="goreecloud-glaze-ui" content="[^"]+"',
        f'name="goreecloud-glaze-ui" content="{GLAZE_VERSION}"',
        html,
    )
    html = re.sub(
        r'href="(?:/)?css/glaze(?:-ui)?-[^"/]+\.css" data-glaze-ui="[^"]+"',
        f'href="{GLAZE_BUNDLE}" data-glaze-ui="{GLAZE_VERSION}"',
        html,
    )
    return html


def apply_glaze_ui(html: str) -> str:
    html = _activate_glaze_v11(html)

    replacements = (
        ('class="site-header"', 'class="site-header glaze-material-soft glz11-glaze"'),
        ('class="site-header glaze-material-soft"', 'class="site-header glaze-material-soft glz11-glaze"'),
        ('class="site-nav"', 'class="site-nav glaze-navigation-capsule glz11-nav"'),
        ('class="site-nav glaze-navigation-capsule"', 'class="site-nav glaze-navigation-capsule glz11-nav"'),
        ('class="button primary"', 'class="button primary glaze-button glz11-button glz11-button-primary"'),
        ('class="button primary glaze-button"', 'class="button primary glaze-button glz11-button glz11-button-primary"'),
        ('class="button secondary"', 'class="button secondary glaze-button glz11-button glz11-button-secondary"'),
        ('class="button secondary glaze-button"', 'class="button secondary glaze-button glz11-button glz11-button-secondary"'),
        ('class="hero-card"', 'class="hero-card glaze-material glz11-radius-hero"'),
        ('class="hero-card glaze-material"', 'class="hero-card glaze-material glz11-radius-hero"'),
        ('Glaze UI 1.5.0 is the current Stable', 'GLAZE UI V1.1 / 1.1.0 is the current Stable'),
        ('Glaze UI 2.0.0 is the current Stable', 'GLAZE UI V1.1 / 1.1.0 is the current Stable'),
        ('Glaze UI 2.1.0 is the current Stable', 'GLAZE UI V1.1 / 1.1.0 is the current Stable'),
        ('Glaze UI 2.2.0 is the current Stable', 'GLAZE UI V1.1 / 1.1.0 is the current Stable'),
        ('Glaze UI 1.5 is the current Stable', 'GLAZE UI V1.1 is the current Stable'),
        ('Glaze UI 2.0 is the current Stable', 'GLAZE UI V1.1 is the current Stable'),
        ('Glaze UI 2.1 is the current Stable', 'GLAZE UI V1.1 is the current Stable'),
        ('Glaze UI 2.2 is the current Stable', 'GLAZE UI V1.1 is the current Stable'),
        ('Glaze UI 1.5 Stable', 'GLAZE UI V1.1 Stable'),
        ('Glaze UI 2.0 Stable', 'GLAZE UI V1.1 Stable'),
        ('Glaze UI 2.1 Stable', 'GLAZE UI V1.1 Stable'),
        ('Glaze UI 2.2 Stable', 'GLAZE UI V1.1 Stable'),
        ('Stable 1.5', 'Stable V1.1'),
        ('Stable 2.0', 'Stable V1.1'),
        ('Stable 2.1', 'Stable V1.1'),
        ('Stable 2.2', 'Stable V1.1'),
        (
            'The public portfolio uses Glaze UI 2.1.0 Stable as its current design target; each independently deployed site must still earn exact-revision deployment acceptance.',
            'The public portfolio uses GLAZE UI V1.1 / 1.1.0 Stable as its current design target; each independently deployed site must still earn exact-revision rendered and deployment acceptance.',
        ),
        (
            'The public portfolio uses Glaze UI 2.2.0 Stable as its current design target; each independently deployed site must still earn exact-revision deployment acceptance.',
            'The public portfolio uses GLAZE UI V1.1 / 1.1.0 Stable as its current design target; each independently deployed site must still earn exact-revision rendered and deployment acceptance.',
        ),
        (
            'The GoreeCloud Design Center for Glaze UI 2.1.0 Stable: interaction, material, adaptive form factors, accessibility, motion, visual language, and design-system governance.',
            'The GoreeCloud Design Center for GLAZE UI V1.1 / 1.1.0 Stable: interaction, material, adaptive form factors, accessibility, motion, visual language, and design-system governance.',
        ),
        ('current 53-repository portfolio', 'current 57-repository portfolio'),
        ('current 56-repository portfolio', 'current 57-repository portfolio'),
        ('the five substantive platform systems', 'the six substantive platform systems'),
        (
            'Glaze UI, Privacy Shield, Wardveil Security, Everkeep, and GoreeCloud Mesh remain substantive platform systems',
            'Glaze UI, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and GoreeCloud Identity remain substantive platform systems',
        ),
    )
    for old, new in replacements:
        html = html.replace(old, new)

    # Keep current Suite directory additions synchronized with dedicated Suite.
    if 'data-suite-app="drive"' in html:
        html = _insert_suite_card_after(html, "drive", FILE_MANAGER_CARD)
        html = _insert_suite_card_after(html, "location", MAPS_CARD)
        html = _insert_suite_card_after(html, "launcher", APP_STORE_CARD)
        html = html.replace(
            'Status labels describe GoreeCloud lifecycle and acceptance state, not upstream project maturity. A source repository, milestone, beta, or release-candidate label does not imply production approval unless the card explicitly states a Stable or current-service status.',
            'Status labels describe GoreeCloud lifecycle and acceptance state, not upstream project maturity. A source repository, milestone, beta, or release-candidate label does not imply production approval unless the card explicitly states a Stable or current-service status. Products without approved canonical artwork use a neutral text mark until the branding authority publishes an approved asset.',
        )
    return html


# Compatibility name retained while downstream build/test imports migrate.
def apply_glaze_ui_2(html: str) -> str:
    return apply_glaze_ui(html)
