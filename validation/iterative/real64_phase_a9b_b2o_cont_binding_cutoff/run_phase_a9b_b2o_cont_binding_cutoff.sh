#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2n_real64_frozen_qfiss/phase_a9b_b2n_real64_frozen_qfiss_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2o_cont_binding_cutoff_receipt.sha256"
EXPECTED_PARENT_COMMIT=aa7906e3bcb0e3405c41c55ac0e0e2e54c3211c3
EXPECTED_PARENT_HASH=06f9349e341a1bb3d07087e4f5236f8408b6fe67599a565d68c1b18ca7c51cc5
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2o.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2o FAILURE: $*" >&2
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
  [ -f "$PARENT_RECEIPT" ] || fail "B2n parent receipt missing"
  parent_hash=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
  [ "$parent_hash" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2n parent receipt changed"
  [ -f "$RECEIPT" ] || fail "B2o implementation receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2o implementation receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$($FC --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2n parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2n parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$HERE/check_phase_a9b_b2o_cont_binding_cutoff.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  test_phase_a9b_b2o_cont_binding_cutoff_contract
verify_receipts

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
copy_exact "$ROOT/src/SPOR64_B2C.f90" "$SOURCE_DIR/SPOR64_B2C.f90"
copy_exact "$ROOT/src/SPOR64_B2B.f90" "$SOURCE_DIR/SPOR64_B2B.f90"
copy_exact "$ROOT/src/SPOR64_B2O.f90" "$SOURCE_DIR/SPOR64_B2O.f90"
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
  -J "$OBJECT_DIR" -c "$HERE/b2o_capture_stubs.f90" \
  -o "$OBJECT_DIR/b2o_capture_stubs.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2B.f90" -o "$OBJECT_DIR/SPOR64_B2B.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2O.f90" -o "$OBJECT_DIR/SPOR64_B2O.o"
"$FC" -O0 -g -std=legacy -pedantic-errors -Wall -Wextra -Werror \
  -ffixed-line-length-72 -fcheck=all -fbacktrace -ffp-contract=off \
  -fno-fast-math -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/FLU.f" -o "$OBJECT_DIR/FLU.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$HERE/test_b2o_cont_binding_cutoff.f90" \
  -o "$OBJECT_DIR/test_b2o_cont_binding_cutoff.o"

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/b2o_capture_stubs.o" \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2B.o" \
  "$OBJECT_DIR/SPOR64_B2O.o" \
  "$OBJECT_DIR/test_b2o_cont_binding_cutoff.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2o_cont_binding_cutoff"

nm -g "$BUILD_DIR/test_b2o_cont_binding_cutoff" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|spor64_a8|fludrv|flugpi|xdrkin|xdrexp|_dragon|_flu2dr_$' \
  "$BUILD_DIR/harness.nm"; then
  fail "B2o harness links a production solver or Dragon component"
fi

(
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2o_cont_binding_cutoff" \
    seed.xsm macro.xsm track.xsm system.xsm source.xsm \
    >harness.log 2>&1
)
count_exact 1 '^B2O CONT-BINDING-CUTOFF PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2O REAL-B2B-CALLS=33 REJECTIONS=32$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2O STUB-XDRTA2-CALLS=1 STUB-CORE-CALLS=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2O SEALER-CALLS=7 POSITIVES=2 REJECTIONS=5$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2O INT64-CUTOFF-SENTINEL=4294967311$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 5 ] || \
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

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$HERE/check_phase_a9b_b2o_cont_binding_cutoff.py"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2o CONT-BINDING-CUTOFF PASS'
printf '%s\n' 'CLAIM=ONE-SEALED-SAME-INDEX-CONT-INGRESS-AND-INT64-CUTOFF-OBSERVABILITY-CLOSED'
printf '%s\n' 'REAL-B2B-CALLS=33 REJECTIONS-BEFORE-CORE=32'
printf '%s\n' 'SEALER-CALLS=7 POSITIVES=2 REJECTIONS-BEFORE-PUBLICATION=5'
printf '%s\n' 'STUB-CORE-CALLS=1 STUB-XDRTA2-CALLS=1'
printf '%s\n' 'INT64-CUTOFF-SENTINEL=4294967311'
printf '%s\n' 'STATIC-CONTRACT-TESTS=25'
printf '%s\n' 'PRODUCTION-FLU-EXECUTIONS=0 DRAGON-EXECUTIONS=0'
printf '%s\n' 'TRANSPORT-SOLVES=0 PICARD-MAPS=0'
printf '%s\n' 'SEED-SYSTEM-SELECTION=SEALED-SAME-ARCHIVE-ITEM'
printf '%s\n' 'GLOBAL-LINEAGE-ID=NOT-PRESENT EPOCH=LOCAL-STAGE-LABEL'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
