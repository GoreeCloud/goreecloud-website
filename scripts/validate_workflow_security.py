#!/usr/bin/env python3
"""Validate GitHub Actions supply-chain and least-privilege controls."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
VALIDATE_WORKFLOW = WORKFLOWS / "validate.yml"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
USES_RE = re.compile(r"^\s*uses:\s*([^\s#]+)", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
WRITE_PERMISSION_RE = re.compile(r"(?mi)^\s*[A-Za-z0-9_-]+\s*:\s*write\s*(?:#.*)?$")
REQUIRED_ACTIONS = (
    "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",  # v7.0.1
    "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",  # v7.0.0
    "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",  # v7.0.0
)


def require(errors: list[str], text: str, marker: str, message: str) -> None:
    if marker not in text:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    workflow_paths = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])

    if not workflow_paths:
        errors.append("No GitHub Actions workflow files were found.")

    # Every external action in every workflow must be immutable. Local actions and
    # docker:// references are not Git refs and are intentionally exempt here.
    for path in workflow_paths:
        text = path.read_text(encoding="utf-8")
        for action_ref in USES_RE.findall(text):
            if action_ref.startswith("./") or action_ref.startswith("docker://"):
                continue
            if "@" not in action_ref:
                errors.append(f"External action is missing an immutable ref in {path.relative_to(ROOT)}: {action_ref}")
                continue
            action, ref = action_ref.rsplit("@", 1)
            if not action or not SHA_RE.fullmatch(ref):
                errors.append(
                    f"External action must be pinned to a full 40-character commit SHA in "
                    f"{path.relative_to(ROOT)}: {action_ref}"
                )

    # The public validation workflow never needs elevated repository access or
    # repository secrets. Keep these requirements specific to validate.yml so a
    # future deployment workflow can carry separately justified permissions.
    if not VALIDATE_WORKFLOW.exists():
        errors.append(".github/workflows/validate.yml is required.")
    else:
        validation = VALIDATE_WORKFLOW.read_text(encoding="utf-8")

        if re.search(r"(?m)^\s*pull_request_target\s*:", validation):
            errors.append("Validation workflow must not use pull_request_target.")
        if re.search(r"(?mi)^\s*permissions\s*:\s*write-all\s*(?:#.*)?$", validation):
            errors.append("Validation workflow must not request write-all permissions.")
        if WRITE_PERMISSION_RE.search(validation):
            errors.append("Validation workflow must not request any write permission.")
        if "${{ secrets." in validation:
            errors.append("Validation workflow must not consume repository or environment secrets.")

        require(errors, validation, "permissions:\n  contents: read", "Validation workflow must declare read-only contents permission.")
        require(errors, validation, "concurrency:\n", "Validation workflow must define concurrency control.")
        require(errors, validation, "cancel-in-progress: true", "Validation workflow must cancel superseded runs.")
        require(errors, validation, "timeout-minutes: 10", "Validation job must retain its 10-minute timeout.")
        require(errors, validation, "persist-credentials: false", "Checkout must keep persisted Git credentials disabled.")

        for action_ref in REQUIRED_ACTIONS:
            require(
                errors,
                validation,
                action_ref,
                f"Validation workflow must retain the reviewed Node 24-capable immutable action pin: {action_ref}",
            )

        required_validation_commands = (
            ("python scripts/validate_workflow_security.py", "workflow-security validator"),
            ("python scripts/validate_performance_budget.py", "performance-budget validator"),
            ("python scripts/build_public_site.py", "isolated public-site build"),
            ("python scripts/validate_build_artifact.py", "isolated build-artifact validator"),
        )
        for command, label in required_validation_commands:
            require(errors, validation, command, f"Validation workflow must run the {label}.")

        build_position = validation.find("python scripts/build_public_site.py")
        artifact_position = validation.find("python scripts/validate_build_artifact.py")
        if build_position >= 0 and artifact_position >= 0 and build_position > artifact_position:
            errors.append("Validation workflow must build the isolated public artifact before validating it.")

    if not DEPENDABOT.exists():
        errors.append(".github/dependabot.yml is required to keep pinned GitHub Actions reviewably updated.")
    else:
        dependabot = DEPENDABOT.read_text(encoding="utf-8")
        required_markers = (
            'package-ecosystem: "github-actions"',
            'directory: "/"',
            'interval: "weekly"',
            'day: "monday"',
            "open-pull-requests-limit: 5",
        )
        for marker in required_markers:
            if marker not in dependabot:
                errors.append(f"Dependabot GitHub Actions configuration is missing: {marker}")

    if errors:
        print("Workflow security validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Workflow security validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
