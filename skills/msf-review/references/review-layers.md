# Review layers

Strength controls how many layers run, not how carefully each one runs.

## Layer 1: Conformance

Question: does the result satisfy the approved plan?

- Build a table of every acceptance criterion and task with the evidence you observed: command, exit status, and meaningful output, or the file and line that proves it.
- Re-run the checks that decide pass or fail instead of trusting recorded results.
- A criterion with no fresh evidence is `unverified`, never `passed`. Never translate "not run" or "probably" into "passed".
- Compare the final diff with the approved scope. Report unplanned changes and untouched planned targets.

## Layer 2: Defects

Question: is this change wrong or fragile?

- Check logic errors, boundary and error handling, regressions in neighboring flows, compatibility, security, and data handling.
- Check that tests would fail if the behavior broke; flag tests that only assert implementation details or always pass.
- Check consistency with local conventions and repository instructions.
- Limit this layer to the diff and the code it directly affects.

## Layer 3: Critique

Question: what are the project's most valuable weaknesses relative to its goals?

- Judge against the plan's goals and the repository's own standards, not personal taste.
- Report at most 10 findings, ranked by value. Prefer a few well-evidenced findings to a long list.
- Discard any finding that lacks a concrete file, line, or command output, or that restates a Layer 1 or 2 finding.
- Do not propose rewrites for style. Propose changes only where they reduce a demonstrated risk or cost.
- Never turn a critique finding into an edit. Each becomes a follow-up candidate.

## Severity

- `blocker`: violates an acceptance criterion, breaks behavior, or creates a security or data risk.
- `major`: likely to cause defects or significant maintenance cost.
- `minor`: small, local, low-risk improvement.

Layer 1 and 2 findings of `blocker` or `major` severity yield `needs_fixes`. Open questions that prevent judging the result yield `blocked`.
