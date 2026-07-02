---
name: superpowers-systematic-debugging
description: Project-local copy of the Superpowers systematic debugging skill. Use for SRAD compile failures, simulation failures, Vitis/AIE/HLS errors, runtime bugs, and performance regressions before proposing fixes.
---

# Superpowers Systematic Debugging

Iron law: no fixes before root-cause investigation.

## Four phases

1. Reproduce: exact command, cwd, target, environment, full first error.
2. Localize: identify failing layer: Python data/checks, AIE graph/kernels, PL HLS, V++ link/package, PS host/XRT, board runtime.
3. Compare: find a working variant or previous passing path; list concrete differences.
4. Patch: write the smallest failing test/check first, then fix root cause, then verify.

## SRAD compile bug checklist

- Confirm cwd is `variants/srad/ours_192lane` unless using root delegation.
- Check VCK190 variables: `XILINX_VITIS`, `XILINX_HLS`, `EDGE_COMMON_SW_PATH`, `SYSROOT_PATH`, `PLATFORM_REPO_PATHS`, `BASE_PLATFORM`.
- Check generated-state mismatch: `Work/`, `.aie_target.*`, `_x/`, `*.xo`, `*.xsa`.
- Use `docs/CODEMAP_ours_192lane.md` before reading long files.
- If three fixes fail, stop and question the partition/stream architecture instead of stacking patches.
