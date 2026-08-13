# Three-update direct Picard census

This records the final predeclared short-census update

\[
x_3=G(x_2).
\]

It completes the current three-update observation. No fourth update was run.

## Frozen parent and controls

The input was the hash-locked accepted `iterative-map2-current` state. The
source commit before adding this continuation was `5c3865b`, and the Dragon
SHA-256 remained
`dabc549461c401a5d5806753b4cfd0db627e2def61f1938aceaf2432c3762e28`.

Rank remained one in all 370 groups and the inner tolerance remained
\(5\times10^{-7}\). There was no relaxation, damping, fitting, clipping,
parameter change or automatic retry.

The calculation contained exactly three new radial fixed-source solves,
fixed-basis response assembly and one returned axial solve. The radial and
axial Dragon processes used 60 and 48 CPU seconds, respectively. Each had a
75 s process timeout followed, only on timeout, by at most 5 s of TERM grace.

## Strict inner termination

The radial solves reached their strict predicates after 3, 21 and 19 outer
iterations. The axial solve reached its strict predicate after 140 outer
iterations. All four reported `EUNK-VALID=1`, `STATE=1`, `IGDEB=371`, and
residuals no greater than the declared tolerance. Dragon ended normally in
both processes.

## Three-update trajectory

The independently checked third defect is

\[
\begin{aligned}
R_{\rho,3} &= 0,\\
R_{L,3}    &= 4.324867328124437\times10^{-4},\\
D_{L,3}    &= 6.341142579913139\times10^{-7},\\
R_{a,3}    &= 2.325209380436949\times10^{-6}.
\end{aligned}
\]

| update | \(R_\rho\) | \(R_L\) | \(D_L\) | \(R_a\) |
|---|---:|---:|---:|---:|
| \(x_0\to x_1\) | \(1.281155\times10^{-6}\) | \(7.922853\times10^{-4}\) | \(1.161650\times10^{-6}\) | \(9.228256\times10^{-7}\) |
| \(x_1\to x_2\) | \(0\) | \(3.956456\times10^{-4}\) | \(5.800975\times10^{-7}\) | \(7.237784\times10^{-7}\) |
| \(x_2\to x_3\) | \(0\) | \(4.324867\times10^{-4}\) | \(6.341143\times10^{-7}\) | \(2.325209\times10^{-6}\) |

From the second to the third update, \(R_L\) and \(D_L\) increased by a
factor of 1.09312 and \(R_a\) increased by a factor of 3.21260. The inverse
eigenvalue defect remained zero at the stored binary32 eigenvalue precision.

Therefore the observed direct-Picard trajectory is not monotonically
decreasing. These three updates do not establish whether the rise is caused
by a noncontractive/oscillatory map component or by the inexact-inner-solve
floor. The magnitudes of \(D_L\) and the inner stopping tolerance are similar,
but they are different quantities, so that observation is not an error bound.
No contraction factor is fitted and no convergence claim is made.

The global balance norm was \(3.443536\times10^{-9}\). The separately
reported maximum Galerkin diagnostic was \(5.84892\times10^{-7}\); it is not
used as an empirical acceptance factor.

## Independent check and artifacts

The Ganlib-only continuation checker passed the fixed POD package, live
radial response, positive radial flux, canonical layout, independently
recomputed raw defect and restart-archive time ordering. It confirmed that
the radial solve used \(k_2,L_2\) and that the returned archive contains
\(L_3\).

The accepted local evidence is hash-frozen under
`validation/artifacts/iterative-map3-current`:

```text
618c783a17482dfc6455cfca988f987bd4979a8b6e35b691ab1767166123f7c6  radial.log
5b2b3802c6d286d478eae1d532d99c08bb2fe65b1a08376070b5a86a731aec02  axial.log
d7567e86430436e3008d92bb1c97cc4ee3b610cb89b313a2dd9b62ea010fc0d6  state3_system.xsm
32cac2cc7d97272bf98a9a6b58c481676fb9fc0fcdb9d3034a4ecd214c069404  state3_axial.xsm
83bf149a153ad0a463f0af519e72b8043a8f0edfd0dfe672bab3faac4819f888  state3_snapshots.xsm
```

## Boundary

The three-update census is complete. A valid \(x_3\) exists, but it is not
accepted as a fixed point. Blind continuation to \(x_4\) is not justified by
this census.
