# Cell-characteristic slab comparison: declared accuracy target passed

The positive cell-characteristic candidate passes the previously frozen
one-dimensional test. At 256 cells, all 13 analytic slabs have true scalar
cell-average and total-escape errors below 1%. The largest scalar error is
**0.564867%**, down from **11.0863%** for the preceding upwind method in the
same conservative strong-scattering slab. The largest total-escape error is
**0.270112%**, versus **5.75610%** for upwind in that 99%-scattering case.

This admits the candidate on the specified manufactured slab only. The
native radial/axial reference remains spatially unqualified, and no coupled
eigenproblem, POD training or production change is admitted.

## Evidence and fixed comparison

- [Predeclared contract](axial_cell_characteristic_contract.md)
- [Run plan](../artifacts/axial-cell-characteristic-20260929/plan.json)
- [Complete numeric results](../artifacts/axial-cell-characteristic-20260929/analysis/result.json)
- [Verification](../artifacts/axial-cell-characteristic-20260929/verification.json)
- [Artifact and replay instructions](../artifacts/axial-cell-characteristic-20260929/README.md)
- [Previous analytic upwind result](analytic_axial_slab_result.md)

The inputs remain height 20 cm, S2 directions +/-1/sqrt(3), angular weights
1/2, unit source in each directional equation and vacuum incoming faces.
Totals 0.02, 0.2 and 2 per cm each use scattering fractions 0, 0.9, 0.99 and
1; the thirteenth case is a void. Every case uses 8/16/32/64/128/256 cells.
There are 78 physical-source solves and 65 adjacent-grid comparisons.

References are the actual analytic cell means from the sealed preceding
experiment. Every copied reference is checked against a fresh evaluation,
including independent derivative, boundary, global-balance and cell-quadrature
controls. Recomputed upwind fields also match every saved field exactly.

## Candidate and independent equation checks

For cell path length `L=h/abs(mu)`, compute nonnegative exact T/B/D integrals.
Each direction obeys

```
Q_i = sigma_s*phi_i + q_i
psi_out = T*psi_in + B*Q_i
mean_psi = (B*psi_in + D*Q_i)/L
phi_i = (mean_psi_plus + mean_psi_minus)/2
```

Neighboring cells share one angular face value. Analytically eliminating the
faces produces an n-by-n system for **all** scalar cell means; solving it
directly and recovering every angular mean and face is the full source-response
formulation permitted by the contract. It does not truncate the spatial state
or incur source-iteration stopping error. Independent tests compare it with
the expanded 3n+2 face/mean equations on nonuniform, heterogeneous grids with
unequal directional sources, including periodic boundaries.

Thin-cell D uses its convergent dimensionless series; other cells use stable
exponential integrals. Void coefficients are exactly T=1, B=L, D=L^2/2.
No flux clipping, balancing multiplier or fitted transport coefficient is used.
The smallest `1-sigma_s*D/L` is 0.115450, strictly positive.

## True errors and convergence

All entries below are **percent relative errors** at 256 cells. Scalar and
directional errors use the preceding height-weighted cell-mean L2 norms.
The complete file also retains signed cell currents, angular means, face
currents, separate bottom/top escape errors and all coarse meshes.

| Total / cm | Scatter fraction | Upwind scalar | Candidate scalar | Upwind total escape | Candidate total escape |
|---:|---:|---:|---:|---:|---:|
| 0.02 | 0 | 0.242958 | 3.21324e-13 | 0.0936862 | 4.80128e-13 |
| 0.02 | 0.9 | 0.323291 | 6.01609e-06 | 0.0125013 | 2.11213e-07 |
| 0.02 | 0.99 | 0.334452 | 6.82104e-06 | 0.0012935 | 2.40733e-08 |
| 0.02 | 1 | 0.335741 | 6.91369e-06 | 2.4869e-13 | 6.21725e-13 |
| 0.2 | 0 | 0.212869 | 5.96671e-14 | 0.0094606 | 7.69939e-14 |
| 0.2 | 0.9 | 0.35679 | 0.00172005 | 0.188581 | 0.00110467 |
| 0.2 | 0.99 | 0.563208 | 0.00318948 | 0.0364003 | 0.000221421 |
| 0.2 | 1 | 0.606207 | 0.00348408 | 2.8777e-12 | 6.03961e-13 |
| 2 | 0 | 0.502716 | 1.39508e-14 | 9.61481e-14 | 1.92296e-14 |
| 2 | 0.9 | 0.617137 | 0.0265338 | 4.37373 | 0.207868 |
| 2 | 0.99 | 2.06033 | 0.0963143 | 5.7561 | 0.270112 |
| 2 | 1 | 11.0863 | 0.564867 | 1.71596e-11 | 8.70415e-12 |
| 0 | 0 | 0.390625 | 2.46926e-14 | 1.77636e-14 | 1.77636e-14 |

![True analytic errors on fixed grids](../artifacts/axial-cell-characteristic-20260929/figures/true_errors.png)

The strongest conservative case improves by 19.63 times at the fixed finest
grid. Scalar observed orders over 128→256 cells range from 1.969 to 2.000
for the nine scattering cases. Pure-absorption and void errors are at roundoff,
so no observed order is assigned to them. Conservative total escape remains
balance-constrained and is not evidence for scalar accuracy on its own.

Coarse meshes still fail the true-error target: the largest scalar error is
2.21118% at 128 cells and 8.14896% at 64 cells. The largest total-escape error
is 1.07022% at 128 cells. The successful declaration applies to 256 cells.
This experiment has zero adjacent-grid false admissions, but this does not
turn adjacent changes into a general error bound.

## Positivity, balance and limiting controls

In addition to the 78 physical sources, all 13,104 independent directional
cell-unit source responses and 156 boundary-unit responses are retained.
Every outgoing angle and angular cell mean is nonnegative, without a
roundoff clipping allowance; zero is attained by physical vacuum inflows
and uncoupled source responses.

| Check | Maximum measured | Frozen limit |
|---|---:|---:|
| Physical direct matrix residual | 4.37e-13 | 5e-12 |
| Unit-response direct matrix residual | 3.26e-14 | 5e-12 |
| Face/cell characteristic consistency, all responses | 4.91e-15 | 5e-12 |
| Scalar mean consistency, all responses | 3.28e-15 | 5e-12 |
| Boundary consistency | 0 | 5e-12 |
| Raw global balance, all responses | 1.28e-13 | 1e-10 |
| T/B/D segment identities | 2.05e-16 | 5e-12 |
| Pure-absorption/void analytic means and faces | 4.83e-15 | 5e-12 |
| Absorbing periodic constant mode | 8.39e-13 | 5e-12 |

Raw local even/odd balance defects are retained; their largest scaled values
are 4.59e-15 and 4.49e-15. The verifier also independently evaluates each
directional finite-volume equation from saved faces and cell means.

All 24 pure-absorption/void mesh controls recover the analytic directional
means and faces. All 54 positive-absorption periodic controls recover
`phi=q/(sigma_t-sigma_s)`. The 24 conservative/void periodic positive-source
controls are rejected by integrated compatibility before solving: they have
no steady solution. They are expected incompatibility checks, not failed
vacuum slab cases or normalized periodic solutions.

## Cost and reproducibility

These are one-run medians over the 13 materials at each grid, in milliseconds.
Candidate physical time includes response assembly, factorization and one
physical solve. Basis time uses the same factorization for 2n+2 additional
right-hand sides. Upwind time recomputes one full physical solve. The
comparison concerns these independent dense Python implementations and is
not a production-performance claim.

| Cells | Candidate physical | Candidate basis | Upwind physical |
|---:|---:|---:|---:|
| 8 | 0.239 | 0.231 | 0.095 |
| 16 | 0.194 | 0.055 | 0.084 |
| 32 | 0.244 | 0.097 | 0.110 |
| 64 | 0.361 | 0.406 | 0.201 |
| 128 | 0.642 | 1.856 | 0.646 |
| 256 | 1.492 | 12.297 | 3.008 |

The complete primary calculation took 5.24 seconds and peaked at 276.92 MiB;
fresh replay took 5.23 seconds and 250.78 MiB. Both stay below the frozen
600-second and 512-MiB caps. Source snapshots, inputs, raw fields, complete
per-case timings, commands and runtime versions are archived.

Eleven candidate tests and eleven independent analytic-reference tests pass
from maintained and archived code. Fresh-directory replay reproduces all
79 analysis files byte for byte and 5,262 numeric arrays exactly. Verification
also checks 997 protected files, 170 copied-input hashes, and 2,177 manifest
entries in 18 preceding artifacts. No production source or live D4 runtime
was edited, and no preceding failure was relabelled.

## Next bounded step

The [native segment-composition contract](native_segment_composition_contract.md)
now specifies the next prerequisite. Axial crossings subdivide radial flights;
native tabulated T/B/D coefficients must first be checked for partition
compatibility, with exact and native-kernel changes measured separately.
The one-dimensional slab success cannot establish that property.

Only after that audit can a geometry-specific retained-direction crossing
scheme be specified and tested against native zero-gradient responses,
common radial white return and current balance. The prior native spatial
failure, full coupled-reference qualification and production readiness all
remain unresolved.
