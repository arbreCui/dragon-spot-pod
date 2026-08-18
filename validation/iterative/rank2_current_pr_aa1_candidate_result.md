# Minimum-order AA(1) proposal from $q_9,p,q_{10},r$

Date: 2026-08-18

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The unchanged standard unregularized AA(1) calculation used only the two
latest genuine residuals $p-q_9$ and $r-q_{10}$ and produced

$$
q_{11}=0.21697843452735655\,p+
0.78302156547264345\,r.
$$

The exact denominator is `2.1912767600921286e-12`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.50304720552788507`, `0.87862793996767796`, and
`0.82134690926235421`, all strictly below one.  All 8880 reconstructed
points are positive.

The existing generic checker roles are bound exactly as $Q6=q_9$, $M=p$,
$Q7=q_{10}$, and $N=r$.  Thus its two residuals are precisely $p-q_9$ and
$r-q_{10}$; the generic labels do not alter the arithmetic.  The independent
checker reproduced the weights, denominator, direction ratios, carrier, and
publication bitwise.  The output remains an `AA1-RAW-FLUX` carrier.

The Git-ignored artifact contains ten regular files, no symbolic links, and
a passing 9/9 receipt:

- proposal AX: `20b4a9fb31f6baa4f62d9fa5b22cf0801709ceb37579bf9f16dfc7e6c450f05d`;
- proposal snapshots: `d974a4883eaa5460614d25cdf81284644760218308c88f35ed41bd54065d0167`;
- receipt: `98efcfad6fe207c1261eaa9c33cd1333541eae8e4c6dbb2162378a8e3e34f83e`.

This is a parameter-free direction authorization, not convergence evidence.
No Dragon, ASM, FLU, transport, or physical map was run while materializing
the proposal.  No relaxation, damping, clipping, fit, regularization,
pseudoinverse, condition cutoff, empirical parameter, mixed-unit objective,
older-window search, or AA(3) is used.
