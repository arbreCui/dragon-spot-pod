# Fixed three-return Picard diagnostic — design only

## Decision

This is a **protocol-only design**.  It authorizes no implementation, no
Dragon process and no transport solve:

```text
status             FROZEN-PROTOCOL-ONLY
governance         NO-GO-UNDER-CURRENT-STAGE4
Dragon processes   0
Stage-4 v2         UNRESOLVED
outer convergence  NOT-EVALUATED
Stage 5            NOT-AUTHORIZED
```

Calling the proposed calculation a census or a diagnostic would not change
the fact that

\[
x^0\longrightarrow x^1\longrightarrow x^2\longrightarrow x^3
\]

is a Picard trajectory beyond one return.  The current validation plan
forbids that execution until Stage 4 is qualified.  This file therefore
freezes only what such a future descriptive experiment would mean.  It does
not weaken or reinterpret the frozen `UNRESOLVED` result.

## Mathematical object

The future experiment would use the existing finite-precision online map
\(G_h^{32}\), with

\[
x^{m}=(a^m,\rho^m,L^m),\qquad \rho^m=1/k^m,
\]

and direct substitution

\[
x^{m+1}:=G_h^{32}(x^m),\qquad m=0,1,2.
\]

There is no relaxation parameter.  Rank, basis, physical inputs, solver
controls and arithmetic route remain fixed.  After \(x^3\) is constructed,
the process stops without evaluating \(G_h^{32}(x^3)\).

Three returns are the minimum length that produces three update magnitudes
and therefore two adjacent comparisons.  That statement concerns only the
amount of descriptive data.  It does not make three returns a convergence
test.

## One online return

Each of the three future map blocks would have to be written explicitly:

```text
canonical current state
  -> SPOPROJ FIXB reconstructs B*a_current
  -> SpotRefFS visits all three radial planes
     -> SPOFSRC freezes F*phi_current/k_current
     -> ASM forms the leakage-coupled radial system
     -> FLU TYPE S solves the radial fixed-source equation online
     -> SPOFCHK records the same-equation radial response
  -> ASM SPOD FIXB rebuilds the radial operator in the unchanged basis
  -> axial FLU returns the next reduced axial field
  -> SPOGBAL and SPOSTATE establish the canonical next state
  -> SPOXCONV records the component-wise raw defect
  -> SPOLEAK closes L_next
```

The complete valid returned state is the only permitted input to the next
block.  An archived \(x^1\) may not be joined to two new returns and called
one online three-return trajectory.

With three planes and three returns, the future process contains exactly
nine radial fixed-source solves and three returned axial solves.  It is a
real transport calculation, not a compile test or synthetic smoke test.
Existing evidence indicates that it would probably take minutes rather than
seconds.  A wall-clock safety limit must therefore be frozen separately
before any execution can be considered.

## Fixed numerical map

The proposed map is the legacy binary32 radial route, not the unimplemented
REAL64 lane:

```text
rank             1
groups           370
radial planes    3
h bits           0x350637bd
MAXOUT           500
MAXINR           740
radial solver    TYPE S + MCCG
REAL64 lane      OFF
```

The initial state is assembled without a transport initializer: read the
frozen basis, axial \(x^0\) and snapshot seed, then reconstruct \(L^0\) once
with `SPOLEAK`.  The first transport solve must therefore belong to the
first declared return.

## Separate measurements

There is no declared norm for the heterogeneous full state
\((a,\rho,L)\).  A single \(D_m=\|x^{m+1}-x^m\|\) would introduce undeclared
cross-component weights and is forbidden.

For each \(m=0,1,2\), save the signed updates

\[
\delta\rho_m=\rho^{m+1}-\rho^m,\qquad
\delta L_m=L^{m+1}-L^m,\qquad
\delta a_m=a^{m+1}-a^m,
\]

and the three separate magnitudes

\[
D_{\rho,m}=|\delta\rho_m|,
\]

\[
D_{L,m}=\|\delta L_m\|_\infty,
\]

\[
D_{a,m}=
\sqrt{\delta a_m^T\,\mathrm{Gram}\,\delta a_m}.
\]

The existing \(R_\rho,R_L,D_L,R_a\) records are retained.  The numerator and
denominator of \(R_L\) and \(R_a\) are also saved so that denominator motion
cannot be mistaken for a smaller update.

Only these exact adjacent relations are reported, component by component:

\[
D_{\bullet,1}\mathrel{\{<,=,>\}}D_{\bullet,0},
\qquad
D_{\bullet,2}\mathrel{\{<,=,>\}}D_{\bullet,1}.
\]

No percentage decrease, ratio threshold, weighted score or aggregate
`PASS/FAIL` is defined.

## Fail-closed boundary

Every radial and returned axial solve must satisfy its existing strict
terminal rule.  Identity, fixed basis, rank, normalization, source,
leakage, positivity, finite-value, balance, Galerkin and archive contracts
remain mandatory.  Existing balance and Galerkin quantities are recorded;
no new magnitude threshold is attached to them.

If any return fails, it is not \(x^{m+1}\), it cannot drive the next block,
and no three-step trend may be reported.  There is no retry, resume,
automatic replay, tolerance change, longer cap or adaptive early stop.

A future complete process could only be labeled
`CENSUS-COMPLETE-DIAGNOSTIC-ONLY`.  An incomplete process is
`CENSUS-INCOMPLETE-NO-SCIENTIFIC-RESULT`.  Both stop immediately and
authorize neither replay, Stage 4, Stage 5 nor a longer trajectory.

Even if every component decreases twice, the allowed statement is only
that the named component decreased on those two finite adjacent
comparisons.  The words `converged`, `diverged`, `contractive`, `stable`,
`qualified` and `pass` are not valid conclusions.

## What would be required before a run

A future run would require three new, explicit decisions:

1. a governance amendment acknowledging that it changes the prior
   no-Picard execution boundary while preserving every frozen result;
2. an implementation freeze binding the explicit three-block deck,
   executable, parser, independent checker, inputs and total wall limit;
3. a separate authorization for one isolated capture process.

None of those decisions is made here.  The machine-readable authority is
[picard_three_return_protocol.json](picard_three_return_protocol.json).
