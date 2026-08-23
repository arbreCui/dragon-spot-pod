# A8/A9 runtime-geometry result

## Scope

This is a no-transport interface result.  It verifies that the strict REAL64
radial call chain no longer encodes the pin cell's region, material or unknown
counts in `SPOR64_A8` or `SPOR64_A9`.  It is not a D4-A physics or convergence
result.

The unchanged method constraints are:

- 370 energy groups;
- runtime MCCG numerical surface-current unknowns;
- six fixed physical boundary/albedo code slots;
- the existing REAL64 equations, loop order, iteration limits and strict
  terminal predicates;
- no relaxation, fitted coefficient or empirical parameter.

## Cases

The test compiles the current A8/A9 sources and checks two shapes:

| case | regions | materials | numerical surfaces | unknowns |
|---|---:|---:|---:|---:|
| validated pin boundary | 8 | 8 | 6 | 14 |
| manufactured real D4-A tuple | 132 | 6 | 12 | 144 |

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
A8/A9 RUNTIME-GEOMETRY PASS: pin and D4-A (132,144,12) tuple; no transport.
```

The D4-A dimensions were read independently from its real TRACK object.  The
test payload itself is manufactured and proves only runtime shape propagation;
it is not a transport or convergence result.
