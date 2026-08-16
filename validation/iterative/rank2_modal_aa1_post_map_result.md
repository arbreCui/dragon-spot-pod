# One strict map from the next rank-2 modal Anderson(1) proposal

Date: 2026-08-15

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
x_{\mathrm{next}}^+=G_2(x_{\mathrm{next}}),\qquad
x_{\mathrm{next}}=
0.140844300824004787x_3+
0.859155699175995213x_{\mathrm{AA1}}^+.
\]

The source tree was frozen at commit
`084d524608c71b13bd01fe693b0b6e73701a3429`. The proposal AX and snapshot
hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89` |
| proposal snapshots | `0c22cc9748beb813757d154ca592f343654e61c710f9b852ad35270ae19e186c` |

The exact `AA1-RAW-FLUX` marker identified the complete latest-returned raw
carrier; it did not replace the affine canonical proposal or any physical
equation. The unchanged host reconstructed the rank-two radial fields, used
the proposal eigenvalue in the frozen-fission source, ran three online radial
fixed-source solves, and then ran one axial solve. There was one attempt and
no retry, relaxation, damping, clipping, fitted closure or empirical
coefficient.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) terminal gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `3` | `4.04027929e-7` | `4.93129164e-7` |
| radial plane 2 | `7` | `4.70510287e-7` | `2.98444178e-7` |
| radial plane 3 | `11` | `2.93698207e-7` | `4.58326440e-7` |
| axial | `216` | `3.64225713e-7` | `4.68290153e-7` |

The axial `EEXT` was `2.94037260e-11`. The radial and axial logs report 68 s
and 137 s of CPU time, respectively, and each contains exactly one normal
Dragon termination. The terminal axial FLU eigenvalue was
`1.3624108711846150`; reciprocal canonical publication gave
\(k=1.3624109029769897\).

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.1284469617` | pass |
| \(R_L\) | `4.563675297849584e-4` | `912.7350596` | fail |
| \(R_a\) | `1.342855929959847e-6` | `2.6857118599` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, this valid map is not a fixed point at the declared tolerance. The
dimensional leakage change is

\[
D_L=6.686605047434568\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a dimensional diagnostic, not a fourth dimensionless stopping test.
The axial global/max-group balance was
`7.030714e-9 / 1.636353e-3`; per-plane radial balances were
`3.004723e-7`, `2.887718e-7` and `3.583166e-7`. None is an outer stopping
quantity. All returned flux points accepted by the independent checker were
strictly positive.

## Bounded comparison

Relative to the preceding evaluated proposal map
\(x_{\mathrm{AA1}}^+=G_2(x_{\mathrm{AA1}})\), the cross-input ratios for
\((R_\rho,R_L,D_L,R_a)\) are

\[
(0.5000000432,\ 1.0844443659,\ 1.0844425564,\ 0.8099857153).
\]

Thus \(R_\rho\) fell by about 50.0% and \(R_a\) by 19.0%, while \(R_L\) and
\(D_L\) rose by about 8.44%. The parents differ, so these are local
cross-input comparisons, not convergence factors, a contraction estimate,
a monotone trajectory or proof of Anderson superiority. Leakage remains the
dominant stopping failure.

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact proposal and
`AA1-RAW-FLUX` lifecycle. The independent post-map checker then passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`ed63c33253ba2ff42bf0e59539dd33e475293a8430b67cbc3acfc44ea03659de`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `1dbdd60232be82d02aff618fc370a16547f9aca4a0c9aa33b0a2b183c57cf857` |
| `candidate_radial.xsm` | `9fbb33511548d4357688c2f6ff6401a0f87d40aaf69702f8a4c3e645c7135fa7` |
| `candidate_axial.xsm` | `dfe9bc56a38c44799b63f5086aaecfbd24a9060d1dc45bbc6ca721d1c4c2c89d` |
| `candidate_snapshots.xsm` | `1944de57cd6c18f7b47022dc6eac80b0c6b578546d53dad4caba1347f5640bf1` |
| `radial.log` | `682cda87da6e230671ea491873387e3cc7111196749f51d9d69ce7ce7437c351` |
| `axial.log` | `d62e96570417e5946c49f02c861e88d251733ae5d8b9f1813ed76bc8ed0aaffd` |
| `parent_preflight.log` | `218081feb2a29e87d4fc76340649c7bf4864f7c44df595285185e8f1733a3da0` |
| `independent_check.log` | `852969d74c0664055c23a42ca49dbc2608c05ce18ca2e95cac46bc3cdb32bb75` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, Anderson superiority, rank
adequacy or physical accuracy. No successor map was started.
