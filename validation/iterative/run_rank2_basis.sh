#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
SNAP_XSM=${SNAP_XSM:-"$ROOT/validation/artifacts/iterative-seed/initial_snapshots.xsm"}
REFERENCE_XSM=${REFERENCE_XSM:-"$ROOT/validation/artifacts/iterative-map1/basis_reference.xsm"}
ARTIFACT_DIR=${ARTIFACT_DIR:-"$ROOT/validation/artifacts/iterative-rank2-basis"}
OUTPUT_XSM=${OUTPUT_XSM:-"$ARTIFACT_DIR/rank2_basis.xsm"}
EXPECTED_SNAP_SHA=37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95
EXPECTED_REFERENCE_SHA=dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504
EXPECTED_OUTPUT_SHA=2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8
EXPECTED_SNAP_SIZE=227725476
EXPECTED_REFERENCE_SIZE=800220
EXPECTED_OUTPUT_SIZE=832780
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

BUILDER_SOURCE="$ROOT/validation/iterative/build_rank2_basis_xsm.f90"
CHECKER_SOURCE="$ROOT/validation/iterative/check_rank2_basis_xsm.f90"

for input in \
  "$SNAP_XSM" "$REFERENCE_XSM" "$GANLIB_LIB" \
  "$GANLIB_MOD/ganlib.mod" "$ROOT/Utilib/src/ALSVDF.f" \
  "$ROOT/src/SPOPOD.f90" "$BUILDER_SOURCE" "$CHECKER_SOURCE"
do
  test -f "$input"
  test ! -L "$input"
done
mkdir -p "$ARTIFACT_DIR" "$(dirname "$OUTPUT_XSM")"
canonical_path() (
  cd "$(dirname "$1")"
  printf '%s/%s\n' "$(pwd -P)" "$(basename "$1")"
)
SNAP_CANONICAL=$(canonical_path "$SNAP_XSM")
REFERENCE_CANONICAL=$(canonical_path "$REFERENCE_XSM")
OUTPUT_CANONICAL=$(canonical_path "$OUTPUT_XSM")
test "$OUTPUT_CANONICAL" != "$SNAP_CANONICAL"
test "$OUTPUT_CANONICAL" != "$REFERENCE_CANONICAL"
test ! -L "$OUTPUT_XSM"
test ! -d "$OUTPUT_XSM"
if test -e "$OUTPUT_XSM"; then
  test ! "$OUTPUT_XSM" -ef "$SNAP_XSM"
  test ! "$OUTPUT_XSM" -ef "$REFERENCE_XSM"
fi
test "$(wc -c < "$SNAP_XSM" | tr -d ' ')" = "$EXPECTED_SNAP_SIZE"
test "$(wc -c < "$REFERENCE_XSM" | tr -d ' ')" = "$EXPECTED_REFERENCE_SIZE"

hash_file() {
  hash_output=$(shasum -a 256 "$1")
  digest=${hash_output%% *}
  printf '%s\n' "$digest" | rg -q '^[0-9a-f]{64}$'
  printf '%s\n' "$digest"
}

test "$(hash_file "$SNAP_XSM")" = "$EXPECTED_SNAP_SHA"
test "$(hash_file "$REFERENCE_XSM")" = "$EXPECTED_REFERENCE_SHA"

WORK=$(mktemp -d "/private/tmp/spot-rank2-basis.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

# Ganlib XSM names are limited to 72 characters.  These short, temporary
# aliases point only to the two hash-checked read-only inputs.
ln -s "$SNAP_XSM" "$WORK/snapshots.xsm"
ln -s "$REFERENCE_XSM" "$WORK/reference.xsm"
test "$(hash_file "$WORK/snapshots.xsm")" = "$EXPECTED_SNAP_SHA"
test "$(hash_file "$WORK/reference.xsm")" = "$EXPECTED_REFERENCE_SHA"

for branch in a b
do
  cp "$REFERENCE_XSM" "$WORK/rank1_control_$branch.xsm"
  cp "$REFERENCE_XSM" "$WORK/rank2_candidate_$branch.xsm"
  cmp "$REFERENCE_XSM" "$WORK/rank1_control_$branch.xsm"
  cmp "$REFERENCE_XSM" "$WORK/rank2_candidate_$branch.xsm"
done

BUILD_FLAGS='-O2 -march=native -ffp-contract=off -g -fPIC -Wall -Wextra -Werror -Wno-compare-reals -ffree-line-length-none -ffixed-line-length-none'

"$FC" $BUILD_FLAGS -I "$GANLIB_MOD" \
  "$ROOT/Utilib/src/ALSVDF.f" \
  "$ROOT/src/SPOPOD.f90" \
  "$BUILDER_SOURCE" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/build_rank2_basis_xsm"

"$FC" $BUILD_FLAGS -I "$GANLIB_MOD" \
  "$CHECKER_SOURCE" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_rank2_basis_xsm"

nm "$WORK/build_rank2_basis_xsm" > "$WORK/builder.nm"
nm "$WORK/check_rank2_basis_xsm" > "$WORK/checker.nm"
if rg -qi '(_|[[:space:]])(asm|flu|dragon|spoasm|spot1p|spof)(_|[[:space:]]|$)' \
  "$WORK/builder.nm" "$WORK/checker.nm"; then
  echo 'rank-2 offline tools contain a forbidden solver symbol' >&2
  exit 2
fi
if rg -qi '(_|[[:space:]])(spopod|alsvdf)(_|[[:space:]]|$)' \
  "$WORK/checker.nm"; then
  echo 'independent rank-2 checker links the production SVD path' >&2
  exit 2
fi

for branch in a b
do
  (
    cd "$WORK"
    ./build_rank2_basis_xsm \
      snapshots.xsm reference.xsm \
      "rank1_control_$branch.xsm" "rank2_candidate_$branch.xsm" \
      > "build_$branch.log"
    ./check_rank2_basis_xsm \
      snapshots.xsm reference.xsm \
      "rank1_control_$branch.xsm" "rank2_candidate_$branch.xsm" \
      > "check_$branch.log"
  )
done

cmp "$WORK/rank1_control_a.xsm" "$WORK/rank1_control_b.xsm"
cmp "$WORK/rank2_candidate_a.xsm" "$WORK/rank2_candidate_b.xsm"
cmp "$WORK/build_a.log" "$WORK/build_b.log"
cmp "$WORK/check_a.log" "$WORK/check_b.log"

test "$(hash_file "$SNAP_XSM")" = "$EXPECTED_SNAP_SHA"
test "$(hash_file "$REFERENCE_XSM")" = "$EXPECTED_REFERENCE_SHA"

STAGED_OUTPUT="$ARTIFACT_DIR/.rank2_basis.xsm.$$"
cp "$WORK/rank2_candidate_a.xsm" "$STAGED_OUTPUT"
cmp "$WORK/rank2_candidate_a.xsm" "$STAGED_OUTPUT"
test "$(wc -c < "$STAGED_OUTPUT" | tr -d ' ')" = "$EXPECTED_OUTPUT_SIZE"
test "$(hash_file "$STAGED_OUTPUT")" = "$EXPECTED_OUTPUT_SHA"
mv "$STAGED_OUTPUT" "$OUTPUT_XSM"
test "$(hash_file "$OUTPUT_XSM")" = "$EXPECTED_OUTPUT_SHA"
test "$(hash_file "$SNAP_XSM")" = "$EXPECTED_SNAP_SHA"
test "$(hash_file "$REFERENCE_XSM")" = "$EXPECTED_REFERENCE_SHA"

cat "$WORK/check_a.log"
printf '%s\n' \
  "RANK2-BASIS INPUT-SNAPSHOT-SHA256=$EXPECTED_SNAP_SHA" \
  "RANK2-BASIS INPUT-REFERENCE-SHA256=$EXPECTED_REFERENCE_SHA" \
  "RANK2-BASIS OUTPUT-SHA256=$EXPECTED_OUTPUT_SHA" \
  'RANK2-BASIS REPLAY-BITWISE PASS' \
  'RANK2-BASIS INPUTS-READ-ONLY PASS' \
  'RANK2-BASIS DRAGON/ASM/TRANSPORT=0' \
  'RANK2-BASIS CLASSIFICATION=OFFLINE_RECONSTRUCTION_ONLY'
