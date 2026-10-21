---
name: msf-review
description: Independently review the result of one explicitly named MSF agent plan in a fresh session, covering plan conformance, defects, and strength-scaled critique, and write an evidence-backed report without editing the project.
disable-model-invocation: true
---

# MSF Review

Judge a finished Action attempt from the plan and the evidence, not from the author's account. The reviewer never writes the implementation and never expands the approved contract.

## Communication

Reply to the user in Chinese by default. Switch only when explicitly requested. Preserve code, commands, paths, identifiers, and quoted text in their necessary original form.

<HARD-GATE>
Run only after explicit invocation and require the user to name one `.msf/plan/*.ai.md` file. Never select the newest plan, infer an active plan, or accept a directory as the target.

Review must run in a context that did not write the code. If this session planned or executed the named plan, stop and instruct the user to start a new session, or to let `/msf-auto` dispatch a fresh reviewer.
</HARD-GATE>

## Boundary

- Write only the review report under `.msf/review/`.
- Do not modify code, tests, configuration, dependencies, the plan pair, Action records, or Git state.
- Do not use computer-use or desktop control. Gather evidence from files, the Git diff, and commands run in the shell. A browser may be used only when the plan's acceptance criteria require observing a web UI, and only as supplementary evidence.
- Run only read-only or already-planned verification commands. Anything destructive, networked, or credentialed is out of bounds.

## Load narrowly

Read the agent plan, its linked human plan, the Action development log and checkpoint that reference this exact plan, repository instructions, and project memory. Then read the actual diff and the files it touches. Treat the development log and any worker report as claims to check, never as evidence.

## Choose the layers

Take the strength recorded in the plan unless the user explicitly overrides it. Apply [references/review-layers.md](references/review-layers.md):

- Light: Layer 1.
- Medium: Layers 1 and 2.
- High and Ultra: Layers 1, 2, and 3.

## Run the review

1. **Conformance** — map every acceptance criterion and planned task to fresh evidence you observed yourself. Re-run the verification commands that decide pass or fail.
2. **Defects** — review the diff for bugs, regressions, missing error handling, security and data-handling problems, and tests that do not test the claimed behavior.
3. **Critique** — only at High and Ultra, name the project's most valuable weaknesses relative to the plan's goals and the repository's own standards.

Every finding needs evidence and a severity, and must follow the cap and discard rules in the layers reference. Discard impressions you cannot ground in a file, line, or command output.

## Report

Write the report using [references/review-format.md](references/review-format.md) to `.msf/review/YYYY-MM-DD-<plan-topic>-review.md` (append `-02`, `-03` on collision). Conclude with exactly one verdict: `accepted`, `needs_fixes`, or `blocked`.

Finish by reporting the verdict, the report path, the blocking findings, and the follow-up candidates. Findings in Layers 1 and 2 may be fixed within the approved contract by the same Action worker. Layer 3 findings are never fixed automatically: they become follow-up plan candidates for the user to take to `/msf-plan`.
