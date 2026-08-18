# Direct Picard map from the latest returned state $k$

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

After both latest-window AA directions were rejected, the newest valid
return was used unchanged in exactly one direct continuation

$$
l=G_2(k).
$$

The map was evaluated from source commit
`de35bc474fa5788acda9ce037d7a31721e07d34d`.  Three fresh online radial
fixed-source solves and one axial solve produced the physical residual
$l-k$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
3.744499849949860\times10^{-4},\,
5.486363079398870\times10^{-7}\ \mathrm{cm}^{-1},\,
1.628119765098577\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.128446962` tolerance multiples.  $R_L$ and $R_a$ fail at
`748.899970` and `3.256239530` multiples.  Dimensional $D_L$ remains
diagnostic only, so SPOT still has no accepted rank-two fixed point.

Relative to the preceding consecutive residual $k-q_5$, $R_L$ and $D_L$
increase by about `9.698%`, and $R_a$ increases by about `22.342%`.  This
single adjacent observation is not proof of divergence.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 12 | `0` | `3.99931452e-7` | 2 | `4.62753604e-7` |
| radial plane 2 | 6 | `0` | `4.58176856e-7` | 4 | `2.36994651e-7` |
| radial plane 3 | 24 | `0` | `3.67537041e-7` | 1 | `3.79753430e-7` |
| axial | 253 | `3.80954518e-10` | `4.80351275e-7` | 1 | `4.80351275e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`continued` checker passed the fixed POD package, live radial operator, raw
radial positivity, canonical layout, bitwise raw defects, and restart
archive.  The global balance diagnostic is `7.736085e-9`; it is separate
from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `fee603751609b7a9ab79ac854e7ecfa93125f3f4597e411e020728ae267180d0` |
| returned snapshots | `9ffe3428e70f001a5f0e3384a5030fe4a0334787d7454c0f0d143b2b4a5b165f` |
| radial log | `14648c4c9933bd86684f7c3d24950ecd11e25addf08b77bf051bab6b097f74a5` |
| axial log | `ced64ce06a098b8beafbddf7a5b82b776b66733d4596351e8a6bf550572a2867` |
| independent check | `0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02` |
| receipt | `393597539ad275c1094afea9d241265c7258dbd14229034c90c31140963766bf` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $k-q_5$ and $l-k$.  Its
standard unconstrained affine output direction is

$$
0.99334779753418823\,k+
0.0066522024658117341\,l.
$$

The scalar denominator is `3.9604495076589152e-13`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.81736979605403082,\ 0.80173988821917219,\
0.90621455552995278).
$$

All three are strictly below one, so the final offline classification is
`AA1_DIRECTION_PASS_AA2_SKIPPED`.  The independent checker reproduced the
weights and ratios bitwise, verified the returned-state and snapshot
lifecycle, and found 8880/8880 positive reconstructed points.  This is a
direction authorization, not convergence evidence.

The diagnostic proposal remained temporary and was deleted after the
decision; no durable successor and no second physical map were produced.
AA(2) was not calculated.  No relaxation, damping, clipping, fit,
regularization, pseudoinverse, condition cutoff, empirical parameter,
mixed-unit objective, older-window search, or AA(3) was used.
