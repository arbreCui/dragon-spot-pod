# Current s/t/u/v/v/w standard AA(2) candidate

Date: 2026-08-17

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The three genuine returned-map residuals are \(s\mapsto t\),
\(u\mapsto v\), and \(v\mapsto w\). The schema requires the returned
\(v\) path and the next-map input \(v\) path to be identical. The standard
unregularized full-Gram 2-by-2 solve gives

\[
x_{\mathrm{AA2}}=
0.31289249339137026\,t+
0.34535495185011489\,v+
0.34175255475851485\,w.
\]

The Gram entries are `H00=7.5745720743142734e-12`,
`H01=1.1212225422833167e-12`, and
`H11=2.0056749117494527e-13`. The determinant is
`2.6207292834475100e-25`, strictly positive without a condition threshold,
regularization, damping, or fitted parameter. The predicted modal residual
squared is `3.9966332332107560e-15`.

The unchanged three-direction screen passes: modal, leakage height-\(L_2\),
and leakage \(D_L\) ratios against the current \(v\mapsto w\) residual are
`0.0628492636`, `0.5870176478`, and `0.5468089499`. All 8880 reconstructed
publication points are strictly positive; the minimum is
`1.75340436e-15`.

The independent checker reproduced the solve and publication bitwise,
verified the \(v\mapsto w\) snapshot lifecycle, and confirmed that the
complete raw AX/snapshot payload comes only from returned \(w\). The
proposal carrier marker remains `AA2-RAW-FLUX`. The artifact receipt is
9/9. No Dragon, transport map, stopping defect, or convergence decision was
produced. The minimum-order selection is recorded in
[rank2_current_uvvw_decision_result.md](rank2_current_uvvw_decision_result.md).

| output | SHA-256 |
|---|---|
| proposal AX | `2bfa87e6cfb0e1a4567e0fd210d5879a196ae2594f7fb7ce76ff8831860acf5e` |
| proposal snapshots | `9849404ff2a87ae886be47949c52e77f263447121116828f30dd306d29afa1d2` |
| receipt | `52aa756557bf5cd8657be8802fb4323737e84b8dbe3a809645236c5aea9d6d72` |
