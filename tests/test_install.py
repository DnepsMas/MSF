from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.install import SKILLS, default_destination, install


class InstallTests(unittest.TestCase):
    def test_default_destination_is_user_skills_directory(self) -> None:
        self.assertEqual(Path.home() / ".agents" / "skills", default_destination())

    def test_fresh_install_copies_all_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "skills"
            targets = install(destination)
            self.assertEqual([destination / name for name in SKILLS], targets)
            for target in targets:
                self.assertTrue((target / "SKILL.md").is_file())

    def test_existing_install_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "skills"
            install(destination)
            with self.assertRaises(FileExistsError):
                install(destination)

    def test_force_replaces_stale_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "skills"
            install(destination)
            stale = destination / "msf-plan" / "stale.txt"
            stale.write_text("old", encoding="utf-8")
            install(destination, force=True)
            self.assertFalse(stale.exists())

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "skills"
            targets = install(destination, dry_run=True)
            self.assertEqual(4, len(targets))
            self.assertFalse(destination.exists())

    def test_legacy_install_requires_explicit_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            destination = root / ".agents" / "skills"
            legacy = root / ".codex" / "skills"
            (legacy / "msf-plan").mkdir(parents=True)
            with self.assertRaises(FileExistsError):
                install(destination, legacy_root=legacy)

    def test_remove_legacy_keeps_only_new_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            destination = root / ".agents" / "skills"
            legacy = root / ".codex" / "skills"
            for name in SKILLS:
                skill = legacy / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text("legacy", encoding="utf-8")

            targets = install(destination, remove_legacy=True, legacy_root=legacy)

            self.assertTrue(all((target / "SKILL.md").is_file() for target in targets))
            self.assertTrue(all(not (legacy / name).exists() for name in SKILLS))

    def test_legacy_cleanup_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            destination = root / ".agents" / "skills"
            legacy = root / ".codex" / "skills"
            (legacy / "msf-init").mkdir(parents=True)

            install(destination, dry_run=True, remove_legacy=True, legacy_root=legacy)

            self.assertFalse(destination.exists())
            self.assertTrue((legacy / "msf-init").is_dir())


if __name__ == "__main__":
    unittest.main()
