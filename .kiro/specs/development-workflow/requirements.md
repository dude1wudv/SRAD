# Development Workflow Requirements

## Goal

Create a repository-committed workflow that lets SRAD collaborators change `variants/srad/ours_192lane/` without rereading long files, while using TDD and systematic debugging for compile/performance issues.

## Requirements

- Provide project-local skills under `.agents/skills/`.
- Include `plan-docs`/`plan-docx` for fuzzy input, `spec-subagents` for Kiro/spec/large-file-read work, and `skill-creator` for future local skill maintenance.
- Preserve Superpowers-style TDD red-green-refactor locally.
- Provide a code map for long files and targeted reads.
- Provide a debug playbook for Vitis/AIE/HLS/PS failures.
- Provide one reusable local check command.
- Validate project-local skill structure in the reusable check command.
- Synchronize instructions into `AGENTS.md` and `CLAUDE.md`.

## Non-goals

- Do not refactor SRAD implementation code.
- Do not require collaborators to install global Codex/Claude skills before reading the workflow.
