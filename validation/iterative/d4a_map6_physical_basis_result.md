# D4 map-6 frozen operator: physical-coordinate comparison is incomplete

Attempted 2026-09-28. The full 132-coordinate axial solve reached its declared
1,200-second budget without an accepted terminal. **No rank-error estimate
is available from this attempt.** The last printed eigenvalue is an iterate,
not a reference result. No tolerance was loosened and no retry was launched.

A [subsequent passive column trace](d4a_map6_physical_column_trace_result.md)
now exposes a reference-admissibility issue: the fission-free columns lose
essentially all flux, and the original runtime rejects the raw-10 checkpoint
for nonpositive active scalar flux. The next-step interpretation below is
superseded by that diagnostic and its coupled-reference contract; this
original attempt's inputs, logs and incomplete status are unchanged.

## What was controlled and verified

The baseline is the completed twelve-cell `cold_tight` rank-2 state from the
[initial-guess study](d4a_map6_axial_repeatability_result.md). SPOPHYS builds
a complete physical radial basis from the same frozen map-6 SYSTEM: rank 132
in all 370 groups, rather than rank 3 of the three snapshots. The diagonal
basis has entries `1/sqrt(area_i/sum(area))`. The tracking, MACROLIB, axial
mesh, SN8, SCAT3 and vacuum boundaries remain unchanged. The repaired Dragon
executable is copied without rebuilding it.

Independent Ganlib-only checks confirm:

- Every group's radial operator, volumes, total/self-scattering data and
  snapshot spectrum are retained bit for bit.
- The new basis has all 132 expected diagonal entries and exactly zero
  off-diagonal entries.
- Reexpressing the completed rank-2 seed in the physical basis changes its
  FLUX64 field, k and leakage by exactly zero in the saved-state comparison.

The physical solve starts from that reexpressed seed, with EXTE/UNKT/THER all
2e-7, EXTE 500, REBA OFF and ACCE 3 3. It uses one thread and the same
bounded runner as the preceding experiments. A full physical basis removes
the POD restriction but retains the transverse-response and plane-leakage
closures; it is not an independent full 3D reference.

## Actual outcome

The runner stopped the process at 1,200.131 measured seconds. The native log
contains 25 completed outer updates, but no `FLU2DR-TERM OUTER-GATE=PASS`
and no final completion marker. No final `axial.xsm` was written. The last
printed outer PRC is 2.47e-6 versus the declared 2e-7 target; that printed
quantity alone would not certify all inner criteria in any case.

All private and source input hashes remain unchanged. The failed attempt is
classified `INCOMPLETE_NO_RANK_ERROR_ESTIMATE`. In particular, the intermediate
k trend cannot be used to subtract a POD contribution from the SPOT–CE gap,
select a rank, claim a speedup, or promote this run to a coupled reference.

The first setup in `case/` completed SPOPHYS but then tried to delete a
lifecycle marker absent from the cold diagnostic seed. UTL rejected that
operation before FLU ran. `case_unmarked_seed/` removes only that inapplicable
deletion and contains the single attempted transport solve. Both logs and
the correction note are retained.

## What to do next

The preceding [mesh study](d4a_map6_axial_mesh24_result.md) establishes a
+39.23943 pcm frozen-radial 12/24-cell sensitivity; the tighter same-grid
cold/warm difference is 0.02254 pcm. Neither establishes the missing rank
effect. The next rank-study milestone is a qualified complete-coordinate
terminal, with a declared solver strategy and budget, before a coupled rank
comparison or a basis-enrichment decision.

There is a useful diagnostic lead in the existing implementation:
`SPOT1P64` detects this diagonal physical basis and exactly separates its
within-group boundary systems by radial coordinate. This is verified algebraic
structure, not evidence that it caused the slow outer iteration. Inspect the
global eigen-iteration and flux-shape history on a separately prepared run
before deciding between a larger budget and a different qualified iteration
strategy. Do not infer that raising an iteration/time limit guarantees
convergence, and do not change the active coupled runtime.

## Retained evidence

`validation/artifacts/d4a-map6-frozen-physical-basis-20260928/` contains the
pre-execution plan, exact input receipts, setup decks, failed and corrected
build logs, operator and initial-field checks, the bounded solve log,
`execution.json`, and `analysis/summary.json`. The analysis explicitly refuses
to report a rank comparison for an incomplete run. `result.sha256` seals the
local evidence. The protected-input check also verifies all 997 files in the
earlier source/runtime inventory unchanged.

The comparison and analysis tools are separate read-only diagnostics. No
new radial transport, coupled map, CE calculation or source rebuild was run.
