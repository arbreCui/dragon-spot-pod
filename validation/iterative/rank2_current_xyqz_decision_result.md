# Minimum-order decision after the latest AA(2) return

Date: 2026-08-17

Classification: `READ_ONLY_DIRECTION_DECISION`.

Let \(q\) be the latest AA(2) proposal and \(z=G_2(q)\) its valid returned
state.  The latest two evaluated maps are

\[
x\mapsto y,\qquad q\mapsto z.
\]

They are independent chronological map pairs; neither \(z-y\) nor any other
return-to-return difference is a fixed-point residual.  Standard
unregularized full-Gram AA(1), using only \(y-x\) and \(z-q\), gives

\[
q_1=6.3585033702921443\,y-5.3585033702921443\,z.
\]

Its scalar denominator is `5.0088801044621228e-14`, strictly positive
without a cutoff.  Relative to the current residual \(z-q\), the modal,
leakage height-\(L_2\), and leakage \(D_L\) same-weight direction ratios
are `0.62176664228546874`, `11.197161194771111`, and
`13.237128491309985`.  The affine inverse eigenvalue is
`0.73399254325819330`; all 8880 reconstructed publication points are
positive, with minimum `1.7533977996066858e-15`.  Both leakage directions
increase strongly, so AA(1) fails the unchanged componentwise authorization
gate.  The negative weight is not itself the rejection criterion.

Only then were the latest three evaluated maps

\[
v\mapsto w,\qquad x\mapsto y,\qquad q\mapsto z
\]

examined with standard unregularized full-Gram AA(2).  The result is

\[
q_2^+=
0.62181989589964526\,w+
0.37312990847343913\,y+
0.0050501956269156101\,z.
\]

The unmodified 2-by-2 system has

\[
H_{00}=7.9208580051727201\times10^{-12},\quad
H_{01}=4.8213346418105533\times10^{-13},\quad
H_{11}=5.0088801044640899\times10^{-14},
\]

with determinant `1.6429360344072260e-25`, strictly positive without a
condition threshold.  Its predicted modal residual squared is
`8.0499311822300159e-15`.  The modal, leakage height-\(L_2\), and leakage
\(D_L\) ratios against \(z-q\) are `0.049379303011681620`,
`1.2848181393779037`, and `1.2266816623249386`.  All weights are positive,
the affine inverse eigenvalue is `0.73399292765971136`, and all 8880
publication points are positive, with minimum `1.7534052111449743e-15`.
Both leakage directions nevertheless increase, so AA(2) fails the same
gate.

No Anderson proposal is materialized.  As predeclared, the selected next
state is the valid returned state \(z\) itself, permitting one ordinary
Picard evaluation \(G_2(z)\).  This is the original parameter-free fixed
point map, not a fitted fallback and not a prediction of convergence.  No
older-window scan, Dragon, relaxation, damping, clipping, regularization,
pseudoinverse threshold, condition cutoff, leakage fit, or mixed-unit norm
was used.  Dimensional \(D_L\,[\mathrm{cm}^{-1}]\) remains outside the final
dimensionless AND gate.
