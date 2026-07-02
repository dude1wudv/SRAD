---
name: plan-docs
description: Project-local planning/docs skill for SRAD. Use when user input is vague, requirements are ambiguous, a task needs PRD/spec/design/tasks/docs, or the user says plan-docs/plan-docx/Kiro/spec/需求/规划/文档/开发追踪. Automatically turn fuzzy input into docs/changes/YYYY-MM-DD-short-name with original words, requirements, design, index, tracking, and tests before implementation.
---

# Plan Docs

Use for fuzzy or multi-step SRAD requests before coding.

## Required outputs for a new change

Create `docs/changes/YYYY-MM-DD-short-name/`:

- `用户原话.md`: quote user words exactly.
- `01-需求文档.md`: goal, scope, non-goals, acceptance.
- `02-架构文档.md`: touched modules and data/control flow.
- `03-索引.md`: module tree and dependency table.
- `04-开发追踪.md`: ordered tasks with status.
- `08-测试用例.md`: red/green/verification commands.

For durable implementation specs, mirror into `.kiro/specs/<short-name>/requirements.md`, `design.md`, `tasks.md`.

## Discipline

Ask one focused question if a real decision blocks planning. Otherwise choose the smallest useful workflow. Do not dump long prose into root docs; keep each change isolated under `docs/changes/`.
