from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_all_skills_are_explicit_only_and_default_to_chinese(self) -> None:
        for name in ("msf-init", "msf-plan", "msf-action"):
            with self.subTest(skill=name):
                self.assertIn("allow_implicit_invocation: false", self.read(f"skills/{name}/agents/openai.yaml"))
                self.assertIn("Reply to the user in Chinese by default", self.read(f"skills/{name}/SKILL.md"))

    def test_plan_keeps_strength_and_session_gates(self) -> None:
        plan = self.read("skills/msf-plan/SKILL.md")
        self.assertIn("<HARD-GATE>", plan)
        for level in ("Light", "Medium", "High", "Ultra"):
            self.assertIn(level, plan)
        self.assertIn("Never transition to implementation in this session", plan)
        self.assertIn("explicit user approval", plan)

    def test_plan_persists_a_live_report_before_approval(self) -> None:
        plan = self.read("skills/msf-plan/SKILL.md")
        plan_format = self.read("skills/msf-plan/references/plan-format.md")
        self.assertIn("immediately create the dated human plan", plan)
        self.assertIn("Do not wait for the user to ask for a file", plan)
        self.assertIn("Persist the decision before moving to a new topic", plan)
        self.assertIn("status `draft`", plan_format)
        self.assertIn("Do not create this file for a draft", plan_format)

    def test_action_requires_named_plan_and_evidence(self) -> None:
        action = self.read("skills/msf-action/SKILL.md")
        self.assertIn("Never select the newest plan", action)
        self.assertIn("Plan and Action must be separate sessions", action)
        self.assertIn("fresh evidence", action)
        self.assertIn("development log at the first mutation", action)

    def test_local_markdown_references_exist(self) -> None:
        for name in ("msf-init", "msf-plan", "msf-action"):
            folder = ROOT / "skills" / name
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            for reference in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" not in reference and not reference.startswith("#"):
                    with self.subTest(skill=name, reference=reference):
                        self.assertTrue((folder / reference).exists())


if __name__ == "__main__":
    unittest.main()
