# Current-window standard AA(1) proposal

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The latest actual maps are (p\mapsto t) and (t\mapsto u).  Standard
unregularized full-Gram AA(1) gives

\[
q=0.41546155012473063\,t+0.58453844987526937\,u.
\]

The denominator is `9.1628280657850502e-12`, finite and positive without a
cutoff.  Relative to the current residual $u-t$, the modal, leakage
height-$L_2$, and leakage $D_L$ direction ratios are respectively
`0.092304347566644032`, `0.66391212983258452`, and
`0.56107589029972316`.  All three are strictly below one.  AA(1) therefore
passes the fixed parameter-free screen and AA(2) is skipped.

The same weights act on $(a,\rho,L)$.  The affine inverse eigenvalue is
`0.73399291408231893`; publication gives (k=1.3624110221862793) and
(\rho=0.73399288739993207).  All 8880 reconstructed points are strictly
positive, with minimum `1.7534001289472908e-15`.

The complete latest returned (u) AX/raw-flux and snapshot payloads are the
carriers.  `X4-RAW-FLUX` is only the existing protocol marker; the input
manifest and bitwise checker bind the payload to (u).  The independent
checker reproduced the weights, three direction ratios, REAL64/REAL32
publication, fixed rank-two bundle, raw carrier, lagged system, and
positivity.

The artifact contains 10 regular files, no symbolic links, and a passing
9/9 receipt.

| output | SHA-256 |
|---|---|
| proposal AX | `75dd254844b001596f3e57e6aad373e6bdec7aa84958e79b9111c555e93556cf` |
| proposal snapshots | `169be7e8f17e7b1985b65ae2522966bbba0768febadb2a031f0e0a860e0a11fd` |
| build log | `8922725285a615624d98a2aa54029f048218e8174bd0b3f0947c2c30b77b4fad` |
| independent-check log | `af7f0e44c480ec2f3a3668897bdd3774464adcf59d8cd07cf706a455a9576fcb` |
| receipt | `f437788d3458fca094615459c08badbf75f5086239dd34f5efdedfebf7f45777` |

This offline stage ran no Dragon or transport solve and introduced no
relaxation, damping, clipping, leakage fit, regularization, condition
threshold, or empirical parameter.  The proposal is not a convergence
result; exactly one fresh physical map is required before the original AND
gate can accept it.
