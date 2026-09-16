# MSF — My Skill Folder

[简体中文](README.zh-CN.md) | English

MSF is a lightweight, explicit Codex workflow for persistent project planning and disciplined execution across separate sessions. It keeps useful specification-driven rigor without forcing every coding request through a large skill chain.

## Skills

- `$msf-init` creates and summarizes the repository-local `.msf/` workspace.
- `$msf-plan` scales planning depth, investigates the repository, checks requirement/task coverage, and produces a dated approved human/agent plan pair without editing business files.
- `$msf-action` critically reviews and executes a user-specified plan in a new session, tracks recoverable task progress, diagnoses failures from evidence, and verifies acceptance before completion.

The skills never activate implicitly. `.msf/` belongs in the project repository; the skills themselves are installed in the user's Codex skill directory.

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

If MSF was previously installed under `~/.codex/skills`, migrate it instead of keeping both copies:

```powershell
python scripts/install.py --force --remove-legacy
```

The installer refuses to create duplicate menu entries when it detects the legacy copy. `--remove-legacy` removes only the three `msf-*` directories from the old location after installing the new copy.

The default destination is `~/.agents/skills`, Codex's user-level skills directory. Use `--destination <path>` for testing or a nonstandard location. Codex normally detects newly installed skills automatically; restart Codex if they do not appear.

Verify the installation in Codex with `/skills`, then explicitly invoke `$msf-init` inside the project where you want to use MSF.

## Update

Pull the latest version and replace the installed skill directories:

```powershell
git pull
python scripts/install.py --force
```

## Use

In a project session, explicitly invoke `$msf-init`. Start a separate session with `$msf-plan` to create an approved plan. Start another new session with `$msf-action` and name the exact `.msf/plan/*.ai.md` file to execute.

MSF defaults to Chinese user-facing replies. It prefers native choice prompts when the host exposes them and falls back to plain text. It does not require worktrees, subagents, TDD, or commits universally; repository rules and task risk decide when those practices apply.

## Development checks

```powershell
python -m unittest discover -s tests -v
python scripts/validate.py
```

## License

[MIT](LICENSE)
