# Code Map: `variants/srad/ours_192lane`

Use this before reading long files. If a file is over 500 lines or 50KB, read targeted ranges/search hits only.

## Core constants and mapping

- `aie/Config.h:1-137`: single source of truth for board size, row blocks, lanes, PLIO merge shape, AIE placement, and `static_assert`s.
- `conn.cfg:1-274`: V++ CU count and stream wiring. Key facts: `TopPL:12`, `Q0Ctrl:1`, 192 input streams, 48 merged output streams, q0 stat/control streams.
- `pl/README.md:1-18`: human-readable 12-CU row/column split.

## AIE graph and kernels

- `aie/TopGraph.cpp:1-16`: simulator main and `graphOursPLQ0` instance.
- `aie/TopGraph.h:1-3`: graph extern.
- `aie/ProcessGraph/StencilCoreGraph.h:9-48`: one lane graph, local_q -> coeff_update, FIFO depths, dimensions.
- `aie/ProcessGraph/StencilCoreGraph.h:51-89`: 192-lane top graph, PLIO creation, 4-way pktmerge outputs.
- `aie/ProcessUnit/srad.h:1-84`: buffer types, optional vector helpers, kernel declarations.
- `aie/ProcessUnit/srad_local_q.cc`: local q stage math.
- `aie/ProcessUnit/srad_coeff_update.cc`: coefficient/update stage math and packet output.

## PL kernels

`pl/TopPL.cpp` is long; do not read it whole.

- `pl/TopPL.cpp:1-80`: compile-time assumptions and stream-size constants.
- `pl/TopPL.cpp:84-152`: float packing, worker id/row/column helpers, active iteration clamp.
- `pl/TopPL.cpp:157-181`: initial per-worker sum/sum2 stats.
- `pl/TopPL.cpp:183-228`: input forwarding and merged-output packet capture.
- `pl/TopPL.cpp:230-431`: load 16-lane DDR rows into AIE streams.
- `pl/TopPL.cpp:433-597`: decode/capture/store AIE output rows and row stats.
- `pl/TopPL.cpp:599-798`: output-row store and stats collection.
- `pl/TopPL.cpp:800-1083`: one strip-batch dataflow orchestration.
- `pl/TopPL.cpp:1085-1137`: worker iteration loop and ping-pong current/next buffers.
- `pl/TopPL.cpp:1139-1159`: final worker region copy.
- `pl/TopPL.cpp:1161-1165`: `extern "C" TopPL` HLS entry.

`pl/Q0Ctrl.cpp`:

- `pl/Q0Ctrl.cpp:1-22`: assumptions, debug slots.
- `pl/Q0Ctrl.cpp:24-66`: float unpack, q0 calculation, iteration clamp.
- `pl/Q0Ctrl.cpp:68-115`: debug write and stat stream reads.
- `pl/Q0Ctrl.cpp:117-148`: q0 broadcast to 12 TopPL CUs.
- `pl/Q0Ctrl.cpp:150-214`: `extern "C" Q0Ctrl` HLS entry and loop.

## Host

- `ps/host.cpp:31-45`: timing and iteration clamp.
- `ps/host.cpp:47-95`: input/output text IO.
- `ps/host.cpp:97-112`: kernel CU open fallback logic.
- `ps/host.cpp:114-145`: diagnostics and timing struct.
- `ps/host.cpp:147-348`: main XRT flow: load xclbin, register AIE, open 12 TopPL CUs, allocate BOs, run graph/Q0/TopPL, wait, timing, optional dump.

## Python data/check layer

- `data/gen_case.py:9-124`: parse `Config.h` into Python constants.
- `data/gen_case.py:126-192`: scalar SRAD reference math for generation.
- `data/gen_case.py:194-272`: PLIO/matrix writers and row-stream input construction.
- `data/gen_case.py:274-310`: stale cleanup and CLI.
- `data/verify_srad.py:12-88`: parse config and defaults.
- `data/verify_srad.py:90-236`: read/resolve/decode AIE packet outputs.
- `data/verify_srad.py:238-427`: golden SRAD reference and row-stream output construction.
- `data/verify_srad.py:429-485`: row-stream comparison.
- `data/verify_srad.py:487-520`: CLI.
- `data/test_sim_semantics.py`: fast regression tests for config, graph, Makefile, conn, host, packet merge, and verifier behavior; use targeted `Select-String` for test names.

## Build/test entrypoints

- `Makefile:1-263`: variant build. Bare `make sim` uses `TARGET=sw_emu`; `TARGET=hw sim` uses aiesimulator.
- `scripts/check_ours_192lane.py`: shared quick check runner.
- `scripts/test_check_ours_192lane.py`: tests the shared runner.
