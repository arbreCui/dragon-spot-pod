# Physical map from the $i,j$ AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard unconstrained full-Gram proposal

$$
q_5=1.1922339465680236\,i-
0.19223394656802359\,j
$$

was evaluated exactly once from source commit
`fbe6058300a93cc771bc050f81397aa2f563b9e7`.  Three fresh online radial
fixed-source solves and one axial solve produced $k=G_2(q_5)$ and the
physical residual $k-q_5$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
3.413471840828782\times10^{-4},\,
5.001347744837403\times10^{-7}\ \mathrm{cm}^{-1},\,
1.330790586136073\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.128446962` tolerance multiples.  $R_L$ and $R_a$ fail at
`682.694368` and `2.661581172` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Relative to the preceding genuine residual $j-q_4$, $R_L$ and $D_L$
decrease by about `31.344%`, and $R_a$ decreases by about `77.834%`.
Because the two residuals were evaluated at different inputs, this is not a
contraction factor or proof of convergence.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 3 | `0` | `4.99504893e-7` | 5 | `2.67670941e-7` |
| radial plane 2 | 6 | `0` | `4.75656321e-7` | 4 | `3.13539744e-7` |
| radial plane 3 | 10 | `0` | `4.08440343e-7` | 5 | `4.37871421e-7` |
| axial | 223 | `1.08976905e-9` | `4.40006659e-7` | 1 | `4.40006659e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.644753e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `d8c77928f992adf67136331192a018060f203bedf3d1728d46a39d987c6938de` |
| returned snapshots | `343afaa62d1c6b0e880afe1cd090c944ffc7ecab837125c76b048987634ea9ae` |
| radial log | `6681119c0a37817e49a6a0c4264aa8a27ab5ef66f25dc52f5f3113a187d5360f` |
| axial log | `19f92f7b417d5eaf2743e4b43c21f0325c01744590c8b5d0cdcc2fb6672f9245` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `8c8b9d18f208f91494b3fac79947abcbd2bd46b2605b9af6e441c6eba93bd5f0` |

## Minimum-order direction decision

AA(1) was tested first, using only the genuine residuals $j-q_4$ and
$k-q_5$.  Its standard affine output direction is

$$
0.17292455736665602\,j+0.82707544263334398\,k.
$$

Its denominator is `2.3273113779303836e-11`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.33957735217447371,\ 0.88879107302551907,\
1.0008704340662933).
$$

The third ratio is not strictly below one, so the unchanged gate rejects
AA(1).  Only after that strict rejection, the latest three genuine
residuals $i-q_3$, $j-q_4$, and $k-q_5$ were used in standard unregularized
full-Gram AA(2).  Its affine output direction is

$$
0.64695441259132080\,i-
0.029106166249854366\,j+
0.38215175365853354\,k.
$$

The exact $2\times2$ determinant is `4.8856879432852540e-24`.  Its three
direction ratios are

$$
(0.060133483366234260,\ 0.49773629519031415,\
1.2201877109802688).
$$

AA(2) also fails the unchanged maximum-$|D_L|$ screen.  Strict production
builders rejected both directions before publication.  Temporary
diagnostic-only copies bypassed only the already-triggered gate abort so
the ratios could be emitted and reproduced bitwise by the independent
checker; both hypothetical reconstructions remained positive at 8880/8880
points.  The temporary proposals were not authorized or retained.

The final offline classification is
`AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL`.  No durable successor and no
second physical map were produced.  No relaxation, damping, clipping, fit,
regularization, pseudoinverse, condition cutoff, empirical parameter,
mixed-unit objective, older-window search, or AA(3) was used.
