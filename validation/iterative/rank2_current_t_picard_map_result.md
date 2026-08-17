# Direct Picard map from the latest AA(1) return

Date: 2026-08-17

Classification: `VALID_NOT_MET`.

Standard AA(1) on the then-latest evaluated residuals $s-r$ and $t-p$ was
rejected because its leakage height-$L_2$ and $D_L$ directions increased.
Only after that failure, standard unregularized AA(2) on $r-z$, $s-r$, and
$t-p$ was checked and rejected for the same reason.  Neither affine state
was materialized.

Exactly one direct continuation

\[
t^+=G_2(t)
\]

ran from source commit
`dc7189fd1f6b08ebbae3e3285b18d86fa392b871`.  The complete parent return
$t$ was used unchanged; there was no state mixing, relaxation, damping,
clipping, regularization, empirical coefficient, retry, fallback, or
automatic successor.

| solve | `IEXTF` | `EEXT` | `EUNK` | `EINR` | FLU CPU |
|---|---:|---:|---:|---:|---:|
| radial plane 1 | 5 | `0` | `4.32243922e-7` | `4.04364840e-7` | 18 s |
| radial plane 2 | 6 | `0` | `4.77821686e-7` | `4.21303042e-7` | 22 s |
| radial plane 3 | 11 | `0` | `4.30804448e-7` | `3.07959141e-7` | 28 s |
| axial | 205 | `3.71150638e-10` | `4.68289130e-7` | `4.68289130e-7` | 140 s |

Every strict terminal passed below `4.99999999e-7`; the 120/180-second
limits were process-safety bounds only.  At the unchanged outer AND gate:

| quantity | raw value | tolerance multiple | gate |
|---|---:|---:|---|
| $R_\rho$ | `6.422348086676521e-8` | `0.128447` | pass |
| $R_L$ | `8.609298200966152e-4` | `1721.859640` | fail |
| $R_a$ | `1.895065973245708e-6` | `3.790132` | fail |

The dimensional diagnostic is

\[
D_L=1.261418219655752\times10^{-6}\ \mathrm{cm}^{-1};
\]

it is not part of the dimensionless outer gate.  The preceding evaluated
map was $p\mapsto t$, so $t-p$ and $t^+-t$ are genuinely adjacent
fixed-point residuals.  Relative to $t-p$, $R_L$ and $D_L$ increased by
75.8367%, while $R_a$ decreased by 28.7745%; $R_\rho$ was effectively
unchanged.  These are observed adjacent residual ratios, not proof of an
asymptotic contraction, cycle, convergence, or divergence.

The independent `continued` Ganlib checker passed fixed POD identity, live
radial-operator change, raw radial positivity, canonical layout, bitwise raw
defects, and restart archive.  Global and maximum-group balance diagnostics
were `7.395645e-9` and `1.634258e-3`; they are not stopping defects.

The Git-ignored artifact contains 22 regular files, no symbolic links, and
a passing 21/21 receipt.

| object | SHA-256 |
|---|---|
| parent AX | `e35636e5badd21a5deb02964b995a948ea0df4eb110b7fd2783ef5c41f36145e` |
| parent snapshots | `30240ad9c99de510c04c277a40ce97b162cce2cc364f548268ad66e6570f9435` |
| returned AX | `7620e0a4a7bdfd77e89e83a46c09b5bd66d235c0e9cd0c0c68718a711b96ae3c` |
| returned snapshots | `44ef4eacf25de10818824bb7e3da5cd4022a5a005e832ac1069880a8003ec9cd` |
| receipt | `4eb30a87d765c07abc5bb390528dbe6a2bb9e13801048fbae01e20138c280f20` |

This is a valid physical map, not a converged fixed point and not an
inner-solver failure.  No retry or successor was started.
