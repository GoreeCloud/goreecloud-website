#!/usr/bin/env python3
"""Validate GitHub Actions supply-chain and least-privilege controls."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
VALIDATE_WORKFLOW = WORKFLOWS / "validate.yml"
REMOTE_VERIFY_WORKFLOW = WORKFLOWS / "verify-deployment.yml"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
USES_RE = re.compile(r"^\s*uses:\s*([^\s#]+)", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
WRITE_PERMISSION_RE = re.compile(r"(?mi)^\s*[A-Za-z0-9_-]+\s*:\s*write\s*(?:#.*)?$")
DIRECT_INPUT_IN_RUN_RE = re.compile(r"(?m)^\s*run:.*\$\{\{\s*inputs\.target\s*\}\}")
CHECKOUT_ACTION = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"  # v7.0.1
SETUP_PYTHON_ACTION = "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97"  # v7.0.0
SETUP_NODE_ACTION = "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020"  # v7.0.0
REQUIRED_ACTIONS = (CHECKOUT_ACTION, SETUP_PYTHON_ACTION, SETUP_NODE_ACTION)


def require(errors: list[str], text: str, marker: str, message: str) -> None:
    if marker not in text:
        errors.append(message)


def validate_read_only_workflow(path: Path, text: str, errors: list[str], label: str) -> None:
    if re.search(r"(?m)^\s*pull_request_target\s*:", text):
        errors.append(f"{label} must not use pull_request_target.")
    if re.search(r"(?mi)^\s*permissions\s*:\s*write-all\s*(?:#.*)?$", text):
        errors.append(f"{label} must not request write-all permissions.")
    if WRITE_PERMISSION_RE.search(text):
        errors.append(f"{label} must not request any write permission.")
    if "${{ secrets." in text:
        errors.append(f"{label} must not consume repository or environment secrets.")
    require(errors, text, "permissions:\n  contents: read", f"{label} must declare read-only contents permission.")
    require(errors, text, "persist-credentials: false", f"{label} checkout must keep persisted Git credentials disabled.")


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

    # The public validation workflow never needs elevated repository access or secrets.
    if not VALIDATE_WORKFLOW.exists():
        errors.append(".github/workflows/validate.yml is required.")
    else:
        validation = VALIDATE_WORKFLOW.read_text(encoding="utf-8")
        validate_read_only_workflow(VALIDATE_WORKFLOW, validation, errors, "Validation workflow")

        require(errors, validation, "concurrency:\n", "Validation workflow must define concurrency control.")
        require(errors, validation, "cancel-in-progress: true", "Validation workflow must cancel superseded runs.")
        require(errors, validation, "timeout-minutes: 10", "Validation job must retain its 10-minute timeout.")

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
            ("python scripts/verify_remote_deployment.py --check-config", "remote-verifier configuration check"),
        )
        for command, label in required_validation_commands:
            require(errors, validation, command, f"Validation workflow must run the {label}.")

        build_position = validation.find("python scripts/build_public_site.py")
        artifact_position = validation.find("python scripts/validate_build_artifact.py")
        if build_position >= 0 and artifact_position >= 0 and build_position > artifact_position:
            errors.append("Validation workflow must build the isolated public artifact before validating it.")

    # Remote verification is read-only. Manual inputs are constrained to a choice
    # and passed through an environment variable; the Python verifier independently
    # enforces a fixed host allowlist. A daily scheduled run verifies production on
    # the default branch without interpolating user-controlled input.
    if not REMOTE_VERIFY_WORKFLOW.exists():
        errors.append(".github/workflows/verify-deployment.yml is required.")
    else:
        remote = REMOTE_VERIFY_WORKFLOW.read_text(encoding="utf-8")
        validate_read_only_workflow(REMOTE_VERIFY_WORKFLOW, remote, errors, "Remote verification workflow")

        required_remote_markers = (
            ("workflow_dispatch:", "manual workflow_dispatch trigger"),
            ("type: choice", "choice-constrained deployment target"),
            ("- branch-preview", "branch-preview target option"),
            ("- production", "production target option"),
            ("schedule:", "scheduled production verification trigger"),
            ('cron: "17 8 * * *"', "off-hour daily schedule"),
            ('timezone: "America/Chicago"', "Central Time schedule"),
            ("timeout-minutes: 5", "five-minute verification timeout"),
            ("concurrency:\n", "concurrency control"),
            ("cancel-in-progress: true", "superseded-run cancellation"),
            (CHECKOUT_ACTION, "reviewed checkout action pin"),
            (SETUP_PYTHON_ACTION, "reviewed setup-python action pin"),
            ("python scripts/verify_remote_deployment.py --check-config", "verifier configuration check"),
            ("if: github.event_name == 'workflow_dispatch'", "manual-event guard"),
            ("TARGET: ${{ inputs.target }}", "environment-mediated target input"),
            ('python scripts/verify_remote_deployment.py --target "$TARGET"', "manual deployment verification command"),
            ("if: github.event_name == 'schedule'", "scheduled-event guard"),
            ("python scripts/verify_remote_deployment.py --target production", "fixed scheduled production verification command"),
        )
        for marker, label in required_remote_markers:
            require(errors, remote, marker, f"Remote verification workflow must retain its {label}.")

        if DIRECT_INPUT_IN_RUN_RE.search(remote):
            errors.append(
                "Remote verification workflow must not interpolate inputs.target directly into a run command; "
                "pass it through the TARGET environment variable and let the verifier enforce choices."
            )
        if remote.count("${{ inputs.target }}") != 1:
            errors.append("Remote verification workflow must reference inputs.target exactly once, through the TARGET environment variable.")
        if remote.count("- branch-preview") != 1 or remote.count("- production") != 1:
            errors.append("Remote verification workflow must expose exactly the branch-preview and production target choices.")
        if remote.count("schedule:") != 1:
            errors.append("Remote verification workflow must retain exactly one scheduled trigger block.")

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
