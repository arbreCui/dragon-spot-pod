# Active iterative validation

This directory contains the direct fixed-space SPOD/Picard contracts and one
generic, default-off continuation host.

## Active files

- `check_source_identity.py`: frozen-fission source and returned-source
  identity.
- `check_fixed_basis_contract.py`: fixed POD package and live radial response.
- `check_state_contract.py`, `test_state_math.py`: canonical
  $x=(a,1/k,L)$ state and the three raw defects.
- `test_spot_strict_inner.py`: fail-closed radial and axial terminal rules.
- `test_picard_control.py`: direct substitution and three-component AND stop.
- `nonlinear_solver_contract.md`, `test_nonlinear_solver_contract.py`:
  solver-independent acceptance and an exact-Newton synthetic reference.
- `check_rank_census_xsm.f90`, `run_rank_census.sh`,
  `rank_census_result.md`: hash-locked real snapshot-spectrum census.
- `build_rank2_basis_xsm.f90`, `check_rank2_basis_xsm.f90`,
  `run_rank2_basis.sh`, `rank2_basis_result.md`: production-convention,
  no-transport rank-2 reconstruction and independent audit.
- `continuation_rank2_radial.x2m`, `continuation_rank2_axial.x2m`,
  `run_rank2_map.sh`, `rank2_parent.tsv`, `rank2_map_policy.md`,
  `test_rank2_map_contract.py`: default-off single rank-sensitivity map.
- `rank2_map_attempt_result.md`: first bounded attempt and its strict
  `INVALID_MAP` evidence boundary.
- `run_rank2_axial_only.sh`, `rank2_axial_only_parent.tsv`,
  `rank2_axial_only_policy.md`, `test_rank2_axial_only_contract.py`: one
  default-off second operational attempt that reuses the frozen radial half.
- `rank2_axial_only_result.md`: valid rank-2 map, raw defects and the strict
  `VALID_NOT_MET` interpretation boundary.
- `rank2_mode2_anatomy_result.md`: no-Dragon, exact Gram partition of the
  archived rank-2 update into mode-1, mode-2 and signed coupling terms.
- `continuation_rank2_continued_radial.x2m`, `run_rank2_next_map.sh`,
  `rank2_next_parent.tsv`, `rank2_next_map_policy.md`,
  `test_rank2_next_map_contract.py`: one default-off direct rank-2 continued
  map from the valid but tolerance-not-met candidate, with no automatic third
  map.
- `rank2_next_map_result.md`: valid second rank-2 map, exact raw defects and
  the read-only two-update direction boundary.
- `rank2_solver_decision.md`: no-Dragon selection and real-data coefficient
  for one modal-projected Anderson(1) proposal using the full Gram metric.
- `rank2_modal_aa1_inputs.tsv`, `build_rank2_modal_aa1_candidate.f90`,
  `check_rank2_modal_aa1_candidate.f90`,
  `run_rank2_modal_aa1_candidate.sh`,
  `test_rank2_modal_aa1_candidate_contract.py`,
  `rank2_modal_aa1_candidate_result.md`: hash-locked offline publication and
  independent audit of that one proposal.
- `rank2_modal_aa1_map_parent.tsv`, `rank2_modal_aa1_map_policy.md`,
  `run_rank2_modal_aa1_map.sh`, `test_rank2_modal_aa1_map_contract.py`,
  `rank2_modal_aa1_map_result.md`: one default-off fresh strict map from the
  proposal, with no retry or automatic successor.
- `rank2_modal_aa1_next_history.tsv`,
  `rank2_modal_aa1_next_history_result.md`: hash-locked read-only AA(1)
  update from the two evaluated pairs.
- `rank2_modal_aa1_next_candidate_inputs.tsv`,
  `run_rank2_modal_aa1_next_candidate.sh`,
  `rank2_modal_aa1_next_candidate_result.md`: deterministic no-Dragon
  publication and independent audit of that next proposal; no new map.
- `rank2_modal_aa1_next_map_parent.tsv`,
  `rank2_modal_aa1_next_map_policy.md`,
  `run_rank2_modal_aa1_next_map.sh`,
  `rank2_modal_aa1_next_map_result.md`: strict pre-Dragon `Z-RAW-FLUX` gate
  and the one completed, no-retry map from the next proposal.
- `rank2_modal_aa1_u_history.tsv`,
  `rank2_modal_aa1_u_history_result.md`: latest read-only AA(1) history from
  the two evaluated proposal maps.
- `rank2_modal_aa1_u_candidate_inputs.tsv`,
  `run_rank2_modal_aa1_u_candidate.sh`,
  `rank2_modal_aa1_u_candidate_result.md`: deterministic no-Dragon
  publication with an independently audited `V-RAW-FLUX` lifecycle; no map.
- `rank2_modal_aa1_u_map_parent.tsv`,
  `rank2_modal_aa1_u_map_policy.md`,
  `run_rank2_modal_aa1_u_map.sh`,
  `rank2_modal_aa1_u_map_result.md`: exact `V-RAW-FLUX` preflight and the one
  completed, no-retry map from the latest proposal.
- `rank2_modal_aa1_u_next_parent.tsv`,
  `rank2_modal_aa1_u_next_map_policy.md`,
  `rank2_modal_aa1_u_next_map_result.md`: one direct, no-retry Picard
  continuation from that valid returned state using the generic host.
- `rank2_modal_aa1_u_leakage_localization_result.md`: no-Dragon REAL64
  localization of the two adjacent leakage defects, scales, hotspots and
  signs.
- `run_bounded_dragon.py`, `test_bounded_dragon.py`: bounded process-group
  handling.
- `continuation_radial.x2m`, `continuation_axial.x2m`,
  `run_continuation_short.sh`: one unchanged direct continuation.
- `check_one_map_xsm.f90`: Ganlib-only one-map, continued-map, three-state
  residual-direction and archived rank-2 modal checker.
- `run_residual_direction_audit.sh`, `residual_direction_inputs.tsv`,
  `residual_direction_result.md`: hash-locked x6--x8 read-only audit.
- `current_parent.tsv`: the six role- and hash-locked parent objects.
- `continuation_policy.md`, `test_continuation_contract.py`: frozen
  decision and static host contract.
- `current_result.md`, `x7_result.sha256`, `x8_result.sha256`: concise final
  boundary, parent receipt and final publication receipt.

## Fast gate

```sh
make spot-fast
```

This performs no transport calculation. It compiles and statically checks the
proposal builder and checker, but does not materialize the real-data proposal.

## Generic continuation

The host is default-off. It uses three online radial fixed-source solves, one
axial solve, strict terminal checks, and an independent Ganlib-only audit.

```sh
RUN_CONTINUATION=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_continuation_short.sh
```

The runner validates the six parent hashes, launches each half once, validates
the independent checker, then publishes a candidate and receipt. It has no
retry, does not overwrite a result, does not update the parent and never
starts the next map.

## Rank-2 sensitivity map

The rank-2 host is also default-off:

```sh
RUN_RANK2_MAP=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_rank2_map.sh
```

It canonicalizes the same raw x7 axial field in the rank-2 basis before the
map.  It does not zero-fill a coefficient or rerun the rank-1 reference.

The first attempt completed and retained the radial staging, but the axial
host reported an 80-second timeout before any strict terminal record.  It is
therefore `INVALID_MAP` (reported reason `TIMEOUT_BEFORE_TERMINAL`): no rank-2
defects, convergence result or accuracy claim exist, and no result directory
was published.  The timeout line is a labelled host-output transcription;
the durable axial log independently establishes only the missing terminal and
normal end.  See
[rank2_map_attempt_result.md](rank2_map_attempt_result.md).

The separately authorized axial-only host is also default-off:

```sh
RUN_RANK2_AXIAL_ONLY=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_rank2_axial_only.sh
```

It verifies and copies the frozen radial staging, runs no radial equation,
starts the unchanged axial deck exactly once under a 420-second host bound,
and requires the same independent `--reencoded` audit before publication.
The one authorized run completed and passed every validity gate. Its
classification is `VALID_NOT_MET`: all three stopping-rule defects exceed
`5.0e-7`. The first operational attempt remains `INVALID_MAP`; see
[rank2_axial_only_result.md](rank2_axial_only_result.md). The completed run
does not authorize a rerun or the next Picard map.

The same valid map has now been decomposed offline in its stored Gram metric.
The mode-2 diagonal term is only `3.5820e-5` of the current state Gram-metric
squared norm but is `0.775258` of this update numerator; the signed Gram
coupling share is only `2.3466e-9`. This is a basis-dependent exact anatomy
of one frozen update, not evidence of instability, rank adequacy or physical
accuracy. See
[rank2_mode2_anatomy_result.md](rank2_mode2_anatomy_result.md).

One next direct map is now frozen separately as
$x^{(2)}_2=G_2(x^{(2)}_1)$. It consumes the valid rank-2 candidate without
re-encoding it, reruns all three online radial equations, then uses the
unchanged axial deck and the independent `--continued` checker. Its host is
default-off and allows one 120-second radial launch and one 420-second axial
launch, with no retry:

```sh
RUN_RANK2_NEXT_MAP=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_rank2_next_map.sh
```

These are operational process limits, not physical or convergence
parameters. The host never starts a third rank-2 map.

The one authorized run completed and passed its independent audit and full
receipt. It remains `VALID_NOT_MET`: all three stopping defects and diagnostic
$D_L$ decreased, but the stopping defects still exceed the tolerance.
Offline, the full modal updates have norm ratio `0.864118` and cosine
`-0.874929`; the basis-dependent, $G_{22}$-restricted mode-2 updates have
ratio `0.932560` and cosine `-0.915973`. They are locally strongly
anti-aligned, not proof of a cycle, convergence or divergence. See
[rank2_next_map_result.md](rank2_next_map_result.md).

No third direct map is defined. The next solver study instead freezes one
modal-projected Anderson(1) coefficient in the full Gram-height metric from
the two valid rank-2 updates. Its latest-state weight is
`0.5388643265136009`; it is computed, unclipped and applied as one scalar to
the complete state. No mixed-unit state norm or blockwise coefficient is
introduced. The published AX proposal and x2 raw-flux snapshot carrier pass
an independent Ganlib-only audit, including 8880/8880 strictly positive
REAL32 reconstructions. Their classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`; within that publication stage the
affine screen is not an acceptance test and no Dragon run or new map exists.
See
[rank2_solver_decision.md](rank2_solver_decision.md) and
[rank2_modal_aa1_candidate_result.md](rank2_modal_aa1_candidate_result.md).

With the local hash-locked inputs present, materialize into a fresh artifact
directory with:

```sh
make spot-rank2-modal-aa1-candidate
```

The separately authorized fresh map from this proposal has also completed.
It passed the three radial terminals, axial terminal, independent
`--proposal` audit and receipt, but is `VALID_NOT_MET`:

\[
(R_\rho,R_L,R_a)=
(6.5763515\times10^{-5},\,2.2656585\times10^{-3},\,
4.6646819\times10^{-4}).
\]

All three exceed `5.0e-7`. They are locally smaller than the corresponding
defects from the direct second rank-2 map, but this single cross-input
comparison is not an asymptotic convergence or accuracy claim. See
[rank2_modal_aa1_map_result.md](rank2_modal_aa1_map_result.md).

The map host remains default-off and refuses to overwrite an existing result:

```sh
RUN_RANK2_MODAL_AA1_MAP=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_rank2_modal_aa1_map.sh
```

The completed experiment does not authorize rerunning this target or starting
a subsequent map.

The next history decision is also complete without Dragon. It uses the
correct residual pairs

\[
p=x_2-x_1,\qquad q=z-y_{\rm pub},
\]

and combines their corresponding map outputs, not their inputs:

\[
w=(1-\beta_z)x_2+\beta_z z,
\qquad \beta_z=0.9302745506696768.
\]

The unique coefficient is naturally convex and the publication preflight has
8880/8880 strictly positive `B2a` values. The proposal has now been
deterministically materialized with the audited `z` carrier. Its independent
Ganlib checker verifies the affine publication, complete non-leakage snapshot
payload, lagged SYSTEM and strict positivity. The classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`; see
[rank2_modal_aa1_next_history_result.md](rank2_modal_aa1_next_history_result.md)
and
[rank2_modal_aa1_next_candidate_result.md](rank2_modal_aa1_next_candidate_result.md).
The proposal publication itself contains no map.

With the local hash-locked parents present, the no-Dragon materialization is:

```sh
make spot-rank2-modal-aa1-next-candidate
```

The target refuses to overwrite the frozen local artifact.

The corresponding one-map host remains default-off:

```sh
make spot-rank2-modal-aa1-next-map
```

It prints the default-off terminal without reading the repository or starting
Dragon. Its separately authorized single attempt has completed with no retry.
The map is valid, but

\[
(R_\rho,R_L,R_a)=
(8.3490452\times10^{-7},\,8.6727309\times10^{-4},\,
4.4416561\times10^{-5}),
\]

so all three stopping defects exceed `5.0e-7` and the classification is
`VALID_NOT_MET`. No subsequent map was started or authorized. See
[rank2_modal_aa1_next_map_result.md](rank2_modal_aa1_next_map_result.md).

The latest no-Dragon history calculation now uses the actual pairs
\(y_{\rm pub}\to z\) and \(w_{\rm pub}\to v\). In the same full modal
Gram-height metric it gives

\[
\beta_v=0.956973882871698711,
\qquad
u=0.0430261171283013z+0.956973882871699v.
\]

The denominator is strictly positive and the canonical publication preflight
has 8880/8880 strictly positive reconstructed values. The affine modal screen
is `0.882410` of the latest known residual norm, but it is not a new map
residual or convergence factor. The resulting proposal has now been
deterministically materialized from the latest returned \(v\) carrier. Its
independent checker recursively binds all unchanged AX/snapshot payload,
proves the \(w_{\rm pub}\to v\) lifecycle and verifies 8880/8880 strictly
positive published reconstructions. The classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`; no Dragon or map was run. See
[rank2_modal_aa1_u_history_result.md](rank2_modal_aa1_u_history_result.md)
and
[rank2_modal_aa1_u_candidate_result.md](rank2_modal_aa1_u_candidate_result.md).

With all frozen local inputs present, reproduce this no-transport stage into
a fresh artifact directory with:

```sh
make spot-rank2-modal-aa1-u-candidate
```

The corresponding one-map host is prepared but default-off:

```sh
make spot-rank2-modal-aa1-u-map
```

Its `V-RAW-FLUX` preflight precedes any Dragon launch. The separately
authorized single attempt has now completed with no retry. The map is valid,
but

\[
(R_\rho,R_L,R_a)=
(8.3490525\times10^{-7},\,4.0398154\times10^{-4},\,
1.4335690\times10^{-5}),
\]

so all three stopping defects exceed `5.0e-7` and the classification is
`VALID_NOT_MET`. No automatic successor was started. See
[rank2_modal_aa1_u_map_result.md](rank2_modal_aa1_u_map_result.md).

One later separately authorized direct Picard continuation from the returned
state has also completed exactly once. It remains `VALID_NOT_MET`:

\[
(R_\rho,R_L,R_a)=
(6.4223464\times10^{-7},\,5.2175156\times10^{-4},\,
7.2463300\times10^{-6}).
\]

Relative to the preceding map, \(R_\rho\) and \(R_a\) decreased by about
23.1% and 49.5%, while \(R_L\) increased by about 29.2%. The adjacent defects
are not componentwise monotone and establish neither convergence nor
divergence. No successor map was started. See
[rank2_modal_aa1_u_next_map_result.md](rank2_modal_aa1_u_next_map_result.md).

The subsequent no-Dragon REAL64 localization found identical \(R_L\) scales
in the two adjacent maps. The unique \(D_L\) hotspot moved from snapshot 1/group
328 with positive increment to snapshot 1/group 326 with a larger negative
increment. Thus the 29.1523% rebound comes from the leakage change itself,
not the normalization scale. This is local oscillatory evidence, not proof of
a two-cycle or its cause; see
[rank2_modal_aa1_u_leakage_localization_result.md](rank2_modal_aa1_u_leakage_localization_result.md).

## Current boundary

Direct rank-1 Picard has valid maps through the predeclared final x8, but has
not converged. The final defects are

$$
(R_\rho,R_L,D_L,R_a)=
(6.4057634863\times10^{-8},\,
3.7849611670\times10^{-4},\,
5.5495183915\times10^{-7}\ \mathrm{cm}^{-1},\,
2.6731297644\times10^{-7}).
$$

The predeclared result is `VALID_NOT_MET`: only $R_L$ fails, at
756.992233 times the outer tolerance. The x8 publication receipt hashes are
tracked in [x8_result.sha256](x8_result.sha256); the 443 MB artifact remains
local and Git-ignored.

One real leakage-Anderson candidate made $R_L$ and $R_a$ worse and was
rejected. See [current_result.md](current_result.md).

Stop after x8. The direct rank-1 census is complete; no x9 is defined. The
retained x7 parent manifest records the exact input to x8 and is not a next-map
instruction.

The offline x6--x8 direction audit is complete. The leakage updates are nearly
opposite in an explicitly non-production height-$L_2$ diagnostic
($c_L=-0.969649$); the production $D_L$ hotspot is uniquely plane 3/group 325
in both updates and reverses sign. The modal Gram-height cosine is
$c_a=-0.314863$. This motivates a separately declared nonlinear-solver study
but neither selects a solver nor establishes a cycle or divergence. See
[residual_direction_result.md](residual_direction_result.md).

The next solver boundary is now frozen in
[nonlinear_solver_contract.md](nonlinear_solver_contract.md). Every proposed
state must be evaluated by the unchanged real map and pass the same three raw
defects; no linear prediction or combined norm can accept it. Full exact
Newton is tested only as a parameter-free manufactured-problem oracle. The
real SPOT map has no validated exact Jacobian, so no production Newton or
JFNK implementation and no new transport run are authorized. The minimal
finite-difference probe now gives quotients $0$, $1$ and $4/3$ for the same
linear direction under three binary32-scale perturbations. This is a local
publication-resolution counterexample, not a general rejection of JFNK.

The no-transport rank census is also complete. The frozen basis reference
retains all three singular values in every group, so rank-1/rank-2 optimal
snapshot errors were computed without reading the raw 218 MiB snapshots.
Rank 1 has worst within-group error 1.5004%, while rank 2 has worst error
0.03408%; all 370 groups have numerical rank 3. This is `DIAGNOSTIC_ONLY` and
does not attribute Picard failure to rank or authorize a rank change. See
[rank_census_result.md](rank_census_result.md).

The next representation-only step is also complete: the genuine second mode
has been rebuilt from those same original snapshots with production
`SPOPOD`/`ALSVDF`. A fresh rank-1 control, the rank-2 mode-1 prefix, stored
diagnostics and duplicate rank-2 files all agree bitwise under their declared
checks. The local rank-2 package remains inactive and Git-ignored. This is
`OFFLINE_RECONSTRUCTION_ONLY`; the later single-map attempt did not complete
the axial half and therefore does not promote this basis to a validated
rank-2 map. See [rank2_basis_result.md](rank2_basis_result.md) and
[rank2_map_attempt_result.md](rank2_map_attempt_result.md).

The removed detailed validation history is recoverable from Git tag
`archive-pre-lean-20260814`.
