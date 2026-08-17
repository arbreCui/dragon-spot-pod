# Physical map from the $e,f$ AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
q_1=0.54317069088638781\,e+
0.45682930911361219\,f
$$

was evaluated exactly once from source commit
`afbd273a52ac55cd2164b465f59eb94d7f110171`.  Three fresh online radial
fixed-source solves and one axial solve produced $g=G_2(q_1)$ and the
physical residual $g-q_1$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
3.858515151996695\times10^{-4},\,
5.653419066220522\times10^{-7}\ \mathrm{cm}^{-1},\,
1.741219010720005\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$ and
$R_a$ pass at `0.128446962` and `0.348243802` tolerance multiples.  $R_L$
fails at `771.703030` multiples.  Dimensional $D_L$ is diagnostic only.
SPOT therefore still has no accepted rank-two fixed point.

Against the preceding genuine residual $f-e$, $R_\rho$, $R_L$, $D_L$, and
$R_a$ decreased by `50.000004%`, `53.614182%`, `53.614156%`, and
`88.431949%`.  This is a favorable single step, not an asymptotic
contraction or convergence result.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `4.98841018e-7` | 3 | `4.60739244e-7` | 19 s |
| radial plane 2 | 6 | `0` | `3.11236732e-7` | 4 | `3.02890214e-7` | 21 s |
| radial plane 3 | 17 | `0` | `2.46186147e-7` | 4 | `2.94098811e-7` | 36 s |
| axial | 211 | `1.17899979e-9` | `4.88895523e-7` | 1 | `4.88895523e-7` | 138 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.08650e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `1b52b5ebd421e620f1f9d7d4e60e50fb002f85c25031533cc4d650e858dd030a` |
| returned snapshots | `7a0e441a25ad2cc3067210dd6ebd90cb26ba5a9722a4c38ea289237590e90602` |
| radial log | `142fb066d07bab930ecc917d6c204b564b523c9a4b729b0c4863d96a59af4dca` |
| axial log | `b549e7672b247f03ae693dbd6466c2e6acf0340663329d6ff15522cfa8687fb3` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `2c852d2ba1cc07e5a3bfeef2c5618c7603e34738cafb64fdf3f3a3f5ca325747` |

## Minimum-order direction decision

The next AA(1) used only the genuine residuals $f-e$ and $g-q_1$.  Its
affine output direction is

$$
q_{\mathrm{AA1}}=-0.054660706649195978\,f+
1.0546607066491960\,g,
$$

with denominator `8.9502797595728729e-13`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.89522417182376191,\ 1.0164960989601337,\
1.0021076380581850).
$$

Both leakage ratios exceed one, so AA(1) fails the predeclared strict
direction gate.  Only then was standard unregularized full-Gram AA(2)
evaluated from the latest three genuine residuals
$e-c_{\mathrm{next}}$, $f-e$, and $g-q_1$.  Its affine output direction is

$$
q_{\mathrm{AA2}}=0.37059923635358261\,e+
0.28970803656130206\,f+
0.33969272708511533\,g.
$$

The exact Gram-system entries are

$$
(H_{00},H_{01},H_{11})=
(8.4049480818263211\times10^{-13},\,
-8.3167915360888345\times10^{-13},\,
8.9502797595728517\times10^{-13}),
$$

with positive determinant `6.0576152422719129e-26`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ ratios are

$$
(0.33342566026806181,\ 0.47696732762436056,\
0.39981312880450964).
$$

All three are strictly below one.  Independent builder and checker
arithmetic agree and confirm 8880/8880 positive reconstructed points.  The
final offline classification is `AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS`.

This direction decision is not convergence evidence.  No durable next
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
