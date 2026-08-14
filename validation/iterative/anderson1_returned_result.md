# One nonlinear evaluation of the leakage-Anderson trial

The single predeclared leakage-driven Anderson(1) trial was evaluated once
through the real fixed-space SPOD map. This was one bounded point evaluation

\[
x_R=G(x_A),
\]

not an additional fitted model and not an outer iteration loop. The fixed
rank remained one, every radial and axial solve used
`5.0e-7`, and no relaxation, clipping, floor, calibration, or retry was
introduced.

The three radial fixed-source solves and the axial eigenvalue solve each
reached their strict inner and outer terminal branches. Both Dragon processes
ended normally. A Ganlib-only checker then independently verified the trial
publication, fixed POD bundle, returned state contract, four raw defects,
restart leakage, fixed-source metadata, and strict positivity of every keyed
raw radial scalar flux.

## Result

The independently reproduced raw defect is

\[
(R_\rho,R_L,D_L,R_a)=
(6.405763486316829\times10^{-8},
 2.445892032823307\times10^{-4},
 3.586173988878727\times10^{-7}\ {\rm cm}^{-1},
 1.129218064658488\times10^{-6}).
\]

With the unchanged `5e-7` outer gate, only \(R_\rho\) passes. \(R_L\) and
\(R_a\) fail, so \(x_R\ne x_A\) at the declared tolerance and outer
convergence is not established. (D_L) is dimensional and remains a
reported diagnostic, not a fourth stop condition.

Relative to the preceding direct result \(x_6=G(x_5)\), \(R_L\) and \(D_L\)
increase by `16.7962%`, while \(R_a\) increases by `48.9029%`. The actual
nonlinear map therefore did not realize the reduction predicted by the
two-residual affine screen. This rejects this one leakage-Anderson candidate
as an improving accepted iterate. It does not prove that Anderson methods are
generally invalid, that direct Picard diverges, that rank one is adequate, or
that the transport solution is physically accurate.

No \(x_7\), second coefficient, second activation, or retry was run.

## Evidence

The local artifact directory is
`validation/artifacts/iterative-anderson1-returned-120-80s`. Its manifest
passes `shasum -a 256 -c scientific.sha256`. The small repository receipt
`anderson1_returned_scientific.sha256` freezes the runner, decks, checker,
the two copied SPOT fixed-source procedures, logs, and returned objects. The
receipt is a result-and-source integrity record; it does not freeze the full
compiler, Ganlib, or linked Dragon toolchain. The Dragon executable hash was
`61673fa6ec3a2cbf25aa7ddfbda8acc5339c3392fd4888b9d9bb45e3ca1e0001`.

`run_anderson1_map_once.sh` remains default-off. Its successful activation
used a 120 s radial bound and an 80 s axial bound, with at most 5 s process
cleanup after either bound and no retry.
