# Cleanup Policy

This repository keeps source, configs, tests, scripts, docs, and reference papers. It excludes local generated state.

Ignored or removable files include:

- Vitis/AIE build outputs: `Work/`, `Emulation-SW/`, `Emulation-HW/`, `_x/`, `.Xil/`, `package/`, `sd_card/`.
- Generated kernels/packages: `*.xo`, `*.xclbin`, `*.xsa`, `*.xclbin.info`.
- Simulator logs and traces: `*.log`, `*.jou`, `*.wdb`, `aiesimulator_output/`.
- Generated data files under `data/` and `board_data/`: `*.txt`, `*.csv`, `*.dat`, `*.bin`, `*.npy`, `*.npz`, `*.pgm`.
- Python caches: `__pycache__/`, `*.pyc`.

Use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/clean-generated.ps1
```
