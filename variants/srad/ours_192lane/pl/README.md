This directory contains the PL side of the Ours SRAD mapping.

Current board path:

- `TopPL.cpp` is instantiated twelve times.
- The twelve CUs form six row blocks by two column workers. Each `TopPL` owns
  16 AIE lanes and one contiguous 2000-column half image over a 667-row center
  block.
- `TopPL_0/1` handle center rows 0..666, `TopPL_2/3` handle rows 667..1333,
  `TopPL_4/5` handle rows 1334..2000, `TopPL_6/7` handle rows 2001..2667,
  `TopPL_8/9` handle rows 2668..3334, and `TopPL_10/11` handle padded rows
  3335..4001. Even worker IDs handle columns 0..1999; odd worker IDs handle
  columns 2000..3999.
- Each worker streams one north context row, 667 center rows, and two south
  context rows to AIE. Internal row-block boundaries are handled by rereading
  adjacent DDR rows as halo context.
- Padding rows beyond the real 4000-row image are consumed to keep the AIE stream
  shape uniform but are not written back and are not included in `sum/sum2`.
- `Q0Ctrl.cpp` aggregates the twelve local `sum/sum2` reports, computes one global
  `q0sqr` over `kBoardPixels`, and broadcasts that value back to all TopPL CUs.
