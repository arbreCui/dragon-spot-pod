# Strict-LEAK1D64 rank-2 clean replay

## Decision

`VALID_MET`.

The corrected fixed-rank-two 2D/1D SPOD map satisfies the original outer
gate and is reproducible from an isolated source baseline.  No empirical
coefficient, relaxation parameter, rank change, gate change or added model
term was used.

## 1. Source isolation

The replay started from detached commit
`6aa91c571b09ce349ced30a5fc5bae6d6c9080c2` and applied the exact 12-file
patch with SHA-256
`60e1514040ae651ae99e9afb3a59397699f2a9f2c148755f6f29be4b12bce6ba`.
The unrelated local `SPOPHYS:` dispatcher change was excluded.

The clean link exposed a repository closure defect: tracked `KDRDRV.F`
already calls `MGXEXP`, `SPOLIB` and `SPORATE`, while their sources were
ignored.  Their exact existing sources were included in the replay and are
now unignored for publication.  This changes source availability, not the
iterative physical operator; the two physical decks call none of those
three modules.

The clean Dragon SHA-256 is
`665c5b4a38a319696503ff9d165fa1205e216591bae78a2876f97487c807a82a`.

## 2. One zero-retry replay

Exactly one radial run and one axial run were made, each with an 80 s hard
limit.  Both ended normally; no physical retry occurred.

- radial time: 69 s;
- axial time: 15 s;
- projected/returned `LEAK1D64` mismatches: 0;
- returned REAL64/REAL32 mirror mismatches: 0;
- production RETURNED admission: pass;
- independent one-map checker: pass;
- no-transport close: `CLOSED/69`;
- all six physical XSM outputs: byte-for-byte equal to the prior accepted
  strict-LEAK1D64 artifact.

The independently read closed defects are

$$
(R_\rho,R_L,D_L,R_a)=
(3.1217481155643156\times10^{-8},
 4.7437809682878498\times10^{-9},
 6.9504964934560820\times10^{-12},
 2.6517344241198609\times10^{-9}).
$$

The unchanged criterion is
`R_rho <= 5e-7 AND R_L <= 5e-7 AND R_a <= 5e-7`; all three pass.
`D_L` is reported only as a dimensional diagnostic.

## 3. Existing independent reference

A read-only deck extracted, without a new transport solve,

- `k = 1.362411321869362`;
- axial nu-fission fractions
  `[0.259455602, 0.483591353, 0.256953045]`.

Against the hash-frozen OpenMC reference these give

- reactivity difference: `-174.244453 pcm`;
- maximum absolute floor-fraction difference: `8.130674535e-4`;
- maximum relative floor-fraction difference: `3.019708538e-3`.

No new comparison tolerance was introduced.  The reference artifact keeps
its summary, inputs and run log under SHA-256, but not the OpenMC statepoint;
therefore this is a hash-tied comparison to existing independent evidence,
not a fresh OpenMC recomputation.

The full local receipt is
`validation/artifacts/r2-leak64-clean-replay/`.

## Repository check boundary

The active `make spot-fast` gate passes without launching Dragon.  It checks
the current method and strict-REAL64 decks, strict inner termination, bounded
process behavior, fixed-state contracts and the Level-1/2 algebra kernels.
Every clean-replay receipt hash also verifies.  Campaign-specific legacy
continuation/AA source snapshots remain preserved in `run_picard_fast.sh` as
historical archaeology; they are not used to claim this numerical result.
