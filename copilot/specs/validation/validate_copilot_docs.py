#!/usr/bin/env python3
"""Validation checks for Copilot workflow docs."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
COPILOT = ROOT / "copilot"

AGENTS = COPILOT / "agents"
SKILLS = COPILOT / "skills"
TEMPLATES = COPILOT / "TEMPLATES.md"
INTEGRATION = COPILOT / "COPILOT_INTEGRATION.md"


REQUIRED_TEMPLATE_HEADERS = [
    "## Checkpoint Template",
    "## Skill Invocation Template",
    "## Error Handling Template",
    "## Safety Violation Template",
    "## Completion Template",
    "## Mandatory Structured Payload (Machine-Checkable)",
]


def fail(msg: str) -> None:
    print(f"❌ {msg}")


def ok(msg: str) -> None:
    print(f"✅ {msg}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_agents(errors: list[str]) -> None:
    for file in sorted(AGENTS.glob("*.agent.md")):
        text = read(file)

        if "## Quick Example" not in text:
            errors.append(f"{file.relative_to(ROOT)} missing section: ## Quick Example")

        if "## Error Handling" not in text:
            errors.append(f"{file.relative_to(ROOT)} missing section: ## Error Handling")

        has_flow = (
            "## Execution Flow" in text
            or "## Execution Configuration" in text
            or re.search(r"##\s+\d+-Stage Process", text) is not None
            or re.search(r"##\s+\d+-Phase Process", text) is not None
        )
        if not has_flow:
            errors.append(
                f"{file.relative_to(ROOT)} missing execution flow/configuration section"
            )

        has_do_dont = (
            "## DO and DON'T" in text
            or ("## DO:" in text and "## DON'T:" in text)
        )
        if not has_do_dont:
            errors.append(f"{file.relative_to(ROOT)} missing DO/DON'T sections")


def check_templates(errors: list[str]) -> None:
    text = read(TEMPLATES)
    for header in REQUIRED_TEMPLATE_HEADERS:
        if header not in text:
            errors.append(f"{TEMPLATES.relative_to(ROOT)} missing header: {header}")


def check_stage_references(errors: list[str]) -> None:
    # Ensure stages referenced stay inside 1..9 for this workflow design.
    paths = [INTEGRATION, *sorted(AGENTS.glob("*.agent.md"))]
    pattern = re.compile(r"\b[Ss]tage[s]?\s*(\d+)(?:\s*[-–]\s*(\d+))?")
    for path in paths:
        text = read(path)
        for m in pattern.finditer(text):
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            if a < 1 or b > 9:
                errors.append(
                    f"{path.relative_to(ROOT)} has out-of-range stage reference: {m.group(0)}"
                )


def check_skill_references(errors: list[str]) -> None:
    skill_files = {p.name for p in SKILLS.glob("*.skill.md")}
    paths = [INTEGRATION, *sorted(AGENTS.glob("*.agent.md"))]
    ref = re.compile(r"([a-z0-9-]+\.skill\.md)")
    for path in paths:
        text = read(path)
        for name in ref.findall(text):
            if name not in skill_files:
                errors.append(
                    f"{path.relative_to(ROOT)} references missing skill file: {name}"
                )


def check_normative_docs(errors: list[str]) -> None:
    required = [
        COPILOT / "COPILOT_INTEGRATION.md",
        COPILOT / "TEMPLATES.md",
        COPILOT / "specs" / "EXECUTION_RULES.md",
        COPILOT / "specs" / "NORMATIVE_SOURCES.md",
        COPILOT / "specs" / "TOKEN_BUDGET_POLICY.md",
        COPILOT / "specs" / "VERSIONING_POLICY.md",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing required doc: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    check_agents(errors)
    check_templates(errors)
    check_stage_references(errors)
    check_skill_references(errors)
    check_normative_docs(errors)

    if errors:
        for e in errors:
            fail(e)
        fail(f"Validation failed with {len(errors)} error(s)")
        return 1

    ok("All Copilot doc validation checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
