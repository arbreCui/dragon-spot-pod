# Standard AA(1) candidate from consecutive v-w-x states

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The existing standard full-Gram-height AA(1) builder independently recomputed

\[
\beta=0.62189690650343510,\qquad
c=0.37810309349656490w+0.62189690650343510x.
\]

The denominator was `4.0332768469441034e-12`, finite and strictly positive.
The same convex weights were applied to $A$, $\rho$ and $L$; all 8880
published points were strictly positive.

The independent checker passed the fixed rank-two bundle, publication,
raw-flux carrier, snapshot leakage, lagged system and stale-result checks.
The nine-entry artifact receipt passed 9/9. Its frozen products are:

- axial proposal SHA-256:
  `31579eccb0d6668c21c02add7d9dea9d64752fa9f32e20409ca22e3a53bf3255`;
- snapshot proposal SHA-256:
  `484dd243ca76b84887c951d1c0be7e59c6396e68ffd4962a4cfb2f41e59fd0d9`;
- receipt-file SHA-256:
  `d3e5f837aad89879aeb8b4f3d85bbe39f3b5129e1244863be93166c4a99c2987`.

The candidate stage ran no Dragon, ASM, FLU or transport solve. It is only the
hash-locked parent for one separately authorized real map; it makes no
convergence claim.
