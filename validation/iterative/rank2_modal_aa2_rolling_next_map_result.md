# One strict map from the shifted rolling rank-2 modal Anderson(2) proposal

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
x_{\mathrm{rAA2}}^+=G_2(x_{\mathrm{rAA2}}),
\]

where

\[
x_{\mathrm{rAA2}}=
-1.2827949098497831x_{\mathrm{roll}}^+
+0.23700413908563411x_{\mathrm{roll2}}^+
+2.0457907707641487x_{\mathrm{AA2}}^+.
\]

The source tree was frozen at commit
`d82976182ccac80eade6e17926fb259b31adc833`. The proposal AX and snapshot
hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `ce9544e8f58b01d933f5937d781a0f1b70a58862468bbd380d5d2bc5c0e07715` |
| proposal snapshots | `61604c1dfb586abe71115544aa73b4628f7528f5da32f6bce14ce8f7f8f30763` |

The method-level `AA2-RAW-FLUX` marker identified the complete latest-returned
\(x_{\mathrm{AA2}}^+\) carrier; the shifted generation was bound by the
manifest and hashes. The same fixed rank-two basis, physical decks and map
definition were used. The host reconstructed the proposal radial fields,
used its published eigenvalue in the frozen-fission source, ran three online
radial fixed-source solves and then one axial solve. There was one attempt and
no retry, relaxation, damping, clipping, fitted closure, regularization,
pseudoinverse, fallback or empirical coefficient.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) terminal gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `4` | `4.30529269e-7` | `2.04730142e-7` |
| radial plane 2 | `3` | `4.98394854e-7` | `2.43551085e-7` |
| radial plane 3 | `4` | `3.96986934e-7` | `3.36040387e-7` |
| axial | `199` | `4.47429045e-7` | `4.47429045e-7` |

The axial `EEXT` was `3.92051891e-10`, and its terminal FLU eigenvalue was
`1.3624110572789168`. The three radial FLU solves report 54 s total CPU time;
the complete axial run reports 138 s total CPU time. The radial and axial
Dragon logs each contain exactly one normal termination.

The final-source radial response balance was `3.0903451e-7`. A plane-3
balance diagnostic evaluated with the saved work RHS was `8.76419e-7`; the
separate saved-RHS lag L2/max diagnostics were
`2.7242694e-7 / 2.6345959e-7`. The axial Galerkin maximum diagnostic was
`5.11295e-7`. These are not predeclared stopping tests; they do not replace
the strict solve terminals or the raw outer gate.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `1.284469730578053e-7` | `0.2568939461` | pass |
| \(R_L\) | `1.170144756375341e-3` | `2340.289513` | fail |
| \(R_a\) | `1.799470745437237e-6` | `3.598941491` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, this valid map is not a fixed point at the declared tolerance. The
dimensional leakage change is

\[
D_L=1.714477548375726\times10^{-6}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. The axial global/max-group
balance was `7.767588e-9 / 1.636559e-3`; these values are also diagnostics.
All returned raw radial scalar-flux points checked independently were
strictly positive, and the axial balance audit reported zero nonpositive
cells.

## Bounded comparison

Relative to the preceding evaluated \(x_{\mathrm{AA2}}\) map, \(R_\rho\),
\(R_L\), diagnostic \(D_L\) and \(R_a\) increased by approximately
`100.0000%`, `132.1303%`, `132.1308%` and `78.5263%`, respectively. The two
maps have different parent inputs. These are finite cross-input comparisons,
not convergence factors, a contraction estimate, a monotone trajectory or
evidence that Anderson(2) is generally superior or inferior. Leakage remains
the dominant stopping failure.

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
`6f45b34ecc6720329f64417a627139d5504fcff0664ec7c3a8eb50f162fd34f5`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `c3777b2bdb2c3ec4ce582b8e42351cbb14e1884b2c82c4cc8d7799809b74b442` |
| `candidate_radial.xsm` | `cfb1022ec3f741e95179a99d8cfde72059eb62136534d4092ab39308d35ea467` |
| `candidate_axial.xsm` | `21e5f4e8660020aee9509a656993c45049deb9a01029d86e63801432c948ab67` |
| `candidate_snapshots.xsm` | `9c69da5c78d0c6a4a2b99eba54b23e9ce9869df5f142c2ed86c40859ba1176a8` |
| `radial.log` | `8d86b440e1f57132f70d0c7a400224c7e63bc6f5fad411f416fcaf26afe5ecd9` |
| `axial.log` | `c0c5ab8d79f62459038874746903429d6b959835dc3d638cd2345cb06a57b79c` |
| `parent_preflight.log` | `fea11130449d6da16dfa535b09eec78c77a1ed71c962bfe51d1e923c7eb2c5f0` |
| `independent_check.log` | `44833ba13613d7a928f6ad64bf603848051268cb60078aa60fe687c5b99fdfe2` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, Anderson superiority or
inferiority, rank adequacy or physical accuracy. No retry, successor proposal
or successor map was started.
