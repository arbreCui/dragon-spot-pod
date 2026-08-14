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

The predeclared short Stage-3 census continued through \(x_3=G(x_2)\). The
earlier third update was archived after its legacy radial inner-return path
was tightened. Its replacement used three strictly terminated online radial
solves, one fresh strictly terminated axial solve, and an independent
Ganlib-only check. The current third defect is

\[
(R_\rho,R_L,R_a)=
(0,\,4.3252643\times10^{-4},\,3.2409694\times10^{-7}).
\]

The eigenvalue and modal components pass the declared
\(5\times10^{-7}\) outer gate; leakage fails it by about a factor of 865.
Stage 3 is therefore complete with `OUTER-CONVERGENCE NOT-ESTABLISHED`, and
the replacement \(x_3\) is not accepted as a fixed point. The two map-4 decks
are prepared from the hash-frozen strict \(x_3\) and separately compile-checked.
One authorized activation reached its 75 s radial bound after a strictly
terminated plane 1 and the start of plane 2. Process-group cleanup completed,
and the axial deck was not started. A separately authorized radial-only run
then used the identical deck and inputs with a 120 s safety bound. All three
radial planes terminated strictly. A separately authorized axial-only process
then terminated strictly within 80 s. The independent Ganlib-only checker
reproduced the complete raw map and defects
\((R_\rho,R_L,R_a)=(0,5.6855251\times10^{-4},1.4817206\times10^{-6})\).
Leakage and modal defects fail the unchanged \(5\times10^{-7}\) AND gate, so
\(x_4\) is not a fixed point. A no-Dragon check of the \(x_2\to x_3\) and
\(x_3\to x_4\) updates finds modal cosine/norm ratio
`-0.7947401/4.571844` and height-weighted leakage cosine/norm ratio
`-0.7744331/1.535402`; the production leakage-infinity ratio is `1.314491`.
These are separate observed reversals with amplification, not proof of
divergence, a two-cycle, or a physical cause. One predeclared stop/go
continuation then completed strict \(x_5=G(x_4)\), with
\((R_\rho,R_L,R_a)=(6.4057635\times10^{-8},3.1253506\times10^{-4},
2.3143260\times10^{-7})\). Only leakage fails. Relative to \(x_3\to x_4\),
the \(x_4\to x_5\) modal norm ratio is `0.156192`, the height-weighted
leakage ratio is `0.731416`, and the production infinity ratio is `0.549703`.
Thus the repeated-amplification stop condition was not met, but convergence
was not established. One unchanged continuation then completed strict
\(x_6=G(x_5)\), with
\((R_\rho,R_L,R_a)=(0,2.0941536\times10^{-4},7.5835882\times10^{-7})\).
Leakage decreases but still fails, and the modal defect fails again. The
\(x_5\to x_6\) modal cosine/ratio is `-0.7987202/3.276802`; leakage remains
obtuse but contracts by `0.731538` in height-weighted \(L_2\) and `0.670054`
in the production infinity diagnostic. There is no common stable contraction,
no outer convergence result, and no \(x_7\). An
earlier read-only check of the replacement \(x_1,x_2,x_3\) sequence finds
that the modal update is acute and smaller, whereas the leakage update has a
negative height-weighted \(L_2\) cosine and a smaller aggregate norm but a
1.0932-times larger infinity diagnostic. This does not establish a whole-state
oscillation or distinguish physical-map behavior from inner-solver state
error. The two infinity maxima are unique at the same coordinate (plane-list index 1,
energy-group index 326), where the signed update changes from
`+5.8010e-7` to `-6.3417e-7`. This is a local rebound, not evidence of a
two-cycle. A subsequent no-Dragon reconstruction closes all canonical
leakages bit for bit; a separate binary64 endpoint decomposition traces
`98.695%` and `98.323%` of the hotspot numerator changes to its high-\(z\)
face. The production denominator's relative change is about 45–50 times smaller
than the numerator's and has the opposing ratio effect. This is provenance of
the observed rebound, not a physical-cause claim. A further exact radial split
finds all eight high-face region contributions nonzero and reversing sign
together; the unique largest index carries about `51.08%`, so the change is
multi-region rather than a single-region anomaly. At the same interface, both
the adjacent scalar-flux ratio and the signed current divided by the adjacent
mean flux reverse their update sign in all eight rows. These two dimensionless
ratios are invariant to a common state normalization; all face currents
themselves retain the same negative direction. No Fick coefficient or causal
model is inferred.

Earlier one-shot, REAL64-forensics, and B2 lifecycle files are historical
records only. They are not prerequisites of this plan and are not run by the
active fast gate.
