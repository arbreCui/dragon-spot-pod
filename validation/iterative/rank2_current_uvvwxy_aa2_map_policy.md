# One strict map from the latest chronological AA(2) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

This default-off stage permits exactly one evaluation

\[
G_2(q_2),\qquad
q_2=0.39248173027184491\,v
   +0.28907503340209423\,w
   +0.31844323632606092\,y.
\]

The three positive weights are the standard unregularized full-Gram AA(2)
solution from the genuine chronological maps \(u\mapsto v\),
\(v\mapsto w\), and \(x\mapsto y\).  The newest AA(1) was checked first
and rejected because its leakage height-\(L_2\) direction ratio was
`1.066406`; its modal and \(D_L\) screens are not used to excuse that
failure.

AA(2)'s same-weight modal, leakage height-\(L_2\), and \(D_L\) direction
ratios are `0.029854`, `0.576288`, and `0.622210`; all 8880 publication
points are positive.  These are authorization diagnostics only, not
stopping defects or a prediction of the nonlinear result.

The proposal carries returned \(y\)'s complete raw AX and snapshot payload
as the method-level `AA2-RAW-FLUX` carrier.  The unchanged fixed-rank-two
host performs three online radial fixed-source solves followed by one
reduced axial solve.  Rank, basis, equations, normalization, strict solve
terminals, and the original gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional \(D_L\,[\mathrm{cm}^{-1}]\) is a diagnostic and is not compared
with this dimensionless gate.  The 120-second radial and 180-second axial
bounds are process-safety limits, not model or convergence parameters.  One
activation permits one attempt, with no retry, fallback, relaxation,
damping, clipping, fitted coefficient, regularization, pseudoinverse
threshold, condition cutoff, or automatic successor.
