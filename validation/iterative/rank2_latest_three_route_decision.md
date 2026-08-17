# Latest three-pair route decision

Date: 2026-08-16

Classification: `OFFLINE_ROUTE_DECISION_COMPLETE_NO_MAP`.

## 1. Standard AA(2) audit

The read-only audit used exactly the three latest evaluated rank-two pairs

\[
w\mapsto x,\qquad c\mapsto d,\qquad y\mapsto e.
\]

Writing their modal map residuals as

\[
f_0=x-w,\qquad f_1=d-c,\qquad f_2=e-y,
\]

the unchanged full-Gram AA(2) calculation sets

\[
d_0=f_0-f_2,\qquad d_1=f_1-f_2
\]

and solves the standard two-by-two affine least-squares system. Its matrix is

\[
H=
\begin{bmatrix}
1.0183169132013186\times10^{-12} &
1.9786790949047020\times10^{-12}\\
1.9786790949047020\times10^{-12} &
4.1054736047172805\times10^{-12}
\end{bmatrix},
\]

with

\[
\det H=2.6550224777230087\times10^{-25}>0.
\]

No determinant cutoff, regularization, pseudoinverse or lower-depth fallback
was used. The unique standard solution on the returned states is

\[
q_{\mathrm{AA2}}=
0.72283238162036112x
-0.23768716180315402d
+0.51485478018279296e.
\]

The weights sum to one. The negative weight is part of the unmodified AA(2)
solution; it was not clipped.

| diagnostic | value |
|---|---:|
| current modal residual norm | `3.0707061399219778e-7` |
| predicted AA(2) modal residual norm | `1.0100284493210273e-7` |
| predicted modal/current | `0.32892383813277903` |
| same-weight leakage height-L2/current | `0.17379554457385943` |
| same-weight \(D_L\)/current | `0.20629174352109161` |
| affine \(\rho\) | `0.73399290329254729` |
| reciprocal published \(\rho\) | `0.73399288739993207` |
| minimum published \(B_2A\) | `1.7534015053758301e-15` |
| positive publication points | `8880 / 8880` |

An independent scratch-only checker reproduced the standard system,
fixed-rank-two publication, latest-returned carrier and snapshot lifecycle.
It found no solver symbols. This preflight ran no Dragon and created no
versioned proposal.

## 2. Predeclared route decision

Before the calculation, this bounded study required the AA(2) solution to be
unique, finite, all-convex and publication-positive before authorizing a real
map. The solution passes every item except all-convexity because
`alpha_d=-0.23768716180315402`.

This does **not** show that standard AA(2) is mathematically or physically
invalid. Convexity is the frozen authorization boundary for this one study,
not a new convergence criterion. Changing that boundary after seeing the
weights would be a post-hoc decision. Clipping the negative weight would no
longer be the standard parameter-free AA(2) method. Therefore this route is
not materialized and no real map is authorized here.

The latest sequential AA(1) comparison is finite, convex and positive:

\[
q_{\mathrm{AA1}}=
0.11069001957465097d+0.88930998042534903e.
\]

Its predicted modal/current ratio is `0.68303570010539882`; its leakage
height-L2/current and \(D_L\)/current screens are `0.94096614044404392` and
`0.92918404976424229`. These are only small local leakage reductions while
the current real-map \(R_L\) is 2570.36 times the stopping tolerance. It is
not substituted as an unannounced fallback. A direct continuation is also
not selected: the latest real leakage defect increased by about 60.27%
relative to the preceding map, so it has no current leakage-contraction
evidence.

## 3. Frozen no-map boundary

This three-step batch ends at the route decision. It changes no SPOD
equation, basis, rank, inner tolerance, physical map or outer stopping gate.
It adds no empirical coefficient, damping, relaxation, clipping or fitted
closure. It starts no radial solve, axial solve, Dragon process, retry or
successor map.

The result is not convergence. It is a negative but decisive selection
result: none of the audited routes is authorized by the conditions frozen
for this batch. Filling the remaining branch with a trial map would be
post-hoc experimentation rather than the promised three-step test.

The seconds-scale \`make spot-fast\` gate passed. A process census found no
Dragon or Donjon process, and no route-specific AA(2) candidate or map
artifact exists.

## Frozen provenance

| role | SHA-256 |
|---|---|
| \(w\) | `defdee0cf442470eb623ebb83c8bed59b8c20308121951ef0c72073ddba3c243` |
| \(x\) | `b693b310ae8f499a869254cee77b1b787f9fa66813c24321dbfe5b00994c7196` |
| \(c\) | `31579eccb0d6668c21c02add7d9dea9d64752fa9f32e20409ca22e3a53bf3255` |
| \(d\) | `4e1d50a42353a8d76e3796539746225de6f62857045275847b5049f28e542a48` |
| \(y\) | `fded732054da400dc6000b492287e29f7ae88fa2e8c62f80c7dda972940af2d1` |
| \(e\) | `96cb06444bfca395b1765b907944aa2d32c4e877af41dbd58dee258b49025e45` |
| latest returned snapshots | `608b4ae084d7c5fdebbe3eaad30e82a453cd81fca160419eed4a7e73be288c91` |
| fixed rank-two basis | `2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8` |
