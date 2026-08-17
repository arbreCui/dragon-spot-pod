# Minimum-order decision after the latest AA(1) map

Date: 2026-08-17

Classification: `READ_ONLY_DIRECTION_DECISION`.

Let $t=G_2(p)$ be the then-latest valid return from the accepted previous
AA(1) proposal.  The two then-latest evaluated fixed-point residuals are

\[
f(r)=s-r,\qquad f(p)=t-p.
\]

They are valid Anderson history entries because both maps were actually
evaluated; Anderson does not require the accelerated input $p$ to equal the
preceding output $s$.  The return-to-return difference $t-s$ is not used.

Standard unregularized full-Gram AA(1) gives

\[
p_1=-2.4457706598178919\,s+3.4457706598178919\,t.
\]

Its denominator is `4.6653961992325445e-13`, finite and strictly positive
without a cutoff.  Relative to the current residual $t-p$, the modal,
leakage height-$L_2$, and leakage $D_L$ same-weight ratios are
`0.33536538753830303`, `4.5264612159503210`, and
`3.7219595041373470`.  The two leakage directions increase, so AA(1) fails
the fixed componentwise direction screen.  It is not materialized.

Only after that failure, the then-latest three evaluated maps

\[
z\mapsto r,\qquad r\mapsto s,\qquad p\mapsto t
\]

were checked with standard unregularized full-Gram AA(2).  The affine output
combination is

\[
p_2=
0.70710894519475420\,r
-0.16355463490873412\,s
+0.45644568971397992\,t.
\]

The unmodified 2-by-2 system has

\[
H_{00}=5.5462104864511575\times10^{-12},\quad
H_{01}=-1.5057710754184061\times10^{-12},\quad
H_{11}=4.6653961992325324\times10^{-13},
\]

and determinant `3.2018040079658118e-25`, strictly positive without a
condition threshold.  The predicted modal residual squared is
`1.0503837043351299e-14`.  Relative to $t-p$, the modal, leakage
height-$L_2$, and leakage $D_L$ direction ratios are
`0.057797030555672736`, `1.7018125733694425`, and
`1.1884041542212693`.  The affine dimensional leakage direction is
`8.5253774879384046e-7 cm^-1`; it is an authorization diagnostic, not an
outer stopping defect.  The affine inverse eigenvalue is
`0.73399299703641874`; all 8880 reconstructed publication points are
positive, with minimum `1.7533964231781466e-15`.

Both leakage directions again increase, so AA(2) fails the same screen and
is not materialized.  Negative affine weights are not themselves a rejection
criterion.  No older-window search or AA(3) is performed.

The read-only calculations used the unchanged fixed rank-two Gram-height
metric and the same weights for $(a,\rho,L)$.  They introduced no relaxation,
damping, clipping, regularization, pseudoinverse threshold, condition cutoff,
leakage fit, mixed-unit objective, empirical parameter, Dragon, or transport
solve.

By the predeclared minimum-order rule, the selected next input is the
then-latest valid return $t$ itself, unchanged.  Exactly one direct
$G_2(t)$ evaluation is permitted before the original three-component AND
gate is tested.
