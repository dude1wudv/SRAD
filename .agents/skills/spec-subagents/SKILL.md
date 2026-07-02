---
name: spec-subagents
description: Project-local spec-driven workflow for SRAD. Use when a task mentions Kiro, specs, requirements/design/tasks, subagents, context-window overflow, large file reads, Get-Content, or spans 3+ files. Prefer durable .kiro/specs plus bounded agents or targeted reads.
---

# Spec Subagents

## Use

- Create `.kiro/specs/<name>/requirements.md`, `design.md`, `tasks.md` for multi-step work.
- Use `docs/CODEMAP_ours_192lane.md` before reading long files.
- Do not read files over 500 lines or 50KB whole; use targeted ranges/search or a scout agent.
- Keep subagent tasks disjoint and bounded. Agents inherit the same model unless the user asks otherwise.

## Scout packet

```text
Goal:
Read:
Do not edit:
Return: paths, line ranges, key symbols, risks.
```

## Worker packet

```text
Goal:
Read:
Write:
Do not touch:
Verification:
Return: changed files, evidence, risks.
```
