# Rank-two REAL64 solver-floor boundary

Date: 2026-08-18

Status: `SOLVER_FLOOR_BOUNDARY`; the `5e-7` outer AND gate is unchanged.

This is a no-Dragon, read-only consolidation of already-frozen evidence.
It creates no candidate, runs no map, and changes no gate, tolerance,
physics, or parameter.

## Evidence

1. Three same-parent axial-terminal points on the unchanged epoch-5
   window:
   - `solver_eps = 2.5e-7`: $R_L=2.4829538\times10^{-6}$
     (`iterative-rank2-h2-r64-aa1-z-map`);
   - `solver_eps = 1.25e-7`: $R_L=2.9994077\times10^{-6}$, a 20.80%
     increase under a tighter terminal
     (`iterative-rank2-h2-r64-aa1-z-axial-tight`);
   - `solver_eps = 5.0e-8`: no strict terminal exists.  The solve
     exhausted `MAXOUT=500` with `EEXT=1.3e-11` and a flux-update
     plateau `EUNK=5.79228015e-7`, and strict termination refused
     publication (`iterative-rank2-h2-r64-aa1-z-axial-eps5e8`).
2. Two independent affine-screen violations at small amplitude: the
   `c` proposal map increased $R_L$ by a factor of about 17.5 although
   all three direction ratios were below one
   (`iterative-rank2-h2-r64-aa1-b-map`), and the `e` proposal map
   recovered only to about 41.6 gate multiples
   (`iterative-rank2-h2-r64-aa1-d-map`).
3. Across eleven REAL64 maps, $R_\rho$ passes throughout, $R_a$
   decreased monotonically once accelerated and passes at
   $1.2406359\times10^{-7}$, and $R_L$ has never certified below
   $2.4829538\times10^{-6}$.

## Boundary statement

Under the present single-precision flux kernel, the certifiable floor
of the leakage stopping defect is approximately
$R_L\approx2.5\times10^{-6}$, about five gate multiples.  The two best
frozen states are the epoch-5 return `u`
($R_L=2.4829538\times10^{-6}$, $R_a=2.7689296\times10^{-7}$) and the
epoch-9 return `b` ($R_L=2.7411806\times10^{-6}$,
$R_a=1.3271558\times10^{-7}$); both pass $R_\rho$ and $R_a$ and fail
only $R_L$.  The coupled 2D-1D + POD iteration is therefore at the
solver's certification floor, not at the unchanged `5e-7` gate: the
classification of every map remains `VALID_NOT_MET`, and no
convergence under the gate is claimed.

Further maps under the current numerical-map contract cannot certify
below this floor, so continuation-map production is suspended at
`CLOSED/11` pending the REAL64 axial flux-kernel scoping decision.
The gate itself is deliberately left unchanged so that any future
higher-precision kernel is measured against the original target.
