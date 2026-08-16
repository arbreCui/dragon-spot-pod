# One strict map from the standard rank-2 modal Anderson(2) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
x_{\mathrm{AA2}}^+=G_2(x_{\mathrm{AA2}}),
\]

where

\[
x_{\mathrm{AA2}}=
0.77664274528264354x_{\mathrm{next}}^+
-0.54521415283366947x_{\mathrm{roll}}^+
+0.76857140755102593x_{\mathrm{roll2}}^+.
\]

The source tree was frozen at commit
`cae32975000b3f7c2d0a7ea73a9fb30357c49b6e`. The proposal AX and snapshot
hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `aaa0d6afa2883f5eb528c26c466833454629160e2fd1b2f1a2e53a69168183ed` |
| proposal snapshots | `a6231acf84ed551e9144811c4bc775368c4a21132817ac757143a4c7e74d51dc` |

The exact `AA2-RAW-FLUX` marker identified the complete latest-returned raw
carrier; it did not replace the canonical AA(2) proposal or enter a physical
equation. The same fixed rank-two basis, physical decks and map operator were
used. The host reconstructed the rank-two radial fields, used the proposal
eigenvalue in the frozen-fission source, ran three online radial fixed-source
solves, and then ran one axial solve. There was one attempt and no retry,
relaxation, damping, clipping, fitted closure, regularization, pseudoinverse,
fallback or empirical coefficient.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) terminal gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `4` | `4.19929421e-7` | `3.69598666e-7` |
| radial plane 2 | `6` | `3.22750736e-7` | `3.92778873e-7` |
| radial plane 3 | `7` | `4.99698388e-7` | `3.91351790e-7` |
| axial | `223` | `4.68292598e-7` | `4.68292598e-7` |

The axial `EEXT` was `1.33132644e-10`, and its terminal FLU eigenvalue was
`1.3624108461277424`. The three radial FLU solves report 60 s total CPU time;
the axial FLU solve reports 141 s. The radial and axial Dragon logs each
contain exactly one normal termination.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422348086676521e-8` | `0.1284469617` | pass |
| \(R_L\) | `5.040897264815401e-4` | `1008.179453` | fail |
| \(R_a\) | `1.007958625290916e-6` | `2.015917251` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, this valid map is not a fixed point at the declared tolerance. The
dimensional leakage change is

\[
D_L=7.385824574157596\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. The axial global/max-group
balance was `6.918881e-9 / 1.634493e-3`; these values are also diagnostics.
All returned raw radial scalar-flux points checked independently were
strictly positive; the axial balance audit reported zero nonpositive cells.

## Bounded comparison

Relative to the preceding evaluated XRP-carrier map, \(R_\rho\) decreased by
approximately `50.0000%`, while \(R_L\), diagnostic \(D_L\) and \(R_a\)
increased by `21.3364%`, `21.3364%` and `29.6496%`, respectively. The two
maps have different parent inputs. These are finite cross-input comparisons,
not convergence factors, a contraction estimate, a monotone trajectory or
evidence of Anderson superiority. Leakage remains the dominant stopping
failure.

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact proposal and
`AA2-RAW-FLUX` lifecycle. The independent post-map checker then passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`ca55db48f6d22a1bda25447f3d5756e83c77964fece62f89a4317c1ec91f499e`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `68a523efcea192fbf3ab50a78bbd1817149f6c0c8dfc69bbadb1f7c614348285` |
| `candidate_radial.xsm` | `faf0ee9dfdded8b4a81a2e277023814d511701563301ae27d84c7d75c857d824` |
| `candidate_axial.xsm` | `ebab72eb17b6b70e79fd8b48d0903b3dc9388ca417757efa90730bd3859acc17` |
| `candidate_snapshots.xsm` | `3f71736ec3a7b490f8635e9b0dcd7c365e7be05bc4a5af21232431954ac74f21` |
| `radial.log` | `1c357f309ae6921f1fa609f0c2a295cb10dc2972c4eb3846edddd48a4a44dd06` |
| `axial.log` | `dbcd2340d60173c5d7733afa6e772135fa669384e53593f80307923c291ae019` |
| `parent_preflight.log` | `fea11130449d6da16dfa535b09eec78c77a1ed71c962bfe51d1e923c7eb2c5f0` |
| `independent_check.log` | `44833ba13613d7a928f6ad64bf603848051268cb60078aa60fe687c5b99fdfe2` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, Anderson superiority, rank
adequacy or physical accuracy. No retry or successor was started as part of
that map evaluation.

## Subsequent offline proposal

The three-map AA(2) window was later shifted forward once to include this
returned state. A separate Ganlib-only stage materialized a finite, positive
rolling AA(2) proposal without Dragon or a new map. It created no stopping
defect and prepared no map host as part of that offline stage; see
[rank2_modal_aa2_rolling_next_candidate_result.md](rank2_modal_aa2_rolling_next_candidate_result.md).
