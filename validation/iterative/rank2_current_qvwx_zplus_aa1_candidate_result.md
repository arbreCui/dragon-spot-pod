# AA(1) candidate after the direct map from $z$

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

For the genuine consecutive maps $y\mapsto z$ and $z\mapsto z^+$, the
standard unregularized full-Gram AA(1) state is

$$
c=0.41511181447765411\,z+
0.58488818552234589\,z^+.
$$

The denominator is `4.3847089635551763e-12`.  The modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios relative to
$z^+-z$ are

$$
(0.093357573037484751,\ 0.42214650302136542,\
0.61065652318148245).
$$

All three are strictly below one.  The published reconstructed field is
positive at 8880/8880 points, with minimum
`1.7534035170790798e-15`.  Therefore minimum order passes and AA(2) remains
skipped.

The independent checker reproduced the affine publication bitwise,
verified the $z\mapsto z^+$ snapshot lifecycle, and confirmed that the
complete raw AX and snapshot carrier comes only from returned $z^+$.  The
candidate is marked `AA1-RAW-FLUX`.  The artifact contains 10 regular files,
no symbolic links, and a passing 9/9 receipt.

| output | SHA-256 |
|---|---|
| proposal AX | `5d462c634e7f909ff059d72ac8bb8d9240cb18c21232c682c99d8f34d791c67c` |
| proposal snapshots | `3c216fff2be1336c29e584e4b8b0d6d9eca537f80c6a5fc07bf08f4ad509eb84` |
| receipt | `9e62eaf4dd4f6e2337065dfc34ab78f2fad9e3aa9ead96e09f5fa32b503c9430` |

No Dragon, assembly, transport, map, stopping defect, or convergence
decision is produced by this offline step.  No empirical parameter,
relaxation, damping, clipping, fit, regularization, pseudoinverse, condition
cutoff, or mixed-unit objective is used.
