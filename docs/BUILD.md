# Build And Test Guide

## Vitis/AIE Variants

Example:

```bash
cd variants/srad/ours_32lane
make data
make sim
```

Useful targets:

- `make data`: generate local input and golden data.
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

## Python Checks

Repository-level syntax check:

```bash
python -m compileall variants benchmarks research archive scripts
```

This does not replace Vitis simulation; it only catches Python syntax errors in generators, verifiers, and helper scripts.

## Generated Data

Generated files under `data/` and `board_data/` are ignored by Git. Regenerate them with variant-local scripts or `make data`.
