# SPOT validation plan

Validation follows the dependencies of the method. A later benchmark cannot
repair an incorrect source, state, map, or unconverged inner solve.

## 1. Algebra and interface gate

Without transport execution, verify:

- volume-weighted POD construction, reconstruction and rank behavior;
- $p=Ba$ and the stored Gram metric;
- frozen fission source $\mathcal F(Ba)/k$;
- final off-group scattering with no second fission evaluation;
- radial-response and leakage signs;
- canonical state $x=(a,1/k,L)$;
- separate $(R_\rho,R_L,R_a)$ defects;
- direct substitution and the three-component AND stopping rule;
- fail-closed radial and axial inner iteration caps.

Status: PASS. Run with `make spot-fast`.

## 2. One real map

For one frozen input, evaluate $x^+=G(x)$. Require:

- strict radial and axial inner terminals;
- finite positive physical flux;
- radial source identity and balance;
- unchanged POD basis and rank;
- independently recomputed defects;
- consistent restart leakage ordering.

Status: PASS for the accepted real-map records through the final x8. The x8
classification is `VALID_NOT_MET`; its independent checker and publication
receipt both pass.

## 3. Fixed-point iteration

Run direct updates

$$
x_{m+1}=G(x_m)
$$

without relaxation or parameter changes. At every step report all three
defects. If any inner solve fails its strict terminal, $G(x_m)$ was not
evaluated and the run fails closed. If all three outer defects do not pass,
the last state is not a converged solution.

Status: DIRECT CENSUS COMPLETE, NOT CONVERGED through x8. The final result is

$$
(R_\rho,R_L,R_a)=
(6.4057635\times10^{-8},\,
3.7849612\times10^{-4},\,
2.6731298\times10^{-7})
$$

at an outer tolerance of $5\times10^{-7}$.

A single real leakage-Anderson candidate worsened the leakage and modal
defects relative to direct $x_6$; it is rejected. No empirical damping or
untested second Anderson candidate is authorized.

Next: stop direct Picard. The predeclared x8 endpoint was evaluated once and
no x9 is defined. First inspect the stored x6--x8 residual directions offline,
without transport or fitted coefficients. Any later nonlinear-solver study
must be declared separately for the same $F(x)=G(x)-x$ and may not alter the
physical map.

## 4. Numerical qualification

Only after a reproducible fixed point exists, vary one choice at a time:

1. POD rank;
2. radial and axial meshes;
3. angular quadrature;
4. energy groups;
5. inner solver tolerances.

Rank is accepted only when the self-consistent state and declared observables
are stable under rank increase. It is never calibrated to a desired answer.

## 5. Reference validation

Compare the numerically qualified SPOT fixed point with an independent
higher-fidelity transport reference using predeclared observables such as
eigenvalue, plane power, axial shape and reaction rates. Keep equation and
iteration errors separate from model-to-reference differences.

The concise current evidence is
[../validation/iterative/current_result.md](../validation/iterative/current_result.md).
Historical diagnostics are preserved at Git tag
`archive-pre-lean-20260814`.
