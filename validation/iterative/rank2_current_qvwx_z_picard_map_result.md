# Direct Picard map from the current $qvwx$ return

Date: 2026-08-17

Map classification: `VALID_NOT_MET`.

Exactly one direct continuation

$$
z^+=G_2(z)
$$

ran from source commit
`3a30ffd94100df023bfb446487a44311a05a181f`.  The hash-locked returned
state $z$ was used unchanged; there was no affine mixing, retry, fallback,
or automatic successor.  Three fresh online radial fixed-source solves and
one axial solve returned

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,5.324646091595354\times10^{-4},\,
7.801572792232037\times10^{-7}\ \mathrm{cm}^{-1},\,
1.309957085222539\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes.  $R_L$ and $R_a$ fail at `1064.929218` and `2.619914` tolerance
multiples.  Dimensional $D_L$ remains diagnostic only and is not part of
the gate.  SPOT therefore still has no accepted rank-two fixed point.

The preceding physical residual is $z-y$, so this comparison is genuinely
consecutive.  From $z-y$ to $z^+-z$, $R_L$ and $D_L$ increased by
`40.8691996%`, while $R_a$ decreased by `28.8731546%`.  This single
component-wise change is neither an asymptotic contraction factor nor a
proof of divergence or cycling.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|---:|
| radial plane 1 | 3 | `0` | `4.98582494e-7` | 3 | `3.47066845e-7` | 15 s |
| radial plane 2 | 4 | `0` | `3.46972257e-7` | 4 | `3.60374116e-7` | 16 s |
| radial plane 3 | 13 | `0` | `4.84215036e-7` | 3 | `4.84215036e-7` | 34 s |
| axial | 198 | `1.63543068e-10` | `4.47429983e-7` | 1 | `4.40005721e-7` | 135 s |

All strict terminals passed below `4.99999999e-7`.  The independent
`continued` Ganlib checker passed fixed POD identity, live radial-operator
change, raw radial positivity, canonical layout, bitwise raw defects, and
restart archive.  The global balance diagnostic is `7.14047e-9`; it is
separate from the outer fixed-point gate.

The Git-ignored artifact has 22 regular files, no symbolic links, and a
passing 21/21 receipt.

| output | SHA-256 |
|---|---|
| returned AX | `0f2bf2c721097ab85afd0946500578c4fd8feaac657e8302515ed1d494ffa5b3` |
| returned snapshots | `e070b086b8a6aac41108b6cbd27918cc906e77e5c329a442fbac04ac7e2b7e95` |
| radial log | `72903c1753e85b465884817acdde75fa60478f68246116f60a3e9c42a5051f93` |
| axial log | `88e1899c842d933604e6e7f40209f4981ca3e49ecabb11d63b46c2c1c64b2f17` |
| independent check | `0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02` |
| receipt | `933d0fb34a517006c48edf0e9afa13b9424331d729fe3c0e31fc33ee1f6dd0ac` |

## Next minimum-order direction

Only after the map, the genuine adjacent residuals

$$
f_0=z-y,\qquad f_1=z^+-z
$$

were used in standard, unregularized full-Gram AA(1).  It gives the formal
next proposal

$$
y_{\mathrm{AA1}}=
0.41511181447765411\,z+
0.58488818552234589\,z^+.
$$

The denominator is `4.3847089635551763e-12`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.093357573037484751,\ 0.42214650302136536,\
0.61065652318148245).
$$

All three are strictly below one.  The reconstructed field is positive at
8880/8880 points, with minimum `1.7534035170790798e-15`.  The classification
is therefore `AA1_DIRECTION_PASS_AA2_SKIPPED`: minimum order passes, so AA(2)
is not computed.

An independent temporary checker reproduced the bitwise carrier and
snapshot lifecycle.  Its deterministic temporary AX and snapshot hashes
were `5d462c634e7f909ff059d72ac8bb8d9240cb18c21232c682c99d8f34d791c67c`
and `3c216fff2be1336c29e584e4b8b0d6d9eca537f80c6a5fc07bf08f4ad509eb84`.
They are audit values, not published candidate artifacts.

This batch stops at the direction decision.  It does not materialize the
proposal and does not run a second physical map.  No relaxation, damping,
clipping, fit, regularization, pseudoinverse, condition cutoff, empirical
parameter, mixed-unit objective, older-window search, or AA(3) is used.
