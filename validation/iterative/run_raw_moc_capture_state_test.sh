#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
DIRNAME=$(uname -sm | sed 's/[ ]/_/')
FC=${FC:-gfortran}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/lib/$DIRNAME/modules"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/lib/$DIRNAME/libGanlib.a"}
UTILIB_LIB=${UTILIB_LIB:-"$ROOT/Utilib/lib/$DIRNAME/libUtilib.a"}
WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-raw-moc-state.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

for path in "$GANLIB_MOD/ganlib.mod" "$GANLIB_LIB" "$UTILIB_LIB"; do
  test -f "$path" || {
    echo "missing build dependency: $path" >&2
    exit 2
  }
done

COMMON_FLAGS="-Wall -Wextra -ffp-contract=off -fno-fast-math"
"$FC" $COMMON_FLAGS -std=f2008 -I "$GANLIB_MOD" -J "$WORK" \
  -c "$ROOT/src/SPOMOC.f90" -o "$WORK/SPOMOC.o"
"$FC" $COMMON_FLAGS -std=f2008 -I "$GANLIB_MOD" -I "$WORK" -J "$WORK" \
  -c "$ROOT/validation/iterative/test_raw_moc_capture_state.f90" \
  -o "$WORK/test_raw_moc_capture_state.o"
"$FC" "$WORK/test_raw_moc_capture_state.o" "$WORK/SPOMOC.o" \
  "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ \
  -o "$WORK/test_raw_moc_capture_state"

for source in FLUGPI.f FLU.f FLUDRV.f FLU2DR.f MCCGF.f MCGFL1.f MCGMRE.f
do
  "$FC" -Wall -ffixed-form -ffixed-line-length-72 -ffp-contract=off \
    -fno-fast-math -I "$GANLIB_MOD" -I "$WORK" \
    -c "$ROOT/src/$source" -o "$WORK/${source%.f}.o"
done

if nm -u "$WORK/SPOMOC.o" | grep -E \
  'DOORFV|MCGFCS|MCGFCF|MOCFCF|MCGFST|MCGFCA|MCGSCR|FLUBAL|FLU2AC'
then
  echo "capture helper references a solver or transport routine" >&2
  exit 1
fi

"$WORK/test_raw_moc_capture_state" off >"$WORK/off_a.log"
"$WORK/test_raw_moc_capture_state" off >"$WORK/off_b.log"
"$WORK/test_raw_moc_capture_state" valid >"$WORK/valid_a.log"
"$WORK/test_raw_moc_capture_state" valid >"$WORK/valid_b.log"
cmp "$WORK/off_a.log" "$WORK/off_b.log"
cmp "$WORK/valid_a.log" "$WORK/valid_b.log"
test "$(cat "$WORK/off_a.log")" = "RAW-MOC-STATE OFF PASS"
test "$(cat "$WORK/valid_a.log")" = "RAW-MOC-STATE VALID PASS"

for mode in duplicate wrong-path partial-publish wrong-step overwrite
do
  if "$WORK/test_raw_moc_capture_state" "$mode" \
       >"$WORK/$mode.log" 2>&1
  then
    echo "fail-closed mode unexpectedly passed: $mode" >&2
    exit 1
  fi
done

grep -q 'nested or repeated BEGIN' "$WORK/duplicate.log"
grep -q 'direct vector DOORFV path required' "$WORK/wrong-path.log"
grep -q 'primary tuple is incomplete' "$WORK/partial-publish.log"
grep -q 'first primary step required' "$WORK/wrong-step.log"
grep -q 'primary tuple overwrite attempted' "$WORK/overwrite.log"

echo "RAW-MOC-CAPTURE STATE TEST PASS"
