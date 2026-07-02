# SRAD

SRAD implementations and experiments for Xilinx Vitis, AI Engine, FPGA PL kernels, CUDA, and RTX4090 benchmark paths.

This repository was reorganized from a research workspace into a public GitHub project. Variant directories remain self-contained so their original relative paths and Makefile workflows keep working.
The journal-target implementation is `variants/srad/ours_192lane/`, targeting the Xilinx VCK190 board.

## Layout

```text
variants/
  srad/            Main SRAD Vitis/AIE/CUDA/FPGA variants
  stencilflow/     Stencilflow experiment variants
benchmarks/
  rtx4090/         RTX4090 CUDA benchmark code
research/
  sparta/          SPARTA reference material
archive/
  srad-snapshot/   Previous nested SRAD source snapshot
docs/              Project and build documentation
scripts/           Maintenance helpers
```

## Quick Start

Run builds from a concrete variant directory:

```bash
cd variants/srad/ours_192lane
make data
python data/test_sim_semantics.py
make sim
```

Common targets:

- `make data` generates input and golden data.
- `python data/test_sim_semantics.py` runs the fast pure-Python mapping and stream checks for `ours_192lane`.
- `make sim` builds and runs the default software emulation simulation.
- `make TARGET=hw sim` runs the hardware-target AIE simulation path where supported.
- `make all` builds AIE, PL kernels, host, package, and `sd_card/` output where supported.
- `make clean` removes generated outputs for that variant.

See [docs/BUILD.md](docs/BUILD.md) and [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

Shared workflow skills are committed under `.agents/skills/`; see [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md). The reusable local check is:

```bash
python scripts/check_ours_192lane.py
```

## Toolchain

Most Vitis/AIE variants expect environment variables such as:

- `XILINX_VITIS`
- `XILINX_HLS`
- `XILINX_XRT`
- `EDGE_COMMON_SW_PATH`
- `SYSROOT_PATH`
- `PLATFORM_REPO_PATHS`

CUDA benchmark paths require an NVIDIA CUDA toolchain.

The final board target is VCK190. `variants/srad/ours_192lane/Makefile` defaults `BASE_PLATFORM` to the VCK190 base platform path under `PLATFORM_REPO_PATHS`.

## Repository Policy

Generated data, simulator traces, Vitis build products, XRT packages, and Python bytecode are intentionally ignored. Regenerate them locally with variant-local scripts and Makefiles.
`research/sparta/` and `archive/srad-snapshot/` are retained as provenance and comparison material; do not clean them as generated output.

No repository-wide open-source license has been selected yet. See [LICENSE.md](LICENSE.md).
