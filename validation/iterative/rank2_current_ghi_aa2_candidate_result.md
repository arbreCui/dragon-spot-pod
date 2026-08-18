# Minimum-order AA(2) proposal from $q_1,g,q_2,h,q_3,i$

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

AA(1) on $h-q_2$ and $i-q_3$ was tried first and failed because its
leakage height-$L_2$ direction ratio is `1.0001541854604454`.  Only then,
the unchanged standard unregularized full-Gram AA(2) calculation used the
three genuine residuals $g-q_1$, $h-q_2$, and $i-q_3$ and produced

$$
q_4=0.54656692430484066\,g+
0.22903224207636369\,h+
0.22440083361879565\,i.
$$

The exact Gram entries are
`H00=4.3985149551517116e-13`,
`H01=9.3117635317024804e-13`, and
`H11=2.1525757104699756e-12`, with positive determinant
`7.9724244756408422e-26`.  No regularization or condition cutoff is used.
The modal, leakage height-$L_2$, and same-weight maximum-$|D_L|$ direction
ratios are `0.085602787687317231`, `0.50064418931908561`, and
`0.44048518991529284`, all strictly below one.  All 8880 reconstructed
points are positive.

The independent checker reproduced the weights, Gram system, direction
ratios, and publication bitwise.  The three proposal inputs are strictly
identified as `AA1-RAW-FLUX`, `AA2-RAW-FLUX`, and `AA1-RAW-FLUX`; the
output is `PROPOSAL + AA2-RAW-FLUX`.  The Git-ignored artifact contains ten
regular files, no symbolic links, and a passing 9/9 receipt:

- proposal AX: `5202ebe842a373800fe65c0748890a6a21fdc43e497bb24f152d536fb53ae391`;
- proposal snapshots: `d841554d9bb0b9e158dfda323ead4016c98c450387bb656416218f3b6d1d5548`;
- receipt: `ad195329b64ea33abc9dee918a0b169ce1de3d174c6a560055692184aae2fd08`.

No Dragon, ASM, FLU, transport, or physical map was run.  No relaxation,
damping, clipping, fit, regularization, pseudoinverse, condition cutoff,
empirical parameter, mixed-unit objective, older-window search, or AA(3)
is used.
