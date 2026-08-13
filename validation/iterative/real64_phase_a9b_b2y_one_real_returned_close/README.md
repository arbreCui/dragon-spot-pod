# Phase-A9b B2y: one bounded real returned-to-closed axial half-step

B2y freezes one deliberately narrow real experiment: given the B2z-staged
`RETURNED/1` file whose content is byte-identical to the RETURNED accepted
and recorded by B2v, can the production
`SpotCloseR64` procedure execute once and publish one valid `CLOSED/1`
axial/archive pair?

The experiment is deployment-default-off and its receipt is pending.  No
B2y Dragon activation has yet been made.  Until the runtime and independent
posterior evidence below both pass, the result remains `NOT-EVALUATED`.
The default-off preflight currently passes 73 directed mutation tests, strict
production compilation, real CLEPIL/OBJPIL compilation, private Dragon
linking and independent-posterior compilation in about five seconds, with
Dragon execution fixed at zero.

## Supplied input, never regenerated here

The radial result is the canonical B2z prerequisite, not work authorized for
B2y:

```text
path                   validation/artifacts/iterative-b2z/returned.xsm
RETURNED SHA-256        dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054
RETURNED bytes          231572260
B2z receipt             2f003d175a2ff7eea2feb73cc87e46d83c1c11e1e09f97ebe228472f7d741844
B2z runtime result      6627924e8bed19e23537ede946c3c7c2cc7dcf2f53b84055a4b8e047fe444850
B2z artifact manifest   22949de59c8662c43ca7f7ec3293e27287571ae85b58ecddf24fc2148a67ca0f
B2v historical receipt  af2b47504adcefc7d1e9fd2ae2ecf4517298e7b5b1be1cd75633ca0fa5482bcb
```

B2z is the direct input parent. B2x remains the frozen close-contract lineage,
and B2v is only the historical content reference. B2y verifies the B2z receipt
from the repository root, verifies the B2z artifact manifest inside its own
directory, requires the tracked and artifact runtime summaries to be
byte-identical, and requires all seven artifact entries to be regular,
non-symlink files. These gates run before the durable B2y attempt sentinel is
created and again after the posterior checks.

The axial inputs are likewise hash-pinned:

```text
TRACK_AX  101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
MACROLIB3 2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a
BASIS_REF dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504
```

If `B2Y_RETURNED_XSM` is not exactly the canonical B2z path—even if another
file has the same hash—or if any B2z receipt, summary, manifest, inventory,
byte count, or content gate fails, B2y stops before Dragon with
`INVALID-NO-SCIENTIFIC-RESULT`. It must not run `SpotStepR64`,
repeat B2v, reconstruct a substitute RETURNED object, search for an
unmanifested replacement, or launch any radial solve.  The same rule applies
to a missing or changed axial input.  Input and procedure hashes are checked
again after every attempted activation.

## Exactly one production call

An explicit opt-in may start at most one private Dragon process, in one fresh
process group, and make exactly one call to `SpotCloseR64`:

```text
supplied accepted RETURNED/1
  -> one private FEEDBACK deep copy
  -> SPOR64V exact read-only admission
  -> ASM SPOD 1 FIXB
  -> FLU TYPE K B1 SIGS
  -> SPOSTATE
  -> SPOLEAK direct L1
  -> SPOR64X -> SPOR64_B2W_CLOSE
  -> AX CLOSED/1 + ARCHIVE CLOSED/1
```

Within that one procedure call, the private FEEDBACK, assembled SYSTEM and
axial FLUX remain live in the same Dragon process until B2w either rejects
them or performs the final logical commit.  This is the permitted same-
process claim. Because the supplied file is a B2z rematerialization loaded
from disk, B2y must not claim that the B2v or B2z radial activation and the
B2y axial close occurred in the same process or in one continuous
`SpotStepR64 -> SpotCloseR64` host call.

There is no retry, restart, tolerance change, fallback, alternate rank,
second Dragon launch, or reuse of a partial output after any failure.

The only authorized activation form is:

```sh
RUN_B2Y=1 \
  B2Y_RETURNED_XSM="$(pwd)/validation/artifacts/iterative-b2z/returned.xsm" \
  make spot-real64-phase-a9b-b2y-one-real-returned-close
```

Immediately before the only Dragon launch, B2y atomically creates the local
ignored sentinel
`validation/artifacts/.real64-phase-a9b-b2y-attempted`. Success and failure
cleanup never remove it. Therefore any attempted close—including a timeout,
signal, strict failure or later evidence/publication failure—consumes the
one-real authorization and a second Dragon is mechanically refused.

## Frozen physical generation

The input represents the completed radial work generation.  Before ASM,
`SPOR64V` requires every child leakage value to equal its same-index SYSTEM
value bit for bit. Denote this field by \(L_0\). The three solved children
retain one common binary64 \(\rho_0\), the matching binary32 \(k_0\), and the
frozen fission source `QFISS0` that actually entered their radial equations.

`ASM SPOD 1 FIXB` uses the supplied rank-one fixed basis and rebuilds the
current response from those returned radial results.  Rank one is a declared
trial-space dimension, not a fitted physical coefficient, and its adequacy
is not decided by this experiment.  `FLU` then attempts one axial eigenvalue
solve.  A valid return must pass the unchanged strict predicate

```text
e_ext < eps_out
e_unk < eps_unk
e_inr < eps_inr
inner state = STRICT
outer visit >= 2
```

with the frozen binary32 threshold bits `0x348637bd` (`2.5E-7`),
`MAXOUT=500`, and the inherited axial `MAXINR=740`.  Success on the final
allowed visit is still success if that strict predicate is true.  Merely
reaching either cap is never a solution, and an exhausted SPOT TYPE-K solve
must abort before solution publication.  Formatted log values may round to
the printed threshold; the scientific evidence is entry through the hashed
strict-`<` production branch, not replacement of `<` by `<=`.

After strict axial termination, `SPOSTATE` constructs

```text
x1 = (a1, rho1, L1),  rho1 = 1/k1,
```

and `SPOLEAK` writes the freshly integrated, undamped (L_1) into only the
private feedback copy.  B2w may then publish the closed pair.  The closed
AX/root owns \((k_1,\rho_1,L_1,a_1)\), while each archived `SOLVED/1` child
correctly retains \((\rho_0,k_0,\mathrm{QFISS0})\), and each archived radial
SYSTEM retains \(L_0\). `QFISS0` must not be recomputed with \(\rho_1\) or
relabeled as a generation-1 axial source.

Neither \(\rho_1=\rho_0\) nor \(L_1=L_0\) is required. The componentwise
stored fields define the diagnostic

```text
D_L = max(abs(L1-L0)),
```

which is a dimensional transition diagnostic only. It is not an acceptance
threshold, damping trigger, fitted score, or convergence result.

## Required evidence for the success classification

A normal Dragon exit or a completion marker alone is insufficient.  A
successful future activation must provide all of the following:

- exactly one caller marker pair around exactly one `SpotCloseR64` call;
- exactly one ordered begin/end pair for `SPOR64V`, `ASM`, `FLU`,
  `SPOSTATE`, `SPOLEAK`, and `SPOR64X`, with no radial CONT or second axial
  solve;
- exactly one paired `FLU2DR-TERM` outer/inner success record, strict inner
  state 1, all 370 groups completed, and no cap-failure or XABORT path;
- fresh AX/archive output files and unchanged hashes for every input;
- two identical reports from an independent, read-only GANLIB/UTILIB
  posterior that links no Dragon, ASM, FLU, SPOSTATE, SPOLEAK, B2w, or
  transport symbol;
- exact `CLOSED/1` schemas, \(\rho_1=1/k_1\) bit for bit, all 370 ranks equal
  to one, `POD-FIXED`/`FIXB=1`, and finite canonical arrays with the frozen
  packed rank-one extents;
- exact preservation of the three child ρ0/k0/QFISS0 authorities and
  their REAL32 mirrors, exact recursive preservation of TRACK/MICROLIB2,
  retained SYSTEM (L_0), child (L_1), and bitwise agreement between
  canonical `SPOT-X-L` and the promoted child (L_1).

This posterior checks closed content and exact copy/promotion identities. It
does not independently recompute the canonical coordinates, normalization,
fixed basis, axial equation residual, or global balance. Those claims require
a separate read-only oracle with the frozen axial track, macrolib and basis as
explicit inputs.

On success, the two CLOSED XSM files, raw Dragon log, both posterior logs,
the bounded runtime summary and a content manifest are published together
to the local Git-ignored directory
\`validation/artifacts/real64-phase-a9b-b2y\`.  The final directory must be
fresh.  An activation lock is acquired before Dragon, and publication occurs
only after every runtime, posterior, lineage and frozen-input check.  A
same-filesystem Darwin \`renameatx_np(..., RENAME_EXCL)\` publishes the whole
bundle atomically without replacement.  Failure rolls back only a staging,
lock or final inode owned by that invocation; it never overwrites pre-existing
evidence.  This preserves the exact CLOSED state for later independent
residual and global-balance checks without another axial activation.

## Resource and failure contract

The sole opt-in Dragon process has hard safety limits of 80 s wall time,
75 s CPU, 2 GiB leader RSS, 512 MiB per file and 64 MiB log, with one thread
and core dumps disabled. At the absolute 80 s close deadline the wrapper
sends SIGKILL to only its fresh process group; there is no grace interval
after that deadline. Every earlier resource-census failure, managed wrapper
signal, or exception uses the same immediate group kill. Thus no cleanup path
adds a child-computation grace interval beyond the absolute wall deadline.
These are execution-safety limits, not physical coefficients or convergence
criteria.

The mutually exclusive classifications are:

- missing, changed or rejected prerequisite; nonfresh output path; or a
  pre-activation validation failure:
  `INVALID-NO-SCIENTIFIC-RESULT`;
- wall, CPU, RSS, file or log cap after the sole activation begins:
  `INVALID-RUNTIME-BUDGET-NO-CLOSED-RESULT`;
- nonzero/abnormal Dragon end, XABORT, strict FLU failure, or any failure to
  publish both closed objects:
  `FAILED-NO-CLOSED`;
- normal end but missing, repeated, interleaved or incorrectly ordered route
  and terminal records:
  `INVALID-RUNTIME-EVIDENCE`;
- normal evidenced route but missing, mutable or posterior-rejected output:
  `INVALID-CLOSED-EVIDENCE`;
- every input, runtime and independent posterior condition satisfied:
  `ONE-REAL-SUPPLIED-RETURNED-TO-CLOSED-AXIAL-HALF-STEP`.

Any file left by a failed or invalid run has no scientific status.  Failure
does not prove physical divergence, nonexistence of a coupled solution, or
failure of the 2D/1D method.

## Empirical-control boundary and nonclaims

B2y adds zero empirical coupling or model-completion coefficients.  The
direct update has no relaxation factor (α is not an input), damping,
clipping, fitting, correction, acceptance score, or retry.  Rank one,
`B1/SIGS`, the inner tolerances, iteration caps and external resource bounds
are disclosed numerical/discretization choices; they are not fitted feedback
coefficients.  This wording does not claim that the complete legacy solver
contains no fixed numerical settings or acceleration machinery.

Even after the success classification, B2y proves only one real supplied-
RETURNED axial half-step and its closed-state content.  It does not prove:

- same-process continuity with the earlier B2v radial activation;
- a complete production Picard map or any second outer update;
- outer convergence, contraction, stability, or fixed-point existence;
- rank-one sufficiency or rank refinement;
- an independent axial equation residual or global neutron balance;
- eigenvalue, flux, leakage, reaction-rate or power accuracy;
- mesh, axial-floor, angle, energy-group or inner-tolerance convergence;
- benchmark agreement, another-code agreement, full-core validity, repeated-
  run reproducibility, or cross-platform reproducibility.
