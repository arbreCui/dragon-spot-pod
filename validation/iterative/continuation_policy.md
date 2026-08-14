# Continuation decision rule

The three decision predicates below were frozen before evaluating
$x_7=G(x_6)$ and apply unchanged to any separately authorized final
$x_8=G(x_7)$. The numerical method, rank, basis and all solver tolerances
also remain unchanged.

The outer tolerance is

$$
\varepsilon=5\times10^{-7}.
$$

Exactly one of three outcomes is reported:

- **INVALID_MAP**: a radial or axial inner solve misses its strict terminal
  predicate, a required value is non-finite, or an independent contract check
  fails. No candidate is published. This says that the requested $G(x)$ was
  not evaluated; it is not evidence that Picard diverges.
- **TOLERANCE_MET**: the map is valid and
  $R_\rho\le\varepsilon$, $R_L\le\varepsilon$ and
  $R_a\le\varepsilon$. This meets only the predeclared discrete stopping
  rule; it does not establish rank adequacy or physical accuracy.
- **VALID_NOT_MET**: the map is valid but at least one of those three defects
  exceeds $\varepsilon$. $D_L$ and balance values remain diagnostics and
  do not enter the decision.

No defect ratio, monotonicity test or improvement threshold is used. The
runner never starts another map automatically. A possible $x_8$ requires a
separate authorization, uses the identical map and parameters once, and ends
the direct census; there is no automatic $x_9$.
