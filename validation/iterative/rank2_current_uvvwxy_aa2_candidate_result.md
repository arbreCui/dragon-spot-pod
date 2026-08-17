# Current u/v/v/w/x/y standard AA(2) candidate

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The three genuine evaluated-map residuals are \(u\mapsto v\),
\(v\mapsto w\), and \(x\mapsto y\).  The schema requires the returned
\(v\) path and the next-map input \(v\) path to be identical.  Standard
unregularized full-Gram AA(2) gives

\[
q_2=
0.39248173027184491\,v+
0.28907503340209423\,w+
0.31844323632606092\,y.
\]

The Gram entries are `H00=5.0632544795914974e-12`,
`H01=5.9346834331359149e-12`, and
`H11=7.0066798778552519e-12`.  The determinant is
`2.5613582707632480e-25`, strictly positive without a condition threshold,
regularization, damping, or fitted parameter.  The predicted modal residual
squared is `2.4193811744749871e-15`.

The unchanged three-direction screen passes: modal, leakage height-\(L_2\),
and leakage \(D_L\) ratios against the current \(x\mapsto y\) residual are
`0.029854100610551285`, `0.57628836727793609`, and
`0.62221015506703192`.  All 8880 reconstructed publication points are
strictly positive; the minimum is `1.7534043641120271e-15`.

The independent checker reproduced the solve and publication bitwise,
verified the \(x\mapsto y\) snapshot lifecycle, and confirmed that the
complete raw AX/snapshot payload comes only from returned \(y\).  The
proposal carrier marker remains `AA2-RAW-FLUX`.  The artifact receipt is
9/9.  No Dragon, transport map, stopping defect, or convergence decision was
produced.  The minimum-order selection is recorded in
[rank2_current_vwxy_decision_result.md](rank2_current_vwxy_decision_result.md).

| output | SHA-256 |
|---|---|
| proposal AX | `68cac6d4968785e7cfa5a0bc5c90a6619bf0d9d31d203b75b440894bf472c194` |
| proposal snapshots | `44e00f71215c64985b8ab8a60646830ff9b5b239d2f42c0f8f87d510f4f1360b` |
| receipt | `66b7bf63bea41a65a577b749c782dced03504c9120cc8ac6ca5f35a3f264bfc3` |
