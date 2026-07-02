# `ours_192lane` Journal Evidence

Canonical variant: `variants/srad/ours_192lane/`

Board target: Xilinx VCK190

## Baseline Commands

```bash
cd variants/srad/ours_192lane
make data
python data/test_sim_semantics.py
make sim
```

Hardware-target checks:

```bash
cd variants/srad/ours_192lane
make TARGET=hw sim
make all
```

## Run Record Template

```text
Date:
Commit:
Variant: variants/srad/ours_192lane
Board/platform: Xilinx VCK190 / <BASE_PLATFORM>
Vitis:
XRT:
Image size: 4000 x 4000
Iterations:
Command:
Input:
Output:
Verifier result:
Timing lines:
  pl_total_us:
  timing us:
  ddr_to_ddr_kernel_us:
Notes:
```

## Evidence Policy

- Record the exact command, commit, platform, image size, iteration count, timing output, and verifier result for every result used in the paper.
- Keep generated data, logs, `Work/`, `_x/`, `package/`, `sd_card/`, `*.xo`, `*.xclbin`, and `*.xsa` out of Git unless explicitly requested.
- Keep `research/sparta/` and `archive/srad-snapshot/` as provenance and comparison material.
