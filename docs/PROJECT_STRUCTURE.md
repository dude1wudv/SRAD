# Project Structure

## Root

- `variants/srad/ours_192lane/`: final journal-target SRAD implementation for VCK190.
- `variants/srad/`: other SRAD implementation and baseline variants.
- `variants/stencilflow/`: stencilflow experiment variants.
- `benchmarks/rtx4090/`: CUDA benchmark code for RTX4090.
- `research/sparta/`: SPARTA reference material and paper, retained for provenance.
- `archive/srad-snapshot/`: previous nested SRAD source tree kept for comparison.
- `docs/`: repository-level documentation.
- `scripts/`: maintenance scripts.
- `.github/`: GitHub issue, pull request, and CI configuration.

## Variant Layout

Most Vitis variants follow this shape:

```text
<variant>/
  aie/       AI Engine graph and kernels
  pl/        Vitis HLS PL kernels
  ps/        Host program
  data/      Data generators, verifiers, and generated local data
  Makefile   Variant-local build entrypoint
  conn.cfg   Stream/connectivity config
  xrt.ini    XRT runtime config
  run.sh     Board or emulation run helper
```

## Important Convention

Run commands from the variant directory. Variant Makefiles use relative paths such as `./data`, so root-level build commands should delegate into the target variant instead of moving files across variants.
Keep `research/` and `archive/` as reference material unless a cleanup task explicitly says to remove them.
