# Standard AA(1) proposal from Q(s)→v and v→w

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

Using the two consecutive real map residuals

\[
p=v-Q(s),\qquad q=w-v,
\]

the unchanged full-Gram-height modal rule gives

\[
\beta=0.58613211193957626,qquad
y=0.41386788806042374v+0.58613211193957626w.
\]

The denominator is `9.0691291898807979e-12`; it is finite and strictly
positive. This is a convex combination. The same weights were applied to
\(A\), \(\rho\), and \(L\), with no clipping, damping, relaxation,
regularization, fitted coefficient or separate leakage weight.

The independently recomputed same-coefficient leakage L2/current and
\(D_L\)/current ratios are `0.59562646285803311` and
`0.59916457255893851`. They are risk diagnostics only and do not enter the
coefficient or accept the state.

Publication produced positive \(\rho\), REAL32
\(k=1.3624109029769897\), and 8880/8880 positive reconstructed points. The
independent Ganlib checker reproduced the coefficient and complete
publication bitwise, verified the fixed rank-two bundle and the complete
returned \(w\) AX/snapshot carrier, and confirmed that the builder/checker
have no Dragon, ASM, FLU or transport symbols.

| artifact | SHA-256 |
|---|---|
| proposal AX | `18860e284a02f104821a6eba26ea7743863ccf1193e01089389685648ef7f6c0` |
| proposal snapshots | `77a3f082955c42ecdcae925a8b52f40217e129715123eca4c5fb45ce6c9440e8` |
| receipt | `fabdf17b2c58fe47b92a02672f32c7dd21e3e66bdae367174e262ce273459b47` |

The artifact contains ten regular files, no symlinks and a passing 9/9
receipt. This offline stage ran no map and created no new stopping defect.
