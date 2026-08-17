# SPOT: Synthesis Proper Orthogonal Decomposition

SPOT is a reduced-order iterative 2D/1D neutron-transport method. A fixed POD
space represents radial dependence, online 2D fixed-source solves update the
radial response, and a reduced 1D axial solve returns axial leakage. The final
goal is one self-consistent state, not a prescribed number of iterations.

The active method is deliberately small:

- one volume-weighted POD basis, fixed during the iteration;
- online radial transport at every outer step;
- one reduced axial solve;
- direct Picard as the baseline, with standard full-Gram AA(1) formed only
  from actual map residuals;
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

The baseline nonlinear iteration is simply

$$
x^{m+1}=G(x^m).
$$

When two actual residuals \(p=G(x^{m-1})-x^{m-1}\) and
\(q=G(x^m)-x^m\) are available, the tested parameter-free accelerator is

$$
\beta=\frac{\lVert p\rVert_{HG}^2-\langle p,q\rangle_{HG}}
{\lVert q-p\rVert_{HG}^2},\qquad
y=(1-\beta)G(x^{m-1})+\beta G(x^m).
$$

The same \(\beta\) acts on \((a,\rho,L)\). Only a fresh physical map
\(G(y)\) and the original three-component AND gate can accept it.

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

## Current rank-2 result

The latest bounded three-step study used the genuine fixed-rank-two map and
stopped after the promised two real evaluations:

| map | \(R_\rho\) | \(R_L\) | \(D_L\;[\mathrm{cm}^{-1}]\) | \(R_a\) |
|---|---:|---:|---:|---:|
| direct \(v\mapsto w\) | `6.4223492e-8` | `2.6358057e-4` | `3.8619328e-7` | `1.8766784e-6` |
| standard AA(1) \(y\mapsto G_2(y)\) | `6.4223481e-8` | `3.2381696e-4` | `4.7445064e-7` | `5.4687342e-7` |

Both maps are independently valid, but both are `VALID_NOT_MET` at the
unchanged \(5\times10^{-7}\) AND gate. The final AA(1) map passes
\(R_\rho\), misses \(R_a\) by about 9.37%, and still misses \(R_L\) by a
factor of 647.6. Therefore SPOT has a verified physical iteration path, but
not yet a converged rank-two fixed point. See
[the direct result](validation/iterative/rank2_qv_picard_map_result.md) and
[the final AA(1) result](validation/iterative/rank2_qsvw_aa1_map_result.md).

## Historical validation record

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

## Historical scientific record

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

The separately authorized map \(v=G_2(w_{\rm pub})\) has now run exactly once.
Its pre-Dragon `Z-RAW-FLUX` gate, three radial terminals, axial terminal,
independent audit and 21-entry receipt all pass. The classification is
`VALID_NOT_MET`:
\(R_\rho=8.34905\times10^{-7}\),
\(R_L=8.67273\times10^{-4}\), and
\(R_a=4.44166\times10^{-5}\), all above `5.0e-7`. Every component is locally
smaller than for the preceding proposal map, but this is not a convergence
factor or an accuracy claim. No retry or subsequent map was started; see
[validation/iterative/rank2_modal_aa1_next_map_result.md](validation/iterative/rank2_modal_aa1_next_map_result.md).

The newest read-only AA(1) history calculation uses the two actual pairs
\(y_{\rm pub}\to z\) and \(w_{\rm pub}\to v\). The unique full-Gram modal
weight on \(v\) is `0.956973882871698711`, giving the possible raw formula
\(u=0.0430261171283013z+0.956973882871699v\). Its denominator is strictly
positive and all 8880 publication-preflight values are strictly positive.
The affine screen ratio `0.882410` is not a map residual or convergence
factor. That formula has now been deterministically published with the
latest returned \(v\) payload and an explicit `V-RAW-FLUX` lifecycle. The
independent full-carrier and snapshot audit passes, including 8880/8880
strictly positive reconstructions. Its status is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no map or Dragon run was performed;
see
[validation/iterative/rank2_modal_aa1_u_history_result.md](validation/iterative/rank2_modal_aa1_u_history_result.md)
and
[validation/iterative/rank2_modal_aa1_u_candidate_result.md](validation/iterative/rank2_modal_aa1_u_candidate_result.md).

The separately authorized \(G_2(u_{\rm pub})\) map has now completed exactly
once. Its exact `V-RAW-FLUX` parent gate, four strict solve terminals,
independent audit and 21-entry receipt all pass. It remains `VALID_NOT_MET`:
\(R_\rho=8.34905\times10^{-7}\),
\(R_L=4.03982\times10^{-4}\), and
\(R_a=1.43357\times10^{-5}\), all above `5.0e-7`. Leakage and modal defects
decreased locally relative to the preceding map, while \(R_\rho\) increased
very slightly; this is not an asymptotic convergence claim. There was no
retry, and no successor was started automatically; see
[validation/iterative/rank2_modal_aa1_u_map_result.md](validation/iterative/rank2_modal_aa1_u_map_result.md).

A later separately authorized direct Picard continuation from that returned
state has also completed exactly once. It is valid but remains
`VALID_NOT_MET`:
\(R_\rho=6.42235\times10^{-7}\),
\(R_L=5.21752\times10^{-4}\), and
\(R_a=7.24633\times10^{-6}\). Relative to the preceding map,
\(R_\rho\) and \(R_a\) decreased by about 23.1% and 49.5%, while
\(R_L\) increased by about 29.2%. The defects are therefore not
componentwise monotone, and no convergence or accuracy claim follows. No
successor map was started; see
[validation/iterative/rank2_modal_aa1_u_next_map_result.md](validation/iterative/rank2_modal_aa1_u_next_map_result.md).

A no-Dragon REAL64 localization now explains the leakage rebound. Both
adjacent \(R_L\) denominators are the identical middle-state value
`1.46519986446946859e-3 cm^-1`; \(D_L\) increased by 29.1523%. Its unique
hotspot moved from snapshot 1/group 328 with a positive increment to snapshot
1/group 326 with a larger negative increment. This is local oscillatory
evidence, not proof of a two-cycle or its cause; see
[validation/iterative/rank2_modal_aa1_u_leakage_localization_result.md](validation/iterative/rank2_modal_aa1_u_leakage_localization_result.md).

The next no-Dragon step now uses those two genuinely consecutive Picard
maps to materialize one standard modal Anderson(1) proposal. The computed,
unclipped latest-output weight is `0.6723407962072613`, so

$$
x_{\mathrm{AA1}}=0.3276592037927387\,x_2+
0.6723407962072613\,x_3.
$$

The same scalar is applied to `(A,rho,L)`. Raw flux is not interpolated: the
proposal carries the complete latest returned \(x_3\) payload under the
truthful `X3-RAW-FLUX` marker. Its independent checker passes all 8880
strict-positivity points and the exact snapshot lifecycle. This candidate
publication stage itself did not evaluate a map and makes no convergence
claim.
See
[validation/iterative/rank2_modal_aa1_consecutive_candidate_result.md](validation/iterative/rank2_modal_aa1_consecutive_candidate_result.md).

Its default-off one-map host has now been executed once under separate
authorization, with no retry. The dedicated `proposal-x3` gate, three radial
terminals, axial terminal, independent audit and 21-entry receipt all pass.
The result is valid but not converged:

$$
(R_\rho,R_L,R_a)=
(1.2844695\times10^{-7},\,4.2083074\times10^{-4},\,
1.6578761\times10^{-6}).
$$

At `5.0e-7`, $R_\rho$ passes but $R_L$ and $R_a$ fail. The defects are
all lower than in the immediately preceding direct Picard map, but the
parents differ, so this is not a convergence factor or proof of Anderson
superiority. No successor map was started; see
[validation/iterative/rank2_modal_aa1_consecutive_map_result.md](validation/iterative/rank2_modal_aa1_consecutive_map_result.md).

The next step has now been completed offline using the two latest evaluated
residuals $p=x_3-x_2$ and
$q=x_{\mathrm{AA1}}^+-x_{\mathrm{AA1}}$. Standard modal Anderson(1) gives
the unique, unclipped coefficient `0.8591556991759952`, hence

$$
x_{\mathrm{next}}=
0.1408443008240048x_3+
0.8591556991759952x_{\mathrm{AA1}}^+.
$$

All 8880 reconstructed points are positive. The complete latest raw carrier
is preserved as `AA1-RAW-FLUX`, and the independent publication/lifecycle
audit passes. This is `MATERIALIZED_PROPOSAL_NOT_EVALUATED`: this stage
launched no Dragon and produced no new defect or convergence conclusion.
See
[validation/iterative/rank2_modal_aa1_post_candidate_result.md](validation/iterative/rank2_modal_aa1_post_candidate_result.md).

Its dedicated default-off host was then authorized exactly once, with no
retry. The strict `AA1-RAW-FLUX` preflight, three radial terminals, axial
terminal, independent audit and 21-entry receipt all pass. The result is
valid but not converged:

$$
(R_\rho,R_L,R_a)=
(6.4223481\times10^{-8},\,4.5636753\times10^{-4},\,
1.3428559\times10^{-6}).
$$

Only $R_\rho$ meets `5.0e-7`; $R_L$ and $R_a$ fail. Relative to the preceding
evaluated proposal map, the leakage defect rose about 8.44%, so the update is
not componentwise improving. This is a cross-input comparison, not a
convergence factor or proof of Anderson superiority. No successor map was
started; see
[validation/iterative/rank2_modal_aa1_post_map_result.md](validation/iterative/rank2_modal_aa1_post_map_result.md).

The two latest valid maps now define one further seconds-scale, no-Dragon
rolling AA(1) proposal:

$$
x_{\mathrm{roll}}=
0.4392205811942803x_{\mathrm{AA1}}^+
+0.5607794188057197x_{\mathrm{next}}^+.
$$

The coefficient is the unique standard Gram-height minimizer; it is naturally
convex and was not clipped or tuned. The independently checked publication
keeps all 8880 reconstructed points positive and carries the complete latest
returned raw payload as `XNP-RAW-FLUX`. This is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: the predicted modal residual reduction
is not a real stopping defect, and no Dragon or successor map was started.
See
[validation/iterative/rank2_modal_aa1_rolling_candidate_result.md](validation/iterative/rank2_modal_aa1_rolling_candidate_result.md).

Its dedicated host was then executed exactly once, with no retry. The strict
`XNP-RAW-FLUX` preflight, three radial terminals, axial terminal, independent
audit and 21-entry receipt all pass. The result is valid but not converged:

$$
(R_\rho,R_L,R_a)=
(0,\,3.6004863\times10^{-4},\,1.4537807\times10^{-6}).
$$

At `5.0e-7`, only $R_\rho$ passes. Relative to the preceding evaluated map,
$R_L$ and diagnostic $D_L$ fell about 21.1%, while $R_a$ rose about 8.26%.
Because the parents differ, this is not a convergence factor or monotone
convergence evidence. No successor proposal or map was started; see
[validation/iterative/rank2_modal_aa1_rolling_map_result.md](validation/iterative/rank2_modal_aa1_rolling_map_result.md).

Using this map and the preceding valid map, the next standard rolling AA(1)
proposal has now been materialized offline:

$$
x_{\mathrm{roll2}}=
0.7941295518990515x_{\mathrm{next}}^+
+0.2058704481009485x_{\mathrm{roll}}^+.
$$

The coefficient is the unmodified Gram-height result. Independent checks pass
the fixed rank-two publication, complete latest `XRP-RAW-FLUX` carrier, true
snapshot lifecycle and 8880/8880 positive reconstructions. Its classification
is `MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon, map, stopping defect or
convergence conclusion was produced. See
[validation/iterative/rank2_modal_aa1_rolling_next_candidate_result.md](validation/iterative/rank2_modal_aa1_rolling_next_candidate_result.md).

Its dedicated default-off host was then executed exactly once, with no retry.
The strict `XRP-RAW-FLUX` preflight, three radial terminals, axial terminal,
independent audit and 21-entry receipt all pass. The map is valid but not
converged:

$$
(R_\rho,R_L,R_a)=
(1.2844695\times10^{-7},\,4.1544793\times10^{-4},\,
7.7744807\times10^{-7}).
$$

Only $R_\rho$ meets `5.0e-7`; leakage remains the dominant failure. Relative
to the preceding different-parent map, $R_L$ rose about 15.39% while $R_a$
fell about 46.52% but still failed. This mixed comparison is not a convergence
factor or monotone-convergence claim. No retry or successor map was started;
see
[validation/iterative/rank2_modal_aa1_rolling_next_map_result.md](validation/iterative/rank2_modal_aa1_rolling_next_map_result.md).

The latest three valid map residuals were then used once in the same
Gram-height metric to materialize the standard AA(2) proposal

$$
x_{\mathrm{AA2}}=
0.7766427453x_{mathrm{next}}^+
-0.5452141528x_{mathrm{roll}}^+
+0.7685714076x_{mathrm{roll2}}^+.
$$

The finite two-by-two system has strictly positive determinant. No condition
threshold, regularization, pseudoinverse, nonnegativity constraint or fallback
was used; the negative coefficient is the unmodified standard solution.
Independent checks pass exact publication, the latest `AA2-RAW-FLUX` carrier
and 8880/8880 positive reconstructions. This is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon, map or stopping defect was
produced. See
[validation/iterative/rank2_modal_aa2_candidate_result.md](validation/iterative/rank2_modal_aa2_candidate_result.md).

Its dedicated host was then executed exactly once, with no retry. The exact
`AA2-RAW-FLUX` preflight, all four strict solve terminals, independent audit
and 21-entry receipt pass. The unchanged gate gives

$$
(R_\rho,R_L,R_a)=
(6.4223481\times10^{-8},\,5.0408973\times10^{-4},\,
1.0079586\times10^{-6}),
$$

so the classification is `VALID_NOT_MET`. Only $R_\rho$ passes `5.0e-7`;
leakage remains the dominant failure. Relative to the preceding
different-parent map, $R_\rho$ fell about 50.0%, but $R_L$ and $R_a$ rose
about 21.34% and 29.65%. This mixed comparison is not a convergence factor or
monotonicity claim. No retry, successor proposal or successor map was
started as part of that map evaluation; see
[validation/iterative/rank2_modal_aa2_map_result.md](validation/iterative/rank2_modal_aa2_map_result.md).

The three-pair AA(2) window was then shifted forward once, offline, to
\((x_{\mathrm{roll}},x_{\mathrm{roll2}},x_{\mathrm{AA2}})\). The exact
standard solve materialized

$$
x_{\mathrm{rAA2}}=
-1.2827949098x_{\mathrm{roll}}^+
+0.2370041391x_{\mathrm{roll2}}^+
+2.0457907708x_{\mathrm{AA2}}^+.
$$

The determinant is finite and strictly positive. The unmodified
extrapolating weights were not clipped or regularized, and all 8880 published
rank-two flux values remain strictly positive. This is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon, map or stopping defect was
produced, and no map host was prepared as part of that offline stage. See
[validation/iterative/rank2_modal_aa2_rolling_next_candidate_result.md](validation/iterative/rank2_modal_aa2_rolling_next_candidate_result.md).

Its dedicated host was then frozen and executed exactly once, with no retry.
The carrier preflight, all four strict solve terminals, independent audit and
21-entry receipt pass. The unchanged gate gives

$$
(R_\rho,R_L,R_a)=
(1.2844697\times10^{-7},\,1.1701448\times10^{-3},\,
1.7994707\times10^{-6}),
$$

so the classification is `VALID_NOT_MET`. Only $R_\rho$ passes `5.0e-7`;
leakage remains the dominant failure. Relative to the preceding
different-parent map, all three stopping defects increased. This finite
cross-input comparison is not a convergence factor, a stability result or a
general verdict on Anderson(2). No retry or successor was started as part of
that map evaluation; see
[validation/iterative/rank2_modal_aa2_rolling_next_map_result.md](validation/iterative/rank2_modal_aa2_rolling_next_map_result.md).

The complete returned state was then used directly as the parent of exactly
one Picard successor, with no mixing or retry. All four strict solve
terminals, the independent continued-state audit and the 21-entry receipt
pass. The unchanged gate gives

$$
(R_\rho,R_L,R_a)=
(6.4223470\times10^{-8},\,6.2880209\times10^{-4},\,
1.4780076\times10^{-6}),
$$

so the classification is `VALID_NOT_MET`: only $R_\rho$ passes `5.0e-7`.
Relative to its direct parent, the three stopping defects fell about 50.0%,
46.26% and 17.86%. This is one local componentwise improvement, not a
convergence factor, contraction result, convergence-order measurement or
future prediction. No retry or further successor was started; see
[validation/iterative/rank2_modal_aa2_rolling_next_picard_map_result.md](validation/iterative/rank2_modal_aa2_rolling_next_picard_map_result.md).

A subsequent no-Dragon three-state audit reproduced both adjacent maps'
defects bit for bit. The unique leakage hotspot remains at snapshot 1/group
327: its signed increment changes from
`+1.7144775e-6` to `-9.2131086e-7 cm^-1`. The common leakage scale is
unchanged, so the 46.26% reduction in $R_L$ comes from the smaller absolute
update. This is a locally damped sign reversal, not a contraction proof.
Strict inner termination passed and the outer map remains unclosed; the data
do not identify rank two or finite inner error as the cause. No new map was
started as part of that audit; see
[validation/iterative/rank2_latest_picard_direction_result.md](validation/iterative/rank2_latest_picard_direction_result.md).

The complete latest returned state was then used for exactly one further
direct Picard map. All strict solve terminals, the independent audit and the
21-entry receipt pass. The unchanged gate gives

$$
(R_\rho,R_L,R_a)=
(6.4223470\times10^{-8},\,4.7549514\times10^{-4},\,
2.9019324\times10^{-6}),
$$

so the result is `VALID_NOT_MET`. Relative to its direct parent, $R_L$ falls
about 24.38% while $R_a$ rises about 96.34%; the defects are no longer
componentwise decreasing. This mixed step proves neither convergence nor
divergence. No retry or further map was started; see
[validation/iterative/rank2_latest_picard_next_map_result.md](validation/iterative/rank2_latest_picard_next_map_result.md).

The latest two direct modal residuals are nearly opposed in the existing
Gram-height metric, with cosine `-0.985084` and norm ratio `1.963408`.
Therefore the smallest parameter-free next study is one standard modal
Anderson(1) proposal,

$$
y=0.6636421413x_3+0.3363578587x_4.
$$

The publication-aware state $Q(y)$ has now been materialized and independently
checked offline. All 8880 published rank-two flux points are positive, the
complete $x_4$ raw carrier is retained, and the nine-entry receipt passes.
Its classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon, map, stopping defect or
map host was produced. See
[validation/iterative/rank2_latest_modal_aa1_candidate_result.md](validation/iterative/rank2_latest_modal_aa1_candidate_result.md).

That proposal was then evaluated by the unchanged physical map exactly once.
The strict `X4-RAW-FLUX` preflight, three online radial solves, one axial
solve, independent checker and 21-entry receipt all pass. The unchanged gate
gives

$$
(R_\rho,R_L,R_a)=
(6.4223470\times10^{-8},\,6.5357267\times10^{-4},\,
8.4905090\times10^{-7}),
$$

so the result is `VALID_NOT_MET`: only $R_\rho$ passes. Relative to the
historical direct $x_4=G_2(x_3)$ evaluation, $R_a$ falls about 70.74% but
$R_L$ rises about 37.45%; this is not
componentwise improvement and is not proof for or against AA(1). No retry or
successor was started. See
[validation/iterative/rank2_latest_modal_aa1_map_result.md](validation/iterative/rank2_latest_modal_aa1_map_result.md).

The next decision has now been made without another transport solve. Using
the two real residuals \(p=x_4-x_3\) and \(q=z-Q(y)\), the unique standard
modal AA(1) coefficient is

$$
\beta=0.7766660303945517,
\qquad
t=0.2233339696054483x_4+0.7766660303945517z.
$$

The affine modal screen is `0.1927051998914537` of the latest residual. The
same coefficient, without fitting leakage separately, gives offline leakage
height-$L_2$ and $D_L$ ratios `0.7632785965453454` and
`0.7073369976148646`. The publication preflight is positive at 8880/8880
points. This is only a read-only directional decision: no candidate, Dragon
run or new stopping defect was produced. The next minimal step is to
materialize and independently check \(Q(t)\) offline. See
[validation/iterative/rank2_latest_modal_aa1_history_result.md](validation/iterative/rank2_latest_modal_aa1_history_result.md).

That selected state has now been deterministically materialized as \(Q(t)\).
The independent checker reproduces the standard coefficient and publication,
verifies the complete returned-\(z\) `Z-RAW-FLUX` AX/snapshot carrier, and
accepts all 8880 reconstructed points. The nine-entry receipt passes. Its
classification is `MATERIALIZED_PROPOSAL_NOT_EVALUATED`: the publication
stage itself ran no Dragon or map and produced no stopping defect. A separate
default-off host was then activated exactly once for the unchanged
$G_2(Q(t))$, using the strict `proposal-z` gate, a 120-second radial bound
and an 80-second axial bound. The carrier preflight and all three radial
strict terminals passed, but the axial solve produced no strict terminal
before the 80-second process bound. The classification is therefore
`INVALID_MAP` with reason `TIMEOUT_BEFORE_TERMINAL`: no candidate, stopping
defect, or scientific map result exists, and there was no retry. See
[validation/iterative/rank2_latest_modal_aa1_next_candidate_result.md](validation/iterative/rank2_latest_modal_aa1_next_candidate_result.md).
The subsequent no-Dragon timing census found 14 strict historical completions
with the identical axial deck under the established 420-second cap; their
recorded CPU times are 132--141 seconds. Because exact wall times were not
recorded, this shows only that the 80-second cap was operationally aggressive,
not how long $Q(t)$ would require or that it would complete under a larger
cap.
A separately authorized recovery then evaluated the same $G_2(Q(t))$
exactly once from fresh radial staging. It changed no parent, rank, basis,
deck, equation, tolerance, AA(1) coefficient, or stopping gate; it restored
only the established external axial process cap from 80 to 420 seconds. All
four strict solves and the independent checker passed. The valid raw defects
are

$$
(R_\rho,R_L,D_L,R_a)=
(6.4223480867\times10^{-8},\,
4.4345562393\times10^{-4},\,
6.4974301495\times10^{-7}\ \mathrm{cm}^{-1},\,
3.7041235150\times10^{-6}).
$$

The unchanged three-component AND gate therefore gives `VALID_NOT_MET`:
$R_L$ and $R_a$ fail. The invalid 80-second attempt remains unchanged; none
of its staging was reused, and no retry or successor map was started.
The attempt record and frozen pre-run policy are
[validation/iterative/rank2_latest_modal_aa1_next_map_attempt_result.md](validation/iterative/rank2_latest_modal_aa1_next_map_attempt_result.md)
and
[validation/iterative/rank2_latest_modal_aa1_next_map_policy.md](validation/iterative/rank2_latest_modal_aa1_next_map_policy.md).
The recovery policy is
[validation/iterative/rank2_latest_modal_aa1_next_map_recovery_policy.md](validation/iterative/rank2_latest_modal_aa1_next_map_recovery_policy.md).
The completed recovery result is
[validation/iterative/rank2_latest_modal_aa1_next_map_recovery_result.md](validation/iterative/rank2_latest_modal_aa1_next_map_recovery_result.md).

The subsequent no-Dragon audit used the two latest valid pairs
$Q(y)\mapsto z$ and $Q(t)\mapsto u$. Standard modal AA(1), with no fitted or
clipped coefficient, gives

$$
s=0.815637869982362540z+0.184362130017637404u.
$$

Its affine modal screen is `0.0390808376459939` of the latest residual and
all 8880 publication points are positive. The leakage evidence is mixed:
the same-coefficient height-$L_2$ screen is `0.8110507722462015` of the
latest value, while the maximum $D_L$ screen is `1.1325277442611905`.
Therefore this does not establish AA(1) superiority or convergence. It only
makes the unique parameter-free $Q(s)$ eligible for a separate offline
materialization. See
[validation/iterative/rank2_latest_modal_aa1_recovery_history_result.md](validation/iterative/rank2_latest_modal_aa1_recovery_history_result.md).

That one eligible state has now been materialized and independently checked.
The coefficient was recomputed from the four frozen publication-aware
states; the same value was used for $A$, $\rho$ and $L$. The proposal
copies the complete latest returned-$u$ carrier without mixing raw fluxes
and is marked `PROPOSAL + U-RAW-FLUX`. The checker reproduces the REAL64 and
REAL32 publication arithmetic, preserves the `Q(t) -> u` snapshot
lifecycle, and accepts 8880/8880 positive reconstructed points. The 9/9
receipt passes. Its classification is
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon, map, stopping defect or
convergence decision was produced. The minimal `U-RAW-FLUX` host was then
activated exactly once for the unchanged $G_2(Q(s))$, with 120/420-second
process bounds. All four strict terminals, normal ends, the independent
checker and 21/21 receipt passed. The raw result is

$$
(R_\rho,R_L,D_L,R_a)=
(1.2844697306\times10^{-7},\,
4.2079128466\times10^{-4},\,
6.1653554440\times10^{-7}\ \mathrm{cm}^{-1},\,
2.6531418674\times10^{-6}).
$$

The classification is `VALID_NOT_MET`: $R_L$ and $R_a$ fail the unchanged
AND gate. There was no retry, new proposal or successor map. See
[validation/iterative/rank2_latest_modal_aa1_recovery_candidate_result.md](validation/iterative/rank2_latest_modal_aa1_recovery_candidate_result.md).
The frozen pre-run contract is
[validation/iterative/rank2_latest_modal_aa1_recovery_map_policy.md](validation/iterative/rank2_latest_modal_aa1_recovery_map_policy.md).
The completed result is
[validation/iterative/rank2_latest_modal_aa1_recovery_map_result.md](validation/iterative/rank2_latest_modal_aa1_recovery_map_result.md).

The subsequent no-Dragon audit used the actual pairs
$Q(t)\mapsto u$ and $Q(s)\mapsto v$. The unrestricted standard modal AA(1)
minimizer is

$$
x_{\mathrm{AA1}}=-2.43937066250607248u
                 +3.43937066250607248v.
$$

This is a genuine extrapolation, not a tuned relaxation: the two modal
residuals have cosine `0.9983735514`. Its modal affine screen is `0.1981` of
the latest residual, but the same-coefficient leakage $L_2$ and $D_L$
screens increase to `5.26` and `5.90` times their latest values. All 8880
publication points remain positive. Thus the unique state is arithmetically
eligible only for separate offline materialization; it is high risk and does
not establish convergence, componentwise improvement, or AA(1) superiority.
No proposal or map was started. See
[validation/iterative/rank2_latest_modal_aa1_qv_history_result.md](validation/iterative/rank2_latest_modal_aa1_qv_history_result.md).

That one unrestricted state has now been materialized offline, without
clipping its coefficient:

$$
x_{\mathrm{AA1}}=-2.43937066250607248u
                 +3.43937066250607248v.
$$

The same scalar publishes $(A,\rho,L)$. The complete raw AX and snapshot
carrier comes only from the latest returned $v$ and is marked
`V2-RAW-FLUX`; raw fluxes were not mixed. The independent checker binds the
hash-locked $Q(t)\to u$ pair, verifies the $Q(s)\to v$ snapshot lifecycle,
reproduces the REAL64/REAL32 publication, and accepts 8880/8880 points. The
9/9 receipt passes. The result remains
`MATERIALIZED_PROPOSAL_NOT_EVALUATED`: no Dragon, map, stopping defect, or
convergence decision was produced. See
[validation/iterative/rank2_latest_modal_aa1_qv_candidate_result.md](validation/iterative/rank2_latest_modal_aa1_qv_candidate_result.md).

## Latest three-step convergence attempt

The new bounded study is complete. First, a read-only comparison froze the
genuine consecutive direct route. Second, one $x=G_2(w)$ was evaluated with
fresh online radial transport; it was valid but not converged:

\[
(R_\rho,R_L,R_a)=
(0,\,4.5994291504\times10^{-4},\,1.1437675695\times10^{-6}).
\]

Its leakage defect increased, while its two modal updates were nearly
opposed (cosine `-0.990028`). The third and final step therefore used the
unique standard full-Gram AA(1) state

\[
c=0.37810309349656490w+0.62189690650343510x.
\]

The coefficient was not fitted or clipped. One fresh $G_2(c)$ passed all
strict inner terminals, the independent checker and the 21/21 receipt, but

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223492191\times10^{-8},\,
8.0189470417\times10^{-4},\,
1.1749216355\times10^{-6}\ \mathrm{cm}^{-1},\,
2.7219350042\times10^{-6}).
\]

Thus only $R_\rho$ passes the unchanged $5\times10^{-7}$ three-component
AND gate. The result is `VALID_NOT_MET`: the physical map is valid, but the
rank-two fixed point has not converged. No retry, fallback, empirical
coefficient or successor map was started. See the
[direct result](validation/iterative/rank2_vwx_picard_map_result.md),
[direction decision](validation/iterative/rank2_vwx_direction_result.md),
[AA(1) candidate](validation/iterative/rank2_vwx_aa1_candidate_result.md),
and [final map](validation/iterative/rank2_vwx_aa1_map_result.md).

No further map is authorized by this result.
