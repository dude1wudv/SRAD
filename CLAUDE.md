# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

SRAD (Speckle Reducing Anisotropic Diffusion) journal work: algorithm exploration, Vitis/AIE/PL/PS implementation variants, and reproducible evidence for a final VCK190 board design.

- `variants/srad/ours_192lane/`: canonical, actively-optimized VCK190 journal implementation. Treat all other `variants/srad/*` (`CUDA/`, `FPGA/`, `tri/`, `ours_32lane/`, `ours_96lane/`, etc.) as baselines — don't edit them unless the task explicitly asks to.
- `variants/stencilflow/`: unrelated stencilflow experiment variants (`tri_*`, `dual*`, `four_*`, `five_*`, `six_*`) with their own `SystemConfig.h`/`Config.h`, `aie/`, `ps/`, `data/`.
- `benchmarks/rtx4090/`: CUDA benchmark code for RTX4090 (separate NVIDIA toolchain, unrelated to VCK190).
- `research/sparta/`: SPARTA reference material, read-only provenance.
- `archive/srad-snapshot/`: previous nested SRAD source snapshot, read-only comparison material.
- `docs/`: build, cleanup, structure, and journal-evidence docs.
- `scripts/clean-generated.ps1`: removes generated build/data artifacts.

Most Vitis variants share this layout: `aie/` (graph + kernels), `pl/` (Vitis HLS PL kernels), `ps/` (host program), `data/` (generators/verifiers + local generated data), plus variant-local `Makefile`, `conn.cfg`, `run.sh`, `xrt.ini`.

## Project-Local Skills And Workflow

This repository commits shared skills under `.agents/skills/` so GitHub collaborators can use the same workflow even without global Claude/Codex skills installed.

- Start `ours_192lane` work with `.agents/skills/srad-ours-192lane-workflow/SKILL.md`.
- Fuzzy user input, vague requirements, PRD/spec/docs, or `plan-docx`/`plan-docs` requests -> `.agents/skills/plan-docs/SKILL.md`.
- Kiro/spec/subagent/context-window/large-file-read work -> `.agents/skills/spec-subagents/SKILL.md`.
- Code changes and bug fixes -> Superpowers TDD copy: `.agents/skills/superpowers-test-driven-development/SKILL.md`. Write and run the RED failing check before implementation, then GREEN, then refactor.
- Compile/test/runtime/performance bugs -> `.agents/skills/superpowers-systematic-debugging/SKILL.md` before fixing.
- Completion claims -> `.agents/skills/superpowers-verification-before-completion/SKILL.md` and fresh `python scripts/check_ours_192lane.py` output.

Do not read long files whole. Use `docs/CODEMAP_ours_192lane.md` first, then targeted ranges/search hits.

## Build, Test, and Development Commands

Run from inside the variant directory:

```bash
cd variants/srad/ours_192lane
make data                          # generate input data under data/
python data/test_sim_semantics.py  # fast pure-Python semantic/mapping checks (no Vitis needed)
make sim                           # default TARGET=sw_emu (x86simulator) correctness check
make TARGET=hw sim                 # aiesimulator instruction-level AIE sim
make all                           # aie -> kernels -> xsa -> host -> package -> sd_card
make clean                         # remove all generated build products for this variant
```

Or from the repo root, passing the variant explicitly (root `Makefile` just delegates via `-C`):

```bash
make VAR=variants/srad/ours_192lane data
make VAR=variants/srad/ours_192lane sim
```

Repo-wide Python syntax check (does not replace simulation):

```bash
python -m compileall variants benchmarks research archive scripts
```

CI (`.github/workflows/metadata-check.yml`) runs exactly these two: `python -m compileall ...` and `python data/test_sim_semantics.py` in `ours_192lane`.

Notes on the `ours_192lane` Makefile:
- Bare `make sim` implicitly forces `TARGET=sw_emu` (quick x86sim check); pass `TARGET=hw` explicitly for real aiesimulator runs.
- Requires Vitis/XRT env vars: `XILINX_VITIS`, `XILINX_HLS`, `EDGE_COMMON_SW_PATH`, `SYSROOT_PATH`, `PLATFORM_REPO_PATHS`. `BASE_PLATFORM` defaults to `xilinx_vck190_base_202320_1` under `PLATFORM_REPO_PATHS`.
- Per repo policy, keep heavy Vitis/XRT/platform installs on a remote lab machine; the local Windows box only needs Git, SSH/SCP, an editor, and light Python (`numpy`, `pytest`, `jinja2`) for local checks.

## Architecture: `variants/srad/ours_192lane/`

192 AIE row-stream lanes process a 4000x4000 board image, split into a PL/AIE/PS pipeline:

- **`aie/Config.h`** — single source of truth for lane count, dimensions, board partitioning, PLIO merge shape, and AIE tile placement helpers (`lane_tile_col`, `local_q_tile_row`, `coeff_update_tile_row`). Heavily `static_assert`-guarded (192 lanes, 12 TopPL workers, 384 AIE cores, 48 merged output PLIOs, etc.) — these assertions encode the current fixed board mapping.
- **`aie/ProcessGraph/StencilCoreGraph.h`** — `SradCoreGraph` (one AIE lane: `k_local_q` -> `k_coeff_update` kernel pair) and `GraphOursPLQ0` (top-level graph instantiating `kParallelLanes` (192) `SradCoreGraph` cores, fanning PLIO inputs per-lane, and merging outputs 4-ways via `pktmerge` into 48 output PLIOs).
- **`aie/ProcessUnit/`** — `srad_local_q.cc`/`srad_coeff_update.cc` kernels implementing the two-stage SRAD math (local q computation, then coefficient/update), with shared types in `srad.h`/`include.h`.
- **`pl/TopPL.cpp`** — instantiated 12 times as CUs; the 12 CUs form 6 row blocks x 2 column workers. Each `TopPL` owns 16 AIE lanes and a contiguous 2000-column half-image over a 667-row center block (see `pl/README.md` for the exact row/column split and halo-row handling).
- **`pl/Q0Ctrl.cpp`** — aggregates the 12 CUs' local `sum`/`sum2` reports, computes one global `q0sqr` over the full board, and broadcasts it back to all `TopPL` CUs.
- **`ps/host.cpp`** — XRT host program: opens kernel CUs, launches in the correct order, times execution, optionally dumps output.
- **`data/gen_case.py`** — generates the input image and per-lane PLIO stream files consumed by both simulation and hardware runs.
- **`data/verify_srad.py`** — decodes simulator/hardware output and compares against a golden reference; also exposes `read_config()`, reflecting `Config.h` constants into Python for `data/gen_case.py` and tests.
- **`data/test_sim_semantics.py`** — fast pure-Python checks that `gen_case`/`verify_srad`/`StencilCoreGraph.h` stay consistent with `Config.h` without invoking Vitis.

When changing lane counts, board dimensions, row partitioning, or PLIO shape, keep these files in sync together: `aie/Config.h`, `aie/ProcessGraph/StencilCoreGraph.h`, `pl/TopPL.cpp`, `pl/Q0Ctrl.cpp`, `ps/host.cpp`, `conn.cfg`, `data/gen_case.py`, `data/verify_srad.py`, `data/test_sim_semantics.py`, `pl/README.md`.

## Coding Style

C++20 for host/AIE/PL code. Match existing indentation per file (tabs in Makefiles, compact C/C++ style in `*.cpp`/`*.h`/`*.cc`). Keep generated data filenames descriptive and variant-local (e.g. `data/plio_ours_j_0.txt`, `data/gold_gpu_srad_c.txt`). Preserve existing kernel/graph names (`TopGraph`, `TopPL`, `Q0Ctrl`) unless build files are updated in the same change.

## Testing Guidelines

Match the check to the change:

- Mapping/stream/generator/verifier edits -> `python data/test_sim_semantics.py`
- AIE kernel/graph edits -> `make sim`
- Hardware-target placement/resource edits -> `make TARGET=hw sim` before attempting `make all`

Don't commit generated data, simulator traces, Vitis build directories, XRT packages, or `sd_card/` outputs unless explicitly requested — `scripts/clean-generated.ps1` removes these.

## Target Hardware

Default board is Xilinx VCK190. Write new Vitis/AIE/PL/PS code and dependency instructions for VCK190 unless told otherwise. Don't introduce unrelated board stacks (e.g. Intel/Altera AOCL) except for legacy RTX4090/FPGA benchmark work. Keep board/platform paths configurable via env vars or Makefile variables — never hard-code local install paths.

## Working Across Variants

Prefer improving `ours_192lane` first. Before copying changes to other `ours_*` variants, diff the target Makefile/config first — lane counts and data file lists differ between variants. Don't restructure directories or delete comparison material (`research/`, `archive/`) without explicit confirmation.
