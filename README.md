# SPOT: Synthesis Proper Orthogonal Decomposition

SPOT is a reduced-order iterative 2D/1D neutron-transport method. A fixed POD
space represents radial dependence, online 2D fixed-source solves update the
radial response, and a reduced 1D axial solve returns axial leakage. The final
goal is one self-consistent state, not a prescribed number of iterations.

The active method is deliberately small:

- one volume-weighted POD basis, fixed during the iteration;
- online radial transport at every outer step;
- one reduced axial solve;
- direct Picard substitution;
- no fitted closure, relaxation, damping, clipping, flux floor, CMFD
  correction, or empirical coupling coefficient.

## Equations

For energy group $g$, construct the fixed radial basis from snapshots:

$$
W^{1/2}P_g=U_g\Sigma_g Z_g^T,
\qquad B_g=W^{-1/2}U_{g,1:r_g}.
$$

The coupled state is

$$
x=(a,\rho,L),\qquad \rho=1/k,
$$

where $a$ contains the POD coordinates and $L$ is the plane-wise axial
leakage. Given $x$, each radial plane solves

$$
[\mathcal A_\perp(L)-\mathcal S_\perp]u^+
=\rho\,\mathcal F(Ba).
$$

Fission is frozen during that fixed-source solve. The new radial response is
projected into the same basis, the axial problem is solved, and the returned
state defines

$$
x^+=G(x).
$$

The current nonlinear method is simply

$$
x^{m+1}=G(x^m).
$$

Writing an $\alpha=1$ would add notation but no method. The rank $r$ is the
number of retained radial basis functions; it is a discretization order, not
a fitted physical parameter.

The concise derivation is in
[SPOT_doc/rederivation.md](SPOT_doc/rederivation.md).

## Convergence contract

For one raw map $x^+=G(x)$, SPOT reports three separate defects:

$$
R_\rho=|\rho^+-\rho|,
$$

$$
R_L=
\frac{\lVert L^+-L\rVert_\infty}
{\max(\lVert L^+\rVert_\infty,\lVert L\rVert_\infty)},
$$

$$
R_a^2=
\frac{\sum_{s,g}H_s\Delta a_{s,g}^TM_g\Delta a_{s,g}}
{\sum_{s,g}H_s(a^+_{s,g})^TM_ga^+_{s,g}}.
$$

All three must pass the declared tolerance. They are not combined into a
tuned score. The dimensional $D_L=\lVert L^+-L\rVert_\infty$ is reported
only as a diagnostic.

An inner solve that reaches its iteration cap without satisfying the strict
terminal predicate is rejected; its last iterate is not accepted as $G(x)$.

## Current result

The fixed rank-1 trajectory has been evaluated through $x_6=G(x_5)$. Each
accepted map passed the independent fixed-basis, state, source, balance, raw
defect, and restart checks. The earlier legacy $x_3$ was superseded by the
strict-inner result shown here.

| map | $R_\rho$ | $R_L$ | $D_L\;[\mathrm{cm}^{-1}]$ | $R_a$ |
|---|---:|---:|---:|---:|
| $x_0\to x_1$ | $1.2811548\times10^{-6}$ | $7.9228532\times10^{-4}$ | $1.1616503\times10^{-6}$ | $9.2282558\times10^{-7}$ |
| $x_1\to x_2$ | $0$ | $3.9564556\times10^{-4}$ | $5.8009755\times10^{-7}$ | $7.2377835\times10^{-7}$ |
| $x_2\to x_3$ | $0$ | $4.3252643\times10^{-4}$ | $6.3417247\times10^{-7}$ | $3.2409694\times10^{-7}$ |
| $x_3\to x_4$ | $0$ | $5.6855251\times10^{-4}$ | $8.3361374\times10^{-7}$ | $1.4817206\times10^{-6}$ |
| $x_4\to x_5$ | $6.4057635\times10^{-8}$ | $3.1253506\times10^{-4}$ | $4.5823981\times10^{-7}$ | $2.3143260\times10^{-7}$ |
| $x_5\to x_6$ | $0$ | $2.0941536\times10^{-4}$ | $3.0704541\times10^{-7}$ | $7.5835882\times10^{-7}$ |

At the unchanged $5\times10^{-7}$ outer gate, $x_6$ is not converged:
$R_L$ fails by a factor of 418.83 and $R_a$ fails by a factor of 1.52.
The components do not show one stable contraction.

One leakage-driven Anderson(1) candidate was also passed through the real
nonlinear map once. Its returned defects were

$$
(R_\rho,R_L,D_L,R_a)=
(6.4057635\times10^{-8},\,2.4458920\times10^{-4},\,
3.5861740\times10^{-7},\,1.1292181\times10^{-6}).
$$

Relative to direct $x_6$, $R_L$ increased by 16.8% and $R_a$ by 48.9%.
That candidate is rejected. This is not a general theorem against Anderson;
it is enough reason not to add another coefficient now.

The full concise evidence boundary is
[validation/iterative/current_result.md](validation/iterative/current_result.md).
Detailed historical scaffolding remains recoverable from the Git tag
`archive-pre-lean-20260814`.

## Validation

Run the active no-transport gate with:

```sh
make spot-fast
```

It compiles the production Picard procedure, the generic continuation decks
and the independent Ganlib checker, and runs the algebra, source, state, rank,
strict-inner and continuation-contract tests. It does not launch Dragon.

The validation plan is
[SPOT_doc/validation_plan.md](SPOT_doc/validation_plan.md).

## Next scientific step

The generic continuation host is implemented and default-off. Its six parent
objects are role- and hash-locked, and its decision rule is frozen in
[validation/iterative/continuation_policy.md](validation/iterative/continuation_policy.md).
The next action is to authorize exactly one unchanged
$x_7=G(x_6)$, with no retry, relaxation or parameter change.

That result is classified only as `INVALID_MAP`, `TOLERANCE_MET` or
`VALID_NOT_MET`. It adds one datum and cannot by itself prove convergence
or divergence. No $x_8$ starts automatically. Rank, mesh and reference
studies come only after a reproducible fixed point exists.
