# Minimum-order AA(1) proposal from $q_7,n,q_8,o$

Date: 2026-08-18

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The unchanged standard unregularized AA(1) calculation used only the two
latest genuine residuals $n-q_7$ and $o-q_8$ and produced

$$
q_9=0.14445266271586943\,n+
0.85554733728413057\,o.
$$

The exact denominator is `3.8680130073227605e-14`.  No regularization or
condition cutoff is used.  The modal, leakage height-$L_2$, and same-weight
maximum-$|D_L|$ direction ratios are `0.99405602856832498`,
`0.78327883203609316`, and `0.82926667695332601`, all strictly below one.
All 8880 reconstructed points are positive.

The independent checker reproduced the weight, denominator, direction
ratios, carrier, and publication bitwise.  The inputs are strictly identified
as the genuine map pairs $q_7\mapsto n$ and $q_8\mapsto o$ with proposal
carriers `AA1-RAW-FLUX` and `AA2-RAW-FLUX`; the output is
`PROPOSAL + AA1-RAW-FLUX`.  The Git-ignored artifact contains ten regular
files, no symbolic links, and a passing 9/9 receipt:

- proposal AX: `c5d3275ead6dc8b5afb6d7ec125965678a0659ed8cf027d547edd6a009738b4e`;
- proposal snapshots: `f7476c9f42d5de128e56c01044609e233a11ec147019942d429b8db419ba30ab`;
- receipt: `f067f4c6b84714cba07d3326f5915848e34d4be52db4b8a0f1404bfd26c39fd5`.

This is a parameter-free direction authorization, not convergence evidence.
No Dragon, ASM, FLU, transport, or physical map was run while materializing
the proposal.  No relaxation, damping, clipping, fit, regularization,
pseudoinverse, condition cutoff, empirical parameter, mixed-unit objective,
older-window search, or AA(3) is used.
