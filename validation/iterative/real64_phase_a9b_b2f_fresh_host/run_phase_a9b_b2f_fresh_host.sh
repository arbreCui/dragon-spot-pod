#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2e_plane1_admission/phase_a9b_b2e_plane1_admission_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2f_fresh_host_receipt.sha256"
CHECKER="$HERE/check_phase_a9b_b2f_fresh_host.py"
EXPECTED_PARENT_COMMIT=bbc188a6b5a268fdb30a7e855e2c3a140ac9d066
EXPECTED_PARENT_HASH=a87f8d14706e6d9f0812f1140b8e2fced59e52c60486860a59c221a963cd2bae
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2f.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2f FAILURE: $*" >&2
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
  [ -f "$PARENT_RECEIPT" ] || fail "parent receipt missing"
  parent_hash=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
  [ "$parent_hash" = "$EXPECTED_PARENT_HASH" ] || \
    fail "parent receipt changed"
  [ -f "$RECEIPT" ] || fail "implementation receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "implementation receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2e parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2e parent commit is not an ancestor"

verify_receipts
[ -f "$CHECKER" ] || fail "independent checker missing"
PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"

# Copy both production modules away from src/ so stale generated .mod files in
# that directory cannot satisfy the changed B2C interface while B2B compiles.
copy_exact "$ROOT/src/SPOR64_B2C.f90" "$SOURCE_DIR/SPOR64_B2C.f90"
copy_exact "$ROOT/src/SPOR64_B2B.f90" "$SOURCE_DIR/SPOR64_B2B.f90"

# Use short local XSM names because GANLIB's LCM filename bridge is 72 bytes.
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

# The validation core intentionally ignores physical-input dummies and is the
# only source compiled with this narrowly scoped warning exception.
"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" \
  -J "$OBJECT_DIR" -c "$HERE/b2f_accept_stubs.f90" \
  -o "$OBJECT_DIR/b2f_accept_stubs.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2B.f90" -o "$OBJECT_DIR/SPOR64_B2B.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$HERE/test_b2f_fresh_host.f90" \
  -o "$OBJECT_DIR/test_b2f_fresh_host.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/b2f_accept_stubs.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2B.o" \
  "$OBJECT_DIR/test_b2f_fresh_host.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2f_fresh_host"

nm -g "$OBJECT_DIR/SPOR64_B2B.o" >"$BUILD_DIR/b2b.nm"
for symbol in \
  ___spomoc_audit_MOD_spomoc_active \
  ___spor64_a9_MOD_flu2dr64_core \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  _xdrta2_; do
  count_exact 1 " U ${symbol}$" "$BUILD_DIR/b2b.nm"
done

nm -g "$OBJECT_DIR/b2f_accept_stubs.o" >"$BUILD_DIR/stubs.nm"
for symbol in \
  ___spomoc_audit_MOD_spomoc_active \
  ___spor64_a9_MOD_flu2dr64_core \
  _xdrta2_; do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/stubs.nm"
done

nm -g "$OBJECT_DIR/SPOR64_B2C.o" >"$BUILD_DIR/b2c.nm"
count_exact 1 ' T ___spor64_b2c_MOD_spor64_b2c_publish$' "$BUILD_DIR/b2c.nm"
nm -g "$BUILD_DIR/test_b2f_fresh_host" >"$BUILD_DIR/harness.nm"
for symbol in \
  ___spor64_b2b_MOD_spor64_b2b_ingress \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  ___spomoc_audit_MOD_spomoc_active \
  ___spor64_a9_MOD_flu2dr64_core \
  _xdrta2_; do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/harness.nm"
done
if grep -Eiq \
  'doorfv|mccgf|mcgmre|spor64_a8|fludrv|flugpi|xdrkin|xdrexp|_dragon|_flu2dr_$' \
  "$BUILD_DIR/harness.nm"; then
  fail "fresh-host harness links a production solver or Dragon component"
fi

(
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2f_fresh_host" \
    seed.xsm macro.xsm track.xsm system.xsm source.xsm \
    >harness.log 2>&1
)
count_exact 1 '^B2F FRESH-HOST PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2F REAL-B2B-CALLS=7$' "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2F STUB-XDRTA2-CALLS=1 STUB-CORE-CALLS=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2F PRODUCTION-PUBLISHER-CALLS=8 COMMITS=1$' \
  "$CASE_DIR/harness.log"
line_count=$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')
[ "$line_count" -eq 4 ] || fail "unexpected harness output line count"

cmp "$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm" \
  "$CASE_DIR/seed.xsm" || fail "FLUX_OLD copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_macro0.xsm" \
  "$CASE_DIR/macro.xsm" || fail "MACRO0 copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_track.xsm" \
  "$CASE_DIR/track.xsm" || fail "TRACK copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_system.xsm" \
  "$CASE_DIR/system.xsm" || fail "SYSTEM copy mutated"
cmp "$ROOT/validation/artifacts/raw-moc-capture/common/restart_source.xsm" \
  "$CASE_DIR/source.xsm" || fail "FSOURCE copy mutated"

PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
  python3 -m unittest -v test_phase_a9b_b2f_fresh_host_contract
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2f FRESH-HOST PASS'
printf '%s\n' 'CLAIM=FRESH-OUTPUT-READ-ONLY-SEED-BOOTSTRAP-CONTRACT-CLOSED'
printf '%s\n' 'CONTRACT-TESTS=47 MUTATION-CASES=46'
printf '%s\n' 'REAL-B2B-CALLS=7 BLOCKED-INGRESS-SCENARIOS=6'
printf '%s\n' 'PRODUCTION-PUBLISHER-CALLS=8 PRODUCTION-PUBLISHER-COMMITS=1'
printf '%s\n' 'PUBLISHER-PREFLIGHT-REJECTIONS=7'
printf '%s\n' 'STUB-XDRTA2-CALLS=1 STUB-CORE-CALLS=1'
printf '%s\n' 'PRODUCTION-XDRTA2-CALLS=0 PRODUCTION-CORE-CALLS=0'
printf '%s\n' 'DRAGON-EXECUTIONS=0 SEQUENTIAL-TRACKING-RECORD-READS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'ORIGINAL-ARTIFACT-MUTATIONS=0 C2M-HOST-EXECUTIONS=0'
printf '%s\n' 'PRODUCTION-EXECUTION-AUTHORIZED=false'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED'
printf '%s\n' 'OUTER-PICARD-CONVERGENCE=NOT-EVALUATED'
