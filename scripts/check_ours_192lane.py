#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VARIANT = ROOT / "variants" / "srad" / "ours_192lane"


def command_label(cmd: list[str]) -> str:
    display = list(cmd)
    if display and Path(display[0]) == Path(sys.executable):
        display[0] = "python"
    return " ".join(display)


def run(cmd: list[str], cwd: Path, dry_run: bool) -> int:
    print(f"[check] ({cwd.relative_to(ROOT)}) {command_label(cmd)}")
    if dry_run:
        return 0
    return subprocess.run(cmd, cwd=cwd).returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run reusable checks for variants/srad/ours_192lane."
    )
    parser.add_argument(
        "--sim",
        action="store_true",
        help="also run make sim; requires Vitis/make environment",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print commands without running them",
    )
    args = parser.parse_args()

    checks: list[tuple[list[str], Path]] = [
        ([sys.executable, "data/test_sim_semantics.py"], VARIANT),
        ([sys.executable, "-m", "compileall", "variants/srad/ours_192lane/data", "scripts"], ROOT),
        ([sys.executable, "scripts/validate_project_skills.py"], ROOT),
    ]
    if args.sim:
        checks.append((["make", "sim"], VARIANT))

    for cmd, cwd in checks:
        code = run(cmd, cwd, args.dry_run)
        if code:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
