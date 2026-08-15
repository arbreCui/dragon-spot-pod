# Nonlinear-solver contract

## Status and scope

This is a no-transport contract for studying a solver around the unchanged
SPOT map. It does not select or implement a production solver, authorize
another real map, or define $x_9$.

The root equation is

$$
F(x)=G(x)-x=0,
$$

with the same fixed POD basis, rank, state layout, source construction,
normalization, geometry, material data and strict inner terminals already
used by the accepted map evaluations. A solver may propose a state; it may
not change $G$.

## Only acceptance rule

For a proposed state $y$, first materialize the state in the exact form that
the production map consumes, giving $y_{\mathrm{pub}}$. Then evaluate one
actual strict map

$$
z=G(y_{\mathrm{pub}}).
$$

The proposal passes only when the existing three separate defects of
$(y_{\mathrm{pub}},z)$ satisfy

$$
R_\rho\leq\varepsilon,
\qquad R_L\leq\varepsilon,
\qquad R_a\leq\varepsilon.
$$

The gate remains a three-component AND. A linear prediction, residual
decrease, combined state norm, auxiliary $D_L$, or height-$L_2$ leakage
diagnostic cannot accept a state. When the gate passes, the receipt retains
both states and the classification is `TOLERANCE_MET`. The accepted state is
$y_{\mathrm{pub}}$, because the evaluated residual is
$z-y_{\mathrm{pub}}$; $z$ is the actual map return used to form that
residual, but $z$ itself has not been tested by $G(z)-z$. A failed gate is
`VALID_NOT_MET` and has no accepted state.

If the gate does not pass and another solver step is later authorized, its
base is $y_{\mathrm{pub}}$ with the already evaluated residual
$z-y_{\mathrm{pub}}$. Using $z$ as the base would silently revert to a
Picard update.

Any failed radial or axial strict terminal makes the map evaluation invalid.
It produces no residual, derivative update or accepted history, and triggers
no retry or fallback. A proposed state must be finite, have positive $\rho$
and positive reconstructed flux, and preserve the frozen basis metadata.
Clipping, floors and post-hoc repair are forbidden.

## Exact-Newton mathematical reference

The smallest parameter-free reference is the full exact-Newton step

$$
J_F(x_m)s_m=-F(x_m),
\qquad J_F(x_m)=DG(x_m)-I,
$$

$$
y_m=x_m+s_m.
$$

It has no relaxation coefficient, damping, line search, trust radius,
regularization, pseudoinverse, fitted block weight or Picard fallback. A
missing, nonfinite, dimensionally inconsistent or singular exact Jacobian
fails closed. Exact Newton is covariant under a consistent invertible linear
change of coordinates, so its mathematical definition needs no Euclidean
norm that mixes $a$, $\rho$ and $L$.

This formula is only a manufactured-problem oracle. Current SPOT provides
trusted evaluations of $G$, but not a trusted exact $DG$. Its real input path
also contains binary32 publication steps for projected flux, leakage and
effective eigenvalue. Small REAL64 perturbations can therefore publish as
the same input. A finite-difference step would add a new step-size choice and
cannot be called the exact Jacobian. JFNK would additionally introduce a
Krylov tolerance, restart and preconditioning choices, as well as many map
evaluations. None is authorized here.

## Finite-difference publication probe

This probe stops before Krylov iteration. It is not a JFNK implementation or
a production step-size rule. Let $Q$ denote materialization into the state
actually consumed by the map and define

$$
F_Q(y)=G(Q(y))-Q(y).
$$

The finite directional secant examined here is

$$
D_hF_Q(x;v)=\frac{F_Q(x+hv)-F_Q(x)}{h}.
$$

The manufactured scalar case uses $G(y)=2y$, hence the underlying smooth
residual is $F(y)=y$, with $x=v=1$. The perturbations are exactly
representable binary fractions derived from the binary32 spacing at one;
they are test fixtures, not tuned solver parameters.

| $h$ | $Q_{32}(x+hv)-Q_{32}(x)$ | published quotient |
|---:|---:|---:|
| $2^{-25}$ | $0$ | $0$ |
| $2^{-23}$ | $2^{-23}$ | $1$ |
| $3\,2^{-24}$ | $2^{-22}$ | $4/3$ |

The final row is a binary32 midpoint and uses IEEE round-to-nearest,
ties-to-even; the test asserts that platform rule explicitly.

Without publication, the same linear residual gives quotient one. Thus one
determinate perturbation is hidden, another happens to reproduce the smooth
direction, and another is distorted. This is the expected behavior of a
finite secant across a quantized publication map. In the current real path,
`SPOPROJ` converts reconstructed flux to default REAL, `K-EFFECTIVE` and
`SPOT-LEAK1D` are stored as LCM type 2, and later REAL64 state construction
cannot restore the discarded bits.

The result is only a local publication-resolution counterexample. It does
not prove that every finite-difference step fails, that JFNK is impossible,
or that real SPOT cannot converge. It does prove that a smooth binary64
finite-difference assumption is insufficient and that no GMRES/JFNK path is
authorized without a separately justified publication-aware secant policy.

## Established by the synthetic test

The seconds-scale synthetic test uses exact rational arithmetic for the
Newton algebra and exactly representable binary fractions for the publication
probe. It verifies:

- one full Newton step solves a coupled affine root and the candidate is
  checked by a fresh map evaluation;
- a zero linearized residual cannot replace the true nonlinear gate;
- every one of the three defects is necessary, including equality at the
  declared tolerance;
- consistent leakage-unit scaling gives the same physical Newton step;
- a failed map or singular Newton system fails closed;
- the same manufactured directional quotient is exact before publication
  but can be hidden or distorted by binary32 materialization;
- the modal-projected Anderson(1) scalar in the full Gram metric satisfies its
  exact least-squares normal equation, is unchanged by a common metric
  scaling, commutes with independent changes of units in the state blocks,
  and fails closed when its scalar system is singular.

The test proves only the algebra and control boundary. It does not show that
real SPOT has an exact Jacobian, that Newton is practical, that it converges,
that the rank-2 Anderson proposal improves the real residual, or that either
rank is adequate.
