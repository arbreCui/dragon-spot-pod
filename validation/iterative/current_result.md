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
| $x_6\to x_7$ | 6.4057634863e-8 | 3.0515093508e-4 | 4.4741318561e-7 | 1.5063944615e-7 | `afd9617` |
| $x_7\to x_8$ | 6.4057634863e-8 | 3.7849611670e-4 | 5.5495183915e-7 | 2.6731297644e-7 | `7273253` |

The predeclared final x8 classification is `VALID_NOT_MET`. $R_\rho$ and
$R_a$ pass at 0.128115 and 0.534626 times the tolerance, respectively, but
$R_L$ fails by a factor of 756.992233. Therefore the fixed point has not
been reached. Earlier zero $R_\rho$ entries mean only that the stored
binary32 `K-EFFECTIVE` did not change; they are not exact-arithmetic claims.

The leakage and modal components are nonmonotone and do not share a stable
observed contraction. This trajectory alone proves neither divergence nor a
two-cycle. Relative to x7, x8 $R_L$, $D_L$ and $R_a$ increased by
24.035706%, 24.035647% and 77.452177%, respectively; these one-step changes
do not enter the stopping rule.

The x8 global balance diagnostic is $3.301196\times10^{-9}$. The worst
relative group diagnostic is $3.231639\times10^{-3}$ at group weight
$4.82940\times10^{-12}$, and the Galerkin maximum is
$5.56322\times10^{-7}$. These are reported transparently but are not part
of the frozen Picard stopping criterion.

## Last-two-residual geometry

The hash-locked, no-Dragon audit defines only the two actual map residuals

$$
f_6=x_7-x_6,\qquad f_7=x_8-x_7,
$$

and keeps the state blocks separate. In the physical modal $H_sM_g$ metric,
their norms are $1.0055666009\times10^{-7}$ and
$1.7843996820\times10^{-7}$, their inner product is
$-5.6496911499\times10^{-15}$, and their cosine is $-0.3148630729$.

For leakage, the frozen-height $L_2$ quantity is explicitly an auxiliary,
non-production direction diagnostic. Its two norms are
$8.9898197018\times10^{-6}$ and $1.0047159318\times10^{-5}$, with inner
product $-8.7580759569\times10^{-11}$ and cosine $-0.9696487385$. The
production infinity changes remain
$D_L=4.4741318561\times10^{-7}$ and
$5.5495183915\times10^{-7}\ \mathrm{cm}^{-1}$. Both have one unique hotspot
at plane 3, group 325; its signed update reverses from
$-4.4741318561\times10^{-7}$ to $+5.5495183915\times10^{-7}$ and grows by
24.035647% in magnitude. The stored $\rho$ increments likewise reverse from
$-6.4057634863\times10^{-8}$ to $+6.4057634863\times10^{-8}$, subject to the
binary32 `K-EFFECTIVE` quantization.

Thus the latest leakage residuals are strongly opposed and the second is not
smaller; the modal residuals are also obtuse. No mixed-unit whole-state angle,
fitted coefficient or new stopping rule is defined. Two residuals do not
establish a cycle, divergence, a Jacobian spectrum, rank adequacy, a physical
cause or an inner-error bound. The reproducible details are in
[residual_direction_result.md](residual_direction_result.md).

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

The fixed-basis package, live radial response, physical source, canonical
states, raw defects and restart ordering passed their independent checks for
the valid map evaluations; balance diagnostics were recorded separately.
This establishes trustworthy evaluations of the discrete map $G$; it does
not establish:

- a fixed point;
- rank-1 adequacy;
- discretization convergence;
- accuracy against MPACT, DeCART, nTRACER or a 3D reference.

Full pre-cleanup files and receipts are preserved by Git tag
`archive-pre-lean-20260814`. The final x8 publication receipt hashes are
tracked in [x8_result.sha256](x8_result.sha256), with
[x7_result.sha256](x7_result.sha256) retained as parent evidence. The 443 MB
x8 artifact directory remains local and Git-ignored. The six objects frozen
by role and hash in [current_parent.tsv](current_parent.tsv) are the exact x7
inputs used to produce x8; the manifest is retained as provenance, not as
authorization for x9.

## Next decision

Stop after x8. The frozen direct rank-1 Picard census did not reach its
discrete gate, and no x9 is defined. This result does not by itself establish
divergence, a cycle, rank adequacy or physical accuracy.

The no-transport nonlinear-solver boundary is now frozen in
[nonlinear_solver_contract.md](nonlinear_solver_contract.md). It preserves
$F(x)=G(x)-x$ and requires every proposed state to pass a fresh strict map and
the unchanged three-component AND gate. Full exact Newton is retained only as
a small exact-arithmetic reference: the current real map has no validated
exact Jacobian, and its binary32 publication steps exclude calling a finite
difference an exact derivative. Therefore this phase authorizes neither a
production Newton/JFNK implementation nor another transport evaluation.
