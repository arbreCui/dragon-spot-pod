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
parameter; the same scalar would be applied to the complete state without
forming a mixed-unit state norm. No candidate or new map has been produced. See
[iterative/rank2_solver_decision.md](iterative/rank2_solver_decision.md).

Historical REAL64/B2 staging, GMRES/raw-MOC forensics, sensitivity probes,
numbered map continuations and Anderson scaffolding are not part of the active
gate. They remain recoverable from Git tag `archive-pre-lean-20260814`.
