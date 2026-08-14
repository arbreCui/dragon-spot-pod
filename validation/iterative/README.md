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
- `run_bounded_dragon.py`, `test_bounded_dragon.py`: bounded process-group
  handling.
- `continuation_radial.x2m`, `continuation_axial.x2m`,
  `run_continuation_short.sh`: one unchanged direct continuation.
- `check_one_map_xsm.f90`: Ganlib-only one-map and continued-map checker.
- `current_parent.tsv`: the six role- and hash-locked parent objects.
- `continuation_policy.md`, `test_continuation_contract.py`: frozen
  decision and static host contract.
- `current_result.md`: concise current boundary.

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

## Current boundary

Direct rank-1 Picard has valid maps through $x_6$, but has not converged.
The current defects are

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,2.0941536233\times10^{-4},\,
3.0704541132\times10^{-7}\ \mathrm{cm}^{-1},\,
7.5835881646\times10^{-7}).
$$

One real leakage-Anderson candidate made $R_L$ and $R_a$ worse and was
rejected. See [current_result.md](current_result.md).

The continuation host and its three-way decision rule are now frozen. The
next scientific action is a separately authorized, unchanged
$x_7=G(x_6)$, bounded and without retry. That one datum cannot alone prove
convergence or divergence. No further numbered deck should be added and no
$x_8$ is automatic.

The removed detailed validation history is recoverable from Git tag
`archive-pre-lean-20260814`.
