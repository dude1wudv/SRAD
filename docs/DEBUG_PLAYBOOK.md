# Debug Playbook for `ours_192lane`

Use this before fixing compile, simulation, runtime, or performance problems.

## Rule

Do not patch from guesses. Reproduce, localize the layer, compare with a working path, write a failing check when possible, then fix.

## 1. Capture reproduction

Record:

```text
cwd:
command:
TARGET:
machine:
Vitis:
XRT:
BASE_PLATFORM:
first error line:
log path:
recent git diff:
```

## 2. Localize layer

- Python/data failure: `data/gen_case.py`, `data/verify_srad.py`, `data/test_sim_semantics.py`.
- AIE compile/sim failure: `aie/Config.h`, `aie/ProcessGraph/StencilCoreGraph.h`, `aie/ProcessUnit/*`, `Work/` logs.
- HLS kernel failure: `pl/TopPL.cpp`, `pl/Q0Ctrl.cpp`, `pl/*.cfg`, `hw.xo_dir/` or `sw_emu.xo_dir/` logs.
- V++ link/package failure: `conn.cfg`, `Makefile`, `_x/`, `*.xsa`, package logs.
- Host/XRT failure: `ps/host.cpp`, xclbin load, CU names, BO group IDs, board runtime logs.
- Performance regression: compare timing fields from `ps/host.cpp` output and record in `docs/journal/ours_192lane-evidence.md`.

## 3. Common checks

```bash
python scripts/check_ours_192lane.py
```

On Vitis machine:

```bash
cd variants/srad/ours_192lane
make clean
make data
make sim
make TARGET=hw sim
```

Clean only the active variant. Do not delete `research/` or `archive/`.

## 4. Fix discipline

- One hypothesis at a time.
- One smallest patch at a time.
- If touching `Config.h`, also check `conn.cfg`, graph, PL, host, generators, verifier, and tests.
- If three fixes fail, stop and question stream/partition architecture before continuing.
