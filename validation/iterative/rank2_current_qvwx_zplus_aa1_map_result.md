# Physical map from the post-$z^+$ AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
c=0.41511181447765411\,z+
0.58488818552234589\,z^+
$$

was evaluated exactly once from source commit
`246a4cf48e7b2babbf04c089d9d09a0074f079e2`.  Three fresh online radial
fixed-source solves and one axial solve produced $d=G_2(c)$ and the physical
residual $d-c$:

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.958958534883100\times10^{-4},\,
7.265771273523569\times10^{-7}\ \mathrm{cm}^{-1},\,
1.309164007655304\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.128446962` tolerance multiples.  $R_L$ and $R_a$ fail at
`991.791707` and `2.618328` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Against the preceding genuine residual $z^+-z$, $R_L$ decreased by
`6.8678284%`, $D_L$ decreased by `6.8678654%`, and $R_a$ decreased by
`0.0605423%`.  $R_\rho$ changed from exact zero to a value still within
tolerance, so no percentage is assigned to it.  One simultaneous decrease
does not establish an asymptotic contraction rate or convergence.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.79798530e-7` | 3 | `4.99991131e-7` | 16 s |
| radial plane 2 | 5 | `0` | `3.69534376e-7` | 5 | `3.15914122e-7` | 20 s |
| radial plane 3 | 6 | `0` | `4.11651513e-7` | 1 | `3.94446772e-7` | 18 s |
| axial | 216 | `4.46501808e-10` | `4.81848076e-7` | 1 | `4.81848076e-7` | 134 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.53587e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `4a354fc32db3b9d12690b303527980b2f142c51cf27e1f2f4068180fdd1e7f93` |
| returned snapshots | `8d39306ab59adae8e9f4b05743cbdaace0c96f14506f26b34c82c06757052395` |
| radial log | `909f8646de945b7d8066c4336719a2e88fc9db361ddcf7ee62396be79c36f201` |
| axial log | `6a07cea488170ea3d97351fb81da6836c388eaa237a2d169e0103df9521a1c59` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `a610eebb33fee18a5af5040777e42948bc122463222904c11ab7bb8783188d39` |

## Next minimum-order direction

Only after the valid map, the genuine residuals

$$
f_0=z^+-z,\qquad f_1=d-c
$$

were used in standard unregularized full-Gram AA(1).  Two independent
read-only calculations agree on

$$
c_{\mathrm{next}}=
0.48771444550122545\,z^++
0.51228555449877455\,d.
$$

The denominator is `3.7547749561704630e-14`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.99411674241637549,\ 0.93884958302279575,\
0.79362266755606770).
$$

All three are strictly below one, so the classification is
`AA1_DIRECTION_PASS_AA2_SKIPPED`.  The modal ratio is close to one; this is
a valid direction authorization, not evidence that the next nonlinear map
will converge.  The reconstructed field is positive at 8880/8880 points,
with minimum `1.7534007642220012e-15`.

The temporary independent publication hashes were
`978593b2813bad2242ad8c235fdd83e6f5bc33b3aff624b60ccecaaf077d95c6`
for AX and
`cf43ed781a1f86625aa6ae46023eca2e6e000ed76d16c81470a3544b13bb0354`
for snapshots.  They are audit values, not materialized artifacts.

This batch stops at that direction decision.  AA(2) is not computed.  The next proposal is not materialized, and no second map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3) is
used.
