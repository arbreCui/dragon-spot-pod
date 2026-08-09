#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
SOURCE="$ROOT/src/SPOR64_B2W.f90"
LEAKAGE_SOURCE="$ROOT/src/SPOT_LEAKAGE.f90"
SPOLEAK_SOURCE="$ROOT/src/SPOLEAK.f90"
FIXTURE="$HERE/b2w_fixture_support.f90"
STUBS="$HERE/b2w_spoleak_parser_stubs.f90"
HARNESS="$HERE/test_b2w_returned_close.f90"
POSTERIOR="$HERE/check_b2w_returned_close.f90"
STATIC_CHECKER="$HERE/check_phase_a9b_b2w_returned_close.py"
MUTATION_TEST=test_phase_a9b_b2w_returned_close
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2v_one_real_continuation/phase_a9b_b2v_one_real_continuation_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2w_returned_close_receipt.sha256"
EXPECTED_PARENT_COMMIT=607eccf472dfb95fa24b0775f950e4e50eda5efa
EXPECTED_PARENT_HASH=af2b47504adcefc7d1e9fd2ae2ecf4517298e7b5b1be1cd75633ca0fa5482bcb
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2w.XXXXXX")
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2w FAILURE: $*" >&2
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

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2v parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2v parent receipt changed"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2v parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2v parent commit is not an ancestor"
  [ -f "$RECEIPT" ] || fail "B2w contract receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2w contract receipt verification failed"
}

run_limited()
(
  ulimit -c 0
  ulimit -t 15
  ulimit -f 262144
  "$@"
)

[ "$(uname -s)" = Darwin ] || fail "validated platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "validated architecture is arm64"
[ -x "$FC" ] || fail "strict compiler missing"
[ "$($FC --version | sed -n '1p')" = "$EXPECTED_FC_BANNER" ] || \
  fail "unaudited compiler"
for required in "$SOURCE" "$LEAKAGE_SOURCE" "$SPOLEAK_SOURCE" \
  "$FIXTURE" "$STUBS" "$HARNESS" "$POSTERIOR" "$STATIC_CHECKER" \
  "$HERE/$MUTATION_TEST.py"
do
  [ -f "$required" ] || fail "required input missing: $required"
done
verify_receipts

mkdir -p "$OBJECT_DIR" "$CASE_DIR"

if ! PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,220p' "$BUILD_DIR/static.log" >&2
  fail "static returned-close contract rejected"
fi
count_exact 1 '^B2W STATIC RETURNED-CLOSE PASS$' "$BUILD_DIR/static.log"
count_exact 1 '^B2W FEEDBACK-ROOT=EXACT9 OUTPUT-ARCHIVE=EXACT8$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2W L1=BITWISE-PROMOTION L1ERR=EXACT-MAX-DELTA SYSTEM-L0=RETAINED$' \
  "$BUILD_DIR/static.log"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v "$MUTATION_TEST" \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,260p' "$BUILD_DIR/mutations.log" >&2
  fail "returned-close mutation suite rejected"
fi
count_exact 1 '^Ran 17 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all,no-array-temps -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$LEAKAGE_SOURCE" -o "$OBJECT_DIR/SPOT_LEAKAGE.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SPOLEAK_SOURCE" -o "$OBJECT_DIR/SPOLEAK.o"
"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE" -o "$OBJECT_DIR/SPOR64_B2W.o"
"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$FIXTURE" -o "$OBJECT_DIR/b2w_fixture_support.o"
"$FC" $FLAGS -J "$OBJECT_DIR" \
  -c "$STUBS" -o "$OBJECT_DIR/b2w_spoleak_parser_stubs.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$HARNESS" -o "$OBJECT_DIR/test_b2w_returned_close.o"
"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$POSTERIOR" -o "$OBJECT_DIR/check_b2w_returned_close.o"

"$FC" -O0 -g -fcheck=all,no-array-temps -fbacktrace \
  "$OBJECT_DIR/SPOT_LEAKAGE.o" "$OBJECT_DIR/SPOLEAK.o" \
  "$OBJECT_DIR/SPOR64_B2W.o" "$OBJECT_DIR/b2w_fixture_support.o" \
  "$OBJECT_DIR/b2w_spoleak_parser_stubs.o" \
  "$OBJECT_DIR/test_b2w_returned_close.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2w_returned_close"
"$FC" -O0 -g -fcheck=all,no-array-temps -fbacktrace \
  "$OBJECT_DIR/check_b2w_returned_close.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/check_b2w_returned_close"

nm -g "$BUILD_DIR/test_b2w_returned_close" >"$BUILD_DIR/harness.nm"
if grep -Eiq '(^|[[:space:]])_?(dragon|asm|asmdrv|spoasm|flu|fludrv|flu2dr|flugpi|spomoc|mccgf|mcgmre|xdrta2|xdrkin|xdrexp)_$' \
  "$BUILD_DIR/harness.nm"
then
  fail "harness links Dragon, ASM, FLU, transport, or Picard code"
fi
nm -g "$BUILD_DIR/check_b2w_returned_close" >"$BUILD_DIR/posterior.nm"
if grep -Eiq 'spor64_b2[wr]|(^|[[:space:]])_?(spoleak|dragon|asm|asmdrv|spoasm|flu|fludrv|flu2dr|flugpi|spomoc|mccgf|mcgmre|xdrta2|xdrkin|xdrexp)_$' \
  "$BUILD_DIR/posterior.nm"
then
  fail "posterior links B2W, B2R, SPOLEAK, or solver code"
fi

start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/test_b2w_returned_close" \
    ax_input.xsm feedback_input.xsm ax_closed.xsm archive_closed.xsm \
    >harness.log 2>&1
)
then
  sed -n '1,260p' "$CASE_DIR/harness.log" >&2
  fail "synthetic returned-close harness rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "synthetic harness exceeded 15 seconds"
count_exact 1 '^SPOLEAK ITER K ' "$CASE_DIR/harness.log"
count_exact 1 '^SPOLEAK DIRECT ERROR/MIN/MAX ' "$CASE_DIR/harness.log"
count_exact 1 '^B2W RETURNED-CLOSE SYNTHETIC PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2W REAL-SPOLEAK-CALLS=1 REDGET=2 REDPUT=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2W CLOSES=1 REJECTIONS=25 ZERO-WRITE=25$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2W ROOT-INPUT=EXACT9 ROOT-OUTPUT=EXACT8 L1ERR=DROPPED$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2W DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 8 ] || \
  fail "unexpected harness output line count"

EVIDENCE='ax_input.xsm feedback_input.xsm ax_closed.xsm archive_closed.xsm'
for file in $EVIDENCE
do
  [ -s "$CASE_DIR/$file" ] || fail "XSM evidence missing: $file"
  eval "HASH_$(printf '%s' "$file" | tr '.-' '__')=$(hash_of "$CASE_DIR/$file")"
  chmod 444 "$CASE_DIR/$file"
done

start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/check_b2w_returned_close" $EVIDENCE \
    >posterior1.log 2>&1
  run_limited "$BUILD_DIR/check_b2w_returned_close" $EVIDENCE \
    >posterior2.log 2>&1
)
then
  sed -n '1,260p' "$CASE_DIR/posterior1.log" >&2
  sed -n '1,260p' "$CASE_DIR/posterior2.log" >&2
  fail "independent posterior rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "two posterior runs exceeded 15 seconds"
cmp "$CASE_DIR/posterior1.log" "$CASE_DIR/posterior2.log" || \
  fail "posterior reports differ"
count_exact 1 '^B2W RETURNED-CLOSE POSTERIOR PASS$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2W AUTHORITY64-BITS=46620 MIRROR32-BITS=46620$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2W LEAKAGE-PROMOTIONS=1110 SYSTEM-L0-GROUPS=1110$' \
  "$CASE_DIR/posterior1.log"
count_exact 1 '^B2W FOUR-LIST-DEEP-COPIES=12$' \
  "$CASE_DIR/posterior1.log"
[ "$(wc -l <"$CASE_DIR/posterior1.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected posterior output line count"

for file in $EVIDENCE
do
  current=$(hash_of "$CASE_DIR/$file")
  eval "before=\$HASH_$(printf '%s' "$file" | tr '.-' '__')"
  [ "$current" = "$before" ] || fail "posterior mutated $file"
done

PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER" >/dev/null
verify_receipts
printf '%s\n' 'SPOR64 PHASE-A9b-B2w RETURNED-CLOSE PASS'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2v'
printf '%s\n' 'CLAIM=SYNTHETIC-RETURNED-CLOSE-WITH-ONE-REAL-SPOLEAK-CALL'
printf '%s\n' 'CLOSES=1 REJECTIONS=25 ZERO-WRITE=25 POSTERIOR-RUNS=2'
printf '%s\n' 'FEEDBACK=RETURNED/1-EXACT9 OUTPUT=CLOSED/1-EXACT8'
printf '%s\n' 'RHO0=CHILD-RETAINED RHO1=AX-RECIPROCAL ROOT-COMMITTED'
printf '%s\n' 'L1ERR=EXACT-MAX-DELTA-THEN-DROPPED SYSTEM-L0=RETAINED'
printf '%s\n' 'DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0'
printf '%s\n' 'TEMPORARY-PRODUCTS=CLEANED-ON-EXIT'
