# D4-A saved radial operator balance

## Repaired 12-cell CLOSED/6: current-epoch saved-data check

2026-09-28. A transport-free read of
`validation/artifacts/d4a-scattering-mesh12-picard-map6-20260927/candidate_radial.xsm`
checks its RETURNED/6 radial fixed-source equation. No input, production code,
active map-7 file, physical coefficient or acceptance threshold was changed.

The existing GANLIB-only reader was used without recompilation, followed by
the existing independent arithmetic checker. Both calls had 10-second caps;
extraction, replay and after-hash checks took 0.202 seconds. All 1110 unique
plane/group rows replay exactly in binary64; the five pinned source/reader
files are unchanged. The reader used authoritative REAL64 FLUX/QFISS/LEAK1D64,
not terminal SOUR or the closed archive's relabelled source.

| Plane | Frozen source F | Operator net removal M | Imposed axial loss Z | sum(abs(R_g))/sum(F_g) |
| --- | ---: | ---: | ---: | ---: |
| bottom | 4.077267141478e-3 | 3.751211920091e-3 | 3.260552213865e-4 | 1.33976e-14 |
| middle | 7.497946972335e-3 | 6.926848633936e-3 | 5.710983383991e-4 | 1.37403e-14 |
| top | 3.992094869458e-3 | 3.683654746159e-3 | 3.084401232991e-4 | 1.23068e-14 |

Here `R=M+Z+B-F`, with `B=0` from the stored conservative identity-paired
white boundary condition. The largest individual `abs(R)/S` is
`9.015471944903435e-16`; the largest difference between component-wise and
local-first summation is `3.131285591374586e-18`. Values use the archive's
native planar normalization, not absolute thermal power.

**Scope:** this establishes repaired-epoch archive/operator consistency.
`FLUBAL64` already enforces group-integrated balance, so this is not an
independent reaction-channel or 3D local-current conservation test and does
not resolve the remaining CE k discrepancy. CLOSED/6 remains NOT_MET.

Evidence: `validation/artifacts/d4a-mesh12-map6-radial-balance-20260928`.
Its six-file result manifest verifies, with SHA-256
`a4c7550000ba69d82d9b6d8ad51e5d11465977c0c41d2f3baf60edd3addd9608`;
the CSV hash is
`adb63ea1fe992f10d5a0bccc2f7636d9e1572c3d24d5c3c6218232c31e3e06d3`.
The wrapper refuses existing outputs and records the unchanged source pins.

## Historical pre-repair map 8

**Historical / superseded physical state.** This map belongs to the old
pre-scattering-repair maps 1–11. Its numerical results are retained without
alteration, but cannot validate the repaired runtime or the current 12-cell
chain. The separate repaired CLOSED/6 calculation above and the boundary
cross-check in [the scope review](d4a_neutron_balance_readiness.md) do not
transfer this historical result into the repaired epoch.

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
