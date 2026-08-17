# One strict physical map from the published Q(s)

Date: 2026-08-16

Classification: `VALID_NOT_MET`.

## Frozen experiment

The authorized stage evaluated exactly once

\[
v=G_2(Q(s)),\qquad
s=0.815637869982362540z+0.184362130017637404u.
\]

The source tree and remote branch were frozen at commit
`2e05b2ad17c568fa6b7a2359d0ae752962ab8409`. The proposal hashes were:

| parent | SHA-256 |
|---|---|
| proposal AX | `53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193` |
| proposal snapshots | `3404d4295b8f71fa20d9b565fc88c0631184775dcac336be2f50e797999cefaa` |

The 9/9 proposal receipt, all six map-parent hashes and the strict
`PROPOSAL + U-RAW-FLUX` preflight passed before Dragon. Three online radial
fixed-source solves and one axial solve then used the unchanged rank two,
fixed basis, normalization, decks, equations, solver tolerances and stopping
gate. The process bounds were 120 seconds radial and 420 seconds axial.
There was one activation and no retry, fallback or empirical control.

## Strict solve terminals

All four solves met the unchanged strict $5\times10^{-7}$ terminal contract:

| solve | `IEXTF` | `EUNK` | `EINR` |
|---|---:|---:|---:|
| radial plane 1 | `6` | `2.02372576e-7` | `2.84272630e-7` |
| radial plane 2 | `4` | `4.25450594e-7` | `2.36935421e-7` |
| radial plane 3 | `18` | `4.21222182e-7` | `3.49582564e-7` |
| axial | `228` | `4.13012884e-7` | `4.80350707e-7` |

The axial `EEXT` was `2.12814141e-10`. The radial and axial logs report 85
and 144 seconds of CPU time and each contains exactly one normal Dragon end.
The radial balance diagnostic was `3.757744710567186e-7`. The axial
global/max-group balance was `7.72332e-9 / 1.63497e-3`, its Galerkin maximum
was `4.81476e-7`, and it contained zero nonpositive flux cells. These are
diagnostics, not outer stopping quantities.

## Raw stopping result

For the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked raw result is:

| quantity | raw value | multiple of $\varepsilon$ | gate |
|---|---:|---:|---|
| $R_\rho$ | `1.284469730578053e-7` | `0.256894` | pass |
| $R_L$ | `4.207912846624437e-4` | `841.583` | fail |
| $R_a$ | `2.653141867393721e-6` | `5.30628` | fail |

The three-component AND gate therefore fails through $R_L$ and $R_a$. The
dimensional leakage diagnostic is

\[
D_L=6.165355443954468\times10^{-7}\ \mathrm{cm}^{-1}.
\]

Relative only to the preceding valid $Q(t)\mapsto u$ map, $R_L$ decreased
by `5.11085%`, $D_L$ by `5.11086%`, and $R_a$ by `28.3733%`; $R_\rho$
approximately doubled but remains below tolerance. This adjacent comparison
does not establish convergence, contraction or AA(1) superiority.

## Independent audit and receipt

The post-map Ganlib checker passed the U carrier identity, fixed POD package,
canonical layout, live radial-operator change, raw radial positivity, bitwise
four-defect recomputation and restart-archive lifecycle.

The local Git-ignored artifact contains 22 regular files, no symbolic links,
and a passing 21/21 receipt. Its receipt-file SHA-256 is
`57bdd4825d61f1947dafe1b8564aaae21748cc09ee519a70dd2745616ddb932a`.

| output | SHA-256 |
|---|---|
| `candidate_system.xsm` | `6bc2a5dd3e1a0a8f31395629e10bc2b10f650d28ae86b5841e1fcdec0e084796` |
| `candidate_radial.xsm` | `316637cd37c9ac4d79597e9c70c833706eda1f1500a657e1c15a3636a945d038` |
| `candidate_axial.xsm` | `0842ea931a0b53babb7ea7cde6af459ad86d219ea70e83f1242b7b86ce2bf737` |
| `candidate_snapshots.xsm` | `a701f41dfc42fb31043befad8c3607d669bbba456c1dda663a6c6a1873d1f9ed` |
| `radial.log` | `5f414a95095b286e1bd867607f1941c812e583b033107d423f7a426fd9d5db26` |
| `axial.log` | `300441642cf0ab4a44b573738b6ce8d24a181c481c75df24e78f519bd1f35460` |
| `parent_preflight.log` | `349ee84cf5079756c231dc48421f24b3f2237f7791d66520c87103ea035b7b52` |
| `independent_check.log` | `213bda234ea88f3cc91d3e3bb4fff938bca47cd50c160c51b34b9b7dff4560a4` |

The receipt-locked policy remains the frozen pre-run authorization and
therefore says `PREPARED_NOT_RUN`; the runtime logs and classification record
the completed result.

## Scientific boundary

This is one valid evaluation of the stated fixed-rank-two map.
It does not meet the convergence target.
It establishes no asymptotic convergence, stability, contraction,
convergence order, AA(1) superiority, rank adequacy
or physical accuracy. No retry, new proposal or successor map was started.
