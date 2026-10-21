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
- Model inventory source: <native tool metadata, runtime catalog, unavailable, or other authoritative source>
- Model inventory observed: <timestamp with timezone>
- Available model identifiers: <exact current identifiers, unavailable, or unknown>
- Model originally requested: <user spelling, default gpt-6-luna, or none>
- Model resolved: <exact confirmed identifier, pending, or none>
- Model resolution: exact | confirmed_correction | waiting_user | inventory_unavailable | rejected_after_spawn
- Suggested identifiers: <up to three closest exact identifiers, or none>
- Reasoning effort: <resolved supported value, pending, or default>
- Worker identity: <native subagent ID, or none>
- Spawn result: <confirmed, exact error, or not_started>
- Action checkpoint: <exact path, pending, or none>
- Development log: <exact path, pending, or none>
- Last meaningful event: <timestamp and concise event>

## Supervision
- Corrections sent: <concise approved-contract clarifications, or none>
- Reconcile before next action: <live state that must be checked>
- Stop if: <material deviation, duplicate writer, lost authority, or other boundary>
```

Keep this file compact. The approved plan is the contract, the Action development log is the execution record, and the Action checkpoint is the worker recovery pointer. Do not paste transcripts, hidden reasoning, full diffs, secrets, credentials, or large command output.

Update it before dispatch, after each meaningful worker event or correction, before waiting or replacing a worker, and during closure. If the coordinator disappears, the next Auto session must treat the recorded worker identity as stale until Codex confirms that subagent is still live.
