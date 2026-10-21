# Auto coordination checkpoint

The Auto checkpoint preserves coordinator state without duplicating the Action development log. Create one per Auto attempt:

```text
.msf/memory/sessions/YYYYMMDD-HHMM-auto-<topic>.md
```

Append `-02`, `-03`, and so on on collision. Update the same file throughout the attempt.

```markdown
# Auto checkpoint: <topic>

## Identity
- Updated: <timestamp with timezone>
- Mode: auto
- Attempt ID: <stable ID>
- Strength: Light | Medium | High | Ultra
- Human plan: <exact repository-relative path>
- Agent plan: <exact repository-relative .ai.md path>
- Plan ID: <ID from plan>
- Repository baseline: <commit or explicit non-Git/unknown value>

## Coordinator
- Status: planning | waiting_approval | waiting_model_selection | dispatching | supervising | reviewing | partial | blocked | completed
- Next action: <one exact coordinator action>
- Waiting on: <user, worker, external dependency, or none>

## Worker
- State: not_started | running | waiting | stopped | completion_candidate | completed | failed | unknown
- Model inventory source: <Agent tool schema accepted values, or other authoritative source>
- Model inventory observed: <timestamp with timezone>
- Available model identifiers: <exact accepted values, or unknown>
- Model originally requested: <user spelling, or none (host default)>
- Model resolved: <exact confirmed value, default, pending, or none>
- Model resolution: exact | default | confirmed_correction | waiting_user | rejected_after_spawn
- Suggested identifiers: <up to three closest exact identifiers, or none>
- Reasoning effort: <explicit supported value, or default>
- Worker identity: <Agent tool agent ID, or none>
- Spawn result: <confirmed, exact error, or not_started>
- Action checkpoint: <exact path, pending, or none>
- Development log: <exact path, pending, or none>
- Last meaningful event: <timestamp and concise event>

## Review
- Reviewer identity: <Agent tool agent ID, or none>
- Review report: <exact path, pending, or none>
- Verdict: accepted | needs_fixes | blocked | pending
- Fix rounds used: <0, 1, or 2>
- Follow-up candidates: <count and report path, or none>

## Supervision
- Corrections sent: <concise approved-contract clarifications, or none>
- Reconcile before next action: <live state that must be checked>
- Stop if: <material deviation, duplicate writer, lost authority, or other boundary>
```

Keep this file compact. The approved plan is the contract, the Action development log is the execution record, and the Action checkpoint is the worker recovery pointer. Do not paste transcripts, hidden reasoning, full diffs, secrets, credentials, or large command output.

Update it before dispatch, after each meaningful worker event or correction, before waiting or replacing a worker, and during closure. If the coordinator disappears, the next Auto session must treat the recorded worker identity as stale until Claude Code confirms that agent is still live.
