# D4-A geometry-only TRACK result

## Classification

`VALID_PRODUCTION_COMPATIBLE_GEOMETRY_TOPOLOGY_ONLY`.

This probe runs `SALT` and `MCCGT` on the frozen IRENA D4-A 1/12 geometry.
It does not load cross sections or perform an eigenvalue, radial fixed-source,
axial or Picard solve.  Dragon has a 30-second execution timeout followed by
at most five seconds of process-group cleanup.  Compilation and record checks
are outside that execution timeout.  All generated TRACK artifacts remain in
a temporary directory that is removed on exit.

The frozen geometry SHA-256 is
`ca46ef77ea769059ddc612f1a78e4b565c32990401b21652c822bf2e11497a3e`.

## Verified topology

The independent GANLIB checker obtained

```text
NREG=132 NMAT=6 NSURF=12 NUNK=144 NCODE=6 EPSI=1E-5
MATCOD=132 VOLUME=132 V$MCCG=144 NZON$MCCG=144
KEYFLX=132 KEYCUR$MCCG=12 ICODE=6 ALBEDO=6 BC-REFL+TRAN=12
```

It also verifies positive finite measures, identical isotropic region-key
records, complete non-duplicated coverage of all 144 unknowns, and surface
boundary codes in `[-6,-1]`.  Thus 12 numerical surface-current unknowns
reuse six physical boundary/albedo code slots; these are not interchangeable
dimensions.  The checker also requires the exact existing production
`REAL-PARAM(1)=1.0e-5` bit pattern and zero remaining REAL-PARAM entries.  This
is the frozen MCCG numerical tolerance already required by `SPOR64_B2B/A8`,
not a fitted physical or coupling coefficient.

The independent checker reads the XSM TRACK object.  It records the generated
binary TRACK hash but does not parse that binary payload; the first physical
radial admission must exercise that remaining boundary.

Run the permanent probe with:

```sh
sh validation/iterative/run_d4a_track_geometry_probe.sh
```

The corrected passing invocation produced temporary artifacts with:

```text
track.xsm  SHA-256 5e0f726997b7ddd901821803984f4be488bdce3d7fcc34e322a4bf1578721fcb
           282612 bytes
track.bin  SHA-256 d2bcd5c078e7b66772f44963039eb0505300e4d51d4661125823f6037d2d51d7
           100566180 bytes
```

Two preliminary geometry-only executions were not accepted as the final
result.  In the first, Dragon completed but the harness incorrectly required
an ECHO marker to occur exactly once; the input listing and output each
contained it, so the TRACK checker was not run.  After that assertion alone
was corrected, the topology checker passed, but independent review found that
the probe deck's `EPSI=1e-6` did not match the current production TRACK gate.
The deck was aligned to the existing `1e-5` value, the exact bit check was
added, and the bounded invocation recorded above passed.  No physical solve
or automatic scientific-result retry occurred.

This result admits the real D4-A geometry topology only.  It is not evidence
of a D4-A transport solution or convergence.  The next required physical
input is one current, hash-locked set of three D4-A snapshots.
