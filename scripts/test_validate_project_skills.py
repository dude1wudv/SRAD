#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_project_skills.py"


class ValidateProjectSkillsTest(unittest.TestCase):
    def test_validates_all_committed_project_skills(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("srad-ours-192lane-workflow", proc.stdout)
        self.assertIn("plan-docs", proc.stdout)
        self.assertIn("spec-subagents", proc.stdout)
        self.assertIn("superpowers-test-driven-development", proc.stdout)


if __name__ == "__main__":
    unittest.main()
