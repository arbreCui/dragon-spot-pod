# Standard AA(1) proposal from the latest consecutive residuals

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The genuine fixed-point residuals $k-q_5$ and $l-k$ give the standard
unconstrained full-Gram AA(1) proposal

$$
q_6=0.99334779753418823\,k+
0.0066522024658117341\,l.
$$

The scalar denominator is `3.9604495076589152e-13`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.81736979605403082,\ 0.80173988821917219,\
0.90621455552995278).
$$

All three are strictly below one.  The independent checker reproduced the
weights and ratios bitwise, verified the $k\mapsto l$ snapshot lifecycle and
fixed rank-two bundle, and found 8880/8880 positive reconstructed points.
The 9/9 receipt passes.

| output | SHA-256 |
|---|---|
| proposal AX | `d223068dbabd5424762f6f73fb488a927cca94ca4db3cee7ef3bbf7f090d825d` |
| proposal snapshots | `c6c9546bb7807864aa2b0eaa56e289ee91ffa1ec4328b7889a5deb81d9b2cec6` |
| receipt | `c0ca1244186e3b70e23efde028cb5bb2fd04a215364cf8728abc95250bcf4e6e` |

No Dragon, ASM, FLU, radial transport, axial solve, or physical map ran
during materialization.  AA(2) was not calculated because AA(1) passed the
predeclared parameter-free direction gate.  There is no relaxation, damping,
clipping, fit, regularization, pseudoinverse, condition cutoff, empirical
parameter, mixed-unit objective, older-window search, or AA(3).
