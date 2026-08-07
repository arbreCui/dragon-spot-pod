#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
B2L_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm"
B2M_DIR="$ROOT/validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit"
PARENT_RECEIPT="$B2M_DIR/phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2n_real64_frozen_qfiss_receipt.sha256"
EXPECTED_PARENT_COMMIT=635d8d7963be8f882bb69956b0e0f3e8ac51de73
EXPECTED_PARENT_HASH=8caa46c1af00e9dbe896123a6294dfa96b790e020c9592e0b76d13f093c09314
EXPECTED_B2C_HASH=9028d686aa20f96bbda59994fa59b4dd1c5489b52f8ad448d1db8b56f5e63e18
EXPECTED_B2I_HASH=3c54d50d21795c5907917fc35b09c8f93a3c7a40c001dcaa85dda82e95a79446
EXPECTED_B2H_HASH=3ce30d8e5a3f42b2d407c6abec4d95725b8f8eb1b6c04fed8fac5b543cb35994
EXPECTED_B2J_HASH=3efe5f83579f0e59e6a486c5857ea3ab3b517fe5c47e4da0ccab4e8de2c8aaaa
EXPECTED_PREPARER_HASH=5b57989f0095f35fccde54e1453621d584ed447eab50abeff443b8a98c4b10d8
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
RUN_B2N=${RUN_B2N:-0}

STATIC_CHECKER="$HERE/check_phase_a9b_b2n_real64_frozen_qfiss.py"
CONTRACT_TEST=test_phase_a9b_b2n_real64_frozen_qfiss_contract
BOUNDED="$HERE/run_bounded_b2n.py"
BOUNDED_TEST=test_run_bounded_b2n
PREPARER="$B2L_DIR/prepare_b2l_projected.f90"
BUILDER="$HERE/build_b2n_real64_frozen_qfiss.f90"
POSTERIOR="$HERE/check_b2n_real64_frozen_qfiss.f90"
SOURCE="$ROOT/src/SPOR64_B2N.f90"

AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
AXIAL_TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_AXIAL_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
EXPECTED_PROJECTED_HASH=c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c
EXPECTED_PROJECTED_BYTES=225315452
EXPECTED_MACRO_HASH=6430b5e43b03125f8bd94c350bae2d8fc97978f86b3a5bb25f2026fd10914ada
EXPECTED_MACRO_BYTES=9878532
EXPECTED_SOURCE_HASH=37a3499742125db65fb51e505797e2890f6ae29461af9640bf14352aad898f2d
EXPECTED_SOURCE_BYTES=625560

BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2n.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"

cleanup()
{
  status=$?
  trap - EXIT HUP INT TERM
  if [ "$status" -ne 0 ] && [ -d "$CASE_DIR" ]; then
    for log in prepare.log build.log posterior_a.log posterior_b.log
    do
      if [ -f "$CASE_DIR/$log" ]; then
        printf '%s\n' "--- retained tail before cleanup: $log ---" >&2
        tail -n 120 "$CASE_DIR/$log" >&2
        printf '%s\n' "--- end retained tail: $log ---" >&2
      fi
    done
  fi
  cd /
  rm -rf "$BUILD_DIR"
  exit "$status"
}

trap cleanup EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2n FAILURE: $*" >&2
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

hash_of()
{
  shasum -a 256 "$1" | awk '{print $1}'
}

require_hash()
{
  path=$1
  expected=$2
  [ "$(hash_of "$path")" = "$expected" ] || fail "hash differs: $path"
}

require_parent_entry()
{
  relative_path=$1
  expected=$2
  grep -F -x "$expected  $relative_path" "$PARENT_RECEIPT" >/dev/null || \
    fail "B2m parent receipt entry differs: $relative_path"
  require_hash "$ROOT/$relative_path" "$expected"
}

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2m parent receipt missing"
  require_hash "$PARENT_RECEIPT" "$EXPECTED_PARENT_HASH"
  if [ -f "$RECEIPT" ]; then
    (
      cd "$ROOT"
      shasum -a 256 -c "$RECEIPT" >/dev/null
    ) || fail "B2n receipt verification failed"
  fi
}

show_failure_log()
{
  log=$1
  if [ -f "$log" ]; then
    printf '%s\n' "--- bounded child log: $log ---" >&2
    tail -n 120 "$log" >&2
    printf '%s\n' '--- end bounded child log ---' >&2
  fi
}

case "$RUN_B2N" in
  0|1) ;;
  *) fail "RUN_B2N must be exactly 0 or 1" ;;
esac

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"

for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J
do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
for path in "$SOURCE" "$STATIC_CHECKER" "$HERE/$CONTRACT_TEST.py" \
  "$BOUNDED" "$HERE/$BOUNDED_TEST.py" "$PREPARER" "$BUILDER" \
  "$POSTERIOR" "$AX_ARTIFACT" "$ARCHIVE_ARTIFACT" \
  "$AXIAL_TRACK_ARTIFACT"
do
  [ -f "$path" ] || fail "required input missing: $path"
done

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2m parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2m parent commit is not an ancestor"
verify_receipts
require_parent_entry src/SPOR64_B2C.f90 "$EXPECTED_B2C_HASH"
require_parent_entry src/SPOR64_B2I.f90 "$EXPECTED_B2I_HASH"
require_parent_entry src/SPOR64_B2H.f90 "$EXPECTED_B2H_HASH"
require_parent_entry src/SPOR64_B2J.f90 "$EXPECTED_B2J_HASH"
require_parent_entry \
  validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm/prepare_b2l_projected.f90 \
  "$EXPECTED_PREPARER_HASH"

PYTHONDONTWRITEBYTECODE=1 python3 "$STATIC_CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST" "$BOUNDED_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J
do
  copy_exact "$ROOT/src/$source.f90" "$SOURCE_DIR/$source.f90"
done
copy_exact "$SOURCE" "$SOURCE_DIR/SPOR64_B2N.f90"
copy_exact "$PREPARER" "$SOURCE_DIR/prepare_b2l_projected.f90"
copy_exact "$BUILDER" "$SOURCE_DIR/build_b2n_real64_frozen_qfiss.f90"
copy_exact "$POSTERIOR" "$SOURCE_DIR/check_b2n_real64_frozen_qfiss.f90"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"

for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J SPOR64_B2N
do
  "$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
    -c "$SOURCE_DIR/$source.f90" -o "$OBJECT_DIR/$source.o"
done
for source in prepare_b2l_projected build_b2n_real64_frozen_qfiss \
  check_b2n_real64_frozen_qfiss
do
  "$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
    -c "$SOURCE_DIR/$source.f90" -o "$OBJECT_DIR/$source.o"
done

"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.o" "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" "$OBJECT_DIR/SPOR64_B2J.o" \
  "$OBJECT_DIR/prepare_b2l_projected.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/prepare_b2l_projected"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2N.o" \
  "$OBJECT_DIR/build_b2n_real64_frozen_qfiss.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/build_b2n_real64_frozen_qfiss"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/check_b2n_real64_frozen_qfiss.o" "$GANLIB" "$UTILIB" \
  -o "$BUILD_DIR/check_b2n_real64_frozen_qfiss"

nm -g "$BUILD_DIR/prepare_b2l_projected" >"$BUILD_DIR/prepare.nm"
nm -g "$BUILD_DIR/build_b2n_real64_frozen_qfiss" >"$BUILD_DIR/build.nm"
nm -g "$BUILD_DIR/check_b2n_real64_frozen_qfiss" >"$BUILD_DIR/posterior.nm"
grep -i 'spor64_b2n.*build' "$BUILD_DIR/build.nm" >/dev/null || \
  fail "builder lacks production SPOR64_B2N boundary"
if grep -Eiq \
  '(^|[[:space:]])_?(asm|asmdrv|doorav|doorpv|mccga|mcgasm|flu|fludrv|spor64k)_$' \
  "$BUILD_DIR/prepare.nm" "$BUILD_DIR/build.nm" "$BUILD_DIR/posterior.nm"
then
  fail "source gate links a forbidden solver"
fi
if grep -i 'spor64_b2n' "$BUILD_DIR/posterior.nm" >/dev/null
then
  fail "independent posterior links production SPOR64_B2N"
fi
grep -i 'lcmop' "$BUILD_DIR/posterior.nm" >/dev/null || \
  fail "independent posterior lacks GANLIB read path"

if [ "$RUN_B2N" = 0 ]; then
  printf '%s\n' 'SPOR64 PHASE-A9b-B2n PREFLIGHT PASS'
  printf '%s\n' \
    'ACTIVATION=DEFAULT-OFF; SET RUN_B2N=1 FOR ONE BOUNDED REAL SOURCE BUILD'
  printf '%s\n' \
    'REAL-SOURCE-BUILDS=0 DRAGON=0 ASM=0 SPOR64K=0 FLU=0 TRANSPORT=0 PICARD=0'
  printf '%s\n' 'REAL64-QFISS=NOT-EVALUATED'
  exit 0
fi

ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$AXIAL_TRACK_ARTIFACT" "$CASE_DIR/axial_track.xsm"
[ ! -e "$CASE_DIR/projected.xsm" ] || fail "PROJECTED output path exists"
[ ! -e "$CASE_DIR/macro0.xsm" ] || fail "MACRO0 output path exists"
[ ! -e "$CASE_DIR/fsource.xsm" ] || fail "FSOURCE output path exists"

if ! python3 "$BOUNDED" prepare "$BUILD_DIR/prepare_b2l_projected" - \
  "$CASE_DIR/prepare.log" ax.xsm archive.xsm axial_track.xsm projected.xsm
then
  show_failure_log "$CASE_DIR/prepare.log"
  fail "bounded PROJECTED preparation failed"
fi
count_exact 1 '^B2L FULL PROJECTED PREPARATION PASS$' "$CASE_DIR/prepare.log"
[ -s "$CASE_DIR/projected.xsm" ] || fail "PROJECTED materialization missing"
[ ! -L "$CASE_DIR/projected.xsm" ] || fail "PROJECTED output is a symlink"
PROJECTED_BYTES=$(stat -f '%z' "$CASE_DIR/projected.xsm")
[ "$PROJECTED_BYTES" -eq "$EXPECTED_PROJECTED_BYTES" ] || \
  fail "PROJECTED byte count differs"
PROJECTED_HASH=$(hash_of "$CASE_DIR/projected.xsm")
[ "$PROJECTED_HASH" = "$EXPECTED_PROJECTED_HASH" ] || \
  fail "PROJECTED hash differs"

if ! python3 "$BOUNDED" build \
  "$BUILD_DIR/build_b2n_real64_frozen_qfiss" - "$CASE_DIR/build.log" \
  projected.xsm macro0.xsm fsource.xsm
then
  show_failure_log "$CASE_DIR/build.log"
  fail "bounded REAL64 frozen-source build failed"
fi
count_exact 1 '^B2N REAL64 FROZEN-QFISS BUILD PASS$' "$CASE_DIR/build.log"
count_exact 1 '^B2N PRODUCTION-BUILD-CALLS=1 PLANE=1 STATE=FROZEN-QFIS/1$' \
  "$CASE_DIR/build.log"
count_exact 1 '^B2N WHOLE-OBJECT-XSM-COPIES=2$' "$CASE_DIR/build.log"
count_exact 1 '^B2N DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0$' \
  "$CASE_DIR/build.log"
count_exact 1 '^B2N CONVERGENCE=NOT-EVALUATED$' "$CASE_DIR/build.log"
[ "$(wc -l <"$CASE_DIR/build.log" | tr -d '[:space:]')" -eq 5 ] || \
  fail "builder output inventory differs"
for path in macro0.xsm fsource.xsm
do
  [ -s "$CASE_DIR/$path" ] || fail "missing output: $path"
  [ ! -L "$CASE_DIR/$path" ] || fail "output is a symlink: $path"
  [ "$(stat -f '%z' "$CASE_DIR/$path")" -le 134217728 ] || \
    fail "output cap exceeded: $path"
done
MACRO_HASH=$(hash_of "$CASE_DIR/macro0.xsm")
SOURCE_HASH=$(hash_of "$CASE_DIR/fsource.xsm")
MACRO_BYTES=$(stat -f '%z' "$CASE_DIR/macro0.xsm")
SOURCE_BYTES=$(stat -f '%z' "$CASE_DIR/fsource.xsm")
[ "$MACRO_HASH" = "$EXPECTED_MACRO_HASH" ] || fail "MACRO0 hash differs"
[ "$SOURCE_HASH" = "$EXPECTED_SOURCE_HASH" ] || fail "FSOURCE hash differs"
[ "$MACRO_BYTES" -eq "$EXPECTED_MACRO_BYTES" ] || fail "MACRO0 byte count differs"
[ "$SOURCE_BYTES" -eq "$EXPECTED_SOURCE_BYTES" ] || fail "FSOURCE byte count differs"
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_HASH" ] || \
  fail "PROJECTED input mutated by source builder"

if ! python3 "$BOUNDED" posterior \
  "$BUILD_DIR/check_b2n_real64_frozen_qfiss" - \
  "$CASE_DIR/posterior_a.log" projected.xsm macro0.xsm fsource.xsm
then
  show_failure_log "$CASE_DIR/posterior_a.log"
  fail "first independent posterior failed"
fi
if ! python3 "$BOUNDED" posterior \
  "$BUILD_DIR/check_b2n_real64_frozen_qfiss" - \
  "$CASE_DIR/posterior_b.log" projected.xsm macro0.xsm fsource.xsm
then
  show_failure_log "$CASE_DIR/posterior_b.log"
  fail "second independent posterior failed"
fi
cmp "$CASE_DIR/posterior_a.log" "$CASE_DIR/posterior_b.log" || \
  fail "read-only posterior output is not repeatable"
count_exact 1 '^B2N REAL64 FROZEN-QFISS POSTERIOR PASS$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2N QFISS-R64-BITS=5180 DSOUR-R32-PROJECTIONS=5180 QINT-R32-PROJECTIONS=370$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 \
  '^B2N POSITIVE-REGION-FLUX=2960 NONREGION-POSITIVE-ZERO-QFISS=2220$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2N NUSIGF-POSITIVE-ZERO=94720 MACRO-OTHER-RECORDS=BIT-IDENTICAL$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2N STATE=FROZEN-QFIS/1 PLANE=1 SAME-RHO=BIT-IDENTICAL$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2N FIRST-GROUP-INTEGRAL=POSITIVE$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2N DRAGON=0 ASM=0 FLU=0 CONVERGENCE=NOT-EVALUATED$' \
  "$CASE_DIR/posterior_a.log"
count_exact 1 '^B2N EMPIRICAL-CONTROLS=0 CONT=0$' \
  "$CASE_DIR/posterior_a.log"
[ "$(wc -l <"$CASE_DIR/posterior_a.log" | tr -d '[:space:]')" -eq 8 ] || \
  fail "posterior output inventory differs"

require_hash "$AX_ARTIFACT" "$EXPECTED_AX_HASH"
require_hash "$ARCHIVE_ARTIFACT" "$EXPECTED_ARCHIVE_HASH"
require_hash "$AXIAL_TRACK_ARTIFACT" "$EXPECTED_AXIAL_TRACK_HASH"
[ "$(hash_of "$CASE_DIR/projected.xsm")" = "$PROJECTED_HASH" ] || \
  fail "PROJECTED input mutated during posterior"
[ "$(hash_of "$CASE_DIR/macro0.xsm")" = "$MACRO_HASH" ] || \
  fail "MACRO0 mutated during read-only posterior"
[ "$(hash_of "$CASE_DIR/fsource.xsm")" = "$SOURCE_HASH" ] || \
  fail "FSOURCE mutated during read-only posterior"
[ "$(stat -f '%z' "$CASE_DIR/macro0.xsm")" -eq "$MACRO_BYTES" ] || \
  fail "MACRO0 byte count changed during posterior"
[ "$(stat -f '%z' "$CASE_DIR/fsource.xsm")" -eq "$SOURCE_BYTES" ] || \
  fail "FSOURCE byte count changed during posterior"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2n REAL64-FROZEN-QFISS PASS'
printf '%s\n' \
  'CLAIM=PLANE1-SAME-EPOCH-REAL64-QFISS-BITWISE-VERIFIED-AND-ZERO-LIVE-FISSION-MACRO0-VERIFIED'
printf '%s\n' \
  'MATERIALIZER-EXECUTIONS=1 SOURCE-BUILDER-EXECUTIONS=1 POSTERIOR-EXECUTIONS=2'
printf '%s\n' \
  'DRAGON=0 ASM=0 SPOR64K=0 FLU=0 TRANSPORT=0 CONT=0 PICARD=0 RETRIES=0'
printf '%s\n' \
  'QFISS-R64-BITS=5180 DSOUR-R32-PROJECTIONS=5180 QINT-R32-PROJECTIONS=370'
printf '%s\n' \
  'POSITIVE-REGION-FLUX=2960 NONREGION-POSITIVE-ZERO-QFISS=2220 NUSIGF-POSITIVE-ZERO=94720'
printf '%s\n' "PROJECTED-SHA256=$PROJECTED_HASH BYTES=$PROJECTED_BYTES"
printf '%s\n' "MACRO0-SHA256=$MACRO_HASH BYTES=$MACRO_BYTES"
printf '%s\n' "FSOURCE-SHA256=$SOURCE_HASH BYTES=$SOURCE_BYTES"
printf '%s\n' \
  'EMPIRICAL-PHYSICS-COEFFICIENTS=0 RELAXATION=0 MODEL-COMPLETION=0'
printf '%s\n' \
  'RADIAL-FLUX-SOLVE=NOT-EXECUTED RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
if [ -f "$RECEIPT" ]; then
  printf '%s\n' 'RECEIPT=FROZEN PARENT=B2m'
else
  printf '%s\n' 'RECEIPT=PENDING-MAIN-AUDIT PARENT=B2m'
fi
