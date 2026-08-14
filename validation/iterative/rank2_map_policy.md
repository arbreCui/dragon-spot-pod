# One rank-2 map decision rule

This is one rank-sensitivity evaluation, not a continuation of the frozen
rank-1 trajectory.  The same raw x7 axial solution is canonicalized by
production `SPOSTATE` in the frozen rank-2 space before any online solve.
The retained rank-1 x8 map is not rerun.

The solver tolerance remains

$$
\varepsilon=5\times10^{-7}.
$$

Exactly one map is attempted, with three online frozen-fission radial solves
and one axial solve.  There is no retry, relaxation, damping, fitted closure,
clipping or empirical coefficient.  Exactly one outcome is reported:

- **INVALID_MAP**: an inner terminal, physical value, provenance check or
  independent audit fails; no result is published.
- **TOLERANCE_MET**: the map is valid and its separate rank-2 defects satisfy
  $R_\rho\leq\varepsilon$, $R_L\leq\varepsilon$ and
  $R_a\leq\varepsilon$.
- **VALID_NOT_MET**: the map is valid but at least one of those three defects
  exceeds $\varepsilon$.

$D_L$ and balance quantities remain diagnostics.  Rank-1 and rank-2 modal
coordinates are not compared componentwise.  A valid single map establishes
only sensitivity to the retained POD order at this frozen parent; it cannot
establish rank adequacy, iteration convergence, stability or physical
accuracy against a 3D/reference transport solution.
