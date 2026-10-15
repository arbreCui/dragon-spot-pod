# Exact-kernel companion on the complete retained native flight

The [segment-composition audit](native_segment_composition_result.md) finds
that exact T/B/D compose to roundoff, while the native tabulated kernel changes
under partitioning. Its largest fixture response change is about 2.96e-5
relative. The strict native-preservation gate remains failed; balancing factors
or a relaxed equality threshold are not a repair.

The next bounded step evaluates an explicitly different **exact-exponential
kernel companion** on the complete frozen radial flight. This measures how
the primitive change propagates through actual track aggregation and common
white return before introducing axial crossings. It does not claim to preserve
the original tabulated operator exactly.

## Inputs and distinct comparisons

Keep the original groups 51, 61, 98, ray ordering, physical lengths
`h2*ZMU`, native total precision, quadrature/volume/surface weights, planar
orientations and the independently defined axial signs. Keep the original
eight regions and six surfaces. Reuse all 216 prescribed source/inflow pairs
per group from the sealed signed-state experiment, including the signed
controls and the deliberately separate-sign boundary comparison.

First rerun the native branch on those 648 fixed inputs. Recover its retained
integrals, boundary responses, scalar and axial-current moments at the
existing `5e-12` tolerance. Keep the rounded PJJ completion exactly where it
was previously defined; it must not be spread over directions or segments.

Then replace only per-segment coefficients with the exact physical integrals
T/B/D. Apply the same fixed inputs so differences measure a kernel change.
For this exact companion derive scalar and current moments from its actual
retained integrals. Do not add the old native PJJ completion to the exact
own-source term. Report table-kernel and PJJ-completion differences separately.

Next rebuild **one common** radial white-return map from the exact companion's
full angular source/boundary responses. Sum all polar nodes, both planar
orientations and both axial signs into each common surface amplitude. Solve
the small boundary system directly. Reclose the 64 directional volume-unit
sources and the three fixed even/odd source profiles per group; holding the
old native inflow fixed is not an exact-kernel white-boundary solution.
Preserve the separate-sign model only as an explicitly labelled control.

## Mathematical and physical controls

For the exact companion repeat each complete flight with every original
segment unsplit, split into 2/4/8 equal pieces, and split 1/3 + 2/3. These are
zero-gradient algebraic partitions, not a discretized axial geometry. Require
the complete outgoing and integrated response, scalar and nonzero current
moments to recover the unsplit exact flight at `5e-12`. Declare an absolute
source-induced moment scale for zero/current-cancellation cases before running;
do not divide by a vanishing net current or tune a scale from a failing case.

Require nonnegative retained amplitudes/integrals for all 642 nonnegative
prescribed inputs and the newly reclosed positive-source cases. Preserve
the six signed controls as signed responses; do not apply positivity to them.
Check the entire common-boundary inverse response and boundary closure
residual at `5e-12`. Retain actual directional states and both current moments.

Raw segment/track source-minus-collision-minus-escape balance for exact
coefficients must be below `1e-10` on the established source/current scale.
Keep geometric source/surface measures and the native stored normalizers as
separate ledgers. Disclose their known rounding difference instead of repairing
it; compare assembled raw global balance with the earlier `1e-6` context limit.
The native-versus-exact full-flight differences are measured changes, not a
new fitted physical-accuracy pass criterion. Report componentwise/weighted
scalar and current errors, outgoing currents, their worst input labels, and
the effect of recomputing white return.

## Execution and admission

Freeze source identities, all metrics and zero-moment scales in a plan before
running. Use one numerical thread, a 512 MiB cap and 600 seconds per process.
Batch source columns/track records and release scratch arrays. Keep complete
raw source/response fields, failed controls, runtime measurements and an
independent fresh-directory replay. Preserve the failed 8192-record
composition attempt and its successful compact follow-up unchanged.

Passing establishes a reproducible exact-kernel full-flight companion and
quantifies its difference from the original operator. It does not turn the
native partition-preservation or spatial-refinement failures into passes.
The subsequent geometry contract must still define actual oblique axial
crossings, their quadrature, top/bottom inflow and shared current measures.
No multigroup/fission eigenproblem, POD training, shared build, live D4 run
or production replacement belongs to this step.
