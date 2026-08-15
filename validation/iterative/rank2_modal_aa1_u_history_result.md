# Latest rank-2 modal AA(1) history decision

Date: 2026-08-15

Classification: `ELIGIBLE_TO_MATERIALIZE_NOT_EVALUATED`.

This is a read-only, no-Dragon history calculation. It writes no candidate
XSM and evaluates no new map.

## Two evaluated pairs

The latest two actual input-output pairs are

\[
(y_{\rm pub},z),\qquad (w_{\rm pub},v),
\]

with modal residuals

\[
q=z-y_{\rm pub},\qquad r=v-w_{\rm pub}.
\]

Both inputs are the actual REAL32-published proposals, not ideal affine
precursors. In the unchanged full modal Gram-height metric, the unique
depth-one least-squares scalar is

\[
\beta_v=
\frac{\langle q,q-r\rangle_{HG}}
     {\lVert q-r\rVert_{HG}^{2}},
\qquad
u=(1-\beta_v)z+\beta_v v.
\]

The proposal formula combines the two map outputs, not the two inputs. The
coefficient is formed only from modal coordinates; the same scalar would be
applied to the complete `(a,rho,L)` state without constructing a mixed-unit
whole-state norm.

## Real-data result

The Ganlib-only checker bitwise replayed both map defects and verified that
all four states share the fixed rank-two layout, basis, Gram matrix, heights
and normalization identifier.

| quantity | value |
|---|---:|
| \(\lVert q\rVert_{HG}\) | `3.10866323541343214e-4` |
| \(\lVert r\rVert_{HG}\) | `2.96022587831658376e-5` |
| \(\langle q,r\rangle_{HG}\) | `-3.63189481642573057e-9` |
| \(\lVert q-r\rVert_{HG}^{2}\) | `1.04777954470028051e-7` |
| \(\beta_v\), weight on \(v\) | `0.956973882871698711` |
| weight on \(z\) | `0.0430261171283012889` |
| affine modal-history screen | `2.61213299210214508e-5` |
| screen divided by \(\lVert r\rVert_{HG}\) | `0.882410025274020127` |

The denominator is finite and strictly positive, so the minimizer is unique.
The two weights are naturally convex. No clipping, damping, fallback,
near-singular empirical threshold or fitted coefficient was used.

The `0.882410` ratio concerns only an affine combination of two already known
modal residuals. It is not \(G_2(u)-u\), an actual convergence factor or a
prediction that a future map will meet tolerance.

## Publication preflight

Without creating an XSM object, the checker applied the canonical publication
arithmetic:

| quantity | value |
|---|---:|
| raw affine \(\rho\) | `0.733993308401465594` |
| REAL32-published \(k\) | `1.36241018772125244` |
| reciprocal published \(\rho\) | `0.733993336964534504` |
| publication shift in \(\rho\) | `2.85630689100813129e-8` |
| largest leakage REAL32 round trip | `5.78241842429105812e-11` |
| smallest REAL32-published \(B_2a\) | `1.75341971658419605e-15` |

All `370 x 3 x 8 = 8880` reconstructed values are strictly positive. The
minimum occurs at group 370, snapshot 3, region 2. This is a strict positivity
result in the stated arithmetic, not a robustness margin.

## Frozen inputs and reproduction

| role | AX SHA-256 | artifact-receipt SHA-256 |
|---|---|---|
| \(y_{\rm pub}\) | `ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56` | `8549c574353594debcc3ee14b7dc268590334af4ac7b0d3c78b3fb73a59f880e` |
| \(z\) | `a57feb6e83487561a153ae376874339c116192d0ece3d716cd10e2dac203376e` | `45bf76532df56c849b526fe78d5c9ffd81d9ecb98fc844a27b45f12d2684a785` |
| \(w_{\rm pub}\) | `c2df5e526aa9a0c0c3dc354d3ec539475814fe73c87af19ba04dde05c1475ff4` | `8698e62fe04a21b9f7305e140f38e078100559b02661d513d82955f331897280` |
| \(v\) | `02f922cf157a0dde1b9d072f45cdb1e39c64fa1f8682ad3a1e4fe21fede12a62` | `5d19edfecabfae1d17d4d796929c5ea7ebd3b8343fc5d3a08f8d142338d50a73` |

All four artifact receipts pass. The frozen manifest is
[`rank2_modal_aa1_u_history.tsv`](rank2_modal_aa1_u_history.tsv), with SHA-256
`183117377acb252f231787de5ef0e1691ee05298b38b2442747d26c7a86a3d74`.
The checker SHA-256 is
`eb2b5c1f26196e14b304cc7745da966a5ecf3afa04086cd2d6674243ebac3395`.

After strict compilation of `check_one_map_xsm.f90` against Ganlib, reproduce
from `validation/artifacts/` with paths shorter than the Ganlib limit:

```sh
/path/to/check_one_map_xsm --rank2-aa1-u-history \
  iterative-rank2-modal-aa1-candidate/proposal_axial.xsm \
  iterative-rank2-modal-aa1-map/candidate_axial.xsm \
  iterative-rank2-modal-aa1-next-candidate/proposal_axial.xsm \
  iterative-rank2-modal-aa1-next-map/candidate_axial.xsm
```

The historical `--rank2-aa1-history` result was rerun with the updated checker
and reproduced its original weight `0.930274550669676792`. A wrong Z-carrier
input to the new mode was rejected.

## Scientific boundary

`ELIGIBLE_TO_MATERIALIZE_NOT_EVALUATED` means only that this unique formula,
state provenance and publication preflight pass. It is not a candidate
artifact, map result, stopping defect, convergence result, stability claim,
rank-adequacy result or physical-accuracy validation.

Any future materialization requires a separate decision. It would need to
reuse the latest returned \(v\) raw-flux/snapshot carrier and introduce an
explicitly audited `V-RAW-FLUX` lifecycle; that carrier and builder path are
not implemented or authorized here.
