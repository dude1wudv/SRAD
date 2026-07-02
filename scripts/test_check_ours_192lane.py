#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_ours_192lane.py"


class CheckOurs192LaneTest(unittest.TestCase):
    def test_dry_run_lists_reusable_project_checks(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--dry-run"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("python data/test_sim_semantics.py", proc.stdout)
        self.assertIn("python -m compileall", proc.stdout)
        self.assertIn("python scripts/validate_project_skills.py", proc.stdout)
        self.assertNotIn("make sim", proc.stdout)

    def test_dry_run_can_include_vitis_sim_when_requested(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--dry-run", "--sim"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("make sim", proc.stdout)


if __name__ == "__main__":
    unittest.main()
