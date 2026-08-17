# Consecutive v-w-x direction audit

Date: 2026-08-16

Classification: `OFFLINE_DECISION_COMPLETE`.

The read-only Ganlib audit used the real consecutive direct states
$v\mapsto w\mapsto x$. It ran no Dragon or transport.

| diagnostic | value |
|---|---:|
| modal update cosine | `-0.9900280992450681` |
| modal norm ratio, latest/previous | `0.6094638546459439` |
| leakage height-L2 cosine | `-0.3389953522960061` |
| leakage height-L2 norm ratio | `1.4423942276482196` |
| $D_L$ ratio | `1.7449790873808357` |

The leakage hotspot moved from plane 3/group 321 to plane 2/group 325. The
modal updates are strongly alternating, while the latest leakage update grew.
Therefore another unmodified direct map is not selected for the final trial.

The existing standard full-Gram-height AA(1) arithmetic gives

\[
\beta=0.62189690650343510,\qquad
c=0.37810309349656490w+0.62189690650343510x.
\]

The denominator is `4.0332768469441034e-12`, finite and strictly positive.
This is a convex combination. The same coefficient applies to $A,\rho,L$.
All 8880 publication points are positive. The same-beta leakage L2 affine
ratio `0.5873192588486897` is recorded only as a risk diagnostic; the prior
experiment established that such a screen is not a nonlinear-map predictor.

The selected final trial is exactly one fresh $G_2(c)$. There is no clipping,
damping, relaxation, fitted leakage coefficient, combined norm, retry or
fallback.
