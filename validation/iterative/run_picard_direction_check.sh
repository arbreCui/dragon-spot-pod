#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
X1_DIR=${X1_DIR:-"$ROOT/validation/artifacts/iterative-map1"}
X2_DIR=${X2_DIR:-"$ROOT/validation/artifacts/iterative-map2-current"}
X3_DIR=${X3_DIR:-"$ROOT/validation/artifacts/iterative-map3-current"}
X1_NAME=${X1_NAME:-state1_axial.xsm}
X2_NAME=${X2_NAME:-state2_axial.xsm}
X3_NAME=${X3_NAME:-state3_axial.xsm}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
LOCK=${LOCK:-"$ROOT/validation/iterative/picard_direction_scientific.sha256"}

test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
test -f "$LOCK"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-picard-direction.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

verify_locked() {
  source_dir=$1
  name=$2
  expected=$(awk -v file="$name" '$2 == file { print $1 }' "$LOCK")
  actual=$(shasum -a 256 "$source_dir/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_locked "$X1_DIR" "$X1_NAME"
verify_locked "$X2_DIR" "$X2_NAME"
verify_locked "$X3_DIR" "$X3_NAME"

cp "$X1_DIR/$X1_NAME" "$WORK/x1.xsm"
cp "$X2_DIR/$X2_NAME" "$WORK/x2.xsm"
cp "$X3_DIR/$X3_NAME" "$WORK/x3.xsm"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one_map_xsm"

(
  cd "$WORK"
  ./check_one_map_xsm --directions x1.xsm x2.xsm x3.xsm
)

verify_locked "$X1_DIR" "$X1_NAME"
verify_locked "$X2_DIR" "$X2_NAME"
verify_locked "$X3_DIR" "$X3_NAME"

printf '%s\n' \
  'PICARD-DIRECTION READ-ONLY HASH PASS' \
  'PICARD-DIRECTION NO-DRAGON PASS'
