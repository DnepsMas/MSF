from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.install import SKILLS, default_destination, install


class InstallTests(unittest.TestCase):
    def test_default_destination_is_user_skills_directory(self) -> None:
        self.assertEqual(Path.home() / ".claude" / "skills", default_destination())

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


if __name__ == "__main__":
    unittest.main()
