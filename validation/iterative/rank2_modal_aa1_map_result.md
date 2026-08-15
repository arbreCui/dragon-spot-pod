# Fresh map from the rank-2 modal AA(1) proposal

Date: 2026-08-14

Classification: `VALID_NOT_MET`.

The separately authorized experiment evaluated exactly one unchanged physical
map

\[
z=G_2(y_{\rm pub}),
\]

from the hash-locked, publication-aware modal AA(1) proposal. It used the
fixed rank-2 basis, three online frozen-fission radial solves and one axial
solve. There was one attempt, no retry and no subsequent map. No relaxation,
damping, clipping, fitted closure or empirical coefficient was introduced.

## Strict validity evidence

All three radial fixed-source terminals passed strictly:

| plane | `IEXTF` | `EUNK` | `EINR` |
|---:|---:|---:|---:|
| 1 | `7` | `4.18793888e-7` | `4.39565270e-7` |
| 2 | `4` | `3.69540572e-7` | `4.95551262e-7` |
| 3 | `7` | `4.86562669e-7` | `4.84259999e-7` |

The axial terminal also passed strictly:

| quantity | value | limit |
|---|---:|---:|
| outer iterations | `198` | `500` |
| outer error | `5.48021961e-10` | `5.0e-7` |
| unknown error | `3.63727480e-7` | `5.0e-7` |
| terminal inner error | `4.80501626e-7` | `5.0e-7` |

The terminal axial eigenvalue is `1.3623637074465578`; the canonical
REAL32-published value is `1.3623636960983276`. The separate Ganlib-only
checker passed the proposal-input lifecycle, fixed POD package, live radial
operator, raw radial positivity, canonical layout, bitwise-recomputed defects
and returned-leakage archive checks.

The logs report 61 CPU seconds for the radial deck and 137 CPU seconds for the
complete axial deck. The 120-second and 420-second host bounds were operational
process limits only, not physical or convergence parameters.

## Fresh defects

With the unchanged outer tolerance

\[
\varepsilon=5\times10^{-7},
\]

the independently checked result is

| quantity | value | role | multiple of `epsilon` | passes? |
|---|---:|---|---:|---:|
| \(R_\rho\) | `6.576351536824454e-5` | stopping rule | `131.527030736` | no |
| \(R_L\) | `2.265658510333105e-3` | stopping rule | `4531.31702067` | no |
| \(D_L\) (`cm^-1`) | `3.319932147860527e-6` | diagnostic | not applicable | not applicable |
| \(R_a\) | `4.664681926544893e-4` | stopping rule | `932.936385309` | no |

Because all three stopping components exceed the tolerance, this valid map is
not a converged state.

The global and maximum-group balance diagnostics are `1.126193e-8` and
`1.655038e-3`. They do not enter the acceptance gate. In particular, their
different behavior relative to the direct map does not support a general
claim that balance improved.

## Local comparison with the direct second Picard map

Relative to the earlier direct result \(x_2=G_2(x_1)\), the fresh defects at
this one proposal have the ratios

| quantity | proposal-map / direct-map |
|---|---:|
| \(R_\rho\) | `0.101740877724` |
| \(R_L\) | `0.404231524210` |
| \(D_L\) | `0.404192444246` |
| \(R_a\) | `0.0795539272471` |

Thus, for this frozen problem and this single proposal, every stopping
component is smaller than in the direct second Picard map. These are local
cross-input comparisons, not asymptotic convergence factors. They do not show
that Anderson is generally superior to Picard, validate the earlier offline
prediction quantitatively, or establish stability, a Jacobian spectrum, rank
adequacy or physical accuracy.

## Reproduction identity

The Git-ignored artifact is
`validation/artifacts/iterative-rank2-modal-aa1-map/`. Its 20-entry checksum
receipt passes in full. Essential hashes are

| object | SHA-256 |
|---|---|
| `candidate_system.xsm` | `e50f0e5d34c66b6d94331f43ee749d248f7c448fde22b6e517641a111fc9002b` |
| `candidate_radial.xsm` | `3e699e39455a552ee3564a66970d08cd9b930cc70296c403a50e8a510b74e6bb` |
| `candidate_axial.xsm` | `a57feb6e83487561a153ae376874339c116192d0ece3d716cd10e2dac203376e` |
| `candidate_snapshots.xsm` | `f40f83502f18cd97eb21e89ddeb892e3cf8c5fa4530f2f149ca9436e15ded746` |
| `radial.log` | `e65b0617ab0ad8bf7c5cb23b66cc4564206d0a3e285280bf1e4e70a270f7f79c` |
| `axial.log` | `a58ab6bc20ef7a7eb755a2410c3e8865fbd886445e2d5283ce5ab61b61399c14` |
| `independent_check.log` | `cb9c4ff4296b493fdc2f6ad77cffaad93235c46a3ba1b35d24cdc17c762e4551` |
| `result.sha256` | `45bf76532df56c849b526fe78d5c9ffd81d9ecb98fc844a27b45f12d2684a785` |

The artifact's frozen inputs, decks, checker, runner and runtime library
hashes were independently rechecked against the current files. No Dragon
process remained after publication.

## Scientific boundary

This result closes the one-map proposal test. It establishes a valid nonlinear
response with smaller stopping defects in this single cross-input comparison,
but it does not establish convergence. It authorizes neither automatic
acceptance nor another map. Any subsequent solver step must be separately
declared against the same physical map and the same three-component stopping
gate.
