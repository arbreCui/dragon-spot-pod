# Rank-2 nonlinear-solver decision

## Decision

The next method study is one **modal-projected Anderson(1)** proposal using
the full modal Gram-height metric. This decision defines only an offline
coefficient. It does not
materialize a candidate state, call Dragon, evaluate another map or define a
third direct Picard iterate.

Let the two valid rank-2 maps be

\[
x_1=G_2(x_0),\qquad x_2=G_2(x_1),
\]

and let the modal residuals in the unchanged rank-2 space be

\[
f_0^a=a_1-a_0,\qquad f_1^a=a_2-a_1.
\]

Using the existing physical Gram-height inner product

\[
\langle u,v\rangle_{HG}
=\sum_{s,g}H_s\,u_{s,g}^{T}M_gv_{s,g},
\]

define the unique minimizer of this stated scalar modal least-squares problem

\[
\beta_a=
-\frac{\langle f_0^a,f_1^a-f_0^a\rangle_{HG}}
       {\lVert f_1^a-f_0^a\rVert_{HG}^{2}},
\qquad
y=(1-\beta_a)x_1+\beta_a x_2.
\]

The same scalar is applied to every component of the coupled state
\(x=(a,\rho,L)\).  The coefficient is computed only in the modal Hilbert
space; no inner product or sum is formed across the unlike physical blocks.
This is not a full-state residual optimum.

## Frozen real-data value

The existing independent Ganlib checker replays both raw defects before
forming the coefficient.  The hash-locked states give

\[
\beta_a=0.538864326513600944,
\qquad 1-\beta_a=0.461135673486399056.
\]

The denominator is
\(6.67626947253604868\times10^{-5}\), and the affine modal-residual
prediction is

\[
\left\lVert(1-\beta_a)f_0^a+\beta_a f_1^a\right\rVert_{HG}
=1.04919178380867301\times10^{-3},
\]

which is `0.268251892777420176` of
\(\lVert f_1^a\rVert_{HG}\).  This is only a two-residual linear screen.  It
is not \(G_2(y)-y\), an acceptance result or evidence of convergence.  The
coefficient happens to be a convex weight; no clipping rule is introduced.

## Why this is the smallest defensible acceleration study

- Direct Picard remains the only implemented production iteration.  The
  second rank-2 map is valid and all three defects decreased, so the data do
  not reject a third direct step.  They do show that the full modal updates
  are strongly opposed and shrink only to `0.864118`, while the leakage
  update shrinks to `0.024606`; blindly extending the expensive census is
  therefore not the most informative next experiment.
- A full-state least-squares Anderson coefficient would require a new metric
  that weights \(a\), \(\rho\) and \(L\) together.  No such mixed-unit metric
  is defined.
- Separate Aitken or Anderson coefficients for the three blocks would add a
  block algorithm and a leakage-norm choice, and would no longer follow one
  affine history of the coupled state.
- A mode-2-only coefficient would be basis dependent.  The complete modal
  Gram metric already exists and is the natural SPOD metric.
- Exact Newton remains a mathematical reference, but the real map provides
  no trusted exact Jacobian.  Finite-difference/JFNK would add a perturbation
  scale and Krylov controls and is obstructed by the existing binary32
  publication path.

Thus \(\beta_a\) is a data-computed algorithmic coefficient, not an
empirical physical parameter, fitted closure, prescribed relaxation factor
or damping constant.  Selecting the modal block is nevertheless an explicit
algorithm choice; the method is not mathematically unique and is not claimed
to be a full-state optimum.

## Unchanged acceptance boundary

A later, separately declared construction may form the publication-aware
state

\[
y_{\mathrm{pub}}=Q(y).
\]

It must fail closed unless the fixed basis metadata are unchanged and the
published state is finite, has positive \(\rho\), and has positive
reconstructed flux. No floor, clipping, damping, fallback or retry is
allowed.

Only a subsequent fresh strict evaluation

\[
z=G_2(y_{\mathrm{pub}})
\]

can test the proposal.  Acceptance remains the original separate AND gate

\[
R_\rho\leq\varepsilon,\qquad
R_L\leq\varepsilon,\qquad
R_a\leq\varepsilon.
\]

The offline prediction, a combined score, \(D_L\), or leakage height-\(L_2\)
cannot accept the state.  The earlier rank-1 leakage-driven Anderson trial
made both \(R_L\) and \(R_a\) worse after its fresh map; that result reinforces
this boundary but does not reject Anderson methods in general.

## Reproduction

Compile the current
[`check_one_map_xsm.f90`](check_one_map_xsm.f90) and invoke

```sh
check_one_map_xsm --rank2-directions \
  validation/artifacts/iterative-rank2-map-axial2/rank2_parent_axial.xsm \
  validation/artifacts/iterative-rank2-map-axial2/candidate_axial.xsm \
  validation/artifacts/iterative-rank2-picard2/candidate_axial.xsm
```

The three state hashes and their map receipts are frozen in
[`rank2_next_map_result.md`](rank2_next_map_result.md).  This check is
read-only and launches no Dragon process. `make spot-fast` separately checks
the exact least-squares normal equation, metric-scale invariance,
state-unit covariance and singular-denominator rejection on rational
manufactured data.

The separately scoped publication step has since materialized and independently
checked this proposal without evaluating a map; see
[`rank2_modal_aa1_candidate_result.md`](rank2_modal_aa1_candidate_result.md).
