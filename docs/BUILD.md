# Build And Test Guide

## Vitis/AIE Variants

Example:

```bash
cd variants/srad/ours_192lane
make data
python data/test_sim_semantics.py
make sim
```

Useful targets:

- `make data`: generate local input and golden data.
- `python data/test_sim_semantics.py`: run fast Python semantic checks for the final `ours_192lane` mapping.
- `make sim`: build and run the default simulation path.
- `make TARGET=hw sim`: run the hardware-target simulation path where supported.
- `make all`: build AIE, PL kernels, host, package, and `sd_card/` output.
- `make clean`: remove generated build products in that variant.

## CUDA Benchmark

Example:

```bash
cd benchmarks/rtx4090/srad
make
```

Some CUDA subdirectories carry their own Makefiles and README files. Prefer their local instructions.

## Board Target

The journal-target SRAD design is `variants/srad/ours_192lane/` for Xilinx VCK190. Its Makefile defaults `BASE_PLATFORM` to `xilinx_vck190_base_202320_1` under `PLATFORM_REPO_PATHS`.

## Python Checks

Repository-level syntax check:

```bash
python scripts/check_ours_192lane.py
```

This runs the fast `ours_192lane` semantic checks, Python compilation, and project-local skill validation. It does not replace Vitis simulation.

## Generated Data

Generated files under `data/` and `board_data/` are ignored by Git. Regenerate them with variant-local scripts or `make data`.
