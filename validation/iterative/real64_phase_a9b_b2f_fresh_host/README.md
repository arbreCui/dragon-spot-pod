# Phase A9b-B2f: fresh-output bootstrap host

B2f closes one host-lifecycle boundary: the explicit REAL64 plane path can
read its initial state from a distinct, read-only `FLUX_OLD` object and publish
the accepted result into a fresh `FLUX` object.  This is a bootstrap result,
not an online Picard-convergence result.

The seven entries have one owner each:

```text
FLUX       create, sole publication target
MACRO0     read-only
TRACK      read-only
TRACK_f    read-only sequential descriptor
SYSTEM     read-only
FSOURCE    read-only
FLUX_OLD   read-only initial-flux seed
```

`FLUX` and every right-hand-side object must be distinct.  The target must be
an empty LCM object, `REC=false`, and `LIMERG=true`.  B2B reads the seed and
the other five inputs but contains no LCM mutation.  Only an accepted terminal
state is handed synchronously to the real B2C publisher, which is the sole
writer of the new object.  An empty daughter table is not a root target and
is rejected by both boundaries.

The production path remains default OFF.  The existing `SpotPlaneFS` and
`SpotRefFS` procedures are unchanged and do not request `R64`.  The new
`SpotPlaneR64` and `SpotRefR64` names are explicit suffixes, and no shipped
top-level deck selects `SpotRefR64`.  The B2f harness calls B2B directly; it
does not execute either C2M procedure or Dragon.

## Exact validation boundary

The executable harness links and executes the real production
`SPOR64_B2B` ingress and `SPOR64_B2C` publisher.  It deliberately replaces
three later boundaries with validation-owned test doubles:

- `SPOMOC_ACTIVE` is a counter that returns false;
- `XDRTA2` is a zero-argument counter;
- `FLU2DR64_CORE` is a deterministic copy oracle that returns the promoted
  initial flux and frozen fixed source as an accepted terminal state.

The copy oracle is not a transport operator, physical model, or convergence
iteration.  It exists only to exercise the accepted host and publication
lifecycle without entering production XDR initialization or the solver core.

Five frozen XSM artifacts are copied byte-for-byte into a temporary directory
and opened read-only:

- `restart_cap.xsm` as `FLUX_OLD`;
- `restart_macro0.xsm` as `MACRO0`;
- `restart_track.xsm` as `TRACK`;
- `restart_system.xsm` as `SYSTEM`;
- `restart_source.xsm` as `FSOURCE`.

The original artifacts are never modified.  `TRACK_f` is represented by a
validation-only descriptor and its sequential file is never opened or read.
Consequently the gate does read real LCM metadata, but performs zero
sequential tracking-record reads.

The real macrolib stores three scattering components, P0, P1 and P2, while
the real MCCG track activates one component.  Therefore the legacy active
order is exactly

```text
min(TRACK/STATE-VECTOR(6)-1, MACRO0/STATE-VECTOR(3)-1)
  = min(0, 2) = 0.
```

B2B verifies the stored P1/P2 `NJJS01` and `NJJS02` shapes but loads only the
active P0 `NJJS00`, `IJJS00`, `IPOS00`, and `SCAT00` data.  It neither deletes,
zeros, nor reinterprets the stored P1/P2 records.

The seed is required to have no `SPOT-R64` directory.  This is intentional:
B2f proves only the first bootstrap from the legacy type-2 `FLUX` seed.  It
does not silently use a once-rounded compatibility mirror as the next REAL64
Picard state.  Consuming an earlier type-4 `SPOT-R64/FLUX` authority requires
a later, explicit continuation contract.

The positive case promotes the frozen binary32 seed and source once, passes
through the copy oracle, and exercises the real publisher.  The readback
checks all type-4 authority values, type-2 compatibility values, state,
tolerances, merge map, links, option, key map, and leakage cache.  A second
publication and six direct invalid-publication cases fail before writing.
Six invalid ingress cases also stop before the stub XDR/core boundary.

The controlled execution inventory is:

```text
REAL-B2B-CALLS=7
CONTRACT-TESTS=47
MUTATION-CASES=46
BLOCKED-INGRESS-SCENARIOS=6
PRODUCTION-PUBLISHER-CALLS=8
PRODUCTION-PUBLISHER-COMMITS=1
PUBLISHER-PREFLIGHT-REJECTIONS=7
STUB-XDRTA2-CALLS=1
STUB-CORE-CALLS=1
PRODUCTION-XDRTA2-CALLS=0
PRODUCTION-CORE-CALLS=0
DRAGON-EXECUTIONS=0
SEQUENTIAL-TRACKING-RECORD-READS=0
TRANSPORT-SOLVES=0
ORIGINAL-ARTIFACT-MUTATIONS=0
C2M-HOST-EXECUTIONS=0
```

Run the seconds-scale gate with:

```sh
sh validation/iterative/real64_phase_a9b_b2f_fresh_host/run_phase_a9b_b2f_fresh_host.sh
```

No transport equation, SPOD basis, cross section, source term, or convergence
criterion is changed.  No relaxation, fitted coefficient, empirical
parameter, clipping rule, fallback, or model completion is introduced.  This
gate does not validate a physical transport response, runtime provenance, a
continuous REAL64 iteration, radial convergence, or outer Picard convergence.
Production execution remains unauthorized; both convergence results remain
`NOT-EVALUATED`.
