# One physical map from the latest AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard proposal

$$
q_6=0.99334779753418823\,k+
0.0066522024658117341\,l
$$

was evaluated exactly once from source commit
`5cf970008de0eb600b253fae3e2e6a4a2e1caadc`:

$$
m=G_2(q_6).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $m-q_6$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
6.815023315567540\times10^{-4},\,
9.985233191400766\times10^{-7}\ \mathrm{cm}^{-1},\,
4.087844475064791\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes; $R_L$ and $R_a$ fail.  Dimensional $D_L$ remains diagnostic only,
so SPOT still has no accepted rank-two fixed point.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `4.39794547e-7` | 4 | `2.29756651e-7` |
| radial plane 2 | 4 | `0` | `3.88510045e-7` | 3 | `4.21303071e-7` |
| radial plane 3 | 17 | `0` | `4.73592706e-7` | 4 | `3.80436859e-7` |
| axial | 169 | `3.92150368e-10` | `4.81848417e-7` | 1 | `4.81848417e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.780383e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact has a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `76e4d5e44a6f0a1020fd6280c8da262b322acba80940799a28fc3998ef3da4fc` |
| returned snapshots | `af1ffa33b39dc9df8e6a7f4813d408974f933bd39f4e512e68f135927d9cb406` |
| radial log | `0bc85ccc3e4d7ff59525d109191679b4f24ed22f2e85c44339659a120239cb3f` |
| axial log | `9f65970e686bd05f0eaa2334841686457d55c533261dd8a23bd4e58684bcb277` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `2a53e45bcefc7347b0187cfa302cbe4276108fb1dc6bfdaac6e1099cd63ea79c` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $l-k$ and $m-q_6$.  Its
standard unconstrained affine output direction is

$$
q_7=0.71958187611175339\,l+
0.28041812388824661\,m.
$$

The scalar denominator is `1.4220277430317252e-11`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.089320649038882691,\ 0.82454368960985658,\
0.56421285796347498).
$$

All three are strictly below one, so the offline classification is
`AA1_DIRECTION_PASS_AA2_SKIPPED`.  The independent checker reproduced the
weights and ratios bitwise, verified the $q_6\mapsto m$ snapshot lifecycle,
and found 8880/8880 positive reconstructed points.  This is a direction
authorization, not convergence evidence.

The diagnostic proposal was temporary and was deleted after the decision;
no durable successor and no second physical map were produced.
AA(2) was not calculated.  No relaxation, damping, clipping, fit, regularization,
pseudoinverse, condition cutoff, empirical parameter, mixed-unit objective,
older-window search, or AA(3) was used.
