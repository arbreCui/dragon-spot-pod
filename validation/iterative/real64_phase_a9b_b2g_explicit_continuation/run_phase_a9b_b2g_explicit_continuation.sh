#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2f_fresh_host/phase_a9b_b2f_fresh_host_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2g_explicit_continuation_receipt.sha256"
EXPECTED_PARENT_COMMIT=2dc5a870470c2e689e505d583ab6aca8a87d2fa4
EXPECTED_PARENT_HASH=1d0716cb3963fef0550b63db618d1da1a5abc8d72e5d71a8e73b1b951c2c6845
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2g.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
PARSER_DIR="$BUILD_DIR/parser"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2g FAILURE: $*" >&2
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
  fail "B2f parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2f parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$HERE/check_phase_a9b_b2g_explicit_continuation.py"
verify_receipts
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  test_phase_a9b_b2g_explicit_continuation_contract

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR" "$PARSER_DIR"
copy_exact "$ROOT/src/SPOR64_B2C.f90" "$SOURCE_DIR/SPOR64_B2C.f90"
copy_exact "$ROOT/src/SPOR64_B2B.f90" "$SOURCE_DIR/SPOR64_B2B.f90"
copy_exact "$ROOT/src/FLU.f" "$SOURCE_DIR/FLU.f"

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

"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" \
  -J "$OBJECT_DIR" -c "$HERE/b2g_capture_stubs.f90" \
  -o "$OBJECT_DIR/b2g_capture_stubs.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2B.f90" -o "$OBJECT_DIR/SPOR64_B2B.o"
"$FC" -O0 -g -std=legacy -pedantic-errors -Wall -Wextra -Werror \
  -ffixed-line-length-72 -fcheck=all -fbacktrace -ffp-contract=off \
  -fno-fast-math -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/FLU.f" -o "$OBJECT_DIR/FLU.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$HERE/test_b2g_explicit_continuation.f90" \
  -o "$OBJECT_DIR/test_b2g_explicit_continuation.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/b2g_capture_stubs.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2B.o" \
  "$OBJECT_DIR/test_b2g_explicit_continuation.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2g_explicit_continuation"

nm -g "$OBJECT_DIR/SPOR64_B2B.o" >"$BUILD_DIR/b2b.nm"
for symbol in \
  ___spomoc_audit_MOD_spomoc_active \
  ___spor64_a9_MOD_flu2dr64_core \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  _xdrta2_; do
  count_exact 1 " U ${symbol}$" "$BUILD_DIR/b2b.nm"
done
nm -g "$BUILD_DIR/test_b2g_explicit_continuation" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|spor64_a8|fludrv|flugpi|xdrkin|xdrexp|_dragon|_flu2dr_$' \
  "$BUILD_DIR/harness.nm"; then
  fail "continuation harness links a production solver or Dragon component"
fi

(
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2g_explicit_continuation" \
    seed.xsm macro.xsm track.xsm system.xsm source.xsm \
    >harness.log 2>&1
)
count_exact 1 '^B2G EXPLICIT-CONTINUATION PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2G REAL-B2B-CALLS=13 REJECTIONS=11$' "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2G STUB-XDRTA2-CALLS=2 STUB-CORE-CALLS=2$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2G TYPE4-POISON-PROOF=BITWISE$' "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 4 ] || \
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

# Execute the real FLUGPI parser against a deterministic token/LCM shim.
"$FC" $FLAGS -I "$PARSER_DIR" -J "$PARSER_DIR" \
  -c "$HERE/b2g_synthetic_ganlib.f90" \
  -o "$PARSER_DIR/b2g_synthetic_ganlib.o"
"$FC" -O0 -g -std=legacy -pedantic-errors -ffixed-line-length-72 \
  -fcheck=all -fbacktrace -ffp-contract=off -fno-fast-math \
  -I "$PARSER_DIR" -J "$PARSER_DIR" -c "$ROOT/src/FLUGPI.f" \
  -o "$PARSER_DIR/FLUGPI.o"
if nm -g "$PARSER_DIR/FLUGPI.o" | \
  grep -Eiq 'lcmput|lcmptc|lcmpdl|lcmppd|lcmlid|lcmdid'; then
  fail "parser exposes a GANLIB write symbol"
fi
"$FC" $FLAGS -I "$PARSER_DIR" -J "$PARSER_DIR" \
  -c "$HERE/b2g_parser_driver.f90" -o "$PARSER_DIR/b2g_parser_driver.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$PARSER_DIR/b2g_synthetic_ganlib.o" "$PARSER_DIR/FLUGPI.o" \
  "$PARSER_DIR/b2g_parser_driver.o" -o "$PARSER_DIR/b2g_parser"

for scenario in off boot cont reset rec_reset; do
  "$PARSER_DIR/b2g_parser" "$scenario" >"$PARSER_DIR/$scenario.log" 2>&1
  grep -q '^B2G-PARSER-PASS ' "$PARSER_DIR/$scenario.log" || \
    fail "positive parser case $scenario"
done
count_exact 1 '^B2G-PARSER-PASS off 0 T$' "$PARSER_DIR/off.log"
count_exact 1 '^B2G-PARSER-PASS boot 1 T$' "$PARSER_DIR/boot.log"
count_exact 1 '^B2G-PARSER-PASS cont 2 T$' "$PARSER_DIR/cont.log"
count_exact 1 '^B2G-PARSER-PASS boot 1 T$' "$PARSER_DIR/reset.log"
count_exact 1 '^B2G-PARSER-PASS off 0 T$' "$PARSER_DIR/reset.log"
count_exact 1 '^B2G-PARSER-PASS cont 2 T$' "$PARSER_DIR/rec_reset.log"
count_exact 1 '^B2G-PARSER-PASS rec_off 0 F$' "$PARSER_DIR/rec_reset.log"

expect_parser_failure()
{
  scenario=$1
  pattern=$2
  if "$PARSER_DIR/b2g_parser" "$scenario" \
    >"$PARSER_DIR/$scenario.log" 2>&1; then
    fail "negative parser case returned: $scenario"
  fi
  grep -q -E "$pattern" "$PARSER_DIR/$scenario.log" || \
    fail "negative parser diagnostic: $scenario"
  if grep -q '^B2G-PARSER-PASS ' "$PARSER_DIR/$scenario.log"; then
    fail "negative parser case published PASS: $scenario"
  fi
}

expect_parser_failure bare \
  '^B2G-XABORT FLUGPI: R64 BOOT OR CONT EXPECTED\.$'
expect_parser_failure integer \
  '^B2G-XABORT FLUGPI: R64 BOOT OR CONT EXPECTED\.$'
expect_parser_failure unknown \
  '^B2G-XABORT FLUGPI: R64 BOOT OR CONT EXPECTED\.$'
expect_parser_failure duplicate \
  '^B2G-XABORT FLUGPI: DUPLICATE R64 KEYWORD\.$'
expect_parser_failure isolated_boot \
  '^B2G-XABORT FLUGPI: READ ERROR - ILLEGAL KEYWORD BOOT$'
expect_parser_failure isolated_cont \
  '^B2G-XABORT FLUGPI: READ ERROR - ILLEGAL KEYWORD CONT$'

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$HERE/check_phase_a9b_b2g_explicit_continuation.py"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2g EXPLICIT-CONTINUATION PASS'
printf '%s\n' 'CLAIM=CONT-TYPE4-FLUX-QFISS-BIT-PRESERVING-INGRESS-CLOSED'
printf '%s\n' 'REAL-B2B-CALLS=13 REJECTIONS-BEFORE-CORE=11'
printf '%s\n' 'BOOT-TYPE2-PROMOTIONS=2 CONT-TYPE4-AUTHORITY-CAPTURES=2'
printf '%s\n' 'ROOT-TYPE2-POISONS=2'
printf '%s\n' 'REAL32-ROUNDTRIP-BIT-LOSS-WITNESSES=10360'
printf '%s\n' 'PARSER-EXECUTIONS=11 PARSER-CALLS=13 PARSER-NEGATIVES=6'
printf '%s\n' 'STATIC-CONTRACT-TESTS=12 MUTATION-CASES=11'
printf '%s\n' 'PRODUCTION-CORE-CALLS=0 DRAGON-EXECUTIONS=0'
printf '%s\n' 'SEQUENTIAL-TRACKING-RECORD-READS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2f'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
