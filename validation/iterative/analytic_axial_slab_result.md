# Analytic axial check: small mesh changes can admit inaccurate cell averages

All 78 prescribed S2 slab solves pass the frozen algebra, raw balance and
positivity gates, and the analytic reference checks pass. Nevertheless,
the predeclared adjacent-grid comparison produces **two false admissions**:
both scalar and escape changes are below 1%, while the true fine-grid
scalar cell-average error is 1.28–1.40%. In a conservative strong-scattering
case, 256-cell scalar error is still 11.09% although leakage is fixed almost
exactly by global balance.

This qualifies the manufactured implementation and diagnoses a limitation
of the convergence criterion. It does not qualify native mesh convergence,
reproduce native radial white return, or admit a coupled eigenreference.

The [artifact](../artifacts/analytic-axial-discretization-20260929/README.md)
contains the [predeclared plan](../artifacts/analytic-axial-discretization-20260929/plan.json),
[numeric results](../artifacts/analytic-axial-discretization-20260929/analysis/result.json),
[interior-operator analysis](../artifacts/analytic-axial-discretization-20260929/analysis/interior_identity.json)
and [verification](../artifacts/analytic-axial-discretization-20260929/verification.json).
The [experiment contract](native_streaming_discretization_contract.md) was
frozen before running. Physical gates and comparison thresholds were not changed.

## Problem and reference

The homogeneous slab has height 20 cm, directions `+/-1/sqrt(3)` with weights
1/2, unit source in each direction, isotropic scattering, and vacuum incoming
flux at both ends. Totals 0.02, 0.2 and 2 per cm are each paired with scattering
fractions 0, 0.9, 0.99 and 1; the void is the thirteenth case. These constants
are prescribed controls, not fitted native-group constants. Meshes are
8/16/32/64/128/256 cells, using the original signed upwind operator imported
from the frozen preceding artifact.

The scalar and current definitions are `phi=(psi+ + psi-)/2` and
`J=mu*(psi+ - psi-)/2`. The analytic moments solve
`J' + sigma_a*phi=q` and `mu^2*phi' + sigma_t*J=0`, with the corresponding
vacuum boundary conditions. Positive-absorption hyperbolic solutions are
evaluated with stable exponential expressions; conservative and void limits
use their exact polynomial forms.

"True scalar error" throughout this report means the height-weighted L2
error against **analytic averages over the same cells**. Directional errors
also include half weights. These are not point samples at cell centers or a
claim to have measured every continuous reconstruction error. Each adjacent
comparison conservatively averages the fine-cell pairs before comparing
scalar flux; escape is outgoing bottom plus top current.

## Two false admissions

Both occur in the pure absorber `sigma_t=2`, `sigma_s=0`.

| Coarse / fine cells | Adjacent scalar change | Adjacent escape change | True fine scalar error | True / adjacent scalar error |
| --- | ---: | ---: | ---: | ---: |
| 16 / 32 | 0.4540% | 2.356e-10% | 1.4002% | 3.084 |
| 32 / 64 | 0.5767% | 0% at saved precision | 1.2845% | 2.228 |

Thus the two-observable 1% adjacent-grid rule would accept these fine meshes,
even though their matching scalar cell averages fail the same 1% true-error
comparison. This is an observed counterexample to that rule as an accuracy
bound. It is not a failure of the linear solve or a retroactive change to
earlier acceptance labels.

The pure-absorber cell-average error initially grows with refinement before
decreasing. Coarse averages can hide an unresolved boundary-layer shape;
refining changes which part of that shape the cell-average metric resolves.
A low adjacent-grid change by itself does not establish an asymptotic regime.

![Cell-average and escape errors against the analytic solution](../artifacts/analytic-axial-discretization-20260929/figures/analytic_errors.png)

## Strong scattering and the cost of upwind diffusion

Selected 256-cell errors are:

| Total / scattering fraction | True scalar error | True total escape error | Last observed scalar order |
| --- | ---: | ---: | ---: |
| 2 / 0 | 0.5027% | roundoff | 0.787 |
| 2 / 0.9 | 0.6171% | 4.3737% | 0.909 |
| 2 / 0.99 | 2.0603% | 5.7561% | 0.943 |
| 2 / 1 | 11.0863% | 1.716e-11% | 0.837 |
| Void | 0.390625% | roundoff | 1.000 |

The no-absorption escape equals the integrated external source, so its tiny
error cannot diagnose the remaining scalar-shape error. The void has the
exact discrete scalar-error identity `1/n`, despite exact total escape.
For the weaker-total cases, finest scalar errors are approximately
0.21–0.61%, with last observed orders 0.978–0.999. The strong cases approach
first order more slowly; no continuum error is inferred from a last mesh
difference alone.

The signed upwind equations imply the following **exact interior stencil
identities**, with centered difference `D0` and the usual second difference
`Delta_h`:

```
D0 J - mu*h/2 * Delta_h(phi) + sigma_a*phi = q
mu^2*D0 phi - mu*h/2 * Delta_h(J) + sigma_t*J = 0
```

An independent arbitrary-field test verifies these identities. On the saved
solves their source-scaled discrepancy is at most `8.013e-13`. This is a
descriptive postprocessing check, not an added acceptance gate.

In the formal slowly varying diffusion limit, substituting
`J ~ -mu^2/sigma_t * phi'` gives diffusion coefficient
`mu^2/sigma_t + mu*h/2`. The extra-to-physical diffusion ratio is therefore
`eta=sigma_t*h/(2*mu)`. For total 2 at 256 cells, eta is 13.53%.
Reducing **this coefficient ratio** below 1% would require more than 3,464
cells at the same height and angle. This is a cost indicator, not a promise
that such a mesh achieves 1% flux or escape error, and it cannot be transferred
to native radial white-return transport. It motivates testing a more accurate
positive discretization before launching much larger native meshes.

## Verification and limits

All 78 numerical solutions are nonnegative without clipping. Maximum matrix
residual relative to the unit source is `4.5475e-12`, below the fixed `5e-12`
gate; maximum raw global imbalance is `1.7160e-13`, below `1e-10`.
Maximum even/odd cell-balance defects are below `2.384e-15`.
The maximum analytic equation, boundary, integrated-balance and independent
32-point cell-quadrature discrepancies are respectively `4.441e-16`,
`1.026e-16`, `2.748e-16` and `4.101e-16`, all below `5e-12`.

Eleven tests pass from both maintained and archived sources. They include
pure-absorption directional exponentials, independent transfer-matrix
boundary solutions, nonuniform-cell quadrature, the conservative polynomial,
void escape versus scalar error, and the interior numerical-diffusion identity.
The initial nonuniform-cell test caught cancellation in small currents;
its source and failed log remain archived. Stable exponential differences
fixed the implementation before the full run, without changing thresholds.

A fresh-directory replay reproduces all 80 analysis files byte for byte and
all 1,248 arrays exactly. All 997 protected files, 10 source-input hashes,
13 copied-input hashes, and 1,978 entries from 17 preceding artifacts verify
unchanged. The primary calculation used about 100 MiB peak RSS and 0.20 s,
with one numerical thread; this cost is for the manufactured slab only.

The next [positive cell-characteristic comparison](axial_cell_characteristic_contract.md)
will use these same analytic cases and grids. It must check exact cell means,
positivity and balance before comparing true errors. Success there would
still require a separate native directional coupling and zero-gradient
qualification. The native 64-cell failure, all earlier angular failures,
and the live D4 chain remain unchanged.
