# Physical map from the $o,p$ AA(1) proposal

Date: 2026-08-18

Map classification: `VALID_NOT_MET`.

The standard unconstrained AA(1) proposal

$$
q_{10}=1.2246645215600993\,o-
0.22466452156009933\,p
$$

was evaluated exactly once from source commit
`25c4f31132290de4c3816d972b4f469c1b682357`:

$$
r=G_2(q_{10}).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $r-q_{10}$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
9.408223459489815\times10^{-4},\,
1.378473825752735\times10^{-6}\ \mathrm{cm}^{-1},\,
5.576247465674659\times10^{-7}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes.  $R_L$ and $R_a$ fail at `1881.644692` and `1.115249493`
tolerance multiples.  Dimensional $D_L$ remains diagnostic only.  SPOT
therefore still has no accepted rank-two fixed point.

Relative to the preceding genuine residual $p-q_9$, $R_L$ and $D_L$
increase by about `38.5155%`, while $R_a$ decreases by about `68.3465%`.
This is mixed single-step evidence, not a convergence-rate claim.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.27178463e-7` | 3 | `3.79028648e-7` |
| radial plane 2 | 3 | `0` | `4.57631046e-7` | 4 | `2.28626902e-7` |
| radial plane 3 | 7 | `0` | `4.05371537e-7` | 4 | `2.09612523e-7` |
| axial | 229 | `5.49542967e-10` | `4.68290722e-7` | 1 | `4.68290722e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.121521e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact contains 22 regular files, no symbolic links, and a passing 21/21
receipt.

| output | SHA-256 |
|---|---|
| returned AX | `d92f92919316f1abd8b2c00712b0c804c6a82d141d4501c39d2dc77c9dec10ff` |
| returned snapshots | `4cc762f6932ed42af7ea22d6130b741c14c463d37c388c93fff2269646ee22f9` |
| radial log | `f0b7722d2190a005b49fb9abecb608539f8cdb97e07318aa724479580051af12` |
| axial log | `3a597a1bb04d011887d498ff0ea093bfb7e599d22a9a3cbba580222d61f27455` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `61e023e4d795618d6f8cf4fd2b4774b84a8fcf55afc24a75ebce47b6ddd92606` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $p-q_9$ and $r-q_{10}$.
The existing two-AA1 generic checker roles were bound exactly as
$Q6=q_9$, $M=p$, $Q7=q_{10}$, and $N=r$.  The standard affine output
direction is

$$
q_{11}=0.21697843452735655\,p+
0.78302156547264345\,r.
$$

The denominator is `2.1912767600921286e-12`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.50304720552788507,\ 0.87862793996767796,\
0.82134690926235421).
$$

All three are strictly below one.  Independent builder and checker arithmetic
agree bitwise and confirm 8880/8880 positive reconstructed points.  The final
offline classification is `AA1_DIRECTION_PASS_AA2_SKIPPED`: because AA(1)
passes, AA(2) is not calculated.

The temporary diagnostic publication hashes were
`20b4a9fb31f6baa4f62d9fa5b22cf0801709ceb37579bf9f16dfc7e6c450f05d`
for AX and
`d974a4883eaa5460614d25cdf81284644760218308c88f35ed41bd54065d0167`
for snapshots.  They were deleted after verification; no durable $q_{11}$
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
