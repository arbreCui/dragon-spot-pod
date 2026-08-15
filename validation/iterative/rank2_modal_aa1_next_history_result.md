# Next rank-2 modal AA(1) history decision

Date: 2026-08-14

Classification: `ELIGIBLE_TO_MATERIALIZE_NOT_EVALUATED`.

This is a read-only, no-Dragon history update. It writes no candidate and
evaluates no new map.

## Correct two-pair history

The two latest evaluated input-output pairs are

\[
(x_1,G_2(x_1))=(x_1,x_2),
\qquad
(y_{\rm pub},G_2(y_{\rm pub}))=(y_{\rm pub},z).
\]

Their modal residuals are therefore

\[
p^a=a_{x_2}-a_{x_1},
\qquad
q^a=a_z-a_{y_{\rm pub}}.
\]

The second residual uses the actually published input `y_pub`, not its
unpublished ideal affine precursor. The standard depth-one Anderson weight on
the latest output is

\[
\beta_z=
\frac{\lVert p^a\rVert_{HG}^2-\langle p^a,q^a\rangle_{HG}}
     {\lVert p^a-q^a\rVert_{HG}^2},
\]

and the possible next raw proposal is

\[
w=(1-\beta_z)x_2+\beta_z z.
\]

It is not a combination of `y_pub` and `z`. The same scalar acts on the full
state `(a,rho,L)` while its coefficient is formed only in the existing full
modal Gram-height metric.

## Frozen real-data result

The independent Ganlib-only checker bitwise replayed both saved map defects
and established that all four states use the same fixed rank-2 layout, basis,
Gram matrix, height and normalization identifier. It then reported

| quantity | value |
|---|---:|
| \(\lVert p^a\rVert_{HG}\) | `3.91121856753954503e-3` |
| \(\lVert q^a\rVert_{HG}\) | `3.10866323541343214e-4` |
| \(\langle p^a,q^a\rangle_{HG}\) | `-1.13501300439387783e-6` |
| denominator \(\lVert q^a-p^a\rVert_{HG}^2\) | `1.76642945629659538e-5` |
| \(\beta_z\) | `0.930274550669676792` |
| weight on \(x_2\) | `0.0697254493303232081` |
| affine modal-history screen | `1.03732639026344388e-4` |
| screen divided by \(\lVert q^a\rVert_{HG}\) | `0.333688891883294092` |

The denominator is finite and strictly positive, so the scalar minimizer is
unique. The two weights naturally form a convex combination. No clipping,
damping, fallback or empirical limit was applied.

The final screen is only the affine combination of two known modal residuals.
It is not \(G_2(w_{\rm pub})-w_{\rm pub}\), a convergence factor or evidence
that Anderson is generally superior to Picard.

## Publication preflight

Without writing an XSM object, the checker applied the same publication
arithmetic that a later builder would use:

| quantity | value |
|---|---:|
| raw affine \(\rho\) | `0.733993014460187831` |
| REAL32-published \(k\) | `1.36241078376770020` |
| reciprocal published \(\rho\) | `0.733993015846905128` |
| publication shift in \(\rho\) | `1.38671729654760156e-9` |
| largest leakage REAL32 round trip | `5.28309021963907499e-11` |
| smallest REAL32-published \(B_2a\) | `1.75332114312495933e-15` |

All `370 x 3 x 8 = 8880` reconstructed points are strictly positive. The
minimum occurs at group 370, snapshot 3, region 2. This proves strict
positivity in the actual publication arithmetic, not a robustness margin.

Thus the canonical `(a,rho,L)` state is eligible for a separate deterministic
materialization step. Full carrier materialization would still have to use
and explicitly label the already audited `z` raw-flux snapshot carrier.

## Frozen inputs and reproduction

| role | SHA-256 |
|---|---|
| \(x_1\) | `5ec5a3576fab3662cd5fabc18226d98e56fd9b936deabe6bd70a09623f596f61` |
| \(x_2\) | `bff9299595121b4b189f8b6d8e39c3b06bcefe0598d387f4aebf57861546ca02` |
| \(y_{\rm pub}\) | `ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56` |
| \(z\) | `a57feb6e83487561a153ae376874339c116192d0ece3d716cd10e2dac203376e` |

All four parent artifact receipts pass. The frozen manifest is
[`rank2_modal_aa1_next_history.tsv`](rank2_modal_aa1_next_history.tsv), with
SHA-256 `cb338334fc7e085520b4c02bf02f8238ab386967d31aa2e8f93dd01e2c2fae29`.
The checker SHA-256 is
`2df827c317e1cf55c477c0eff69d3035cd6dc41955564c660ea20231d45eef66`.

After compiling `check_one_map_xsm.f90` against Ganlib, reproduce from
`validation/artifacts/` with paths shorter than the Ganlib path limit:

```sh
/path/to/check_one_map_xsm --rank2-aa1-history \
  iterative-rank2-map-axial2/candidate_axial.xsm \
  iterative-rank2-picard2/candidate_axial.xsm \
  iterative-rank2-modal-aa1-candidate/proposal_axial.xsm \
  iterative-rank2-modal-aa1-map/candidate_axial.xsm
```

## Scientific boundary

`ELIGIBLE_TO_MATERIALIZE_NOT_EVALUATED` means only that the unique AA(1)
formula and canonical publication preflight pass. No proposal XSM has been
created, no transport equation has been solved at `w_pub`, and no new outer
defect exists. This result is neither `TOLERANCE_MET` nor `VALID_NOT_MET` and
does not authorize a map. The smallest next step, if separately authorized,
is deterministic materialization using the `z` carrier; it still performs no
Dragon calculation.
