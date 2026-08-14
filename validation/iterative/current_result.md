# Current SPOD/Picard result

## Frozen method

- fixed-space volume-weighted Galerkin SPOD;
- rank $r=1$;
- state $x=(a,\rho,L)$, with $\rho=1/k$;
- online 2D frozen-fission radial solves;
- one reduced 1D axial return;
- direct $x^{m+1}=G(x^m)$;
- inner and outer tolerance $5\times10^{-7}$;
- no relaxation, damping, clipping, fitted closure or empirical parameter.

## Direct trajectory

Every listed state is an actual returned map state. The legacy third map was
superseded by the strict-inner $x_3$.

| map | $R_\rho$ | $R_L$ | $D_L\;[\mathrm{cm}^{-1}]$ | $R_a$ | source commit |
|---|---:|---:|---:|---:|---|
| $x_0\to x_1$ | 1.2811548254e-6 | 7.9228531577e-4 | 1.1616502889e-6 | 9.2282558413e-7 | `a3a81e3` |
| $x_1\to x_2$ | 0 | 3.9564556446e-4 | 5.8009754866e-7 | 7.2377835180e-7 | `e631410` |
| $x_2\to x_3$ | 0 | 4.3252643235e-4 | 6.3417246565e-7 | 3.2409693945e-7 | `61bf69e` |
| $x_3\to x_4$ | 0 | 5.6855251297e-4 | 8.3361373981e-7 | 1.4817206328e-6 | `b411143` |
| $x_4\to x_5$ | 6.4057634863e-8 | 3.1253505970e-4 | 4.5823981054e-7 | 2.3143260254e-7 | `ed9e399` |
| $x_5\to x_6$ | 0 | 2.0941536233e-4 | 3.0704541132e-7 | 7.5835881646e-7 | `46a1209` |

At $x_6$, $R_L$ fails the outer gate by 418.83 and $R_a$ fails by
1.52. Therefore the fixed point has not been reached. The zero stored
$R_\rho$ values mean that the binary32 `K-EFFECTIVE` value did not change;
they are not exact-arithmetic claims.

The leakage and modal components are nonmonotone and do not share a stable
observed contraction. This trajectory alone proves neither divergence nor a
two-cycle.

## One Anderson trial

The leakage-residual least-squares screen gave the unique unclipped
coefficient

$$
\gamma_L=0.3898692835066931.
$$

It was not inserted as an empirical constant: it was computed from the frozen
residuals. One actual nonlinear evaluation $G(x_A)$ returned

$$
(R_\rho,R_L,D_L,R_a)=
(6.4057634863\times10^{-8},\,
2.4458920328\times10^{-4},\,
3.5861739889\times10^{-7}\ \mathrm{cm}^{-1},\,
1.1292180647\times10^{-6}).
$$

Compared with direct $x_6$, $R_L$ and $D_L$ increased by 16.7962% and
$R_a$ increased by 48.9029%. The candidate is rejected as an improving
iterate. This single result does not reject Anderson methods in general.

## Evidence boundary

The fixed-basis package, live radial response, physical source and balance,
canonical states, raw defects and restart ordering passed their independent
checks for the accepted maps. This establishes trustworthy evaluations of the
discrete map $G$; it does not establish:

- a fixed point;
- rank-1 adequacy;
- discretization convergence;
- accuracy against MPACT, DeCART, nTRACER or a 3D reference.

Full pre-cleanup files and receipts are preserved by Git tag
`archive-pre-lean-20260814`. The six local objects needed to continue from
$x_6$ are frozen by role and hash in
[current_parent.tsv](current_parent.tsv).

## Next decision

The generic continuation host and
[three-way decision rule](continuation_policy.md) are implemented and
default-off. The next action is to authorize one unchanged
$x_7=G(x_6)$, once, with no retry. This adds one datum and cannot alone
prove convergence or divergence. The host does not start $x_8$ or modify
the frozen parent.
