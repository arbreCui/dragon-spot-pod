# One strict map from the latest rank-2 modal AA(1) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
z=G_2(Q(y)),\qquad
y=0.66364214132573696x_3+0.33635785867426299x_4.
\]

The source tree was frozen at commit
`cb4fbd62b7f30d7939d6cd13f3578eeb68dac7a6`. The parent hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d` |
| proposal snapshots | `b5d03cb519ce54f0ade469288f70a50e303bb6a7bd7d4396c04558d38ffd108b` |

The proposal's nine-entry receipt and all six map-parent hashes passed before
execution. `X4-RAW-FLUX` identified only the complete raw carrier; the map
input was the independently published \(Q(y)\) state. The unchanged host
reconstructed radial flux from the proposal coordinates, used its published
eigenvalue in the frozen-fission source, performed three online radial
fixed-source solves, and then one axial solve. Rank two, the fixed basis,
normalization, decks, physical equations, and tolerances were unchanged.
There was one attempt and no retry, relaxation, damping, clipping, fitted
closure, regularization, fallback, or empirical coefficient.

## Strict solve terminals

All four solves met the unchanged strict \(5\times10^{-7}\) terminal
contract:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `12` | `4.64710240e-7` | `3.96604520e-7` |
| radial plane 2 | `4` | `3.22750566e-7` | `3.82024808e-7` |
| radial plane 3 | `5` | `3.77390450e-7` | `2.57657575e-7` |
| axial | `187` | `4.81848474e-7` | `4.81848474e-7` |

The axial `EEXT` was `1.01481179e-9`. Its terminal REAL64 eigenvalue was
`1.3624110170257520`; canonical REAL32 publication gave
`1.3624110221862793`. The radial and axial logs report 68 s and 136 s CPU
time, respectively, and each contains exactly one normal Dragon termination.

The three radial solve-used balance diagnostics were `2.775923e-7`,
`3.148402e-7`, and `3.526113e-7`; the assembled radial balance was
`3.393552911480168e-7`. The axial global/max-group balance was
`7.26500e-9 / 1.63809e-3`, and its Galerkin maximum diagnostic was
`4.64920e-7`. These are diagnostics, not outer stopping quantities.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422346976453497e-8` | `0.1284469395` | pass |
| \(R_L\) | `6.535726745879074e-4` | `1307.1453492` | fail |
| \(R_a\) | `8.490508952762415e-7` | `1.6981017906` | fail |

The stopping rule is the three-component AND gate. Since \(R_L\) and
\(R_a\) fail, this valid map does not close the declared fixed-point gate.
The dimensional leakage change is

\[
D_L=9.576033335179090\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. `SPOSTATE` retained
`2220 = 370*3*2` coefficients. The axial audit found zero nonpositive cells,
and the independent checker found all returned raw radial values strictly
positive.

## Bounded comparison with the direct \(x_4\) map

Relative to the historical direct map \(x_4=G_2(x_3)\),
the recorded ratios for \((R_\rho,R_L,D_L,R_a)\) are

\[
(1.0000000000,\ 1.3745096947,\ 1.3745091486,\ 0.2925812144).
\]

Thus the modal defect falls by about `70.7419%`, but the leakage stopping
defect and its dimensional change both rise by about `37.451%`. The result is
not componentwise improved and leakage remains the dominant failure. Because
the inputs differ, these are not adjacent convergence factors, a contraction
test, or proof for or against AA(1).

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact
`PROPOSAL + X4-RAW-FLUX` lifecycle. The post-map checker then passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`9e614de527fa2c4b9dbe7ba5375ec89b1769077ba5b8c690fc9445bd96eb3b8e`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `882ed350ab0b0e999905eeac6b548b9b3c135f105487cdd101512b8641aea932` |
| `candidate_radial.xsm` | `d0013ce3eff06dce02d0d0263d393e614247b31d1ef6f3b32cf686760c919f13` |
| `candidate_axial.xsm` | `8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9` |
| `candidate_snapshots.xsm` | `01d8fe5bc2556c1efa0931f72e69b727925589a3d2ad34aeac82c362b83d8647` |
| `radial.log` | `a72905161a512b8c4be4dc24d0a9863f6cb615c6782b462022f11266f00d011c` |
| `axial.log` | `a797976cfd9b846dc2fa1e86e0725eeea99d528d421b878a25267f83d0e20851` |
| `parent_preflight.log` | `af8fb829b39cf508c21c7ac97d7c21fba76f8a8614555544b0e9ede28692e67e` |
| `independent_check.log` | `52a7f21aff57d8d0f3fb8097e98d55fce4d3c266873db2c0bc02e936f1c5dc1b` |

The artifact's receipt-locked `continuation_policy.md` remains the pre-run
authorization record and therefore says `PREPARED_NOT_RUN`; the runtime logs
and `classification.txt` record the completed result.

## Scientific boundary

This is one valid evaluation of the stated fixed-rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, AA(1) superiority, rank adequacy,
or physical accuracy. No retry, new proposal, or successor map was started.
