# One continued rank-2 map decision rule

This stage evaluates exactly one direct map
$x^{(2)}_2=G_2(x^{(2)}_1)$, where $x^{(2)}_1$ is the valid but
tolerance-not-met candidate from the first rank-2 map. The rank-2 basis,
equations and solver tolerance remain unchanged.

The outer tolerance is

$$
\varepsilon=5\times10^{-7}.
$$

The map contains three online frozen-fission radial solves followed by one
axial solve. It uses direct substitution and contains no retry, relaxation,
damping, fitted closure, clipping or empirical coefficient. The 120-second
radial and 420-second axial host limits are operational process bounds, not
model or convergence parameters.

Exactly one outcome is reported:

- **INVALID_MAP**: a strict inner terminal, physical value, provenance check
  or independent audit fails; no candidate is published.
- **TOLERANCE_MET**: the map is valid and its separate rank-2 defects satisfy
  $R_\rho\leq\varepsilon$, $R_L\leq\varepsilon$ and
  $R_a\leq\varepsilon$.
- **VALID_NOT_MET**: the map is valid but at least one of those three defects
  exceeds $\varepsilon$.

$D_L$ and balance quantities remain diagnostics. Defect ratios and update
directions may be described only after a valid map and do not enter its
acceptance. This one additional map can show whether the observed update
shrinks, reverses or persists locally; it cannot establish asymptotic
convergence, stability, rank adequacy or physical accuracy. No third rank-2
map is started automatically.
