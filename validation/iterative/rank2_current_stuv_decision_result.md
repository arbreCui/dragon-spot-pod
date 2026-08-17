# Minimum-order decision after the current AA(2) return

Date: 2026-08-17

Classification: `READ_ONLY_DIRECTION_DECISION`.

Let the latest genuine maps be

\[
s\mapsto t,\qquad u\mapsto v,
\]

where \(s\) is a `Z-RAW-FLUX` proposal, \(u\) is an
`AA2-RAW-FLUX` proposal, and \(t,v\) are their returned states. Standard
unregularized full-Gram AA(1) gives

\[
x_{\mathrm{AA1}}=
0.2560239609154612\,t+0.7439760390845388\,v.
\]

Relative to the current residual \(v-u\), the modal, leakage height-\(L_2\),
and \(D_L\) same-weight direction ratios are respectively
`0.1600081833`, `1.0818433649`, and `1.0742873210`. The publication is
strictly positive at 8880/8880 points, but both leakage directions increase.
AA(1) therefore fails the fixed componentwise authorization gate.

Only then were the latest three genuine maps

\[
p\mapsto z,\qquad s\mapsto t,\qquad u\mapsto v
\]

examined with standard unregularized full-Gram AA(2). The result is

\[
x_{\mathrm{AA2}}=
-0.043596750567857584\,z
+0.30973740187162246\,t
+0.73385934869623515\,v.
\]

The unmodified 2-by-2 system has

\[
H_{00}=8.478202312142947\times10^{-12},\quad
H_{01}=6.816564410389893\times10^{-12},\quad
H_{11}=5.532694480922610\times10^{-12},
\]

and determinant `4.417527795444883e-25`, strictly positive without a
condition threshold. Its modal, leakage height-\(L_2\), and \(D_L\) ratios
are `0.1587289304`, `1.1404401779`, and `1.1690963012`. It is also positive
at 8880/8880 points, but both leakage directions increase. AA(2) therefore
fails the same gate.

Neither Anderson state is published as a project proposal artifact or
evaluated. The selected next state is the returned state \(v\) itself, so the
next permitted operation is one ordinary Picard evaluation \(G_2(v)\). This
selection contains no fitted
coefficient, relaxation, damping, clipping, regularization, pseudoinverse
threshold, condition cutoff, leakage fit, or mixed-unit norm. The
same-unit \(D_L\) ratio is only a direction screen; dimensional
\(D_L\,[\mathrm{cm}^{-1}]\) remains outside the final dimensionless AND gate.

This is an authorization decision, not a prediction that Picard is
contractive or that the next map will converge. No Dragon or nonlinear map
was run in making it.
