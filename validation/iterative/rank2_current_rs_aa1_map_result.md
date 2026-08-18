# Physical map from the $r,s$ AA(1) proposal

Date: 2026-08-18

Map classification: `VALID_NOT_MET`.

The standard unconstrained AA(1) proposal

$$
q_{12}=0.41267816249435374\,r+
0.58732183750564626\,s
$$

was evaluated exactly once from source commit
`3f3df1d58f03bfc7fb990e476d2f9358089f484c`:

$$
t=G_2(q_{12}).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $t-q_{12}$

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,4.684047945454728\times10^{-4},\,
6.862974260002375\times10^{-7}\ \mathrm{cm}^{-1},\,
5.179951998082914\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes.  $R_L$ and $R_a$ fail at `936.809589` and `1.035990400` tolerance
multiples.  Dimensional $D_L$ remains diagnostic only.  SPOT therefore still
has no accepted rank-two fixed point.

Relative to the preceding genuine residual $s-q_{11}$, $R_L$ and $D_L$
increase by about `7.1231%`, $R_a$ increases by about `28.9944%`, and
$R_\rho$ becomes zero.  This is mixed single-step evidence, not a
convergence-rate claim.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 3 | `0` | `4.21292270e-7` | 4 | `3.28225696e-7` |
| radial plane 2 | 7 | `0` | `4.96231621e-7` | 1 | `4.96231621e-7` |
| radial plane 3 | 13 | `0` | `4.54335947e-7` | 1 | `4.54335947e-7` |
| axial | 216 | `6.24070351e-10` | `4.13012714e-7` | 1 | `4.81848133e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.015660e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact contains 22 regular files, no symbolic links, and a passing 21/21
receipt.

| output | SHA-256 |
|---|---|
| returned AX | `135334cf0c961eae0c591d6a75e59a0cd60d42d7a660c421e45da3d2248d2b54` |
| returned snapshots | `88e442304e73a82cf1dd91c11225c41c3492a5706c3819250080df9ed3ef4579` |
| radial log | `fc8dcd67c2ebfcc9e288b9a0a7294535535e077a38b8b264e9aa45b7be9ea00a` |
| axial log | `ec15ff1254d7e21214c0c9782fdeb867155a9a30a9fdfb4cc9c1ef3e1f1d5dce` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `048e71f74d1d534a5fdb753ed6e50461731f6b78c4f31cc3984ebb3dd5d8daf6` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $s-q_{11}$ and
$t-q_{12}$.  The existing two-AA1 generic checker roles were bound exactly
as $Q6=q_{11}$, $M=s$, $Q7=q_{12}$, and $N=t$.  The standard affine output
direction is

$$
q_{13}=0.71645836326662038\,s+
0.28354163673337962\,t.
$$

The denominator is `1.0985063835946206e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.72586264533733025,\ 0.72631617652927194,\
0.90812221320053177).
$$

All three are strictly below one.  Independent builder and checker arithmetic
agree bitwise and confirm 8880/8880 positive reconstructed points.  The final
offline classification is `AA1_DIRECTION_PASS_AA2_SKIPPED`: because AA(1)
passes, AA(2) is not calculated.

The temporary diagnostic publication hashes were
`20c3f84d2e5cfc32a5a8f91e6349aa63a1902ae001d34eab27645b67166a25e5`
for AX and
`97e887f6612c743c961d7fa6e6a9a75a87583b02f12f47a89ef7a1c63aa0810b`
for snapshots.  They were deleted after verification; no durable $q_{13}$
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
