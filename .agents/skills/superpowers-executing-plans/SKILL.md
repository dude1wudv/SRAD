---
name: superpowers-executing-plans
description: Project-local copy of the Superpowers plan execution skill. Use when executing a written SRAD implementation plan task-by-task with TDD and verification checkpoints.
---

# Superpowers Executing Plans

1. Read the plan completely.
2. Check for blockers, missing commands, or unclear files before editing.
3. Execute each task in order: RED, GREEN, refactor, verify.
4. Stop and ask if a command is missing, a RED test cannot be produced, or verification fails repeatedly.
5. Before completion, use `superpowers-verification-before-completion`.

Never skip the plan's checks. Never batch unrelated fixes.
