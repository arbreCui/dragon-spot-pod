# Minimum-order AA(1) proposal from $q_8,o,q_9,p$

Date: 2026-08-18

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The unchanged standard unregularized AA(1) calculation used only the two
latest genuine residuals $o-q_8$ and $p-q_9$ and produced

$$
q_{10}=1.2246645215600993\,o-
0.22466452156009933\,p.
$$

The exact denominator is `9.0412608575558238e-13`.  The negative weight is
the standard unconstrained affine result; it is not clipped or replaced.
No regularization or condition cutoff is used.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.12764993865086841`, `0.82141838136874701`, and
`0.89227926518865730`, all strictly below one.  All 8880 reconstructed
points are positive.

The independent checker reproduced the weights, denominator, direction
ratios, carrier, and publication bitwise.  The inputs are strictly identified
as the genuine map pairs $q_8\mapsto o$ and $q_9\mapsto p$ with proposal
carriers `AA2-RAW-FLUX` and `AA1-RAW-FLUX`; the output is
`PROPOSAL + AA1-RAW-FLUX`.  The Git-ignored artifact contains ten regular
files, no symbolic links, and a passing 9/9 receipt:

- proposal AX: `bd0785e9f3da27b9639c3ac4c04d3bf25689c5dc7f16fc51cdcdde7306b154fb`;
- proposal snapshots: `4587fcc293ba18c40c0c785e6de4991d969cc10cca8975b4b4fddf114725c209`;
- receipt: `907855530c6b1e07cfad007086463a996417490f3cfa92eafff4fbe3ee1c28cc`.

This is a parameter-free direction authorization, not convergence evidence.
No Dragon, ASM, FLU, transport, or physical map was run while materializing
the proposal.  No relaxation, damping, clipping, fit, regularization,
pseudoinverse, condition cutoff, empirical parameter, mixed-unit objective,
older-window search, or AA(3) is used.
