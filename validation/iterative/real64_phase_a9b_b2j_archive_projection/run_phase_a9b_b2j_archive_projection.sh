#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2i_bootstrap_lifecycle/phase_a9b_b2i_bootstrap_lifecycle_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2j_archive_projection_receipt.sha256"
EXPECTED_PARENT_COMMIT=891e67c2cc84aa69e87a9047cf1b230b10c9a48e
EXPECTED_PARENT_HASH=a985deea1344733a8f004cfa1124e8724d188e4ec3d67d11e579305eee6b541f
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CHECKER="$HERE/check_phase_a9b_b2j_archive_projection.py"
CONTRACT_TEST=test_phase_a9b_b2j_archive_projection_contract
SUPPORT="$HERE/b2j_fixture_support.f90"
HARNESS="$HERE/test_b2j_archive_projection.f90"
AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2j.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2j FAILURE: $*" >&2
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

verify_receipts()
{
  [ -f "$PARENT_RECEIPT" ] || fail "B2i parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
    fail "B2i parent receipt changed"
  [ -f "$RECEIPT" ] || fail "B2j implementation receipt missing"
  (
    cd "$ROOT"
    shasum -a 256 -c "$RECEIPT" >/dev/null
  ) || fail "B2j implementation receipt verification failed"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing"
FC_BANNER=$("$FC" --version | sed -n '1p')
[ "$FC_BANNER" = "$EXPECTED_FC_BANNER" ] || fail "unaudited compiler"
for source in SPOR64_B2C SPOR64_B2I SPOR64_B2H SPOR64_B2J; do
  [ -f "$ROOT/src/$source.f90" ] || fail "production $source missing"
done
[ -f "$CHECKER" ] || fail "independent static checker missing"
[ -f "$HERE/$CONTRACT_TEST.py" ] || fail "mutation tests missing"
[ -f "$SUPPORT" ] || fail "real-XSM fixture support missing"
[ -f "$HARNESS" ] || fail "dynamic GANLIB harness missing"
[ -f "$AX_ARTIFACT" ] || fail "frozen AX artifact missing"
[ -f "$ARCHIVE_ARTIFACT" ] || fail "frozen archive artifact missing"
[ -f "$TRACK_ARTIFACT" ] || fail "frozen axial-track artifact missing"
[ "$(hash_of "$AX_ARTIFACT")" = "$EXPECTED_AX_HASH" ] || \
  fail "frozen AX artifact changed"
[ "$(hash_of "$ARCHIVE_ARTIFACT")" = "$EXPECTED_ARCHIVE_HASH" ] || \
  fail "frozen archive artifact changed"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen axial-track artifact changed"
git -C "$ROOT" cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}" || \
  fail "B2i parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2i parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
copy_exact "$ROOT/src/SPOR64_B2C.f90" "$SOURCE_DIR/SPOR64_B2C.f90"
copy_exact "$ROOT/src/SPOR64_B2I.f90" "$SOURCE_DIR/SPOR64_B2I.f90"
copy_exact "$ROOT/src/SPOR64_B2H.f90" "$SOURCE_DIR/SPOR64_B2H.f90"
copy_exact "$ROOT/src/SPOR64_B2J.f90" "$SOURCE_DIR/SPOR64_B2J.f90"
copy_exact "$SUPPORT" "$SOURCE_DIR/b2j_fixture_support.f90"
copy_exact "$HARNESS" "$SOURCE_DIR/test_b2j_archive_projection.f90"
ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$TRACK_ARTIFACT" "$CASE_DIR/track.xsm"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2I.f90" -o "$OBJECT_DIR/SPOR64_B2I.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2H.f90" -o "$OBJECT_DIR/SPOR64_B2H.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2J.f90" -o "$OBJECT_DIR/SPOR64_B2J.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/b2j_fixture_support.f90" \
  -o "$OBJECT_DIR/b2j_fixture_support.o"
"$FC" $FLAGS -I "$GANMOD" -I "$OBJECT_DIR" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/test_b2j_archive_projection.f90" \
  -o "$OBJECT_DIR/test_b2j_archive_projection.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/SPOR64_B2H.o" \
  "$OBJECT_DIR/SPOR64_B2J.o" \
  "$OBJECT_DIR/b2j_fixture_support.o" \
  "$OBJECT_DIR/test_b2j_archive_projection.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2j_archive_projection"

nm -g "$OBJECT_DIR/SPOR64_B2J.o" >"$BUILD_DIR/b2j.nm"
count_exact 1 \
  ' T ___spor64_b2j_MOD_spor64_b2j_project_archive$' "$BUILD_DIR/b2j.nm"
nm -g "$BUILD_DIR/test_b2j_archive_projection" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|flu2dr|fludrv|flugpi|xdrkin|xdrexp|_dragon|spomoc' \
  "$BUILD_DIR/harness.nm"; then
  fail "projection harness links a transport solver or Dragon component"
fi

if ! (
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2j_archive_projection" ax.xsm archive.xsm track.xsm \
    >harness.log 2>&1
); then
  sed -n '1,200p' "$CASE_DIR/harness.log" >&2
  fail "dynamic archive-projection harness failed"
fi
count_exact 1 '^B2J ARCHIVE-PROJECTION PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2J CALLS=13 COMMITS=1 REJECTIONS=12$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J FRESH-ZERO-WRITE-REJECTIONS=11 COLLISION-NO-NEW-WRITES=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J INDEPENDENT-B\*A-SLICES=1110 AX-L-LEAKAGE-BITS=1110$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J REGION64-BITS=8880 NONREGION64-BITS=6660 MIRROR32-BITS=15540$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2J TWO-LIST-DEEP-COPIES=6 B2H-REPLACEMENTS=3$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J PLANE-SOURCE-ABSENCES=6 PLANE-QFISS-ABSENCES=6 ARCHIVE-SYSTEM-ABSENCES=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J PRODUCTION-B2C-CALLS=3 B2I-CALLS=1 B2H-COMMITTED-PLANES=3$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J REAL-XSM-INPUTS=3 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2J SYSTEM=ABSENT SOURCE=ABSENT QFISS=NOT-BUILT CONT=NOT-EXECUTED$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 10 ] || \
  fail "unexpected harness output line count"

[ "$(hash_of "$AX_ARTIFACT")" = "$EXPECTED_AX_HASH" ] || \
  fail "frozen AX artifact mutated"
[ "$(hash_of "$ARCHIVE_ARTIFACT")" = "$EXPECTED_ARCHIVE_HASH" ] || \
  fail "frozen archive artifact mutated"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen axial-track artifact mutated"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2j ARCHIVE-PROJECTION PASS'
printf '%s\n' 'CLAIM=CONTROLLED-B2I-CLOSED0-TO-ARCHIVE-PROJECTED1'
printf '%s\n' 'B2J-CALLS=13 COMMITS=1 PREFLIGHT-OR-STAGE-REJECTIONS=12'
printf '%s\n' 'B*A-SLICES=1110 REGION64-BITS=8880 NONREGION64-BITS=6660'
printf '%s\n' 'AX-L-LEAKAGE-BITS=1110 MIRROR32-BITS=15540'
printf '%s\n' 'TRACK-LIBRARY-DEEP-COPIES=6 B2H-PLANE-REPLACEMENTS=3'
printf '%s\n' 'SYSTEM=ABSENT-PENDING-ASM SOURCE=ABSENT QFISS=ABSENT'
printf '%s\n' 'PRODUCTION-B2C-CALLS=3 B2I-CALLS=1 B2H-PLANES=3'
printf '%s\n' 'STATIC-CONTRACT-TESTS=35 MUTATION-REGRESSION-CASES=34'
printf '%s\n' 'PRODUCTION-B2J-HOST-CALLS=0 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'SEQUENTIAL-TRACKING-RECORD-READS=0 LONG-CALCULATIONS=0'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2i'
printf '%s\n' 'QFISS=NOT-BUILT CONT=NOT-EXECUTED ASM=NOT-EXECUTED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
