#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
SEED_DIR=${SEED_DIR:-"$ROOT/validation/artifacts/iterative-seed"}
X1_DIR=${X1_DIR:-"$ROOT/validation/artifacts/iterative-map1"}
X2_DIR=${X2_DIR:-"$ROOT/validation/artifacts/iterative-map2-current"}
X3_DIR=${X3_DIR:-"$ROOT/validation/artifacts/iterative-map3-strict-current"}
SEED_LOCK=${SEED_LOCK:-"$ROOT/validation/iterative/seed.sha256"}
STATE_LOCK=${STATE_LOCK:-"$ROOT/validation/iterative/picard_strict_direction_scientific.sha256"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
test -f "$SEED_LOCK"
test -f "$STATE_LOCK"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-leakage-faces.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

verify_locked() {
  lock=$1
  source_dir=$2
  name=$3
  expected=$(awk -v file="$name" '$2 == file { print $1 }' "$lock")
  actual=$(shasum -a 256 "$source_dir/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_all() {
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_axial_track.xsm
  verify_locked "$STATE_LOCK" "$X1_DIR" state1_axial.xsm
  verify_locked "$STATE_LOCK" "$X2_DIR" state2_axial.xsm
  verify_locked "$STATE_LOCK" "$X3_DIR" state3_axial.xsm
}

verify_all
cp "$SEED_DIR/initial_axial_track.xsm" "$WORK/track.xsm"
cp "$X1_DIR/state1_axial.xsm" "$WORK/x1.xsm"
cp "$X2_DIR/state2_axial.xsm" "$WORK/x2.xsm"
cp "$X3_DIR/state3_axial.xsm" "$WORK/x3.xsm"

"$FC" -O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror \
  -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_one_map_xsm"

nm "$WORK/check_one_map_xsm" >"$WORK/symbols.txt"
if grep -Eiq 'SPOLE1|SPOLEAK|SPOSTATE|FLU2DR|GANDRV|GANMAIN' \
    "$WORK/symbols.txt"; then
  printf '%s\n' 'LEAKAGE-FACES ERROR: PRODUCTION/DRIVER SYMBOL LINKED.' >&2
  exit 2
fi

(
  cd "$WORK"
  ./check_one_map_xsm --leakage-faces \
    track.xsm x1.xsm x2.xsm x3.xsm >leakage_faces.log
)

grep -Fq 'LEAKAGE-FACES HOTSPOT PLANE/GROUP/TIES 1 326 1' \
  "$WORK/leakage_faces.log"
grep -Fq 'LEAKAGE-FACES CANONICAL-SP32 BITWISE PASS' \
  "$WORK/leakage_faces.log"
grep -Fq 'LEAKAGE-FACES DELTA12 HIGH-Z-FACE-DOMINANT' \
  "$WORK/leakage_faces.log"
grep -Fq 'LEAKAGE-FACES DELTA23 HIGH-Z-FACE-DOMINANT' \
  "$WORK/leakage_faces.log"
grep -Fq 'LEAKAGE-FACES COMPLETE' "$WORK/leakage_faces.log"

verify_all
cat "$WORK/leakage_faces.log"
printf '%s\n' \
  'LEAKAGE-FACES READ-ONLY HASH PASS' \
  'LEAKAGE-FACES GANLIB-ONLY PASS' \
  'LEAKAGE-FACES NO-DRAGON PASS'
