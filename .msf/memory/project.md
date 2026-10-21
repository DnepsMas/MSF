# Project memory

## Project overview

MSF (My Skill Folder) is a lightweight, explicit Claude Code workflow (the `claude` branch; `main` targets Codex) for persistent project planning and execution. It packages four explicitly invoked skills: `msf-init`, `msf-plan`, `msf-action`, and `msf-auto`.

## Technology and structure

- Python 3 is required for installation and validation tooling.
- `skills/` contains the four Claude Code skill packages and their instructions, references, and assets.
- `scripts/install.py` installs the skills into `~/.claude/skills`.
- `scripts/validate.py` validates package structure and workflow invariants.
- `tests/test_install.py` contains unit tests for fresh, guarded, forced, and dry-run installation behavior.
- `demo/agent-canvas/index.html` is a standalone, zero-dependency concept demo for a visual Agent orchestration canvas.

## Verified commands

- `python -m unittest discover -s tests -v`
- `python scripts/validate.py`

## Durable constraints

- MSF skills activate only when explicitly invoked.
- Repository-local `.msf/` content is intended to remain eligible for version control.
- Planning and action occur in separate sessions, and action requires the user to name the exact plan file.

## Decisions

- Keep persistent plans, development logs, project memory, and session handoffs under `.msf/`.
- Action sessions create a per-attempt context checkpoint before production edits, refresh it at meaningful execution boundaries, and recover only after matching the user-named plan and reconciling the real worktree.
- Auto sessions preserve the Plan/Action context boundary while one coordinator plans, spawns a fresh-context Action worker via the `Agent` tool, supervises corrections, and independently verifies completion.
