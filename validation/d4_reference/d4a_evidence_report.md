# D4-A saved-evidence report

Repaired scattering, fixed rank 2, three physical zones / twelve axial cells; maps 1–9 completed through 2026-09-29 01:33 Asia/Shanghai, with CLOSED/9 final saved-output diagnostics on 2026-09-29. Map-7/8 leakage/pin diagnostics are not evaluated. Later or running maps are intentionally excluded.

Generated from an explicitly selected completed prefix; this is a dated diagnostic,
not live run status or final physical acceptance. No transport is performed.

CE k = 1.303084888393; sigma = 19.55037 pcm;
existing k comparison budget = 558.65111 pcm.

The signed difference is 1e5 (1/k_CE - 1/k_SPOT); negative means SPOT is lower.

| Map | Rrho | Rleak | Ra | CE difference (pcm) | Leakage excess (percentage points) | Pin max / RMS (%) | Wall (h) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | 2.04333e-03 | 1.13691e-01 | 7.19513e-03 | -1143.92669 | 1.482537 | 2.11097 / 0.91734 | 4.439 |
| 2 | 6.39763e-04 | 1.49518e-02 | 1.76808e-03 | -1079.95038 | 1.499289 | 2.02936 / 0.90171 | 4.089 |
| 3 | 2.01221e-04 | 1.84426e-03 | 5.72090e-04 | -1100.07246 | 1.495170 | 2.05402 / 0.90653 | 4.154 |
| 4 | 5.69383e-05 | 3.72527e-04 | 1.84938e-04 | -1094.37862 | 1.496587 | 2.04565 / 0.90485 | 4.081 |
| 5 | 1.19426e-05 | 5.49844e-05 | 6.04892e-05 | -1095.57288 | 1.496211 | 2.04798 / 0.90527 | 4.095 |
| 6 | 5.20953e-07 | 1.63844e-05 | 1.96005e-05 | -1095.62498 | 1.496293 | 2.04715 / 0.90509 | 4.049 |
| 7 | 6.08292e-07 | 2.90850e-06 | 5.46714e-06 | -1095.56415 | not evaluated | not evaluated | 4.166 |
| 8 | 5.65871e-09 | 1.07395e-06 | 9.04997e-07 | -1095.56471 | not evaluated | not evaluated | 4.111 |
| 9 | 2.91194e-08 | 2.98318e-07 | 3.64179e-07 | -1095.56180 | 1.496292 | 2.04726 / 0.90509 | 4.162 |

Latest selected classification: **VALID_MET**.
All three outer defects must independently satisfy 5e-7.

Latest radial/axial CPU: **14942 / 1 seconds**.
Completed-prefix wall time: **37.347 hours**
(excludes snapshot construction, bootstrap and earlier experiments).

The last map changes reactivity by 0.00291 pcm,
while its CE difference remains -1095.56180 pcm.
These are observed differences, not a bound on future iterations or an error decomposition.

Optional leakage/pin diagnostics omitted from the input selection are marked not evaluated;
they are never filled with zero or borrowed from another map. Declared inputs still must verify.
Pin quantities are globally normalized nu-fission fractions, not thermal power.
The maximum and unweighted RMS relative differences include CE sampling noise.
No normalized-fraction covariance or shape-accuracy verdict is inferred.

Regenerate with `make spot-evidence`; `--json` emits computed values and input hashes.
The tool checks only files it consumes against existing manifests and binds map
identity to the saved reviews. It does not rerun checkers or the full lineage audit.

See the [experiment matrix](../../SPOT_doc/validation_plan.md),
[current handoff](../iterative/d4a_final_validation_handoff.md), and
[acceptance matrix](../iterative/d4a_corrected_acceptance_matrix.md).
