# Latest rank-2 modal AA(1) direction audit after the recovery map

Date: 2026-08-16

Classification: `OFFLINE_DECISION_COMPLETE`.

## Scope

This was one read-only, Ganlib-only calculation using the latest two valid
fixed-rank-two input-output pairs:

\[
Q(y)\longmapsto z,
\qquad
Q(t)\longmapsto u=G_2(Q(t)).
\]

The 80-second invalid attempt has no returned state and was excluded. The
calculation used the actual publication-aware materialized proposal states,
including the prescribed REAL32 publication steps, not their ideal affine
precursors. It ran no Dragon, radial solve, axial solve, map, proposal
publication, or model update.

Define the two real map residuals

\[
q=z-Q(y),\qquad r=u-Q(t).
\]

The checker replayed both saved map defects bit for bit and required all four
states to share the same fixed rank-two POD space. It also required the exact
`X4-RAW-FLUX` and `Z-RAW-FLUX` proposal carriers.

## Standard modal AA(1)

In the unchanged full Gram-height modal metric, the unique depth-one scalar
is

\[
\beta=
\frac{\lVert q\rVert_{HG}^{2}-\langle q,r\rangle_{HG}}
     {\lVert r-q\rVert_{HG}^{2}},
\qquad
s=(1-\beta)z+\beta u.
\]

| quantity | value |
|---|---:|
| \(\lVert q\rVert_{HG}\) | `5.65865271195166948e-7` |
| \(\lVert r\rVert_{HG}\) | `2.46867988169239516e-6` |
| \(\langle q,r\rangle_{HG}\) | `-1.36612700994946577e-12` |
| \(\lVert r-q\rVert_{HG}^{2}\) | `9.14683788331648823e-12` |
| \(\beta\), weight on \(u\) | `0.184362130017637404` |
| weight on \(z\) | `0.815637869982362540` |
| affine modal residual norm | `9.64780776563518284e-8` |
| affine modal residual / \(\lVert r\rVert_{HG}\) | `0.0390808376459938628` |

The denominator is finite and strictly positive, and both weights are
naturally convex. No clipping, damping, fitted coefficient, regularization,
pseudoinverse threshold, or fallback was used. The same scalar would have to
act on the complete `(A,rho,L)` state; leakage was not fitted separately.

## Leakage cross-check

Leakage did not enter the coefficient. Applying the same modal \(\beta\) to
the saved leakage residuals gives:

| quantity | value |
|---|---:|
| leakage \(\lVert q_L\rVert_{H2}\) | `1.63842538674819758e-5` |
| leakage \(\lVert r_L\rVert_{H2}\) | `1.54183083487505860e-5` |
| leakage cosine | `-0.398699078640322890` |
| same-\(\beta\) affine \(L_2\) / current | `0.811050772246201479` |
| \(D_L(q)\) | `9.57603333517909050e-7 cm^-1` |
| \(D_L(r)\) | `6.49743014946579933e-7 cm^-1` |
| same-\(\beta\) affine \(D_L\) | `7.35851991066915217e-7 cm^-1` |
| same-\(\beta\) affine \(D_L\) / current | `1.13252774426119052` |

The evidence is mixed: the modal and leakage height-\(L_2\) screens decrease,
while the maximum dimensional leakage-change screen increases by about
`13.25%`. None of these affine quantities is a new \(R_L\), \(R_a\), or
fixed-point defect, so they cannot establish componentwise improvement or
AA(1) superiority.

## Publication preflight

Without writing a proposal XSM, the checker applied canonical publication
arithmetic to the affine output:

| quantity | value |
|---|---:|
| raw affine \(\rho\) | `0.733992899240309749` |
| REAL32-published \(k\) | `1.36241102218627930` |
| reciprocal published \(\rho\) | `0.733992887399932070` |
| publication shift in \(\rho\) | `-1.18403776783182479e-8` |
| maximum leakage REAL32 round trip | `5.20275916533058380e-11` |
| minimum published REAL32 \(B_2a\) | `1.75340224652965893e-15` |
| strictly positive reconstructed points | `8880 / 8880` |

This establishes arithmetic admissibility only. No proposal was created and
no map was authorized.

## Frozen provenance and reproduction

| role | AX SHA-256 | artifact-receipt SHA-256 |
|---|---|---|
| \(Q(y)\) | `0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d` | `0ab7e28a1f5924d5fc369ed6335abfdc02b4d8f6f2702c631e0dcebb0375e241` |
| \(z\) | `8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9` | `9e614de527fa2c4b9dbe7ba5375ec89b1769077ba5b8c690fc9445bd96eb3b8e` |
| \(Q(t)\) | `e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c` | `de0be838f43dc4a644480e47474d6f1667031259e8a402fc148db7a734716329` |
| \(u\) | `d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744` | `50898b375ffd92d7ad2355cf9ed6cc7b72e0f0c5c9318da78b011ad06b0cf3d3` |

All four receipts pass. The frozen manifest is
[`rank2_latest_modal_aa1_recovery_history.tsv`](rank2_latest_modal_aa1_recovery_history.tsv),
with SHA-256
`28e83b947900b681780fb4b73bb07b81f148cbb7c17c05e5b9de956a33dbfa01`.
The checker SHA-256 is
`c5b19a8ee3b448b772c783b4bc6643ed8026dea135d356cadd8a8e29356bf46f`.

After strict compilation against Ganlib, reproduce from
`validation/artifacts/`:

```sh
/path/to/check_one_map_xsm --rank2-aa1-x4z-history \
  iterative-rank2-latest-modal-aa1-candidate/proposal_axial.xsm \
  iterative-rank2-latest-modal-aa1-map/candidate_axial.xsm \
  iterative-rank2-latest-modal-aa1-next-candidate/proposal_axial.xsm \
  iterative-rank2-latest-modal-aa1-next-map-recovery/candidate_axial.xsm
```

The older `--rank2-aa1-u-history` and `--rank2-aa1-x4-history` modes exactly
reproduced their recorded coefficients after this checker extension. A wrong
X4-carrier object in the new mode's `Q(t)` slot was rejected before the
calculation.

## Decision boundary

There is no componentwise physical verdict between direct Picard and AA(1)
from this offline evidence. Under the already declared modal AA(1) policy,
however, the unique parameter-free state

\[
Q(s)=Q\!\left(0.815637869982362540z+
               0.184362130017637404u\right)
\]

is eligible for a separate no-Dragon materialization and independent carrier
check. This is not a claim that AA(1) is superior, and it does not authorize
a real map. Only a separately authorized evaluation of the unchanged
physical map could produce new \(R_\rho,R_L,R_a\) and apply the stopping AND
gate.
