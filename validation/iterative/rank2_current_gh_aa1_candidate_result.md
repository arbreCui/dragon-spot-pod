# Minimum-order AA(1) proposal from $q_1,g,q_2,h$

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The unchanged full-Gram builder used only the genuine residuals $g-q_1$
and $h-q_2$ and produced

$$
q_3=0.92198482219461153\,g+
0.078015177805388483\,h.
$$

The scalar denominator is `7.3007449964465324e-13`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.11971305975561962,\ 0.47525043616253554,\
0.70441518119387303).
$$

All three are strictly below one.  The independent checker reproduced the
weights and ratios bitwise, confirmed the `AA1-RAW-FLUX` to $g$ and
`AA2-RAW-FLUX` to $h$ lifecycles, and found 8880/8880 positive
reconstructed points.

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt:

- proposal AX: `c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6`;
- proposal snapshots: `3cd88d1d7f65ad05cc7a62025cb12a2d50bc016a52d35b251685da71c559b37f`;
- receipt: `8b7ddf314b8d62c5a60cf3eb75b341157dcdb5ebfa90307d8bf41a2909beafa6`.

No Dragon, ASM, FLU, transport, or physical map was run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(2)
was used.
