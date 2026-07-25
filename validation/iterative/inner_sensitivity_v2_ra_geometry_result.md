# Stage-4 v2 axial-state geometry result

## Result

The committed read-only diagnostic `6256bd9652fa46635fb21c37bebe30971b4ffc62`
reproduced the frozen \(R_a\) bits with two byte-identical builds.  It read
the three existing axial XSM states and ran no Dragon process.

Let

\[
u=a_{2h}-a_0,\qquad e=a_h-a_{2h},\qquad v=a_h-a_0.
\]

The stored POD Gram/height metric gives

\[
\|u\|_V=1.5057597483342492\times10^{-5},
\]

\[
\|e\|_V=1.5267299827710861\times10^{-5},
\qquad
\|v\|_V=6.1601563962267794\times10^{-7}.
\]

Their geometry is

\[
\cos_V(u,e)=-0.9992702991313999,
\qquad
\frac{\langle u,e\rangle_V}{\|u\|_V^2}
=-1.0131868169967067,
\]

and the component of \(e\) orthogonal to \(u\) has norm

\[
\frac{\|e-\beta u\|_V}{\|u\|_V}
=0.0387270788552574.
\]

Thus the change caused by tightening the radial inner tolerance from \(2h\)
to \(h\) is almost antiparallel to, and slightly larger along the same
direction than, the coarse axial POD update.  The small fine-map update
\(v=u+e\) is largely a cancellation of those two much larger vectors.

This explains the frozen ordering

\[
R_{\mathrm{in}}
=2.2871261661792861\times10^{-5}
>
R_{\mathrm{out},2h}
=2.2557116628569681\times10^{-5}.
\]

The result is not a new convergence test.  It geometrically explains why
the existing exact Stage-4 test returned `UNRESOLVED`.

## Localization

The additive squared-metric excess

\[
R_{\mathrm{in}}^2-R_{\mathrm{out},2h}^2
\]

has the following plane contributions:

| axial plane | \(\Delta^{(2)}\) |
|---|---:|
| 1 | \(-1.2454884621508295\times10^{-12}\) |
| 2 | \(-4.7079030995933044\times10^{-13}\) |
| 3 | \(+1.5987378179411575\times10^{-11}\) |

The positive net excess appears in plane 3 after negative contributions
from planes 1 and 2.  This locates where the returned axial state displays
the sensitivity; it does not establish that the plane-3 radial solve caused
it.

Across energy groups, 328 contributions are positive and 42 are negative.
The largest absolute contribution is group 80,
\(3.7888761758829870\times10^{-13}\).  This is a broad signed decomposition,
not a group-selection rule.

The four reported binary64 folds differ by a few final bits because the
strongly cancelling sums have different declared association orders:

```text
post division  0x3DAF61EA2CD57AC0
cell fold      0x3DAF61EA2CD57B76
plane fold     0x3DAF61EA2CD57B6C
group fold     0x3DAF61EA2CD57B6D
```

No tolerance is used to equate them.

## Physical boundary

The earlier capture passed strict radial/axial termination, raw scalar-flux
positivity, independent source reconstruction, leakage, layout, and the
declared balance checks.  The frozen classification was triggered by
\(R_a\); no negative-flux marker or balance-checker failure was observed.
Because those balance diagnostics had no magnitude acceptance threshold,
this geometry diagnostic does not itself prove conservation accuracy or
rule out a separate conservation error.  It does not invalidate the SPOD
equations.

The fixed case is rank one, so every plane/group block has only one retained
modal coordinate.  The result neither proves rank one sufficient nor
justifies a rank change.

The frozen boundaries remain:

```text
CAPTURE UNRESOLVED
REPLAY NOT-AUTHORIZED
OUTER-CONVERGENCE NOT-EVALUATED
CLASSIFICATION-CHANGE NONE
```

No second capture, replay, tolerance search, relaxation, empirical
coefficient, or Picard trajectory is authorized.  If the project retains
the iterative objective, the next scientific route must be separately
frozen: improve the verifiability of the radial inner solve, for example
with a complete working-precision lane or an independent equation-residual
criterion, and then restart Stage 4.  This diagnostic does not choose
between those future methods.

The compact machine record is
[`inner_sensitivity_v2_ra_geometry_result.txt`](inner_sensitivity_v2_ra_geometry_result.txt).
The tracked
[`result receipt`](inner_sensitivity_v2_ra_geometry_result_receipt.sha256)
binds this record, the frozen implementation, the parent capture result, and
the three local XSM inputs.  Verifying its final three rows requires the
ignored local artifacts.
