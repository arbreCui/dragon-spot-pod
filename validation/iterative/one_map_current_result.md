# Current one-map result

This records one evaluation of

\[
x_1=G(x_0)
\]

with the current SPOT source. It is evidence for one map, not for outer
convergence.

## Fixed input and execution

- source commit before adding this bounded driver:
  `84fe028bafab6f03a6f3757fd64d6fe13fb96f4a`;
- Dragon SHA-256:
  `dabc549461c401a5d5806753b4cfd0db627e2def61f1938aceaf2432c3762e28`;
- fixed-basis SHA-256:
  `dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504`;
- fixed-state \(x_0\) SHA-256:
  `0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb`;
- rank: 1 in each of 370 groups;
- inner tolerance: \(5\times10^{-7}\);
- relaxation, fitting, clipping and empirical coupling parameters: absent.

The calculation was split only at the physical 2D/1D interface so each
process had a 75 s solve timeout followed, only on timeout, by at most 5 s of
TERM grace before KILL:

- three online radial fixed-source solves: 57 CPU s;
- one returned axial eigenvalue solve: 47 CPU s;
- automatic retries and parameter changes: zero.

The radial output was passed directly to the axial process. No B2 or REAL64
lifecycle path was used.

## Strict inner termination

The three radial solves terminated after 27, 6 and 2 outer iterations. The
returned axial solve terminated after 135 outer iterations. All four records
reported:

```text
EUNK-VALID=1
STATE=1
IGDEB=371
```

and their eigenvalue, flux and thermal residuals were no greater than the
declared \(5\times10^{-7}\) tolerance. Each radial solution had positive
active scalar flux and a nonnegative, nonzero frozen fission source.

## Raw map defect

\[
\begin{aligned}
R_\rho &= 1.281154825449882\times10^{-6},\\
R_L    &= 7.922853157695863\times10^{-4},\\
D_L    &= 1.161650288850069\times10^{-6},\\
R_a    &= 9.228255841281554\times10^{-7}.
\end{aligned}
\]

The returned eigenvalue is

\[
k_1=1.3641735315322876.
\]

The reported global balance norm is \(3.606202\times10^{-9}\), and the
separately reported maximum Galerkin diagnostic is \(5.91575\times10^{-7}\).
Neither diagnostic is converted into an empirical acceptance coefficient.

## Independent checks

The Ganlib-only checker passed:

```text
POD-PACKAGE BITWISE PASS
RADIAL-OP LIVE-CHANGE PASS
RAW-RADIAL-POSITIVITY PASS
CANONICAL-LAYOUT BITWISE PASS
RAW-DEFECT BITWISE PASS
RESTART-ARCHIVE BITWISE PASS
```

The current `state1_system.xsm` and `state1_axial.xsm` reproduce the
frozen reference containers byte for byte:

```text
fa693cbcc8a60f64521f6ad5be660c8d13414586f03da91506a01021ed5981c2
2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
```

The split-run snapshot container has SHA-256
`64c035cbfd93e54fd29f6d00bc217daa95c64eeffc33c8950ff9cb60585f5bc6`.
Its whole-file hash differs from the earlier single-process serialization, so
whole-container identity is not claimed. Its physical restart records pass
the independent bitwise checker above.

## Development-run note

An initial axial launch reached strict solver termination but its postsolve
GREP failed because two diagnostic holders in the new deck were declared
`DOUBLE` instead of the required `REAL`. A subsequent launch was rejected
before FLU by a leftover CLE object file. After correcting the declaration,
the accepted axial run used a fresh directory and the unchanged radial
output, rank and tolerance. Neither failed launch supplied a scientific
result.

## Boundary

One current, deterministic map evaluation passes. This does not establish
that repeated direct Picard updates converge.
