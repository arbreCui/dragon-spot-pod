#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2o_cont_binding_cutoff/phase_a9b_b2o_cont_binding_cutoff_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2p_solved_lifecycle_receipt.sha256"
EXPECTED_PARENT_COMMIT=e5fe1490b93060ffe516f7a40fadee7012f888d8
EXPECTED_PARENT_HASH=2ccb78da1d0a9660f303f1003ad51b5e6cc4da43ce64ff035fe4d450de195271
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2p.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
PARENT_SOURCE_DIR="$BUILD_DIR/parent-source"
PARENT_MODULE_DIR="$BUILD_DIR/parent-modules"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2p FAILURE: $*" >&2
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

copy_exact()
{
  source_path=$1
  target_path=$2
  cp "$source_path" "$target_path"
  cmp "$source_path" "$target_path" || fail "copy differs: $target_path"
}

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2o parent receipt missing"
  parent_hash=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
  [ "$parent_hash" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2o parent receipt changed"
  [ -f "$RECEIPT" ] || fail "B2p implementation receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2p implementation receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$($FC --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2o parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2o parent commit is not an ancestor"
verify_receipts

for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2H
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
[ -f "$HERE/b2p_capture_stubs.f90" ] || fail "capture stubs missing"
[ -f "$HERE/test_b2p_solved_lifecycle.f90" ] || fail "harness missing"
[ -f "$HERE/legacy_b2c_abi_caller.f90" ] || fail "legacy ABI caller missing"
[ -f "$HERE/check_phase_a9b_b2p_solved_lifecycle.py" ] || \
  fail "static contract checker missing"
[ -f "$HERE/test_phase_a9b_b2p_solved_lifecycle_contract.py" ] || \
  fail "contract mutation tests missing"

if ! PYTHONDONTWRITEBYTECODE=1 \
  python3 "$HERE/check_phase_a9b_b2p_solved_lifecycle.py" \
  >"$BUILD_DIR/static.log" 2>&1
then
  sed -n '1,160p' "$BUILD_DIR/static.log" >&2
  fail "static SOLVED-lifecycle contract rejected"
fi
count_exact 1 '^B2P STATIC SOLVED-LIFECYCLE PASS$' "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2P COPIER-CONTRACT=SEALED-PROJECTED\(N\)->ACCEPTED-SOLVED\(N\)$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2P PRODUCTION-ROUTE=PROJECTED/1->SOLVED/1$' \
  "$BUILD_DIR/static.log"
count_exact 1 \
  '^B2P B2H=SOLVED\(N\)->PROJECTED\(N\+1\) CONSUMER-ONLY$' \
  "$BUILD_DIR/static.log"

if ! (
  cd "$HERE"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
    python3 -m unittest -v \
    test_phase_a9b_b2p_solved_lifecycle_contract \
    >"$BUILD_DIR/mutations.log" 2>&1
)
then
  sed -n '1,200p' "$BUILD_DIR/mutations.log" >&2
  fail "SOLVED-lifecycle contract mutation suite rejected"
fi
count_exact 1 '^Ran 35 tests in [0-9.]+s$' "$BUILD_DIR/mutations.log"
count_exact 1 '^OK$' "$BUILD_DIR/mutations.log"
verify_receipts

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$PARENT_SOURCE_DIR" \
  "$PARENT_MODULE_DIR" "$CASE_DIR"
for source in SPOR64_B2C SPOR64_B2B SPOR64_B2O SPOR64_B2H
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done

copy_exact \
  "$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm" \
  "$CASE_DIR/seed.xsm"
copy_exact \
  "$ROOT/validation/artifacts/raw-moc-capture/common/restart_macro0.xsm" \
  "$CASE_DIR/macro.xsm"
copy_exact \
  "$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm" \
  "$CASE_DIR/track.xsm"
copy_exact \
  "$ROOT/validation/artifacts/raw-moc-capture/common/restart_system.xsm" \
  "$CASE_DIR/system.xsm"
copy_exact \
  "$ROOT/validation/artifacts/raw-moc-capture/common/restart_source.xsm" \
  "$CASE_DIR/source.xsm"
chmod 444 "$CASE_DIR/seed.xsm" "$CASE_DIR/macro.xsm" \
  "$CASE_DIR/track.xsm" "$CASE_DIR/system.xsm" "$CASE_DIR/source.xsm"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

git -C "$ROOT" show \
  "$EXPECTED_PARENT_COMMIT:src/SPOR64_B2C.f90" \
  >"$PARENT_SOURCE_DIR/SPOR64_B2C.f90"
[ -s "$PARENT_SOURCE_DIR/SPOR64_B2C.f90" ] || \
  fail "parent B2C source extraction failed"
"$FC" $FLAGS -I "$GANMOD" -J "$PARENT_MODULE_DIR" \
  -c "$PARENT_SOURCE_DIR/SPOR64_B2C.f90" \
  -o "$PARENT_MODULE_DIR/SPOR64_B2C-parent.o"
"$FC" $FLAGS -I "$PARENT_MODULE_DIR" -I "$GANMOD" \
  -J "$PARENT_MODULE_DIR" -c "$HERE/legacy_b2c_abi_caller.f90" \
  -o "$PARENT_MODULE_DIR/legacy_b2c_abi_caller.o"

"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" \
  -J "$OBJECT_DIR" -c "$HERE/b2p_capture_stubs.f90" \
  -o "$OBJECT_DIR/b2p_capture_stubs.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
nm -g "$OBJECT_DIR/SPOR64_B2C.o" >"$BUILD_DIR/b2c.nm"
count_exact 1 '___spor64_b2c_MOD_spor64_b2c_publish$' "$BUILD_DIR/b2c.nm"
count_exact 1 '___spor64_b2c_MOD_spor64_b2c_publish_cont$' "$BUILD_DIR/b2c.nm"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$PARENT_MODULE_DIR/legacy_b2c_abi_caller.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/legacy_b2c_abi_caller"
"$BUILD_DIR/legacy_b2c_abi_caller" >"$BUILD_DIR/legacy-abi.log" 2>&1
count_exact 1 '^B2P LEGACY-PARENT-MOD-CALLER PASS$' \
  "$BUILD_DIR/legacy-abi.log"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2B.f90" -o "$OBJECT_DIR/SPOR64_B2B.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2O.f90" -o "$OBJECT_DIR/SPOR64_B2O.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2H.f90" -o "$OBJECT_DIR/SPOR64_B2H.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$HERE/test_b2p_solved_lifecycle.f90" \
  -o "$OBJECT_DIR/test_b2p_solved_lifecycle.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/b2p_capture_stubs.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2B.o" \
  "$OBJECT_DIR/SPOR64_B2O.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" \
  "$OBJECT_DIR/test_b2p_solved_lifecycle.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2p_solved_lifecycle"

nm -g "$BUILD_DIR/test_b2p_solved_lifecycle" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|spor64_a8|fludrv|flugpi|xdrkin|xdrexp|_dragon|_flu2dr_$' \
  "$BUILD_DIR/harness.nm"
then
  fail "B2p harness links a production solver, FLU, or Dragon component"
fi

if ! (
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2p_solved_lifecycle" \
    seed.xsm macro.xsm track.xsm system.xsm source.xsm \
    >harness.log 2>&1
)
then
  sed -n '1,200p' "$CASE_DIR/harness.log" >&2
  fail "SOLVED-lifecycle harness rejected"
fi
count_exact 1 '^B2P SOLVED-LIFECYCLE PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2P REAL-B2B-CONT=3 STUB-CORE=3 STUB-XDRTA2=3$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2P SOLVED-TYPE4-BITS=10360 SOLVED-MIRROR-BITS=10360$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2P PROJECTED-TYPE4-BITS=5180 PROJECTED-MIRROR-BITS=5180$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2P LEGACY-COMMITS=1 METADATA-REJECTIONS=16 ALIAS-REJECTIONS=1 TOKEN-REJECTIONS=1 CORE-REJECTIONS=2$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2P EPOCH=1->2 B2H-PLANE-CARRYOVER=NOT-PRESENT$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 6 ] || \
  fail "unexpected harness output line count"

cmp "$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm" \
  "$CASE_DIR/seed.xsm" || fail "FLUX_OLD artifact copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_macro0.xsm" \
  "$CASE_DIR/macro.xsm" || fail "MACRO0 artifact copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm" \
  "$CASE_DIR/track.xsm" || fail "TRACK artifact copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_system.xsm" \
  "$CASE_DIR/system.xsm" || fail "SYSTEM artifact copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_source.xsm" \
  "$CASE_DIR/source.xsm" || fail "FSOURCE artifact copy mutated"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2p SOLVED-LIFECYCLE PASS'
printf '%s\n' 'CHAIN=B2O-SEAL->REAL-B2B-CONT->B2C-SOLVED/1->B2H-PROJECTED/2'
printf '%s\n' 'LIFECYCLE-PUBLICATION=PROJECTED/1->SOLVED/1'
printf '%s\n' 'B2H-PROJECTED/2=SCHEMA-PROBE-ONLY'
printf '%s\n' 'REAL-B2B-CONT=3 STUB-CORE=3 STUB-XDRTA2=3'
printf '%s\n' 'STATIC-CONTRACT-TESTS=35'
printf '%s\n' 'LEGACY-PARENT-MOD-CALLER=1 SEALED-SEED-FULL-VERIFICATIONS=5'
printf '%s\n' 'LEGACY-B2C-COMMITS=1 METADATA-PREFLIGHT-REJECTIONS=16'
printf '%s\n' 'ALIAS-PREFLIGHT-REJECTIONS=1 TOKEN-PREFLIGHT-REJECTIONS=1'
printf '%s\n' 'CORE-RESULT-REJECTIONS=2'
printf '%s\n' 'PRODUCTION-FLU-EXECUTIONS=0 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'B2H-PLANE-CARRYOVER=NOT-PRESENT SECOND-CONT=NOT-CLOSED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
