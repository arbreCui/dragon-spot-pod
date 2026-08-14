# SPOT validation

The active validation tree follows the dependencies of the method:

| path | purpose |
|---|---|
| `level1/` | volume-weighted POD algebra and rank behavior |
| `level2/` | radial source, leakage sign, balance and final-source identities |
| `iterative/` | fixed-basis state, strict inner termination and one-map contracts |

Run the complete no-transport gate with:

```sh
make spot-fast
```

The gate launches no Dragon process. It checks the production method,
compiles the retained CLE-2000 and Fortran paths, and runs only seconds-scale
tests.

The generic continuation host is default-off. Enabling it evaluates one
unchanged direct map from the hash-locked parent and requires a new result
directory:

```sh
RUN_CONTINUATION=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
RESULT_DIR=/absolute/path/to/new-result \
  sh validation/iterative/run_continuation_short.sh
```

It runs the radial and axial halves once each, with fixed process bounds and
no retry. It never updates the parent or starts another map automatically.

Current scientific status and the minimum frozen inputs for the next
continuation are in
[iterative/current_result.md](iterative/current_result.md) and
[iterative/current_parent.tsv](iterative/current_parent.tsv). The predeclared
three-way decision is in
[iterative/continuation_policy.md](iterative/continuation_policy.md).

Historical REAL64/B2 staging, GMRES/raw-MOC forensics, sensitivity probes,
numbered map continuations and Anderson scaffolding are not part of the active
gate. They remain recoverable from Git tag `archive-pre-lean-20260814`.
