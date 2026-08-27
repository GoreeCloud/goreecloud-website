#!/usr/bin/env python3
"""Normalize the GoreeCloud homepage into the public website hub."""

from __future__ import annotations

import re

HERO_PREFIX = re.compile(
    r'<div class="hero-labels[^"]*"[^>]*>.*?(?=\s*<h1>)',
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
BAND_BLOCK = re.compile(
    r'\n    <section class="band" aria-label="Core principles">.*?</section>\n',
    re.DOTALL,
)
STORY_BLOCK = re.compile(
    r'\n    <section id="story" class="section">.*?(?=\n    <section id="follow")',
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
HOMEPAGE_STYLESHEET = '<link rel="stylesheet" href="css/homepage-v6.css">'

EXPECTED_WEBSITE_DOMAINS = (
    "goreecloud.com",
    "suite.goreecloud.com",
    "projects.goreecloud.com",
    "design.goreecloud.com",
    "privacy.goreecloud.com",
    "security.goreecloud.com",
    "everkeep.goreecloud.com",
    "roadmap.goreecloud.com",
    "blog.goreecloud.com",
    "archive.goreecloud.com",
)

PLATFORM_SYSTEM_LABELS = (
    "Glaze UI",
    "Privacy Shield",
    "Wardveil Security",
    "Everkeep",
    "GoreeCloud Mesh",
)


def canonical_hero_labels() -> str:
    """Keep the hero focused; platform-system detail belongs in dedicated sections/sites."""
    return (
        '<div class="hero-labels hero-context" aria-label="GoreeCloud platform focus">\n'
        '            <span class="eyebrow">Private • Self-hosted • Recoverable</span>\n'
        '          </div>\n\n          '
    )


def website_card(
    name: str,
    url: str,
    domain: str,
    description: str,
    status: str,
    status_class: str,
    card_class: str,
    mark: str,
) -> str:
    """Render one concise website card without a simulated browser preview."""
    return (
        f'<article class="service-card website-card {card_class}">\n'
        '  <div class="website-card-body">\n'
        '    <div class="website-card-head">\n'
        f'      <span class="website-mark" aria-hidden="true">{mark}</span>\n'
        f'      <span class="badge {status_class}">{status}</span>\n'
        '    </div>\n'
        f'    <p class="service-kicker">{domain}</p>\n'
        f'    <h3>{name}</h3>\n'
        f'    <p>{description}</p>\n'
        f'    <a class="website-link" href="{url}" aria-label="Visit {name} website">Visit website →</a>\n'
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
            "Everkeep",
            "https://everkeep.goreecloud.com/",
            "everkeep.goreecloud.com",
            "The dedicated resilience and preservation website for recovery, continuity, portability, succession, assurance, and evidence-backed protection state.",
            "Platform System",
            "growing",
            "website-everkeep",
            "EK",
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
        '        <div class="section-heading website-heading">\n'
        '          <p class="eyebrow">GoreeCloud websites</p>\n'
        '          <h2>Ten focused destinations. One GoreeCloud ecosystem.</h2>\n'
        '          <p>The main site stays concise while dedicated destinations carry product, design, privacy, security, resilience, roadmap, publishing, and historical depth.</p>\n'
        '        </div>\n'
        '        <div class="service-grid website-grid">\n'
        f'          {rendered_cards}\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>\n'
    )


def story_section() -> str:
    milestones = (
        ("2026-06-01", "June 1, 2026", "Initial planning begins", "The first planning work starts with a goal of replacing subscription dependence with greater privacy, control, and data ownership."),
        ("2026-06-07", "June 7, 2026", "The GoreeCloud name is established", "GoreeCloud becomes the name for the complete ecosystem: hardware, software, infrastructure, services, configurations, and data."),
        ("2026-06-25", "June 25, 2026", "GoreeCloud.com is purchased", "The domain becomes the public identity for the platform and its future applications."),
        ("2026-08-12", "August 12, 2026", "Glaze UI and the software portfolio expand", "Glaze UI becomes the shared design language while the first-party software portfolio grows across productivity, organization, communication, and platform management."),
        ("2026-08-14", "August 14, 2026", "Native software ownership expands", "GoreeCloud Notes, Memos, Notify, and other first-party projects deepen the move from assembled services toward software directly governed by GoreeCloud."),
        ("2026-08-16", "August 16, 2026", "GoreeCloud Monitor enters public development", "Native availability and recovery monitoring begins its path toward replacing externally branded monitoring at the GoreeCloud experience layer."),
        ("2026-08-17", "August 17, 2026", "GoreeCloud-owned service layers expand", "Search, notifications, monitoring, and the public repository portfolio continue moving toward first-party interfaces and explicit GoreeCloud governance."),
    )
    rendered = []
    for datetime_value, label, title, description in milestones:
        rendered.append(
            '          <article class="story-milestone" role="listitem">\n'
            f'            <time datetime="{datetime_value}">{label}</time>\n'
            '            <span class="story-rail" aria-hidden="true"><span class="story-dot"></span></span>\n'
            '            <div class="story-card">\n'
            f'              <h3>{title}</h3>\n'
            f'              <p>{description}</p>\n'
            '            </div>\n'
            '          </article>'
        )
    rendered.append(
        '          <article class="story-milestone story-milestone-current" role="listitem">\n'
        '            <span class="story-current-label">Ongoing</span>\n'
        '            <span class="story-rail" aria-hidden="true"><span class="story-dot"></span></span>\n'
        '            <div class="story-card">\n'
        '              <h3>From homelab to documented personal cloud</h3>\n'
        '              <p>The project continues toward locally owned infrastructure with defined governance, recovery requirements, software standards, and long-term family continuity.</p>\n'
        '            </div>\n'
        '          </article>'
    )
    return (
        '\n    <section id="story" class="section story-section">\n'
        '      <div class="container story-layout">\n'
        '        <div class="story-intro">\n'
        '          <p class="eyebrow">The GoreeCloud story</p>\n'
        '          <h2>Built through deliberate milestones.</h2>\n'
        '          <p>GoreeCloud started in 2026 as a self-hosting plan and grew through a sequence of decisions about ownership, governance, first-party software, recoverability, and long-term preservation.</p>\n'
        '          <a class="story-archive-link" href="https://archive.goreecloud.com/">Explore the GoreeCloud Archive →</a>\n'
        '        </div>\n'
        '        <div class="story-timeline" role="list" aria-label="GoreeCloud milestones">\n'
        f'{chr(10).join(rendered)}\n'
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
        raise ValueError("homepage hero context could not be normalized")

    normalized, portfolio_count = PORTFOLIO_BLOCK.subn(websites_section(), normalized, count=1)
    if portfolio_count != 1:
        raise ValueError("homepage Suite/capability block could not be replaced with website hub")

    normalized, band_count = BAND_BLOCK.subn("\n", normalized, count=1)
    if band_count != 1:
        raise ValueError("duplicated homepage principle band could not be removed")

    normalized, story_count = STORY_BLOCK.subn(story_section(), normalized, count=1)
    if story_count != 1:
        raise ValueError("homepage story could not be normalized into the Glaze milestone timeline")

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

    for stylesheet in (WEBSITE_STYLESHEET, HOMEPAGE_STYLESHEET):
        if stylesheet not in normalized:
            normalized = normalized.replace("</head>", f"  {stylesheet}\n</head>", 1)

    hero = HERO_PREFIX.search(normalized)
    hero_text = hero.group(0) if hero else ""
    if "Private • Self-hosted • Recoverable" not in hero_text:
        raise ValueError("homepage hero focus label is missing")
    for label in PLATFORM_SYSTEM_LABELS:
        if label in hero_text:
            raise ValueError(f"platform-system detail must not be duplicated in the hero: {label}")
    if "GoreeCloud Identity" in hero_text:
        raise ValueError("GoreeCloud Identity must not appear in the homepage hero")

    if 'data-suite-app=' in normalized or 'data-capability=' in normalized:
        raise ValueError("Suite application/capability cards must live on suite.goreecloud.com, not the main homepage")
    if normalized.count('id="websites"') != 1:
        raise ValueError("homepage must contain exactly one GoreeCloud websites section")
    for domain in EXPECTED_WEBSITE_DOMAINS:
        if normalized.count(f'<p class="service-kicker">{domain}</p>') != 1:
            raise ValueError(f"homepage website portfolio must show destination domain exactly once: {domain}")
    website_section_match = re.search(r'<section id="websites".*?</section>', normalized, re.DOTALL)
    website_section = website_section_match.group(0) if website_section_match else ""
    if website_section.count('class="service-card website-card ') != len(EXPECTED_WEBSITE_DOMAINS):
        raise ValueError("homepage website portfolio card count must match the website manifest")
    if "website-preview" in website_section or "website-preview-browser" in website_section:
        raise ValueError("simulated browser previews must not appear in the website directory")
    if website_section.count('class="website-mark"') != len(EXPECTED_WEBSITE_DOMAINS):
        raise ValueError("each website card must include one compact site identity mark")
    if normalized.count('class="story-milestone') != 8:
        raise ValueError("homepage story must contain the complete eight-milestone sequence")
    if "2026 →" in normalized:
        raise ValueError("homepage story must use an explicit ongoing state instead of a fake future date")
    if 'href="https://archive.goreecloud.com/"' not in normalized:
        raise ValueError("homepage story must link to the dedicated GoreeCloud Archive")
    if '<section class="band" aria-label="Core principles">' in normalized:
        raise ValueError("duplicated homepage principle band must not return")
    for stylesheet in (WEBSITE_STYLESHEET, HOMEPAGE_STYLESHEET):
        if normalized.count(stylesheet) != 1:
            raise ValueError(f"homepage must include {stylesheet} exactly once")
    if "Open WebUI" in normalized or "AnythingLLM" in normalized:
        raise ValueError("retired AI front ends remain in the public homepage")
    return normalized
