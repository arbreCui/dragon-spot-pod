# Physical map from the $l,m,n$ AA(2) proposal

Date: 2026-08-18

Map classification: `VALID_NOT_MET`.

The standard full-Gram proposal

$$
q_8=0.37973124035268829\,l+
0.10995812065327257\,m+
0.51031063899403917\,n
$$

was evaluated exactly once from source commit
`334d3eebddaef382ddedc4ba99457518a375d83d`:

$$
o=G_2(q_8).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $o-q_8$

$$
(R_\rho,R_L,D_L,R_a)=
(0,\,
4.573608580149287\times10^{-4},\,
6.701156962662935\times10^{-7}\ \mathrm{cm}^{-1},\,
3.915463384152092\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$ and
$R_a$ pass; $R_L$ fails at `914.721716` tolerance multiples.  Dimensional
$D_L$ remains diagnostic only.  SPOT therefore still has no accepted
rank-two fixed point.

Relative to the preceding genuine residual $n-q_7$, $R_L$ and $D_L$
decrease by about `8.3582%`, and $R_a$ decreases by about `15.6025%`.
This is favorable single-step evidence, not a convergence-rate claim.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.56006944e-7` | 2 | `4.27348340e-7` |
| radial plane 2 | 6 | `0` | `4.42536447e-7` | 5 | `4.18054185e-7` |
| radial plane 3 | 6 | `0` | `3.78753100e-7` | 3 | `3.65814373e-7` |
| axial | 216 | `3.02496667e-10` | `4.13012771e-7` | 1 | `4.81848247e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa2` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`6.706487e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact contains 22 regular files, no symbolic links, and a passing 21/21
receipt.

| output | SHA-256 |
|---|---|
| returned AX | `48369be8c875f7c1389c850b89287d5a649d72047afd34964dc69a7067eb1a13` |
| returned snapshots | `3a11159cd8dff5703a28da1222ee8dab798f46d54ba0a0a46bee1119e70caf3e` |
| radial log | `ba6afa042f1ba2ab615ea1ea9596e4b672ba3b80666fc3cc0f99796609505324` |
| axial log | `82b1cbfaa4b5f005a8b2e0cc85741fabe76e347cc9e704b1a4685860623075ef` |
| independent check | `44833ba13613d7a928f6ad64bf603848051268cb60078aa60fe687c5b99fdfe2` |
| receipt | `05261d095719f530baf4ed3743e964aa4e6ec0c799ea36021676d3f1fbe69a3c` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $n-q_7$ and $o-q_8$.
Its standard unconstrained affine output direction is

$$
q_9=0.14445266271586943\,n+
0.85554733728413057\,o.
$$

The denominator is `3.8680130073227605e-14`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.99405602856832498,\ 0.78327883203609316,\
0.82926667695332601).
$$

All three are strictly below one.  Independent builder and checker
arithmetic agree bitwise and confirm 8880/8880 positive reconstructed points.
The final offline classification is
`AA1_DIRECTION_PASS_AA2_SKIPPED`: because AA(1) passes, AA(2) is not
calculated.

The temporary diagnostic publication hashes were
`c5d3275ead6dc8b5afb6d7ec125965678a0659ed8cf027d547edd6a009738b4e`
for AX and
`f7476c9f42d5de128e56c01044609e233a11ec147019942d429b8db419ba30ab`
for snapshots.  They were deleted after verification; no durable $q_9$
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
