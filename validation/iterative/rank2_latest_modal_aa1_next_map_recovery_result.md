# One strict recovery map from the latest modal AA(1) history proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized recovery evaluated exactly once the unchanged
fixed-rank map

\[
Q(t)^+=G_2(Q(t)),\qquad
t=0.223333969605448268x_4+0.776666030394551732z.
\]

The source tree and remote branch were frozen at commit
`2da48acefe9bb9cd313b785580eed9e2a3b9e3d2`. The proposal hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c` |
| proposal snapshots | `8414fb2298bcd9797f5d1b0613d985413c7c87d533feb80e8f24360471c05b38` |

The nine-entry proposal receipt, the frozen ten-entry receipt and
classification of the earlier invalid attempt, and all six parent hashes
passed before execution. The earlier attempt remains
`INVALID_MAP / TIMEOUT_BEFORE_TERMINAL / Scientific result NONE`.

This run started again from the hash-locked proposal and reused none of the
failed attempt's radial staging. It performed three online radial
fixed-source solves and one axial solve. Rank two, fixed basis,
normalization, physical decks, equations, strict solver tolerances, AA(1)
coefficient, and stopping gate were unchanged. The sole operational change
was the external axial process-safety cap from 80 to 420 seconds; the radial
cap remained 120 seconds. There was one activation and no retry, relaxation,
damping, clipping, fitted closure, regularization, fallback, or empirical
coefficient.

## Strict solve terminals

All four solves met the unchanged strict \(5\times10^{-7}\) terminal
contract:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `4` | `2.02972799e-7` | `2.21422908e-7` |
| radial plane 2 | `21` | `4.03853818e-7` | `3.11236846e-7` |
| radial plane 3 | `6` | `3.91597467e-7` | `3.45966384e-7` |
| axial | `235` | `4.81847849e-7` | `4.81847849e-7` |

The axial `EEXT` was `3.46332879e-10`. Its terminal REAL64 eigenvalue was
`1.3624109015697181`; the returned canonical publication recorded
`1.3624109029769897`. The radial and axial logs report 87 and 145 seconds of
CPU time, respectively, and each contains exactly one normal Dragon end.

The assembled radial balance diagnostic was
`3.916631779407657e-7`. The axial global/max-group balance was
`7.35638e-9 / 1.63422e-3`, and its Galerkin maximum diagnostic was
`4.80130e-7`. These are diagnostics, not outer stopping quantities.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.128447` | pass |
| \(R_L\) | `4.434556239270658e-4` | `886.911` | fail |
| \(R_a\) | `3.704123514999033e-6` | `7.40825` | fail |

The stopping rule is the three-component AND gate. Because \(R_L\) and
\(R_a\) fail, this valid map does not meet the declared convergence target.
The dimensional leakage change is

\[
D_L=6.497430149465799\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. `SPOSTATE` retained
`2220 = 370*3*2` coefficients. The axial audit found zero nonpositive flux
cells, and the independent checker accepted the returned raw radial
positivity and bitwise raw defects.

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact
`PROPOSAL + Z-RAW-FLUX` lifecycle. The post-map checker passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`50898b375ffd92d7ad2355cf9ed6cc7b72e0f0c5c9318da78b011ad06b0cf3d3`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `86fe5aa3b73246eaa4dbbb212b8dc32009999be6a726ebdbf97a387fbc60ce4b` |
| `candidate_radial.xsm` | `7e96218bdb0d5eeda539102d2a3cd4885122e2a247035ae6c5c6fc5bb8b08e0e` |
| `candidate_axial.xsm` | `d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744` |
| `candidate_snapshots.xsm` | `7d8763c2e3da9082393aee35b79820173f72dc062f75a2a3dd07e5d305d1367c` |
| `radial.log` | `832fefe1a8374be8b0c2cb0cb13b0345cc3faa83f612625ccad02465be724476` |
| `axial.log` | `c1ef888a7100a8852ebb00c59a7e2b4023b0e28bb8af432caf24f14aed468a2c` |
| `parent_preflight.log` | `818d15e93955911638ae2deda01f54f3731b9fde57c1141a5d962ea79af516c9` |
| `independent_check.log` | `d866a4937a819c3ea9215d8d326794de3d2a9f9ccea48ebb7d2dd14830561cb9` |

The artifact's receipt-locked `continuation_policy.md` remains the frozen
pre-run authorization and therefore says `PREPARED_NOT_RUN`; the runtime
logs and `classification.txt` record the completed result. A post-exit
process census found no SPOT/Dragon process.

## Scientific boundary

This is one valid evaluation of the stated fixed-rank-two discrete map. It
does not satisfy the stopping rule and does not establish asymptotic
convergence, divergence, stability, contraction, convergence order, AA(1)
superiority, rank adequacy, or physical accuracy. No retry, new proposal, or
successor map was started.
