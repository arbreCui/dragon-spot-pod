# One direct Picard map after the latest evaluated proposal

Date: 2026-08-15

Classification: `VALID_NOT_MET`.

## Frozen experiment

The experiment evaluated exactly one unchanged fixed-rank map

\[
x_{n+1}=G_2(x_n),
\]

where \(x_n\) was the valid returned state from the completed
\(u_{\rm pub}\to G_2(u_{\rm pub})\) experiment. The source tree was frozen at
commit `d787e3f445db0e4f32d79d2a97cc9e705953ebfd`; the archived inputs and host
files match that commit bit for bit. The parent AX and snapshot hashes were
`046a4ff0cd5bd87af59688ba6a01d5de6155e9a71da82d3c97c57ac17abb3bba`
and `c3204649054ff3e4ca8d110031ebf37b4144bd62bd4e81e3b166ae4bb9c6bd57`.

The map used the unchanged fixed rank-two POD package, three online radial
fixed-source solves and one axial solve. There was one attempt and no retry,
re-encoding, AA update, relaxation, damping, clipping, fitted closure or
empirical coefficient. The generic host used its `continued` lifecycle; a
proposal-carrier preflight was therefore not applicable.

## Strict solve terminals

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `13` | `4.60425156e-7` | `3.40188052e-7` |
| radial plane 2 | `5` | `3.60135090e-7` | `2.42800155e-7` |
| radial plane 3 | `7` | `4.94167807e-7` | `2.13177756e-7` |
| axial | `216` | `4.16247246e-7` | `4.81833467e-7` |

The axial `EEXT` was `3.10549086e-10`. The radial and axial logs report 75 s
and 137 s of CPU time and each contains exactly one normal Dragon end. The
terminal REAL64 eigenvalue was `1.3624105119192029`; canonical REAL32
publication gave \(k=1.3624105453491211\).

## Raw stopping result

For \(\varepsilon=5\times10^{-7}\):

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422346406909085e-7` | `1.2844692814` | fail |
| \(R_L\) | `5.217515597326579e-4` | `1043.5031195` | fail |
| \(R_a\) | `7.246330000318798e-6` | `14.4926600` | fail |

All three stopping defects exceed the tolerance. The dimensional diagnostic
is

\[
D_L=7.644703146070242\times10^{-7}\ \mathrm{cm}^{-1};
\]

it is not compared with the dimensionless tolerance.

Relative to the immediately preceding valid map, the new/old ratios for
\((R_\rho,R_L,D_L,R_a)\) are

\[
(0.7692305673,\ 1.2915232570,\ 1.2915232570,\ 0.5054747839).
\]

Thus \(R_\rho\) and \(R_a\) decreased by about 23.1% and 49.5%, while
\(R_L\) and \(D_L\) increased by about 29.2%. This adjacent step is not
componentwise monotone; leakage remains the dominant stopping defect.

The global/max-group balance diagnostics were
`7.206137e-9 / 1.637805e-3`. The per-plane radial balances were
`2.947157e-7`, `3.989469e-7` and `2.927806e-7`; the assembled radial balance
was `4.192101953536255e-7`. None is an outer stopping quantity.

## Independent audit and receipt

The independent Ganlib-only checker passed the fixed POD package, live radial
operator, raw radial positivity, canonical layout, bitwise raw-defect
recomputation and restart archive checks. The Git-ignored artifact contains
22 regular files and no symbolic links. Its 21-entry receipt passes 21/21;
the receipt-file SHA-256 is
`1cbaa2dd31d568839b911984ab2961bd240da5b8f45854ff2a743d043ea8778e`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `66c7f4c9cf4106c6f4bb3a222b78c53069020628f002e29b606e35439d27ad20` |
| `candidate_radial.xsm` | `b20aa1bcfae10f5b96f856c835c98c1167cdb8bd2dbe7bdd272fd10a08d106ba` |
| `candidate_axial.xsm` | `8db8a8d3c1d9c3c0085b2e106f8a5bbbab3899bbccfbfa073fa801c6d33d67b5` |
| `candidate_snapshots.xsm` | `422143f0402ed47ce7f94bf61b6de020ad04668f1364a84811ba13b37e4b35a7` |

## Scientific boundary

This is one valid map of the fixed rank-two discrete model, but it does not
meet the stopping rule. The mixed component trend does not establish
convergence, divergence, stability, contraction, rank adequacy or physical
accuracy. No successor map was started.
