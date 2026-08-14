#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
X4_DIR=${X4_DIR:-"$ROOT/validation/artifacts/iterative-map4-axial-80s"}
X5_DIR=${X5_DIR:-"$ROOT/validation/artifacts/iterative-map5-axial-80s"}
X6_DIR=${X6_DIR:-"$ROOT/validation/artifacts/iterative-map6-axial-80s"}
X4_NAME=${X4_NAME:-state4_axial.xsm}
X5_NAME=${X5_NAME:-state5_axial.xsm}
X6_NAME=${X6_NAME:-state6_axial.xsm}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
LOCK=${LOCK:-"$ROOT/validation/iterative/anderson1_modal_scientific.sha256"}

test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
test -f "$LOCK"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-anderson1-modal.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

verify_locked() {
  source_dir=$1
  name=$2
  expected=$(awk -v file="$name" '$2 == file { print $1 }' "$LOCK")
  actual=$(shasum -a 256 "$source_dir/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_locked "$X4_DIR" "$X4_NAME"
verify_locked "$X5_DIR" "$X5_NAME"
verify_locked "$X6_DIR" "$X6_NAME"

cp "$X4_DIR/$X4_NAME" "$WORK/x4.xsm"
cp "$X5_DIR/$X5_NAME" "$WORK/x5.xsm"
cp "$X6_DIR/$X6_NAME" "$WORK/x6.xsm"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one_map_xsm"

RESULT=$(
  cd "$WORK"
  ./check_one_map_xsm --anderson1 x4.xsm x5.xsm x6.xsm
)
printf '%s\n' "$RESULT"
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1 AFFINE R_RHO SCREEN PASS'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1 R_RHO RELATIVE-CURRENT WORSENED'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1 LEAKAGE H-L2 RELATIVE-CURRENT WORSENED'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1 AFFINE R_L SCREEN FAIL'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1 AFFINE R_A SCREEN PASS'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1 AFFINE CANONICAL SCREEN REJECT'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1-LEAKAGE R_RHO SCREEN PASS'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1-LEAKAGE R_L SCREEN PASS'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1-LEAKAGE R_A SCREEN PASS'
printf '%s\n' "$RESULT" | grep -Fqx \
  'ANDERSON1-LEAKAGE CANONICAL SCREEN PASS'

verify_locked "$X4_DIR" "$X4_NAME"
verify_locked "$X5_DIR" "$X5_NAME"
verify_locked "$X6_DIR" "$X6_NAME"

printf '%s\n' \
  'ANDERSON1 READ-ONLY HASH PASS' \
  'ANDERSON1 NO-DRAGON PASS'
