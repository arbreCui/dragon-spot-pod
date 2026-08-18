# Minimum-order AA(2) proposal from $k,l,q_6,m,q_7,n$

Date: 2026-08-18

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

AA(1) on $m-q_6$ and $n-q_7$ was tried first.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios were
`0.86145202366683948`, `1.0902164970939685`, and
`1.0741288780839371`.  Because the two leakage screens failed, and only
then, the unchanged standard unregularized full-Gram AA(2) calculation used
the three latest genuine residuals $l-k$, $m-q_6$, and $n-q_7$ and produced

$$
q_8=0.37973124035268829\,l+
0.10995812065327257\,m+
0.51031063899403917\,n.
$$

The exact Gram entries are
`H00=1.8044480565486487e-12`,
`H01=-2.9455774211730038e-12`, and
`H11=6.5246745314225818e-12`, with positive determinant
`3.0970099337137395e-24`.  No regularization or condition cutoff is used.
The modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.16177043590261239`, `0.45458049672516687`, and
`0.46901724246492071`, all strictly below one.  All 8880 reconstructed
points are positive.

The independent checker reproduced the weights, Gram system, direction
ratios, carrier, and publication bitwise.  The three proposal inputs are
strictly identified as the genuine map pairs $k\mapsto l$,
$q_6\mapsto m$, and $q_7\mapsto n$; the output is
`PROPOSAL + AA2-RAW-FLUX`.  The Git-ignored artifact contains ten regular
files, no symbolic links, and a passing 9/9 receipt:

- proposal AX: `6dee27775279ddf1b75113ceafa62bf60acad27965b13f2122c146976ae892c8`;
- proposal snapshots: `d925a87d087cf971b1d2a8f18dae9603caed3b3233b738ada97bae82a0b6998e`;
- receipt: `1b0bae6de9918643aae1058a6eaa3d5aa3c7faac7feb958b1802f0a2f8d44d67`.

This is a parameter-free direction authorization, not convergence evidence.
No Dragon, ASM, FLU, transport, or physical map was run while materializing
the proposal.  No relaxation, damping, clipping, fit, regularization,
pseudoinverse, condition cutoff, empirical parameter, mixed-unit objective,
older-window search, or AA(3) is used.
