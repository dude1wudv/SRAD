# Contributing

## Development Flow

1. Work inside the relevant variant directory.
2. Keep changes scoped to that variant unless intentionally syncing variants.
3. Run the narrowest useful check before committing.
4. Document toolchain assumptions and commands run in pull requests.

## Build Evidence

For Vitis/AIE changes, include:

- Affected variant path.
- Vitis/XRT/platform version when known.
- Commands run, for example `make data`, `make sim`, or `make all`.
- Whether generated artifacts were omitted or intentionally included.

## Style

- Match existing local formatting in touched files.
- Keep Makefile indentation as tabs.
- Preserve variant-local relative paths unless build files are updated together.
