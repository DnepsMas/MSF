# Review report

```text
.msf/review/YYYY-MM-DD-<plan-topic>-review.md
```

```markdown
# Review: <plan title>

## Identity
- Plan path / plan ID:
- Strength reviewed at: Light | Medium | High | Ultra
- Layers run:
- Reviewed against: <commit or worktree state>
- Verdict: accepted | needs_fixes | blocked

## Conformance
| Criterion or task | Status (passed / failed / unverified) | Evidence |

## Findings
| ID | Layer | Severity | Location | Finding | Evidence |

## Verification run by the reviewer
- Exact command / exit status / meaningful result

## Follow-up candidates
- Layer 3 findings worth a new plan, one line each with the value gained

## Open questions
- What prevented judging, if the verdict is blocked
```

Keep it compact. Do not paste transcripts, hidden reasoning, full diffs, secrets, or large command output. The plan is the contract; this report never amends it.
