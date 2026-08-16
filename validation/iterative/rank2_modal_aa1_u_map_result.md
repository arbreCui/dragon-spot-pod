# One strict map from the latest rank-2 modal AA(1) proposal

Date: 2026-08-15

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one map

\[
u^+=G_2(u_{\rm pub})
\]

from the hash-locked `V-RAW-FLUX` proposal. The run used source commit
`3fa413806d8552bc3429bd50876ca199c3393f6f`, the unchanged fixed rank-two POD
package, three online radial fixed-source solves and one axial solve. There
was one attempt and no retry, re-encoding, relaxation, damping, clipping,
fitted closure or empirical coefficient.

The parent manifest locked the proposal to:

| Parent | SHA-256 |
|---|---|
| AX | `77a4bc3916db21064dc2bae73a0397faeb15fb8033de6f761fcaa4cfd0f6852b` |
| snapshots | `2f526c84f4ef42afd51178dde9481ff7336c0de5b0ff486135635a0b7fc79a81` |

The pre-Dragon check accepted the exact proposal lifecycle and
`V-RAW-FLUX` carrier. Carrier provenance did not replace the online radial
solves.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) inner/outer gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `6` | `4.04196982e-7` | `2.99950642e-7` |
| radial plane 2 | `4` | `3.46971518e-7` | `4.03701222e-7` |
| radial plane 3 | `12` | `3.57200008e-7` | `2.65386575e-7` |
| axial | `187` | `4.81873997e-7` | `4.81873997e-7` |

The axial `EEXT` was `1.03107738e-10`. The logged radial and axial CPU times
were 69 s and 132 s. Each log contains exactly one normal Dragon termination.

The terminal eigenvalue was `1.3624117256367803`; canonical REAL32
publication produced \(k=1.3624117374420166\). The input proposal had
\(k=1.3624101877212524\).

## Raw stopping result

The outer tolerance is

\[
\varepsilon=5\times10^{-7}.
\]

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `8.349052520451039e-7` | `1.669810504` | fail |
| \(R_L\) | `4.039815442129971e-4` | `807.9630884` | fail |
| \(R_a\) | `1.433569038774645e-5` | `28.67138078` | fail |

All three required stopping defects exceed the tolerance, so the only valid
classification is `VALID_NOT_MET`.

The dimensional leakage change is

\[
D_L=5.919137038290501\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic with units and is not compared with the dimensionless
outer tolerance. Other diagnostics are:

- axial global/max-group balance: `7.239895e-9 / 1.637827e-3`;
- per-plane radial balance: `2.756445e-7`, `3.539942e-7`, `7.481286e-7`;
- assembled radial balance: `3.528403436347851e-7`.

The third per-plane balance exceeds `5e-7`, but balance is not a declared
solve terminal or outer acceptance quantity.

Relative to the preceding map \(v=G_2(w_{\rm pub})\), the local new/old ratios
for \((R_\rho,R_L,D_L,R_a)\) are

\[
(1.000000874982,\ 0.4658066148,\ 0.4657628361,\ 0.3227555221).
\]

Thus \(R_L\), \(D_L\) and \(R_a\) decreased locally, while \(R_\rho\) increased
very slightly. These are observed adjacent-map ratios, not an asymptotic
convergence factor or proof of AA(1) superiority.

## Independent audit and receipt

The Ganlib-only checker independently passed:

- exact V-carrier proposal input;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of the four archived defect fields;
- restart snapshot lifecycle.

The local Git-ignored artifact receipt contains 21 unique entries and passes
21/21. Its receipt-file SHA-256 is
`db2ec0b70b192019036c1b940c51f097a7f602c2a4cdf538c601282a16239d53`.
The principal output hashes are:

| Output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `7298756f6d7ea0eb985cb5a9bda44d17a450d1ac50593ba8448f8337b578e5ba` |
| `candidate_radial.xsm` | `946981f23bdc67d198ed81d640a41e79496cce445ad9990de9d50b4d7fe1b72b` |
| `candidate_axial.xsm` | `046a4ff0cd5bd87af59688ba6a01d5de6155e9a71da82d3c97c57ac17abb3bba` |
| `candidate_snapshots.xsm` | `c3204649054ff3e4ca8d110031ebf37b4144bd62bd4e81e3b166ae4bb9c6bd57` |

The receipt also freezes both logs, parent preflight, independent checker,
manifest, policy, physical decks, host, bounded runner, Dragon and Ganlib
hashes, configuration and classification.

## Scientific boundary

This is one valid map of the stated fixed rank-two discrete model. It does not
meet the stopping rule. It does not establish asymptotic convergence,
stability, convergence order, AA(1) superiority, rank adequacy or physical
accuracy. The earlier offline `0.882410` screen is not this map residual.

No subsequent map was started or authorized by this result.
