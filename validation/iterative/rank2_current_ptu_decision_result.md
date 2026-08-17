# Minimum-order decision after the direct return u

Date: 2026-08-17

Classification: `AA1_DIRECTION_PASS_AA2_SKIPPED`.

Let $t=G_2(p)$ and $u=G_2(t)$.  Hash and raw-defect checks establish the
two latest actual map residuals

\[
f_0=t-p,\qquad f_1=u-t.
\]

Standard unregularized full-Gram AA(1) gives the unique affine output

\[
q=0.41546155012473063\,t+0.58453844987526937\,u.
\]

The modal scalar denominator is
`9.1628280657850502e-12`, finite and strictly positive without a cutoff.  The
predicted modal residual norm is `1.16580470578225e-7`.  Relative to the
latest residual $u-t$, the parameter-free direction ratios are:

| component | candidate/current |
|---|---:|
| modal Gram-height norm | `0.092304347566644032` |
| leakage height-$L_2$ norm | `0.6639121298325844` |
| leakage $D_L$ infinity norm | `0.5610758902997232` |

All three are strictly below one.  The dimensional candidate leakage
direction is `7.0775135063364284e-7 cm^-1`; it is a same-unit authorization
diagnostic, not part of the dimensionless outer stopping gate.

The same affine weights act on $(a,\rho,L)$.  The affine inverse eigenvalue
is `0.73399291408231893`, the deterministic REAL32 publication gives
`k=1.3624110221862793`, and all 8880 reconstructed flux points are strictly
positive, with minimum `1.7534001289472908e-15`.

AA(1) therefore passes the predeclared componentwise screen.  By the
minimum-order rule, AA(2) is not formed or searched.  The weights happen to
be convex, but no convexity constraint was imposed.  This calculation used
no Dragon, transport solve, relaxation, damping, clipping, leakage fit,
regularization, pseudoinverse threshold, condition cutoff, mixed-unit norm,
or empirical coefficient.

This is an offline direction decision only.  It does not establish a fixed
point.  The sole authorized continuation is to materialize $q$, verify its
publication and the latest $u$ raw carrier independently, and then evaluate at
most one fresh physical map $G_2(q)$ before applying the original
three-component AND gate.
