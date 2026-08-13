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
by the map itself or by the inexact-inner-solve floor. In particular,
\(D_L\) is a dimensional leakage difference, whereas
the inner stopping tolerance is a normalized successive-iterate gate. They
cannot be compared numerically, and the inner gate is not a state-error bound.
No contraction factor is fitted and no convergence claim is made.

## Frozen update-direction diagnostic

After the census, a Ganlib-only checker read the hash-locked \(x_1,x_2,x_3\)
states without calling Dragon or evaluating another map. It first confirmed
the fixed canonical layout, basis, Gram matrices and plane heights bit for
bit, then independently reproduced the saved \(x_1\to x_2\) and
\(x_2\to x_3\) defects bit for bit.

For the modal increments

\[
d_{12}^a=a_2-a_1,\qquad d_{23}^a=a_3-a_2,
\]

the checker used the already-defined fixed-space metric

\[
\langle u,v\rangle_{HG}
=\sum_{g,s}H_s u_{s,g}^{T}M_gv_{s,g}.
\]

It obtained

\[
\cos_{HG}(d_{12}^a,d_{23}^a)=-0.888850884278291,
\qquad
\frac{\|d_{23}^a\|_{HG}}{\|d_{12}^a\|_{HG}}
=3.212598682168675.
\]

Thus the two stored modal increments form an obtuse angle and the second is
larger in the production modal norm. This is a signed geometric observation
about the frozen canonical states; it does not prove a two-cycle, divergence,
or a physical oscillatory mode.

For leakage, the production diagnostic remains
\(D_L=\|\Delta L\|_\infty\), whose successive ratio is
\(1.093116596427855\). A separate height-weighted \(L_2\) diagnostic used

\[
\langle u,v\rangle_H=\sum_{s,g}H_su_{s,g}v_{s,g}
\]

and gave

\[
\cos_H(d_{12}^L,d_{23}^L)=-0.154123132217496,
\qquad
\frac{\|d_{23}^L\|_H}{\|d_{12}^L\|_H}
=0.735710432283278.
\]

This leakage angle is explicitly non-production: it supplies signed geometry
but does not replace \(D_L\). The two \(\rho\) increments are both exactly
zero at the stored precision, so their direction is undefined. No combined
angle is formed from \((a,\rho,L)\), whose components have different units
and metrics.

The current evidence therefore remains
`INNER-ERROR-BOUND NOT-AVAILABLE`,
`PHYSICAL-VS-NUMERICAL-CAUSE UNRESOLVED`, and
`OUTER-CONVERGENCE NOT-ESTABLISHED`. The short read-only reproduction is

```sh
sh validation/iterative/run_picard_direction_check.sh
```

## Bounded refined attempts from x2

Two separately authorized radial attempts toward \(G_{h/2}(x_2)\), with
\(h/2=2.5\times10^{-7}\), were made from the unchanged hash-locked \(x_2\).
Relative to the accepted map-3 decks, only the common radial and axial solver
tolerance was halved; the basis, rank, physical inputs, iteration caps and
direct update were unchanged. There was no relaxation or automatic retry.

The first radial process reached its 75 s bound. A later, explicitly
authorized process used the identical deck and inputs with a 120 s bound.
Both raw logs ended immediately after the first-plane `ASM` step, before any
`FLU2DR-TERM` record; neither has a normal-end marker or returned scientific
XSM state. A later verbose trace established that this logged endpoint did
not mean the process remained in `ASM`: the first-plane FLU solve was active
but its normal `EDIT 0` mode emitted no progress records. The axial process
was never started. The raw-log SHA-256 values are

```text
c79e5fc514df1fb4f06bfc8b35fa380687ab8240d34e24b88c1ad523e3a6c1dd  radial.log
9fa072e8f9415c6dafa0ea9b06435632890ebc39d74c425551e86b360c324f1c  radial_120s.log
```

They are retained locally under
`validation/artifacts/x2-half-timeouts/`.

The one 30 s diagnostic trace changed only the temporary FLU print level from
`EDIT 0` to `EDIT 1` and enabled unbuffered output. It recorded 27 completed
outer iterations and 35 inner-iteration records in the first plane. The
printed outer flux residual did not decrease monotonically: it reached
\(2.49\times10^{-7}\) at outer iteration 23, just below the printed
\(2.50\times10^{-7}\) target, while the corresponding inner flux residual
was \(3.46\times10^{-7}\) and its first unconverged group was
\(2.62\times10^{-7}\). The outer residual then rose again and was
\(1.35\times10^{-6}\) at iteration 27. Thus the strict inner and outer gates
were never simultaneously satisfied in the observed interval. The trace has
SHA-256
`45e8d191cdc7a76da8a84f88cb9842407466054f21f9c6383db0b00c20934a3b`
and is retained as `trace_30s.log` in the same local directory.

A matched 30 s trace then disabled variational acceleration with the standard
FLU control `ACCE 3 0`; with zero accelerated iterations, neither the inner
nor outer `FLU2AC` branch is entered. No physical input, tolerance,
rebalancing rule or termination gate changed. This trace completed 25 outer
iterations. Its printed outer residual also rebounded, with a best observed
value of (5.17\times10^{-7}) and a final value of
\(1.82\times10^{-6}\), both above the target. The corresponding accelerated
trace completed 27 iterations, reached a best value of
\(2.49\times10^{-7}\), and ended at \(1.35\times10^{-6}\).

Therefore disabling `FLU2AC` did not remove the observed rebound and does not
support blaming variational acceleration as its sole cause. The fixed-time
traces contain different iteration counts, so they do not establish that
either iteration scheme is asymptotically better. The no-acceleration log has
SHA-256
`594ab1bced1c401b6f315c36479f78128fe1f0fa6dbaab2384356e6cfc9b0a5e`
and is retained as `trace_noacc_30s.log` in the same local directory.

This outcome is `TIMEOUT / NO SCIENTIFIC RESULT`. Because the process did not
reach even the first inner-solver terminal record, it is not evidence that
the \(h/2\) equations converge or fail to converge. It adds no information
about the cause of the stored update reversal and does not prove asymptotic
stagnation, but it rules out an inactive/hung first-plane calculation and
variational acceleration as the unique explanation for the observed
rebound. It does not change the outer-convergence classification. No further
attempt was made.

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
