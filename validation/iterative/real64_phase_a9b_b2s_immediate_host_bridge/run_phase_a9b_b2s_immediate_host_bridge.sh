#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2r_returned_archive/phase_a9b_b2r_returned_archive_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2s_immediate_host_bridge_receipt.sha256"
EXPECTED_PARENT_COMMIT=7d40c0ef71e136a6c424a29b67dd58011b10f3f7
EXPECTED_PARENT_HASH=8970a7c383259a6f71cda2489ce64a7983ae867c5fc56ddc8a2abd01d58eb394
STATIC_CHECKER="$HERE/check_phase_a9b_b2s_immediate_host_bridge.py"
MUTATION_TEST=test_phase_a9b_b2s_immediate_host_bridge
STUB="$HERE/b2s_capture_stubs.f90"
FIXTURE="$HERE/b2s_fixture_support.f90"
HARNESS="$HERE/test_b2s_immediate_host_bridge.f90"
POSTERIOR="$HERE/check_b2s_immediate_host_bridge.f90"
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2s.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2s FAILURE: $*" >&2
  exit 1
}

count_exact()
{
  expected=$1
  pattern=$2
  file=$3
  found=$(grep -c -E "$pattern" "$file" || true)
  [ "$found" -eq "$expected" ] || \
    fail "$file: expected $expected matches for $pattern, found $found"
}

hash_of()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" || fail "copy differs: $target_path"
}

run_limited()
(
  ulimit -c 0
  ulimit -t 15
  ulimit -f 262144
  perl -e '$seconds=shift @ARGV; alarm $seconds; exec @ARGV' 15 "$@"
)

verify_parent()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2r parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2r parent receipt changed"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2r parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2r parent commit is not an ancestor"
}

verify_receipt()
{
  [ -f "$RECEIPT" ] || fail "B2s contract receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2s contract receipt verification failed"
}

verify_input_copy()
{
  original=$1
  copied=$2
  expected_hash=$3
  cmp "$original" "$copied" || fail "read-only input changed: $copied"
  [ "$(hash_of "$original")" = "$expected_hash" ] || \
    fail "source artifact hash changed: $original"
  [ "$(hash_of "$copied")" = "$expected_hash" ] || \
    fail "read-only case input hash changed: $copied"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
command -v perl >/dev/null 2>&1 || fail "wall-time limiter missing"
FC_BANNER=$($FC --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
verify_parent
verify_receipt

for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
[ -f "$STUB" ] || fail "capture stubs missing"
[ -f "$FIXTURE" ] || fail "fixture support missing"
[ -f "$HARNESS" ] || fail "immediate bridge harness missing"
[ -f "$POSTERIOR" ] || fail "independent posterior missing"
[ -f "$STATIC_CHECKER" ] || fail "static immediate-bridge checker missing"
[ -f "$HERE/$MUTATION_TEST.py" ] || fail "immediate-bridge mutation suite missing"

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,220p' "$BUILD_DIR/static.log" >&2
  fail "static immediate-host-bridge contract rejected"
fi
count_exact 1 '^B2S STATIC IMMEDIATE-HOST-BRIDGE PASS$' "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2S DEFAULT=OFF OBJECT-ACCESS=0 SCRATCH=0 SUBCALLS=0$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2S ON=B2O\(3\)->B2B-CONT/HOST_COMMITTED\(3\)->B2R\(1\)$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2S CALLER-SOLVED=FORBIDDEN LOOSE-PHYSICS-CONTROLS=0$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2S CUTOFF=INT64-PER-PLANE-DIAGNOSTIC-ONLY$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2S TRUE-TRANSPORT/CONVERGENCE=NOT-CLAIMED$' \
  "$BUILD_DIR/static.log"
[ "$(wc -l <"$BUILD_DIR/static.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected static checker output line count"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,280p' "$BUILD_DIR/mutations.log" >&2
  fail "immediate-host-bridge mutation suite rejected"
fi
count_exact 1 '^Ran 46 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"
verify_parent
verify_receipt

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2R SPOR64_B2S
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
copy_exact "$STUB" "$SOURCE_DIR/b2s_capture_stubs.f90"
copy_exact "$FIXTURE" "$SOURCE_DIR/b2s_fixture_support.f90"
copy_exact "$HARNESS" "$SOURCE_DIR/test_b2s_immediate_host_bridge.f90"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2s_immediate_host_bridge.f90"

SEED_SOURCE="$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm"
MACRO_SOURCE="$ROOT/validation/artifacts/raw-moc-capture/common/restart_macro0.xsm"
TRACK_SOURCE="$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm"
SYSTEM_SOURCE="$ROOT/validation/artifacts/raw-moc-capture/common/restart_system.xsm"
QSOURCE_SOURCE="$ROOT/validation/artifacts/raw-moc-capture/common/restart_source.xsm"
for input in "$SEED_SOURCE" "$MACRO_SOURCE" "$TRACK_SOURCE" \
  "$SYSTEM_SOURCE" "$QSOURCE_SOURCE"
do
  [ -f "$input" ] || fail "frozen B2p input missing: $input"
done
SEED_HASH=$(hash_of "$SEED_SOURCE")
MACRO_HASH=$(hash_of "$MACRO_SOURCE")
TRACK_HASH=$(hash_of "$TRACK_SOURCE")
SYSTEM_HASH=$(hash_of "$SYSTEM_SOURCE")
QSOURCE_HASH=$(hash_of "$QSOURCE_SOURCE")
copy_exact "$SEED_SOURCE" "$CASE_DIR/seed.xsm"
copy_exact "$MACRO_SOURCE" "$CASE_DIR/macro.xsm"
copy_exact "$TRACK_SOURCE" "$CASE_DIR/track.xsm"
copy_exact "$SYSTEM_SOURCE" "$CASE_DIR/system.xsm"
copy_exact "$QSOURCE_SOURCE" "$CASE_DIR/source.xsm"
chmod 444 "$CASE_DIR/seed.xsm" "$CASE_DIR/macro.xsm" \
  "$CASE_DIR/track.xsm" "$CASE_DIR/system.xsm" "$CASE_DIR/source.xsm"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/b2s_capture_stubs.f90" \
  -o "$OBJECT_DIR/b2s_capture_stubs.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2B.f90" -o "$OBJECT_DIR/SPOR64_B2B.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2O.f90" -o "$OBJECT_DIR/SPOR64_B2O.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2R.f90" -o "$OBJECT_DIR/SPOR64_B2R.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2S.f90" -o "$OBJECT_DIR/SPOR64_B2S.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/b2s_fixture_support.f90" \
  -o "$OBJECT_DIR/b2s_fixture_support.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/test_b2s_immediate_host_bridge.f90" \
  -o "$OBJECT_DIR/test_b2s_immediate_host_bridge.o"
"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/check_b2s_immediate_host_bridge.f90" \
  -o "$OBJECT_DIR/check_b2s_immediate_host_bridge.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/b2s_capture_stubs.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2B.o" \
  "$OBJECT_DIR/SPOR64_B2O.o" \
  "$OBJECT_DIR/SPOR64_B2R.o" \
  "$OBJECT_DIR/SPOR64_B2S.o" \
  "$OBJECT_DIR/b2s_fixture_support.o" \
  "$OBJECT_DIR/test_b2s_immediate_host_bridge.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2s_immediate_host_bridge"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2s_immediate_host_bridge.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/check_b2s_immediate_host_bridge"

nm -g "$BUILD_DIR/test_b2s_immediate_host_bridge" >"$BUILD_DIR/harness.nm"
FORBIDDEN_SOLVERS='(^|[[:space:]])_?(dragon|asm|asmdrv|spoasm|doorav|doorfv|doorpv|mccga|mccgf|mcgasm|mcgmre|flu|fludrv|flu2dr|flugpi|xdrkin|xdrexp|spomoc|spor64k)_$|spor64_a8_'
if grep -Eiq "$FORBIDDEN_SOLVERS" "$BUILD_DIR/harness.nm"
then
  fail "harness links Dragon, ASM, FLU, A8, or a transport implementation"
fi
count_exact 1 '___spor64_a9_MOD_flu2dr64_core$' "$BUILD_DIR/harness.nm"
count_exact 1 ' _xdrta2_$' "$BUILD_DIR/harness.nm"
nm -g "$BUILD_DIR/check_b2s_immediate_host_bridge" \
  >"$BUILD_DIR/posterior.nm"
if grep -Eiq "spor64_|$FORBIDDEN_SOLVERS" "$BUILD_DIR/posterior.nm"
then
  fail "independent posterior links SPOR64 or solver code"
fi

[ ! -e "$CASE_DIR/returned.xsm" ] || fail "RETURNED path is not fresh"
start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/test_b2s_immediate_host_bridge" \
    seed.xsm macro.xsm track.xsm system.xsm source.xsm returned.xsm \
    >harness.log 2>&1
)
then
  sed -n '1,260p' "$CASE_DIR/harness.log" >&2
  fail "immediate-host-bridge harness rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "synthetic bridge exceeded 15 seconds"
count_exact 1 '^B2S IMMEDIATE-HOST-BRIDGE PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2S DEFAULT-OFF=0-ACCESS EXPLICIT-OFF=0-ACCESS$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2S DUPLICATE-PLANE=PRE-CORE PLANE2-FAIL=EMPTY-OUTPUT$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2S XDRTA2=3 STUB-CORE=3 RETURNED=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2S TERMINAL64=31080 MIRROR32=31080 QFISS64=31080$' \
  "$CASE_DIR/harness.log"
if [ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -ne 5 ]
then
  sed -n '1,260p' "$CASE_DIR/harness.log" >&2
  fail "unexpected immediate-bridge harness output line count"
fi
[ -f "$CASE_DIR/returned.xsm" ] || fail "RETURNED XSM evidence missing"
[ -s "$CASE_DIR/returned.xsm" ] || fail "RETURNED XSM evidence is empty"

verify_input_copy "$SEED_SOURCE" "$CASE_DIR/seed.xsm" "$SEED_HASH"
verify_input_copy "$MACRO_SOURCE" "$CASE_DIR/macro.xsm" "$MACRO_HASH"
verify_input_copy "$TRACK_SOURCE" "$CASE_DIR/track.xsm" "$TRACK_HASH"
verify_input_copy "$SYSTEM_SOURCE" "$CASE_DIR/system.xsm" "$SYSTEM_HASH"
verify_input_copy "$QSOURCE_SOURCE" "$CASE_DIR/source.xsm" "$QSOURCE_HASH"

OUTPUT_HASH=$(hash_of "$CASE_DIR/returned.xsm")
OUTPUT_BYTES=$(stat -f '%z' "$CASE_DIR/returned.xsm")
chmod 444 "$CASE_DIR/returned.xsm"
start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/check_b2s_immediate_host_bridge" returned.xsm \
    >posterior1.log 2>&1
  run_limited "$BUILD_DIR/check_b2s_immediate_host_bridge" returned.xsm \
    >posterior2.log 2>&1
)
then
  sed -n '1,260p' "$CASE_DIR/posterior1.log" >&2
  sed -n '1,260p' "$CASE_DIR/posterior2.log" >&2
  fail "independent immediate-bridge posterior rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "two posterior runs exceeded 15 seconds"
cmp "$CASE_DIR/posterior1.log" "$CASE_DIR/posterior2.log" || \
  fail "independent posterior reports differ"
[ "$(hash_of "$CASE_DIR/returned.xsm")" = "$OUTPUT_HASH" ] || \
  fail "read-only posterior mutated RETURNED XSM"
[ "$(stat -f '%z' "$CASE_DIR/returned.xsm")" -eq "$OUTPUT_BYTES" ] || \
  fail "read-only posterior changed RETURNED XSM size"
count_exact 1 '^B2S IMMEDIATE-HOST-BRIDGE POSTERIOR PASS$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2S R64-FLUX-BITS=15540 R64-SOUR-BITS=15540 R64-QFISS-BITS=15540$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2S R32-FLUX-BITS=15540 R32-SOUR-BITS=15540 R32-QFISS-BITS=15540$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2S TRACK-COPIES=3 MICROLIB2-COPIES=3 SYSTEM-COPIES=3$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2S CHILD-PLANE-ABSENCES=3 TERMINAL-LOWBIT-WITNESSES=31080$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2S ROOT-RHO=ABSENT ROOT-K=ABSENT AX-NEXT=ABSENT CLOSED=ABSENT$' \
  "$CASE_DIR/posterior1.log"
[ "$(wc -l <"$CASE_DIR/posterior1.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected independent posterior output line count"

verify_input_copy "$SEED_SOURCE" "$CASE_DIR/seed.xsm" "$SEED_HASH"
verify_input_copy "$MACRO_SOURCE" "$CASE_DIR/macro.xsm" "$MACRO_HASH"
verify_input_copy "$TRACK_SOURCE" "$CASE_DIR/track.xsm" "$TRACK_HASH"
verify_input_copy "$SYSTEM_SOURCE" "$CASE_DIR/system.xsm" "$SYSTEM_HASH"
verify_input_copy "$QSOURCE_SOURCE" "$CASE_DIR/source.xsm" "$QSOURCE_HASH"
PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" >/dev/null
verify_parent
verify_receipt

printf '%s\n' 'SPOR64 PHASE-A9b-B2s IMMEDIATE-HOST-BRIDGE PASS'
printf '%s\n' 'DEFAULT=OFF DISABLED-OBJECT-ACCESS=0 DISABLED-SUBCALLS=0'
printf '%s\n' 'ENABLED=B2O(3)->REAL-B2B-CONT(3)->B2R(1)->RETURNED/1'
printf '%s\n' 'SOURCE-CALL-ORDER=2,3,1 RADIAL-ORDER=1,2,3'
printf '%s\n' 'STUB-XDRTA2=3 STUB-CORE=3 TRUE-TRANSPORT=0'
printf '%s\n' 'R64-FLUX/SOUR/QFISS-BITS=15540/15540/15540'
printf '%s\n' 'R32-FLUX/SOUR/QFISS-BITS=15540/15540/15540'
printf '%s\n' 'POSTERIOR-RUNS=2 INPUTS=READ-ONLY'
printf '%s\n' 'DRAGON=0 ASM=0 SPOASM=0 FLU=0 A8=0 PRODUCTION-A9=0'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
printf '%s\n' 'ROOT=RETURNED/1 ROOT-RHO=ABSENT ROOT-K=ABSENT CLOSED=ABSENT'
printf '%s\n' "RETURNED-XSM-SHA256=$OUTPUT_HASH BYTES=$OUTPUT_BYTES"
