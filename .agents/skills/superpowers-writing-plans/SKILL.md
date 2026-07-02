---
name: superpowers-writing-plans
description: Project-local copy of the Superpowers planning skill. Use when SRAD work has a spec/requirements or spans multiple files before touching code; writes bite-sized TDD plans with exact files, commands, and expected outputs.
---

# Superpowers Writing Plans

Create a plan before multi-file SRAD changes.

Save plans to `docs/superpowers/plans/YYYY-MM-DD-short-name.md` unless a `.kiro/specs/<name>/tasks.md` plan already exists.

Each task must include:
- exact files and code-map anchors
- RED test/check command and expected failure
- minimal implementation step
- GREEN command and expected pass
- final verification command

No placeholders. If a task cannot have an automated RED check, state the closest reproducible manual failure and why.
