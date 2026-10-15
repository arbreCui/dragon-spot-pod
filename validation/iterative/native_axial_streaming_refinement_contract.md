# Refinement of the retained-state axial streaming candidate

This is the next bounded experiment after
[the 1/2/4/8-cell result](native_axial_streaming_result.md), whose 4-to-8-cell
escape change failed the frozen 1% gate. The preceding artifact and failed
gate remain immutable. This document specifies future work, not completed
refinement evidence.

## Fixed physical and numerical model

Keep groups 51, 61 and 98, height 20 cm, the same original tracks, polar
quadrature, independent axial signs, first-order upwind streaming, native
geometric measures, both exact and native-compatible segment kernels, and
common radial white return. Include radial vacuum controls. Axial inflow
remains vacuum for the refinement sources. Do not alter coefficient factors,
normalizations, angular weights, boundary mixing or radial segmentation.

Use the same two held-out volume sources: uniform and region index divided
by eight, each constant along z. Keep positive-source tests distinct from
signed odd-current diagnostics. No multigroup scattering/fission solve,
eigenvalue, POD training or production changes belong to this stage.

## Implementation and calibration before extension

The next implementation may process ray/polar lines in fixed batches and
apply Toeplitz Green functions without materializing all angular/cell/source
columns simultaneously. Retain every shift power for the chosen grid; no
low-rank approximation, small-entry pruning or clipping is allowed.
Preserve raw balance defects.

Before any grid above eight cells, calibrate on the frozen 1/2/4/8-cell
artifact. Require native and exact kernels separately to reproduce Green
coefficients, the two held-out half-state fields, scalar flux, radial
outgoing state and axial face current within `5e-12` under the existing
maximum relative norms. Compare with the independent dense-block and
two-material controls as well. Different summation order must be disclosed.
If calibration fails, stop before interpreting refined results.

Freeze the actual batching/memory cap and command in a separate run plan.
Use one numerical CPU thread and bounded temporary arrays, because another
task owns live D4 work. Reuse no mutable live files. A cost or memory cap
ends the stage as incomplete; it is not permission to substitute a reduced
state or omit failed cases.

## Declared meshes, observables and gates

Run 16, 32 and 64 cells in that order. Reuse the sealed 8-cell results only
after calibration. The intended new comparison set is 3 groups × 2 kernels
× 2 radial boundaries × 3 meshes × 2 sources = 72 prescribed solves.
No grid beyond 64 is implied. Save every intermediate mesh, including any
failed balance, positivity or refinement gate.

For each mesh save scalar and half-state flux, Jz, top/bottom face currents,
radial incoming/outgoing state, total axial escape, and even/odd balances.
Check nonnegative primitives, Green responses and white inverse/solution;
report raw segment defects separately. Retain these limits:

- strict nonnegative response, minimum zero, with no clipping;
- exact global and axial-cell relative balance below `1e-10`;
- native-compatible global below `1e-6` and axial-cell below `1e-5`;
- face-versus-streaming absolute defect below `1e-13` and radial-return
  relative defect below `5e-12`.

For every adjacent mesh pair, report conservative fine-to-coarse scalar
flux changes in the same native-volume/height weighted L2 norm, and relative
top-plus-bottom escape changes using the finer mesh as denominator.
The final 32-to-64 comparison must be below 1% in both observables for both
sources, all three groups and both radial boundaries. Report exact and
native-compatible outcomes separately; both are required for this stage.
Also disclose preceding changes and observed order when defined; do not
claim an asymptotic error bound from the last difference alone.

Separate exact-versus-native coefficient effects from mesh changes at every
level. Preserve fine-grid failures or non-monotone behavior and stop at 64;
any later discretization or mesh extension needs a new declared experiment.

## Admission boundary

Passing this stage would qualify only these single-group prescribed-source
mesh comparisons. It would not qualify a multigroup eigenproblem or erase
earlier group-61 vacuum and group-51 fine-grid failures under the historical
closure. A later full-coordinate coupled reference must separately qualify
scattering/fission sources, currents, positivity, spatial/angular refinement
and neutron balance before any same-operator POD comparison.

Archive input identities, source snapshots, command/runtime metadata and a
fresh-directory replay. Do not mutate earlier sealed artifacts or the live
D4 sources, binaries, libraries, decks, controls or maps.
