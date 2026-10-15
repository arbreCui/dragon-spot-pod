# Repaired 12-cell D4: same-operator terminal repeat — 2026-09-28

One isolated axial re-solve started from the completed CLOSED/6 flux, with
exact copies of its SYSTEM, TRACK and MACROLIB and the sealed repaired Dragon.
It completed in **1.78 seconds**, passing the original three inner tests at
`2e-6`. The result moved slightly from the previously accepted inner terminal.
This is an inner-repeatability diagnostic, not another coupled map.

| Quantity | Result |
| --- | ---: |
| Original map-6 k64 | 1.2847427149054287 |
| Repeated k64 | 1.2847430103542397 |
| Reactivity change, 1e5 (1/k_old - 1/k_repeat) | +0.01789987 pcm |
| Absolute inverse-k change | 1.7899867633e-7 |
| Relative leakage change | 3.3528108172e-7 |
| Gram/height modal-flux change | 5.6123669804e-7 |
| Final EEXT | 1.07573876e-7 |
| Final EUNK = EINR | 1.57318981e-6 |
| IEXTF / ITERF | 2 / 1 |

All physical coefficients, the fixed rank-two basis, 12-cell mesh, scattering,
EXTE 500, REBA OFF and ACCE 3 3 stayed unchanged. The only solve-input change
relative to the prior axial call is starting at its returned flux; logging was
increased to EDIT 1. No ASM or online radial solve was invoked. UTL removed
the copied lifecycle state/epoch markers as in the production restart, and
SPOSTATE/SPOXCONV reported the same canonical norms after the solve.

The modal change is **1.12247 times** the numerical outer Ra threshold, while
the k and leakage changes are smaller than their respective outer thresholds.
That is a comparison of scales, not an outer gate applied to a coupled map.
It shows that one inner PASS does not freeze the returned modal state to the
outer accuracy scale. It does not establish an error floor, prove that the
coupled gate is unreachable, or separate restart quantization from finite
inner stopping error. No tolerance or current-runtime parameter was changed.

The k movement is tiny compared with the approximately -1096 pcm CE difference.
The old three-cell cold/warm discrepancy of 0.48144 pcm is a different experiment;
this twelve-cell warm repeat neither reproduces nor cancels that result.

## Execution and retained evidence

The first setup was rejected before any solve because the private deck named
its macrolib `MAC` whereas the saved SYSTEM required `MACROLIB3`. Its failed
log is preserved; it has no scientific result. A fresh subdirectory corrected
only the CLE object identifiers to the original names. It completed under a
590-second cap, within the 600-second study allowance. There was one actual
axial solve and no continuation or automatic repetition afterward.

Evidence: `validation/artifacts/d4a-map6-axial-repeat-20260928/`, including
both setup logs, exact decks, input hashes, saved repeated axial state,
terminal records and `execution.json`. All copied and original input/runtime
hashes remained unchanged. The independent running Picard calculation and its
control files were not edited or signalled.

Next, pair this frozen-operator result with a cold solve and an independently
bounded tighter-inner comparison, keeping mesh/rank/operator fixed. Report
normalized modal and physical flux plus leakage, not only k. Those additional
solves have not been performed by this diagnostic.
