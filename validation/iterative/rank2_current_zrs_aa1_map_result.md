# Physical map from the latest-return standard AA(1) proposal

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

The latest two genuine consecutive residuals, $r-z$ and $s-r$, gave the
standard unregularized full-Gram AA(1) state

\[
p=0.80686776173198704\,r+0.19313223826801298\,s.
\]

The modal, leakage height-$L_2$, and dimensional leakage-direction ratios
were `0.0551069`, `0.799194`, and `0.787927`, respectively.  All three were
strictly below one, so the predeclared minimum-order rule authorized AA(1)
and did not form AA(2).  The same affine weights acted on $(a,\rho,L)$;
there was no fitted coefficient, relaxation, damping, clipping,
regularization, or empirical parameter.

Exactly one fresh physical map

\[
p^+=G_2(p)
\]

ran from source commit
`6e7b6ecc3102bf76423807bb8908107b69e06bca`.  It used the unchanged
fixed-rank-two basis, three online radial fixed-source solves, and one axial
solve.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 4 | `0` | `4.98840279e-7` | `4.56007797e-7` | 17 s |
| radial plane 2 | 13 | `0` | `4.34213831e-7` | `4.34213831e-7` | 31 s |
| radial plane 3 | 11 | `0` | `3.81057475e-7` | `3.90524519e-7` | 36 s |
| axial | 181 | `6.46774717e-11` | `4.81848417e-7` | `4.81848417e-7` | 133 s |

Every strict terminal passed below `4.99999999e-7`; the 120/180-second
limits were process-safety bounds only.  At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| $R_\rho$ | `6.422349219104007e-8` | `0.128447` | pass |
| $R_L$ | `4.896188255170843e-4` | `979.237651` | fail |
| $R_a$ | `2.660658391293558e-6` | `5.321317` | fail |

The dimensional diagnostic is

\[
D_L=7.173803169280291\times10^{-7}\ \mathrm{cm}^{-1};
\]

it is not part of the dimensionless outer gate.  Compared only as a
cross-input diagnostic with the preceding direct map $r\mapsto s$, $R_L$
and $D_L$ are 34.5364% smaller and $R_a$ is 26.9536% smaller.  Because the
two parents differ ($p$ versus $r$), these numbers are not a contraction
factor or proof of convergence.

The independent Ganlib checker passed the materialized-proposal parent,
latest raw carrier, fixed POD package, live radial-operator change, raw
radial positivity, canonical layout, bitwise raw defects, and restart
archive.  Global and maximum-group balance diagnostics were
`7.841120e-9` and `1.634965e-3`; they are not stopping defects.

The Git-ignored artifact contains 22 regular files, no symbolic links, and
a passing 21/21 receipt.

| object | SHA-256 |
|---|---|
| parent proposal AX | `d00a310cffb832cfec6ef2bdaa6cf27cfd51443904afd8d26ca57418e140d225` |
| parent proposal snapshots | `1e1ed5556c464ae319784ecab8ee408decba7392c419d45de796ab396f82d72d` |
| returned AX | `e35636e5badd21a5deb02964b995a948ea0df4eb110b7fd2783ef5c41f36145e` |
| returned snapshots | `30240ad9c99de510c04c277a40ce97b162cce2cc364f548268ad66e6570f9435` |
| receipt | `bfaa6ca03d67e912477e89164da476d4589bdc9d7e812d4b495875039c301a9a` |

This is one valid physical map, not a converged fixed point.  No retry,
fallback, AA(2), or successor map was started.
