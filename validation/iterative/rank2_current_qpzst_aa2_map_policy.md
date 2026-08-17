# One strict map from the current three-residual AA(2) proposal

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

This default-off stage permits exactly one evaluation

\[
G_2(u),\qquad
u=0.60952347586151479p
 +0.31275948892760236z
 +0.07771703521088286t.
\]

The three positive weights are the unique standard unregularized full-Gram
AA(2) solution from the genuine maps \(q_{\mathrm{AA2}}\mapsto p\),
\(p\mapsto z\), and \(s\mapsto t\). AA(1) was checked first and rejected
because its leakage screens increased by factors `3.27` and `3.95`.

AA(2)'s same-weight modal, leakage height-\(L_2\), and \(D_L\) ratios are
`0.043912`, `0.215746`, and `0.326454`; all 8880 publication points are
positive. These are authorization diagnostics only, not convergence
acceptance or a prediction of the nonlinear result.

The proposal carries returned \(t\)'s complete raw AX and snapshot payload
as the method-level `AA2-RAW-FLUX` carrier. The unchanged host performs three
online radial fixed-source solves followed by one reduced axial solve. Rank,
basis, equations, normalization, decks, strict inner predicates and the
original gate

\[
R_\rho,R_L,R_a\le5\times10^{-7}
\]

remain unchanged. The 120-second radial and 180-second axial bounds are only
process-safety limits. One activation permits one attempt, with no retry,
fallback, relaxation, damping, clipping, fitted coefficient, regularization,
condition cutoff, or automatic successor.
