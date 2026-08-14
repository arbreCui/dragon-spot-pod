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

The only retained transport replay is the frozen $x_0\to x_1$ experiment.
It is default-off and is not a generic continuation host:

```sh
RUN_ONE_MAP=1 \
DRAGON_BIN=/absolute/path/to/Dragon \
SEED_DIR=/absolute/path/to/iterative-seed \
X0_DIR=/absolute/path/to/iterative-map1 \
  sh validation/iterative/run_one_map_short.sh
```

It has a fixed process timeout, no retry, and requires hash-locked local
artifacts. It proves one map evaluation, not outer convergence.

Current scientific status and the minimum frozen inputs for the next
continuation are in
[iterative/current_result.md](iterative/current_result.md) and
[iterative/current_parent.sha256](iterative/current_parent.sha256).

Historical REAL64/B2 staging, GMRES/raw-MOC forensics, sensitivity probes,
numbered map continuations and Anderson scaffolding are not part of the active
gate. They remain recoverable from Git tag `archive-pre-lean-20260814`.
