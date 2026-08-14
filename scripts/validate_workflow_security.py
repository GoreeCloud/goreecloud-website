#!/usr/bin/env python3
"""Validate GitHub Actions supply-chain controls without third-party packages."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
USES_RE = re.compile(r"^\s*uses:\s*([^\s#]+)", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def main() -> int:
    errors: list[str] = []
    workflow_paths = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])

    if not workflow_paths:
        errors.append("No GitHub Actions workflow files were found.")

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

    if not DEPENDABOT.exists():
        errors.append(".github/dependabot.yml is required to keep pinned GitHub Actions reviewably updated.")
    else:
        dependabot = DEPENDABOT.read_text(encoding="utf-8")
        required_markers = (
            'package-ecosystem: "github-actions"',
            'directory: "/"',
            'interval: "weekly"',
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
