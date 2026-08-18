# Minimum-order AA(1) proposal from $q_3,i,q_4,j$

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The unchanged full-Gram builder used only the genuine residuals $i-q_3$
and $j-q_4$ and produced

$$
q_5=1.1922339465680236\,i-
0.19223394656802359\,j.
$$

The scalar denominator is `1.1217162258501826e-11`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.064424480296712869,\ 0.93186663298811390,\
0.97357313211276764).
$$

All three are strictly below one.  The negative $j$ weight is the standard
unconstrained AA(1) result and was not clipped or replaced.  The independent
checker reproduced the weights and ratios bitwise, confirmed the
`AA1-RAW-FLUX` $q_3\to i$ and `AA2-RAW-FLUX` $q_4\to j$ lifecycles, and
found 8880/8880 positive reconstructed points.

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt:

- proposal AX: `27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743`;
- proposal snapshots: `f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c`;
- receipt: `00a4011204736be578dd2c65eb94f6505e4fde0e7a29c593e044210f37261752`.

No Dragon, ASM, FLU, transport, or physical map was run in this step.  No
relaxation, damping, clipping, fit, regularization, pseudoinverse, condition
cutoff, empirical parameter, mixed-unit objective, older-window search, or
AA(2) was used.
