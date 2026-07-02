---
name: superpowers-test-driven-development
description: Project-local copy of the Superpowers TDD skill. Use before implementing any SRAD feature, bug fix, refactor, or behavior/performance change. Requires a failing test first, red-green-refactor, and evidence that the test failed before implementation.
---

# Superpowers Test-Driven Development

Iron law: no production code change without a failing test first, unless the user explicitly exempts generated/config-only work.

## Red-Green-Refactor

1. RED: add the smallest test or check that expresses the desired behavior or reproduces the bug.
2. Run it and confirm it fails for the expected reason, not typo/setup noise.
3. GREEN: write the smallest implementation change.
4. Run the same test and confirm it passes.
5. Refactor only after green, then rerun.

## SRAD defaults

- Python generator/verifier/mapping changes: add/update `variants/srad/ours_192lane/data/test_sim_semantics.py` or `scripts/test_*.py`.
- Build/check tooling changes: add/update a small `scripts/test_*.py`.
- AIE/PL/PS behavior changes that cannot be unit-tested locally: add a semantic Python check first when possible; otherwise document the manual RED in the change spec and run the closest available simulation on VCK190/Vitis.
- Performance changes still need a correctness guard first; benchmark after green.

## Required report

When finishing, include:
- RED command and failure summary.
- GREEN command and pass summary.
- Any skipped test and why it was not technically possible.
