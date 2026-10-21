# MSF — My Skill Folder

[简体中文](README.zh-CN.md) | English

MSF is a lightweight, explicit Claude Code workflow for persistent project planning and disciplined execution across separate sessions. It keeps useful specification-driven rigor without forcing every coding request through a large skill chain.

## Skills

- `/msf-init` creates and summarizes the repository-local `.msf/` workspace.
- `/msf-plan` scales planning depth, investigates the repository, checks requirement/task coverage, and produces a dated approved human/agent plan pair without editing business files.
- `/msf-action` critically reviews and executes a user-specified plan in a new session, automatically checkpoints recoverable context under `.msf`, diagnoses failures from evidence, and verifies acceptance before completion.
- `/msf-auto` plans in the parent session, obtains approval, dispatches a fresh-context Action subagent, supervises corrections, and independently verifies completion without merging the two agent contexts.

The skills never activate implicitly. `.msf/` belongs in the project repository; the skills themselves are installed in the user's Claude Code skills directory.

## Install

Requires Python 3. Run from this repository:

```powershell
git clone https://github.com/DnepsMas/MSF.git
cd MSF
python scripts/install.py
```

To replace an older MSF installation:

```powershell
python scripts/install.py --force
```

The default destination is `~/.claude/skills`, Claude Code's personal skills directory; copy the `msf-*` folders into a project's `.claude/skills/` instead to scope MSF to one repository. Use `--destination <path>` for testing or a nonstandard location. Claude Code picks up new skills in a running session automatically when `~/.claude/skills` already existed; otherwise restart it. On WSL, `~` is the WSL home, not the Windows one.

Verify the installation by typing `/msf` in Claude Code, then explicitly invoke `/msf-init` inside the project where you want to use MSF.

## Update

Pull the latest version and replace the installed skill directories:

```powershell
git pull
python scripts/install.py --force
```

## Use

In a project session, explicitly invoke `/msf-init`. Start a separate session (a new terminal or `/clear`) with `/msf-plan` to create an approved plan. Start another new session with `/msf-action` and name the exact `.msf/plan/*.ai.md` file to execute.

Alternatively, invoke `/msf-auto` with a planning strength to keep one coordinator session from planning through supervised execution. After approval, Auto spawns a fresh-context Action subagent through the `Agent` tool (it never forks the coordinator's chat) and uses the host default model unless you name one. A named model must exactly match a value the `Agent` tool accepts; otherwise Auto shows up to three close candidates and waits for confirmation instead of silently correcting or downgrading. The coordinator waits for the worker, steers it with `SendMessage`, and verifies independently, but does not edit production files. Resume interrupted supervision with `/msf-auto resume <exact .ai.md path>`.

During Action, MSF writes an Action checkpoint before production edits and refreshes it at task, verification, waiting, interruption, and closure boundaries. After a model switch, capacity limit, crash, or intentional new session, invoke `/msf-action` again with the same exact plan path. It will use the matching `.msf/memory/sessions/` checkpoint and development log, reconcile them with the real worktree, and resume without relying on chat history. A sudden failure can lose work since the most recent checkpoint, so unrecorded changes are always treated as unverified until reconciled.

MSF defaults to Chinese user-facing replies. It uses `AskUserQuestion` for choices when available and falls back to plain text. It does not require worktrees, subagents, TDD, or commits universally; repository rules and task risk decide when those practices apply.

## Development checks

```powershell
python -m unittest discover -s tests -v
python scripts/validate.py
```

## License

[MIT](LICENSE)
