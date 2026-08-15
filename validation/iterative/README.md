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

This performs no transport calculation.

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
the complete state. No mixed-unit state norm, blockwise coefficients,
candidate file or Dragon run is added. The affine modal screen is not an
acceptance test; see
[rank2_solver_decision.md](rank2_solver_decision.md).

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
