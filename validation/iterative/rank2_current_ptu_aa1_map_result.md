# Physical map from the current-window AA(1) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

The standard full-Gram AA(1) proposal

$$
q=0.41546155012473063\,t+0.58453844987526937\,u
$$

was evaluated exactly once as $q^+=G_2(q)$.  The map performed three fresh
online radial fixed-source solves and one axial solve.  It returned

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,3.987427427192006\times10^{-4},\,
5.842302925884724\times10^{-7}\ \mathrm{cm}^{-1},\,
2.422247198731598\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$ and
$R_a$ pass, while $R_L$ fails by a factor `797.485485438401`.  Dimensional
$D_L$ is reported separately and is not part of that dimensionless gate.
SPOT therefore has no accepted rank-two fixed point.

Compared with the preceding evaluated residual $u-t$, the new defect
magnitudes $R_L$, $D_L$, and $R_a$ are lower by `53.6846403%`,
`53.6846477%`, and `87.2181379%`, respectively.  This comparison uses a
different input $q$ and is evidence of a useful local accelerated step, not
a contraction factor or proof of future convergence.

## Strict solver terminals

All four solves met the unchanged strict terminal contract:

| solve | IEXTF | EUNK | EINR | FLU time |
|---|---:|---:|---:|---:|
| radial snapshot 1 | 4 | `4.70654669e-7` | `4.51018394e-7` | 17 s |
| radial snapshot 2 | 6 | `3.97476271e-7` | `2.43587408e-7` | 21 s |
| radial snapshot 3 | 5 | `4.31628933e-7` | `4.48281781e-7` | 20 s |
| axial | 204 | `4.81848588e-7` | `4.68288249e-7` | 140 s |

The axial eigenvalue terminal also has
`EEXT=3.13754439e-11`.  The process bounds of 120 s for the combined radial
stage and 180 s for the axial stage were safety limits, not model or
convergence parameters.

The independent Ganlib checker passed the proposal-parent lifecycle, fixed
POD package, live radial-operator change, raw radial positivity, canonical
layout, all four raw defects, and restart archive bit for bit.  The global
balance diagnostic is `7.261102e-9`; it is reported separately from the
outer fixed-point gate.

## Reproducibility

The default-off host was activated once from source commit
`39f075dc1d23b128f7a5b49c2469df7119c8138b`.  It made no retry, fallback,
or automatic successor.  The result artifact contains 22 regular files, no
symbolic links, and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `b58e6022a2d56f580038015bc0db2d2d584911d27633eccfbdb2d30ad9296fed` |
| returned snapshots | `2cb0fdc254599faacd695e25a043e2f3fd9331c848526929fb934ced2074ed81` |
| radial log | `89b23b66c7e2e36dd48cd11b1384ed055994e423f0c0dde1450fad2edb8b775a` |
| axial log | `f141401f06b44cdd5abf0c89e93879c58a0fbbc9f2460de14cb22cc2ee90127e` |
| independent check | `52a7f21aff57d8d0f3fb8097e98d55fce4d3c266873db2c0bc02e936f1c5dc1b` |
| receipt | `273d441e865381eb1a7d3742172d3e3e81de23ad8444d14f0fbab4f490e0f487` |

This stage introduced no relaxation, damping, clipping, fitted closure,
regularization, condition threshold, mixed-unit objective, or empirical
parameter.  No further map is authorized by this result.
