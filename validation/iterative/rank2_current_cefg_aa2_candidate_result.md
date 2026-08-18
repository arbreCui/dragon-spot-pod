# Minimum-order AA(2) proposal from $c_{\mathrm{next}},e,f,q_1,g$

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The preceding AA(1), formed only from $f-e$ and $g-q_1$, failed the strict
leakage direction screen.  Only then, the existing standard unregularized
full-Gram AA(2) calculation used the three genuine residuals
$e-c_{\mathrm{next}}$, $f-e$, and $g-q_1$ and produced

$$
q_2=0.37059923635358261\,e+
0.28970803656130206\,f+
0.33969272708511533\,g.
$$

The exact Gram entries are
`H00=8.4049480818263211e-13`,
`H01=-8.3167915360888345e-13`, and
`H11=8.9502797595728517e-13`, with positive determinant
`6.0576152422719129e-26`.  The modal, leakage height-$L_2$, and same-weight
maximum-$|D_L|$ direction ratios are
`0.33342566026806181`, `0.47696732762436056`, and
`0.39981312880450964`, all strictly below one.  All 8880 reconstructed
points are positive.

The independent checker reproduced the weights, Gram system, direction
ratios, and publication.  Both proposal inputs were strictly identified as
`AA1-RAW-FLUX`; the output is `PROPOSAL + AA2-RAW-FLUX`.  The Git-ignored
artifact contains ten regular files, no symbolic links, and a passing 9/9
receipt:

- proposal AX: `d4b25fc5bf9b3cc2eb4c6665833f7560073408ffd5462c0f07e4cf30ead0d1fe`;
- proposal snapshots: `b0aac9dd5575fc48ca351e0b330946afc968777152a6356f9846b5c9ac1b1c79`;
- receipt: `f35e63307b41e2a6f59c4323844ad19159f9587bf0a3befc5a0bdb02f500b979`.

No Dragon, ASM, FLU, transport, or physical map was run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
