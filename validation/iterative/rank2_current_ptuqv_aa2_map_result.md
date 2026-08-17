# Physical map from the latest three-pair AA(2) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
w=0.19768585711059219\,t
 +0.21627230078843410\,u
 +0.58604184210097376\,v
$$

was evaluated exactly once as $x=G_2(w)$.  The map performed three fresh
online radial fixed-source solves and one axial solve.  It returned

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.727944364001103\times10^{-4},\,
6.927293725311756\times10^{-7}\ \mathrm{cm}^{-1},\,
1.393495790324661\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.12844696` tolerance multiples.  $R_L$ and $R_a$ fail at
`945.588873` and `2.786992` multiples.  Dimensional $D_L$ is diagnostic and
is not part of that gate.  SPOT therefore has no accepted rank-two fixed
point.

Compared with the preceding evaluated residual $v-q$, $R_L$, $D_L$, and
$R_a$ increased by `18.5712957%`, `18.5712862%`, and `475.290495%`.
$R_\rho$ changed from exact zero but remains below tolerance.  Because the
inputs $q$ and $w$ differ, this is a cross-input nonlinear response, not a
contraction, divergence, or cycle measure.  It shows only that this
particular favorable offline AA(2) direction did not produce a smaller
realized nonlinear defect.

## Strict solver terminals

| solve | IEXTF | EUNK | ITERF | EINR | FLU time |
|---|---:|---:|---:|---:|---:|
| radial snapshot 1 | 3 | `4.88917863e-7` | 5 | `2.52248469e-7` | 16 s |
| radial snapshot 2 | 5 | `4.44579456e-7` | 6 | `4.21303184e-7` | 21 s |
| radial snapshot 3 | 5 | `2.75651985e-7` | 4 | `3.43543462e-7` | 21 s |
| axial | 180 | `4.81848474e-7` | 1 | `4.81848474e-7` | 140 s |

The axial eigenvalue terminal has `EEXT=2.91576430e-10`.  The independent
Ganlib checker passed the proposal lifecycle, fixed POD package, live radial
operator, raw radial positivity, canonical layout, four raw defects, and
restart archive.  The global balance diagnostic is `7.078301e-9`; it is
separate from the outer fixed-point gate.

## Reproducibility

The default-off host was activated once from source commit
`9c1fe4b6109c2cd2c2fcfae8904d6aa9c1af190e`.  It made no retry, fallback,
or automatic successor.  The artifact contains 22 regular files, no
symbolic links, and a passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `601a2a1c032d24c0f4a5b04d41d805d035b342f13bee7c5d8c07ef1ec0028d7d` |
| returned snapshots | `043918ac6433363a62f5bbc4ed1f04a80f9715c1669c496623a5ec6b01ff39b2` |
| radial log | `6d8ec0bd8b0a9cd6c37193f1b1eba275bfb51cf3a1011daf72de8f68e1d6b633` |
| axial log | `10d8202ccbf94ebe870044145e485e34cb3fefda60e897865e5a20584503ef2e` |
| independent check | `44833ba13613d7a928f6ad64bf603848051268cb60078aa60fe687c5b99fdfe2` |
| receipt | `30d52dff41de0541eeaff0a52587e9728f7db2a11deeca709d61c8c8d8f003bd` |

This stage introduced no empirical parameter, relaxation, damping,
clipping, fit, regularization, condition cutoff, mixed-unit objective, or
model correction.  No further map is authorized by this result.
