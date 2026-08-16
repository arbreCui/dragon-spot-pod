# Second rolling rank-2 modal Anderson(1) proposal

Date: 2026-08-16

Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`.

## Two latest real map residuals

The proposal uses exactly the two latest valid fixed-rank map pairs

\[
x_{\mathrm{next}}\longmapsto x_{\mathrm{next}}^+,
\qquad
x_{\mathrm{roll}}\longmapsto x_{\mathrm{roll}}^+.
\]

In the unchanged rank-two Gram-height metric, define

\[
p=x_{\mathrm{next}}^+-x_{\mathrm{next}},\qquad
q=x_{\mathrm{roll}}^+-x_{\mathrm{roll}}.
\]

The standard depth-one Anderson scalar is

\[
\beta=
\frac{\lVert p\rVert_{HG}^2-\langle p,q\rangle_{HG}}
     {\lVert p-q\rVert_{HG}^2}
=0.20587044810094848,
\]

with denominator `2.3423675558433505e-13`. It produces

\[
x_{\mathrm{roll2}}=
0.79412955189905154x_{\mathrm{next}}^+
+0.20587044810094848x_{\mathrm{roll}}^+.
\]

The coefficient is naturally between zero and one, but that interval was not
an acceptance gate. The coefficient was not clipped, tuned, relaxed, damped
or regularized. The same scalar was applied to canonical `(A,rho,L)`; raw
flux was not mixed.

## Frozen provenance

The offline generator was frozen at source commit
`cd5e8facf0ff652b73a1450dcd376f40062dbfad`. Its six hash-locked inputs were:

| role | SHA-256 |
|---|---|
| \(x_{\mathrm{next}}\) | `58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89` |
| \(x_{\mathrm{next}}^+\) | `dfe9bc56a38c44799b63f5086aaecfbd24a9060d1dc45bbc6ca721d1c4c2c89d` |
| \(x_{\mathrm{roll}}\) | `a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee` |
| \(x_{\mathrm{roll}}^+\) | `dbb333c8cd1a00a24de40d7b8685349fb83f63a7f0d92c0d2d225c8a25bc07a2` |
| latest returned snapshots | `ca57bdfb2f950aa24cf5a42edf9fe59883ccfa9221388fbc6aee8b76c94480fc` |
| rank-two basis | `2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8` |

The complete latest-returned \(x_{\mathrm{roll}}^+\) AX/raw-flux payload is
carried under the distinct `XRP-RAW-FLUX` marker. The snapshot archive comes
from the same returned map and retains the actual
\(x_{\mathrm{roll}}\to x_{\mathrm{roll}}^+\) lagged `SYSTEM`. Only the
proposal coordinates, eigenvalue and leakage publication were changed.

## Publication and independent check

| quantity | value |
|---|---:|
| affine inverse eigenvalue | `0.73399293840169622` |
| published REAL32 \(k\) | `1.3624109029769897` |
| reciprocal published `rho` | `0.73399295162341294` |
| publication shift in `rho` | `1.3221716721467658e-8` |
| maximum leakage REAL32 round trip | `5.4767050053014521e-11` |
| minimum published REAL32 \(B_2a\) | `1.7533961055407913e-15` |
| strictly positive \(B_2a\) points | `8880 / 8880` |

The independently compiled Ganlib-only checker passed:

- bitwise affine publication in the fixed rank-two bundle;
- complete latest AX/raw-flux and snapshot carrier identity;
- the real \(x_{\mathrm{roll}}\to x_{\mathrm{roll}}^+\) lifecycle;
- leakage/eigenvalue publication and unchanged lagged `SYSTEM`;
- absence of stale defect, balance and epoch records;
- strict positivity at every reconstructed point.

The builder/checker symbol audit reports `DRAGON/ASM/FLU/TRANSPORT=0`. The
local Git-ignored artifact contains 10 regular files and no symbolic links.
Its 9-entry receipt passes 9/9; the receipt-file SHA-256 is
`4550e41b195d521e80a5c6311dbe266fc198af21336132c3599fdf393f52e777`.

| output | SHA-256 |
|---|---|
| `proposal_axial.xsm` | `5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394` |
| `proposal_snapshots.xsm` | `c27fee3d0d396c4427a7389c123b044a8ec61e274a6348b9f83343fb167313ee` |

Reproduce this seconds-scale offline stage with:

```sh
make spot-rank2-modal-aa1-rolling-next-candidate
```

## Scientific boundary

This result establishes one finite, positive and provenance-checked standard
AA(1) proposal. It does not evaluate \(G_2(x_{\mathrm{roll2}})\), create a new
raw stopping defect or establish convergence, contraction, stability,
Anderson superiority, rank adequacy or physical accuracy. No Dragon process,
physical map, retry or successor calculation was started.
