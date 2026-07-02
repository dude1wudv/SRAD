---
name: superpowers-subagent-driven-development
description: Project-local Superpowers companion for executing SRAD plans with bounded subagents. Use when a written plan has independent tasks or when large-file reading should be delegated to scouts.
---

# Superpowers Subagent-Driven Development

Use after `superpowers-writing-plans` when subagents are available.

Rules:

- One fresh worker per independent task.
- Give exact read/write scope and verification command.
- Workers must not touch unrelated files or revert others' changes.
- Main agent reviews diffs and runs verification before completion.
- If subagents are unavailable, use `superpowers-executing-plans` inline.
