# Repository Guidelines

## Project Structure & Module Organization

This repository supports SRAD journal work: algorithm exploration, implementation
variants, and reproducible evidence for the final VCK190 design.

- `variants/srad/ours_192lane/`: canonical VCK190 journal implementation under active optimization.
- `variants/srad/`: comparison and exploration variants such as `CUDA/`, `FPGA/`, `tri/`, `ours_32lane/`, and `ours_96lane/`.
- `variants/stencilflow/`: stencilflow experiment variants.
- `benchmarks/rtx4090/`: RTX4090 CUDA benchmark code.
- `research/sparta/`: SPARTA reference material.
- `archive/srad-snapshot/`: previous nested SRAD source snapshot kept for comparison.

Most Vitis variants use the same layout: `aie/` for graph and kernel code, `pl/` for Vitis HLS PL kernels, `ps/` for the host program, `data/` for generators/verifiers and local generated data, plus variant-local `Makefile`, `conn.cfg`, `run.sh`, and `xrt.ini`.

Treat non-`ours_192lane` SRAD variants as baselines unless the task explicitly asks to edit them. Treat `archive/srad-snapshot/` as read-only comparison material.

## Final Variant Map: `variants/srad/ours_192lane/`

- `aie/Config.h`: single source of truth for dimensions, lane count, board partitioning, PLIO merge shape, and AIE placement helpers.
- `aie/ProcessGraph/`: top-level AIE graph, lane PLIO fanout, pktmerge outputs, and tile placement.
- `aie/ProcessUnit/`: SRAD local-q and coefficient-update AIE kernels.
- `pl/TopPL.cpp`: 12-TopPL-CU board path; each CU owns 16 AIE row-stream lanes.
- `pl/Q0Ctrl.cpp`: global q0 aggregation and broadcast control.
- `ps/host.cpp`: board host program, XRT launch order, timing, and optional output dump.
- `data/gen_case.py`: input and PLIO stream generation.
- `data/verify_srad.py`: simulator output decoding and golden comparison.
- `data/test_sim_semantics.py`: fast Python regression checks for stream and mapping semantics.

## Build, Test, And Development Commands

Run commands from a variant directory, for example:

```bash
cd variants/srad/ours_192lane
make data
python data/test_sim_semantics.py
make sim
```

- `make data` generates input data under `data/`.
- `python data/test_sim_semantics.py` runs the fast pure-Python semantic checks.
- `make sim` builds the AIE graph for the default emulation path and compares outputs where supported.
- `make TARGET=hw sim` runs the hardware-target AIE simulation path when supported.
- `make all` builds AIE, PL kernels, XSA, host executable, package, and `sd_card/` output where supported.
- `make clean` removes generated build products for that variant.

The Makefiles expect Vitis/XRT environment variables such as `XILINX_VITIS`, `XILINX_HLS`, `EDGE_COMMON_SW_PATH`, `SYSROOT_PATH`, and `PLATFORM_REPO_PATHS`.

## Target Hardware & Dependencies

Default target board is Xilinx VCK190. Write new Vitis/AIE/PL/PS code, platform assumptions, and dependency instructions for VCK190 unless the user explicitly names another board.

Prioritize VCK190 toolchain dependencies: Vitis, Vitis HLS, XRT, VCK190 base platform (`xilinx_vck190_*`), sysroot, rootfs, and matching platform repository paths. Do not add or install unrelated board stacks such as Intel/Altera AOCL unless the task is explicitly about legacy RTX4090/FPGA benchmark code.

Keep board/platform paths configurable through environment variables or Makefile variables. Do not hard-code local installation paths.

If using a remote lab VCK190 machine, keep heavy build/runtime dependencies on the remote machine. The local Windows machine only needs Git, SSH/SCP or Remote-SSH, an editor, and Python 3 for local checks. Do not install local Vitis, Vitis HLS, XRT, platform files, sysroot/rootfs, Make/GCC, or Visual Studio Build Tools unless the user explicitly asks for local builds.

From the repository root, pass the final variant explicitly:

```bash
make VAR=variants/srad/ours_192lane data
make VAR=variants/srad/ours_192lane sim
```

## Coding Style & Naming Conventions

Use C++20-compatible code for host/AIE/PL sources. Match existing indentation in touched files: tabs in Makefiles, compact C/C++ formatting in `*.cpp`, `*.h`, and `*.cc`. Keep generated data filenames descriptive and variant-local, for example `data/plio_ours_j_0.txt` or `data/gold_gpu_srad_c.txt`. Preserve existing kernel and graph names such as `TopGraph`, `TopPL`, and `Q0Ctrl` unless build files are updated together.

For `ours_192lane`, keep these files in sync when changing lane counts, board dimensions, row partitioning, or PLIO shape:

- `aie/Config.h`
- `aie/ProcessGraph/StencilCoreGraph.h`
- `pl/TopPL.cpp`
- `pl/Q0Ctrl.cpp`
- `ps/host.cpp`
- `conn.cfg`
- `data/gen_case.py`
- `data/verify_srad.py`
- `data/test_sim_semantics.py`
- `pl/README.md`

## Testing Guidelines

Prefer the smallest check that covers the change:

- Mapping, stream, generator, or verifier edits: run `python data/test_sim_semantics.py`.
- AIE kernel/graph edits: run `make sim`.
- Hardware-target placement/resource edits: run `make TARGET=hw sim` before `make all`.

When changing dimensions, lane counts, or data formats, update `aie/Config.h`, `data/gen_case.py`, and verification expectations in the same variant.

For journal evidence, record the exact variant, commit, command, target, board/platform, image size, iteration count, timing output, and verifier result. Do not commit generated data, simulator traces, Vitis build directories, XRT packages, or `sd_card/` outputs unless explicitly requested.

## Commit & Pull Request Guidelines

Keep commits focused and outcome-oriented. Pull requests should state the affected variant, commands run (`python data/test_sim_semantics.py`, `make sim`, `make all`, etc.), required Vitis/platform versions, and generated artifacts intentionally included or omitted.

## Agent-Specific Instructions

Do not overwrite generated build directories unless cleaning the active variant. Before copying changes across `ours_*` variants, diff the target Makefile/config first; lane counts and data file lists often differ.

Prefer improving `variants/srad/ours_192lane/` first, then document whether older variants remain baselines or need backports. Do not restructure directories or delete comparison material without explicit confirmation.
