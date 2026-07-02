# Repository Guidelines

## Project Structure & Module Organization

This repository contains SRAD implementations and related stencil experiments for Xilinx Vitis/AIE, FPGA PL kernels, CUDA, and RTX4090 benchmarking.

- `variants/srad/`: main SRAD variants such as `CUDA/`, `FPGA/`, `tri/`, `ours_32lane/`, and `ours_192lane/`.
- `variants/stencilflow/`: stencilflow experiment variants.
- `benchmarks/rtx4090/`: RTX4090 CUDA benchmark code.
- `research/sparta/`: SPARTA reference material.
- `archive/srad-snapshot/`: previous nested SRAD source snapshot kept for comparison.

Most Vitis variants use the same layout: `aie/` for graph and kernel code, `pl/` for Vitis HLS PL kernels, `ps/` for the host program, `data/` for generators/verifiers and local generated data, plus variant-local `Makefile`, `conn.cfg`, `run.sh`, and `xrt.ini`.

## Build, Test, And Development Commands

Run commands from a variant directory, for example:

```bash
cd variants/srad/ours_32lane
make data
make sim
```

- `make data` generates input data under `data/`.
- `make sim` builds the AIE graph for the default emulation path and compares outputs where supported.
- `make TARGET=hw sim` runs the hardware-target AIE simulation path when supported.
- `make all` builds AIE, PL kernels, XSA, host executable, package, and `sd_card/` output where supported.
- `make clean` removes generated build products for that variant.

The Makefiles expect Vitis/XRT environment variables such as `XILINX_VITIS`, `XILINX_HLS`, `EDGE_COMMON_SW_PATH`, `SYSROOT_PATH`, and `PLATFORM_REPO_PATHS`.

## Coding Style & Naming Conventions

Use C++20-compatible code for host/AIE/PL sources. Match existing indentation in touched files: tabs in Makefiles, compact C/C++ formatting in `*.cpp`, `*.h`, and `*.cc`. Keep generated data filenames descriptive and variant-local, for example `data/plio_ours_j_0.txt` or `data/gold_gpu_srad_c.txt`. Preserve existing kernel and graph names such as `TopGraph`, `TopPL`, and `Q0Ctrl` unless build files are updated together.

## Testing Guidelines

Prefer `make sim` as the fast correctness check before hardware builds. It regenerates simulation data when needed and runs variant-local verification. When changing dimensions, lane counts, or data formats, update `aie/Config.h`, `data/gen_case.py`, and verification expectations in the same variant.

## Commit & Pull Request Guidelines

Keep commits focused and outcome-oriented. Pull requests should state the affected variant, commands run (`make sim`, `make all`, etc.), required Vitis/platform versions, and generated artifacts intentionally included or omitted.

## Agent-Specific Instructions

Do not overwrite generated build directories unless cleaning the active variant. Before copying changes across `ours_*` variants, diff the target Makefile/config first; lane counts and data file lists often differ.
