# Passive GMRES activity gate

The next SPOT experiment is not yet a precision experiment. It first asks
one exact structural question:

> Does the frozen one-map MCCG path execute any nonzero-\(K\) GMRES
> correction?

The released RAW-MOC evidence proves that the first primary transport
evaluation was reached. It does not contain the affine-RHS calls, Krylov
calls, correction-block count, or per-group `KMAX`. Therefore an
`UPDATE64` comparison performed now could be empty: both arms could agree
only because the proposed update was never executed.

## Minimal observable

For every existing `MCGFL1` call, the audit copies only integer control
state:

- its role: primary, affine RHS, or Krylov;
- its GMRES call, event, block, and global-iteration indexes;
- the 370-entry \(0/1\) `NCONV` mask.

For every correction block it also copies the block-entry `NCONV` mask and
the completed 370-entry `KMAX` vector immediately before the unchanged
`PHIIN` update.

The independent closure is especially simple. For block \(b\) and physical
group \(g\),

\[
K_{b,g}
=
\sum_{\substack{e\ \mathrm{is\ Krylov}\\e\ \mathrm{belongs\ to}\ b}}
m_{e,g},
\qquad m_{e,g}\in\{0,1\}.
\]

Thus every stored per-group `KMAX` is reconstructed from the raw Krylov
activity masks. The first Krylov mask must equal the block-entry mask, and
later masks may only change from \(1\) to \(0\). Histograms, sums, maxima,
role counts, and active-group sums are derived consequences, not trusted
writer summaries.

No residual norm, tolerance comparison, fitted factor, relaxation
coefficient, clipping rule, or model term is added.

## Frozen numerical controls

The two iteration levels are deliberately kept distinct:

- FLU one-map controls: `MAXOUT=1`, `MAXINR=740`, and binary32
  `EPSOUT=EPSUNK=EPSINR=2.5E-7`;
- MCGMRE controls read from the frozen TRACK:
  `MAXI=20`, `MAXIT=19`, `KRYL=10`, and binary32
  `ERRTOL=EPSI=1.0E-5` with bits `3727C5AC`.

The latter values, not FLU `MAXINR`, bound the correction activity being
measured.

## Exact decision

There is no numerical threshold.

- If all contracts pass and at least one \(K_{b,g}>0\), classify the census
  as `VALID-GMRES-UPDATE-ACTIVE`. The next step is to freeze, but not
  automatically run, the narrow GMRES correction-accumulation precision
  A/B.
- If all contracts pass and every \(K_{b,g}=0\), classify it as
  `VALID-GMRES-UPDATE-INACTIVE`. The empty update experiment is abandoned;
  the next candidate is the always-executed `MCGFCS` source arithmetic.
- Any identity, path, reproducibility, or evidence failure is `INVALID`.

Neither valid result explains the earlier nontermination or establishes
Stage 4 convergence.

## Isolation and current status

The tracked production `src/` tree remains byte-identical to commit
`4d7abb23ac7975d4146beaa3b0049e36cdad8776`. Implementation will use a
clean archive of that commit plus a validation-only overlay. The new
standalone `GMRA` keyword will be default off and valid only together with
`MOCA 2`; it writes a sibling `SPOT-GMR-AUD` directory and leaves the
frozen `SPOMOC.f90` and `SPOT-MOC-AUD` contract unchanged.

The two allowed `GMRA` log edits preserve CLE-2000's fixed 120-column
source field: each ` MOCA 2 GMRA ;` token is replaced by
` MOCA 2 ;     `. The five restored spaces are formatting closure, not a
scientific normalization.

## Version-2 evidence amendment

The first authorized attempt at commit
`eb891486e466a3ad30be46f70a97384272ca84ab` ran only OFF. Its full-log
comparison stopped at character 9668 on line 126, before either ON process
or any GMRES ledger was observed. The failed work tree, lock and candidate
artifact were deleted as required. No raw failed-run bytes or hash were
retained, so that attempt remains `INVALID-NO-SCIENTIFIC-RESULT` and cannot
be reused or reclassified.

The differing field belongs to the pre-existing `KDRDRV` module-completion
receipt. `KDRDRV` samples `KDRCPU` and `KDRMEM` around `FLU` and only prints
the differences after `FLU` returns; they do not enter the transport state
or a convergence test. The top-level `cle2000_c` timer is likewise printed
after procedure execution. Version 2 therefore normalizes only these exact
runtime fields, in addition to the two already declared `FLU2DR` CPU
fields:

- exactly one ordered `-->>MODULE FLU:` receipt, with a nonnegative
  13-column `F13.3` time field and a nonnegative 10-column `1P,E10.3`
  memory field, replaced by the equal-width markers `<MODULE-TIME>` and
  `<MEM-TELE>`;
- exactly one ordered `cle2000_c: cpu time= <nonnegative %.2f> second`
  receipt, with only its numeric field replaced by `<CLE-CPU>`.

The raw logs remain unmodified. Missing, duplicate, reordered, malformed or
forged telemetry records fail closed, and every other log byte remains part
of the exact comparison. This amendment changes neither an equation nor a
solver parameter and introduces no tolerance. It also does not authorize an
automatic retry.

The protocol is frozen in
[gmres_activity_protocol.json](gmres_activity_protocol.json), and its
fail-closed static checker is
[check_gmres_activity_protocol.py](check_gmres_activity_protocol.py).

This method freeze authorizes only implementation and no-transport
synthetic tests. The version-1 attempt executed only OFF and remains
invalid. No additional Dragon process has been run under the version-2
amendment; a retry requires a new committed version-2 run/publication
freeze and renewed explicit authorization before `RUN_GMRES_ACTIVITY=1`.
