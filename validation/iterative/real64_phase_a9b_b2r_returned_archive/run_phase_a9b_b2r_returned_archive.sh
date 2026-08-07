#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2q_lifecycle_rho_contract/phase_a9b_b2q_lifecycle_rho_contract_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2r_returned_archive_receipt.sha256"
EXPECTED_PARENT_COMMIT=69adf38dba7b67698ac0f83f6286f729695d72d1
EXPECTED_PARENT_HASH=85dba806828efd557869b78b248feabaa5c11828d8e4afdd3f3a2cb8df739287
SOURCE="$ROOT/src/SPOR64_B2R.f90"
HARNESS="$HERE/test_b2r_returned_archive.f90"
POSTERIOR="$HERE/check_b2r_returned_archive.f90"
STATIC_CHECKER="$HERE/check_phase_a9b_b2r_returned_archive.py"
MUTATION_TEST=test_phase_a9b_b2r_returned_archive
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
SOLVER_SYMBOLS='(^|[[:space:]])_?(dragon|asm|asmdrv|xdrta2|kdrdrv|doorav|doorfv|doorpv|mccga|mccgf|mcgasm|mcgmre|flu|fludrv|flu2dr|flugpi|xdrkin|xdrexp|spomoc|spoasm|spostate|spoleak|spor64k)_$|spor64_(a8|a9)_'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2r.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2r FAILURE: $*" >&2
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
  "$@"
)

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2q parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2q parent receipt changed"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2q parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2q parent commit is not an ancestor"
  [ -f "$RECEIPT" ] || fail "B2r contract receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2r contract receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$($FC --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
[ -f "$SOURCE" ] || fail "SPOR64_B2R production source missing"
[ -f "$HARNESS" ] || fail "synthetic collector harness missing"
[ -f "$POSTERIOR" ] || fail "independent posterior missing"
[ -f "$STATIC_CHECKER" ] || fail "static returned-archive checker missing"
[ -f "$HERE/$MUTATION_TEST.py" ] || fail "returned-archive mutation suite missing"
verify_receipts

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
copy_exact "$SOURCE" "$SOURCE_DIR/SPOR64_B2R.f90"
copy_exact "$HARNESS" "$SOURCE_DIR/test_b2r_returned_archive.f90"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2r_returned_archive.f90"

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,220p' "$BUILD_DIR/static.log" >&2
  fail "static returned-archive contract rejected"
fi
count_exact 1 '^B2R STATIC RETURNED-ARCHIVE PASS$' "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2R API=ASSEMBLED\+SOLVED\(3\)\+FROZEN-QFIS\(3\)->RETURNED/1$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2R PLANE-BINDING=LABEL-SET-\{1,2,3\} NOT-ARGUMENT-ORDER$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2R QFISS=TYPE4-AUTHORITY\+TYPE2-SPOASM-MIRROR SOUR=TERMINAL-WITNESS$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2R CLOSED/1=NOT-PUBLISHED SOLVER-EXECUTIONS=0$' \
  "$BUILD_DIR/static.log"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,260p' "$BUILD_DIR/mutations.log" >&2
  fail "returned-archive mutation suite rejected"
fi
count_exact 1 '^Ran 65 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2R.f90" -o "$OBJECT_DIR/SPOR64_B2R.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/test_b2r_returned_archive.f90" \
  -o "$OBJECT_DIR/test_b2r_returned_archive.o"
"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/check_b2r_returned_archive.f90" \
  -o "$OBJECT_DIR/check_b2r_returned_archive.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2R.o" \
  "$OBJECT_DIR/test_b2r_returned_archive.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2r_returned_archive"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2r_returned_archive.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/check_b2r_returned_archive"

nm -g "$BUILD_DIR/test_b2r_returned_archive" >"$BUILD_DIR/harness.nm"
if grep -Eiq "$SOLVER_SYMBOLS" "$BUILD_DIR/harness.nm"
then
  fail "collector harness links Dragon, ASM, SPOASM, FLU, transport, or Picard code"
fi
nm -g "$BUILD_DIR/check_b2r_returned_archive" >"$BUILD_DIR/posterior.nm"
if grep -Eiq "spor64_b2r|$SOLVER_SYMBOLS" "$BUILD_DIR/posterior.nm"
then
  fail "independent posterior links production collector or solver code"
fi

start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/test_b2r_returned_archive" returned.xsm \
    >harness.log 2>&1
)
then
  sed -n '1,240p' "$CASE_DIR/harness.log" >&2
  fail "synthetic returned-archive harness rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "synthetic harness exceeded 15 seconds"
count_exact 1 '^B2R RETURNED-ARCHIVE SYNTHETIC PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2R SOLVED-ORDER=3,1,2 SOURCE-ORDER=2,3,1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2R COLLECTOR-ACCEPTED=1 REJECTIONS=19$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2R ROOT=RETURNED/1 ROOT-RHO=ABSENT ROOT-K=ABSENT$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2R AX-NEXT=ABSENT CLOSED=ABSENT CHILD-PLANE=ABSENT$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2R DRAGON=0 ASM=0 SPOASM=0 FLU=0 TRANSPORT=0 PICARD=0$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected synthetic harness output line count"
[ -f "$CASE_DIR/returned.xsm" ] || fail "returned XSM evidence missing"
OUTPUT_HASH=$(hash_of "$CASE_DIR/returned.xsm")
OUTPUT_BYTES=$(stat -f '%z' "$CASE_DIR/returned.xsm")
[ "$OUTPUT_BYTES" -gt 0 ] || fail "returned XSM evidence is empty"
chmod 444 "$CASE_DIR/returned.xsm"

start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/check_b2r_returned_archive" returned.xsm \
    >posterior1.log 2>&1
  run_limited "$BUILD_DIR/check_b2r_returned_archive" returned.xsm \
    >posterior2.log 2>&1
)
then
  sed -n '1,240p' "$CASE_DIR/posterior1.log" >&2
  sed -n '1,240p' "$CASE_DIR/posterior2.log" >&2
  fail "independent returned-archive posterior rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "two posterior runs exceeded 15 seconds"
cmp "$CASE_DIR/posterior1.log" "$CASE_DIR/posterior2.log" || \
  fail "independent posterior reports differ"
[ "$(hash_of "$CASE_DIR/returned.xsm")" = "$OUTPUT_HASH" ] || \
  fail "read-only posterior mutated returned XSM"
[ "$(stat -f '%z' "$CASE_DIR/returned.xsm")" -eq "$OUTPUT_BYTES" ] || \
  fail "read-only posterior changed returned XSM size"
count_exact 1 '^B2R RETURNED-ARCHIVE POSTERIOR PASS$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2R R64-FLUX-BITS=15540 R64-SOUR-BITS=15540 R64-QFISS-BITS=15540$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2R R32-FLUX-BITS=15540 R32-SOUR-BITS=15540 R32-QFISS-BITS=15540$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2R TRACK-COPIES=3 MICROLIB2-COPIES=3 SYSTEM-COPIES=3$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2R CHILD-PLANE-ABSENCES=3 SOUR-QFISS-PATH-WITNESSES=15540$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 \
  '^B2R ROOT-RHO=ABSENT ROOT-K=ABSENT AX-NEXT=ABSENT CLOSED=ABSENT$' \
  "$CASE_DIR/posterior1.log"
[ "$(wc -l <"$CASE_DIR/posterior1.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected independent posterior output line count"

PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" >/dev/null
verify_receipts
printf '%s\n' 'SPOR64 PHASE-A9b-B2r RETURNED-ARCHIVE PASS'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2q'
printf '%s\n' 'PLANE-BINDING=LABEL-SET-1,2,3 NOT-ARGUMENT-ORDER'
printf '%s\n' 'COLLECTOR-ACCEPTED=1 REJECTIONS=19 POSTERIOR-RUNS=2'
printf '%s\n' 'R64-FLUX/SOUR/QFISS-BITS=15540/15540/15540'
printf '%s\n' 'R32-FLUX/SOUR/QFISS-BITS=15540/15540/15540'
printf '%s\n' 'SAME-INDEX-COPIES=TRACK:3,MICROLIB2:3,SYSTEM:3'
printf '%s\n' 'ROOT=RETURNED/1 ROOT-RHO=ABSENT ROOT-K=ABSENT'
printf '%s\n' 'AX-NEXT=ABSENT CLOSED/1=NOT-COMMITTED RHO1=NOT-COMPUTED K1=NOT-PUBLISHED'
printf '%s\n' 'DRAGON=0 ASM=0 SPOASM=0 FLU=0 TRANSPORT=0 PICARD=0'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD-CONVERGENCE=NOT-EVALUATED'
printf '%s\n' "RETURNED-XSM-SHA256=$OUTPUT_HASH BYTES=$OUTPUT_BYTES"
