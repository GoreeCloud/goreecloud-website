#!/usr/bin/env python3
"""Validate repository contribution guidance and public/private safety boundaries."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ISSUE_CONFIG = ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml"
BUG_FORM = ROOT / ".github" / "ISSUE_TEMPLATE" / "bug-report.yml"
FEATURE_FORM = ROOT / ".github" / "ISSUE_TEMPLATE" / "feature-request.yml"
PR_TEMPLATE = ROOT / ".github" / "pull_request_template.md"
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
README = ROOT / "README.md"
SECURITY_URL = "https://www.goreecloud.com/security.html"
PRIVATE_PATTERNS = (
    re.compile(r"\b10(?:\.\d{1,3}){3}\b"),
    re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2}\b"),
)
SENSITIVE_TERMS = ("goreecloud-vps-01", ".netbird.selfhosted")


def require_markers(path: Path, markers: tuple[str, ...], errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Required repository guidance file is missing: {path.relative_to(ROOT)}")
        return ""

    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    for marker in markers:
        if marker.lower() not in lower:
            errors.append(f"{path.relative_to(ROOT)} is missing required guidance: {marker}")
    return text


def main() -> int:
    errors: list[str] = []

    config = require_markers(
        ISSUE_CONFIG,
        (
            "blank_issues_enabled: false",
            SECURITY_URL,
            "do not publish vulnerability details",
        ),
        errors,
    )
    bug = require_markers(
        BUG_FORM,
        (
            "name: Bug report",
            SECURITY_URL,
            "do not include security vulnerability details",
            "credentials",
            "private infrastructure",
            "private ip addresses",
            "this is not a security vulnerability report",
        ),
        errors,
    )
    feature = require_markers(
        FEATURE_FORM,
        (
            "name: Feature request",
            SECURITY_URL,
            "private infrastructure",
            "passing ci does not by itself authorize",
        ),
        errors,
    )
    pr_template = require_markers(
        PR_TEMPLATE,
        (
            "## Validation",
            "## Privacy and security boundary",
            SECURITY_URL,
            "private hostnames",
            "private ip addresses",
            "passing CI does not by itself authorize",
            "issue #5",
        ),
        errors,
    )
    workflow = require_markers(
        WORKFLOW,
        (
            "Validate repository guidance",
            "python scripts/validate_repository_guidance.py",
        ),
        errors,
    )
    readme = require_markers(
        README,
        (
            "python scripts/build_public_site.py",
            "Build output directory: `dist`",
            "issue #5",
            "issue #6",
            "Passing CI does not itself authorize",
        ),
        errors,
    )

    for path, text in (
        (ISSUE_CONFIG, config),
        (BUG_FORM, bug),
        (FEATURE_FORM, feature),
        (PR_TEMPLATE, pr_template),
        (README, readme),
    ):
        if not text:
            continue
        for pattern in PRIVATE_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(f"Private-range IP address found in {path.relative_to(ROOT)}: {match.group(0)}")
        lower = text.lower()
        for term in SENSITIVE_TERMS:
            if term.lower() in lower:
                errors.append(f"Private infrastructure identifier found in {path.relative_to(ROOT)}: {term}")

    if config.count("url: https://") != 1:
        errors.append("Issue-template config must expose exactly one HTTPS contact link: the security-reporting policy.")
    if "blank_issues_enabled: true" in config:
        errors.append("Blank issues must remain disabled so reporters receive the public/private safety guidance.")

    if bug.count("required: true") < 6:
        errors.append("Bug report form must keep its required reproduction and safety confirmations.")
    if feature.count("required: true") < 4:
        errors.append("Feature request form must keep its required need, proposal, impact, and boundary confirmations.")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print("Repository guidance validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Repository guidance validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
