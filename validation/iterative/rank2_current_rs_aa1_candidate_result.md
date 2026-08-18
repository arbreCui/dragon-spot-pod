# Minimum-order AA(1) proposal from $q_{10},r,q_{11},s$

Date: 2026-08-18

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The unchanged standard unregularized AA(1) calculation used only the two
latest genuine residuals $r-q_{10}$ and $s-q_{11}$ and produced

$$
q_{12}=0.41267816249435374\,r+
0.58732183750564626\,s.
$$

The exact denominator is `3.8071754534215003e-13`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.30785297571708414`, `0.94676682054309913`, and
`0.98610570398914554`, all strictly below one.  All 8880 reconstructed
points are positive.

The existing generic checker roles are bound exactly as $Q6=q_{10}$, $M=r$,
$Q7=q_{11}$, and $N=s$.  Thus its two residuals are precisely $r-q_{10}$
and $s-q_{11}$; the generic labels do not alter the arithmetic.  The
independent checker reproduced the weights, denominator, direction ratios,
carrier, and publication bitwise.  The output remains an `AA1-RAW-FLUX`
carrier.

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt:

- proposal AX: `11c73abd4e35419da447429b6de73191b05d31cff132db0e762d45316f5b4e26`;
- proposal snapshots: `779e419a8b2a378b837976dd726757c2bf13d406184126182eca64b00c065f6f`;
- receipt: `d4a31593b12e818ab28a5e0f078abb5d65db0a5d2122cc7e32e496886e02a6ab`.

This is a parameter-free direction authorization, not convergence evidence.
No Dragon, ASM, FLU, transport, or physical map was run while materializing
the proposal.  No relaxation, damping, clipping, fit, regularization,
pseudoinverse, condition cutoff, empirical parameter, mixed-unit objective,
older-window search, or AA(3) is used.
