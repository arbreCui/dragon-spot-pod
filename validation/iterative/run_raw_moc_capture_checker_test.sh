#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
DIRNAME=$(uname -sm | sed 's/[ ]/_/')
FC=${FC:-gfortran}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/lib/$DIRNAME/modules"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/lib/$DIRNAME/libGanlib.a"}
UTILIB_LIB=${UTILIB_LIB:-"$ROOT/Utilib/lib/$DIRNAME/libUtilib.a"}
WORK=$(mktemp -d /tmp/moca.XXXXXX)
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
  -c "$ROOT/validation/iterative/make_raw_moc_capture_fixture.f90" \
  -o "$WORK/make_fixture.o"
"$FC" "$WORK/make_fixture.o" "$WORK/SPOMOC.o" \
  "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ -o "$WORK/make_fixture"
"$FC" $COMMON_FLAGS -std=f2008 -I "$GANLIB_MOD" -J "$WORK" \
  -c "$ROOT/validation/iterative/check_raw_moc_capture_xsm.f90" \
  -o "$WORK/check_capture.o"
"$FC" "$WORK/check_capture.o" "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ \
  -o "$WORK/check_capture"

if grep -Eiq \
  '\b(LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMLID|LCMDIL|LCMLIL|LCMDEL|LCMEQU)\b' \
  "$ROOT/validation/iterative/check_raw_moc_capture_xsm.f90"
then
  echo "read-only checker source contains LCM mutation" >&2
  exit 1
fi
if nm -u "$WORK/check_capture.o" | grep -Ei \
  'SPOMOC|DOORFV|MCCGF|MCGFLX|MCGMRE|MCGFL1|MCGFCS|MCGSIG|MCGFCF|MOCFCF'
then
  echo "read-only checker object references production solver symbols" >&2
  exit 1
fi

run_checker()
{
  case_dir=$1
  arm=$2
  output=$3
  "$WORK/check_capture" \
    "$case_dir/track.xsm" \
    "$case_dir/system.xsm" \
    "$case_dir/pre.xsm" \
    "$case_dir/frozen.xsm" \
    "$case_dir/off.xsm" \
    "$case_dir/on.xsm" \
    "$arm" >"$output"
}

for case_name in native_a native_b stationary track
do
  mkdir -p "$WORK/$case_name"
done
"$WORK/make_fixture" "$WORK/native_a" 1 valid
"$WORK/make_fixture" "$WORK/native_b" 1 valid
"$WORK/make_fixture" "$WORK/stationary" 2 valid
"$WORK/make_fixture" "$WORK/track" 1 track

shasum -a 256 "$WORK/native_a"/*.xsm | sort >"$WORK/inputs_before.sha256"
run_checker "$WORK/native_a" 1 "$WORK/native_a.log"
shasum -a 256 "$WORK/native_a"/*.xsm | sort >"$WORK/inputs_after.sha256"
cmp "$WORK/inputs_before.sha256" "$WORK/inputs_after.sha256"
run_checker "$WORK/native_b" 1 "$WORK/native_b.log"
run_checker "$WORK/stationary" 2 "$WORK/stationary.log"
run_checker "$WORK/track" 1 "$WORK/track.log"
cmp "$WORK/native_a.log" "$WORK/native_b.log"

test "$(grep -c '^RAW-MOC-XSM LEDGER ' "$WORK/native_a.log")" -eq 5180
test "$(grep -c '^RAW-MOC-XSM CURRENT ' "$WORK/native_a.log")" -eq 2220
test "$(grep -c '^RAW-MOC-XSM MAX-TIE ' "$WORK/native_a.log")" -eq 1
grep -q '^RAW-MOC-XSM ARM NATIVE$' "$WORK/native_a.log"
grep -q '^RAW-MOC-XSM ARM STATIONARY$' "$WORK/stationary.log"
grep -q '^RAW-MOC-XSM CAPTURE-VALID$' "$WORK/track.log"
grep -q '^RAW-MOC-XSM SCALAR-RELATIVE-TWO-NORM  1.21236465988585977E-007 3E8045A73B866381$' \
  "$WORK/native_a.log"
grep -q '^RAW-MOC-XSM SCALAR-INPUT-NORMALIZED-MAX  1.48067988559094138E-007 3E83DF93CD0CD482$' \
  "$WORK/native_a.log"
grep -q '^RAW-MOC-XSM CAPTURE-VALID$' "$WORK/native_a.log"
grep -q '^RAW-MOC-XSM OUTER-CONVERGENCE NOT-EVALUATED$' \
  "$WORK/native_a.log"
grep -q '^RAW-MOC-XSM STAGE4 NOT-AUTHORIZED$' "$WORK/native_a.log"
grep -q '^RAW-MOC-XSM COMPLETE$' "$WORK/native_a.log"

for mode in status extra non-audit eval source boundary surface-map icode raw
do
  mkdir -p "$WORK/$mode"
  "$WORK/make_fixture" "$WORK/$mode" 1 "$mode"
done

for mode in status extra non-audit eval source boundary surface-map icode
do
  if run_checker "$WORK/$mode" 1 "$WORK/$mode.log" \
       2>"$WORK/$mode.err"
  then
    echo "tampered fixture unexpectedly passed: $mode" >&2
    exit 1
  fi
done
grep -q 'audit STATE-VECTOR differs' "$WORK/status.err"
grep -Eq 'AUDIT ROOT (census|names) differs' "$WORK/extra.err"
grep -q 'non-audit primitive value differs' "$WORK/non-audit.err"
grep -q 'EVAL differs from frozen PRE input' "$WORK/eval.err"
grep -q 'volume source replay differs' "$WORK/source.err"
grep -q 'boundary source replay differs' "$WORK/boundary.err"
grep -q 'boundary source replay differs' "$WORK/surface-map.err"
grep -q 'positive ICODE exceeds group ALBEDO' "$WORK/icode.err"

run_checker "$WORK/raw" 1 "$WORK/raw.log"
grep -q '^RAW-MOC-XSM CAPTURE-VALID$' "$WORK/raw.log"
if cmp -s "$WORK/native_a.log" "$WORK/raw.log"; then
  echo "RAW one-bit change did not alter the scientific receipt" >&2
  exit 1
fi

echo "RAW-MOC-CAPTURE CHECKER TEST PASS"
