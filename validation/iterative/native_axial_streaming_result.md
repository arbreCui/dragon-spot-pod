# Retained-state axial streaming: positive response, unresolved mesh error

The declared characteristic extension passes its native constant-mode,
nonnegative-response and raw balance gates on 1, 2, 4 and 8 axial cells.
It **does not pass the predeclared spatial-convergence gate**. Under common
radial white return, 4-to-8-cell axial escape changes by 1.88–6.11%, above
the 1% limit. This is a prescribed-source result, not a qualified coupled
eigenproblem or a production SPOT repair.

The frozen [artifact](../artifacts/native-axial-streaming-20260929/README.md)
contains the [plan](../artifacts/native-axial-streaming-20260929/plan.json),
[numeric results](../artifacts/native-axial-streaming-20260929/analysis/result.json),
[segment defects](../artifacts/native-axial-streaming-20260929/analysis/segment_balance.json)
and [verification](../artifacts/native-axial-streaming-20260929/verification.json).
The [candidate contract](native_axial_streaming_contract.md) was frozen before
the calculations. No physical threshold was changed afterward.

## Operator and scope

Groups 51, 61 and 98 retain the original 11,364 planar tracks, four polar nodes,
both planar orientations, and the independently declared axial signs. The
20 cm axial domain has vacuum top/bottom inflow, with positive prescribed
inflows tested separately. At each radial segment the entire axial-cell
vector evolves under `A = sigma I + |mu_z| D_up`. The two axial signs select
opposite upstream cells; planar reversal changes radial segment order only.

The exact companion uses `T=exp(-L A)`, `B=integral exp(-s A) ds` and
`D=integral (L-s) exp(-s A) ds`. The tested native-compatible candidate uses
the contract's separate scalar-native factors for T, B and D. That lift is
an explicitly chosen finite-gradient extension, not a uniquely recovered
native axial transport law. For the uniform vacuum grid, all powers of the
nilpotent upstream shift are retained. This introduces no projection error
within the chosen first-order axial mesh.

At each radial surface and axial cell, white return sums all polar nodes and
both axial signs into one incoming amplitude. Its full inverse is checked
entrywise. The historical PJJ rounding remainder is included only in the
zero-gradient P0 calibration. It is not assigned to angles or extended to
finite axial gradients.

For each mesh, kernel, group and radial boundary there are `14*n+18` sources:
all region/cell volume units, all surface/cell common inflow units, all 16
axial face/region units, and two held-out positive volume sources (uniform
and region ramp). Vacuum radial cases precede white cases. These total
3,384 finite-mesh solves, 1,692 per kernel. No scattering, fission,
eigenvalue, POD training, shared compilation or D4 execution is performed.

## Passed checks and disclosed defects

- All retained segment coefficient, incoming, outgoing and full-integral
  Green coefficients are nonnegative. The expanded responses, white
  inverses and resulting half-state fields are also nonnegative. Values
  were not clipped. Signed Jz is not subject to a positivity test.
- The native-compatible zero-gradient extension replays all 648 saved
  signed-state flights with maximum relative half-state error `1.892e-14`;
  it recovers all 93 original P0 cases within `1.581e-14`. The native odd
  response agrees within `7.684e-14`.
- The exact companion differs from native half-state action by as much as
  `3.153e-6`, so it intentionally fails native-table identity. It remains
  an independent numerical control, not a silently substituted native kernel.
- All 384 dense-block coefficient/periodic-constant controls pass. Their
  largest relative differences are `9.516e-15` and `3.124e-15`, respectively.

The balance ledger uses the actual geometric source/inflow measures and the
stored native output measures. Their original rounding mismatch is retained.
"Cell" below means an axial slab summed over all eight radial regions;
these are not eight independently measured radial-interface balances.
Odd balances use the signed first moment and the corresponding second-moment
face flux. Global denominators contain only external source/inflow, excluding
white-boundary recirculation. Cell denominators include local incoming flux.

| Quantity, maximum over the specified cases | Exact companion | Native-compatible lift | Frozen limit |
| --- | ---: | ---: | ---: |
| Even global relative balance defect | 3.610e-14 | 1.383e-7 | exact 1e-10; native 1e-6 |
| Odd global relative balance defect | 6.955e-15 | 1.258e-7 | exact 1e-10; native 1e-6 |
| Even axial-cell relative defect | 1.304e-14 | 1.404e-6 | exact 1e-10; native 1e-5 |
| Odd axial-cell relative defect | 7.203e-15 | 1.459e-6 | exact 1e-10; native 1e-5 |
| Face-current versus streaming-matrix absolute defect | 4.441e-16 | 2.221e-16 | 1e-13 |
| Common radial-return relative defect | 5.937e-16 | 7.299e-16 | 5e-12 |

The all-segment audit includes 439,344 segment/polar samples per group and
mesh. Its induced infinity norms are `||T+A B-I||` and
`||B+A D-L I||/L`. Exact maxima are `8.388e-16` and `1.923e-15`; native-lift
maxima are `2.169e-7` and `1.322e-6`. These are descriptive raw defects,
with no new post-hoc acceptance threshold or balancing correction.

At finite meshes the maximum scalar-response difference between the two
kernels is `2.923e-6` (about 0.0002923%); the maximum face-current difference
under the recorded whole-array relative norm is `5.090e-7`. These kernel
differences are much smaller than the observed mesh changes.

## Failed spatial-convergence gate

Fine-to-coarse restriction averages each pair of fine cells. Scalar errors
use native-volume times cell-height weighted L2 norms; escape errors use the
total outgoing top-plus-bottom current. The denominator is the 8-cell value.
Both quantities, for both held-out sources, had to change by less than 1%.

| Native-compatible group | Uniform flux | Ramp flux | Uniform axial escape | Ramp axial escape |
| --- | ---: | ---: | ---: | ---: |
| 51 | 1.2590% | 1.2618% | 6.0858% | 6.1110% |
| 61 | 0.9959% | 0.9989% | 5.1125% | 5.1371% |
| 98 | 0.3447% | 0.3470% | 1.8831% | 1.8780% |

All three groups fail because their escape change exceeds 1%; group 51 also
fails the flux condition. The exact companion reaches the same gate outcome.
Small algebraic and current-balance residuals therefore do not establish
mesh-independent physical observables. No mesh above 8 was added to this run.

## Reproduction and next step

A fresh-directory replay using archived code and copied inputs reproduces
all 56 analysis files byte for byte and all 900 arrays exactly. Thirteen
analytical tests pass from maintained and archived code, including an
independently assembled two-material full response with both planar orders
and both axial signs. The initial 12-test source/log remain archived; the
13th test adds finite-mesh assembly coverage without changing the kernel.
All 997 protected files and 1,301 manifest entries from 14 earlier artifacts
remain unchanged.

The [next refinement contract](native_axial_streaming_refinement_contract.md)
keeps the same model and sources, declares 16/32/64-cell comparisons, and
requires a bounded-memory implementation to reproduce these coarse results
before extension. Its purpose is to resolve spatial error, not to tune a
reference answer. Until this and subsequent coupled multigroup qualification
succeed, the earlier full-space negative-angle failures remain active
regressions and this candidate must not enter the live D4 chain.
