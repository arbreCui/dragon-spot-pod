# Minimum-order decision after the chronological AA(2) map

Date: 2026-08-17

Classification: `READ_ONLY_DIRECTION_DECISION`.

The latest two evaluated maps are

\[
v\mapsto w,\qquad x\mapsto y,
\]

where \(x\) is the preceding chronological AA(2) proposal and
\(y=G_2(x)\).  They are chronological map pairs, not a direct-consecutive
trajectory because \(w\ne x\).  Standard unregularized full-Gram AA(1),
using the actual residuals \(w-v\) and \(y-x\), gives

\[
q_1=
0.62150849162451971\,w+
0.37849150837548035\,y.
\]

Its scalar denominator is `7.0066798778552567e-12`, strictly positive
without a cutoff.  Relative to the current residual \(y-x\), the modal,
leakage height-\(L_2\), and leakage \(D_L\) same-weight direction ratios
are `0.054458297331438192`, `1.0664059999714603`, and
`0.77718107541701908`.  All 8880 reconstructed publication points are
positive, but leakage height-\(L_2\) increases.  AA(1) therefore fails the
unchanged componentwise authorization gate.

Only then were the latest three evaluated maps

\[
u\mapsto v,\qquad v\mapsto w,\qquad x\mapsto y
\]

examined with standard unregularized full-Gram AA(2).  The result is

\[
q_2=
0.39248173027184491\,v+
0.28907503340209423\,w+
0.31844323632606092\,y.
\]

The unmodified 2-by-2 system has

\[
H_{00}=5.0632544795914974\times10^{-12},\quad
H_{01}=5.9346834331359149\times10^{-12},\quad
H_{11}=7.0066798778552519\times10^{-12},
\]

with determinant `2.5613582707632480e-25`, strictly positive without a
condition threshold.  Its predicted modal residual squared is
`2.4193811744749871e-15`.  The modal, leakage height-\(L_2\), and leakage
\(D_L\) ratios against the current \(x\mapsto y\) residual are
`0.029854100610551285`, `0.57628836727793609`, and
`0.62221015506703192`.  All three weights are positive and sum to one; all
8880 reconstructed publication points are positive, with minimum
`1.7534043641120271e-15`.

AA(2) is therefore the lowest-order admissible standard Anderson candidate
for this fixed chronological window.  No older-window scan was performed.
These offline quantities authorize one candidate publication only; they are
not stopping defects and do not predict the nonlinear map outcome.  The
same-unit \(D_L\) ratio is only a direction screen; dimensional
\(D_L\,[\mathrm{cm}^{-1}]\) remains outside the dimensionless outer AND
gate.  No Dragon, relaxation, damping, clipping, fitted coefficient,
regularization, pseudoinverse threshold, condition cutoff, or mixed-unit
norm was used.
