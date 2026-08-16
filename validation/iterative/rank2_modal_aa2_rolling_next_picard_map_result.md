# One direct Picard successor after the rolling AA(2) map

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment used the latest valid returned state

\[
y=x_{\mathrm{rAA2}}^+=G_2(x_{\mathrm{rAA2}})
\]

and evaluated exactly one direct Picard successor

\[
z=G_2(y).
\]

The source tree was frozen at commit
`a1ded8544b9cccb5dee5337959ee0c3dc8421c31`. The returned parent hashes were:

| parent | SHA-256 |
|---|---|
| returned AX | `21e5f4e8660020aee9509a656993c45049deb9a01029d86e63801432c948ab67` |
| returned snapshots | `9c69da5c78d0c6a4a2b99eba54b23e9ce9869df5f142c2ed86c40859ba1176a8` |

The preceding 21-entry map receipt and all six manifest hashes passed before
execution. The host consumed the returned state directly with the same fixed
rank-two basis, physical decks and map definition. It used the parent
eigenvalue in the frozen-fission source, ran three online radial fixed-source
solves and then one axial solve. There was one attempt and no state selection,
combined norm, Anderson mixing, retry, relaxation, damping, clipping, fitted
closure, regularization, pseudoinverse, fallback or empirical coefficient.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) terminal gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `5` | `4.83331405e-7` | `3.44121133e-7` |
| radial plane 2 | `16` | `4.99307760e-7` | `2.39105503e-7` |
| radial plane 3 | `6` | `3.95413451e-7` | `3.79584947e-7` |
| axial | `187` | `4.81849042e-7` | `4.81849042e-7` |

The axial `EEXT` was `1.11873941e-10`, and its terminal FLU eigenvalue was
`1.3624111400400993`. The complete radial and axial runs report 79 s and
137 s total CPU time, respectively. Their Dragon logs each contain exactly
one normal termination.

The final-source radial response balance was `4.7186226e-7`. A plane-3
balance diagnostic evaluated with the saved work RHS was `5.44248e-7`; the
separate saved-RHS lag L2/max diagnostics were
`2.4727947e-7 / 3.2932453e-7`. The axial Galerkin maximum diagnostic was
`4.84116e-7`. These are not predeclared stopping tests; they do not replace
the strict solve terminals or the raw outer gate.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `6.422346976453497e-8` | `0.1284469395` | pass |
| \(R_L\) | `6.288020914939620e-4` | `1257.604183` | fail |
| \(R_a\) | `1.478007624392311e-6` | `2.956015249` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, this valid map is not a fixed point at the declared tolerance. The
dimensional leakage change is

\[
D_L=9.213108569383621\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic, not a fourth stopping test. The axial global/max-group
balance was `7.306328e-9 / 1.635003e-3`; these values are also diagnostics.
All returned raw radial scalar-flux points checked independently were
strictly positive, and the axial balance audit reported zero nonpositive
cells.

## Bounded comparison

Relative to its direct parent map, \(R_\rho\), \(R_L\), diagnostic \(D_L\)
and \(R_a\) decreased by approximately `50.0000%`, `46.2629%`, `46.2629%`
and `17.8643%`, respectively. This is one componentwise local improvement,
not a convergence factor, contraction estimate, monotone trajectory or
convergence-order measurement. An earlier different-parent map still has
smaller values in all three stopping components, so this result is not a
global best-state claim. Leakage remains the dominant stopping failure.

## Independent audit and receipt

The post-map continued-state checker passed:

- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of all four recorded defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`3a1c7de4181fb7aab5f749a89a49e4bc184ca75993be4a05e3e32da5627d6bf2`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `de86ae12fd20379fd78318f1961540bf297a87d17784ca22d67fb61d10e4b047` |
| `candidate_radial.xsm` | `d705bdcf41e7b97abd0e657fd7cfc837714559227165639ca54acdf9e186146a` |
| `candidate_axial.xsm` | `154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651` |
| `candidate_snapshots.xsm` | `0cf7d0a46ac84e5d94f9ed11d834c1d854f79c89eceea83c581fb1847e9bf911` |
| `radial.log` | `17b19775d235cec5ca965deb15efa3ffb75ec1b9d1ce257da8cae831f14ee26d` |
| `axial.log` | `beb82de5bab922cbc39d4ecc9f93fdea6a8ba5add1dec24979def0e4693a9b58` |
| `parent_preflight.log` | `94771a0794f029515f88a669f7c0a6bddc99858a2ae886af95f94176dc41a232` |
| `independent_check.log` | `0db7dac519f882a1d6102ba00adf8fd102dc00c68aaea346c9dd8067e8715f02` |

The artifact's `continuation_policy.md` is the receipt-locked pre-run policy
and therefore still says `PREPARED_NOT_RUN`; the logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, rank adequacy or physical
accuracy. No retry, further successor proposal or further successor map was
started.
