# Minimal actual-temperature Fe56 reference — completed and independently reviewed

## Execution update, 2026-09-29

The user explicitly approved this 600-second attempt. Started at
2026-09-29T12:27:03.760383 UTC (20:27:03 Beijing); hard deadline
12:37:03.760383 UTC. Run directory:
`validation/artifacts/d4a-fe56-actual-temperature-run-20260929/`.
No retries, TONE, transport, Picard, CE or production replacement. The
preparation/authorization-wait language below records the original proposal.

Processing and first checks finished in 313.425 seconds; independent review
finished at 12:32:46.281751 UTC, 342.521 seconds after start, within the original
budget. All 645 common-control records match exactly. Direct P0 has no negative
entries at the two new temperatures, whereas cubic interpolation has 637/206;
linear interpolation is nonnegative but has 9.72/11.53 times the unweighted
P0 matrix error of cubic in G282–370. See [result](actual_temperature_reference_result.md).
No production replacement or follow-on calculation was started.

## Why this next, 2026-09-29

The completed first-order LIBDRA material comparison removes the reproduced
negative Fe56 P0 values, but does not establish interpolation accuracy. The
matched original library and corrected MT51 candidate both have only five
temperatures: 293, 550, 900, 1200 and 2000 K. The inspected Dragon-project
Fe56 P3 run has the same five temperatures and a different library lineage;
it cannot serve as a direct D4 actual-temperature reference.

Add only the two Fe56 temperatures used by the saved material, **748.1500244140625
and 893.1500244140625 K**, to the original five-node table. Keep the five original
nodes in the same run as controls. They must reproduce the corrected candidate's
same-temperature physical records; a mismatch stops qualification rather than
being covered by a newly selected tolerance.

## Scope and unchanged physics

Reuse `d4a-fe56-mt51-control-candidate-20260929/candidate/build/fe56_njoy` and
its pinned private `libnjoy.dylib`; no recompilation or production replacement.
Its only processing-source change remains the previously verified MF6/MT51
finite-dilution fix. Use the original Fe56 ENDF evaluation and the original
RECONR → BROADR → PURR → THERMR → GROUPR → DRAGR settings. Changes to the decks
are restricted to seven rather than five temperatures, the two actual values,
and the corresponding repeated GROUPR reaction cards. The DRAGR deck is unchanged.

Original BROADR has restart=0, bootstrap=0, starting T=0: each final temperature
is independently broadened from the same zero-temperature reconstruction.
This is confirmed by both the cached source documentation and the original run
log, not an assumption that adding temperatures preserves a bootstrap history.
Original Fe56 PURR reports no unresolved parameters and copies through; retain
that original stage instead of inventing a different processing route.
Keep 370 groups, P0/P1, ten dilutions, reconstruction/broadening/thermal errors,
weighting spectrum, thermal treatment, resonance limits and DRAGR compression.
No fitting, negative clipping, scalar normalization or new physical threshold.

## Evidence to obtain

1. Normal processing termination and unchanged input/executable identities.
2. Same-temperature control agreement at the five original nodes; compare
   decoded REAL32 numerical bit patterns and exact structural fields within
   matching temperature subtrees, not root temperature-count metadata.
3. At each new temperature, compare the direct processed P0/P1 matrices and
   reaction data against the existing one-/three-order sqrt(T) interpolation.
   The first clean interpolation test is infinite-dilution G282–370, where the
   earlier saved-data replay proved the temperature-only origin of negative P0.
   Report full-group and finite-dilution observations separately; do not pretend
   this is a new self-consistent TONE solution.

Report element/column errors and signs; do not invent a pass threshold from the
observed error. This is a necessary Fe56 data reference, **not qualification of
first-order interpolation for all 59 material entries**, a new SPOD eigenvalue,
a CE accuracy result or full-core validation.

## Proposed single budget: 600 seconds, awaiting explicit approval

One run in a new private directory, 600 seconds total including comparisons,
with 120 seconds reserved for checking. No retry or follow-on material/transport.
Budget evidence: the original five-temperature PENDF log ends at 15.3 CPU seconds;
the corrected candidate's last five-temperature GROUPR and DRAGR stages took
17.217 and 90.100 wall seconds. Seven temperatures should be a small extension,
but those old measurements are not a guarantee. Enforce the shared deadline.

No TONE, ASM, FLU, snapshot, Picard, CE, additional nuclide or runtime/library
replacement is in scope. Use the existing bounded process-group supervision;
do not introduce a new runner framework. Preserve failure evidence if any
input, control, format, processing or deadline check fails.

Static deck preparation:
`validation/artifacts/d4a-fe56-actual-temperature-prepared-20260929/`.
These files have not been executed. The previous 900-second material approval
has been used and does not authorize this new nuclear-data processing attempt.
If a later material comparison is separately approved, preserve its full
MICROLIB once, so fuel-mixture rounding can be replayed without another run.
