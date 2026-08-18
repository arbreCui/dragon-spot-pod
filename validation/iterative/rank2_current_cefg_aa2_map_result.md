# Physical map from the $e,f,g$ AA(2) proposal

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
q_2=0.37059923635358261\,e+
0.28970803656130206\,f+
0.33969272708511533\,g
$$

was evaluated exactly once from source commit
`1be7a4070d1083592e7e8f966e383ea44196c14a`.  Three fresh online radial
fixed-source solves and one axial solve produced $h=G_2(q_2)$ and the
physical residual $h-q_2$

$$
(R_\rho,R_L,D_L,R_a)=
(1.284469506313002\times10^{-7},\,
4.808395175515263\times10^{-4},\,
7.045164238661528\times10^{-7}\ \mathrm{cm}^{-1},\,
1.190590942018258\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes at `0.256893901` tolerance multiples.  $R_L$ and $R_a$ fail at
`961.679035` and `2.381181884` multiples.  Dimensional $D_L$ is diagnostic
only.  SPOT therefore still has no accepted rank-two fixed point.

Relative to the preceding genuine residual $g-q_1$, the four reported
magnitudes increased by `99.999983%`, `24.617761%`, `24.617761%`, and
`583.768633%`.  This is a cross-input observation, not an asymptotic
divergence claim.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 3 | `0` | `4.84150689e-7` | 2 | `3.85363620e-7` | 15 s |
| radial plane 2 | 12 | `0` | `2.64450932e-7` | 3 | `3.86947079e-7` | 29 s |
| radial plane 3 | 8 | `0` | `4.93954019e-7` | 3 | `3.84949317e-7` | 21 s |
| axial | 229 | `2.44617687e-10` | `3.62972401e-7` | 1 | `3.62972401e-7` | 140 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa2` checker passed the proposal and carrier identities, fixed
POD package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.15828e-9`; it is separate from the fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `5e53f33aea3d91db6999cc735d4ffd47677545ba350f34e36a266ff5e6f123ad` |
| returned snapshots | `17da9628503fafe310ae7dc3223e34de61d78b4c9cc6e4a302ea6e1b6345e5de` |
| radial log | `ac48ddd23f83d9271b575e7d8607b346c683ac7ddff02acc9a815926ed1b3580` |
| axial log | `e8a3823dc3c636d8fd833f16a7541e8a3a2659c488e7baa3115f8d814f8d7fd3` |
| independent check | `44833ba13613d7a928f6ad64bf603848051268cb60078aa60fe687c5b99fdfe2` |
| receipt | `85b3c046fc88a5f2e7c49a0a8fbeeaf205f5e5627bcf258720f91e8afc463033` |

## Minimum-order direction decision

The next AA(1) used only the genuine residuals $g-q_1$ and $h-q_2$.  Its
affine output direction is

$$
q_3=0.92198482219461153\,g+
0.078015177805388483\,h,
$$

with denominator `7.3007449964465324e-13`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.11971305975561962,\ 0.47525043616253554,\
0.70441518119387303).
$$

All three are strictly below one.  Independent builder and checker
arithmetic agree, verify the `AA1-RAW-FLUX` and `AA2-RAW-FLUX` input
lifecycles, and confirm 8880/8880 positive reconstructed points.  The final
offline classification is `AA1_DIRECTION_PASS`.

This direction decision is not convergence evidence.  No durable $q_3$
proposal is published and no second physical map is run.  Because AA(1)
passes, AA(2) is not calculated.  No relaxation, damping, clipping, fit,
regularization, pseudoinverse, condition cutoff, empirical parameter,
mixed-unit objective, older-window search, or AA(3) is used.
