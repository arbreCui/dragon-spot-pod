# Self-consistent SPOT validation plan

The target is the fixed-space iterative method in
`SPOT_doc/rederivation.md`. Validation proceeds in dependency order. A later
comparison cannot repair a failed equation, map, residual, or inner solve.

This validation starts from a clean evidence boundary. Results from previous
one-shot or dynamic-basis routes are not inherited as qualification evidence.

## Stage 0 — freeze the equations

Before any new transport run, require the implementation contract to state:

- one offline, volume-weighted POD basis \(B\), fixed during iteration;
- outer state \(x=(a,\rho,L)\), with \(\rho=1/k\);
- exactly one global \(\nu\)-fission-production normalization;
- radial fission source \(F(Ba)/k\), frozen during each 2D solve;
- final off-group scattering evaluated from that radial solve's final field;
- `RADIAL-OP` constructed from this same fixed-source equation;
- direct axial leakage return from signed face-current balance;
- raw map defect \(G(x)-x\) evaluated on the variables that drive the next
  map;
- no relaxation input, fitted source, clipping, flux floor, CMFD correction,
  or reference-data feedback.

The active source now implements this contract. `SPOT-QFISS` stores the frozen
fission source, `SPOQFS` adds only final off-group scattering, `FIXB` preserves
the offline POD package, and explicit `SPOPROJ FIXB` feeds the next map from
\(Ba\). Static, manufactured, and no-transport LCM runtime subgates pass.
This Stage-0 result does not imply that a transport map or outer iteration has
passed.

## Stage 1 — algebra and sign tests

Retain the existing weighted-POD and modal-identity tests, then add small
independent fixtures for:

1. \(B^TWB=I\) and projection/reconstruction;
2. the radial fixed-source identity

   \[
   q_{\rm FS}=F(Ba)/k+S_{\rm off}(u_\perp);
   \]

3. the closure

   \[
   d_\perp=-\Sigma_t+\Sigma_{s0}
            +q_{\rm FS}/u_\perp-L;
   \]

4. the sign of positive axial loss in both radial removal and the returned
   leakage;
5. exact agreement between the production and independent formulas on a
   synthetic multigroup problem;
6. fail-closed behavior for nonpositive denominators, inconsistent layouts,
   nonfinite fields, or a missing frozen-source record.

No Dragon or OpenMC calculation is needed at this stage.

## Stage 2 — state, residual, and replay contract

The physical state records must contain, or deterministically reconstruct:

- the restricted axial coordinates \(a\);
- inverse eigenvalue \(\rho\);
- returned leakage \(L\);
- the axial scalar flux and face currents used to form them;
- the frozen context: basis, rank, geometry, materials, tracks, solver
  controls, executable and source hashes.

`SPOSTATE/SPOXCONV` now close the physical variables \(a,\rho,L\), use the
production binary32 restriction, and reject any stored basis-bit change. The
full restart/replay manifest for geometry, materials, tracks, controls and
implementation hashes is still pending and is required before this formal
stage is complete.

For the same input \(x\), a fresh map replay must produce identical scientific
records. The checker independently recomputes

\[
R_\rho=|\rho^+-\rho|,
\]

\[
R_L=
\frac{\|L^+-L\|_\infty}
{\max(\|L^+\|_\infty,\|L\|_\infty)},
\]

and

\[
R_a=\frac{\|B(a^+-a)\|_V}{\|Ba^+\|_V}.
\]

The all-zero leakage case is an exact branch. Formal state records are already
stored at the declared \(\nu\)-fission-production normalization, so the map
defect performs no additional scale fit.

## Stage 3 — one corrected map evaluation

Construct \(x_0\) once from the frozen offline seed and fixed basis. The
initializer axial solve is archived separately. Then run one corrected
fixed-space map:

```text
x1 = G_h(x0)
```

This calculation contains exactly:

- three synchronous radial fixed-source solves;
- one reduced axial eigenvalue solve;
- one direct leakage return.

Require for every inner solve:

- strict declared terminal state;
- positive finite physical flux;
- the radial fixed-source balance using \(q_{\rm FS}\);
- the axial Galerkin equation residual;
- finite global and group balance diagnostics;
- a complete output state and independent raw-defect replay.

This stage validates one map evaluation. It does not claim outer convergence.

## Stage 4 — inner-tolerance sensitivity

From exactly the same frozen input \(x_0\), evaluate

```text
x1_h   = G_h(x0)
x1_h2  = G_h2(x0)
```

where \(h/2\) is the predeclared systematic tolerance refinement. Report

\[
D_{\rm out}=d(x_{1,h},x_0)
\]

as the outer map defect and

\[
D_{\rm in}=d(x_{1,h/2},x_{1,h})
\]

as inner-solver sensitivity.

`D_in` is neither an outer residual nor a rigorous error bound. It is not
subtracted from `D_out`, fitted into a correction, or used to choose a
relaxation factor. If the two scales cannot be separated, the result is
`UNRESOLVED`.

## Stage 5 — direct Picard convergence

Only after Stages 0--4 pass may the direct update

\[
x^{(m+1)}=G(x^{(m)})
\]

be run beyond one return.

The trajectory protocol must predeclare:

- the maximum number of returns;
- inner solver controls;
- separate acceptance targets for \(R_\rho\), \(R_L\), and \(R_a\);
- strict inner residual, balance and positivity gates;
- a restart/checkpoint policy;
- no rank changes, relaxation trials, or reference comparisons during the
  trajectory.

A state is accepted only after a raw map evaluation from that state meets all
outer and inner gates. Completing the maximum iteration count is not
convergence.

If direct Picard does not converge, do not tune an empirical \(\alpha\). The
fixed-point equation \(G(x)-x=0\) and its verified raw defect remain
authoritative. Any nonlinear acceleration is a separately frozen numerical
solver and must be validated against the unmodified raw map.

## Stage 6 — discretization qualification

After one coupled state is accepted, repeat independent studies of:

- POD rank;
- snapshot set;
- radial and axial spatial meshes;
- radial and axial angular order;
- scattering order;
- inner and outer numerical tolerances.

Rank is selected from predeclared discretization evidence, not from agreement
with OpenMC. The former one-shot `QUALIFIED-R1` result does not automatically
qualify rank one for the iterative equations.

## Stage 7 — independent 3D validation

Only a converged, discretization-qualified iterative state may receive a new
3D accuracy comparison.

At minimum report scale-invariant:

- \(k_{\rm eff}\);
- normalized axial and radial reaction-rate shapes;
- complete multigroup scalar-flux shape where matching tallies exist;
- plane-wise leakage

  \[
  L_{s,g}=
  \frac{I^{\rm upper}_{s,g}-I^{\rm lower}_{s,g}}
       {\int_{V_s}\phi_g\,dV}.
  \]

OpenMC current tallies are already area-integrated and flux tallies are
already volume-integrated; neither is multiplied by geometry a second time.
Energy order, plane orientation and radial-region order must be verified with
an independent small fixture before the production comparison.

No previous statepoint or trajectory closes this stage. Matching 3D current
and flux tallies must be generated only after the iterative SPOT state has
passed Stages 0--6.

## Evidence boundary

Only checks generated by the current fixed-space source and frozen protocol
may qualify the method. Earlier results may motivate tests, but they are not
counted as passed gates.
