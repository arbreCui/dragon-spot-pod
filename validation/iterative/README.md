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
instruction. A later nonlinear-solver study must use the same raw map and
must be declared separately. The immediate next check is only an offline
x6--x8 residual-direction audit; it launches no transport and fits no
coefficient.

The removed detailed validation history is recoverable from Git tag
`archive-pre-lean-20260814`.
