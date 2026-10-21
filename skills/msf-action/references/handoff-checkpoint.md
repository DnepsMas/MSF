# Session handoff / context checkpoint

The checkpoint lets a fresh `$msf-action` session resume an explicitly named plan without chat history. It is a compact pointer; the development log and repository remain the detailed evidence.

## Location and identity

Create one file per execution attempt under:

```text
.msf/memory/sessions/YYYYMMDD-HHMM-action-<topic>.md
```

Append `-02`, `-03`, and so on on collision. Record a stable attempt ID in the file and update the same file throughout that attempt. Do not create a new checkpoint at every task boundary.

## Required content

```markdown
# Action checkpoint: <topic>

## Identity
- Updated: <timestamp with timezone>
- Mode: action
- Attempt ID: <stable ID>
- Plan: <exact repository-relative .msf/plan/*.ai.md path>
- Plan ID: <ID from plan>
- Development log: <exact repository-relative path>
- Repository baseline: <commit or explicit non-Git/unknown value>

## State
- Status: in_progress | waiting | partial | blocked | completed
- Current task: <task ID and short name, or none>
- Last completed task: <task ID, or none>
- Next action: <one exact action>
- Waiting on: <user/external dependency, or none>

## Working tree
- MSF-owned changes: <concise paths or groups>
- Pre-existing or unrelated changes: <concise paths or none>
- Unverified changes: <concise paths or none>

## Verification pointer
- Last check: <command/check and result, or none>
- Still required: <checks needed before completion>

## Resume guard
- Re-read: <minimum files/symbols needed next>
- Reconcile: <state or diff that must be checked before editing>
- Stop if: <material conflict, ambiguity, or authorization boundary>
```

Use repository-relative paths when possible. Keep entries factual and bounded. Do not copy full diffs, command logs, plan content, or conversation summaries.

## Update order

At a checkpoint boundary:

1. inspect the current worktree rather than relying on memory;
2. update the development log with task status, decisions, and evidence;
3. update the checkpoint pointer to that log state;
4. verify both files are readable and reference the same plan and attempt.

If only one write can finish, prioritize the development log because it is the execution record. The next session must treat a newer log than checkpoint as recoverable uncheckpointed progress.

## Resume protocol

The user still names the exact approved plan. For that plan only:

1. find unfinished checkpoints whose `Plan` and `Plan ID` match;
2. if exactly one coherent attempt exists, load it and its development log;
3. compare the recorded baseline, changed paths, and task state with the current repository;
4. rerun the smallest check needed to validate claimed progress;
5. update the checkpoint with the reconciled state before new production edits;
6. continue from the first incomplete dependency-ready task.

Never infer the plan from the newest checkpoint. Never overwrite or discard unexplained changes. If multiple unfinished attempts conflict, or the repository differs materially from both checkpoint and log, stop with the evidence and request a choice or a new Plan session.

## Closure

Set `completed`, `partial`, or `blocked`, include the exact next action, and ensure the development log contains the final change and verification record. Completed checkpoints remain as concise historical handoffs; do not delete them automatically.
