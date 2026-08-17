# One strict map from the chronological AA(2) proposal

Date: 2026-08-17

Status: `PREPARED_NOT_RUN`.

This default-off stage permits exactly one evaluation

\[
G_2(x),\qquad
x=0.31289249339137026\,t
 +0.34535495185011489\,v
 +0.34175255475851485\,w.
\]

The three positive weights are the standard unregularized full-Gram AA(2)
solution from the genuine chronological maps \(s\mapsto t\),
\(u\mapsto v\), and \(v\mapsto w\). The newest AA(1) was checked first and
rejected because its leakage height-\(L_2\) and \(D_L\) direction ratios
were `1.896269` and `1.306751`.

AA(2)'s same-weight modal, leakage height-\(L_2\), and \(D_L\) direction
ratios are `0.062849`, `0.587018`, and `0.546809`; all 8880 publication
points are positive. These are authorization diagnostics only, not stopping
defects or a prediction of the nonlinear result.

The proposal carries returned \(w\)'s complete raw AX and snapshot payload
as the method-level `AA2-RAW-FLUX` carrier. The unchanged fixed-rank-two host
performs three online radial fixed-source solves followed by one reduced
axial solve. Rank, basis, equations, normalization, strict solve terminals,
and the original gate remain unchanged:

\[
R_\rho\leq5\times10^{-7},\qquad
R_L\leq5\times10^{-7},\qquad
R_a\leq5\times10^{-7}.
\]

Dimensional \(D_L\,[\mathrm{cm}^{-1}]\) is a diagnostic and is not compared
with this dimensionless gate. The 120-second radial and 180-second axial
bounds are process-safety limits, not model or convergence parameters. One
activation permits one attempt, with no retry, fallback, relaxation,
damping, clipping, fitted coefficient, regularization, pseudoinverse
threshold, condition cutoff, or automatic successor.
