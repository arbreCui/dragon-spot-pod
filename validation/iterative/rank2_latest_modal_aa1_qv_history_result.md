# Latest rank-2 modal AA(1) audit after the \(Q(s)\) map

Date: 2026-08-16

Classification: `OFFLINE_DECISION_COMPLETE`.

## Scope

This was one read-only, Ganlib-only calculation using the latest two valid
fixed-rank-two input-output pairs:

\[
Q(t)\longmapsto u=G_2(Q(t)),
\qquad
Q(s)\longmapsto v=G_2(Q(s)).
\]

The checker used the actual publication-aware proposal states, replayed both
saved map defects bit for bit, required the same frozen rank-two POD space,
and required the exact `Z-RAW-FLUX` and `U-RAW-FLUX` carriers. It ran no
Dragon, radial solve, axial solve, map, proposal publication, or model update.

The second map remains `VALID_NOT_MET`:

\[
(R_\rho,R_L,R_a)=
(1.284469730578053\times10^{-7},
 4.207912846624437\times10^{-4},
 2.653141867393721\times10^{-6}).
\]

Only \(R_\rho\) passes the unchanged \(5\times10^{-7}\) AND gate.

## Standard modal AA(1)

Define the two real map residuals

\[
p=u-Q(t),\qquad q=v-Q(s).
\]

In the unchanged full Gram-height modal metric, standard depth-one Anderson
acceleration gives the unique unrestricted scalar

\[
\beta=
\frac{\lVert p\rVert_{HG}^{2}-\langle p,q\rangle_{HG}}
     {\lVert q-p\rVert_{HG}^{2}},
\qquad
x_{\mathrm{AA1}}=(1-\beta)u+\beta v.
\]

| quantity | value |
|---|---:|
| \(\lVert p\rVert_{HG}\) | `2.46867988169239516e-6` |
| \(\lVert q\rVert_{HG}\) | `1.76823416857308124e-6` |
| \(\langle p,q\rangle_{HG}\) | `4.35810433798562192e-12` |
| modal residual cosine | `0.99837355140795803` |
| \(\lVert q-p\rVert_{HG}^{2}\) | `5.04823757210870257e-13` |
| \(\beta\), weight on \(v\) | `3.43937066250607248` |
| weight on \(u\) | `-2.43937066250607248` |
| affine modal residual norm | `3.50262119111267702e-7` |
| affine modal residual / \(\lVert q\rVert_{HG}\) | `0.198085822192837768` |

The denominator is finite and strictly positive. The two modal residuals are
nearly parallel, so the exact least-squares minimizer is an extrapolation,
not a convex combination. No clipping, damping, relaxation, fitted
coefficient, regularization, pseudoinverse threshold, condition cutoff, or
fallback was used. The same scalar was applied in the offline preflight to
the complete `(A,rho,L)` state.

## Leakage cross-check

Leakage did not enter the coefficient. Applying the same modal scalar to the
saved leakage residuals gives:

| quantity | value |
|---|---:|
| leakage \(\lVert p_L\rVert_{H2}\) | `1.54183083487505860e-5` |
| leakage \(\lVert q_L\rVert_{H2}\) | `1.33366883346627219e-5` |
| leakage cosine | `-0.404627067232454785` |
| same-\(\beta\) affine \(L_2\) / current | `5.25657676352726266` |
| \(D_L(p)\) | `6.49743014946579933e-7 cm^-1` |
| \(D_L(q)\) | `6.16535544395446777e-7 cm^-1` |
| same-\(\beta\) affine \(D_L\) | `3.63907795939401030e-6 cm^-1` |
| same-\(\beta\) affine \(D_L\) / current | `5.90246254652254176` |

The modal prediction decreases, while both same-coefficient leakage screens
increase strongly. These are affine diagnostics, not a new \(R_L\), \(R_a\),
or fixed-point defect. They therefore neither prove convergence nor provide
an academic basis for fitting, clipping, or damping the coefficient.

## Publication preflight

Without writing a proposal XSM, the checker applied the canonical
publication arithmetic to the unrestricted affine output:

| quantity | value |
|---|---:|
| raw affine \(\rho\) | `0.733993172511808067` |
| REAL32-published \(k\) | `1.36241054534912109` |
| reciprocal published \(\rho\) | `0.733993144293923150` |
| publication shift in \(\rho\) | `-2.82178849175807045e-8` |
| maximum leakage REAL32 round trip | `4.23491029570566280e-11` |
| minimum published REAL32 \(B_2a\) | `1.75340245828789574e-15` |
| strictly positive reconstructed points | `8880 / 8880` |

This establishes arithmetic admissibility only. No proposal was created and
no map was authorized.

## Frozen provenance and reproduction

| role | AX SHA-256 | artifact-receipt SHA-256 |
|---|---|---|
| \(Q(t)\) | `e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c` | `de0be838f43dc4a644480e47474d6f1667031259e8a402fc148db7a734716329` |
| \(u\) | `d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744` | `50898b375ffd92d7ad2355cf9ed6cc7b72e0f0c5c9318da78b011ad06b0cf3d3` |
| \(Q(s)\) | `53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193` | `33326758295453f6ab4d4d018d8830d119ceb5bc9ba4cc4b5e82ce1e66500b22` |
| \(v\) | `0842ea931a0b53babb7ea7cde6af459ad86d219ea70e83f1242b7b86ce2bf737` | `57bdd4825d61f1947dafe1b8564aaae21748cc09ee519a70dd2745616ddb932a` |

All four receipts pass. The frozen manifest is
[`rank2_latest_modal_aa1_qv_history.tsv`](rank2_latest_modal_aa1_qv_history.tsv),
with SHA-256
`8c062a10ad796c24beca7c17c6d62bed4873a08cb6ceaf98591ac208e97d347a`.
The checker SHA-256 is
`062fb5028a3b0fe4d3100894cf44e4365c38571810878c42a1e79435c5a39753`.

After strict compilation against Ganlib, reproduce from
`validation/artifacts/`:

```sh
/path/to/check_one_map_xsm --rank2-aa1-zu-history \
  iterative-rank2-latest-modal-aa1-next-candidate/proposal_axial.xsm \
  iterative-rank2-latest-modal-aa1-next-map-recovery/candidate_axial.xsm \
  iterative-rank2-latest-modal-aa1-recovery-candidate/proposal_axial.xsm \
  iterative-rank2-latest-modal-aa1-recovery-map/candidate_axial.xsm
```

The preceding `--rank2-aa1-x4z-history` mode reproduced its frozen
coefficient and diagnostics exactly after this extension. Replacing the
required `U-RAW-FLUX` proposal with the `Z-RAW-FLUX` proposal was rejected
before any AA(1) arithmetic.

## Decision boundary

The standard modal AA(1) rule has exactly one next affine state,

\[
x_{\mathrm{AA1}}=
-2.43937066250607248u+3.43937066250607248v.
\]

Under the already declared unrestricted modal AA(1) policy, it is eligible
only for a separate no-Dragon materialization and independent carrier check.
The adverse leakage screens make it a high-risk proposal, not a convergence
result. This audit does not establish componentwise improvement, AA(1)
superiority, rank adequacy, or satisfaction of the physical AND gate, and it
does not authorize a real map.
