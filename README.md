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

One separately declared rank-2 sensitivity map was then attempted from the
same raw x7 axial solution.  The radial half completed with all three strict
fixed-source terminals.  The host wrapper reported an 80-second timeout; the
durable axial log establishes only that execution entered `FLU` and produced
no terminal or normal end.  No axial candidate, raw defects, independent map
audit or result publication exists, so the classification is `INVALID_MAP`
(reported reason `TIMEOUT_BEFORE_TERMINAL`), not physical nonconvergence.  The
successful radial staging is retained locally under a hash receipt; no run is
retried or continued automatically.  See
[validation/iterative/rank2_map_attempt_result.md](validation/iterative/rank2_map_attempt_result.md).

A separate default-off axial-only host was frozen to consume that exact radial
staging without rerunning a radial equation.  It permits one unchanged axial solve
under a 420-second operational wall bound, followed by the same independent
rank-2 audit.  The separately authorized run completed normally and passed
the independent checker. Its scientific classification is `VALID_NOT_MET`:
the map is valid, but the stopping-rule defects $R_\rho$, $R_L$ and $R_a$
all exceed `5.0e-7`. This
establishes rank sensitivity at the frozen x7 parent, not rank adequacy,
iteration convergence or physical accuracy. The first operational attempt
remains `INVALID_MAP`; see
[validation/iterative/rank2_axial_only_result.md](validation/iterative/rank2_axial_only_result.md).

A subsequent read-only Ganlib audit partitions that valid rank-2 update
exactly in the stored Gram metric. The mode-2 diagonal term is `77.53%` of
the update numerator while it is about `0.003582%` of the current state
Gram-metric squared norm; the net signed cross share is `2.35e-9`. This
basis-dependent partition locates the large modal response, but does not
establish instability, rank adequacy or physical accuracy. See
[validation/iterative/rank2_mode2_anatomy_result.md](validation/iterative/rank2_mode2_anatomy_result.md).

The one direct rank-2 continuation
$x^{(2)}_2=G_2(x^{(2)}_1)$ has now also completed. It consumed the valid but
tolerance-not-met candidate without re-encoding and passed every strict and
independent validity gate. All three stopping defects decreased, but the map
remains `VALID_NOT_MET`. The full modal updates have local norm ratio
`0.864118` and cosine `-0.874929`; the basis-dependent, $G_{22}$-restricted
mode-2 updates have ratio `0.932560` and cosine `-0.915973`. Thus both are
strongly anti-aligned and shrink only modestly, while the leakage defect falls
sharply. This does not prove a cycle, convergence or divergence, and no third
rank-2 map is defined. See
[validation/iterative/rank2_next_map_result.md](validation/iterative/rank2_next_map_result.md).

The next solver study is reduced to one formula, without transport or a new
iterate. A modal-projected Anderson(1) screen in the full Gram-height
metric gives the unique least-squares weight `0.5388643265136009` on the
latest rank-2 state and
`0.4611356734863991` on the preceding state. The same scalar would act on
the complete coupled state, while its coefficient is formed only in the
physical POD modal metric, so no mixed-unit whole-state norm or empirical
relaxation parameter is introduced. That state has now been deterministically
published as a hash-locked AX proposal plus an explicitly labelled x2 raw-flux
snapshot carrier. An independent Ganlib-only checker verifies the fixed basis,
publication arithmetic, carrier identity and strict positivity at all 8880
reconstructed points. Its classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: it is not a map evaluation or
convergence evidence. See
[validation/iterative/rank2_solver_decision.md](validation/iterative/rank2_solver_decision.md)
and
[validation/iterative/rank2_modal_aa1_candidate_result.md](validation/iterative/rank2_modal_aa1_candidate_result.md).

That proposal has now been tested by exactly one fresh strict map
$z=G_2(y_{\rm pub})$. All three radial terminals, the axial terminal, the
independent fixed-basis/defect/restart audit and the full checksum receipt
pass. The result is nevertheless `VALID_NOT_MET`:
$R_\rho=6.57635\times10^{-5}$, $R_L=2.26566\times10^{-3}$ and
$R_a=4.66468\times10^{-4}$, all above `5.0e-7`. The three components are
locally smaller than for the direct second rank-2 map, but one cross-input
comparison is not a convergence factor or proof of Anderson superiority,
rank adequacy or physical accuracy. No retry or subsequent map was started;
see
[validation/iterative/rank2_modal_aa1_map_result.md](validation/iterative/rank2_modal_aa1_map_result.md).

The next AA(1) history update has now been checked offline from the two actual
evaluated pairs $x_1\to x_2$ and $y_{\rm pub}\to z$. The unique weight on
$z$ is `0.9302745506696768`, so the possible next proposal is
$w=0.0697254493303232x_2+0.9302745506696768z$. Its REAL32 publication
keeps all 8880 reconstructed points strictly positive. That proposal has now
been deterministically materialized with an explicitly labelled `Z-RAW-FLUX`
carrier and independently checked down to the complete lagged SYSTEM and
fixed-source payload. Its status is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon run, new map or convergence
evidence exists. See
[validation/iterative/rank2_modal_aa1_next_history_result.md](validation/iterative/rank2_modal_aa1_next_history_result.md)
and
[validation/iterative/rank2_modal_aa1_next_candidate_result.md](validation/iterative/rank2_modal_aa1_next_candidate_result.md).
