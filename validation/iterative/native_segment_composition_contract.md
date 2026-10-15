# Native characteristic composition before an axial crossing bridge

The [cell-characteristic slab result](axial_cell_characteristic_result.md)
qualifies its manufactured one-dimensional problem: all 13 finest-grid scalar
and total-escape errors are below 1%. It does not supply the geometry or
native-kernel compatibility needed for an extruded radial/axial flight.

The next bounded prerequisite checks whether inserting axial crossing points
inside a native radial segment preserves its original T/B/D action. A new
crossing scheme cannot assume a composition property merely because native
coefficients and exact exponentials are numerically close.

## Frozen scope and inputs

Use the sealed directional/signed fixture for groups 51, 61 and 98, its
original native material totals and all retained positive-length segments.
Preserve `L = planar_length * ZMU` and the already qualified independent
axial signs with `abs(mu_z) = sqrt(1 - 1/ZMU**2)`. Keep the native geometric
weights and PJJ rounding completion separate.

For every segment, compare the original unsplit flight with equal 2-, 4-
and 8-piece partitions and an asymmetric 1/3 + 2/3 partition. These fractions
are algebraic probes fixed before execution, not fitted crossing locations.
Use two companions:

1. Stable exact exponential integrals on the whole segment and its pieces.
2. The original native `MCGSCA` and `MCGDSCA` kernels on the same physical
   lengths, with the original total-cross-section precision and modes.

Extract subsegment native coefficients through a private probe linked to the
already identified runtime, or a private build of the exact identified
coefficient routines. Calibrate unsplit extraction against every saved B/D
coefficient at the existing `5e-12` native-action tolerance before interpreting
split results. Do not reconstruct missing D from balance, interpolate whole
segment coefficients, use a scalar regional inverse, or rebuild shared code.

Add independent void, thin, moderate and thick exact controls with optical
lengths 0, 1e-12, 1e-6, 0.001, 0.7, 10 and 100. Native void support is a
separately disclosed interface check; do not force it through a positive-total
branch. Retain any unavailable native branch as unavailable.

## Composition equations and controls

Each piece has incoming amplitude x and a constant prescribed source q:

```
x_out = T*x + B*q
integral_psi = B*x + D*q
T_exact + sigma*B_exact = 1
B_exact + sigma*D_exact = L
```

For two same-material pieces and a common source, composition requires

```
T_12 = T_2*T_1
B_out_12 = T_2*B_1 + B_2
B_integral_12 = B_1 + B_2*T_1
D_12 = D_1 + D_2 + B_2*B_1
```

Keep both B roles in the raw ledger. Check these through independently
implemented direct sweeps and augmented 3-by-3 transition matrices. Test
boundary-unit and whole-source-unit inputs, then each piece-source unit and
the fixed alternating 0/1 source in both travel orders. Save every signed
amplitude, integrated value and raw `out-in+sigma*integral-L*q` defect.

For exact coefficients require positive kernels/responses, direct/matrix
agreement and partition invariance at `5e-12`; source/current balance must
remain below `1e-10`. For native coefficients keep the established positivity
and unsplit recovery gates. A split native action may only be called unchanged
if both outgoing and integral responses recover the unsplit native action
within `5e-12`. Record native balance and native-versus-exact differences
separately, using the earlier `1e-6` global raw-balance limit as context.
Do not loosen native recovery or distribute the PJJ remainder among pieces.

Freeze a plan, dimensional error scales, input hashes and finite resource
caps before execution. Use one numerical thread, a 512 MiB memory cap and
600 seconds for each extraction/analysis process; batch segments if needed.
Keep per-segment failures and a complete fresh-directory replay.

## Decision boundary

A failed split-native recovery gate means that naive repeated application
changes the old kernel; preserve that failure. It does not invalidate exact
characteristics, and it does not authorize fitted correction factors.
The measured discrepancy will decide whether an exact-kernel replacement
needs separate native-action qualification or a different native-preserving
bridge must be derived.

This audit does not yet define a full oblique trajectory quadrature or radial
white closure. The later geometry contract must specify axial-plane crossings,
entrance/exit measures, axial source-cell averages and shared face currents,
and recover the native zero-gradient flight. Common radial white return must
still mix all polar nodes and independent axial signs. The previous native
mesh failures remain failed. No multigroup/fission solve, POD training, live
D4 execution or production change belongs to this prerequisite.
