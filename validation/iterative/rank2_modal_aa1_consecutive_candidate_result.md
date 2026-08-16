# Consecutive-map rank-2 modal Anderson(1) proposal

Date: 2026-08-15

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

The two genuinely consecutive fixed-rank Picard residuals are

\[
p=x_2-x_{1,\mathrm{pub}},\qquad q=x_3-x_2,
\]

where \(x_2=G_2(x_{1,\mathrm{pub}})\) and \(x_3=G_2(x_2)\). The standard
depth-one scalar in the existing Gram-height modal metric is

\[
\beta=\frac{\lVert p\rVert_{HG}^2-\langle p,q\rangle_{HG}}
{\lVert p-q\rVert_{HG}^2}
=0.672340796207261282.
\]

No clipping or fitted coefficient is used. The materialized proposal is the
standard affine combination of the two map outputs,

\[
x_{\mathrm{AA1}}=(1-\beta)x_2+\beta x_3.
\]

Thus the latest output \(x_3\) has weight `0.672340796207261282` and \(x_2\)
has weight `0.327659203792738718`. The same scalar is applied to canonical
`(A,rho,L)`; the scalar is optimized only in modal space, not in a mixed-unit
full-state norm.

## Frozen checks

| quantity | value |
|---|---:|
| modal denominator | `1.9717012615699543e-10` |
| affine inverse eigenvalue | `0.73399293385983211` |
| published REAL32 \(k\) | `1.3624109029769897` |
| reciprocal published `rho` | `0.73399295162341294` |
| maximum leakage REAL32 round trip | `5.2026360433318763e-11` |
| minimum published REAL32 \(B_2a\) | `1.7533983290022779e-15` |
| strictly positive \(B_2a\) points | `8880 / 8880` |

The AX and snapshot carriers are complete copies of the latest returned
\(x_3\) payload, not affine mixtures of raw fluxes. The proposal is explicitly
marked `X3-RAW-FLUX`. Only the canonical proposal fields, published leakage
and eigenvalue are replaced. The checker proves that the lagged `SYSTEM` and
`SPOT-FS-K` still record the actual \(x_2\to x_3\) solve history.

The five input paths and hashes are frozen in
[`rank2_modal_aa1_consecutive_candidate_inputs.tsv`](rank2_modal_aa1_consecutive_candidate_inputs.tsv).
The local Git-ignored artifact is
`validation/artifacts/iterative-rank2-modal-aa1-consecutive-candidate`:

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `7094d4dc57156aae8f0d0180bcac24bf02640f5de0435b46635151ed975186f1` |
| `proposal_snapshots.xsm` | `ebd0d7f0ca762f907f6d767273298b80262039f22cc4b36682d73a15d34065b2` |

Its receipt covers both outputs, both logs, the input manifest, builder,
independent checker, runner and classification. Builder/checker symbol audits
report `DRAGON/ASM/FLU/TRANSPORT=0`.

Reproduce the short offline stage with:

```sh
make spot-rank2-modal-aa1-consecutive-candidate
```

## Scientific boundary

This proves deterministic AA(1) publication, fixed-basis provenance, exact
carrier lifecycle, binary publication arithmetic and strict reconstructed
positivity. It does not evaluate \(G_2(x_{\mathrm{AA1}})\), provide a new
stopping defect, prove convergence or stability, establish superiority over
Picard, or qualify rank adequacy or transport accuracy. No Dragon process or
new map was started.
