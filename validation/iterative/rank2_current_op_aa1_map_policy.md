# One map from the latest admissible AA(1) proposal

Date: 2026-08-18

Status: `EXECUTED_ONCE_VALID_NOT_MET`.

Standard unregularized AA(1) uses only the two latest genuine residuals
$o-q_8$ and $p-q_9$ and gives

$$
q_{10}=1.2246645215600993\,o-
0.22466452156009933\,p.
$$

Its exact denominator is `9.0412608575558238e-13`.  Its modal, leakage
height-$L_2$, and same-weight maximum-$|D_L|$ direction ratios are
`0.12764993865086841`, `0.82141838136874701`, and
`0.89227926518865730`, all strictly below one.  The negative weight is the
standard unconstrained affine solution; it is not clipped or replaced.
These parameter-free screens authorize one direction; they do not predict
convergence.

One explicit activation permits exactly one physical map

$$
r=G_2(q_{10}).
$$

The unchanged fixed-rank-two host performs three online radial fixed-source
solves and one axial solve.  Acceptance uses only the original AND gate

$$
R_\rho\le5\times10^{-7},\qquad
R_L\le5\times10^{-7},\qquad
R_a\le5\times10^{-7}.
$$

Dimensional $D_L\,[\mathrm{cm}^{-1}]$ remains diagnostic only.  If valid,
the physical fixed-point residual is $r-q_{10}$; $r-p$ is not that residual.
The 120 s radial and 180 s axial limits are process-safety bounds, not model
coefficients.

One activation permits one attempt.  There is no retry, fallback, automatic
successor, relaxation, damping, clipping, fit, regularization, pseudoinverse,
condition cutoff, empirical parameter, mixed-unit objective, older-window
search, or AA(3).  This batch permits no second physical map.

## Post-run record

The stage was activated exactly once from source commit
`25c4f31132290de4c3816d972b4f469c1b682357`.  All four strict terminals,
the independent `proposal-aa1` checker, and the 21/21 receipt passed.  The
physical residual $r-q_{10}$ is

$$
(R_\rho,R_L,D_L,R_a)=
(6.422348086676521\times10^{-8},\,
9.408223459489815\times10^{-4},\,
1.378473825752735\times10^{-6}\ \mathrm{cm}^{-1},\,
5.576247465674659\times10^{-7}).
$$

$R_\rho$ passes the original AND gate; $R_L$ and $R_a$ do not.  The map is
therefore `VALID_NOT_MET`.  AA(1) on $p-q_9$ and $r-q_{10}$ has direction
ratios `0.50304720552788507`, `0.87862793996767796`, and
`0.82134690926235421`, all strictly below one.  Thus
`AA1_DIRECTION_PASS_AA2_SKIPPED`; AA(2) is not calculated.  No durable
proposal is published and no second physical map is run.  The artifact's
`continuation_policy.md` remains the receipt-protected pre-run policy copy.
See [rank2_current_op_aa1_map_result.md](rank2_current_op_aa1_map_result.md).
