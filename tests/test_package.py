from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_all_skills_are_explicit_only_and_default_to_chinese(self) -> None:
        for name in ("msf-init", "msf-plan", "msf-action", "msf-review", "msf-auto"):
            with self.subTest(skill=name):
                self.assertIn("disable-model-invocation: true", self.read(f"skills/{name}/SKILL.md").split("---")[1])
                self.assertFalse((ROOT / "skills" / name / "agents").exists())
                self.assertIn("Reply to the user in Chinese by default", self.read(f"skills/{name}/SKILL.md"))

    def test_plan_keeps_strength_and_session_gates(self) -> None:
        plan = self.read("skills/msf-plan/SKILL.md")
        self.assertIn("<HARD-GATE>", plan)
        for level in ("Light", "Medium", "High", "Ultra"):
            self.assertIn(level, plan)
        self.assertIn("Never transition to implementation in this session", plan)
        self.assertIn("explicit user approval", plan)

    def test_plan_batches_draft_writes_after_requirement_questions(self) -> None:
        plan = self.read("skills/msf-plan/SKILL.md")
        plan_format = self.read("skills/msf-plan/references/plan-format.md")
        self.assertIn("when the current turn no longer needs another user requirement answer", plan)
        self.assertIn("Do not wait for the user to request a file", plan)
        self.assertIn("do not write merely because one question was answered", plan)
        self.assertIn("one consolidated report update per such turn", plan)
        self.assertIn("status `draft`", plan_format)
        self.assertIn("Batch updates at meaningful planning checkpoints", plan_format)
        self.assertIn("Do not create this file for a draft", plan_format)

    def test_plan_handles_missing_baseline_and_draft_completion_explicitly(self) -> None:
        plan = self.read("skills/msf-plan/SKILL.md")
        self.assertIn("explicitly invoke `/msf-init`", plan)
        self.assertIn("When still draft or blocked", plan)

    def test_action_requires_named_plan_and_evidence(self) -> None:
        action = self.read("skills/msf-action/SKILL.md")
        self.assertIn("Never select the newest plan", action)
        self.assertIn("Plan and Action must be separate sessions", action)
        self.assertIn("fresh evidence", action)
        self.assertIn("development log and Action checkpoint once the plan identity", action)
        self.assertIn("before the first production mutation", action)

    def test_action_summary_is_a_pointer_and_debugging_does_not_wait_arbitrarily(self) -> None:
        session_format = self.read("skills/msf-action/references/session-format.md")
        debugging = self.read("skills/msf-action/references/debugging.md")
        self.assertIn("Treat the development log as the execution record", session_format)
        self.assertIn("do not repeat changed files", session_format)
        self.assertIn("stop speculative patching", debugging)
        self.assertIn("Ask the user only when progress requires", debugging)

    def test_action_persists_and_resumes_context_checkpoints(self) -> None:
        action = self.read("skills/msf-action/SKILL.md")
        checkpoint = self.read("skills/msf-action/references/handoff-checkpoint.md")
        protocol = self.read("skills/msf-action/references/execution-protocol.md")
        self.assertIn("before the first production mutation", action)
        self.assertIn("The `.msf` records, not chat history", action)
        self.assertIn("model/session switch", action)
        self.assertIn("Attempt ID", checkpoint)
        self.assertIn("Plan ID", checkpoint)
        self.assertIn("Never infer the plan from the newest checkpoint", checkpoint)
        self.assertIn("unverified", checkpoint.lower())
        self.assertIn("exact plan path and plan ID", protocol)

    def test_auto_dispatches_and_supervises_a_fresh_action_worker(self) -> None:
        auto = self.read("skills/msf-auto/SKILL.md")
        checkpoint = self.read("skills/msf-auto/references/coordination-checkpoint.md")
        for level in ("Light", "Medium", "High", "Ultra"):
            self.assertIn(level, auto)
        self.assertIn("Agent(", auto)
        self.assertIn("never use `subagent_type = \"fork\"`", auto)
        self.assertIn("separate Action session required by `/msf-action`", auto)
        self.assertIn("must not start a second writer", auto)
        self.assertIn("must not expand it", auto)
        self.assertIn("completion candidate", auto)
        self.assertIn("Do not ask the user to copy a command", auto)
        self.assertIn("/msf-auto resume <exact-plan.ai.md>", auto)
        self.assertIn("Mode: auto", checkpoint)
        self.assertIn("Worker identity", checkpoint)
        self.assertIn("Spawn result", checkpoint)

    def test_auto_resolves_models_and_reports_typos_before_spawn(self) -> None:
        auto = self.read("skills/msf-auto/SKILL.md")
        checkpoint = self.read("skills/msf-auto/references/coordination-checkpoint.md")
        self.assertIn("exposes no model inventory", auto)
        self.assertIn("omit the `model` parameter", auto)
        self.assertIn("Never silently correct", auto)
        self.assertIn("at most three closest available identifiers", auto)
        self.assertIn("STOP before spawn", auto)
        self.assertIn("renamed or removed between preflight and spawn", auto)
        self.assertIn("retry that exact model later", auto)
        self.assertIn("waiting_model_selection", checkpoint)
        self.assertIn("Model originally requested", checkpoint)
        self.assertIn("Model resolved", checkpoint)
        self.assertIn("Suggested identifiers", checkpoint)

    def test_review_is_independent_evidence_based_and_never_auto_fixes_critique(self) -> None:
        review = self.read("skills/msf-review/SKILL.md")
        layers = self.read("skills/msf-review/references/review-layers.md")
        auto = self.read("skills/msf-auto/SKILL.md")
        verification = self.read("skills/msf-action/references/verification.md")
        self.assertIn("Never select the newest plan", review)
        self.assertIn("did not write the code", review)
        self.assertIn("Do not use computer-use", review)
        self.assertIn("Write only the review report under `.msf/review/`", review)
        for verdict in ("accepted", "needs_fixes", "blocked"):
            self.assertIn(verdict, review)
        self.assertIn("at most 10 findings", layers)
        self.assertIn("Never turn a critique finding into an edit", layers)
        self.assertIn("unverified", layers)
        self.assertIn("msf-review/SKILL.md", auto)
        self.assertIn("at most two fix-and-review rounds", auto)
        self.assertIn("Layer 3 critique findings never trigger fixes", auto)
        self.assertIn("Do not use computer-use", verification)

    def test_local_markdown_references_exist(self) -> None:
        for name in ("msf-init", "msf-plan", "msf-action", "msf-review", "msf-auto"):
            folder = ROOT / "skills" / name
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            for reference in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" not in reference and not reference.startswith("#"):
                    with self.subTest(skill=name, reference=reference):
                        self.assertTrue((folder / reference).exists())


if __name__ == "__main__":
    unittest.main()
