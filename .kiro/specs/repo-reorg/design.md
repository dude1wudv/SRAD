# Repository Reorganization Design

## Target Layout

```text
.
|-- variants/
|   |-- srad/          # Main SRAD Vitis/AIE/CUDA variants
|   `-- stencilflow/   # Stencilflow experiment variants
|-- benchmarks/
|   `-- rtx4090/       # RTX4090 CUDA benchmark code
|-- research/
|   `-- sparta/        # SPARTA reference material and paper
|-- archive/
|   `-- srad-snapshot/ # Previous nested SRAD tree, kept as a source snapshot
|-- docs/
|-- scripts/
|-- .github/
`-- README.md
```

## Variant Policy

Each variant remains self-contained. Build commands still run from the variant directory, so variant-local relative paths such as `./data` keep working.

## Cleanup Policy

Remove:

- `.git` directories.
- Internal AI prompt/agent artifacts with local machine paths.
- Python `__pycache__` folders and bytecode.
- Vitis/XRT/AIE generated build directories.
- Generated `.txt`, `.log`, `.csv`, `.dat`, `.bin`, `.xclbin`, `.xo`, `.xsa`, and simulator outputs under variant data/build folders.

Keep:

- `Makefile`, `conn.cfg`, `xrt.ini`, `run.sh`.
- `aie/`, `pl/`, `ps/`, `data/*.py`, `tests/`, `README*`.
- Source files and small static docs.
