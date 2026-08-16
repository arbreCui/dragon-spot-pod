# One strict map from the second rolling rank-2 modal Anderson(1) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
x_{\mathrm{roll2}}^+=G_2(x_{\mathrm{roll2}}),\qquad
x_{\mathrm{roll2}}=
0.79412955189905154x_{\mathrm{next}}^+
+0.20587044810094848x_{\mathrm{roll}}^+.
\]

The source tree was frozen at commit
`0f31132a29e4fd5266abfbe5d9647920af16f637`. The proposal AX and snapshot
hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394` |
| proposal snapshots | `c27fee3d0d396c4427a7389c123b044a8ec61e274a6348b9f83343fb167313ee` |

The exact `XRP-RAW-FLUX` marker identified the complete latest-returned raw
carrier; it did not replace the affine canonical proposal or enter any
physical equation. The same fixed rank-two basis, physical decks and map
operator were used. The host reconstructed the rank-two radial fields, used
the proposal eigenvalue in the frozen-fission source, ran three online radial
fixed-source solves, and then ran one axial solve. There was one attempt and
no retry, relaxation, damping, clipping, fitted closure, regularization or
empirical coefficient.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) terminal gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `4` | `2.67670856e-7` | `2.65373615e-7` |
| radial plane 2 | `4` | `3.52882466e-7` | `3.67945631e-7` |
| radial plane 3 | `6` | `4.89451907e-7` | `4.06649008e-7` |
| axial | `217` | `4.81848531e-7` | `4.81848531e-7` |

The axial `EEXT` was `6.53556653e-10`, and its terminal FLU eigenvalue was
`1.3624111283549061`. The radial and axial logs report 57 s and 140 s of CPU
time, respectively, and each contains exactly one normal Dragon termination.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `1.284469506313002e-7` | `0.2568939013` | pass |
| \(R_L\) | `4.154479333198419e-4` | `830.8958666` | fail |
| \(R_a\) | `7.774480661208137e-7` | `1.554896132` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, this valid map is not a fixed point at the declared tolerance. The
dimensional leakage change is

\[
D_L=6.087066140025854\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. The axial global/max-group
balance was `7.266193e-9 / 1.634166e-3`; these values are also diagnostics.
All returned flux points accepted by the independent checker were strictly
positive.

## Bounded comparison

Relative to the preceding evaluated rolling-proposal map, \(R_L\) and
diagnostic \(D_L\) increased by `15.3866181%` and `15.3867373%`, respectively.
\(R_a\) decreased by `46.5223280%`, but still failed. The preceding published
\(R_\rho\) was zero, so no finite ratio is defined; the present value remains
below tolerance.

The two maps have different parent inputs. These are finite cross-input
comparisons, not convergence factors, a contraction estimate, a monotone
trajectory or evidence of Anderson superiority. Leakage remains the dominant
stopping failure.

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact proposal and
`XRP-RAW-FLUX` lifecycle. The independent post-map checker then passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

Two independent read-only audits agreed with the runtime classification and
found no empirical or altered-physics path. The local Git-ignored artifact
contains 22 regular files and no symbolic links. Its 21-entry receipt passes
21/21. The receipt-file SHA-256 is
`e0ff82971de6a896b59f56d820b54580ac556803dc1c554d05092cb040feb24f`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `1d6a7680acfcbd4d493dc9576a239aadd78d5384027006a87699049f1a038e44` |
| `candidate_radial.xsm` | `166c713caa19fa6efa68ceea01fb5c85910794253ccf21faf8320dfdae89f331` |
| `candidate_axial.xsm` | `e95e2a7577d82d9c9b8a28f938a121a4c8409e68764a8cdec9910fb3c1c6d70b` |
| `candidate_snapshots.xsm` | `bf08f193d745e1bbf66fc200f5fd8041b3b8eb37d1aa0e6b33757ca60f59eeb4` |
| `radial.log` | `2ff67afb24cd1ea45e02c09556d9d31ce24172b619b0c5259605f16b528f43f5` |
| `axial.log` | `670e906ffbe7e5e79c50de4bbca1636b501aab4f113f5d5caef4f035962b301d` |
| `parent_preflight.log` | `27c3cd655174f311fe8063eecdc6f1b529392b1ab275983da11eefd3955d4928` |
| `independent_check.log` | `a36ca2dba7767d990689581a795e3e99e63082cfd449110e278a7d61b3e2c34c` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, Anderson superiority, rank
adequacy or physical accuracy. No retry or successor map was started as part
of that evaluation.

## Subsequent offline proposal

The latest three valid fixed-rank maps, including this one, were later used
once to materialize a standard AA(2) proposal. That separate no-Dragon stage
is `MATERIALIZED_PROPOSAL_NOT_EVALUATED`; it created no stopping defect and
prepared no map host. See
[rank2_modal_aa2_candidate_result.md](rank2_modal_aa2_candidate_result.md).
