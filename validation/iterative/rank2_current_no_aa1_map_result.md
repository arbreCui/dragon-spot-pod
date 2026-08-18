# Physical map from the $n,o$ AA(1) proposal

Date: 2026-08-18

Map classification: `VALID_NOT_MET`.

The standard AA(1) proposal

$$
q_9=0.14445266271586943\,n+
0.85554733728413057\,o
$$

was evaluated exactly once from source commit
`8f1eb8fc19a3ee71a839f0661712910cac9b6a89`:

$$
p=G_2(q_9).
$$

Three fresh online radial fixed-source solves and one axial solve produced
the physical residual $p-q_9$

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
6.792180645546773\times10^{-4},\,
9.951763786375523\times10^{-7}\ \mathrm{cm}^{-1},\,
1.761650656565653\times10^{-6}).
$$

At the unchanged $5\times10^{-7}$ three-component AND gate, $R_\rho$
passes.  $R_L$ and $R_a$ fail at `1358.436129` and `3.523301313`
tolerance multiples.  Dimensional $D_L$ remains diagnostic only.  SPOT
therefore still has no accepted rank-two fixed point.

Relative to the preceding genuine residual $o-q_8$, $R_L$ and $D_L$
increase by about `48.5081%`, while $R_a$ increases by about `349.9214%`.
This single step is unfavorable; it is not by itself a divergence proof.

## Strict solver terminals

| solve | `IEXTF` | `EEXT` | `EUNK` | `ITERF` | `EINR` |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 6 | `0` | `4.73378662e-7` | 3 | `4.52210941e-7` |
| radial plane 2 | 5 | `0` | `4.09440332e-7` | 4 | `4.29269647e-7` |
| radial plane 3 | 4 | `0` | `4.56070751e-7` | 4 | `3.45333916e-7` |
| axial | 198 | `3.86822269e-10` | `4.16258473e-7` | 1 | `4.81848190e-7` |

All strict terminals passed below `4.99999999e-7`.  The independent
`proposal-aa1` checker passed the materialized proposal carrier, fixed POD
package, live radial operator, raw radial positivity, canonical layout,
bitwise raw defects, and restart archive.  The global balance diagnostic is
`7.450874e-9`; it is separate from the fixed-point gate.  The Git-ignored
artifact contains 22 regular files, no symbolic links, and a passing 21/21
receipt.

| output | SHA-256 |
|---|---|
| returned AX | `6e7bb36ac9c123e86919bfc4655d23e4b9958a0ae6aa24e9d5815a90acc89132` |
| returned snapshots | `7c38ad7b197554c22a101664bff5367153f87496007928adaca601bc975a2649` |
| radial log | `34435b1ae067f74523f5ef1cf91bf31c31fc03ef71d8505edcc50b362503864e` |
| axial log | `75dcc570b001d9d5f24104a69c2b0a3cbbaf14787afae236cd7066d8d63a6b80` |
| independent check | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |
| receipt | `ff37eac4c32abb0bc862a7d2196afa743f9be27b4bac927b0b3a4037ad64a70c` |

## Minimum-order direction decision

AA(1) used only the consecutive genuine residuals $o-q_8$ and $p-q_9$.
Its standard unconstrained affine output direction is

$$
q_{10}=1.2246645215600993\,o-
0.22466452156009933\,p.
$$

The denominator is `9.0412608575558238e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.12764993865086841,\ 0.82141838136874701,\
0.89227926518865730).
$$

All three are strictly below one.  Independent builder and checker arithmetic
agree bitwise and confirm 8880/8880 positive reconstructed points.  The
negative coefficient is the unconstrained AA(1) result; it is not clipped or
replaced.  The final offline classification is
`AA1_DIRECTION_PASS_AA2_SKIPPED`: because AA(1) passes, AA(2) is not
calculated.

The temporary diagnostic publication hashes were
`bd0785e9f3da27b9639c3ac4c04d3bf25689c5dc7f16fc51cdcdde7306b154fb`
for AX and
`4587fcc293ba18c40c0c785e6de4991d969cc10cca8975b4b4fddf114725c209`
for snapshots.  They were deleted after verification; no durable $q_{10}$
proposal is published and no second physical map is run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
