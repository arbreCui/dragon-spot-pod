# Offline Anderson(1) component screens

This check reads the frozen strict \(x_4,x_5,x_6\) states and does not call
Dragon or write a candidate state. With fixed-basis modal coordinates
\(a_i\), define

\[
f_4=a_5-a_4,\qquad f_5=a_6-a_5,
\]

and use the existing Gram-height inner product. The single coefficient is
the unique, unclipped least-squares value

\[
\gamma=
\frac{\langle f_5-f_4,f_5\rangle_{HG}}
     {\lVert f_5-f_4\rVert_{HG}^2},\qquad
a_A=\gamma a_5+(1-\gamma)a_6.
\]

There is no fitted damping or relaxation coefficient. Depth one and the
modal metric are declared algorithm choices.

The frozen data give

```text
gamma                              0.7868687504961641
weight on x6                       0.2131312495038359
||f4||_HG                          1.544886893195163e-7
||f5||_HG                          5.062288215163166e-7
linearized residual norm           7.393723863024349e-8
linearized residual / ||f5||       0.1460549765001090
```

The coefficient is a convex combination. Direct reconstruction of
\(B a_A\) is finite and strictly positive at all 8,880 group/plane/radial
points, without a floor or tolerance. The minimum is
\(1.750004465980173\times10^{-15}\) at group 370, plane 3, radial region 2.

The same coefficient was then applied to the other canonical components,
without combining their units. The affine pair

\[
x_I=\gamma x_4+(1-\gamma)x_5,\qquad
x_A=\gamma x_5+(1-\gamma)x_6
\]

was evaluated with the unchanged separate production-defect definitions:

```text
                         affine pair          current x6
R_rho                    5.0404951102e-8       0
R_L                      2.1899622579e-4       2.0941536233e-4
D_L                      3.2109290110e-7       3.0704541132e-7 cm^-1
R_a                      1.1076207468e-7       7.5835881646e-7
leakage height-L2        6.3541473470e-6       6.2849962241e-6
```

The screening rule introduces no new tolerance: a component already below
the declared \(5\times10^{-7}\) gate must remain below it, while a failing
component must strictly improve. The eigenvalue component is reintroduced
from its current stored zero residual to \(5.04\times10^{-8}\), so it is
relatively worse but remains below the gate. The modal component improves.
The stored zero comes from identical binary32 `K-EFFECTIVE` values and is
not evidence that the underlying continuous eigenvalues are exactly equal.
Leakage grows by 1.10% in the non-production height-\(L_2\) diagnostic and
by 4.58% in the production \(R_L/D_L\) metrics, so leakage fails. The
complete affine canonical candidate is rejected and no XSM state is written.

This remains a secant-model diagnostic. It does not evaluate
\(G(x_A)-x_A\), establish axial balance, or establish convergence. It also
does not show that Anderson acceleration is generally invalid; it rejects
only this modal-selected coefficient on these frozen states.

## Single leakage-driven alternative

Because leakage is the only persistent failing component, one predeclared
alternative determines the coefficient from its height-weighted residual:

\[
\gamma_L=
\frac{\langle f_5^L-f_4^L,f_5^L\rangle_H}
     {\lVert f_5^L-f_4^L\rVert_H^2}
=0.3898692835066931.
\]

No coefficient search, clipping, or added tolerance is used. Applying this
same coefficient to the complete canonical affine pair gives

```text
R_rho                         2.4974104229e-8
R_L                           1.4300849401e-4
D_L                           2.0967946848e-7 cm^-1
R_a                           3.9438537826e-7
leakage height-L2/current     0.6329022855
R_L/current                   0.6828939979
minimum reconstructed B*a     1.7500053319e-15
```

All three unchanged component screens pass and the reconstructed field is
strictly positive. The small positive minimum is not a numerical robustness
margin and does not establish positivity of the complete axial unknown
vector. The leakage defect improves but remains far above the
\(5\times10^{-7}\) convergence gate, by a factor of about 286. This makes
the coefficient eligible for one separately authorized bounded physical-map
evaluation; it is not a converged state or evidence that the true nonlinear
map will improve.

Reproduce the read-only check with

```sh
sh validation/iterative/run_anderson1_modal_check.sh
```

The input hashes are frozen in `anderson1_modal_scientific.sha256`.
