---
name: msf-init
description: Initialize or repair the lightweight repository-local MSF workspace used by explicit MSF Plan and Action sessions. Use only when the user explicitly invokes MSF initialization.
---

# MSF Init

Create a small, version-controlled project context that later sessions can trust.

## Communication

Reply to the user in Chinese by default. Switch only when explicitly requested. Preserve code, commands, paths, identifiers, and quoted text in their necessary original form.

## Scope

Resolve the root from the current Git worktree, otherwise the active workspace. Ask only if multiple roots remain plausible. Read repository instructions before writing.

Create or repair only this baseline from [assets/workspace](assets/workspace):

```text
.msf/
├── README.md
├── plan/
├── devlog/
└── memory/
    ├── project.md
    └── sessions/
```

Preserve all existing content. Never overwrite populated memory or MSF records with templates. Do not edit business files, dependencies, Git history, or unrelated configuration.

## Establish project context

Inspect only enough repository evidence to record durable facts in `.msf/memory/project.md`:

- project purpose when documented;
- languages, frameworks, and package/build systems;
- important module boundaries and entry points;
- repository-local instructions and durable constraints;
- commands confirmed from scripts, manifests, CI, or documentation;
- known test, lint, build, and formatting conventions.

Distinguish confirmed facts from unknowns. Do not run expensive setup or invent architecture. If `project.md` already exists, merge newly confirmed facts narrowly and retain user-authored decisions.

## Version-control invariant

`.msf/` is project knowledge and must remain eligible for version control. If an existing ignore rule excludes it, report the exact rule and remediation; do not silently change the user's ignore policy.

## Verify and report

Confirm the three directories, project memory, and session directory exist. Report created, preserved, updated, unknown, and conflicting items. If Init was a prerequisite invoked within another MSF workflow, return control to that workflow after verification.
