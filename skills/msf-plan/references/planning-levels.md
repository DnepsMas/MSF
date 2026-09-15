# Planning strength

Strength controls investigation and design depth, not response verbosity or quality standards.

## Light

For a narrow fix or localized adjustment with an existing flow to inspect.

- Confirm the symptom or desired delta, affected location, non-goals, regression risk, and focused verification.
- One approach is sufficient unless evidence reveals a real tradeoff.
- Produce a short plan with one or a few coherent tasks.

## Medium

For an ordinary feature, module change, integration adjustment, or local refactor.

- Trace the relevant flow and neighboring interfaces.
- Cover behavior, error handling, compatibility, tests, and affected documentation or configuration.
- Compare alternatives when they materially differ.
- Define dependencies and task-level completion checks.

## High

For a new module, substantial feature, cross-component behavior, public interface, or meaningful migration.

- Analyze architecture, data flow, interfaces, failure modes, security, compatibility, rollout, and recovery where relevant.
- Compare 2–3 credible approaches with tradeoffs.
- Make module boundaries and ownership explicit.
- Include integration verification and operational risks.

## Ultra

For a new product/system, infrastructure foundation, framework decision, or large restructuring.

- First decide whether the request must be decomposed into independently deliverable plans.
- Cover long-term boundaries, non-functional requirements, technology choices, migration stages, observability, rollback, security, data lifecycle, and evolution.
- Identify decision points and irreversible choices explicitly.
- Each resulting plan must still yield a coherent, testable increment; do not create a single giant execution document.

## Ratchet

If investigation exposes materially greater coupling or risk, explain why the selected strength is insufficient and ask the user whether to raise it. Never silently downgrade or upgrade the user's choice.
