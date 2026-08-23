# A8/A9 runtime-geometry result

## Scope

This is a no-transport interface result.  It verifies that the strict REAL64
radial call chain no longer encodes the pin cell's region, material or unknown
counts in `SPOR64_A8` or `SPOR64_A9`.  It is not a D4-A physics or convergence
result.

The unchanged method constraints are:

- 370 energy groups;
- six MCCG outer-surface unknowns, matching the current legacy kernels;
- the existing REAL64 equations, loop order, iteration limits and strict
  terminal predicates;
- no relaxation, fitted coefficient or empirical parameter.

## Cases

The test compiles the current A8/A9 sources and checks two shapes:

| case | regions | materials | unknowns |
|---|---:|---:|---:|
| validated pin boundary | 8 | 8 | 14 |
| manufactured D4-A-sized boundary | 132 | 6 | 138 |

For each shape it checks the A8 tracking ranks, material/operator extents and
the A9 REAL64 state extent.  It then calls the A9 core with null transport
handles and requires a fail-closed return: no acceptance, zero visit count
and zero terminal outputs.

Run:

```sh
make spot-a89-dimensions
```

Expected terminal:

```text
A8/A9 RUNTIME-GEOMETRY PASS: pin-8 and manufactured D4A-132; no transport.
```

The manufactured 138-unknown case proves only runtime shape propagation.
The real D4-A dimensions must still be read from its TRACK object when a
separately authorized physical staging is eventually performed.
