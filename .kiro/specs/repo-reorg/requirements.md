# Repository Reorganization Requirements

## Goal

Turn this SRAD workspace into a clean public GitHub repository while preserving source code and removing local/generated state.

## Scope

- Rebuild Git history from a fresh `git init`.
- Remove root and nested `.git` directories.
- Move top-level implementation families into a documented layout.
- Keep source, scripts, configs, tests, papers, and project docs.
- Remove generated caches, build outputs, simulator traces, and large generated data files.
- Add public-repository documentation and GitHub configuration.
- Publish a new public repository under the active GitHub account.

## Non-goals

- Do not refactor kernel, host, AIE, PL, or CUDA source behavior.
- Do not rewrite Vitis Makefiles for a shared monorepo build.
- Do not assume a permissive open-source license unless explicitly chosen.

## Safety

- Only operate inside the repository root.
- Verify destructive paths resolve under the repository root.
- Prefer preserving source over deleting uncertain files.
- Generated data can be regenerated from variant-local scripts and should not be committed.
