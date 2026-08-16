# SPOT validation

The active validation tree follows the dependencies of the method:

| path | purpose |
|---|---|
| `level1/` | volume-weighted POD algebra and rank behavior |
| `level2/` | radial source, leakage sign, balance and final-source identities |
| `iterative/` | fixed-basis state, strict inner termination and one-map contracts |

Run the complete no-transport gate with:

```sh
make spot-fast
```

The gate launches no Dragon process. It checks the production method,
compiles the retained CLE-2000 and Fortran paths, and runs only seconds-scale
tests.

The generic continuation host is default-off. Enabling it evaluates one
unchanged direct map from the hash-locked parent and requires a new result
directory:

```sh
RUN_CONTINUATION=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_continuation_short.sh
```

It runs the radial and axial halves once each, with fixed process bounds and
no retry. It never updates the parent or starts another map automatically.

Current scientific status and the frozen x8 input provenance are in
[iterative/current_result.md](iterative/current_result.md) and
[iterative/current_parent.tsv](iterative/current_parent.tsv). The predeclared
three-way decision is in
[iterative/continuation_policy.md](iterative/continuation_policy.md).
The valid but unconverged final x8 publication hashes are tracked in
[iterative/x8_result.sha256](iterative/x8_result.sha256); the x7 receipt is
retained as its parent evidence. The full artifacts remain local and
Git-ignored. The direct rank-1 census is complete and no x9 is defined.
The hash-locked, no-Dragon x6--x8 residual-direction result is in
[iterative/residual_direction_result.md](iterative/residual_direction_result.md).
The solver-independent proposal/acceptance boundary and its exact-arithmetic
manufactured tests are in
[iterative/nonlinear_solver_contract.md](iterative/nonlinear_solver_contract.md).
They do not implement or run a real SPOT nonlinear solver.
The hash-locked real snapshot rank census is in
[iterative/rank_census_result.md](iterative/rank_census_result.md). It is an
offline representation diagnostic, not a rank qualification or transport
calculation.

The default-off rank-2 sensitivity host is frozen and compiles under the fast
gate.  Its first bounded run completed the radial half.  The host wrapper
reported a timeout, while the durable axial log establishes only entry into
`FLU` without a strict terminal or candidate state.  It is `INVALID_MAP`
(reported reason `TIMEOUT_BEFORE_TERMINAL`), not a convergence or physics
result; see
[iterative/rank2_map_attempt_result.md](iterative/rank2_map_attempt_result.md).

A default-off gate was frozen for a single axial-only operational attempt from
the hash-locked radial staging. It contains no radial solve or retry; the one
authorized run completed, passed its independent audit and is
`VALID_NOT_MET`. The valid map is rank-sensitivity evidence only. Its
420-second host limit was not a physical or empirical model parameter; see
[iterative/rank2_axial_only_result.md](iterative/rank2_axial_only_result.md).

That valid but tolerance-not-met map was then inspected offline, without
transport or another iteration. Its exact Gram partition shows that the
mode-2 diagonal term is
`0.775258` of the update numerator although it is only `3.5820e-5` of the
current state Gram-metric squared norm; the signed cross share is
`2.3466e-9`. This basis-dependent partition diagnoses one frozen update only;
see
[iterative/rank2_mode2_anatomy_result.md](iterative/rank2_mode2_anatomy_result.md).

A single direct rank-2 continuation was frozen as a separate default-off
stage. Its one authorized run consumed the valid candidate without
re-encoding, evaluated all radial and axial equations once, and passed the
independent `--continued` audit and receipt. It is `VALID_NOT_MET`: all three
stopping defects and diagnostic $D_L$ decreased, while the modal and
$G_{22}$-restricted mode-2 updates are strongly anti-aligned and shrink only
modestly. This is local evidence, not a convergence or cycle claim, and no
third map is defined. See
[iterative/rank2_next_map_result.md](iterative/rank2_next_map_result.md).

The ensuing no-transport solver decision selects only one modal-projected
Anderson(1) proposal in the full Gram-height metric. Its scalar is computed
from the two valid rank-2 modal residuals and is not a fitted relaxation
parameter; the same scalar is applied to the complete state without forming
a mixed-unit state norm. The proposal and its x2 raw-flux carrier have now
been deterministically materialized and independently checked. That
publication stage is `MATERIALIZED_PROPOSAL_NOT_EVALUATED`: by itself it
produced no fresh map or convergence result. See
[iterative/rank2_solver_decision.md](iterative/rank2_solver_decision.md) and
[iterative/rank2_modal_aa1_candidate_result.md](iterative/rank2_modal_aa1_candidate_result.md).

One separately authorized fresh map from that proposal has now completed.
The unchanged three-radial/one-axial chain and independent Ganlib audit pass,
but the classification is `VALID_NOT_MET`: the stopping defects are
`6.57635e-5`, `2.26566e-3` and `4.66468e-4`, versus `5.0e-7`. They are
smaller than the corresponding direct-second-map defects only for this local
comparison; no asymptotic, rank or physical-accuracy conclusion follows. The
stage ran once without retry and starts no next map; see
[iterative/rank2_modal_aa1_map_result.md](iterative/rank2_modal_aa1_map_result.md).

The two evaluated pairs have also been combined in one read-only next-history
AA(1) check. It gives the unique convex weight `0.9302745506696768` on the
latest output and passes the complete canonical publication preflight,
including 8880/8880 strictly positive reconstructed values. The resulting
proposal is now hash-locked and independently verified with a
`Z-RAW-FLUX` carrier. Its status is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`; no Dragon process or map was run. See
[iterative/rank2_modal_aa1_next_history_result.md](iterative/rank2_modal_aa1_next_history_result.md)
and
[iterative/rank2_modal_aa1_next_candidate_result.md](iterative/rank2_modal_aa1_next_candidate_result.md).

The separately authorized next map \(v=G_2(w_{\rm pub})\) has completed once
without retry. Its `proposal-z` parent gate, strict terminals, independent
checker and 21-entry receipt pass. It remains `VALID_NOT_MET`: the stopping
defects are `8.34905e-7`, `8.67273e-4` and `4.44166e-5`, all above `5.0e-7`.
No subsequent map was started; see
[iterative/rank2_modal_aa1_next_map_result.md](iterative/rank2_modal_aa1_next_map_result.md).

The subsequent read-only AA(1) history calculation uses the actual
\(y_{\rm pub}\to z\) and \(w_{\rm pub}\to v\) pairs. It gives the unique
unclipped weight `0.956973882871698711` on \(v\); the denominator, canonical
publication arithmetic and 8880-point positivity preflight pass. Its
proposal has now been hash-locked with a `V-RAW-FLUX` carrier. The independent
checker binds the complete AX and snapshot inventories to the latest returned
\(v\) lifecycle, with only published fields and declared stale removals
excepted. Its classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon process or new map was
produced. See
[iterative/rank2_modal_aa1_u_history_result.md](iterative/rank2_modal_aa1_u_history_result.md)
and
[iterative/rank2_modal_aa1_u_candidate_result.md](iterative/rank2_modal_aa1_u_candidate_result.md).

The separately authorized single map \(G_2(u_{\rm pub})\) has now completed
without retry. Its V-carrier preflight, strict terminals, independent checker
and 21-entry receipt pass. It is `VALID_NOT_MET`: the stopping defects are
`8.34905e-7`, `4.03982e-4` and `1.43357e-5`, all above `5.0e-7`. No automatic
successor was started; see
[iterative/rank2_modal_aa1_u_map_result.md](iterative/rank2_modal_aa1_u_map_result.md).

One later separately authorized direct Picard continuation from that returned
state also completed without retry. It remains `VALID_NOT_MET`, with stopping
defects `6.42235e-7`, `5.21752e-4` and `7.24633e-6`. The first and third
decreased, but the leakage defect increased by about 29.2%, so the adjacent
step is not componentwise monotone. No successor was started; see
[iterative/rank2_modal_aa1_u_next_map_result.md](iterative/rank2_modal_aa1_u_next_map_result.md).

The subsequent read-only REAL64 localization ran no Dragon. The \(R_L\)
scale is identical in both adjacent maps; the 29.1523% rebound comes entirely
from \(D_L\). Its unique hotspot moved from snapshot 1/group 328 with positive
increment to snapshot 1/group 326 with larger negative increment. This is local
oscillatory evidence only; see
[iterative/rank2_modal_aa1_u_leakage_localization_result.md](iterative/rank2_modal_aa1_u_leakage_localization_result.md).

Historical REAL64/B2 staging, GMRES/raw-MOC forensics and retired rank-1
Anderson scaffolding are not part of the active gate. They remain recoverable
from Git tag `archive-pre-lean-20260814`.
