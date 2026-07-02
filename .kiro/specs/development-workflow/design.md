# Development Workflow Design

## Layout

```text
.agents/skills/                         Project-local skills
  srad-ours-192lane-workflow/           SRAD workflow router
  plan-docs/                            Fuzzy input -> docs/changes + specs
  plan-docx/                            Alias for plan-docs typo/trigger
  spec-subagents/                       Kiro/spec/subagent/large-read workflow
  skill-creator/                        Future project-local skill maintenance
  lean-coder/                           Minimal-diff coding discipline
  superpowers-test-driven-development/  TDD local copy
  superpowers-systematic-debugging/     Debugging local copy
  superpowers-verification-before-completion/
  superpowers-writing-plans/
  superpowers-executing-plans/
docs/CODEMAP_ours_192lane.md            Long-file code map
docs/DEBUG_PLAYBOOK.md                  Compile/runtime/perf triage
docs/DEVELOPMENT_WORKFLOW.md            Daily loop
scripts/check_ours_192lane.py           Shared quick check
scripts/test_check_ours_192lane.py      TDD test for the runner
scripts/validate_project_skills.py      Local skill structure validation
```

## Workflow

Skill router → code map → RED test → minimal patch → GREEN → verification → evidence.
