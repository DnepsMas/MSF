"""Validate MSF package structure, references, and workflow contracts."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
SKILLS = ("msf-init", "msf-plan", "msf-action")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sections(text: str) -> set[str]:
    return {match.group(1).strip().lower() for match in re.finditer(r"^## (.+)$", text, re.MULTILINE)}


def validate_links(skill_dir: Path, text: str) -> None:
    for raw in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if "://" not in raw and not raw.startswith("#"):
            require((skill_dir / raw).exists(), f"{skill_dir.name}: broken reference {raw}")


def main() -> int:
    contents: dict[str, str] = {}
    for name in SKILLS:
        folder = ROOT / "skills" / name
        skill_file = folder / "SKILL.md"
        require(skill_file.is_file(), f"{name}: missing SKILL.md")
        text = skill_file.read_text(encoding="utf-8")
        contents[name] = text
        validate_links(folder, text)
        yaml = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
        require("allow_implicit_invocation: false" in yaml, f"{name}: must be explicit-only")
        require("Reply to the user in Chinese by default" in text, f"{name}: default Chinese rule missing")
        if VALIDATOR.is_file():
            subprocess.run([sys.executable, str(VALIDATOR), str(folder)], check=True)

    init_sections = sections(contents["msf-init"])
    plan_sections = sections(contents["msf-plan"])
    action_sections = sections(contents["msf-action"])
    require({"scope", "establish project context", "version-control invariant", "verify and report"} <= init_sections, "msf-init: incomplete lifecycle")
    require("<HARD-GATE>" in contents["msf-plan"], "msf-plan: strength gate missing")
    require({"non-implementation boundary", "load context deliberately", "scale the work", "planning loop"} <= plan_sections, "msf-plan: incomplete lifecycle")
    require("Never transition to implementation in this session" in contents["msf-plan"], "msf-plan: session boundary missing")
    require("<HARD-GATE>" in contents["msf-action"], "msf-action: entry gate missing")
    require({"load narrowly", "preflight before edits", "execute task by task", "completion gate", "close every meaningful session"} <= action_sections, "msf-action: incomplete lifecycle")
    require("Never select the newest plan" in contents["msf-action"], "msf-action: explicit plan selection missing")
    print("MSF package validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
