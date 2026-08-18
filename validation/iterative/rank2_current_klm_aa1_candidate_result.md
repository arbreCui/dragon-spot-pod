# Standard AA(1) proposal from the latest consecutive residuals

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The genuine fixed-point residuals $l-k$ and $m-q_6$ give the standard
unconstrained full-Gram AA(1) proposal

$$
q_7=0.71958187611175339\,l+
0.28041812388824661\,m.
$$

The implementation reuses the existing screened two-residual path with the
exact local mapping `z=k`, `z_plus=l`, `c=q6`, and `d=m`; no new numerical
mode is introduced.  The scalar denominator is `1.4220277430317252e-11`.
The modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are

$$
(0.089320649038882691,\ 0.82454368960985658,\
0.56421285796347498).
$$

All three are strictly below one.  The independent checker reproduced the
weights and ratios bitwise, verified the $q_6\mapsto m$ snapshot lifecycle
and fixed rank-two bundle, and found 8880/8880 positive reconstructed points.
The 9/9 receipt passes.

| output | SHA-256 |
|---|---|
| proposal AX | `74cbee2ffcb72db1a86e728f8643cfbe9dfb6f2784965fe440bd20567a50ee89` |
| proposal snapshots | `78a999ff7b2fab8f7fbfd4b29e0d433b9ae9e9ef5b124ff812c776b7422f437c` |
| receipt | `defc91abd0622bbe45e31fa1633c1fa0e7c80fe483ea255a618d0dcf6d29fc77` |

No Dragon, ASM, FLU, radial transport, axial solve, or physical map ran
during materialization.  AA(2) was not calculated because AA(1) passed the
predeclared parameter-free direction gate.  There is no relaxation, damping,
clipping, fit, regularization, pseudoinverse, condition cutoff, empirical
parameter, mixed-unit objective, older-window search, or AA(3).
