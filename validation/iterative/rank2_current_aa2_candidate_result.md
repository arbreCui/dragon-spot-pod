# Current-window standard AA(2) proposal

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The candidate uses exactly the three evaluated fixed-rank-two pairs

\[
w\mapsto x,\qquad c\mapsto d,\qquad y\mapsto e.
\]

The existing full-Gram standard AA(2) system gives

\[
q_{\mathrm{AA2}}=
0.72283238162036112x
-0.23768716180315402d
+0.51485478018279296e.
\]

The weights sum to one. The negative weight is the unmodified affine
least-squares result: it was not clipped, damped, relaxed or fitted.

| quantity | value |
|---|---:|
| \(H_{00}\) | `1.0183169132013186e-12` |
| \(H_{01}\) | `1.9786790949047020e-12` |
| \(H_{11}\) | `4.1054736047172805e-12` |
| \(\det H\) | `2.6550224777230087e-25` |
| predicted modal residual square | `1.0201574684378390e-14` |
| affine \(\rho\) | `0.73399290329254729` |
| published \(k\) | `1.3624110221862793` |
| reciprocal published \(\rho\) | `0.73399288739993207` |
| maximum leakage publication round trip | `5.7475969730130805e-11` |
| minimum published \(B_2A\) | `1.7534015053758301e-15` |
| strictly positive publication points | `8880 / 8880` |

Only the canonical state \((A,\rho,L)\) was combined. The complete raw AX
and snapshot payload comes from the latest returned state \(e\) and is
marked `PROPOSAL + AA2-RAW-FLUX`; raw fluxes were not mixed.

The independently compiled checker recomputed the two-by-two system and
verified the fixed rank-two bundle, publication bit patterns, latest
raw-flux carrier, \(y\mapsto e\) snapshot lifecycle, stale-record removal
and all-point positivity. Builder and checker symbol audits found no Dragon,
ASM, FLU or transport dependency.

The local Git-ignored artifact contains ten regular files, no symbolic
links and a passing 9/9 payload receipt.

| output | SHA-256 |
|---|---|
| proposal AX | `dc2251e13fa473ceebee7839c32bd5b3244498134a8acfab93b39c55b1e79469` |
| proposal snapshots | `87ed9359809608c838991d2743914a47d96741fc94cedc07d06d512735970b63` |

This stage ran no physical map and produced no stopping defect. Positivity
and the favorable offline residual screens establish arithmetic eligibility,
not convergence. Exactly one separately frozen physical map is the only
authorized next action.
