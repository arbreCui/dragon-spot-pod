# Physical map from the $z^+,d$ AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
c_{\mathrm{next}}=0.48771444550122545\,z^++
0.51228555449877455\,d
$$

was evaluated exactly once from source commit
`fa154ed421598c5f91fe9b5bd1878af46c993386`.  Three fresh online radial
fixed-source solves and one axial solve produced
$e=G_2(c_{\mathrm{next}})$ and the physical residual
$e-c_{\mathrm{next}}$:

$$
(R_\rho,R_L,D_L,R_a)=
(6.422349219104007\times10^{-8},\,
7.777215945396249\times10^{-4},\,
1.139502273872495\times10^{-6}\ \mathrm{cm}^{-1},\,
1.266857654692717\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.128446984` tolerance multiples.  $R_L$ and $R_a$ fail at
`1555.443189` and `2.533715` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Against the preceding genuine residual $d-c$, $R_L$ increased by
`56.831639%`, $D_L$ increased by `56.831564%`, and $R_a$ decreased by
`3.231555%`.  The relative change in the already-passing $R_\rho$ is
`0.0000176%`.  This is one leakage/modal tradeoff and does not establish an
asymptotic contraction or divergence rate.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `4.09391134e-7` | 4 | `3.73969840e-7` | 18 s |
| radial plane 2 | 5 | `0` | `4.59296956e-7` | 4 | `2.13766839e-7` | 18 s |
| radial plane 3 | 4 | `0` | `3.44729045e-7` | 4 | `2.77212763e-7` | 18 s |
| axial | 211 | `1.26764724e-10` | `4.80350138e-7` | 1 | `4.80350138e-7` | 135 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.67398e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `0b5c8d27b4d2e37d90d56d27d75619842851b7a0e0206947b31c3d5b88936828` |
| returned snapshots | `ae6ea8d66c581a496eb56feb512ef5dbbcd0e3a9596871b439a80a3c2a1e66e5` |
| radial log | `62df7c86571fd36b9789f3c4d3a59a031c72412d3dc12bfefc06dd47550bee10` |
| axial log | `90e46e6e80c6b6e38f882cfdc9443a345cad33eb9626db5fc749c99c3e943a0e` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `9d38fee591c54d67f31e57dfe36756a3b71029a1c4739842df1f0d3eb02275f8` |

## Minimum-order direction decision

The next AA(1) used only the genuine residuals $d-c$ and
$e-c_{\mathrm{next}}$.  Its affine output direction is

$$
q_1=-0.39205911614622169\,d+
1.3920591161462217\,e,
$$

with denominator `2.7132489406837032e-14`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.99707055678234369,\ 1.4891030102954350,\
1.5185498258021630).
$$

The two leakage ratios exceed one, so AA(1) fails the predeclared
parameter-free direction gate.  Only then was standard unregularized
full-Gram AA(2) evaluated from the three genuine residuals $z^+-z$, $d-c$,
and $e-c_{\mathrm{next}}$.  Its affine output direction is

$$
q_2=0.27450453816512377\,z^+
-0.60572182962205334\,d
+1.3312172914569296\,e.
$$

The exact $2\times2$ determinant is
`9.8259923215556172e-28`.  Its modal, leakage height-$L_2$, and same-weight
maximum-$|D_L|$ ratios are

$$
(0.99514908347179354,\ 1.3654718014730096,\
1.3434921133428195).
$$

The two leakage ratios again exceed one.  Independent read-only builder and
checker calculations agree, so the final offline classification is
`AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL`.  No next proposal is published and
no second map is run.

No relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3) is used.
