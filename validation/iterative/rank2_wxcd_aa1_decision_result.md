# Standard sequential AA(1) decision from w-x and c-d

Date: 2026-08-16

Classification: `OFFLINE_DECISION_COMPLETE`.

The no-Dragon audit used the two actual evaluated pairs

\[
w\mapsto x,\qquad c\mapsto d.
\]

Their full-Gram-height residual norms are
`7.622844825430474e-7` and `1.814082704662637e-6`; the latest is
`2.379797498449265` times the previous one. Another blind direct Picard step
therefore has no local contraction evidence.

The existing standard sequential AA(1) calculation gives the unique state

\[
y=1.6615840721007848x-0.66158407210078485d.
\]

The denominator is `1.1664323281092084e-12`, finite and strictly positive.
The predicted modal residual is `0.1464043157917969` of the current residual,
and all 8880 publication points are positive. The coefficient is the
unclipped least-squares result, not a tuned relaxation.

This is explicitly an extrapolation. With the same modal coefficient, the
auxiliary leakage height-L2 and dimensional maximum screens are `1.824006`
and `1.589305` times their current values. They are risk diagnostics only and
cannot accept or reject the nonlinear map.

AA(2) was not selected: the existing production AA(2) carrier modes do not
accept these three current map pairs, and adding a new mode would exceed this
study's minimal boundary. The only authorized next action is to materialize
the existing `--next-x4` AA(1) state and, if all checks pass, evaluate it once.
