---
name: lean-coder
description: Project-local lean coding mode. Use for SRAD edits to choose the shortest correct change, avoid speculative abstractions, prefer existing code and standard tools, and keep checks minimal but real.
---

# Lean Coder

Use the first rung that works:

1. Does this need to exist?
2. Is it already in this repo?
3. Can stdlib/native tooling do it?
4. Can one small script/check cover it?
5. Only then add minimal code.

Do not simplify away trust-boundary checks, data-loss handling, hardware calibration, or requested validation. Non-trivial logic needs one runnable check.
