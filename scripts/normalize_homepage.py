#!/usr/bin/env python3
"""Normalize current GoreeCloud homepage identities and roadmap product state."""

from __future__ import annotations

import re

HERO_LABELS = re.compile(
    r'<div class="hero-labels" aria-label="GoreeCloud platform (?:foundations|systems)">.*?</div>',
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


def canonical_hero_labels() -> str:
    return (
        '<div class="hero-labels" aria-label="GoreeCloud platform systems">\n'
        '            <a class="glaze-chip" href="https://design.goreecloud.com/">Glaze UI</a>\n'
        '            <a class="glaze-chip" href="https://privacy.goreecloud.com/">Privacy Shield</a>\n'
        '            <a class="glaze-chip" href="https://security.goreecloud.com/">Wardveil Security</a>\n'
        '            <span class="glaze-chip">Everkeep</span>\n'
        '            <span class="glaze-chip">GoreeCloud Mesh</span>\n'
        '            <span class="glaze-chip">GoreeCloud Identity</span>\n'
        '            <span class="eyebrow">Design • Privacy • Security • Resilience • Coordination • Identity</span>\n'
        '          </div>'
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
    normalized, hero_count = HERO_LABELS.subn(canonical_hero_labels(), source, count=1)
    if hero_count != 1:
        raise ValueError("homepage platform-system labels could not be normalized")

    normalized, ai_count = ROADMAP_AI_CARD.subn(goreecloud_ai_roadmap_card(), normalized, count=1)
    if ai_count != 1:
        raise ValueError("homepage GoreeCloud AI roadmap card could not be normalized")

    if normalized.count('>Everkeep</span>') != 1:
        raise ValueError("homepage must contain exactly one Everkeep platform chip")
    if "Open WebUI" in normalized or "AnythingLLM" in normalized:
        raise ValueError("retired AI front ends remain in the public homepage")
    return normalized
