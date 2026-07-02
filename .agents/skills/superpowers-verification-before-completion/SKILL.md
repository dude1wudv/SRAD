---
name: superpowers-verification-before-completion
description: Project-local copy of the Superpowers verification skill. Use before claiming an SRAD change is done, fixed, passing, or ready for commit/PR.
---

# Superpowers Verification Before Completion

Iron law: evidence before claims.

Before saying fixed/done/passing:

1. Identify the command that proves the claim.
2. Run it fresh in this turn/session.
3. Read the exit code and output.
4. Report the exact command and result.

## SRAD default verification

- Always run: `python scripts/check_ours_192lane.py`.
- If Vitis/make is available and the change touches AIE/PL/PS/build wiring: `python scripts/check_ours_192lane.py --sim` or `make sim` from the variant.
- If claiming hardware readiness: record `make TARGET=hw sim` or `make all` evidence from the VCK190/Vitis machine.

No previous run, no assumed pass, no partial output as success.
