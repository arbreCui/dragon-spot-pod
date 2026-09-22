# Corrected D4-A direct-Picard map 6

The sixth corrected-material rank-two map completed all three online radial
responses and the reduced axial solve with the unchanged `alpha=1` update.
The serial controller independently checked and froze it, then automatically
started map 7 from its portable `CLOSED/6` state.

| item | exact value |
|---|---|
| lifecycle | `CLOSED/5 -> PROJECTED/6 -> RETURNED/6 -> CLOSED/6` |
| classification | `VALID_NOT_MET` |
| portable role | `NEXT_MAP_PARENT_ONLY` |
| `R_rho` | `3.5088946733763393E-05` |
| `R_L` | `3.4738182352291766E-05` |
| `R_a` | `1.1538196291776131E-04` |
| SHA-256 of `result.sha256` | `e77ea7164382d7c834e496b038bebfa3759a2020b7f6cc20b396d631a8b7beab` |

Portable evidence:
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-001.portable`.
On 2026-09-22 its complete `result.sha256` passed verification and the
existing independent XSM checker and three-defect gate were replayed directly
from this directory. All six bitwise/physical checks passed; all three outer
defects remain above the unchanged `5e-7` threshold.

Radial CPU time was 18049 seconds; axial CPU time was 5 seconds. The largest
outer defect decreased from map 5's `3.4736134630042396E-04` to
`1.1538196291776131E-04`. This is observed progress, not a convergence claim
or a guarantee about future maps. No solver, physics, rank or threshold was
changed.

The series table now records global epoch 6. Its `map-002.raw` is the ongoing
global map 7, not an accepted result. There is still no corrected fixed-point
claim, final k/power result or independent CE comparison.
