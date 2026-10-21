---
name: msf-auto
description: Plan, obtain approval, dispatch a fresh-context MSF Action worker, supervise execution, and verify completion in one explicitly invoked coordinator session.
disable-model-invocation: true
---

# MSF Auto

Give the user one supervised workflow while preserving separate planning and execution contexts. The parent agent plans, coordinates, and verifies; only the fresh Action worker edits production files.

## Communication

Reply to the user in Chinese by default. Switch only when explicitly requested. Preserve code, commands, paths, identifiers, and quoted text in their necessary original form.

<HARD-GATE>
Run only after explicit invocation.

For a new workflow, require the user to supply Light, Medium, High, or Ultra. If absent, the first response MUST ask for the strength, briefly describe all four levels, and STOP. Never infer, recommend, or auto-select it.

For recovery, require `resume` plus one exact `.msf/plan/*.ai.md` path. Never select the newest plan, infer an active plan, or accept a directory.

If the repository-local MSF baseline is missing, stop and instruct the user to explicitly invoke `/msf-init` before retrying Auto.
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

Claude Code exposes no model inventory, so resolve the Action model only from the values the `Agent` tool's `model` parameter currently accepts (aliases such as `sonnet`, `opus`, `haiku`, `fable`, as listed in that tool's schema in this session). Never treat model names in this skill, a README, memory, or an earlier checkpoint as proof that a model is available.

- If the user did not name an Action model, omit the `model` parameter so the worker uses the host's default subagent model. Record that the model was defaulted.
- If the user named a model, require an exact accepted value after trimming whitespace and lowercasing aliases. Never silently correct, alias, upgrade, downgrade, or substitute it.
- When an exact match fails, report the requested spelling. If conservative typo similarity finds plausible entries, show at most three closest available identifiers and ask the user to confirm one. Otherwise show the accepted values and ask for an exact selection. Set the Auto checkpoint to `waiting_model_selection` and STOP before spawn in either case.

Set `effort` only when the user explicitly asked for a level the tool accepts; otherwise omit it. If an explicit effort is not accepted, report the accepted values and ask the user to choose rather than silently changing it.

Record the accepted-value source and observation time, originally requested model, resolved model (or `default`), resolution status, suggestions, and effort in the Auto checkpoint. User confirmation applies only to that exact resolved value; refresh resolution before any later replacement worker.

## Dispatch the Action worker

Invoking `/msf-auto` is the user's explicit request to use a subagent, and approval of the plan authorizes dispatch. Use Claude Code's `Agent` tool and spawn exactly one fresh worker:

```text
Agent(
  subagent_type = "general-purpose",
  description = "MSF Action <plan-id>",
  model = <resolved model, omitted when defaulted>,
  effort = <explicit supported effort, omitted otherwise>,
  prompt = <bounded Action dispatch>
)
```

A new `Agent` call starts cold with no inherited conversation, which is the required context boundary; never use `subagent_type = "fork"`, which inherits the coordinator's context. Do not use worktree isolation: the worker must share the checkout so the approved `.msf` artifacts and current worktree are visible. The worker runs in the background and its completion arrives as a notification.

The worker prompt must include the repository root, exact `.ai.md` path, Plan ID, Auto checkpoint path, authorization boundaries, and these instructions: this fresh worker is the separate Action session required by `/msf-action`; because the skill is user-invocable only and cannot be loaded through the `Skill` tool, read `msf-action/SKILL.md` from the installed skills directory (`~/.claude/skills/` or the project's `.claude/skills/`) and follow it and its references for that exact plan; the worker cannot ask the user questions, so stop and end its turn with a report at any question, decision, plan deviation, repository conflict, verification failure, external blocker, or completion candidate.

Record the returned agent ID and the model actually requested in the Auto checkpoint. Do not claim a model was used if spawn did not confirm success.

If spawn is rejected for the `model` value (an invalid or unsupported model), treat the earlier resolution as stale: re-read the tool's accepted values, record the exact error, set Auto to `waiting_model_selection`, offer closest current values when useful, ask the user for one exact model, and STOP. This covers a model renamed or removed between preflight and spawn.

If the exact model still exists but is temporarily unavailable, rate-limited, or inaccessible to the signed-in account, distinguish that from a spelling error. Record the exact error and ask whether the user wants to retry that exact model later or select another accepted value. For a missing `Agent` tool or other non-model prerequisites, set Auto to `blocked` and report the concrete prerequisite.

Do not ask the user to copy a command, do not implement inside the coordinator, and do not silently retry with, downgrade to, or substitute any unconfirmed model.

## Supervise without micromanaging

Use the host's native agent controls:

- wait for the completion notification instead of polling a running worker;
- use `SendMessage` to the worker's agent ID to continue it after it stops, whether to answer a question, correct the current work, or assign further approved work (load it with `ToolSearch` if it is deferred);
- use `TaskStop` only to abort a worker that is about to cause a material deviation, then checkpoint before doing anything else.

Each time the worker ends a turn, read its report, the Action checkpoint, and the development log before responding. Send the smallest useful correction. A correction may clarify or restore the approved contract, but must not expand it. If the needed change is material to scope, architecture, behavior, compatibility, security, or data handling, stop the worker, checkpoint the state, return to planning, and obtain new approval.

Do not duplicate the worker's edits or treat silence as failure. Do not blindly restart after failure. A replacement worker is allowed only after reconciling the latest repository and checkpoint state; more than one replacement for the same unresolved condition requires user direction.

## Verify and close

The worker may report a completion candidate; the coordinator owns final acceptance. First inspect the final diff, Action devlog, Action checkpoint, fresh verification evidence, plan coverage, deviations, and unexplained worktree changes.

Then obtain an independent review. Spawn one fresh reviewer with the `Agent` tool (`subagent_type = "general-purpose"`, never `"fork"`, same model resolution as the worker unless the user chose otherwise) whose prompt gives the repository root, exact `.ai.md` path, Plan ID, strength, and these instructions: read `msf-review/SKILL.md` from the installed skills directory and follow it for that exact plan; do not edit anything except the report under `.msf/review/`; do not use computer-use; end with the report path and verdict. The reviewer shares nothing with the worker or the coordinator beyond the `.msf` artifacts and the checkout.

Act on the verdict:

- `accepted`: continue to closure.
- `needs_fixes`: send only the Layer 1 and 2 blocker and major findings back to the same worker with `SendMessage`, then request a fresh review. Allow at most two fix-and-review rounds; afterwards close as `partial` with the remaining findings.
- `blocked`: set Auto to `blocked` and report what prevented judgment.

Layer 3 critique findings never trigger fixes. Report them as follow-up plan candidates for the user to take to `/msf-plan`.

Mark the Auto checkpoint `completed` only when the approved acceptance criteria are satisfied and the latest review verdict is `accepted`. Otherwise close it as `partial` or `blocked` with the exact next action. Report the plan pair, worker model and identity, Action records, review report path and verdict, verification evidence, deviations, risks, and final Auto checkpoint path.

## Resume

For `/msf-auto resume <exact-plan.ai.md>`, load only Auto checkpoints matching both the exact plan path and Plan ID. Reconcile the checkpoint with the Action devlog/checkpoint, live worktree, and `Agent` task state before acting. Resume supervision when the recorded worker is live; otherwise refresh model resolution and spawn a fresh worker from the first incomplete dependency-ready task only after any required user confirmation. Never duplicate a live writer or trust recorded completion without fresh evidence.
