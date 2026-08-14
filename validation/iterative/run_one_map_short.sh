#!/bin/sh
set -eu

RUN_ONE_MAP=${RUN_ONE_MAP:-0}
case "$RUN_ONE_MAP" in
  0)
    echo "ONE-MAP-SHORT DEFAULT-OFF: no Dragon process started."
    exit 0
    ;;
  1) ;;
  *)
    echo "ONE-MAP-SHORT ERROR: RUN_ONE_MAP must be 0 or 1." >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
SEED_DIR=${SEED_DIR:-"$ROOT/validation/artifacts/iterative-seed"}
X0_DIR=${X0_DIR:-"$ROOT/validation/artifacts/iterative-map1"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
# The process helper waits at most 75 seconds for the Dragon process, then
# allows up to five seconds for TERM before sending KILL.  This is not a
# mathematically strict 80-second total wall-clock deadline.
TIMEOUT_SECONDS=75

test -x "$DRAGON_BIN"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-one-map-short.XXXXXX")
RADIAL_WORK="$WORK/radial"
AXIAL_WORK="$WORK/axial"
mkdir -p "$RADIAL_WORK" "$AXIAL_WORK"
SUCCESS=0
cleanup() {
  if [ "${KEEP_WORK:-0}" = 1 ] || [ "$SUCCESS" != 1 ]; then
    printf 'ONE-MAP-SHORT WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

for name in initial_snapshots.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm initial_radial_track.bin
do
  expected=$(awk -v file="$name" '$2 == file { print $1 }' \
    "$ROOT/validation/iterative/seed.sha256")
  actual=$(shasum -a 256 "$SEED_DIR/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
  cp "$SEED_DIR/$name" "$RADIAL_WORK/$name"
done

for name in basis_reference.xsm state0_axial.xsm
do
  expected=$(awk -v file="$name" '$2 == file { print $1 }' \
    "$ROOT/validation/iterative/one_map_scientific.sha256")
  actual=$(shasum -a 256 "$X0_DIR/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
  cp "$X0_DIR/$name" "$RADIAL_WORK/$name"
done

cp "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" \
  "$RADIAL_WORK/"
cp "$ROOT/validation/iterative/one_map_radial.x2m" \
  "$RADIAL_WORK/radial.x2m"
cp "$ROOT/validation/iterative/one_map_axial.x2m" \
  "$AXIAL_WORK/axial.x2m"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$AXIAL_WORK/check_one_map_xsm"

run_bounded() {
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$ROOT/validation/iterative" \
  python3 -c \
    'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
    "$DRAGON_BIN" "$1" "$2" "$TIMEOUT_SECONDS"
}

echo "ONE-MAP-SHORT RADIAL START: 75 s process timeout + 5 s TERM grace, no retry"
run_bounded "$RADIAL_WORK/radial.x2m" "$RADIAL_WORK/radial.log"
echo "ONE-MAP-SHORT RADIAL END"

for name in initial_axial_track.xsm initial_axial_macrolib.xsm \
  basis_reference.xsm state0_axial.xsm state1_system.xsm \
  state1_radial.xsm
do
  cp "$RADIAL_WORK/$name" "$AXIAL_WORK/$name"
done

echo "ONE-MAP-SHORT AXIAL START: 75 s process timeout + 5 s TERM grace, no retry"
run_bounded "$AXIAL_WORK/axial.x2m" "$AXIAL_WORK/axial.log"
echo "ONE-MAP-SHORT AXIAL END"

if rg -i 'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$RADIAL_WORK/radial.log" "$AXIAL_WORK/axial.log" >/dev/null
then
  echo "ONE-MAP-SHORT FAIL: abnormal or nonconverged solver marker." >&2
  exit 1
fi

test "$(rg -c '^ FLU2DR-TERM OUTER-GATE=PASS ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^ FLU2DR-TERM INNER-TERMINAL ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^ FLU2DR-TERM OUTER-GATE=PASS ' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c '^ FLU2DR-TERM INNER-TERMINAL ' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c 'normal end of execution for dragon' \
  "$RADIAL_WORK/radial.log")" = 1
test "$(rg -c 'normal end of execution for dragon' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c '^SPOFSRC KEFF/QSUM/QMIN/QMAX ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^SPOFCHK L2/MAX/RBAL/MIN/QSUM ' \
  "$RADIAL_WORK/radial.log")" = 3

(
  cd "$AXIAL_WORK"
  ./check_one_map_xsm basis_reference.xsm state1_system.xsm \
    state0_axial.xsm state1_axial.xsm state1_snapshots.xsm
  for name in basis_reference.xsm state0_axial.xsm \
    state1_system.xsm state1_axial.xsm
  do
    expected=$(awk -v file="$name" '$2 == file { print $1 }' \
      "$ROOT/validation/iterative/one_map_scientific.sha256")
    actual=$(shasum -a 256 "$name" | awk '{ print $1 }')
    test "$actual" = "$expected"
    printf 'ONE-MAP-SHORT BITWISE PASS: %s\n' "$name"
  done
  shasum -a 256 state1_snapshots.xsm
)

rg 'ONE-MAP-(RAW-DEFECT|STATE1)|SPOGBAL GLOBAL/MAX-GROUP' \
  "$AXIAL_WORK/axial.log"
shasum -a 256 "$DRAGON_BIN"
echo "ONE-MAP-SHORT PASS: one current raw map; outer convergence not assessed."
SUCCESS=1
