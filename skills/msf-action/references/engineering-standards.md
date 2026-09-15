# Engineering standards

Repository instructions take precedence. Apply these defaults proportionately.

## Correctness and scope

- Implement the approved behavior completely with the smallest coherent change.
- Preserve unrelated user changes and avoid opportunistic refactors.
- Reuse established patterns and abstractions before adding new ones.
- Do not invent APIs, schemas, commands, expected results, or project conventions.
- Preserve backward compatibility unless the plan explicitly changes it.

## Design quality

- Keep responsibilities, module boundaries, and interfaces clear.
- Prefer readable, unsurprising code over clever compression or speculative flexibility.
- Add dependencies only when justified and existing facilities are insufficient.
- Comment intent, invariants, and non-obvious tradeoffs—not syntax.
- Update affected documentation, configuration, examples, or generated artifacts when required for a complete change.

## Safety and data

- Validate at trust boundaries and handle expected failures explicitly.
- Do not expose credentials, secrets, personal data, or sensitive payloads in code, logs, tests, or MSF records.
- For authentication, authorization, external input, file access, network calls, or persistence, inspect abuse and failure paths.
- For schema or persistent-data changes, define migration, compatibility, partial-failure, and recovery behavior before mutation.
- Avoid destructive operations unless the plan and user authority clearly cover them; verify exact targets first.

## Testing

- Test observable behavior rather than implementation trivia.
- Prefer a regression test for fixed defects and test-first for new behavior when practical.
- Cover important success, boundary, and failure paths at the lowest useful level.
- Use mocks only where real dependencies are impractical; do not make mock interactions the sole proof of behavior.
- Keep test changes honest: do not weaken assertions merely to make implementation pass.

## Change hygiene

- Follow formatter, linter, type, naming, and layout conventions already present.
- Avoid debug artifacts, dead code, broad generated diffs, and unrelated dependency churn.
- Review the final diff for accidental edits, scope creep, compatibility breaks, and missing tests or documentation.
