# Corrected D4-A map 8: saved radial operator balance

2026-09-23. **DIAGNOSTIC_ONLY / REPORTED_ONLY.** No transport was run and no
physics, rank, coefficient or convergence threshold changed. This checks the
already saved, group-rebalanced radial fixed-source fields; it is not an
independent physical-accuracy or coupled-fixed-point acceptance.

## Numerical result

For all 3 planes and 370 groups, extract the separate terms in
`R = M + Z + B - F`, where M is operator net removal, Z is imposed axial loss,
B is radial boundary net loss and F is the parent-frozen fission source.
Area-weighted group totals in the archive's native flux normalization are:

| Plane | Frozen source F | Net removal M | Axial loss Z | sum(abs(R_g))/sum(F_g) |
| --- | ---: | ---: | ---: | ---: |
| bottom | 4.083943311149e-3 | 3.701880826477e-3 | 3.820624846721e-4 | 1.19617e-14 |
| middle | 7.612428412905e-3 | 6.948864811067e-3 | 6.635636018372e-4 | 1.31390e-14 |
| top | 4.025399237317e-3 | 3.659290037567e-3 | 3.661091997509e-4 | 1.38312e-14 |

B is zero in every row from the stored unit-albedo, identity-paired white
boundary condition. This is a boundary-condition identity, not independent
incoming/outgoing ray accounting. These are planar sums, not absolute thermal
power or a complete 3D reaction-channel balance.

The largest individual `abs(R)/S` is `9.466444566835009e-16`, where S sums
absolute local collision, self-scatter, each off-group scatter, axial-loss,
frozen-fission and net-boundary terms. S is a reported arithmetic scale, not
a fitted weight or acceptance threshold; zero S is explicitly undefined.
The maximum absolute difference between residuals computed by summing whole
components and by summing local residuals is `2.8386456342655757e-18`.

Thus the saved fields have very small group-integrated operator imbalance.
`FLUBAL64` already enforces that balance during the solve: this is useful
archive/equation consistency evidence, not an independent proof of physical
accuracy. The map remains `VALID_NOT_MET`.

## Inputs and safeguards against misinterpretation

The only XSM input is `candidate_radial.xsm` in
`validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-003.portable`.
Its returned epoch is 8, with parent `rho=0.786088540517927092`.
The extractor reads REAL64 FLUX/QFISS/LEAK1D64, region/current maps and the
actual stored REAL32 operator coefficients promoted to REAL64. Compressed
SCAT00 source groups are decoded in descending order, skipping self; the
system's physical self-scattering must match its unreduced used coefficient.
Axial leakage enters exactly once. No inferred `q/u` leakage is used.

An initially proposed `SOUR == QFISS` assumption was rejected in source review
and by the first read-only probe. A9 replaces its terminal source with the
last fixed-plus-off-group source; QFISS is separately preserved by B2R.
The final reader therefore does **not** use SOUR. This avoids double counting
scattering; no production data or solver was changed. The failed probe log
is retained, and the synthetic valid case now explicitly has SOUR != QFISS.

M is **net removal**, not verified capture-plus-fission absorption: APOL/TONE
processing and multiplicative scattering conventions remain part of the
stored operator. See [the scope review](d4a_neutron_balance_readiness.md).

## Reproduction and evidence

The standalone [reader](diagnose_d4a_radial_balance.f90) links only GANLIB.
The [short test](test_d4a_radial_balance.py) compiles temporary programs and
checks all 1110 synthetic rows against independent exact integer/quarter
arithmetic, including padded/reversed scattering indices, signed XS/leakage,
zero denominators, unchanged inputs, overwrite rejection and 10 invalid cases.
Each compilation/program invocation has a 10-second limit. No main-tree
build, Dragon or OpenMC call is needed:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 validation/iterative/test_d4a_radial_balance.py
# An already built reader accepts a short XSM input path and a new CSV path:
(cd "$MAP8" && "$HOST" candidate_radial.xsm "$NEW_CSV")
```

Artifacts are in `validation/artifacts/d4a-radial-balance-diagnostic-20260923`:
`map8_radial_balance_verified.csv`, `map8_run_verified.log`,
`synthetic_tests_final.log`, `build_final.log`, and the root agent's independent
`independent_summary.py` / `independent_summary_verified.json`.
All three source manifests verified before and after extraction. Two read-only
extractions are byte-identical. Independent CSV replay checks all 1110 unique
plane/group rows and the printed binary64 algebra exactly, then aggregates
with `math.fsum`. Code review's source-semantics finding was corrected and
re-reviewed; no remaining P1/P2 was identified.

Verified CSV SHA-256:
`4f79f8e27c1d755d4acaa7ef1c6cb95f96a632aea9808719c557fbef794ed751`.
