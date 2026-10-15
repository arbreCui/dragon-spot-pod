# D4 map-6 frozen operator: initial guess and stopping sensitivity

Completed 2026-09-28. Three isolated axial solves passed their declared inner
tests. Tightening the three inner thresholds from 2e-6 to 2e-7 substantially
reduces the observed cold/warm difference, but does not bring modal and leakage
repeatability to the existing 5e-7 outer scale. This is a diagnostic result,
not a changed coupled gate or an estimate of a floating-point floor.

## Controlled experiment

All cases use exact copies of the completed map-6 SYSTEM, TRACK, MACROLIB and
sealed repaired Dragon: twelve axial cells, rank 2, SN8, SCAT3, three material
zones. There is no new ASM, radial solve, coupled map or CE calculation.
EXTE 500, REBA OFF and ACCE 3 3 remain fixed. Each new solve had a 600-second
cap, one thread and no retry. The source and private input hashes stayed equal.

The cold cases use native FLU initialization. The warm tighter case starts at
the original CLOSED/6 terminal. EXTE, UNKT and THER thresholds change together
by exactly one decade; this is not an experiment varying just one criterion.
The previously completed warm repeat at 2e-6 is retained as additional evidence.

| Case | Inner thresholds | k64 | Outer iterations | Solve wall seconds |
| --- | ---: | ---: | ---: | ---: |
| Original CLOSED/6 terminal | 2e-6 | 1.2847427149054287 | See original map | See original map |
| Earlier warm terminal repeat | 2e-6 | 1.2847430103542397 | 2 | 1.778 |
| New cold solve | 2e-6 | 1.2847468016911034 | 21 | 199.552 |
| New warm solve | 2e-7 | 1.2847463593764721 | 4 | 12.434 |
| New cold solve | 2e-7 | 1.2847459873766922 | 19 | 222.133 |

## Differences and interpretation

| Comparison, second minus first | Reactivity change (pcm) | Canonical modal norm Ra | Relative leakage-coefficient norm | Physical scalar-flux relative volume L2 |
| --- | ---: | ---: | ---: | ---: |
| Original terminal to cold, 2e-6 | +0.2475986 | 5.85735e-5 | 2.26255e-4 | 6.49982e-5 |
| Warm repeat to cold, both 2e-6 | +0.2296987 | 5.86106e-5 | 2.26340e-4 | 6.50418e-5 |
| Warm to cold, both 2e-7 | -0.0225376 | 1.79834e-6 | 1.31575e-5 | 1.89583e-6 |

The reactivity definition is `1e5 * (1/k_first - 1/k_second)`. Canonical
coordinates and leakage norms follow SPOSTATE/SPOXCONV, including the existing
REAL32 flux-mirror fission normalization. The physical comparison separately
reads every active FLUX64 scalar through KEYFLX and integrates all NUSIGF
components to obtain a single global REAL64 fission normalization. It then
uses volume-weighted L2, with the second field in the denominator. There is no
regional renormalization, clipping, energy-group floor or fitted adjustment.

At 2e-7, the inverse-k difference is 2.25376e-7, below the outer Rrho scale,
but Ra and Rleak are respectively 3.60 and 26.3 times their outer scales.
These are comparisons of scales, not an outer gate on these independent solves.
The tighter cases' source-normalized total outward leakage is respectively
0.0772648784 and 0.0772652566. The worst-group coefficient norm and total
integrated leakage are different observables and must not be interchanged.

The small k changes cannot explain the approximately -1096 pcm SPOT–CE gap.
They also do not certify all modal/flux quantities to the outer tolerance.
Tighter stopping improves this particular initial-guess comparison; it does
not prove a monotone error bound, isolate restart/iteration quantization, or
show that 2e-7 is sufficient for production. The active runtime is unchanged.

## Evidence and checks

`validation/artifacts/d4a-map6-axial-repeatability-20260928/` retains the plan,
exact inputs/decks, bounded runner, all native logs and axial states, input
hashes, comparisons and a result manifest. `analyze.py NEW_DIRECTORY` replays
the saved diagnostics without transport. It reproduces all four SPOXCONV
numbers from every new native solve exactly and checks exact self-comparison.

[compare_saved_axial.f90](compare_saved_axial.f90) is a Ganlib-only read-only
tool. Its [five analytic tests](test_compare_saved_axial.py) cover identity,
volume averaging between nested meshes, a known nonzero shape difference,
refusal of an incompatible refinement direction, and explicit omission of
modal norms when only physical fields are requested. It was compiled only as
a separate diagnostic; no solver or active-runtime binary was rebuilt.

The next 12/24-cell comparison uses the tighter cold case as its baseline and
reports the observed same-grid sensitivity alongside the mesh difference.
Neither that comparison nor this experiment substitutes for a separately
converged coupled mesh study.
