# Rank-two REAL64 fifth standard AA(1) map

Date: 2026-08-18

Status: `VALID_NOT_MET`; next `AA1_DIRECTION_FAIL_NOT_MATERIALIZED`.

Using the genuine map pairs `r -> b` and `c -> d`, the standard
unregularized full-Gram AA(1) proposal is

\[
e=0.460187880181553877\,b+
  0.539812119818446123\,d.
\]

Its three parameter-free direction ratios are
`(0.924823979667296014, 0.544585032932459967,
0.532005871126909557)`, all strictly below one.  It was independently
materialized in the fixed rank-two POD space through the carrier-exact
`--next-r64-bd-screened` hosts, with 8880/8880 positive published
scalar-flux values and a passing `RETURNED/10` carrier and
authority-strip audit.  AA(2) was not used.

Exactly one bounded physical map completed without retry through
`PROPOSAL -> PROJECTED/11 -> RETURNED/11 -> CLOSED/11`.  The radial stage
completed in 21.17 s and the warm axial stage in 13.28 s, each under a
30 s hard bound.  Its independently reproduced raw defect is

\[
(R_\rho,R_L,D_L,R_a)=
(6.4223469764534968\times10^{-8},
 2.0797217948011009\times10^{-5},
 3.0471710488200188\times10^{-8}\ {\rm cm}^{-1},
 1.2406359355142729\times10^{-7}).
\]

At the unchanged `5e-7` AND gate, `Rrho` and `Ra` pass; only `RL` fails,
at about 41.6 gate multiples.  `Ra` is again the smallest modal defect of
the REAL64 track.  `RL` recovered by a factor of about 2.31 from the
preceding overshot AA(1) map but remains far above the level of the
direct map `b`.  Together with the preceding step, this is a second local
observation that the same-coefficient affine leakage screen does not
control the mapped leakage response at amplitudes near and below
`3e-6`.  The map is physically valid but rank two is not converged.

No relaxation, damping, clipping, fitting, regularization, empirical
coefficient, fallback, dynamic rank, or model correction was introduced.

The following standard AA(1), using only `d-c,f-e` (audited through the
carrier-exact `--rank2-aa1-df-history` host, whose log labels map
`QY:=c, Z:=d, QT:=e, U:=f`), gives the direction
`g = 0.433581743451667556 d + 0.566418256548332444 f` with ratios
`(0.937704801608836513, 1.40554725551774284, 1.56734191836560144)`.
Both same-coefficient leakage ratios exceed one, so the existing
componentwise, no-leakage-fit screen rejects this direction.  No proposal
was materialized, no successor map was started, and no standard r64 AA(2)
host exists.  The parameter-free fallback is one direct CONT map from
`CLOSED/11`, which was not started.

The complete receipt is frozen under
`validation/artifacts/iterative-rank2-h2-r64-aa1-d-map/`.
