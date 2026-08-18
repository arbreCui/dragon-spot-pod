# Physical map from the $p,r$ AA(1) proposal

Date: 2026-08-18

Map classification: `VALID_NOT_MET`.

The standard unconstrained AA(1) proposal

$$
q_{11}=0.21697843452735655\,p+
0.78302156547264345\,r
$$

was evaluated exactly once from source commit
`9ff16f11d1d29e2268e0205618c29203088248ef`:

$$
s=G_2(q_{11}).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $s-q_{11}$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
4.372585176123830\times10^{-4},\,
6.406626198440790\times10^{-7}\ \mathrm{cm}^{-1},\,
4.015641907413114\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$ and
$R_a$ pass.  $R_L$ fails at `874.517035` tolerance multiples.  Dimensional
$D_L$ remains diagnostic only.  SPOT therefore still has no accepted
rank-two fixed point.

Relative to the preceding genuine residual $r-q_{10}$, $R_L$ and $D_L$
decrease by about `53.5238%`, $R_a$ decreases by about `27.9867%`, and
$R_\rho$ is unchanged.  This is favorable single-step evidence, not a
convergence-rate claim.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 3 | `0` | `4.04991965e-7` | 3 | `4.98581414e-7` |
| radial plane 2 | 2 | `0` | `3.99691913e-7` | 4 | `3.15466053e-7` |
| radial plane 3 | 4 | `0` | `3.78873978e-7` | 4 | `3.78873892e-7` |
| axial | 218 | `9.36300551e-11` | `4.88895182e-7` | 1 | `4.88895182e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.929295e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact contains 22 regular files, no symbolic links, and a passing 21/21
receipt.

| output | SHA-256 |
|---|---|
| returned AX | `7f9b0e62322acde5ffcfee4aab5d5d4da68b1b04dc7dbdc8314b39787b3b0e11` |
| returned snapshots | `26de1301b2c9773b18258c07686edba6e4bbc18d16168632da14a92483712219` |
| radial log | `dfb06a62affd3a9b70a8376ce5c88a44dd899a9d0a4976403e18e6b3a55f61b2` |
| axial log | `d9b6173784b9164f034e732778a40047b819176ba967f6c5e7923faed4fd89dc` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `e57c0fb5e3afde903024342d3289b664322019c721d2489b90b56b082b9e7b9c` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $r-q_{10}$ and
$s-q_{11}$.  The existing two-AA1 generic checker roles were bound exactly
as $Q6=q_{10}$, $M=r$, $Q7=q_{11}$, and $N=s$.  The standard affine output
direction is

$$
q_{12}=0.41267816249435374\,r+
0.58732183750564626\,s.
$$

The denominator is `3.8071754534215003e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.30785297571708414,\ 0.94676682054309913,\
0.98610570398914554).
$$

All three are strictly below one.  Independent builder and checker arithmetic
agree bitwise and confirm 8880/8880 positive reconstructed points.  The final
offline classification is `AA1_DIRECTION_PASS_AA2_SKIPPED`: because AA(1)
passes, AA(2) is not calculated.

The temporary diagnostic publication hashes were
`11c73abd4e35419da447429b6de73191b05d31cff132db0e762d45316f5b4e26`
for AX and
`779e419a8b2a378b837976dd726757c2bf13d406184126182eca64b00c065f6f`
for snapshots.  They were deleted after verification; no durable $q_{12}$
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
