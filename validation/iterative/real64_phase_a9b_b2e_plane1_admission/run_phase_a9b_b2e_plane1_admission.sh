#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
FC=/opt/homebrew/bin/gfortran
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-b2e-admission.XXXXXX")
CASE_DIR="$BUILD_DIR/case"
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2e FAILURE: $*" >&2
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

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
"$FC" --version | grep -Fq 'GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0' || \
  fail "frozen compiler banner differs"
git -C "$ROOT" merge-base --is-ancestor \
  f20363f9c99c96a23a6b580de644e0d212b59849 HEAD || \
  fail "B2d parent commit absent"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2e_plane1_admission.py"

mkdir -p "$CASE_DIR"
copy_exact \
  "$ROOT/validation/artifacts/iterative-radial-floor/restart_cap.xsm" \
  "$CASE_DIR/flux.xsm"
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

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -Wno-unused-dummy-argument -I "$GANMOD" \
  -J "$BUILD_DIR" -c "$HERE/b2e_noop_stubs.f90" \
  -o "$BUILD_DIR/b2e_noop_stubs.o"
"$FC" $FLAGS -I "$BUILD_DIR" -I "$GANMOD" -J "$BUILD_DIR" \
  -c "$ROOT/src/SPOR64_B2B.f90" -o "$BUILD_DIR/SPOR64_B2B.o"
"$FC" $FLAGS -I "$BUILD_DIR" -I "$GANMOD" -J "$BUILD_DIR" \
  -c "$HERE/test_b2e_current_admission.f90" \
  -o "$BUILD_DIR/test_b2e_current_admission.o"
"$FC" $FLAGS -I "$GANMOD" -J "$BUILD_DIR" \
  -c "$HERE/b2e_strip_legacy_source.f90" \
  -o "$BUILD_DIR/b2e_strip_legacy_source.o"
"$FC" $FLAGS -I "$GANMOD" -J "$BUILD_DIR" \
  -c "$HERE/check_b2e_real_schema.f90" \
  -o "$BUILD_DIR/check_b2e_real_schema.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$BUILD_DIR/b2e_noop_stubs.o" \
  "$BUILD_DIR/SPOR64_B2B.o" \
  "$BUILD_DIR/test_b2e_current_admission.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2e_current_admission"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$BUILD_DIR/b2e_strip_legacy_source.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/b2e_strip_legacy_source"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$BUILD_DIR/check_b2e_real_schema.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/check_b2e_real_schema"

nm -g "$BUILD_DIR/SPOR64_B2B.o" >"$BUILD_DIR/b2b.nm"
for symbol in \
  ___spomoc_audit_MOD_spomoc_active \
  ___spor64_a9_MOD_flu2dr64_core \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  _xdrta2_; do
  count_exact 1 " U ${symbol}$" "$BUILD_DIR/b2b.nm"
done
nm -g "$BUILD_DIR/b2e_noop_stubs.o" >"$BUILD_DIR/stubs.nm"
for symbol in \
  ___spomoc_audit_MOD_spomoc_active \
  ___spor64_a9_MOD_flu2dr64_core \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  _xdrta2_; do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/stubs.nm"
done
nm -g "$BUILD_DIR/test_b2e_current_admission" >"$BUILD_DIR/harness.nm"
if grep -Eiq 'doorfv|mccgf|mcgmre|spor64_a8|fludrv|flugpi|xdrkin|xdrexp|_dragon' \
  "$BUILD_DIR/harness.nm"; then
  fail "admission harness links a production solver component"
fi

(
  cd "$CASE_DIR"
  "$BUILD_DIR/check_b2e_real_schema" flux.xsm macro.xsm track.xsm \
    system.xsm source.xsm \
    >schema.log 2>&1
)
count_exact 1 '^B2E REAL-SCHEMA PASS$' "$CASE_DIR/schema.log"
count_exact 1 '^B2E LEGACY-SOUR-COLLISION=true$' "$CASE_DIR/schema.log"
count_exact 1 '^B2E SOUR-FREE-NEXT-BLOCKER=MACRO0/STATE-VECTOR\(3\)=3$' \
  "$CASE_DIR/schema.log"

(
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2e_current_admission" real-restart \
    flux.xsm macro.xsm track.xsm system.xsm source.xsm \
    >real-restart.log 2>&1
)
count_exact 1 '^B2E CURRENT-ADMISSION BLOCKED PASS real-restart$' \
  "$CASE_DIR/real-restart.log"

copy_exact "$CASE_DIR/flux.xsm" "$CASE_DIR/sour_free.xsm"
(
  cd "$CASE_DIR"
  "$BUILD_DIR/b2e_strip_legacy_source" sour_free.xsm \
    >strip.log 2>&1
  "$BUILD_DIR/test_b2e_current_admission" sour-free-restart \
    sour_free.xsm macro.xsm track.xsm system.xsm source.xsm \
    >sour-free-restart.log 2>&1
)
count_exact 1 '^B2E TEMPORARY STRUCTURAL FIXTURE PASS$' "$CASE_DIR/strip.log"
count_exact 1 '^B2E CURRENT-ADMISSION BLOCKED PASS sour-free-restart$' \
  "$CASE_DIR/sour-free-restart.log"

(
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2e_current_admission" fresh-create \
    flux.xsm macro.xsm track.xsm system.xsm source.xsm \
    >fresh-create.log 2>&1
)
count_exact 1 '^B2E CURRENT-ADMISSION BLOCKED PASS fresh-create$' \
  "$CASE_DIR/fresh-create.log"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2e_plane1_admission.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
  python3 -m unittest -v test_phase_a9b_b2e_plane1_admission_contract

printf '%s\n' 'SPOR64 PHASE-A9b-B2e ADMISSION PASS'
printf '%s\n' 'CLAIM=CURRENT-HOST-ADMISSION-BLOCKED-BEFORE-SOLVER'
printf '%s\n' 'REAL-B2B-SOURCE-LINKS=1 BLOCKED-ADMISSION-SCENARIOS=3'
printf '%s\n' 'PRODUCTION-XDRTA2-CALLS=0 PRODUCTION-CORE-CALLS=0 PRODUCTION-PUBLISHER-CALLS=0'
printf '%s\n' 'DRAGON-EXECUTIONS=0 SEQUENTIAL-TRACKING-RECORD-READS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'ORIGINAL-ARTIFACT-MUTATIONS=0 TEMPORARY-STRUCTURAL-FIXTURE-MUTATIONS=1'
printf '%s\n' 'CANDIDATE-HOST-EXECUTIONS=0 PRODUCTION-EXECUTION-AUTHORIZED=false'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED'
printf '%s\n' 'OUTER-PICARD-CONVERGENCE=NOT-EVALUATED'
