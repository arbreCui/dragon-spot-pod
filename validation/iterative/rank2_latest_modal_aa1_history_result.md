# Latest rank-2 modal AA(1) decision audit

Date: 2026-08-16

Classification: `OFFLINE_DECISION_COMPLETE`.

## Scope

This was one read-only, Ganlib-only calculation using two already evaluated
fixed-rank-two map pairs:

\[
p=x_4-x_3=G_2(x_3)-x_3,
\qquad
q=z-Q(y)=G_2(Q(y))-Q(y).
\]

It ran no Dragon, radial solve, axial solve, map, candidate publication or
model update. The checker independently replayed both saved raw defects bit
for bit and required all four states to share the same fixed POD space. The
published proposal was required to carry the exact `X4-RAW-FLUX` marker; an
old `X2-RAW-FLUX` proposal was rejected by the new mode.

## Standard modal AA(1) result

In the unchanged full Gram-height modal metric, the unique depth-one
coefficient minimizes

\[
\left\lVert(1-\beta)p+\beta q\right\rVert_{HG}^{2},
\qquad
\beta=
\frac{\lVert p\rVert_{HG}^{2}-\langle p,q\rangle_{HG}}
     {\lVert q-p\rVert_{HG}^{2}}.
\]

The corresponding affine output, if separately materialized, is

\[
t=(1-\beta)x_4+\beta z.
\]

| quantity | value |
|---|---:|
| \(\lVert p\rVert_{HG}\) | `1.93404508350515413e-6` |
| \(\lVert q\rVert_{HG}\) | `5.65865271195166948e-7` |
| \(\langle p,q\rangle_{HG}\) | `-1.06029698192934440e-12` |
| modal cosine | `-0.9688306972575571` |
| \(\lVert q-p\rVert_{HG}^{2}\) | `6.18132785403392786e-12` |
| \(\beta\), weight on \(z\) | `0.776666030394551732` |
| weight on \(x_4\) | `0.223333969605448268` |
| affine modal residual norm | `1.09045180197296326e-7` |
| affine modal residual / \(\lVert q\rVert_{HG}\) | `0.192705199891453738` |

The denominator is finite and strictly positive, and both weights are
naturally convex. No clipping, damping, regularization, pseudoinverse
threshold, fitted coefficient or fallback was used.

## Leakage cross-check

Leakage did not participate in the coefficient. The checker applied the same
modal \(\beta\) to the leakage residuals and reported a height-weighted
\(L_2\) diagnostic plus the stored dimensional
\(D_L=\lVert\Delta L\rVert_\infty\) diagnostic:

| quantity | value |
|---|---:|
| leakage \(\lVert p_L\rVert_{H2}\) | `1.55835528349319463e-5` |
| leakage \(\lVert q_L\rVert_{H2}\) | `1.63842538674819758e-5` |
| leakage cosine | `-0.199231292644347552` |
| same-\(\beta\) affine \(L_2\) / current | `0.763278596545345356` |
| \(D_L(p)\) | `6.96687493473291397e-7 cm^-1` |
| \(D_L(q)\) | `9.57603333517909050e-7 cm^-1` |
| same-\(\beta\) affine \(D_L\) | `6.77348266836543632e-7 cm^-1` |
| same-\(\beta\) affine \(D_L\) / current | `0.707336997614864571` |

Thus this latest standard AA(1) screen decreases both the modal residual and
the leakage residual in the two stated offline measures. This is stronger
directional evidence than another blind direct substitution, but it is not
\(G_2(Q(t))-Q(t)\). In particular, the preceding proposal also had a
favorable offline leakage screen and its real nonlinear map did not preserve
that improvement. No convergence factor or monotonicity claim follows.

## Publication preflight

Without writing a candidate XSM, the checker applied the canonical
publication arithmetic to the same affine output:

| quantity | value |
|---|---:|
| raw affine \(\rho\) | `0.733992887399932070` |
| REAL32-published \(k\) | `1.36241102218627930` |
| reciprocal published \(\rho\) | `0.733992887399932070` |
| maximum leakage REAL32 round trip | `5.43286316542074266e-11` |
| minimum published REAL32 \(B_2a\) | `1.75340256416701415e-15` |
| strictly positive reconstructed points | `8880 / 8880` |

This preflight establishes arithmetic admissibility only. It did not create
`Q(t)` and did not authorize a map.

## Frozen provenance and reproduction

| role | SHA-256 |
|---|---|
| \(x_3\) | `154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651` |
| \(x_4\) | `ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08` |
| \(Q(y)\) | `0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d` |
| \(z\) | `8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9` |

The frozen manifest is
[`rank2_latest_modal_aa1_history.tsv`](rank2_latest_modal_aa1_history.tsv),
with SHA-256
`10d03dea5de7d7925516ef0d59188ba0a334571f3c53a5165ff8d0f8c7940481`.
The checker SHA-256 is
`618771fcaae314cc370ae11123687ba0c03167b82481dba542bf1a3d9d4fc2ee`.

After strict compilation against Ganlib, reproduce from
`validation/artifacts/` with paths below Ganlib's path-length limit:

```sh
/path/to/check_one_map_xsm --rank2-aa1-x4-history \
  iterative-rank2-modal-aa2-rolling-next-picard-map/candidate_axial.xsm \
  iterative-rank2-latest-picard-next-map/candidate_axial.xsm \
  iterative-rank2-latest-modal-aa1-candidate/proposal_axial.xsm \
  iterative-rank2-latest-modal-aa1-map/candidate_axial.xsm
```

The two older history modes were rerun with the updated checker and exactly
reproduced their recorded coefficients. The carrier-negative test rejected
an `X2-RAW-FLUX` proposal in the new X4-only mode.

## Decision boundary

The smallest justified convergence-directed next step is to materialize and
independently check exactly one publication-aware state

\[
Q(t)=Q\!\left(0.223333969605448268x_4+
               0.776666030394551732z\right)
\]

offline, using the complete returned \(z\) state only as its raw carrier.
That next step must still run no Dragon and must not start a map. A real map
from `Q(t)`, if later authorized, remains the only way to determine its raw
three-component stopping defects. If that map again gives a mixed response
near the inner terminal scale, a single same-parent tighter-tolerance
sensitivity check is then warranted before any further solver construction.
