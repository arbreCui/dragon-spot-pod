# Minimum-order AA(1) proposal from $c_{\mathrm{next}},e,f$

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The existing full-Gram builder used only the genuine residuals
$e-c_{\mathrm{next}}$ and $f-e$ and produced

$$
q_1=0.54317069088638781\,e+
0.45682930911361219\,f.
$$

The scalar denominator is `3.3988810913576900e-12`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are

$$
(0.059424727376440133,\ 0.19596354669013863,\
0.28717479223258224).
$$

All three are strictly below one.  The independent checker reproduced the
weights and ratios bitwise, confirmed the fixed rank-two package and raw
carrier, and found 8880/8880 positive reconstructed points with minimum
`1.7533991760352251e-15`.

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt:

- proposal AX: `76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd`;
- proposal snapshots: `5b7d6d7c0cf00a4097284b53816d7e3c91ca4e27656f0bc437f6a0472555ac68`;
- receipt: `b4f6b8d0e38d8f4d56110aeacab6114bf300d4250f1bdd6ddafe98e161ca668b`.

No Dragon, ASM, FLU, transport, or physical map was run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
