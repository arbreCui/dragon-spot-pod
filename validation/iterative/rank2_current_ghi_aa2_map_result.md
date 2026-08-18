# Physical map from the $g,h,i$ AA(2) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
q_4=0.54656692430484066\,g+
0.22903224207636369\,h+
0.22440083361879565\,i
$$

was evaluated exactly once from source commit
`d78482590ca0d9be8078d15407a49b04bc5552dd`.  Three fresh online radial
fixed-source solves and one axial solve produced $j=G_2(q_4)$ and the
physical residual $j-q_4$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422346976453497\times10^{-8},\,
4.971869112913671\times10^{-4},\,
7.284688763320446\times10^{-7}\ \mathrm{cm}^{-1},\,
6.003808415562571\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.128446940` tolerance multiples.  $R_L$ and $R_a$ fail at
`994.373823` and `12.007616831` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Relative to the preceding genuine residual $i-q_3$, $R_\rho$ is unchanged
to the shown precision, while $R_L$ and $D_L$ increase by about `5.7948%`
and $R_a$ increases by `476.9614%`.  This single step is unfavorable in the
axial coordinate; it is not a proof of divergence.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.50912381e-7` | 4 | `3.24306058e-7` | 18 s |
| radial plane 2 | 3 | `0` | `4.67423263e-7` | 4 | `2.51384392e-7` | 16 s |
| radial plane 3 | 10 | `0` | `3.29495094e-7` | 4 | `2.88971080e-7` | 26 s |
| axial | 151 | `7.74708020e-10` | `4.81848019e-7` | 1 | `4.81848019e-7` | 134 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa2` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.08851e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `1910e6d0c4bc413cda29713d7bb38191d5ab41ca6f1564f07a9a1a093e240f42` |
| returned snapshots | `ff2f7e2ab6fbd955212fdf337f318657757eb04e507a65bd4669cefe65d0d587` |
| radial log | `fd8fcf95747f19f2579113a1c8753f46d91993793a567e760d6ab71f00f07453` |
| axial log | `0e9d23fbdf9c307738ee23764917c25df08586e3472dad93081fdf5bbd426049` |
| independent check | `44833ba13613d7a928f6ad64bf603848051268cb60078aa60fe687c5b99fdfe2` |
| receipt | `b468c4381da4093d1055f51c320150faf0162f022942acde5611673c49588c1c` |

## Minimum-order direction decision

The next AA(1) used only the genuine residuals $i-q_3$ and $j-q_4$.  Its
standard unregularized affine output direction is

$$
q_5=1.1922339465680236\,i-
0.19223394656802359\,j.
$$

Its denominator is `1.1217162258501826e-11`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.064424480296712869,\ 0.93186663298811390,\
0.97357313211276764).
$$

All three are strictly below one.  Independent builder and checker
arithmetic agree and confirm 8880/8880 positive reconstructed points.  The
negative coefficient is the unconstrained AA(1) result; it is not clipped
or replaced.  The final offline classification is `AA1_DIRECTION_PASS`.

This direction decision is not convergence evidence.  No durable $q_5$
proposal is published and no second physical map is run.  Because AA(1)
passes, AA(2) is not calculated.  No relaxation, damping, clipping, fit,
regularization, pseudoinverse, condition cutoff, empirical parameter,
mixed-unit objective, older-window search, or AA(3) is used.
