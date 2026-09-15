# Verification and completion

Evidence must be fresh and observed in the current Action session.

## Verification ladder

Run what applies, in this order:

1. reproduction or baseline evidence;
2. task-focused tests or checks;
3. affected module/package checks;
4. broader regression suite, build, lint, typecheck, or integration checks proportional to risk;
5. acceptance-criteria walkthrough;
6. final diff and repository-status review.

For each command, record the exact command, exit status, meaningful result, and any skipped scope. Distinguish change-caused failures from confirmed pre-existing or environmental failures; neither may be silently ignored.

## Completion decision

Mark `completed` only when:

- every planned task is completed or explicitly removed by an approved plan revision;
- every acceptance criterion has evidence;
- relevant regression checks pass;
- the final diff matches the approved scope;
- no material blocker or unexplained failure remains.

Otherwise use `partial` or `blocked`, state exactly what remains, and leave a resumable development log. Never translate “not run,” “unavailable,” or “probably” into “passed.”
