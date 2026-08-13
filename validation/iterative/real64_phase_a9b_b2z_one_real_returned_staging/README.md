# Phase-A9b B2z: one production-source RETURNED staging

B2z asks one narrow question: from a deterministically rematerialized
PROJECTED whose bytes match the recorded B2v PROJECTED digest, and the
hash-pinned radial TRACK input, can the privately linked production-source
`SpotStepR64 -> SPOR64T` route return once, pass one GANLIB/UTILIB-only
solver-independent checker executed twice with identical reports, and
reproduce the historical B2v RETURNED content byte for byte?

This is a new, separately authorized production-source activation. It is not a
retry of B2v and it does not rewrite the frozen B2v result. B2v used a
validation observer around the thin adapter; B2z links the unmodified
production `src/SPOR64_B2U.f90`. Therefore B2z does not expose or claim
the historical per-plane cutoff counters.

The default-off gate compiles the complete private route but executes no
Dragon, ASM, radial transport, axial solve, or Picard step:

```sh
make spot-real64-phase-a9b-b2z-one-real-returned-staging
```

The explicitly enabled command is permitted exactly once:

```sh
RUN_B2Z=1 make spot-real64-phase-a9b-b2z-one-real-returned-staging
```

Immediately before the only Dragon launch, B2z atomically creates the local
ignored sentinel `validation/artifacts/.iterative-b2z-attempted`. It is
never removed by success or failure cleanup. Thus a timeout, identity
mismatch, signal or later evidence failure consumes the one-real
authorization and a second Dragon is mechanically refused.

The sole Dragon process is limited to 60 s wall, 55 s CPU, 2 GiB leader
RSS, 512 MiB per file, 64 MiB log, one thread, and no core dump. There is
no retry, fallback, relaxation, damping, clipping, fitted correction,
model completion, or parameter retuning.

Success requires all of the following:

- three ASM module calls followed by one production SPOR64T call;
- no SPOR64K/V/X, FLU, SPOSTATE, SPOLEAK, axial solve, or Picard execution;
- unchanged PROJECTED and radial TRACK inputs;
- two identical reports from two executions of one GANLIB/UTILIB-only,
  solver-independent posterior checker;
- a regular RETURNED file of exactly 231,572,260 bytes with SHA-256
  `dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054`;
- success-only atomic no-replace publication to the local ignored directory
  `validation/artifacts/iterative-b2z`.

The exact hash is a content-identity gate against the recorded B2v digest
for the subsequent B2y experiment, not an empirical physical acceptance
coefficient. Provenance comes jointly from pinned inputs, the privately
linked production-source route census, and retained logs; the digest alone
does not prove causal origin or physical correctness. A valid posterior
result with different bytes is classified as a nonidentical production
return and is not published or passed to B2y. No second Dragon is allowed.

Even a successful B2z result establishes only one same-input, same-platform
privately linked production-source rematerialization that is byte-identical
to the B2v reference.
It does not establish a complete Picard map, outer convergence, a fixed
point, an independent transport residual, SPOD rank sufficiency, or
cross-platform reproducibility.

“Added controls = 0” means B2z adds no empirical coupling or
model-completion control. It does not claim that the inherited solver has no
fixed numerical settings, stopping rules, or acceleration machinery.

## Frozen result

The sole authorized B2z activation completed successfully. The retained
Dragon log directly records one Dragon normal end, three ASM calls, one
privately linked production-source SPOR64T call, and zero forbidden V/X,
FLU, state, leakage, or observer calls. The three radial CONT returns and the
internal B2T/B2S/B2B/A9/B2R route are a control-flow/provenance inference
from the frozen production-source call chain, its strict status gates, the
successful SPOR64T return, and the three-plane posterior structure; they are
not separate runtime print counters. There were zero automatic retries. The
two executions of the same GANLIB/UTILIB-only posterior checker produced
identical reports.

The success artifact directory `validation/artifacts/iterative-b2z` contains
exactly seven non-symlink regular files, each read-only. Its `returned.xsm`
has 231,572,260 bytes and SHA-256
`dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054`.
The artifact manifest has SHA-256
`22949de59c8662c43ca7f7ec3293e27287571ae85b58ecddf24fc2148a67ca0f`,
and the byte-for-byte copied tracked runtime transcript has SHA-256
`6627924e8bed19e23537ede946c3c7c2cc7dcf2f53b84055a4b8e047fe444850`.

The transcript says `RECEIPT=PENDING-RUNTIME-FREEZE` because that line was
written inside the success artifact before the tracked freeze. It is retained
verbatim as primary evidence; the phase receipt now freezes that transcript
and the exact source/checker contract externally. The durable attempt sentinel
has identity `16777230:32670273`, so this B2z authorization is consumed and
must never be run again. B2y may accept only the canonical artifact path and
these exact content identities.

The bounded wrapper reported 15.845 s to the activation console, but that
outer timing was not retained in the success artifact, so it is not promoted
to a frozen result field. Likewise, the private Dragon digest was recorded at
activation but the temporary executable was intentionally not retained; the
digest is provenance metadata, not a new independent re-hash or physical
validation.
