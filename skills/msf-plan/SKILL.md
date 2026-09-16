---
name: msf-plan
description: Run an explicit, strength-scaled MSF planning session that investigates the repository, resolves requirements, obtains approval, and persists a dated human/agent plan pair without implementing code.
---

# MSF Plan

Turn a request into an approved, implementation-ready contract. Plan and Action are always separate sessions.

## Communication

Reply to the user in Chinese by default. Switch only when explicitly requested. Preserve code, commands, paths, identifiers, and quoted text in their necessary original form.

<HARD-GATE>
Before repository inspection, analysis, or file writes, check whether the user explicitly supplied Light, Medium, High, or Ultra in the current request.

If absent, the first response MUST ask for the strength, briefly describe all four levels, and STOP. Never infer, recommend, or auto-select it. Prefer a native structured-choice tool exposed by the host, including Codex `request_user_input` or Claude Code's equivalent. Show all four options when supported. When limited to three plus `Other`, show Light, Medium, High and tell the user to enter Ultra via `Other`. Fall back to plain text when no such tool exists.
</HARD-GATE>

## Non-implementation boundary

- Read repository files needed for planning.
- Write only under `.msf/plan/` and `.msf/memory/`.
- Do not modify code, tests, configuration, dependencies, external documentation, or Git state.
- Do not scaffold, prototype, or begin implementation.
- If the MSF baseline is missing, stop before planning writes and instruct the user to explicitly invoke `$msf-init`; resume Plan afterward.

## Load context deliberately

Read, in order: repository instructions; `.msf/memory/project.md`; recent session summaries relevant to this request; plans explicitly named by the user; then affected code, tests, manifests, and history. Do not bulk-read all memory or assume the newest plan is active.

## Scale the work

Read [references/planning-levels.md](references/planning-levels.md) and apply the chosen level. Depth scales; correctness gates do not. Every level needs a clear goal, bounded scope, repository evidence, acceptance criteria, verification approach, and approval.

## Planning loop

1. **Frame** — restate the problem, desired outcome, constraints, non-goals, and observable success.
2. **Investigate** — trace the affected flow and find analogous working patterns. Label confirmed evidence, user decisions, and assumptions separately.
3. **Clarify** — ask only consequential questions, one at a time. Prefer native choice UI when available. Do not ask the user to decide implementation details that repository evidence can settle.
4. **Open the working report** — when requirement clarification is sufficient, create or update the dated human plan according to **Persist at planning checkpoints** below. Do not wait for the user to request a file.
5. **Design** — present viable approaches when a meaningful tradeoff exists, leading with a recommendation. Keep YAGNI pressure: every component must serve an accepted requirement.
6. **Decompose** — map requirements to coherent implementation tasks, dependencies, affected files or symbols, and task-level verification. Avoid both vague phases and mechanical micro-steps.
7. **Check readiness** — use [references/readiness-check.md](references/readiness-check.md). Fix contradictions and missing coverage before approval.
8. **Approve** — present the proposed design and execution outline in chat. Obtain explicit user approval. Silence is not approval.
9. **Finalize** — update the same human report to status `approved`, add the approval record, and create its paired `.ai.md` execution plan. Never overwrite an unrelated plan.
10. **Remember** — write or finalize the compact session summary using [references/session-format.md](references/session-format.md) and update project memory only with durable facts or decisions.

## Persist at planning checkpoints

The working report is part of planning, but file writes must not interrupt requirement discovery. If the next response needs a user answer, ask the question promptly and keep accumulated discussion in the active context; do not write merely because one question was answered.

Write in batches when the current turn no longer needs another user requirement answer. Useful checkpoints are: clarification is sufficient for autonomous design, a coherent design section is settled, readiness review is complete, approval changes plan status, or the user pauses or ends planning. Normally make one consolidated report update per such turn, not one write per finding or decision. Do not duplicate the transcript.

If the session ends without approval, retain the human report with status `draft`, record unresolved items and the exact next step, and write a session summary. Do not create the `.ai.md` execution plan until approval.

When approved, finish by reporting both exact plan paths and instructing the user to start a new session, explicitly invoke `$msf-action`, and name the `.ai.md` plan. When still draft or blocked, report the human-plan path, unresolved items, and exact next planning step. Never transition to implementation in this session.
