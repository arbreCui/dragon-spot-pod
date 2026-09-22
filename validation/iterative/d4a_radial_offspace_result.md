# Corrected D4-A: online radial projection diagnostic

2026-09-23. **DIAGNOSTIC_ONLY / REPORTED_ONLY.** The saved corrected
maps 6–8 are all `VALID_NOT_MET`. This calculation does not advance Picard,
qualify a rank, or establish physical accuracy.

## Result

The part of the actual online radial field outside the fixed rank-two space
is approximately **0.0312% in the stated global weighted flux norm**, stable
over the three saved maps:

| corrected map | relative offspace norm | percent |
|---|---:|---:|
| 6 | 3.1132194397181308e-4 | 0.0311322% |
| 7 | 3.1246930355265345e-4 | 0.0312469% |
| 8 | 3.1210258637868636e-4 | 0.0312103% |

At map 8, the bottom/middle/top ratios are respectively
`2.8004288048489418e-4`, `3.3186948859952623e-4`, and
`2.6746506828711190e-4`. The largest single plane/group ratio is about
`2.79647%` at plane 1/group 363, but that bin contributes only
`2.0035309106288589e-25` of the global **squared flux norm**. It is not a
representative global error, power fraction, or importance measure.

This is a description of the represented radial shapes, not a bound on
`k`, reaction rates, pin-power error, or the solution of a different-rank
coupled problem. The diagnostic must not be compared with the `5e-7`
Picard stopping threshold: they measure different quantities. The basis,
rank, physical operator and stopping gate are unchanged.

## Source and calculation

The field is the saved REAL64
`candidate_radial.xsm/FLUX[plane]/SPOT-R64/FLUX[group]`, restricted to the
132 physical regions by `TRACK/KEYFLX`. It is not the reconstructed axial
field or the already stored `SPOT-X-PERP`. Candidate and closed-archive
radial fields agree bit-for-bit over all 144 unknowns, 370 groups and three
planes. The REAL32 mirrors also agree with the cast REAL64 authority.

`B` is the frozen REAL32 `POD-BASIS`, promoted to REAL64;
`W = diag(VOL2D / sum(VOL2D))`. The full stored Gram matrix is independently
recomputed in the production arithmetic order and matches bit-for-bit.
For each plane `p` and group `g`:

```text
G = B^T W B
a = G^(-1) B^T W u
E[p,g]^2 = (u - B a)^T W (u - B a)
N[p,g]^2 = u^T W u
overall = sqrt(sum[p,g] H[p] E[p,g]^2 / sum[p,g] H[p] N[p,g]^2)
```

`H` comes from `SPOT-X-H` (50 cm per plane here). This is a norm of the
current 370 group-integrated flux values; it is not an energy or
reaction-rate norm. No flux rescaling, empirical weighting, denominator
floor, or accuracy threshold is introduced. Zero-norm ratios, if present,
are labelled undefined (`-1`), not silently set to zero error.

The source directories are `map-001.portable` through `map-003.portable`
under `validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922`.
Each complete manifest verified before and after extraction. Output is in
`validation/artifacts/d4a-radial-offspace-diagnostic-20260923`: 1110
plane/group rows per map, summaries, and input verification records.

## Short reproduction

Only a stand-alone Ganlib reader is compiled; never rebuild `src` or the
running Dragon. Put the executable in a fresh temporary directory. With
`R` the checkout and `BIN` the new executable path:

```sh
gfortran -std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals \
  -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$R/Ganlib/lib/Darwin_arm64/modules" \
  "$R/validation/iterative/diagnose_d4a_radial_offspace.f90" \
  "$R/Ganlib/lib/Darwin_arm64/libGanlib.a" -lstdc++ -o "$BIN"
python3 "$R/validation/iterative/test_d4a_radial_offspace.py" "$BIN"
# MAP is a verified portable input; EPOCH matches its stored epoch.
# PREFIX names new diagnostic outputs outside MAP. Use short XSM paths.
(cd "$MAP" && "$BIN" . "$EPOCH" "$PREFIX")
```

The actual compile and each program invocation were limited to 10 seconds.
Synthetic checks cover a non-unit/non-diagonal Gram matrix with an exactly
known offspace component, an in-space field, amplitude scaling, zero field,
and invalid inputs; all seven checks passed. An independent CSV aggregation
of the 3330 unique plane/group rows reproduces the displayed overall ratios
without changing normalization. No Dragon, tracking, OpenMC or transport
run is needed.
