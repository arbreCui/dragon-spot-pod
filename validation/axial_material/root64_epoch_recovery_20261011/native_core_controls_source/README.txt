Current ROOT64 native core controls — Source only, 2026-10-11

test_current_ROOT64_native_core.f90 is a new standalone GANLIB program.
It must be compiled and run by the Root's original bounded supervisor;
the author has not compiled, linked or run it.

The complete program makes actual PUBLISH_NATIVE, READ_NATIVE and
IMPORT_NATIVE calls. It creates real in-memory GANLIB objects, an original
RCONTRACT, a 2-region / 3-unknown MCCG context, library/macrolib and system
contexts with all 370 groups, and 370 type-4 REAL64 flux vectors. The flux
includes low bits lost by REAL32 and signed zero at the surface unknown.
All 370 returned groups are compared by raw REAL64 bits.

The 83 planned cases are:
  3 positive cases, one for each allowed plane;
  28 publish refusals with independent full-tree input atomicity checks;
  48 read/import refusals, checking unallocated read output and empty
     imported output after actual calls, plus byte-exact input preservation;
  3 occupied / aliased / non-root output refusals with exact preservation;
  1 intentionally accepted coherent edit to all internal last-group copies.

The last case documents the declared boundary: coherent changes to all
internal copies cannot be authenticated by this module. The independent
external full-file SHA/7ID binding must refuse them before a real native
read. The test does not call that absent external boundary a success.

Each result row is printed only after the calls and all assertions finish.
Any unexpected refusal, acceptance, mutation, allocation or missing value
raises ERROR STOP 1 immediately. No case retries or child launches occur.
The stdout summary can only be produced by the actual compiled test run.
In negative rows, publish_status=2 refers to the real baseline publication
from which the tested tree was cloned. For stages not called in that case,
status=0 means not called; it is not a ROOT64 success code.

CURRENT_NATIVE_CORE_CONTROL_SOURCE_BINDING.json records current full-EOF
Source and dependency pins and the exact proposed compile/link/run vectors.
The three linked scientific objects are from the actual new four-step
compile. They are followed by the original libGanlib.a. No libDragon.a,
old test executable, original missing TMP fixture, or SPOBOOT64.o is linked.
The compiler flags are the original nine flags; the link uses the original
-O2 and -ffp-contract=off. Only one actual run process is required, with no
command-line arguments, under the original caps and no retry.

This synthetic contract fixture is not a transport solve or strict physical
producer. It does not execute REDGET/SPOBOOT64's seven-entry parser, GLOBAL
source lifecycle, host coherent-edit refusal, old 17 controls, native solve,
online BOOT or AAA/ABA science. Those remain separate pending work.
