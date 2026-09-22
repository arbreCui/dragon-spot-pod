# Corrected D4-A map 8: axial current and returned leakage

2026-09-23. **DIAGNOSTIC_ONLY / REPORTED_ONLY.** Read-only saved-field check;
no transport, changed physics, relaxation, clipping or new acceptance threshold.
The corrected Picard chain remains unaccepted for convergence at map 8.

## Result

All **1110/1110** plane/group leakage coefficients reconstructed from actual
saved REAL64 axial face currents are **bitwise equal** to `SPOT-X-L`.
No nonpositive regional scalar flux or negative outward end current was found
in the 370-group fields. The existing track inventory has vacuum ends:
`NCODE=(1,1)`, `ZCODE=(0,0)`.

For each group, the sum of three layer current divergences agrees with bottom
plus top outward current to at most `7.589415207398531e-19` absolute, or
`9.318007909818866e-16` divided by the sum of absolute end outflows. This is a
reported floating-point cancellation scale, not a tolerance or fitted factor.
The 740 shared-face integral pairs are identical. All-energy outward totals,
in the archive's native flux normalization, are bottom `0.04510886549018021`
and top `0.04453889978128477`; they are not an absolute reactor power result.

**120 layer/group divergences are negative.** They mean net inflow to those
layers in those groups; none was clipped or converted to a positive loss.
Their signs do not conflict with positive total outward current at both ends.

## What was checked

The [Ganlib-only reader](diagnose_d4a_axial_current.f90) reads
`initial_axial_track.xsm` and `closed_axial.xsm` from corrected map 8:
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-003.portable`.
It uses `FLUX64`, actual `KEYFLX`, `AREA2D`, `VOL1D`, `MAT1D` and the face block
starting at `LL4=1188`; no REAL32 flux fallback is used. The arithmetic is

```
N(f,g) = sum_i A(i) * (J(f+1,i,g) - J(f,i,g))
D(f,g) = sum_i A(i) * H(f) * phi(f,i,g)
L(f,g) = N(f,g) / D(f,g)
```

Currents are signed in +z at every face. Thus bottom outward current is
`-sum(A*J_bottom)`, top outward current is `+sum(A*J_top)`.
`SPOSTATE` saves the REAL64 ratio to `SPOT-X-L`; B2J copies that new value into
the next equation's `LEAK1D64`. The closed radial archive's own `LEAK1D64`
retains the old value used to solve the preceding radial equation. New and old
leakage must **not** be required to agree before the fixed point is reached.

This establishes saved-current/feedback consistency. It does not independently
validate the SN angular solution, local 3D balance, POD accuracy, nuclear data
or convergence. The internal-face cancellation uses the same stored face on
both sides. No complete angle-resolved interface record was reconstructed.

## Short tests and evidence

The [synthetic test](test_d4a_axial_current.py) exercises the actual XSM reader:
1110 exact rows, reversed scalar indices, permuted layer/snapshot mapping,
signed end currents, and a REAL64 perturbation invisible in REAL32. A changed
saved leakage is reported as a mismatch, not silently replaced. Zero
denominator, invalid index/type and nonfinite field cases are rejected before
publishing output. Inputs stay unchanged; existing output cannot be overwritten.
Each compilation/program invocation has a 10-second limit.

```sh
python3 validation/iterative/test_d4a_axial_current.py
# With a separately built Ganlib-only host and an existing map directory:
(cd "$MAP8" && "$HOST" initial_axial_track.xsm closed_axial.xsm "$NEW_CSV")
```

Evidence: `validation/artifacts/d4a-axial-current-diagnostic-20260923` contains
the CSV, build/test logs, `map8_run.log`, and independent CSV arithmetic replay
and totals. All three map manifests verified before and after extraction.
Independent replay uses explicit sequential additions to reproduce Fortran
order, and `math.fsum` only for aggregate reporting.
CSV SHA-256: `b4688177f006aaa54fbd5d072a98f2912908d649708d76f1681326777b2b9601`.
