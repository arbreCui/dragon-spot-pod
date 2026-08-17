# Minimum-order decision after the direct Picard return

Date: 2026-08-17

Classification: `READ_ONLY_DIRECTION_DECISION`.

The newest two genuine maps are consecutive:

\[
u\mapsto v,\qquad v\mapsto w.
\]

Standard unregularized full-Gram AA(1) gives

\[
x_{\mathrm{AA1}}=
2.0945024076340903\,v-1.0945024076340903\,w.
\]

Its scalar denominator is `2.0056749117494958e-13`, strictly positive
without a condition threshold. Relative to the current residual
\(w-v\), the modal, leakage height-\(L_2\), and \(D_L\) same-weight
direction ratios are `0.3610849186`, `1.8962689658`, and `1.3067512989`.
All 8880 reconstructed publication points are positive, but both leakage
directions increase. AA(1) therefore fails the unchanged componentwise
authorization gate. Its negative coefficient is not itself the rejection
criterion.

Only then were the latest three genuine maps

\[
s\mapsto t,\qquad u\mapsto v,\qquad v\mapsto w
\]

examined with standard unregularized full-Gram AA(2). The result is

\[
x_{\mathrm{AA2}}=
0.31289249339137026\,t+
0.34535495185011489\,v+
0.34175255475851485\,w.
\]

The unmodified 2-by-2 system has

\[
H_{00}=7.5745720743142734\times10^{-12},\quad
H_{01}=1.1212225422833167\times10^{-12},\quad
H_{11}=2.0056749117494527\times10^{-13},
\]

with determinant `2.6207292834475100e-25`, strictly positive without a
cutoff. The modal, leakage height-\(L_2\), and \(D_L\) direction ratios are
`0.0628492636`, `0.5870176478`, and `0.5468089499`. All three weights are
positive and sum to one; all 8880 reconstructed publication points are
strictly positive.

AA(2) is therefore the lowest-order admissible standard Anderson candidate.
These offline quantities authorize one candidate publication only. They are
not stopping defects and do not predict the nonlinear map outcome. The
same-unit \(D_L\) ratio is only a direction screen; dimensional
\(D_L\,[\mathrm{cm}^{-1}]\) remains outside the dimensionless outer AND
gate. No Dragon, relaxation, damping, clipping, fitted coefficient,
regularization, pseudoinverse threshold, condition cutoff, or mixed-unit
norm was used.
