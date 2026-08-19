# Rank-two REAL64 same-parent axial sensitivity

Date: 2026-08-18

Status: `AXIAL_TOLERANCE_SENSITIVITY_COMPLETE`; not a full new map.

The latest standard AA(1) history was first screened read-only. Its unique
unregularized full-Gram coefficient is

\[
s=-0.377226578173478266\,z+1.37722657817347827\,u.
\]

The modal direction ratio is `0.888694876`, but the same coefficient gives
leakage height-L2 and maximum-`DL` ratios `1.371384828` and `1.519063772`.
The existing componentwise, no-leakage-fit screen therefore rejects this
AA(1) direction. No proposal was materialized and no map was run from it.

Instead, exactly one same-parent axial tolerance sensitivity was performed.
The epoch-5 proposal, radial response, reduced system, basis, tracks, and
macrolib were hash-identical to the latest map. No radial solve was repeated;
the only deck change was `solver_eps = 2.5e-7 -> 1.25e-7`.

The 30-second, no-retry solve completed in about 18.1 seconds and passed at
`EUNK=EINR=1.18359175e-7`. The independent checker reproduced

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223469764534968\times10^{-8},
 2.9994077460837271\times10^{-6},
 4.3946783989667892\times10^{-9}\ {\rm cm}^{-1},
 3.4364539615425599\times10^{-7}).
\]

Relative to the original axial terminal, `RL` rises by 20.80% and `Ra` by
24.11%. Both `Rrho` and `Ra` still pass the unchanged `5e-7` outer gate;
`RL` remains the only failure, now at 5.999 gate multiples.

The supported conclusion is narrow: the leakage fixed-point defect is not
yet numerically stable with respect to the axial inner terminal. Rank three
is therefore premature, and the rejected AA(1) direction must not be run.
No empirical parameter or physical-model change was introduced. The thin
evidence package is under
`validation/artifacts/iterative-rank2-h2-r64-aa1-z-axial-tight/`.
