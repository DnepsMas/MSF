"""Validate MSF package structure, references, and workflow contracts."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("msf-init", "msf-plan", "msf-action", "msf-review", "msf-auto")


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
        frontmatter = text.split("---")[1]
        require("disable-model-invocation: true" in frontmatter, f"{name}: must be explicit-only")
        require(not (folder / "agents").exists(), f"{name}: Codex agents metadata must not ship")
        require("Reply to the user in Chinese by default" in text, f"{name}: default Chinese rule missing")

    init_sections = sections(contents["msf-init"])
    plan_sections = sections(contents["msf-plan"])
    action_sections = sections(contents["msf-action"])
    review_sections = sections(contents["msf-review"])
    auto_sections = sections(contents["msf-auto"])
    require({"scope", "establish project context", "version-control invariant", "verify and report"} <= init_sections, "msf-init: incomplete lifecycle")
    require("<HARD-GATE>" in contents["msf-plan"], "msf-plan: strength gate missing")
    require({"non-implementation boundary", "load context deliberately", "scale the work", "planning loop", "persist at planning checkpoints"} <= plan_sections, "msf-plan: incomplete lifecycle")
    require("Do not wait for the user to request a file" in contents["msf-plan"], "msf-plan: proactive draft persistence missing")
    require("Normally make one consolidated report update per such turn" in contents["msf-plan"], "msf-plan: batched persistence missing")
    require("status `draft`" in contents["msf-plan"], "msf-plan: draft lifecycle missing")
    require("Never transition to implementation in this session" in contents["msf-plan"], "msf-plan: session boundary missing")
    require("<HARD-GATE>" in contents["msf-action"], "msf-action: entry gate missing")
    require({"load narrowly", "preflight before edits", "execute task by task", "checkpoint automatically", "completion gate", "close every meaningful session"} <= action_sections, "msf-action: incomplete lifecycle")
    require("Never select the newest plan" in contents["msf-action"], "msf-action: explicit plan selection missing")
    require("before the first production mutation" in contents["msf-action"], "msf-action: pre-mutation checkpoint missing")
    require("The `.msf` records, not chat history" in contents["msf-action"], "msf-action: context handoff contract missing")
    require("<HARD-GATE>" in contents["msf-review"], "msf-review: entry gate missing")
    require({"boundary", "load narrowly", "choose the layers", "run the review", "report"} <= review_sections, "msf-review: incomplete lifecycle")
    require("Do not use computer-use" in contents["msf-review"], "msf-review: computer-use ban missing")
    require("<HARD-GATE>" in contents["msf-auto"], "msf-auto: entry gate missing")
    require({"context boundary", "plan", "open the coordination checkpoint", "resolve the action model", "dispatch the action worker", "supervise without micromanaging", "verify and close", "resume"} <= auto_sections, "msf-auto: incomplete lifecycle")
    require("never use `subagent_type = \"fork\"`" in contents["msf-auto"], "msf-auto: fresh worker boundary missing")
    require("exposes no model inventory" in contents["msf-auto"], "msf-auto: runtime model resolution missing")
    require("Never silently correct" in contents["msf-auto"], "msf-auto: model typo confirmation missing")
    require("must not start a second writer" in contents["msf-auto"], "msf-auto: single-writer rule missing")
    require("must not expand it" in contents["msf-auto"], "msf-auto: correction boundary missing")
    print("MSF package validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
