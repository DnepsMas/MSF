"""Install the MSF skills into a user-level Claude Code skills directory."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


SKILLS = ("msf-init", "msf-plan", "msf-action", "msf-review", "msf-auto")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "skills"


def default_destination() -> Path:
    return Path.home() / ".claude" / "skills"


def validate_source() -> None:
    missing = [name for name in SKILLS if not (SOURCE_ROOT / name / "SKILL.md").is_file()]
    if missing:
        raise RuntimeError(f"Missing source skills: {', '.join(missing)}")


def sync_tree(source: Path, target: Path) -> None:
    """Make target's contents match source without renaming the target directory."""
    target.mkdir(parents=True, exist_ok=True)
    source_files = {path.relative_to(source) for path in source.rglob("*") if path.is_file()}
    target_files = [path for path in target.rglob("*") if path.is_file()]
    for path in target_files:
        if path.relative_to(target) not in source_files:
            path.unlink()
    for path in sorted((path for path in target.rglob("*") if path.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass
    for relative in source_files:
        output = target / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, output)


def install(
    destination: Path,
    force: bool = False,
    dry_run: bool = False,
) -> list[Path]:
    validate_source()
    destination = destination.expanduser().resolve()
    existing = [destination / name for name in SKILLS if (destination / name).exists()]
    if existing and not force:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(f"Already installed: {names}. Re-run with --force to update.")

    targets = [destination / name for name in SKILLS]
    if dry_run:
        return targets

    destination.mkdir(parents=True, exist_ok=True)
    backup_root = Path(tempfile.mkdtemp(prefix=".msf-backup-", dir=destination))
    installed: list[Path] = []
    backed_up: list[tuple[Path, Path]] = []
    try:
        for target in targets:
            if target.exists():
                backup = backup_root / "current" / target.name
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(target, backup)
                backed_up.append((target, backup))
        for name in SKILLS:
            target = destination / name
            if force and target.exists():
                sync_tree(SOURCE_ROOT / name, target)
            else:
                shutil.copytree(SOURCE_ROOT / name, target)
            installed.append(target)
    except Exception:
        for target in reversed(installed):
            backup = next((saved for old, saved in backed_up if old == target), None)
            if backup is not None and backup.exists():
                sync_tree(backup, target)
            elif target.exists():
                shutil.rmtree(target)
        raise
    finally:
        shutil.rmtree(backup_root, ignore_errors=True)
    return targets


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=default_destination())
    parser.add_argument("--force", action="store_true", help="replace existing MSF skill directories")
    parser.add_argument("--dry-run", action="store_true", help="show destinations without writing")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        targets = install(
            args.destination,
            force=args.force,
            dry_run=args.dry_run,
        )
    except (OSError, RuntimeError) as exc:
        print(f"MSF installation failed: {exc}", file=sys.stderr)
        return 1
    action = "Would install" if args.dry_run else "Installed"
    for target in targets:
        print(f"{action}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
