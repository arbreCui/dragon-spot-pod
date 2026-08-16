# Next rank-2 modal Anderson(1) proposal after the evaluated consecutive map

Date: 2026-08-15

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Two evaluated residuals

The next standard depth-one history uses exactly the two evaluated map pairs

\[
x_2\longmapsto x_3=G_2(x_2),\qquad
x_{\mathrm{AA1}}\longmapsto
x_{\mathrm{AA1}}^+=G_2(x_{\mathrm{AA1}}).
\]

It therefore forms the modal residuals

\[
p=x_3-x_2,\qquad
q=x_{\mathrm{AA1}}^+-x_{\mathrm{AA1}},
\]

using the actual published $x_{\mathrm{AA1}}$, not an unrounded ideal
affine state. In the unchanged Gram-height POD metric, the standard scalar is

\[
\beta=
\frac{\lVert p\rVert_{HG}^2-\langle p,q\rangle_{HG}}
     {\lVert p-q\rVert_{HG}^2}
=0.859155699175995213.
\]

The denominator is `3.0770317739134968e-11`, so the scalar system is
nonsingular. The resulting proposal is the affine combination of the two map
outputs,

\[
x_{\mathrm{next}}=
0.140844300824004787x_3+
0.859155699175995213x_{\mathrm{AA1}}^+.
\]

The computed coefficient is naturally between zero and one. It was not
clipped, tuned or supplemented by relaxation, damping, a fitted closure or an
empirical parameter. The same scalar was applied to canonical `(A,rho,L)`;
the scalar was determined only in the modal metric, not in a mixed-unit
whole-state norm.

## Publication

The deterministic binary publication produced:

| quantity | value |
|---|---:|
| affine inverse eigenvalue | `0.73399286840402655` |
| published REAL32 $k$ | `1.3624110221862793` |
| reciprocal published `rho` | `0.73399288739993207` |
| publication shift in `rho` | `1.8995905515239997e-8` |
| maximum leakage REAL32 round trip | `5.7384340551927537e-11` |
| minimum published REAL32 $B_2a$ | `1.7534004465846460e-15` |
| strictly positive $B_2a$ points | `8880 / 8880` |

Raw AX flux and snapshot payload were not affinely mixed. They are complete
copies of the latest returned $x_{\mathrm{AA1}}^+$ carrier, explicitly
marked `AA1-RAW-FLUX`; only the canonical proposal fields, published leakage
and eigenvalue were replaced. The lagged snapshot `SYSTEM` continues to
record the actual
$x_{\mathrm{AA1}}\to x_{\mathrm{AA1}}^+$ solve.

## Independent audit and receipt

The independently compiled Ganlib-only checker recomputed the modal scalar
and publication bit for bit. It also passed:

- fixed rank-two basis and layout;
- complete latest AX/raw-flux carrier identity;
- the $x_{\mathrm{AA1}}\to x_{\mathrm{AA1}}^+$ snapshot lifecycle;
- snapshot leakage/eigenvalue publication and unchanged lagged `SYSTEM`;
- absence of stale defect, epoch and balance records;
- strict positivity at all 8880 reconstructed points.

The Git-ignored artifact is
`validation/artifacts/iterative-rank2-modal-aa1-post-candidate`. It contains
10 regular files and no symbolic links. Its 9-entry receipt passes 9/9; the
receipt-file SHA-256 is
`8de6c187c9d720296da3c7770d8d08f57fddbf06cb05cb32d8286ff2e6069356`.

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89` |
| `proposal_snapshots.xsm` | `0c22cc9748beb813757d154ca592f343654e61c710f9b852ad35270ae19e186c` |
| `build.log` | `3843417b23e80ec1e5b7f7086b2af749cc59aeff9059c96ad651206dce107685` |
| `check.log` | `63505096e5a296891d3a8fd32336a4d39804ab53f5b9961596cc8e5f97bc63ce` |

Reproduce this seconds-scale offline stage with:

```sh
make spot-rank2-modal-aa1-post-candidate
```

The builder and checker symbol audit reports
`DRAGON/ASM/FLU/TRANSPORT=0`.

## Scientific boundary

This result establishes one deterministic, positive and provenance-checked
proposal. It does not evaluate $G_2(x_{\mathrm{next}})$, produce a new raw
stopping defect or prove convergence, contraction, stability, Anderson
superiority, rank adequacy or physical accuracy. In particular,
$x_3\to x_{\mathrm{AA1}}^+$ is not a map pair; the two residuals above are
formed from their own declared inputs. No Dragon process was launched, and no
physical-map host or successor map was created.

## Subsequent evaluation

A separately frozen, default-off host subsequently evaluated this proposal
exactly once. That later map is valid but does not meet the unchanged stopping
gate; it does not alter this proposal-stage classification. See
[rank2_modal_aa1_post_map_result.md](rank2_modal_aa1_post_map_result.md).
