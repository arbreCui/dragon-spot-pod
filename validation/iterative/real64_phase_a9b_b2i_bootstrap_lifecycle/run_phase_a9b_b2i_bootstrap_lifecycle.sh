#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2h_projection_authority/phase_a9b_b2h_projection_authority_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2i_bootstrap_lifecycle_receipt.sha256"
EXPECTED_PARENT_COMMIT=b3a24a7b94c715a81b4f03a8dd12963d3765834a
EXPECTED_PARENT_HASH=2c5d7bb317a419c0ba920ed0ed457b8e8f10f5ebeed07fee144738acf80eb2b9
FC=/opt/homebrew/bin/gfortran
EXPECTED_FC_BANNER='GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0'
CHECKER="$HERE/check_phase_a9b_b2i_bootstrap_lifecycle.py"
CONTRACT_TEST=test_phase_a9b_b2i_bootstrap_lifecycle_contract
AX_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_axial.xsm"
ARCHIVE_ARTIFACT="$ROOT/validation/artifacts/iterative-map1/state1_snapshots.xsm"
TRACK_ARTIFACT="$ROOT/validation/artifacts/iterative-seed/initial_axial_track.xsm"
EXPECTED_AX_HASH=2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484
EXPECTED_ARCHIVE_HASH=1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1
EXPECTED_TRACK_HASH=101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2i.XXXXXX")
SOURCE_DIR="$BUILD_DIR/source"
OBJECT_DIR="$BUILD_DIR/objects"
CASE_DIR="$BUILD_DIR/case"
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

LC_ALL=C
export LC_ALL

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2i FAILURE: $*" >&2
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
  [ -f "$PARENT_RECEIPT" ] || fail "parent receipt missing"
  [ "$(hash_of "$PARENT_RECEIPT")" = "$EXPECTED_PARENT_HASH" ] || \
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
[ -f "$ROOT/src/SPOR64_B2C.f90" ] || fail "production B2C producer missing"
[ -f "$ROOT/src/SPOR64_B2I.f90" ] || fail "production B2i module missing"
[ -f "$CHECKER" ] || fail "independent static checker missing"
[ -f "$HERE/$CONTRACT_TEST.py" ] || fail "mutation tests missing"
[ -f "$HERE/test_b2i_bootstrap_lifecycle.f90" ] || \
  fail "dynamic GANLIB harness missing"
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
  fail "B2h parent commit missing"
git -C "$ROOT" merge-base --is-ancestor "$EXPECTED_PARENT_COMMIT" HEAD || \
  fail "B2h parent commit is not an ancestor"
verify_receipts

PYTHONDONTWRITEBYTECODE=1 python3 "$CHECKER"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" python3 -m unittest -v \
  "$CONTRACT_TEST"

mkdir -p "$SOURCE_DIR" "$OBJECT_DIR" "$CASE_DIR"
copy_exact "$ROOT/src/SPOR64_B2C.f90" "$SOURCE_DIR/SPOR64_B2C.f90"
copy_exact "$ROOT/src/SPOR64_B2I.f90" "$SOURCE_DIR/SPOR64_B2I.f90"
ln -s "$AX_ARTIFACT" "$CASE_DIR/ax.xsm"
ln -s "$ARCHIVE_ARTIFACT" "$CASE_DIR/archive.xsm"
ln -s "$TRACK_ARTIFACT" "$CASE_DIR/track.xsm"

FLAGS='-O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror'
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math"
GANMOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"

"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2C.f90" -o "$OBJECT_DIR/SPOR64_B2C.o"
"$FC" $FLAGS -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$SOURCE_DIR/SPOR64_B2I.f90" -o "$OBJECT_DIR/SPOR64_B2I.o"
"$FC" $FLAGS -I "$OBJECT_DIR" -I "$GANMOD" -J "$OBJECT_DIR" \
  -c "$HERE/test_b2i_bootstrap_lifecycle.f90" \
  -o "$OBJECT_DIR/test_b2i_bootstrap_lifecycle.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$OBJECT_DIR/SPOR64_B2C.o" \
  "$OBJECT_DIR/SPOR64_B2I.o" \
  "$OBJECT_DIR/test_b2i_bootstrap_lifecycle.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_b2i_bootstrap_lifecycle"

nm -g "$OBJECT_DIR/SPOR64_B2I.o" >"$BUILD_DIR/b2i.nm"
count_exact 1 \
  ' T ___spor64_b2i_MOD_spor64_b2i_seal_bootstrap$' "$BUILD_DIR/b2i.nm"
nm -g "$BUILD_DIR/test_b2i_bootstrap_lifecycle" >"$BUILD_DIR/harness.nm"
if grep -Eiq \
  'doorfv|mccgf|mcgmre|flu2dr|fludrv|flugpi|xdrkin|xdrexp|_dragon|spomoc' \
  "$BUILD_DIR/harness.nm"; then
  fail "bootstrap harness links a transport solver or Dragon component"
fi

if ! (
  cd "$CASE_DIR"
  "$BUILD_DIR/test_b2i_bootstrap_lifecycle" ax.xsm archive.xsm track.xsm \
    >harness.log 2>&1
); then
  sed -n '1,180p' "$CASE_DIR/harness.log" >&2
  fail "dynamic bootstrap-lifecycle harness failed"
fi
count_exact 1 '^B2I BOOTSTRAP-LIFECYCLE PASS$' "$CASE_DIR/harness.log"
count_exact 1 '^B2I SEAL-CALLS=13 COMMITS=1 REJECTIONS=12$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2I FRESH-ZERO-WRITE-REJECTIONS=11 COLLISION-NO-NEW-WRITES=1$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2I AUTHORITY64-BITS=31080 MIRROR32-BITS=31080$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2I FOUR-LIST-DEEP-COPIES=12 ROOT-HISTORY-EXCLUSIONS=3$' \
  "$CASE_DIR/harness.log"
count_exact 1 '^B2I PRODUCTION-B2C-PUBLISH-CALLS=3$' \
  "$CASE_DIR/harness.log"
count_exact 1 \
  '^B2I REAL-XSM-INPUTS=3 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0$' \
  "$CASE_DIR/harness.log"
[ "$(wc -l <"$CASE_DIR/harness.log" | tr -d '[:space:]')" -eq 7 ] || \
  fail "unexpected harness output line count"

[ "$(hash_of "$AX_ARTIFACT")" = "$EXPECTED_AX_HASH" ] || \
  fail "frozen AX artifact mutated"
[ "$(hash_of "$ARCHIVE_ARTIFACT")" = "$EXPECTED_ARCHIVE_HASH" ] || \
  fail "frozen archive artifact mutated"
[ "$(hash_of "$TRACK_ARTIFACT")" = "$EXPECTED_TRACK_HASH" ] || \
  fail "frozen axial-track artifact mutated"
verify_receipts

printf '%s\n' 'SPOR64 PHASE-A9b-B2i BOOTSTRAP-LIFECYCLE PASS'
printf '%s\n' 'CLAIM=FRESH-PAIR-ARCHIVE-WIDE-BOOTSTRAP-SEALED-EPOCH0'
printf '%s\n' 'SEAL-CALLS=13 COMMITS=1 PREFLIGHT-REJECTIONS=12'
printf '%s\n' 'AUTHORITY64-BIT-CHECKS=31080 MIRROR32-BIT-CHECKS=31080'
printf '%s\n' 'FOUR-LIST-DEEP-COPY-CHECKS=12 ROOT-HISTORY-EXCLUSIONS=3'
printf '%s\n' 'PRODUCTION-B2C-PUBLISH-CALLS=3'
printf '%s\n' 'STATIC-CONTRACT-TESTS=30 MUTATION-REGRESSION-CASES=29'
printf '%s\n' 'PRODUCTION-B2I-HOST-CALLS=0 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'SEQUENTIAL-TRACKING-RECORD-READS=0 LONG-CALCULATIONS=0'
printf '%s\n' 'RECEIPT=FROZEN PARENT=B2h'
printf '%s\n' 'B*A=NOT-EVALUATED QFISS=NOT-BUILT CONT=NOT-EXECUTED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED OUTER-PICARD=NOT-EVALUATED'
