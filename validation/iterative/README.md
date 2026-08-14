# Active iterative validation

This directory now contains only the direct fixed-space SPOD/Picard contracts
and one retained map replay.

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
- `one_map_radial.x2m`, `one_map_axial.x2m`,
  `run_one_map_short.sh`: frozen $x_0\to x_1$ replay.
- `check_one_map_xsm.f90`: Ganlib-only one-map and continued-map checker.
- `seed.sha256`, `one_map_scientific.sha256`: retained replay inputs.
- `current_result.md`, `current_parent.sha256`: concise current boundary.

## Fast gate

```sh
make spot-fast
```

This performs no transport calculation.

## Retained real-map replay

The replay is default-off. It uses three online radial fixed-source solves,
one axial solve, strict terminal checks, and an independent Ganlib-only audit.

```sh
RUN_ONE_MAP=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
SEED_DIR=/absolute/path/to/iterative-seed \
X0_DIR=/absolute/path/to/iterative-map1 \
  sh validation/iterative/run_one_map_short.sh
```

The runner has no retry and does not assess outer convergence. It is retained
as a reproducible map fixture, not as the future iteration host.

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

The next implementation task is one generic continuation host. Freeze its
continuation/stop criterion, then run one unchanged $x_7=G(x_6)$,
default-off, bounded and without retry. That one datum cannot alone prove
convergence or divergence. No further numbered deck should be added.

The removed detailed validation history is recoverable from Git tag
`archive-pre-lean-20260814`.
