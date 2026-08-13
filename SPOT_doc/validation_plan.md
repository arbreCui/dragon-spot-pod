# SPOT validation plan

Validation follows the dependencies of the method. A later benchmark cannot
repair an incorrect source, state, map, or unconverged inner solve.

## 1. Algebra and interface gate

No transport execution is needed. Verify:

- volume-weighted POD construction, reconstruction, and rank behavior;
- $p=Ba$ and the stored Gram metric;
- frozen fission source $\mathcal F(Ba)/k$;
- final off-group scattering with no second fission evaluation;
- radial-response and leakage signs;
- canonical state $x=(a,1/k,L)$;
- the three independent defects $(R_\rho,R_L,R_a)$;
- direct substitution and the three-component AND stopping rule;
- fail-closed radial and axial inner iteration caps.

This gate is active and runs in a few seconds:

```sh
make spot-fast
```

## 2. One real map

From one frozen input $x_0$, evaluate exactly

\[
x_1=G(x_0).
\]

Require:

- all radial and axial inner solvers satisfy their declared strict terminal
  predicates;
- positive finite physical flux;
- the radial fixed-source identity and radial balance;
- the axial Galerkin residual and global balance;
- unchanged POD basis and rank;
- independently recomputed $(R_\rho,R_L,R_a)$;
- a fresh replay from the same input reproduces the scientific state.

This stage proves one map evaluation, not outer convergence.

## 3. Short Picard census

Only after Stage 2 passes, run a small predeclared number of direct updates

\[
x_{m+1}=G(x_m)
\]

without relaxation or parameter changes. Report all three defects at every
step. Classify the defect magnitudes as decreasing, stationary, increasing,
or nonmonotone component by component. A claim about oscillatory direction
requires consecutive signed updates under a predeclared physical inner
product; defect magnitudes alone cannot establish it. Do not fit a
contraction factor and do not retry a failed inner solve.

If all three defects reach the predeclared outer tolerance, independently
recompute one final raw map $G(x)-x$. Otherwise report `NOT CONVERGED`; the
last iterate is not a converged solution.

## 4. Discretization and numerical qualification

After a reproducible fixed point exists, vary one numerical choice at a time:

1. POD rank;
2. radial and axial spatial meshes;
3. angular quadrature;
4. energy groups;
5. inner solver tolerances.

Rank is accepted only when observables and the self-consistent state are
stable under rank increase. No rank is chosen by calibration to a desired
answer.

## 5. Reference comparison

Compare the qualified SPOT solution with a higher-fidelity transport
reference using predeclared observables such as eigenvalue, plane power,
axial shape, and reaction rates. Keep verification errors (equations and
iteration) separate from validation differences (model versus reference).

## Current boundary

Stages 1 and 2 pass. The current one-map calculation used a hash-locked
initial state, three online radial solves and one returned axial solve. Each
process had a 75 s process timeout with a 5 s termination grace, all four inner
solves reached strict termination, and an independent Ganlib-only checker
reproduced the physical state and raw defect.

The predeclared short Stage-3 census continued through \(x_3=G(x_2)\). Both
continuations pass the same strict inner and independent-state checks. The
second update reduced all three dimensionless defects, but the third
increased the leakage and modal defects. The observed direct trajectory is
nonmonotone; Stage 3 is complete with `OUTER-CONVERGENCE NOT-ESTABLISHED`,
and \(x_3\) is not accepted as a fixed point.

The frozen consecutive modal increments are obtuse under the fixed
Gram-height inner product, but this is only stored-update geometry. The inner
termination record supplies no state-error bound, so the available data do
not distinguish physical map behavior from numerical contamination.

Earlier one-shot, REAL64-forensics, and B2 lifecycle files are historical
records only. They are not prerequisites of this plan and are not run by the
active fast gate.
