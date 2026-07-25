# Stage-4 v2 axial-state geometry diagnostic

## Scope

This is a post-capture, read-only diagnostic of the single unresolved
\(R_a\) component.  It is not a new acceptance gate and cannot change the
frozen `UNRESOLVED` classification.

It performs no Dragon or transport solve, changes no XSM object, searches no
tolerance, and introduces no relaxation, fit, clipping, empirical
coefficient, or magnitude threshold.

## Frozen inputs

| role | file | SHA-256 |
|---|---|---|
| \(a_0\) | `validation/artifacts/iterative-map1/state0_axial.xsm` | `0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb` |
| \(a_{2h}\) | `validation/artifacts/inner-sensitivity-v2-capture-898ffc7/state1_axial.xsm` | `34928aca2cbc8ac7e61966919e8ebbf1c2cb0cf496cde3acfb3d489a2c46bf73` |
| \(a_h\) | `validation/artifacts/iterative-map1/state1_axial.xsm` | `2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484` |

The three objects must have bitwise-identical `SPOT-X-DIMS`,
`SPOT-X-RANK`, `SPOT-X-OFF`, `SPOT-X-GOFF`, `SPOT-X-BOFF`,
`SPOT-X-BASIS`, `SPOT-X-H`, `SPOT-X-GRAM`, and normalization identifier.
The frozen case has 370 groups, three axial planes, and rank one in every
group.

## Geometry

Define

\[
u=a_{2h}-a_0,\qquad
e=a_h-a_{2h},\qquad
v=a_h-a_0=u+e.
\]

For modal vectors \(p,q\), use only the stored physical POD metric

\[
\langle p,q\rangle_V
=\sum_{s,g}H_s\,p_{s,g}^{T}M_gq_{s,g},
\qquad
M_g=B_g^TWB_g.
\]

No exact-orthonormality assumption is made.  The global primitives are

\[
U^2=\langle u,u\rangle_V,\quad
E^2=\langle e,e\rangle_V,\quad
V^2=\langle v,v\rangle_V,\quad
C=\langle u,e\rangle_V,
\]

\[
Q_{2h}^2=\langle a_{2h},a_{2h}\rangle_V,\qquad
Q_h^2=\langle a_h,a_h\rangle_V.
\]

They must reproduce the already frozen values

\[
R_{\mathrm{out},2h}=\sqrt{U^2/Q_{2h}^2},\qquad
R_{\mathrm{in}}=\sqrt{E^2/Q_h^2}
\]

bit for bit:

```text
R_out,2h 0x3EF7A721405AFAAF
R_in     0x3EF7FB7522398B1F
```

The descriptive geometry is

\[
\cos_V(u,e)=\frac{C}{\sqrt{U^2E^2}},\qquad
\beta=\frac{C}{U^2},
\]

\[
E_\perp^2=E^2-\frac{C^2}{U^2},\qquad
r_\perp=\sqrt{E_\perp^2/U^2}.
\]

In exact arithmetic the identities

\[
V^2=U^2+E^2+2C
\]

and

\[
E^2=\beta^2U^2+E_\perp^2
\]

hold.  The checker reconstructs \(V^2\) and \(E_\perp^2\) directly from their
vectors.  It does not require a bitwise-zero residual against a differently
associated form of either identity: strong cancellation makes such a
requirement dependent on binary64 summation order.  No tolerance is used to
equate the paths.  Negative zero, nonfinite values, nonpositive
\(U^2,E^2,Q_{2h}^2,Q_h^2\), or negative directly accumulated
\(E_\perp^2\) are invalid; no cutoff may replace these exact domain checks.

## Additive localization

For each plane/group block, retain the raw contributions

\[
U_{sg}^2,\ E_{sg}^2,\ V_{sg}^2,\ C_{sg},\
Q_{2h,sg}^2,\ Q_{h,sg}^2.
\]

The only localization quantity is the additive squared-metric difference

\[
\Delta^{(2)}_{sg}
=\frac{E_{sg}^2}{Q_h^2}
-\frac{U_{sg}^2}{Q_{2h}^2},
\]

so that in exact arithmetic

\[
\sum_{s,g}\Delta^{(2)}_{sg}
=R_{\mathrm{in}}^2-R_{\mathrm{out},2h}^2.
\]

The global post-division value, the three-plane fold, and the 370-group fold
have distinct declared binary64 operation orders and need not be bitwise
equal.  The checker reports all 3 plane sums and all 370 group sums, their
signs, and the group with largest absolute contribution.  These are
descriptive coordinates of the already failed component.  There is no
top-\(k\) selection, local ratio, dominance threshold, or causal attribution
to a radial plane or energy group.

Because the frozen case is rank one, each plane/group block contains one
modal coordinate.  No separate mode ranking is needed.  This diagnostic
must not generalize that additive attribution to a future rank greater than
one without explicitly treating Gram cross terms.

## Independent execution requirements

The checker is Ganlib-only and opens all inputs read-only.  A source scan
forbids references to Ganlib mutation routines.  A linked-binary symbol scan
requires `LCMOP` and forbids SPOT/Dragon production solver symbols; it does
not misclassify unused mutation symbols exported by the statically linked
Ganlib archive as checker calls.  Two independent builds, checked `-O0` and
optimized `-O2`, must produce byte-identical output on the frozen inputs.

The result may determine whether the unresolved response is primarily an
update-magnitude or update-direction effect.  It cannot select \(h\) or
\(2h\) as more accurate, authorize replay or Picard iteration, weaken the
Stage-4 rule, or establish physical convergence.
