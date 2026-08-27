#!/usr/bin/env python3
"""Normalize the GoreeCloud homepage into the public website hub."""

from __future__ import annotations

import re

HERO_PREFIX = re.compile(
    r'<div class="hero-labels"[^>]*>.*?(?=\s*<h1>)',
    re.DOTALL,
)
HERO_ACTIONS = re.compile(
    r'<div class="hero-actions">.*?</div>',
    re.DOTALL,
)
PORTFOLIO_BLOCK = re.compile(
    r'\n    <section id="services" class="section suite-section">.*?(?=\n    <section id="how-it-works")',
    re.DOTALL,
)
ROADMAP_AI_CARD = re.compile(
    r'          <article class="roadmap-card">\s*'
    r'<div class="roadmap-card-head">\s*'
    r'(?:<span class="roadmap-icon roadmap-art"[^>]*>.*?</span>\s*)?'
    r'<span class="roadmap-state">[^<]*</span>\s*'
    r'</div>\s*'
    r'<p class="roadmap-kicker">Local Intelligence</p>\s*'
    r'<h3>(?:Local AI|GoreeCloud AI)</h3>.*?'
    r'          </article>',
    re.DOTALL,
)

WEBSITE_STYLESHEET = '<link rel="stylesheet" href="css/websites.css">'

EXPECTED_WEBSITE_DOMAINS = (
    "goreecloud.com",
    "suite.goreecloud.com",
    "projects.goreecloud.com",
    "design.goreecloud.com",
    "privacy.goreecloud.com",
    "security.goreecloud.com",
    "roadmap.goreecloud.com",
    "blog.goreecloud.com",
    "archive.goreecloud.com",
)


def canonical_hero_labels() -> str:
    return (
        '<div class="hero-labels" aria-label="GoreeCloud platform systems">\n'
        '            <a class="glaze-chip" href="https://design.goreecloud.com/">Glaze UI</a>\n'
        '            <a class="glaze-chip" href="https://privacy.goreecloud.com/">Privacy Shield</a>\n'
        '            <a class="glaze-chip" href="https://security.goreecloud.com/">Wardveil Security</a>\n'
        '            <span class="glaze-chip">Everkeep</span>\n'
        '            <span class="glaze-chip">GoreeCloud Mesh</span>\n'
        '            <span class="eyebrow">Design • Privacy • Security • Resilience • Coordination</span>\n'
        '          </div>\n\n          '
    )


def website_card(
    name: str,
    url: str,
    domain: str,
    description: str,
    status: str,
    status_class: str,
    preview_class: str,
    preview_mark: str,
) -> str:
    return (
        '<article class="service-card website-card">\n'
        f'  <a class="website-preview {preview_class}" href="{url}" aria-label="Open {name}">\n'
        '    <span class="website-preview-browser" aria-hidden="true">\n'
        '      <span class="website-preview-toolbar">\n'
        '        <i></i><i></i><i></i>\n'
        f'        <span class="website-preview-domain">{domain}</span>\n'
        '      </span>\n'
        '      <span class="website-preview-page">\n'
        f'        <span class="website-preview-mark">{preview_mark}</span>\n'
        f'        <span class="website-preview-title">{name}</span>\n'
        '        <span class="website-preview-lines"><span></span><span></span></span>\n'
        '      </span>\n'
        '    </span>\n'
        '  </a>\n'
        '  <div class="website-card-body">\n'
        f'    <p class="service-kicker">{domain}</p>\n'
        f'    <h3>{name}</h3>\n'
        f'    <p>{description}</p>\n'
        '    <div class="website-card-footer">\n'
        f'      <a class="website-link" href="{url}">Visit website →</a>\n'
        f'      <span class="badge {status_class}">{status}</span>\n'
        '    </div>\n'
        '  </div>\n'
        '</article>'
    )


def websites_section() -> str:
    cards = [
        website_card(
            "GoreeCloud",
            "https://www.goreecloud.com/",
            "goreecloud.com",
            "The main public hub for GoreeCloud: platform direction, project story, repositories, and links into the wider public web ecosystem.",
            "Primary Website",
            "active",
            "website-main",
            "GC",
        ),
        website_card(
            "GoreeCloud Suite",
            "https://suite.goreecloud.com/",
            "suite.goreecloud.com",
            "The dedicated home for GoreeCloud Suite applications, services, umbrella capabilities, lifecycle status, and cross-client product identity.",
            "Dedicated Site",
            "growing",
            "website-suite",
            "SU",
        ),
        website_card(
            "GoreeCloud Projects",
            "https://projects.goreecloud.com/",
            "projects.goreecloud.com",
            "The public software and project portfolio for representative GoreeCloud development work and project-level context.",
            "Portfolio",
            "active",
            "website-projects",
            "PR",
        ),
        website_card(
            "Glaze UI",
            "https://design.goreecloud.com/",
            "design.goreecloud.com",
            "The design-system website for GoreeCloud interface foundations, interaction contracts, adaptive behavior, and visual language.",
            "Platform System",
            "active",
            "website-design",
            "GU",
        ),
        website_card(
            "Privacy Shield",
            "https://privacy.goreecloud.com/",
            "privacy.goreecloud.com",
            "The public privacy identity and documentation surface for GoreeCloud privacy contracts, controls, and data-minimization expectations.",
            "Platform System",
            "active",
            "website-privacy",
            "PS",
        ),
        website_card(
            "Wardveil Security",
            "https://security.goreecloud.com/",
            "security.goreecloud.com",
            "The security and protection website for evidence-backed GoreeCloud security state, reporting, and protection experiences.",
            "Platform System",
            "active",
            "website-security",
            "WS",
        ),
        website_card(
            "GoreeCloud Roadmap",
            "https://roadmap.goreecloud.com/",
            "roadmap.goreecloud.com",
            "The focused public roadmap for planned GoreeCloud infrastructure, applications, services, migrations, and platform evolution.",
            "Roadmap",
            "growing",
            "website-roadmap",
            "RM",
        ),
        website_card(
            "GoreeCloud Blog",
            "https://blog.goreecloud.com/",
            "blog.goreecloud.com",
            "The public development and engineering journal for build notes, implementation lessons, architecture decisions, and project updates.",
            "Publication",
            "active",
            "website-blog",
            "BL",
        ),
        website_card(
            "GoreeCloud Archive",
            "https://archive.goreecloud.com/",
            "archive.goreecloud.com",
            "The curated historical archive for preserving selected GoreeCloud public records, milestones, and project history over time.",
            "Archive",
            "active",
            "website-archive",
            "AR",
        ),
    ]
    rendered_cards = "\n          ".join(cards)
    return (
        '\n    <section id="websites" class="section websites-section">\n'
        '      <div class="container">\n'
        '        <div class="section-heading">\n'
        '          <p class="eyebrow">GoreeCloud websites</p>\n'
        '          <h2>Explore the public GoreeCloud web ecosystem.</h2>\n'
        '          <p>Visual preview cards make each destination easier to recognize while dedicated sites carry the deeper information that does not belong on the main homepage.</p>\n'
        '        </div>\n'
        '        <div class="service-grid website-grid">\n'
        f'          {rendered_cards}\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
    )


def goreecloud_ai_roadmap_card() -> str:
    return (
        '          <article class="roadmap-card" data-roadmap="goreecloud-ai">\n'
        '            <div class="roadmap-card-head">\n'
        '              <span class="roadmap-icon roadmap-art" aria-hidden="true"><img src="assets/suite/ai.svg" alt="" width="52" height="52"></span>\n'
        '              <span class="roadmap-state">Active Development</span>\n'
        '            </div>\n'
        '            <p class="roadmap-kicker">Local Intelligence</p>\n'
        '            <h3>GoreeCloud AI</h3>\n'
        '            <p>First-party private AI experience built around GoreeCloud AI with Ollama as the local model runtime, plus Workspaces, knowledge and RAG, files, tools, orchestration, and controlled current-information research through GoreeCloud Search.</p>\n'
        '            <p class="roadmap-current"><strong>Target:</strong> A dedicated AI Services VM running Ollama and GoreeCloud AI as the first-party conversation, knowledge, and orchestration layer.</p>\n'
        '            <ul class="roadmap-details">\n'
        '              <li>Ollama local model runtime</li>\n'
        '              <li>GoreeCloud AI Workspaces, knowledge, RAG, files, tools, and orchestration</li>\n'
        '              <li>Controlled web research through GoreeCloud Search</li>\n'
        '            </ul>\n'
        '          </article>'
    )


def normalize_homepage(source: str) -> str:
    normalized, hero_count = HERO_PREFIX.subn(canonical_hero_labels(), source, count=1)
    if hero_count != 1:
        raise ValueError("homepage platform-system labels could not be normalized")

    normalized, portfolio_count = PORTFOLIO_BLOCK.subn(websites_section(), normalized, count=1)
    if portfolio_count != 1:
        raise ValueError("homepage Suite/capability block could not be replaced with website hub")

    normalized = normalized.replace(
        '<a href="#services">Suite</a>\n        <a href="#capabilities">Capabilities</a>',
        '<a href="#websites">Websites</a>\n        <a href="https://suite.goreecloud.com/">Suite</a>',
    )

    normalized, action_count = HERO_ACTIONS.subn(
        '<div class="hero-actions">\n'
        '            <a class="button primary" href="#websites">Explore GoreeCloud Websites</a>\n'
        '            <a class="button secondary" href="https://suite.goreecloud.com/">Explore GoreeCloud Suite</a>\n'
        '          </div>',
        normalized,
        count=1,
    )
    if action_count != 1:
        raise ValueError("homepage hero actions could not be normalized")

    normalized, ai_count = ROADMAP_AI_CARD.subn(goreecloud_ai_roadmap_card(), normalized, count=1)
    if ai_count != 1:
        raise ValueError("homepage GoreeCloud AI roadmap card could not be normalized")

    if WEBSITE_STYLESHEET not in normalized:
        normalized = normalized.replace("</head>", f"  {WEBSITE_STYLESHEET}\n</head>", 1)

    hero = HERO_PREFIX.search(normalized)
    hero_text = hero.group(0) if hero else ""
    for label in ("Glaze UI", "Privacy Shield", "Wardveil Security", "Everkeep", "GoreeCloud Mesh"):
        if len(re.findall(rf">{re.escape(label)}<", hero_text)) != 1:
            raise ValueError(f"homepage platform-system identity must appear exactly once: {label}")
    if "GoreeCloud Identity" in hero_text:
        raise ValueError("GoreeCloud Identity is an application identity, not a platform-system hero chip")
    if hero_text.count('class="glaze-chip"') != 5:
        raise ValueError("homepage hero must contain exactly five platform-system chips")

    if 'data-suite-app=' in normalized or 'data-capability=' in normalized:
        raise ValueError("Suite application/capability cards must live on suite.goreecloud.com, not the main homepage")
    if normalized.count('id="websites"') != 1:
        raise ValueError("homepage must contain exactly one GoreeCloud websites section")
    for domain in EXPECTED_WEBSITE_DOMAINS:
        if normalized.count(domain) < 1:
            raise ValueError(f"homepage website portfolio is missing: {domain}")
    website_section_match = re.search(r'<section id="websites".*?</section>', normalized, re.DOTALL)
    website_section = website_section_match.group(0) if website_section_match else ""
    if website_section.count('class="service-card website-card"') != len(EXPECTED_WEBSITE_DOMAINS):
        raise ValueError("homepage website portfolio must contain exactly nine website cards")
    if website_section.count('class="website-preview ') != len(EXPECTED_WEBSITE_DOMAINS):
        raise ValueError("each website card must include a visual preview")
    if normalized.count(WEBSITE_STYLESHEET) != 1:
        raise ValueError("homepage must include the website preview stylesheet exactly once")
    if "Open WebUI" in normalized or "AnythingLLM" in normalized:
        raise ValueError("retired AI front ends remain in the public homepage")
    return normalized
