# One strict map from the v-w-x standard AA(1) state

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

For the consecutive direct residuals $p=w-v$ and $q=x-w$, standard
full-Gram-height AA(1) gives

\[
\beta=0.62189690650343510,\qquad
c=(1-\beta)w+\beta x.
\]

The coefficient is recomputed, unique and not adjustable. It is a convex
combination, and the same weights act on $A,\rho,L$. No leakage fit, clipping,
damping, relaxation, regularization or combined norm is used.

This default-off stage permits exactly one $G_2(c)$. The fixed rank-two POD
basis, physical decks, normalization, online radial transport, axial solve,
strict terminals and original AND gate at $5\times10^{-7}$ remain unchanged.
The 120/420 second bounds are external process limits. There is no retry,
fallback or automatic successor.
