# One direct Picard successor after the rolling AA(2) map

Date: 2026-08-16

Status: `PREPARED_NOT_RUN`.

Let

\[
y=x_{\mathrm{rAA2}}^+=G_2(x_{\mathrm{rAA2}}).
\]

This default-off stage is limited to exactly one direct Picard successor

\[
z=G_2(y).
\]

The parent is the complete valid returned AX/snapshot state from the preceding
map. No state is selected by a combined norm, and no affine proposal or mixed
raw carrier is constructed. The unchanged host consumes \(y\) directly,
reconstructs each radial field in the same fixed rank-two space, uses the
parent eigenvalue in the frozen-fission source, performs three online radial
fixed-source solves and then one axial solve.

The POD package, rank two, normalization, physical decks, strict inner
terminals and three-component outer gate remain unchanged at

\[
\varepsilon=5\times10^{-7}.
\]

The 120-second radial and 420-second axial limits are operational process
bounds, not physical or convergence parameters. The wrapper is default-off.
The preceding map receipt and six parent hashes must pass before either Dragon
invocation; the independent continued-state Ganlib check must pass before
publication to the dedicated sibling result artifact. One activation permits
one attempt and no retry, relaxation, damping, Anderson mixing, clipping,
fitted closure, regularization, pseudoinverse, fallback or empirical
coefficient.

Only three classifications are allowed:

- `INVALID_MAP`: a strict solve terminal, physical value, provenance check,
  fixed-basis check, independent audit or receipt fails; no candidate is
  published.
- `TOLERANCE_MET`: the map is valid and $R_\rho$, $R_L$ and $R_a$ all
  satisfy the unchanged tolerance.
- `VALID_NOT_MET`: the map is valid but at least one stopping defect exceeds
  the tolerance.

The dimensional leakage change and balances remain diagnostics. One map
cannot establish asymptotic convergence, stability, contraction, convergence
order, rank adequacy or physical accuracy, and it starts no successor
proposal or map. Preparing this host performs no Dragon, assembly, transport
or Picard calculation and produces no map result.
