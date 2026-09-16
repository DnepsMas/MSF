# Working report and approved plan pair

After the first useful investigation, create the human report automatically:

```text
.msf/plan/YYYY-MM-DD-<short-topic>.md
```

It begins with status `draft` and is updated throughout discussion. After explicit approval, change the same report to `approved` and create:

```text
.msf/plan/YYYY-MM-DD-<short-topic>.ai.md
```

Use a short lowercase hyphenated topic. On collision append `-02`, `-03`, and so on. Never overwrite an unrelated plan, rename one as “current,” or infer that the newest plan is active. Once approved, both files share the same plan ID, approval timestamp, strength, and approved status.

## Human plan (`.md`)

Default to Chinese unless the user requested another language. While draft, keep unresolved items explicit and maintain a `Last updated` value. Use only applicable sections:

1. Metadata and status
2. Goal, background, requirements, non-goals
3. Repository findings and constraints
4. Chosen design and rejected alternatives
5. Components, interfaces, data/error flow
6. Impacted areas and migration/rollout where relevant
7. Implementation outline
8. Verification strategy and acceptance criteria
9. Risks, mitigations, assumptions, and stop conditions
10. Open questions and next planning step while draft
11. Approval record when approved

## Agent plan (`.ai.md`, approval only)

Optimize for precise execution rather than narration:

```markdown
# <Title> — Agent Execution Plan

## Contract
- Plan ID / status / strength / approved at
- Human plan path
- Objective
- Non-goals
- Global constraints
- Material assumptions to verify before edits

## Requirement coverage
| Requirement | Task(s) | Acceptance evidence |

## Task graph
### T1 — <coherent deliverable>
- Depends on: none | Tn
- Purpose:
- Targets: confirmed repository-relative files/symbols, or discovery rule
- Changes:
- Edge/failure cases:
- Verification:
- Completion evidence:
- Stop conditions:

## Final verification
- Focused checks
- Broader regression checks
- Acceptance walkthrough
- Diff/review checks

## Risks and recovery
```

Do not create this file for a draft or unapproved report. Tasks are independently reviewable units with their own verification, not arbitrary 2-minute fragments. Use exact paths and symbols only when confirmed. If discovery is necessarily deferred, state how Action will resolve it and when it must stop. Do not invent APIs, schemas, commands, expected outputs, or test names. Do not include unresolved material decisions or placeholder instructions such as “handle errors appropriately.”
