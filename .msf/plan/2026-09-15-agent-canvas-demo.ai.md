# Agent Canvas Demo — Agent Execution Plan

## Metadata

- Plan ID: `2026-09-15-agent-canvas-demo`
- Status: `approved`
- Strength: Light
- Date: 2026-09-15

## Objective

Create a zero-dependency, single-page animated concept demo at `demo/agent-canvas/index.html`. It must communicate a ComfyUI-like agent orchestration product in which contextual nodes connect to an Agent, which then invokes a Subagent.

## Constraints

- Work only from this approved plan in a separate MSF Action session.
- Do not add packages, a build system, network dependencies, or credentials.
- Do not modify `scripts/`, `skills/`, `tests/`, or the root `README.md`.
- Keep HTML, CSS, JavaScript, icons, and effects local to one file unless a small `demo/agent-canvas/README.md` is strictly needed for launch instructions.
- Do not implement real model, terminal, browser, session, persistence, or orchestration backends.
- Preserve current repository behavior and tests.

## Assumptions

- The target is a desktop-first product concept animation, not a production editor.
- Modern desktop browser support is sufficient.
- Visual details may be refined within the approved dark professional workbench direction.

## Ordered tasks

1. Create `demo/agent-canvas/index.html`.
   - Add semantic regions for toolbar, viewport, world/canvas, SVG edge layer, nodes, inspector/status UI, and replay control.
   - Completion check: the file opens directly and shows a coherent static layout without external resources.

2. Implement the visual system.
   - Add a dark infinite-grid appearance, translucent panels, legible typography, node ports, status badges, focus states, and distinct accents for Memory, Skill, Prompt, Terminal, Browser, Session, Model API, Agent, and Subagent.
   - Completion check: all nine roles are visually distinguishable and Agent is the primary focal point.

3. Define demo graph data and rendering.
   - Represent nodes, positions, types, labels, summaries, status, and edges in JavaScript data.
   - Render nodes and SVG Bezier paths from that data without inventing backend schemas.
   - Completion check: every approved context node has a visible path into Agent, and Agent has a visible path to Subagent.

4. Implement canvas and node interaction.
   - Support background drag to pan, wheel zoom around the pointer, node drag, node selection, and connection redraw after geometry changes.
   - Separate node-drag and canvas-pan pointer flows and manage pointer capture safely.
   - Completion check: moving nodes and transforming the canvas keep all edge endpoints aligned.

5. Implement the replayable story animation.
   - Reveal the workspace and nodes in sequence.
   - Activate incoming edges one by one with restrained traveling highlights or particles.
   - Transition Agent from idle to running, activate the Agent-to-Subagent edge, then show completion.
   - Reset timers, classes, statuses, and particles before every replay.
   - Completion check: replay works repeatedly without duplicated timers, stuck states, or accumulating visual artifacts.

6. Add resilience and accessibility.
   - Respect `prefers-reduced-motion` with a stable end state or minimal transitions.
   - Ensure controls are keyboard focusable and expose useful labels.
   - Keep core graph and controls usable in a narrower desktop viewport.
   - Completion check: reduced-motion mode and keyboard focus remain clear.

7. Verify the result.
   - Open the file in a browser and inspect the initial state, full animation, replay, dragging, panning, zooming, selection, responsive behavior, and console.
   - Run the existing repository checks below.
   - Completion check: every acceptance criterion passes and existing checks remain green.

## Required tests and commands

- Manual browser verification of `demo/agent-canvas/index.html` with network unavailable.
- Manual browser console check for blocking errors.
- `python -m unittest discover -s tests -v`
- `python scripts/validate.py`

## Acceptance criteria

- Directly opening the HTML file produces the complete demo without installation or network access.
- The graph clearly communicates multiple context sources feeding Agent and Agent invoking Subagent.
- Memory, Skill, Prompt, Terminal, Browser, Session, Model API, Agent, and Subagent are all represented.
- Animation completes and can be replayed reliably.
- Node dragging, canvas panning, pointer-centered zoom, node selection, and dynamic edge alignment work.
- Reduced-motion behavior provides a readable stable experience.
- No secrets, real API calls, external assets, or package dependencies are introduced.
- Existing MSF unit tests and validation pass.

## Non-goals

- Production workflow execution.
- Real context synchronization.
- Arbitrary graph editing or node creation.
- Authentication, persistence, collaboration, or API configuration.
- Mobile-first support.

## Risks

- Coordinate drift between DOM nodes and SVG edges: use one canvas coordinate model and redraw after interaction or viewport changes.
- Pointer gesture conflicts: gate behavior by event target and pointer state.
- Replay leaks: centralize timer and transient-element cleanup.
- Excessive animation cost: cap particles and favor transforms/opacity.

## Stop conditions

- Stop if implementation requires modifying existing MSF skill or Python tooling beyond adding the isolated demo.
- Stop if a real external service, credential, dependency installation, or backend becomes necessary.
- Stop and ask the user if the requested result changes from a concept demo into a functional orchestration product.
