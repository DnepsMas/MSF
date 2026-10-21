# MSF workspace

- `plan/` retains dated approved plans; the user names the plan to execute.
- `devlog/` records implemented changes and verification.
- `review/` holds independent `/msf-review` reports.
- `memory/project.md` stores durable project knowledge.
- `memory/sessions/` stores compact cross-session handoffs. `/msf-action` updates execution checkpoints, while `/msf-auto` records coordinator and Action worker identity/state so supervision can resume without chat history.

Do not store secrets, credentials, or large raw outputs here.
