# x6--x8 residual-direction audit

## Scope

This is a read-only, no-transport audit of two actual direct-map residuals:

$$
f_6=x_7-x_6,\qquad f_7=x_8-x_7.
$$

The three canonical axial states are locked in
[residual_direction_inputs.tsv](residual_direction_inputs.tsv):

| state | SHA-256 |
|---|---|
| x6 | `e54f48fc47e34679ba9ee671d0b96d377d0193b0303e770fd98c2fbe1889c01f` |
| x7 | `e7f7f4e8d7d296a943c10a419052cffe7970eeff017eb76428276d29124f0fee` |
| x8 | `6f20dc5b521b55ed3e9e66590f85876f5e458d7b79a219e2c1f68534ee7d72a5` |

The Ganlib-only checker first reproduces the x6--x7 and x7--x8 saved defects
bit for bit and requires the canonical dimensions, rank, offsets, basis,
Gram matrix, plane heights and normalization to remain fixed. It neither
writes an XSM object nor links or starts Dragon.

Run the audit with:

```sh
sh validation/iterative/run_residual_direction_audit.sh
```

## Separate direction diagnostics

No angle is formed across the mixed-unit $(\rho,L,a)$ state.

| block and metric | $\lVert f_6\rVert$ | $\lVert f_7\rVert$ | $\langle f_6,f_7\rangle$ | cosine |
|---|---:|---:|---:|---:|
| modal, $H_sM_g$ | 1.005566600915272e-7 | 1.784399682012027e-7 | -5.649691149855252e-15 | -0.3148630729242121 |
| leakage, height-$L_2$ | 8.989819701790565e-6 | 1.004715931809631e-5 | -8.758075956921188e-11 | -0.9696487385229673 |

The height-$L_2$ leakage row is an auxiliary, non-production diagnostic. Its
height is fixed geometry, not a fitted weight. It does not replace $R_L$ or
enter the stopping rule.

The production infinity-norm evidence is:

- $D_L$ changes from $4.474131856113672\times10^{-7}$ to
  $5.549518391489983\times10^{-7}\ \mathrm{cm}^{-1}$;
- $R_L$ changes from $3.051509350802849\times10^{-4}$ to
  $3.784961167028899\times10^{-4}$;
- both $D_L$ maxima are unique at plane 3, energy group 325;
- the hotspot update changes from
  $-4.474131856113672\times10^{-7}$ to
  $+5.549518391489983\times10^{-7}$, so it reverses sign and grows by
  24.035647% in magnitude.

The modal saved defects change from
$R_a=1.506394461464391\times10^{-7}$ to
$2.673129764390890\times10^{-7}$. The stored inverse-eigenvalue increments
are $-6.405763486316829\times10^{-8}$ and
$+6.405763486316829\times10^{-8}$; their exact symmetry is limited by the
binary32 `K-EFFECTIVE` representation.

## Scientific decision

The last two leakage residuals are nearly opposite in the auxiliary
height-$L_2$ view, while the production maximum remains at the same unique
component, reverses sign and grows. The modal residuals are also obtuse and
the second modal norm is larger.

This is a local two-residual observation. It does not establish a two-cycle,
divergence, a stable negative eigenvalue, a Jacobian spectrum, rank adequacy,
a physical cause, an inner-error bound or reference accuracy. No residual
ratio is promoted to an asymptotic convergence factor; no coefficient,
combined score or new acceptance threshold is fitted.

The evidence is sufficient to motivate a separately declared nonlinear-solver
study on the unchanged map $F(x)=G(x)-x$. It does not select, tune or authorize
that solver, and it does not define x9.
