# Execution protocol

## Plan preflight

Reject or return to Plan when the named file is absent, outside `.msf/plan`, unapproved, missing its human pair, internally contradictory, or lacks enough information to start safely.

Check:

- plan ID, approval metadata, objective, non-goals, constraints, tasks, and acceptance criteria;
- requirement-to-task and task-to-verification coverage;
- dependency order and stop conditions;
- current repository instructions and dirty state;
- referenced paths, symbols, APIs, tools, and commands;
- changes since the plan's evidence was gathered.

Classify findings:

- **Compatible detail:** decide locally, record if non-obvious, continue.
- **Minor deviation:** still satisfies the contract; record reason and continue.
- **Material deviation:** changes contract, architecture, public behavior, compatibility, security, data, or meaningful scope; stop and return to Plan.
- **External blocker:** permission, credential, unavailable service, environment, or dependency prevents progress; record evidence and request the smallest needed action.

## Task loop

For each ready task:

1. Re-read its purpose, targets, constraints, edge cases, and completion evidence.
2. Mark it `in_progress` in the development log.
3. Establish baseline or failing evidence when applicable.
4. Make the smallest complete implementation for that task.
5. Run focused verification; diagnose failures rather than patching blindly.
6. Review the task diff for scope and contract compliance.
7. Mark `completed`, `partial`, or `blocked` with evidence.

Do not require commits, worktrees, TDD, subagents, or code-review agents universally. Use them when the repository requires them, the user asks, or task risk makes them materially useful.

## Resume

When resuming an incomplete Action session, read the named plan plus the latest development log for that plan. Independently verify repository state before trusting recorded task status. Continue from the first incomplete dependency-ready task; do not repeat completed work without cause.
