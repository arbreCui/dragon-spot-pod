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

The fixed rank-1 trajectory has been evaluated through the predeclared final
$x_8=G(x_7)$. Each
valid map evaluation passed the independent fixed-basis, state, source, raw
defect and restart checks; balance diagnostics are reported separately. The
earlier legacy $x_3$ was superseded by the strict-inner result shown here.

| map | $R_\rho$ | $R_L$ | $D_L\;[\mathrm{cm}^{-1}]$ | $R_a$ |
|---|---:|---:|---:|---:|
| $x_0\to x_1$ | $1.2811548\times10^{-6}$ | $7.9228532\times10^{-4}$ | $1.1616503\times10^{-6}$ | $9.2282558\times10^{-7}$ |
| $x_1\to x_2$ | $0$ | $3.9564556\times10^{-4}$ | $5.8009755\times10^{-7}$ | $7.2377835\times10^{-7}$ |
| $x_2\to x_3$ | $0$ | $4.3252643\times10^{-4}$ | $6.3417247\times10^{-7}$ | $3.2409694\times10^{-7}$ |
| $x_3\to x_4$ | $0$ | $5.6855251\times10^{-4}$ | $8.3361374\times10^{-7}$ | $1.4817206\times10^{-6}$ |
| $x_4\to x_5$ | $6.4057635\times10^{-8}$ | $3.1253506\times10^{-4}$ | $4.5823981\times10^{-7}$ | $2.3143260\times10^{-7}$ |
| $x_5\to x_6$ | $0$ | $2.0941536\times10^{-4}$ | $3.0704541\times10^{-7}$ | $7.5835882\times10^{-7}$ |
| $x_6\to x_7$ | $6.4057635\times10^{-8}$ | $3.0515094\times10^{-4}$ | $4.4741319\times10^{-7}$ | $1.5063945\times10^{-7}$ |
| $x_7\to x_8$ | $6.4057635\times10^{-8}$ | $3.7849612\times10^{-4}$ | $5.5495184\times10^{-7}$ | $2.6731298\times10^{-7}$ |

At the unchanged $5\times10^{-7}$ outer gate, the final x8 is
`VALID_NOT_MET`: $R_\rho$ and $R_a$ pass at 0.128115 and 0.534626 times
the tolerance, but $R_L$ fails by a factor of 756.992233. Relative to x7,
x8 $R_L$, $D_L$ and $R_a$ increased by 24.0357%, 24.0356% and 77.4522%,
respectively. These changes do not establish divergence or a cycle; they do
establish that the predeclared direct rank-1 census ended without satisfying
the discrete fixed-point gate.

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
strict-inner, continuation and nonlinear-solver contract tests. It does not
launch Dragon.

The validation plan is
[SPOT_doc/validation_plan.md](SPOT_doc/validation_plan.md).

## Next scientific step

The valid x8 publication is independently checked and hash-receipted. The
direct rank-1 Picard census is complete, and no x9 is defined. The retained
x7 parent manifest is the frozen provenance for reproducing x8, not an
authorization to continue the sequence.

The transport-free x6--x8 residual-direction audit is complete. The last two
leakage updates have auxiliary height-$L_2$ cosine $-0.969649$, and their
unique production $D_L$ hotspot stays at plane 3, group 325 while reversing
sign and increasing in magnitude. The modal $H_sM_g$ cosine is $-0.314863$.
These are local observations, not a new acceptance score or proof of a cycle.
Full values and input hashes are in
[validation/iterative/residual_direction_result.md](validation/iterative/residual_direction_result.md).

The nonlinear-solver boundary is now declared in
[validation/iterative/nonlinear_solver_contract.md](validation/iterative/nonlinear_solver_contract.md).
It preserves the map, basis, rank, tolerances and three-component gate, and
requires a fresh strict $G$ evaluation for every proposed state. Full exact
Newton is tested only as a parameter-free manufactured-problem oracle. The
current real map has no validated exact Jacobian, so this result does not
authorize production Newton/JFNK or another transport run. A minimal
finite-difference probe additionally shows that the same linear manufactured
direction yields quotients $0$, $1$ and $4/3$ across three binary32-scale
perturbations. This establishes a publication-resolution obstruction, not a
general failure of JFNK. Rank, mesh and reference studies remain downstream
of a reproducible fixed point.

The frozen real snapshot spectra have also been censused without transport.
The worst optimal within-group reconstruction error falls from 1.5004% at
rank 1 to 0.03408% at rank 2, while all 370 groups retain numerical rank 3.
This is an offline representation diagnostic only: it does not explain the
Picard result, qualify rank 2 or alter the active basis. Reproduce it with
`make spot-rank-census` when the local hash-locked basis artifact is present;
details are in
[validation/iterative/rank_census_result.md](validation/iterative/rank_census_result.md).

The genuine rank-2 trial space has now also been rebuilt from the same three
original raw snapshots. A fresh rank-1 control reproduces the locked rank-1
POD fields bitwise; the rank-2 first-mode prefix, all singular values and two
repeated rank-2 builds are likewise bitwise consistent. An independent
Ganlib-only checker recomputes the stored reconstruction and volume-Gram
diagnostics without linking the SVD path. This creates only a local,
Git-ignored, inactive basis package: Dragon, assembly, transport and Picard
were not run, so no convergence or physical-accuracy conclusion follows.
Reproduce it with `make spot-rank2-basis`; details are in
[validation/iterative/rank2_basis_result.md](validation/iterative/rank2_basis_result.md).
