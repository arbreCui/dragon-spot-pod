# Minimum-order decision after the direct Picard return

Date: 2026-08-17

Classification: `READ_ONLY_DIRECTION_DECISION`.

Let $r=G_2(z)$ be the latest valid returned state.  The latest two genuine
fixed-point residuals are $z-q$ and $r-z$, from the consecutive maps

\[
q\mapsto z,\qquad z\mapsto r.
\]

Standard unregularized full-Gram AA(1) gives the affine direction

\[
p_1=-0.40758989134867640\,z
    +1.4075898913486764\,r.
\]

Its scalar denominator is `1.6234914093469272e-12`, strictly positive
without a cutoff.  Relative to the current residual $r-z$, the modal,
leakage height-$L_2$, and leakage $D_L$ same-weight direction ratios are
`0.48906814192182257`, `1.5459305399633334`, and
`1.5669599175231159`.  The affine inverse eigenvalue is
`0.73399304202375126`; all 8880 reconstructed publication points are
positive, with minimum `1.7533929291672391e-15`.  The two leakage
directions increase, so AA(1) fails the predeclared componentwise direction
screen and is not materialized.

Only after that failure, the latest three genuine evaluated maps

\[
x\mapsto y,\qquad q\mapsto z,\qquad z\mapsto r
\]

were examined with standard unregularized full-Gram AA(2).  Their residuals
are exactly $y-x$, $z-q$, and $r-z$; no return-to-return difference is used as a
map residual.  The affine direction is

\[
p_2=
0.68787468891759174\,y
-1.0040269308670913\,z
+1.3161522419494995\,r.
\]

The unmodified 2-by-2 system has

\[
H_{00}=1.2419660205337551\times10^{-12},\quad
H_{01}=1.4076843144180214\times10^{-12},\quad
H_{11}=1.6234914093469317\times10^{-12},
\]

with determinant `3.4746035978811679e-26`, strictly positive without a
condition threshold.  Its predicted modal residual squared is
`7.4665768997441412e-14`.  Relative to $r-z$, the modal, leakage
height-$L_2$, and leakage $D_L$ direction ratios are
`0.45893496514023896`, `1.8351671663939348`, and
`2.1032558289214176`.  The affine inverse eigenvalue is
`0.73399299197359924`; all 8880 reconstructed publication points are
positive, with minimum `1.7533932468045943e-15`.  Both leakage directions
again increase, so AA(2) fails the same screen and is not materialized.

The dimensional $D_L\,[\mathrm{cm}^{-1}]$ direction is a fixed candidate
authorization diagnostic; it is not a fourth member of the final
dimensionless convergence gate.  No Anderson proposal, relaxation,
damping, clipping, regularization, pseudoinverse threshold, condition
cutoff, leakage fit, mixed-unit norm, older-window search, Dragon, or
transport solve was used in this decision.

As predeclared, the selected state is the latest valid return $r$ itself,
unchanged, permitting exactly one ordinary Picard evaluation $G_2(r)$.
This is the original parameter-free fixed-point map, not a fitted fallback
and not a prediction of convergence.
