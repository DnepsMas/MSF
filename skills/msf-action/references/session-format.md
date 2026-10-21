# Action session summary (legacy compatibility)

New Action sessions use [handoff-checkpoint.md](handoff-checkpoint.md). Existing session summaries remain valid recovery pointers and must not be rewritten only to adopt the new format.

Name `YYYYMMDD-HHMM-<topic>.md`, adding a numeric suffix on collision.

Include:

- timestamp, mode, named plan path, and run-log path;
- status (`completed`, `partial`, or `blocked`) and a one-sentence outcome;
- first incomplete task or blocker when applicable;
- exact next action;
- durable decisions not already recorded in the development log.

Treat the development log as the execution record. The session summary is a recovery pointer for a fresh agent; do not repeat changed files, completed tasks, or verification details already present in the log.
