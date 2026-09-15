# Evidence-first debugging

Use for bugs, failing tests, regressions, performance anomalies, and unexpected behavior.

1. **Reproduce and localize** — capture the exact symptom, reliable reproduction, error output, recent changes, and the boundary where correct state becomes incorrect.
2. **Compare patterns** — find a similar working path in the same repository and enumerate relevant differences.
3. **Form one hypothesis** — state a specific root cause and the evidence that predicts it.
4. **Test minimally** — vary one thing or add focused instrumentation. Do not combine speculative fixes.
5. **Protect behavior** — when practical, add a regression test that fails for the expected reason before the production fix.
6. **Fix the source** — make the smallest change that addresses the confirmed cause, then run focused and regression checks.

If a hypothesis fails, return to evidence with the new observation. After three failed fix hypotheses, stop and reassess the architecture or assumptions with the user; do not add a fourth speculative patch. If the cause is external or timing-dependent, document the investigation and add proportionate handling or observability rather than pretending certainty.
