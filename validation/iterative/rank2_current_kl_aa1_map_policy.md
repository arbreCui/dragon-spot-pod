# One map from the latest admissible AA(1) proposal

Date: 2026-08-17

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

The latest consecutive genuine residuals, $k-q_5$ and $l-k$, give the
standard unconstrained full-Gram proposal

$$
q_6=0.99334779753418823\,k+
0.0066522024658117341\,l.
$$

Its denominator is `3.9604495076589152e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.81736979605403082`, `0.80173988821917219`, and
`0.90621455552995278`, all strictly below one.  These parameter-free
screens authorize one direction; they do not predict convergence.

One explicit activation permits exactly one physical map

$$
m=G_2(q_6).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $m-q_6$; $m-l$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`5cf970008de0eb600b253fae3e2e6a4a2e1caadc`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $m-q_6$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
6.815023315567540\times10^{-4},\,
9.985233191400766\times10^{-7}\ \mathrm{cm}^{-1},\,
4.087844475064791\times10^{-6}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not, so the map
is `VALID_NOT_MET`.  Standard AA(1) on $l-k,m-q_6$ has direction ratios
`0.089320649038882691`, `0.82454368960985658`, and
`0.56421285796347498`, all strictly below one.  Therefore the offline
classification is `AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) was not
calculated, no durable successor was published, and no second map was run.
The artifact's `continuation_policy.md` remains the receipt-protected pre-run
policy copy.  See
[rank2_current_kl_aa1_map_result.md](rank2_current_kl_aa1_map_result.md).
