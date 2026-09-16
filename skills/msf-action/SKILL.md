---
name: msf-action
description: Execute one explicitly named, approved MSF agent plan in a fresh implementation session using preflight review, task checkpoints, evidence-based verification, and durable recovery records.
---

# MSF Action

Implement one approved plan with disciplined engineering and recoverable progress. This session never creates or substantially redesigns the plan.

## Communication

Reply to the user in Chinese by default. Switch only when explicitly requested. Preserve code, commands, paths, identifiers, and quoted text in their necessary original form.

<HARD-GATE>
Run only after explicit invocation and require the user to name one `.msf/plan/*.ai.md` file. Never select the newest plan, infer an active plan, or accept a directory as the target.

Plan and Action must be separate sessions. If the plan was produced earlier in this same session, stop and instruct the user to start a new session.
</HARD-GATE>

## Load narrowly

Resolve the named path within the repository. Read the agent plan, its linked human plan, repository instructions, project memory, and only relevant recent session summaries. Do not bulk-load every historical record.

## Preflight before edits

Use [references/execution-protocol.md](references/execution-protocol.md) to:

1. confirm the plan is approved, paired, internally consistent, and free of material unresolved decisions;
2. inspect repository state, affected flows, local conventions, user changes, and required tools;
3. verify that task targets and commands still exist or can be resolved by the plan's discovery rules;
4. map tasks to acceptance evidence and identify repository drift.

Fixing wording or resolving a low-risk implementation detail is allowed. If drift or a gap would materially alter scope, architecture, behavior, compatibility, security, or data handling, write a blocked session summary and return the work to a new Plan session. Do not silently redesign.

## Execute task by task

- Follow the plan's dependency order and keep one coherent task in progress at a time.
- Before production changes, choose a verification strategy appropriate to the change. Prefer a failing behavioral test for bugs and behavior changes when practical; document why when test-first is not suitable.
- For defects or unexplained failures, use [references/debugging.md](references/debugging.md). Establish evidence and a root-cause hypothesis before changing production behavior.
- Apply [references/engineering-standards.md](references/engineering-standards.md) without overriding stricter repository rules.
- After each task, run its focused verification and update the development log checkpoint. Do not stack speculative fixes.
- Minor deviations are allowed only when they preserve the approved contract; record them with reasons.

Create the development log at the first mutation and keep it current using [references/devlog-format.md](references/devlog-format.md). This is the recovery point if the session ends early. Do not edit the approved plan merely to mark progress.

## Completion gate

Use [references/verification.md](references/verification.md). Completion requires fresh evidence for task checks, relevant regression checks, every acceptance criterion, and a final diff review. A passing narrow test does not prove the whole plan.

## Close every meaningful session

Whether completed, partial, or blocked:

1. finalize the development log if any mutation or execution attempt occurred;
2. write a compact recovery-pointer summary using [references/session-format.md](references/session-format.md);
3. update project memory only with durable facts, commands, constraints, or decisions;
4. report status, changed files, verification evidence, deviations, risks, and exact MSF record paths.

Never claim completion, correctness, or passing checks without fresh evidence from the current session.
