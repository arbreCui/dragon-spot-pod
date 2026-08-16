# One strict map from the consecutive rank-2 modal Anderson(1) proposal

Date: 2026-08-15

Classification: `VALID_NOT_MET`.

## Frozen experiment

The separately authorized experiment evaluated exactly one unchanged
fixed-rank map

\[
x_{\mathrm{AA1}}^+=G_2(x_{\mathrm{AA1}}),\qquad
x_{\mathrm{AA1}}=
0.327659203792738718x_2+0.672340796207261282x_3.
\]

The source tree was frozen at commit
`407bbf3ff7ad150ff815faf937a2c2414094f05d`. The parent AX and snapshot
hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `7094d4dc57156aae8f0d0180bcac24bf02640f5de0435b46635151ed975186f1` |
| proposal snapshots | `ebd0d7f0ca762f907f6d767273298b80262039f22cc4b36682d73a15d34065b2` |

The `X3-RAW-FLUX` marker identified the complete latest raw-flux carrier; it
did not replace the affine canonical parent or any physical equation. The
unchanged host reconstructed the rank-two radial fields from the proposal
coordinates, used the proposal eigenvalue in the frozen-fission source, ran
three online radial fixed-source solves, and then ran one axial solve. There
was one attempt and no retry, re-encoding, relaxation, damping, clipping,
fitted closure or empirical coefficient.

## Strict solve terminals

Every solve reached the unchanged strict \(5\times10^{-7}\) terminal gate:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `12` | `3.77748307e-7` | `3.96603951e-7` |
| radial plane 2 | `6` | `3.45348042e-7` | `3.92779185e-7` |
| radial plane 3 | `5` | `3.23104018e-7` | `2.66976912e-7` |
| axial | `210` | `3.18293843e-7` | `4.81850179e-7` |

The axial `EEXT` was `8.45638490e-11`. The radial and axial logs report 75 s
and 136 s of CPU time, respectively, and each contains exactly one normal
Dragon termination. The terminal REAL64 eigenvalue was
`1.3624111386087798`; canonical REAL32 publication gave
\(k=1.3624111413955688\).

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of \(\varepsilon\) | gate |
|---|---:|---:|---|
| \(R_\rho\) | `1.284469506313002e-7` | `0.2568939013` | pass |
| \(R_L\) | `4.208307444409661e-4` | `841.6614889` | fail |
| \(R_a\) | `1.657876064490356e-6` | `3.3157521290` | fail |

The stopping rule is a three-component AND gate. Since \(R_L\) and \(R_a\)
fail, the map is valid but is not a fixed point at the declared tolerance.
The dimensional leakage change is

\[
D_L=6.165937520563602\times10^{-7}\ \mathrm{cm}^{-1}.
\]

It is a diagnostic with units and is not compared with the dimensionless
outer tolerance. The other balance diagnostics are:

- axial global/max-group balance: `7.355939e-9 / 1.638456e-3`;
- per-plane radial balance: `2.749979e-7`, `3.277239e-7`, `4.125038e-7`;
- assembled radial balance: `4.179892019017465e-7`.

None is an outer stopping quantity.

## Bounded comparisons

Relative to the immediately preceding direct Picard evaluation
\(x_3=G_2(x_2)\), the cross-input ratios for
\((R_\rho,R_L,D_L,R_a)\) are

\[
(0.2000000350,\ 0.8065730453,\ 0.8065633685,\ 0.2287883749).
\]

Thus all four recorded defects are lower in this one comparison. The two
parents are different, however: one is \(x_2\), and the other is the affine
AA(1) proposal. These numbers are not adjacent convergence ratios,
contraction factors, a monotone trajectory or proof of Anderson superiority.

For scientific balance, relative to the earlier evaluated proposal map
\(G_2(x_{1,\mathrm{pub}})\), the corresponding ratios are

\[
(0.1538461404,\ 1.0417078465,\ 1.0416953486,\ 0.1156467543).
\]

In that comparison \(R_L\) and \(D_L\) are about 4.17% higher. The current
leakage defect therefore has not improved componentwise against all prior
rank-two map inputs and remains the dominant stopping failure.

## Independent audit and receipt

The pre-Dragon Ganlib check accepted the exact proposal and
`X3-RAW-FLUX` lifecycle. The independent post-map checker then passed:

- materialized-proposal and carrier identity;
- fixed POD package and canonical layout;
- live radial-operator change and raw radial positivity;
- bitwise recomputation of the four raw defect fields;
- returned restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files and no symbolic
links. Its 21-entry receipt passes 21/21. The receipt-file SHA-256 is
`f5e62ed7ce447bd8e3deff46a81dbaa04b8144a4526a625384b92ca4f8ba9089`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `19f29c81c0942ffa728bfa32c0677d84a3b9f367f07fcb34a44644b833275eac` |
| `candidate_radial.xsm` | `1dfa6e085bcbcc25b71957297b85d39167cec4f5c02672e13b8a35f976df5fe2` |
| `candidate_axial.xsm` | `f4a4ad62b3feca3b76db7162ee532ed28605293beb57b82a6476a064c271b059` |
| `candidate_snapshots.xsm` | `6ae0e77b5ef8ce6959da10acff0cfabc870b6d72b31cce369cfd25bd34d18eea` |
| `radial.log` | `0b404f7b94e4a784134974ea2d5ee7a82ae12d841dd5f73ed28ce1d97406a905` |
| `axial.log` | `ae1c0ea962bb74811fa5356674bb3b24216f8c84866bfc488a012713b44aa4bb` |
| `parent_preflight.log` | `7c7424241d0d868763a261f6bfcbde283b4f10cade2ad134be880dfc0ad18c91` |
| `independent_check.log` | `127487a2ac0a7b5ffc1b7f7f75fdb18fe64845c4382201f9f9d471a0eec7188f` |

The artifact's `continuation_policy.md` is deliberately the hash-frozen
pre-run policy and therefore still says `PREPARED_NOT_RUN`. It records what
was authorized before execution; the receipt-locked logs and
`classification.txt` record the completed runtime result.

## Scientific boundary

This is one valid evaluation of the stated fixed rank-two discrete map. It
does not meet the stopping rule and does not establish asymptotic convergence,
stability, contraction, convergence order, Anderson superiority, rank
adequacy or physical accuracy. No successor map was started.

## Subsequent offline proposal

A later no-Dragon stage used this returned state together with the preceding
direct map to materialize the next standard depth-one proposal. That separate
stage remains `MATERIALIZED_PROPOSAL_NOT_EVALUATED` and did not start another
map; see
[rank2_modal_aa1_post_candidate_result.md](rank2_modal_aa1_post_candidate_result.md).
