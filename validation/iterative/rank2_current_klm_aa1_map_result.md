# One physical map from the latest AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard proposal

$$
q_7=0.71958187611175339\,l+
0.28041812388824661\,m
$$

was evaluated exactly once from source commit
`767fe7da92de238fdb7face911cf7e487c7e4901`:

$$
n=G_2(q_7).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $n-q_7$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.990742346753720\times10^{-4},\,
7.312337402254343\times10^{-7}\ \mathrm{cm}^{-1},\,
4.639312542887599\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$ and
$R_a$ pass; $R_L$ fails.  Dimensional $D_L$ remains diagnostic only, so
SPOT still has no accepted rank-two fixed point.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 11 | `0` | `3.69598240e-7` | 1 | `4.88931164e-7` |
| radial plane 2 | 5 | `0` | `4.96844450e-7` | 5 | `3.40953619e-7` |
| radial plane 3 | 2 | `0` | `4.93060440e-7` | 3 | `4.33107232e-7` |
| axial | 222 | `5.57700330e-10` | `3.64224377e-7` | 1 | `4.80351218e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.280868e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact has a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `973f8951dca356d1f9c3d42bfc8791fda19bb5263b3dea3ca9df8fa3f1712e56` |
| returned snapshots | `4371455c7fccff86d6586447d1e0433db5743ee1c1af2cdcdb4c5c30f4df4c4f` |
| radial log | `2af03ce20f1b958776ef94086e00ffb4b859e7d145f26a704e3d11ddfeca1418` |
| axial log | `679556e445847de87f4a60b4ebdf65eb9ef2bf5dd8a66adc3eefa510fa71cbd5` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `11d847935af19f6f74b7295980f194880e64ce58d2929bec7dd970279ad73d79` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $m-q_6$ and $n-q_7$.
Its standard unconstrained affine output direction is

$$
-0.061472310444878220\,m+
1.0614723104448782\,n.
$$

The denominator is `6.5246745314225801e-12`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.86145202366683948,\ 1.0902164970939685,\
1.0741288780839371).
$$

The two leakage ratios exceed one, so AA(1) is rejected.  Only after that
failure, standard unregularized full-Gram AA(2) used the three latest genuine
residuals $l-k$, $m-q_6$, and $n-q_7$.  Its affine output direction is

$$
q_8=0.37973124035268829\,l+
0.10995812065327257\,m+
0.51031063899403917\,n.
$$

The exact $2\times2$ system has

$$
(H_{00},H_{01},H_{11})=
(1.8044480565486487\times10^{-12},\,
-2.9455774211730038\times10^{-12},\,
6.5246745314225818\times10^{-12})
$$

and determinant `3.0970099337137395e-24`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.16177043590261239,\ 0.45458049672516687,\
0.46901724246492071).
$$

All three are strictly below one, so the offline classification is
`AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS`.  The independent checker reproduced
the exact unregularized system, weights and ratios bitwise, verified the
$q_7\mapsto n$ snapshot lifecycle, and found 8880/8880 positive reconstructed
points.  This is a direction authorization, not convergence evidence.

Both diagnostic candidates were temporary and were deleted after the
decision; no durable successor and no second physical map were produced.
No relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3) was used.
