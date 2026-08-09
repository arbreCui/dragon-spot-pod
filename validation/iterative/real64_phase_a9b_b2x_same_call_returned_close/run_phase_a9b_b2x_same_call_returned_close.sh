#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
B2W_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2w_returned_close"
C2M_HELPER="$ROOT/validation/iterative/real64_phase_a9b_b2k_system_assembly/compile_c2m.c"
PARENT_RECEIPT="$B2W_DIR/phase_a9b_b2w_returned_close_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2x_same_call_returned_close_receipt.sha256"
EXPECTED_PARENT_COMMIT=afd2a6cbe313e711ba8aee40a13a3a698fa950fc
EXPECTED_PARENT_HASH=aab4770ea79d6f0c9338fa765e389f3e6847937a7b2aa4d8a46edc9d4ec63948
FC=/opt/homebrew/bin/gfortran
CC=/usr/bin/cc
CPP=/usr/bin/cpp
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2x.XXXXXX")
ADAPTER_DIR="$BUILD_DIR/adapter"
REAL_DIR="$BUILD_DIR/real"
HOST_DIR="$BUILD_DIR/host"
C2M_DIR="$BUILD_DIR/c2m"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2x FAILURE: $*" >&2
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

run_limited()
(
  ulimit -c 0
  ulimit -t 15
  ulimit -f 262144
  "$@"
)

verify_lineage()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2w parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2w parent receipt changed"
  git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
    fail "B2w parent commit missing"
  git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
    fail "B2w parent commit is not an ancestor"
}

verify_receipt()
{
  if [ -f "$RECEIPT" ]; then
    grep -q '"receipt": "frozen"' "$HERE/precision_manifest.json" || \
      fail "receipt exists but manifest is not frozen"
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2x contract receipt verification failed"
    RECEIPT_STATE=FROZEN
  else
    grep -q '"receipt": "pending"' "$HERE/precision_manifest.json" || \
      fail "missing receipt without pending manifest"
    RECEIPT_STATE=PENDING-MAIN-AUDIT
  fi
}

[ "$(uname -s)" = Darwin ] || fail "validated platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "validated architecture is arm64"
[ -x "$FC" ] || fail "strict compiler missing"
[ -x "$CC" ] || fail "C compiler missing"
[ -x "$CPP" ] || fail "preprocessor missing"
[ "$($FC --version | sed -n '1p')" = "$EXPECTED_FC_BANNER" ] || \
  fail "unaudited compiler"

for required in \
  "$ROOT/data/SpotCloseR64.c2m" \
  "$ROOT/src/Makefile" "$ROOT/src/.dragon_deps.mk" \
  "$ROOT/script/make_depend.py" \
  "$ROOT/src/SPOR64_B2W.f90" "$ROOT/src/SPOR64_B2X.f90" \
  "$ROOT/src/SPOT_LEAKAGE.f90" "$ROOT/src/SPOLEAK.f90" \
  "$ROOT/src/SPOSTATE.f90" "$ROOT/src/ASM.f" "$ROOT/src/FLU.f" \
  "$ROOT/src/FLU2DR.f" "$ROOT/src/KDRDRV.F" \
  "$B2W_DIR/b2w_fixture_support.f90" \
  "$B2W_DIR/check_b2w_returned_close.f90" \
  "$HERE/b2x_adapter_probes.f90" "$HERE/b2x_adapter_stubs.f90" \
  "$HERE/b2x_real_parser_stubs.f90" "$HERE/test_spor64x_adapter.f90" \
  "$HERE/test_b2x_real_close.f90" \
  "$HERE/check_phase_a9b_b2x_same_call_returned_close.py" \
  "$HERE/test_phase_a9b_b2x_same_call_returned_close.py" \
  "$HERE/b2x_stub_off.c2m" "$HERE/b2x_stub_on.c2m" \
  "$HERE/README.md" "$HERE/precision_manifest.json" "$C2M_HELPER" \
  "$ROOT/Ganlib/src/cle2000.h" "$ROOT/Ganlib/src/lcm.h" \
  "$ROOT/Ganlib/src/xsm.h" "$ROOT/Ganlib/src/kdi.h" \
  "$ROOT/Ganlib/src/ganlib.h"
do
  [ -f "$required" ] || fail "required input missing: $required"
done

verify_lineage
verify_receipt
git -C "$ROOT" diff --check || fail "whitespace errors"
mkdir -p "$ADAPTER_DIR" "$REAL_DIR" "$HOST_DIR" "$C2M_DIR" "$CASE_DIR"

if ! PYTHONDONTWRITEBYTECODE=1 python3 \
  "$HERE/check_phase_a9b_b2x_same_call_returned_close.py" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,260p' "$BUILD_DIR/static.log" >&2
  fail "static same-call returned-close contract rejected"
fi
count_exact 1 '^B2X STATIC SAME-CALL RETURNED-CLOSE PASS$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2X HOST=COPY->SPOR64V->ASM->FLU->SPOSTATE->SPOLEAK->SPOR64X$' \
  "$BUILD_DIR/static.log"
count_exact 1 '^B2X DEPLOYMENT-DEFAULT=OFF SHIPPED-SELECTIONS=0$' \
  "$BUILD_DIR/static.log"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v test_phase_a9b_b2x_same_call_returned_close \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,300p' "$BUILD_DIR/mutations.log" >&2
  fail "B2x mutation suite rejected"
fi
count_exact 1 '^Ran 34 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"

STRICT_FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
STRICT_FLAGS="$STRICT_FLAGS -fimplicit-none -fcheck=all,no-array-temps"
STRICT_FLAGS="$STRICT_FLAGS -fbacktrace -ffp-contract=off -fno-fast-math"
FIXED_FLAGS='-O0 -g -std=legacy -ffixed-line-length-none'
FIXED_FLAGS="$FIXED_FLAGS -Wall -Wextra -Werror"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"

# Compile and execute the thin adapters against a capture-only B2W module.
"$FC" $STRICT_FLAGS -J "$ADAPTER_DIR" \
  -c "$HERE/b2x_adapter_probes.f90" \
  -o "$ADAPTER_DIR/b2x_adapter_probes.o"
"$FC" $STRICT_FLAGS -I "$ADAPTER_DIR" -J "$ADAPTER_DIR" \
  -c "$HERE/b2x_adapter_stubs.f90" \
  -o "$ADAPTER_DIR/b2x_adapter_stubs.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -I "$ADAPTER_DIR" -J "$ADAPTER_DIR" \
  -c "$ROOT/src/SPOR64_B2X.f90" -o "$ADAPTER_DIR/SPOR64_B2X.o"
"$FC" $STRICT_FLAGS -I "$ADAPTER_DIR" -J "$ADAPTER_DIR" \
  -c "$HERE/test_spor64x_adapter.f90" \
  -o "$ADAPTER_DIR/test_spor64x_adapter.o"
"$FC" -O0 -g -fcheck=all,no-array-temps -fbacktrace \
  "$ADAPTER_DIR/b2x_adapter_probes.o" \
  "$ADAPTER_DIR/b2x_adapter_stubs.o" "$ADAPTER_DIR/SPOR64_B2X.o" \
  "$ADAPTER_DIR/test_spor64x_adapter.o" \
  -o "$BUILD_DIR/test_spor64x_adapter"

# Compile the real read-only admission, one real SPOLEAK, and the B2W close.
"$FC" $STRICT_FLAGS -I "$GANMOD" -J "$REAL_DIR" \
  -c "$ROOT/src/SPOT_LEAKAGE.f90" -o "$REAL_DIR/SPOT_LEAKAGE.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -I "$REAL_DIR" -J "$REAL_DIR" \
  -c "$ROOT/src/SPOLEAK.f90" -o "$REAL_DIR/SPOLEAK.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -J "$REAL_DIR" \
  -c "$ROOT/src/SPOR64_B2W.f90" -o "$REAL_DIR/SPOR64_B2W.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -I "$REAL_DIR" -J "$REAL_DIR" \
  -c "$ROOT/src/SPOR64_B2X.f90" -o "$REAL_DIR/SPOR64_B2X.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -J "$REAL_DIR" \
  -c "$B2W_DIR/b2w_fixture_support.f90" \
  -o "$REAL_DIR/b2w_fixture_support.o"
"$FC" $STRICT_FLAGS -J "$REAL_DIR" \
  -c "$HERE/b2x_real_parser_stubs.f90" \
  -o "$REAL_DIR/b2x_real_parser_stubs.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -I "$REAL_DIR" -J "$REAL_DIR" \
  -c "$HERE/test_b2x_real_close.f90" \
  -o "$REAL_DIR/test_b2x_real_close.o"
"$FC" $STRICT_FLAGS -I "$GANMOD" -J "$REAL_DIR" \
  -c "$B2W_DIR/check_b2w_returned_close.f90" \
  -o "$REAL_DIR/check_b2w_returned_close.o"
"$FC" -O0 -g -fcheck=all,no-array-temps -fbacktrace \
  "$REAL_DIR/SPOT_LEAKAGE.o" "$REAL_DIR/SPOLEAK.o" \
  "$REAL_DIR/SPOR64_B2W.o" "$REAL_DIR/SPOR64_B2X.o" \
  "$REAL_DIR/b2w_fixture_support.o" \
  "$REAL_DIR/b2x_real_parser_stubs.o" \
  "$REAL_DIR/test_b2x_real_close.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/test_b2x_real_close"
"$FC" -O0 -g -fcheck=all,no-array-temps -fbacktrace \
  "$REAL_DIR/check_b2w_returned_close.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/check_b2w_returned_close"

# Compile, but never link or execute, the production axial host sources.
"$FC" $STRICT_FLAGS -Wno-unused-dummy-argument \
  -I "$GANMOD" -I "$REAL_DIR" -J "$HOST_DIR" \
  -c "$ROOT/src/SPOSTATE.f90" -o "$HOST_DIR/SPOSTATE.o"
"$FC" $FIXED_FLAGS -cpp -I "$GANMOD" -c "$ROOT/src/ASM.f" \
  -o "$HOST_DIR/ASM.o"
"$FC" $FIXED_FLAGS -I "$GANMOD" -c "$ROOT/src/FLU.f" \
  -o "$HOST_DIR/FLU.o"
"$FC" $FIXED_FLAGS -Wno-compare-reals -I "$GANMOD" \
  -c "$ROOT/src/FLU2DR.f" -o "$HOST_DIR/FLU2DR.o"
"$CPP" -P -W -traditional -DLinux -DUnix "$ROOT/src/KDRDRV.F" \
  "$HOST_DIR/KDRDRV.pp.f"
"$FC" $FIXED_FLAGS -I "$GANMOD" -c "$HOST_DIR/KDRDRV.pp.f" \
  -o "$HOST_DIR/KDRDRV.o"

# Independently confirm the generated module dependency.
(
  cd "$ROOT/src"
  PYTHONDONTWRITEBYTECODE=1 python3 ../script/make_depend.py --make-deps \
    ./*.f90 ./*.F90 2>/dev/null
) >"$BUILD_DIR/generated-deps.txt"
count_exact 1 '^SPOR64_B2X.o: SPOR64_B2W.o$' "$BUILD_DIR/generated-deps.txt"
count_exact 1 '^SPOR64_B2X.o: SPOR64_B2W.o$' "$ROOT/src/.dragon_deps.mk"

# Use the real CLEPIL/OBJPIL compiler for the procedure and both selection
# shapes. Compilation dispatches no production module.
"$CC" -std=c11 -pedantic -Wall -Wextra -Werror -I "$ROOT/Ganlib/src" \
  -c "$C2M_HELPER" -o "$C2M_DIR/compile_c2m.o"
"$FC" "$C2M_DIR/compile_c2m.o" "$GANLIB" -o "$C2M_DIR/compile_c2m"
for item in \
  "$ROOT/data/SpotCloseR64.c2m:SpotCloseR64.o2m" \
  "$HERE/b2x_stub_off.c2m:b2x_stub_off.o2m" \
  "$HERE/b2x_stub_on.c2m:b2x_stub_on.o2m"
do
  source=${item%:*}
  object=${item#*:}
  if ! (
    cd "$C2M_DIR"
    run_limited ./compile_c2m "$source" "$object" \
      >"$object.log" 2>&1
  )
  then
    sed -n '1,240p' "$C2M_DIR/$object.log" >&2
    fail "CLEPIL/OBJPIL compilation failed: $source"
  fi
  [ -s "$C2M_DIR/$object" ] || fail "empty C2M object: $object"
done

nm -g "$BUILD_DIR/test_spor64x_adapter" >"$BUILD_DIR/adapter.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(dragon|asm|asmdrv|spoasm|flu[a-z0-9_]*|spostate|spoleak|spomoc|mccgf|mcgmre|xdrta2|xdrkin|xdrexp)_$' \
  "$BUILD_DIR/adapter.nm"
then
  fail "adapter witness links solver or leakage code"
fi
nm -g "$BUILD_DIR/test_b2x_real_close" >"$BUILD_DIR/real.nm"
if grep -Eiq \
  '(^|[[:space:]])_?(dragon|asm|asmdrv|spoasm|flu[a-z0-9_]*|spostate|spomoc|mccgf|mcgmre|xdrta2|xdrkin|xdrexp)_$' \
  "$BUILD_DIR/real.nm"
then
  fail "real synthetic witness links axial solver or transport code"
fi
nm -g "$BUILD_DIR/check_b2w_returned_close" >"$BUILD_DIR/posterior.nm"
if grep -Eiq \
  'spor64_b2[wx]|(^|[[:space:]])_?(spoleak|dragon|asm|asmdrv|spoasm|flu[a-z0-9_]*|spostate|spomoc|mccgf|mcgmre|xdrta2|xdrkin|xdrexp)_$' \
  "$BUILD_DIR/posterior.nm"
then
  fail "posterior links production close, leakage, or solver code"
fi

if ! run_limited "$BUILD_DIR/test_spor64x_adapter" \
  >"$BUILD_DIR/adapter.log" 2>&1
then
  sed -n '1,220p' "$BUILD_DIR/adapter.log" >&2
  fail "adapter capture witness rejected"
fi
count_exact 1 '^B2X SPOR64X ADAPTER CAPTURE PASS$' "$BUILD_DIR/adapter.log"
count_exact 1 '^B2X SPOR64V ADAPTER CAPTURE PASS$' "$BUILD_DIR/adapter.log"
count_exact 1 '^B2X ADAPTER-CALLS=15 REAL-B2W=0 ASM=0 FLU=0 SPOSTATE=0$' \
  "$BUILD_DIR/adapter.log"
[ "$(wc -l <"$BUILD_DIR/adapter.log" | tr -d '[:space:]')" -eq 5 ] || \
  fail "unexpected adapter output line count"

start_seconds=$(date +%s)
if ! (
  cd "$CASE_DIR"
  run_limited "$BUILD_DIR/test_b2x_real_close" \
    ax_input.xsm feedback_input.xsm ax_closed.xsm archive_closed.xsm \
    >harness.log 2>&1
)
then
  sed -n '1,260p' "$CASE_DIR/harness.log" >&2
  fail "real synthetic close witness rejected"
fi
elapsed_seconds=$(($(date +%s)-start_seconds))
[ "$elapsed_seconds" -le 15 ] || fail "synthetic witness exceeded 15 seconds"
count_exact 1 '^SPOLEAK ITER K ' "$CASE_DIR/harness.log"
count_exact 1 '^SPOLEAK DIRECT ERROR/MIN/MAX ' "$CASE_DIR/harness.log"
count_exact 1 '^B2X REAL-SPOLEAK-B2W-SPOR64X SYNTHETIC PASS$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2X REAL-RETURNED-ADMISSION SUCCESS=1 L0-REJECTION=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2X CLOSES=1 REJECTIONS=1 ZERO-WRITE=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2X ASM=0 FLU=0 SPOSTATE=0 DRAGON=0 TRANSPORT=0 PICARD=0$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 8 ] || \
  fail "unexpected synthetic witness output line count"

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
[ "$(wc -l <"$CASE_DIR/posterior1.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected posterior output line count"

for file in $EVIDENCE
do
  current=$(hash_of "$CASE_DIR/$file")
  eval "before=\$HASH_$(printf '%s' "$file" | tr '.-' '__')"
  [ "$current" = "$before" ] || fail "posterior mutated $file"
done

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$HERE/check_phase_a9b_b2x_same_call_returned_close.py" >/dev/null
verify_lineage
verify_receipt
printf '%s\n' 'SPOR64 PHASE-A9b-B2x SAME-CALL RETURNED-CLOSE PASS'
printf '%s\n' "RECEIPT=$RECEIPT_STATE PARENT=B2w"
printf '%s\n' 'STATIC-TESTS=34 C2M-COMPILES=3 PRODUCTION-COMPILE-ONLY=5'
printf '%s\n' 'ADAPTER-CALLS=15 SPOR64V=CAPTURED SPOR64X=CAPTURED'
printf '%s\n' 'RETURNED-ADMISSION=SUCCESS1,L0-REJECTION1,BITWISE-GROUPS1110'
printf '%s\n' 'CLOSES=1 TERMINAL-REJECTIONS=1 ZERO-WRITE=1 SPOLEAK=1'
printf '%s\n' 'POSTERIOR-RUNS=2 AUTHORITY64=46620 MIRROR32=46620'
printf '%s\n' 'ASM=0 FLU=0 SPOSTATE=0 DRAGON=0 TRANSPORT=0 PICARD=0'
printf '%s\n' 'TEMPORARY-PRODUCTS=CLEANED-ON-EXIT'
