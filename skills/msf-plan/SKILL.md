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
- Invoke `msf-init` if the MSF baseline is missing, then remain in Plan mode.

## Load context deliberately

Read, in order: repository instructions; `.msf/memory/project.md`; recent session summaries relevant to this request; plans explicitly named by the user; then affected code, tests, manifests, and history. Do not bulk-read all memory or assume the newest plan is active.

## Scale the work

Read [references/planning-levels.md](references/planning-levels.md) and apply the chosen level. Depth scales; correctness gates do not. Every level needs a clear goal, bounded scope, repository evidence, acceptance criteria, verification approach, and approval.

## Planning loop

1. **Frame** — restate the problem, desired outcome, constraints, non-goals, and observable success.
2. **Investigate** — trace the affected flow and find analogous working patterns. Label confirmed evidence, user decisions, and assumptions separately.
3. **Clarify** — ask only consequential questions, one at a time. Prefer native choice UI when available. Do not ask the user to decide implementation details that repository evidence can settle.
4. **Design** — present viable approaches when a meaningful tradeoff exists, leading with a recommendation. Keep YAGNI pressure: every component must serve an accepted requirement.
5. **Decompose** — map requirements to coherent implementation tasks, dependencies, affected files or symbols, and task-level verification. Avoid both vague phases and mechanical micro-steps.
6. **Check readiness** — use [references/readiness-check.md](references/readiness-check.md). Fix contradictions and missing coverage before approval.
7. **Approve** — present the proposed design and execution outline in chat. Obtain explicit user approval. Silence is not approval.
8. **Persist** — only after approval, create the dated pair defined in [references/plan-format.md](references/plan-format.md). Never overwrite an existing plan.
9. **Remember** — write a compact summary using [references/session-format.md](references/session-format.md) and update project memory only with durable facts or decisions.

Keep drafts in the active session. If approval is not reached, do not create plan files; still preserve a session summary when meaningful findings or decisions must survive.

Finish by reporting both exact plan paths and instructing the user to start a new session, explicitly invoke `$msf-action`, and name the `.ai.md` plan. Never transition to implementation in this session.
