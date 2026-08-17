# Latest minimum-order Anderson decision

Date: 2026-08-16

Classification: `READ_ONLY_DIRECTION_DECISION`.

The two latest residual pairs, \(p\mapsto z\) and \(s\mapsto t\), give the
unique standard full-Gram AA(1) state

\[
-2.5376672366087174\,z+3.5376672366087174\,t.
\]

Its modal ratio is `0.4561392669`, but the same-weight leakage
height-\(L_2\) and \(D_L\) ratios are `3.2731013585` and `3.9536083127`.
AA(1) therefore fails the predeclared componentwise gate and is rejected.

Only then were the three genuine pairs
\(q_{\mathrm{AA2}}\mapsto p\), \(p\mapsto z\), and \(s\mapsto t\)
tested. Standard unregularized full-Gram AA(2) gives

\[
u=0.60952347586151545\,p
 +0.31275948892760497\,z
 +0.07771703521087958\,t.
\]

The 2-by-2 Gram determinant is
`6.4387179385320712e-25`, strictly positive without a condition threshold.
The modal, leakage height-\(L_2\), and \(D_L\) ratios are respectively
`0.0439118392`, `0.2157457702`, and `0.3264537700`. All three weights are
positive and sum to one; all 8880 publication points are strictly positive.

AA(2) is therefore the minimum-order admissible standard Anderson candidate.
These offline quantities authorize materialization only. They are not a map,
stopping defects, or a prediction that the nonlinear map will converge. No
Dragon, relaxation, damping, clipping, fitted coefficient, regularization,
pseudoinverse threshold, or mixed-unit combined norm was used.
