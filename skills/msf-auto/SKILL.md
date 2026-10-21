---
name: msf-auto
description: Plan, obtain approval, dispatch a fresh-model MSF Action worker, supervise execution, and verify completion in one explicitly invoked coordinator session.
---

# MSF Auto

Give the user one supervised workflow while preserving separate planning and execution contexts. The parent agent plans, coordinates, and verifies; only the fresh Action worker edits production files.

## Communication

Reply to the user in Chinese by default. Switch only when explicitly requested. Preserve code, commands, paths, identifiers, and quoted text in their necessary original form.

<HARD-GATE>
Run only after explicit invocation.

For a new workflow, require the user to supply Light, Medium, High, or Ultra. If absent, the first response MUST ask for the strength, briefly describe all four levels, and STOP. Never infer, recommend, or auto-select it.

For recovery, require `resume` plus one exact `.msf/plan/*.ai.md` path. Never select the newest plan, infer an active plan, or accept a directory.

If the repository-local MSF baseline is missing, stop and instruct the user to explicitly invoke `$msf-init` before retrying Auto.
</HARD-GATE>

## Context boundary

Auto combines the user experience, not the agent contexts:

- The coordinator may inspect the repository and write planning, memory, and coordination records under `.msf/`.
- Before approval it must not edit business files, tests, configuration, dependencies, or Git state.
- After approval it still must not edit production files; it delegates the approved plan to one fresh Action worker.
- The worker receives artifact paths and repository facts, not inherited chat history.
- While the worker owns execution, the coordinator is read-only for production files and must not start a second writer in the same checkout.

## Plan

Use the existing planning contracts rather than inventing an Auto-specific plan format:

- scale investigation with [planning levels](../msf-plan/references/planning-levels.md);
- persist the human and agent plan pair with [plan format](../msf-plan/references/plan-format.md);
- pass the [readiness check](../msf-plan/references/readiness-check.md);
- record draft or approved planning conclusions with [the Plan session format](../msf-plan/references/session-format.md).

Investigate, clarify consequential requirements, batch draft writes at meaningful checkpoints, present the design and execution outline, and obtain explicit approval. Do not create the `.ai.md` file or dispatch a worker before approval.

Invoking Auto expresses the user's intent to continue into supervised execution after approval, but approval authorizes only the approved plan. It does not authorize commits, pushes, releases, installations, destructive operations, credentials, external messages, or other effects absent from that contract.

## Open the coordination checkpoint

After approval, finalize the plan pair and create one Auto checkpoint before dispatch using [references/coordination-checkpoint.md](references/coordination-checkpoint.md). Record the exact plan path, Plan ID, coordinator state, repository baseline, requested worker model, and next action.

## Resolve the Action model

Before dispatch, resolve the Action model against the current host's authoritative model inventory exposed by the native subagent tool or runtime catalog. Never treat model names in this skill, a README, memory, or an earlier checkpoint as proof that the model is still available.

- If the user did not name an Action model, prefer `gpt-6-luna` only when the current inventory contains that exact identifier. If the inventory proves it is absent or renamed, set the Auto checkpoint to `waiting_model_selection`, show the exact currently available model identifiers, ask the user which one to use, and STOP before spawn.
- If the user named a model, require an exact current identifier after trimming surrounding whitespace. Never silently correct, alias, upgrade, downgrade, or substitute it.
- When an exact match fails, report the requested spelling. If normalized comparison or conservative typo similarity finds plausible entries, show at most three closest available identifiers and ask the user to confirm one. Otherwise show the available identifiers and ask for an exact selection. STOP before spawn in either case.
- If the host exposes no model inventory, state that preflight validation is unavailable. An exact user-supplied identifier or the default Luna preference may be attempted once; a model-resolution rejection must then follow the recovery rule below rather than being treated as a generic execution failure.

Resolve reasoning effort from the selected model's current supported values. Use `high` by default for Luna when supported. For another model, preserve an explicit supported user choice; otherwise use that model's documented default. If an explicit effort is unsupported, report the supported values and ask the user to choose rather than silently changing it.

Record the inventory source and observation time, originally requested model, resolved exact model, resolution status, suggestions, and reasoning effort in the Auto checkpoint. User confirmation applies only to that exact resolved identifier; refresh resolution before any later replacement worker.

## Dispatch the Action worker

Use Codex's native subagent primitive. Spawn exactly one fresh worker with:

- the exact model identifier resolved and, when necessary, confirmed above;
- the supported reasoning effort resolved above;
- no inherited turns or conversation context (`fork_turns=none` or the host equivalent);
- a stable task name derived from the Plan ID;
- the same checkout so the approved `.msf` artifacts and current worktree are visible.

When the Codex collaboration tools are exposed, make the equivalent of this exact call rather than merely describing it:

```text
spawn_agent(
  task_name = "msf_action_<plan-id>",
  fork_turns = "none",
  model = <resolved exact model identifier>,
  reasoning_effort = <resolved supported effort>,
  message = <bounded Action dispatch>
)
```

The worker prompt must include the repository root, exact `.ai.md` path, Plan ID, Auto checkpoint path, authorization boundaries, and these instructions: this fresh worker thread is the separate Action session required by `$msf-action`; explicitly invoke `$msf-action` for that exact plan; follow its preflight/devlog/checkpoint/verification protocol; report meaningful status or blockers to the coordinator.

An explicit spawn model overrides inherited/default subagent model settings. Record the returned worker identity and actual requested model in the Auto checkpoint. Do not silently substitute the coordinator model or claim a model was used if spawn did not confirm success.

If spawn returns `invalid_model`, `model_not_found`, `unsupported_model`, or an equivalent model-resolution rejection, treat the earlier resolution as stale: refresh the authoritative inventory, record the exact error and new inventory, set Auto to `waiting_model_selection`, offer closest current identifiers when useful, ask the user for one exact model, and STOP. This handles a model renamed or removed between preflight and spawn.

If the exact model still exists but is temporarily unavailable, capacity-exhausted, or inaccessible to the signed-in account, distinguish that condition from a spelling error. Record the exact error and ask whether the user wants to retry that exact model later or select one of the currently accessible identifiers. For disabled subagents or other non-model prerequisites, set Auto to `blocked` and report the concrete prerequisite.

Do not ask the user to copy a command, do not implement inside the coordinator, and do not silently retry with, downgrade to, or substitute any unconfirmed model.

## Supervise without micromanaging

Use the host's native agent controls:

- use `wait_agent` for worker progress or completion with bounded event-driven waits;
- use `send_message` while it is running to clarify or correct the current turn;
- use `followup_task` when it is idle and additional approved work remains;
- use `interrupt_agent` only to pause, abort, or prevent an imminent material deviation.

Ask the worker to report only meaningful events: task or verification checkpoint completed, question or required decision, plan deviation or repository conflict, verification failure or external blocker, and completion candidate.

At every event, read the Action checkpoint and development log before responding. Send the smallest useful correction. A correction may clarify or restore the approved contract, but must not expand it. If the needed change is material to scope, architecture, behavior, compatibility, security, or data handling, pause the worker, checkpoint the state, return to planning, and obtain new approval.

Do not continuously poll a healthy worker, duplicate its edits, or treat silence as failure. Do not blindly restart after failure. A replacement worker is allowed only after reconciling the latest repository and checkpoint state; more than one replacement for the same unresolved condition requires user direction.

## Verify and close

The worker may report a completion candidate; the coordinator owns final acceptance. Independently inspect the final diff, Action devlog, Action checkpoint, fresh verification evidence, plan coverage, deviations, and unexplained worktree changes. Send compatible fixes back to the same worker when possible.

Mark the Auto checkpoint `completed` only when the approved acceptance criteria are satisfied. Otherwise close it as `partial` or `blocked` with the exact next action. Report the plan pair, worker model and identity, Action records, verification evidence, deviations, risks, and final Auto checkpoint path.

## Resume

For `$msf-auto resume <exact-plan.ai.md>`, load only Auto checkpoints matching both the exact plan path and Plan ID. Reconcile the checkpoint with the Action devlog/checkpoint, live worktree, and native subagent state before acting. Resume supervision when the recorded worker is live; otherwise refresh model resolution and spawn a fresh worker from the first incomplete dependency-ready task only after any required user confirmation. Never duplicate a live writer or trust recorded completion without fresh evidence.
