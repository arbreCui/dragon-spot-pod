#!/bin/sh
set -eu

RUN_MAP4=${RUN_MAP4:-0}
case "$RUN_MAP4" in
  0)
    printf '%s\n' 'MAP4-SHORT DEFAULT-OFF: no Dragon process started.'
    exit 0
    ;;
  1) ;;
  *)
    printf '%s\n' 'MAP4-SHORT ERROR: RUN_MAP4 must be 0 or 1.' >&2
    exit 2
    ;;
esac

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
SEED_DIR=${SEED_DIR:-"$ROOT/validation/artifacts/iterative-seed"}
BASIS_DIR=${BASIS_DIR:-"$ROOT/validation/artifacts/iterative-map1"}
X3_DIR=${X3_DIR:-"$ROOT/validation/artifacts/iterative-map3-strict-current"}
SEED_LOCK="$ROOT/validation/iterative/seed.sha256"
BASIS_LOCK="$ROOT/validation/iterative/one_map_scientific.sha256"
PARENT_LOCK="$ROOT/validation/iterative/map4_parent_scientific.sha256"
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}
# Each Dragon process waits at most 75 seconds. On timeout the helper allows
# up to five seconds for TERM before KILL. There is no retry.
TIMEOUT_SECONDS=75

test -x "$DRAGON_BIN"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"
test -f "$SEED_LOCK"
test -f "$BASIS_LOCK"
test -f "$PARENT_LOCK"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-map4-short.XXXXXX")
RADIAL_WORK="$WORK/radial"
AXIAL_WORK="$WORK/axial"
mkdir -p "$RADIAL_WORK" "$AXIAL_WORK"
SUCCESS=0
cleanup() {
  if [ "${KEEP_WORK:-0}" = 1 ] || [ "$SUCCESS" != 1 ]; then
    printf 'MAP4-SHORT WORKDIR: %s\n' "$WORK"
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT HUP INT TERM

verify_locked() {
  lock=$1
  source_dir=$2
  name=$3
  expected=$(awk -v file="$name" '$2 == file { print $1 }' "$lock")
  actual=$(shasum -a 256 "$source_dir/$name" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_inputs() {
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_axial_track.xsm
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_axial_macrolib.xsm
  verify_locked "$SEED_LOCK" "$SEED_DIR" initial_radial_track.bin
  verify_locked "$BASIS_LOCK" "$BASIS_DIR" basis_reference.xsm
  verify_locked "$PARENT_LOCK" "$X3_DIR" state3_axial.xsm
  verify_locked "$PARENT_LOCK" "$X3_DIR" state3_snapshots.xsm
}

verify_inputs
for name in initial_axial_track.xsm initial_axial_macrolib.xsm \
  initial_radial_track.bin
do
  cp "$SEED_DIR/$name" "$RADIAL_WORK/$name"
done
cp "$BASIS_DIR/basis_reference.xsm" "$RADIAL_WORK/"
cp "$X3_DIR/state3_axial.xsm" "$X3_DIR/state3_snapshots.xsm" \
  "$RADIAL_WORK/"
cp "$ROOT/data/SpotRefFS.c2m" "$ROOT/data/SpotPlaneFS.c2m" \
  "$RADIAL_WORK/"
cp "$ROOT/validation/iterative/map4_radial.x2m" \
  "$RADIAL_WORK/radial.x2m"
cp "$ROOT/validation/iterative/map4_axial.x2m" \
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

reject_abnormal() {
  if rg -i 'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
    "$1" >/dev/null
  then
    printf '%s\n' \
      'MAP4-SHORT FAIL: abnormal or nonconverged solver marker.' >&2
    exit 1
  fi
}

printf '%s\n' \
  'MAP4-SHORT RADIAL START: 75 s timeout + 5 s TERM grace, no retry'
run_bounded "$RADIAL_WORK/radial.x2m" "$RADIAL_WORK/radial.log"
reject_abnormal "$RADIAL_WORK/radial.log"
test "$(rg -c '^ FLU2DR-TERM OUTER-GATE=PASS ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^ FLU2DR-TERM INNER-TERMINAL ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c 'normal end of execution for dragon' \
  "$RADIAL_WORK/radial.log")" = 1
test "$(rg -c '^SPOFSRC KEFF/QSUM/QMIN/QMAX ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^SPOFCHK L2/MAX/RBAL/MIN/QSUM ' \
  "$RADIAL_WORK/radial.log")" = 3
test "$(rg -c '^>\|MAP4-RADIAL-COMPLETE' \
  "$RADIAL_WORK/radial.log")" = 1
printf '%s\n' 'MAP4-SHORT RADIAL END'

for name in initial_axial_track.xsm initial_axial_macrolib.xsm \
  basis_reference.xsm state3_axial.xsm state4_system.xsm \
  state4_radial.xsm
do
  cp "$RADIAL_WORK/$name" "$AXIAL_WORK/$name"
done

printf '%s\n' \
  'MAP4-SHORT AXIAL START: 75 s timeout + 5 s TERM grace, no retry'
run_bounded "$AXIAL_WORK/axial.x2m" "$AXIAL_WORK/axial.log"
reject_abnormal "$AXIAL_WORK/axial.log"
test "$(rg -c '^ FLU2DR-TERM OUTER-GATE=PASS ' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c '^ FLU2DR-TERM INNER-TERMINAL ' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c 'normal end of execution for dragon' \
  "$AXIAL_WORK/axial.log")" = 1
test "$(rg -c '^>\|MAP4-AXIAL-COMPLETE' \
  "$AXIAL_WORK/axial.log")" = 1
printf '%s\n' 'MAP4-SHORT AXIAL END'

(
  cd "$AXIAL_WORK"
  ./check_one_map_xsm --continued basis_reference.xsm \
    state4_system.xsm state3_axial.xsm state4_axial.xsm \
    state4_snapshots.xsm
  shasum -a 256 state4_system.xsm state4_axial.xsm \
    state4_snapshots.xsm
)

verify_inputs
rg 'MAP4-(RAW-DEFECT|STATE4)|SPOGBAL GLOBAL/MAX-GROUP' \
  "$AXIAL_WORK/axial.log"
shasum -a 256 "$DRAGON_BIN"
printf '%s\n' \
  'MAP4-SHORT PASS: x4=G(x3) complete; convergence not assessed.'
SUCCESS=1
