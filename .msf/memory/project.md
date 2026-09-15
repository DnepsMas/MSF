# Project memory

## Project overview

MSF (My Skill Folder) is a lightweight, explicit Codex workflow for persistent project planning and execution across separate sessions. It packages three explicitly invoked skills: `msf-init`, `msf-plan`, and `msf-action`.

## Technology and structure

- Python 3 is required for installation and validation tooling.
- `skills/` contains the three Codex skill packages and their instructions, references, assets, and agent metadata.
- `scripts/install.py` installs the skills into a Codex skills directory.
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
