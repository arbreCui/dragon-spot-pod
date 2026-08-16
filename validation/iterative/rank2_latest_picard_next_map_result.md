# One further direct Picard map from the latest returned state

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment used the complete latest returned state

\[
x_3=G_2(x_2)
\]

and evaluated exactly one further direct Picard map

\[
x_4=G_2(x_3).
\]

The source tree was frozen at commit
`95dd9204d1010b1583d8d4e4de530b094a80ee98`. The parent hashes were:

| parent | SHA-256 |
|---|---|
| returned AX | `154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651` |
| returned snapshots | `0cf7d0a46ac84e5d94f9ed11d834c1d854f79c89eceea83c581fb1847e9bf911` |

The parent 21-entry receipt and all six parent hashes passed before execution.
The host consumed this state directly with the same fixed rank-two basis,
normalization and physical decks. It used the parent eigenvalue in the
frozen-fission source, performed three online radial fixed-source solves and
then one axial solve. There was one attempt and no proposal, state selection,
combined norm, mixing, retry, relaxation, damping, clipping, fitted closure,
regularization, pseudoinverse, fallback or empirical coefficient.

## Strict solve terminals

Every solve met the unchanged strict \(5\times10^{-7}\) terminal contract:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `5` | `4.70068386e-7` | `2.95877783e-7` |
| radial plane 2 | `17` | `4.32903420e-7` | `2.28092873e-7` |
| radial plane 3 | `6` | `4.06825137e-7` | `1.90401380e-7` |
| axial | `216` | `3.12193379e-7` | `4.68290011e-7` |

The axial `EEXT` was `8.95125418e-10`, and its terminal FLU eigenvalue was
`1.3624109802120421`. The complete radial and axial runs report 76 s and
141 s CPU time, respectively. Each Dragon log contains exactly one normal
termination and no failure marker.

The final-source radial response-balance diagnostic was
`3.543086331261747e-7`; the separate saved-RHS lag L2/max diagnostics were
`2.040725676378107e-7 / 2.634596947503285e-7`. The three radial solve-used
source-balance diagnostics had maximum `4.897868e-7`. The axial
global/max-group balance was `6.994926e-9 / 1.635723e-3`, and the axial
Galerkin maximum diagnostic was `4.49858e-7`. These values are diagnostics,
not stopping tests; in particular, the axial max-group value is not claimed
to pass the outer tolerance.

## Raw stopping result

For the unchanged tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422346976453497e-8` | `0.1284469395` | pass |
| \(R_L\) | `4.754951362754997e-4` | `950.9902726` | fail |
| \(R_a\) | `2.901932364486617e-6` | `5.803864729` | fail |

The stopping rule is the three-component AND gate. Since \(R_L\) and
\(R_a\) fail, this map evaluation does not close the declared fixed-point
gate.
The dimensional leakage change is

\[
D_L=6.966874934732914\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. All returned raw radial
scalar-flux points checked independently were strictly positive, and the
axial balance audit reported zero nonpositive cells. `SPOSTATE` retained
`2220 = 370*3*2` coefficients, confirming the fixed rank-two state.

## Comparison with the direct parent

Relative to the \(x_2\to x_3\) map, the raw \(R_\rho\) value is unchanged,
while \(R_L\) and diagnostic \(D_L\) decreased by approximately `24.3808%`.
In contrast, \(R_a\) increased by approximately `96.3408%`.

Thus the latest direct-Picard defects are not componentwise decreasing.
Leakage improved locally while the modal defect rebounded. This one mixed
step is not evidence of convergence, divergence, a cycle, contraction,
convergence order or future behavior.

## Independent audit and receipt

The continued-state checker passed:

- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`7b07072ef9ac0ebe81cdd199e9710bbde2a09239a898aeef4d02aace3fe0c71f`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `54f8d9343d307f68154deef2d09fbf3704e44f9624efdb9cc42c3222dafd5a21` |
| `candidate_radial.xsm` | `444d4ef4ff9271b2e217af70b3c0fb5c742a9f0b51ee31fdbe6650ee1c179653` |
| `candidate_axial.xsm` | `ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08` |
| `candidate_snapshots.xsm` | `4b5deac64ec6ab50cd9c1c7a9e868f824bb2078895492eeb56c95863bd85e87a` |
| `radial.log` | `8de286d3d5f6676c7a76c78ebfae2b697e14bb58265a1c3350b936365a12867f` |
| `axial.log` | `833ed0019f4b5e4e134bec0ddd9c75406f9e50ab616a617f7d4547867457085a` |
| `parent_preflight.log` | `94771a0794f029515f88a669f7c0a6bddc99858a2ae886af95f94176dc41a232` |
| `independent_check.log` | `0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the runtime logs and
`classification.txt` record the completed result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, rank adequacy or physical
accuracy. No retry, further proposal or further map was started.

## Subsequent offline proposal

The latest two consecutive direct Picard residuals were later used to
materialize exactly one standard modal AA(1) proposal. That no-Dragon stage
does not evaluate a map or create a new stopping defect; see
[rank2_latest_modal_aa1_candidate_result.md](rank2_latest_modal_aa1_candidate_result.md).
