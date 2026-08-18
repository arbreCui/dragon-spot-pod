# Physical map from the $g,h$ AA(1) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
q_3=0.92198482219461153\,g+
0.078015177805388483\,h
$$

was evaluated exactly once from source commit
`a802ba1031414c4e25c74791f1043d453b5387c1`.  Three fresh online radial
fixed-source solves and one axial solve produced $i=G_2(q_3)$ and the
physical residual $i-q_3$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.699542341368844\times10^{-4},\,
6.885675247758627\times10^{-7}\ \mathrm{cm}^{-1},\,
1.040590980549194\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.128446962` tolerance multiples.  $R_L$ and $R_a$ fail at
`939.908468` and `2.081181961` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Relative to the preceding genuine residual $h-q_2$, all four magnitudes
decreased by `49.999996%`, `2.263808%`, `2.263808%`, and `12.598782%`.
This is a one-step observation, not a convergence claim.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.04028157e-7` | 6 | `2.26243088e-7` | 18 s |
| radial plane 2 | 10 | `0` | `2.80131928e-7` | 4 | `3.28463955e-7` | 29 s |
| radial plane 3 | 2 | `0` | `4.58566490e-7` | 2 | `4.74481254e-7` | 14 s |
| axial | 204 | `1.07769260e-9` | `4.13012856e-7` | 1 | `4.81848360e-7` | 132 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.18321e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `c35dc70d8d6dd35b889622734b81112a3e3fdc09455f8390ef262123f5aa3636` |
| returned snapshots | `c4f0b6ff6d6ffa28ff3a34061e5cf9e25c78fb1b31546188e932c5e82492f9b1` |
| radial log | `46ffaf932e88a81998dcd3eead523de9d123ba867fa4752d4c80c95d7438db3d` |
| axial log | `c694862fcba54eef464a0ab72b27f8ffac308b95b9a1c3194b9571a9e57b62cb` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `52f6ddd62d50c6cec8357c8bd7b34eb6c396db1e0cbe850a027d7b23cac37bf3` |

## Minimum-order direction decision

AA(1) was tried first using only the genuine residuals $h-q_2$ and
$i-q_3$:

$$
q_4^{(1)}=0.46547000956679907\,h+
0.53452999043320093\,i.
$$

Its denominator is `2.1525757104699773e-12`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.17415987368600511,\ 1.0001541854604454,\
0.84332141156226892).
$$

The leakage height-$L_2$ ratio is not strictly below one, so AA(1) fails.
Only then, standard unregularized full-Gram AA(2) on $g-q_1$, $h-q_2$, and
$i-q_3$ gives

$$
q_4^{(2)}=0.54656692430484066\,g+
0.22903224207636369\,h+
0.22440083361879565\,i.
$$

The exact $2\times2$ determinant is `7.9724244756408422e-26`; no condition
cutoff or regularization is applied.  Its three direction ratios are

$$
(0.085602787687317231,\ 0.50064418931908561,\
0.44048518991529284),
$$

all strictly below one.  Independent builder and checker arithmetic agree
and confirm 8880/8880 positive reconstructed points.  The final offline
classification is `AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS`.

These direction screens do not establish convergence.  No durable $q_4$
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3) is
used.
