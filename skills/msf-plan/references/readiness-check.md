# Plan readiness check

Before asking for final approval, verify:

- **Need:** goal, users, current behavior, desired behavior, and non-goals are unambiguous.
- **Evidence:** material repository claims point to inspected files, symbols, commands, or user decisions.
- **Coverage:** every accepted requirement maps to at least one task and one acceptance check.
- **Boundaries:** affected components, interfaces, data flow, and ownership are clear at the selected strength.
- **Failure behavior:** relevant invalid input, partial failure, retries, cleanup, and recovery are specified.
- **Compatibility:** public APIs, stored data, configuration, deployment, and migration impacts are addressed where applicable.
- **Verification:** each task has a useful check, and final checks prove the overall acceptance criteria.
- **Feasibility:** commands, paths, APIs, and symbols are confirmed or explicitly marked as assumptions to verify before editing.
- **Consistency:** the design, task order, tests, risks, rollout, and acceptance criteria do not contradict one another.
- **Scope:** no unrelated refactor or speculative capability has entered the plan.

An approved plan may contain documented low-risk assumptions with an Action preflight check. It must not contain unresolved decisions that could materially change behavior, architecture, scope, or safety.
