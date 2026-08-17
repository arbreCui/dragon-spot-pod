# Route decision after the Q(s)-v-w study

Date: 2026-08-16

Classification: `OFFLINE_ROUTE_SELECTED`.

The latest two alternative valid maps are:

| map | $R_\rho$ | $R_L$ | $D_L$ | $R_a$ |
|---|---:|---:|---:|---:|
| direct $v\mapsto w$ | `6.422349219104007e-8` | `2.635805720887253e-4` | `3.861932782456279e-7` | `1.876678378894124e-6` |
| modal AA(1) $y\mapsto z$ | `6.422348086676521e-8` | `3.238169577271681e-4` | `4.744506441056728e-7` | `5.468734245606544e-7` |

The leakage defect remains hundreds of times above tolerance. The direct map
reduced all four recorded defects relative to the preceding $Q(s)\mapsto v$
map. The AA(1) map reduced the modal defect but increased $R_L$ and $D_L$ by
factors `1.22853120` and `1.22853160` relative to the direct map.

The preceding same-beta leakage affine diagnostic predicted a decrease, but
the fresh nonlinear AA(1) map increased leakage. Therefore that diagnostic
is not used as a production selector. No combined norm or leakage-fitted
coefficient is introduced.

The selected route preserves the genuinely consecutive direct trajectory:

\[
x=G_2(w),
\]

followed by a read-only direction audit of $v\mapsto w\mapsto x$, and then at
most one further direct map $G_2(x)$. This is a route decision, not a map or
convergence result. It ran no Dragon and changed no physical model, basis,
rank, deck, tolerance or stopping rule.
