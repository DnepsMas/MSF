# Development log and recovery checkpoint

Create at first mutation:

```text
.msf/devlog/YYYY-MM-DD-<plan-topic>.md
```

On collision append `-02`, `-03`, and so on. Update the same log throughout one execution attempt.

```markdown
# <Plan title> — Development Log

## Run
- Plan path / plan ID
- Action checkpoint path / attempt ID
- Started / last updated
- Status: in_progress | completed | partial | blocked
- Repository baseline when available

## Task status
| Task | Status | Changed targets | Verification evidence | Notes/deviation |

## Decisions and deviations
- What changed from the plan, why it remained compatible, and impact

## Verification record
- Exact command/check
- Exit/result
- Scope and interpretation

## Remaining work or blockers
- First safe next action

## Final change summary
- Files grouped by purpose
- Acceptance evidence
```

Keep it concise. Do not paste large raw logs, secrets, or full diffs. The log records execution state; the approved plan remains immutable.
