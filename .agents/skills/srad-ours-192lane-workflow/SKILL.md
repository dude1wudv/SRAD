---
name: srad-ours-192lane-workflow
description: Use when changing, optimizing, debugging, compiling, testing, or documenting variants/srad/ours_192lane in this SRAD VCK190 repository. Enforces project-local code map first, Kiro-style change docs for multi-step work, Superpowers red-green TDD before behavior changes, systematic debugging before fixes, and fresh verification before completion.
---

# SRAD ours_192lane Workflow

Announce: "Using project-local $srad-ours-192lane-workflow."

## Required local sub-skills

Read these project-local skills from `.agents/skills/` as needed. Prefer the live Superpowers plugin skill when available, but this repo copy is the fallback and shared GitHub source of truth.

- Code change, bug fix, refactor, behavior change: `superpowers-test-driven-development/SKILL.md`.
- Compile bug, test failure, runtime issue, performance regression: `superpowers-systematic-debugging/SKILL.md` first.
- Before saying fixed/done/passing: `superpowers-verification-before-completion/SKILL.md`.
- Fuzzy user input, vague requirements, PRD/spec/docs: `plan-docs/SKILL.md` (also trigger when the user writes "plan-docx").
- Kiro/spec/subagent/large-read work: `spec-subagents/SKILL.md`.
- Multi-step or risky work: `superpowers-writing-plans/SKILL.md`, then `superpowers-executing-plans/SKILL.md`; use `superpowers-subagent-driven-development/SKILL.md` when subagents are available.
- Skill maintenance: `skill-creator/SKILL.md`.
- Small code edits: `lean-coder/SKILL.md`.

## Do not reread long files blindly

Before opening long files, read `docs/CODEMAP_ours_192lane.md`. For files over 500 lines or 50KB, use targeted ranges/search from the code map. `pl/TopPL.cpp` and `data/test_sim_semantics.py` are long; never `Get-Content -Raw` them in the main thread.

## Standard workflow

1. Read `docs/DEVELOPMENT_WORKFLOW.md`.
2. Use `docs/CODEMAP_ours_192lane.md` to choose minimal file/range context.
3. For compile/runtime/performance bugs, follow `docs/DEBUG_PLAYBOOK.md` and identify root cause before patching.
4. For behavior changes, write or update a failing test first and run it red.
5. Make the smallest code change that turns it green.
6. Run `python scripts/check_ours_192lane.py`; use `--sim` only on a machine with Vitis/make.
7. For paper evidence, append the command/timing/verifier result to `docs/journal/ours_192lane-evidence.md`.

## Kiro/change docs

For multi-step changes, create `docs/changes/YYYY-MM-DD-short-name/` with at least:
`用户原话.md`, `01-需求文档.md`, `02-架构文档.md`, `03-索引.md`, `04-开发追踪.md`, `08-测试用例.md`.

For durable implementation specs, also create `.kiro/specs/<short-name>/requirements.md`, `design.md`, and `tasks.md`.
