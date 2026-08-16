# One strict map from the rolling rank-2 modal Anderson(1) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
x_{\mathrm{roll}}^+=G_2(x_{\mathrm{roll}}),\qquad
x_{\mathrm{roll}}=
0.439220581194280313x_{\mathrm{AA1}}^+
+0.560779418805719687x_{\mathrm{next}}^+.
\]

The source tree was frozen at commit
`d8c87eaf70cace3e976ac1fe10d0c60eba35512f`. The proposal AX and snapshot
hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee` |
| proposal snapshots | `6762e58a75cc2bcbffae476187389797a9aebf95e8619355060b6de9c41b5102` |

The exact `XNP-RAW-FLUX` marker identified the complete latest-returned raw
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
| radial plane 1 | `5` | `3.53521727e-7` | `3.51210161e-7` |
| radial plane 2 | `5` | `3.79300275e-7` | `3.60807888e-7` |
| radial plane 3 | `10` | `4.03508466e-7` | `3.46806786e-7` |
| axial | `234` | `3.44177010e-7` | `4.81847849e-7` |

The axial `EEXT` was `3.46162710e-10`. The radial and axial logs report 69 s
and 141 s of CPU time, respectively, and each contains exactly one normal
Dragon termination. The terminal axial FLU eigenvalue was
`1.3624109720133821`; the returned publication used
`1.3624110221862793`.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `0.000000000000000e+0` | `0` | pass |
| \(R_L\) | `3.600486262295603e-4` | `720.0972525` | fail |
| \(R_a\) | `1.453780683665123e-6` | `2.907561367` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, this valid map is not a fixed point at the declared tolerance. The
dimensional leakage change is

\[
D_L=5.275360308587551\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a dimensional diagnostic, not a fourth dimensionless stopping test.
The zero published \(R_\rho\) means that the input and output eigenvalues
occupy the same stored value `1.3624110221862793`; it is not evidence that a
continuous eigenvalue has converged exactly. The axial global/max-group
balance was `6.952170e-9 / 1.638125e-3`. Balance values are diagnostics, not
outer stopping quantities. All returned flux points accepted by the
independent checker were strictly positive.

## Bounded comparison

Relative to the preceding evaluated proposal map
\(x_{\mathrm{next}}^+=G_2(x_{\mathrm{next}})\), the cross-input ratios for
\((R_\rho,R_L,D_L,R_a)\) are

\[
(0,\ 0.7889444422,\ 0.7889445049,\ 1.0826036146).
\]

Thus the reported \(R_\rho\) fell to zero and \(R_L\) and \(D_L\) fell by
about 21.1%, while \(R_a\) rose by about 8.26%. The parents differ, so these
are local cross-input comparisons, not convergence factors, a contraction
estimate, a monotone trajectory or proof of Anderson superiority. Leakage
remains the dominant stopping failure.

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact proposal and
`XNP-RAW-FLUX` lifecycle. The independent post-map checker then passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`dc0ca93e52f45a225582ce1c9234c327e08777a1c6c9366b322daaad3b0ff4d8`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `efbaba2a5e0987c776fe4b6787993f68f088b772992376725dc725d8e0efa40a` |
| `candidate_radial.xsm` | `7af463a2b2af2e64bffacf6e89a60a6d20dd4c83e844051aa00b089eafaff9f5` |
| `candidate_axial.xsm` | `dbb333c8cd1a00a24de40d7b8685349fb83f63a7f0d92c0d2d225c8a25bc07a2` |
| `candidate_snapshots.xsm` | `ca57bdfb2f950aa24cf5a42edf9fe59883ccfa9221388fbc6aee8b76c94480fc` |
| `radial.log` | `f8585ab4885e5c2f75ccfac5d560ec030ad7166335103d3aac99a47b78a09ee8` |
| `axial.log` | `7c772befe574e42321c1931ac6cf528269887a708a668b6f36825dd8734231ae` |
| `parent_preflight.log` | `232c6cd6cfe43638461fcfbdfd3562936451640c37bfd533a199c277e98fee9a` |
| `independent_check.log` | `a690b1d208a3e7a67da84378e727ce52bb4804a4db7cc92c844e4d64ee8cfedf` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, Anderson superiority, rank
adequacy or physical accuracy. No retry, successor proposal or successor map
was started.
