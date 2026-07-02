# Development Workflow for `ours_192lane`

Goal: make code changes, performance fixes, and compile-bug fixes without rereading long files or guessing through Vitis errors.

## Shared project-local skills

Project-local skills live in `.agents/skills/` and are committed with the repo. Any GitHub collaborator can read the same `SKILL.md` files even if their Codex/Claude install lacks the global skills.

Use `srad-ours-192lane-workflow` first for work on `variants/srad/ours_192lane/`. It routes to the project-local Superpowers copies for TDD, debugging, plans, and verification.

Project-local skill set:

- `.agents/skills/srad-ours-192lane-workflow/`: SRAD workflow router.
- `.agents/skills/plan-docs/`: fuzzy input, PRD/spec/docs, change folders. Also covers the `plan-docx` trigger via `.agents/skills/plan-docx/`.
- `.agents/skills/spec-subagents/`: Kiro/spec/subagent/large-file-read workflow.
- `.agents/skills/superpowers-test-driven-development/`: RED/GREEN/REFACTOR before code changes.
- `.agents/skills/superpowers-systematic-debugging/`: root-cause debugging before fixes.
- `.agents/skills/superpowers-verification-before-completion/`: fresh evidence before completion claims.
- `.agents/skills/superpowers-writing-plans/`, `.agents/skills/superpowers-executing-plans/`, `.agents/skills/superpowers-subagent-driven-development/`: plan and execution workflow.
- `.agents/skills/skill-creator/`: adding/updating project-local skills.
- `.agents/skills/lean-coder/`: smallest correct diff discipline.

## Default loop

1. **Orient**: read `docs/CODEMAP_ours_192lane.md`; pick exact file ranges instead of full long-file reads.
2. **Spec**: for vague input, use `plan-docs`; for multi-step/spec/subagent work, use `spec-subagents`. Create or update `docs/changes/YYYY-MM-DD-short-name/` and `.kiro/specs/<short-name>/`.
3. **RED**: write the smallest failing test/check first.
4. **GREEN**: make the smallest change that passes the test.
5. **Refactor**: only after green, and only if it removes real duplication or confusion.
6. **Verify**: run `python scripts/check_ours_192lane.py`; use `--sim` on Vitis/make machines.
7. **Evidence**: record paper-worthy timing/verifier results in `docs/journal/ours_192lane-evidence.md`.

## What to run

```bash
python scripts/check_ours_192lane.py
```

Validate project-local skills only:

```bash
python scripts/validate_project_skills.py
```

On the VCK190/Vitis machine when simulation is needed:

```bash
python scripts/check_ours_192lane.py --sim
```

## When fixing compile or performance bugs

Use `docs/DEBUG_PLAYBOOK.md` before editing. Capture the exact command, first error, layer, hypothesis, and verification result. Do not stack speculative fixes.
