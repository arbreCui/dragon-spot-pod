#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DIRNAME=$(uname -sm | sed 's/[ ]/_/')
FC=${FC:-gfortran}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/lib/$DIRNAME/modules"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/lib/$DIRNAME/libGanlib.a"}
READER="$ROOT/validation/iterative/check_raw_moc_ulp_bridge_xsm.f90"
FIXTURE="$ROOT/validation/iterative/make_raw_moc_ulp_bridge_fixture.f90"
LOG_CHECKER="$ROOT/validation/iterative/check_raw_moc_ulp_bridge_log.py"
WORK=$(mktemp -d /tmp/spot-ulp-test.XXXXXX)
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

for path in "$GANLIB_MOD/ganlib.mod" "$GANLIB_LIB" \
  "$READER" "$FIXTURE" "$LOG_CHECKER"
do
  test -f "$path"
  test ! -L "$path"
done

FC_FLAGS="-std=f2008 -O0 -Wall -Wextra -Werror
  -Wno-compare-reals -fcheck=all -ffp-contract=off
  -fno-fast-math -ffpe-summary=none"
"$FC" $FC_FLAGS -I "$GANLIB_MOD" -c "$READER" \
  -o "$WORK/reader.o"
"$FC" "$WORK/reader.o" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/reader"
"$FC" $FC_FLAGS -I "$GANLIB_MOD" -c "$FIXTURE" \
  -o "$WORK/fixture.o"
"$FC" "$WORK/fixture.o" "$GANLIB_LIB" -lstdc++ \
  -o "$WORK/fixture"

if rg -i \
  '\b(LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMDIL|LCMLID|LCMLIL|LCMDEL|LCMEQU)\b' \
  "$READER" >/dev/null
then
  echo "RAW-MOC-ULP TEST FAIL: reader source contains LCM mutation" >&2
  exit 1
fi
nm -u "$WORK/reader.o" >"$WORK/reader.object.nm"
if rg -i \
  'SPOMOC|DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|MCGFLX|MCGMRE|SPOT1P' \
  "$WORK/reader.object.nm" >/dev/null
then
  echo "RAW-MOC-ULP TEST FAIL: reader object references solver symbols" >&2
  exit 1
fi
rg -i 'lcmop' "$WORK/reader.object.nm" >/dev/null

"$WORK/reader" SELFTEST >"$WORK/selftest_a.log" \
  2>"$WORK/selftest_a.err"
"$WORK/reader" SELFTEST >"$WORK/selftest_b.log" \
  2>"$WORK/selftest_b.err"
test ! -s "$WORK/selftest_a.err"
test ! -s "$WORK/selftest_b.err"
cmp "$WORK/selftest_a.log" "$WORK/selftest_b.log"
grep '^RAW-MOC-ULP SELFTEST PASS$' "$WORK/selftest_a.log" >/dev/null

run_reader()
{
  case_dir=$1
  arm=$2
  output=$3
  (
    cd "$case_dir"
    "$WORK/reader" track.xsm pre.xsm off.xsm on.xsm "$arm"
  ) >"$output"
}

run_reader_clean()
{
  case_dir=$1
  arm=$2
  output=$3
  run_reader "$case_dir" "$arm" "$output" 2>"$output.err"
  test ! -s "$output.err"
}

for name in native_a native_b stationary current raw_bit off_bit \
  raw_underflow raw_subnormal alternate
do
  mkdir "$WORK/$name"
done
"$WORK/fixture" "$WORK/native_a" 1 valid
"$WORK/fixture" "$WORK/native_b" 1 valid
"$WORK/fixture" "$WORK/stationary" 2 valid
"$WORK/fixture" "$WORK/current" 1 current
"$WORK/fixture" "$WORK/raw_bit" 1 raw-bit
"$WORK/fixture" "$WORK/off_bit" 1 off-bit
"$WORK/fixture" "$WORK/raw_underflow" 1 raw-underflow
"$WORK/fixture" "$WORK/raw_subnormal" 1 raw-subnormal
"$WORK/fixture" "$WORK/alternate" 2 key-alternate

shasum -a 256 "$WORK/native_a"/*.xsm | sort \
  >"$WORK/inputs_before.sha256"
run_reader_clean "$WORK/native_a" 1 "$WORK/native_a.log"
shasum -a 256 "$WORK/native_a"/*.xsm | sort \
  >"$WORK/inputs_after.sha256"
cmp "$WORK/inputs_before.sha256" "$WORK/inputs_after.sha256"
run_reader_clean "$WORK/native_b" 1 "$WORK/native_b.log"
run_reader_clean "$WORK/stationary" 2 "$WORK/stationary.log"
run_reader_clean "$WORK/current" 1 "$WORK/current.log"
run_reader_clean "$WORK/raw_bit" 1 "$WORK/raw_bit.log"
run_reader_clean "$WORK/off_bit" 1 "$WORK/off_bit.log"
run_reader_clean "$WORK/raw_underflow" 1 "$WORK/raw_underflow.log"
run_reader_clean "$WORK/raw_subnormal" 1 "$WORK/raw_subnormal.log"
run_reader_clean "$WORK/alternate" 2 "$WORK/alternate.log"

cmp "$WORK/native_a.log" "$WORK/native_b.log"
cmp "$WORK/native_a.log" "$WORK/current.log"
if cmp -s "$WORK/native_a.log" "$WORK/raw_bit.log"; then
  echo "RAW-MOC-ULP TEST FAIL: RAW64 one-bit tamper was invisible" >&2
  exit 1
fi
grep -v ' LEDGER ' "$WORK/native_a.log" >"$WORK/native_a.compact"
grep -v ' LEDGER ' "$WORK/raw_bit.log" >"$WORK/raw_bit.compact"
cmp "$WORK/native_a.compact" "$WORK/raw_bit.compact"
if cmp -s "$WORK/native_a.log" "$WORK/off_bit.log"; then
  echo "RAW-MOC-ULP TEST FAIL: OFF one-bit tamper was invisible" >&2
  exit 1
fi

python3 "$LOG_CHECKER" --fixture "$WORK/native_a.log" \
  >"$WORK/log_check_a.log" 2>"$WORK/log_check_a.err"
python3 "$LOG_CHECKER" --fixture "$WORK/native_a.log" \
  >"$WORK/log_check_b.log" 2>"$WORK/log_check_b.err"
test ! -s "$WORK/log_check_a.err"
test ! -s "$WORK/log_check_b.err"
cmp "$WORK/log_check_a.log" "$WORK/log_check_b.log"
python3 "$LOG_CHECKER" --fixture "$WORK/stationary.log" >/dev/null
python3 "$LOG_CHECKER" --fixture "$WORK/raw_bit.log" >/dev/null
python3 "$LOG_CHECKER" "$WORK/off_bit.log" >/dev/null
python3 "$LOG_CHECKER" "$WORK/raw_underflow.log" >/dev/null
python3 "$LOG_CHECKER" "$WORK/raw_subnormal.log" >/dev/null
python3 "$LOG_CHECKER" "$WORK/alternate.log" >/dev/null
cat "$WORK/native_a.log" "$WORK/alternate.log" \
  >"$WORK/cross_arm_layout.log"
if python3 "$LOG_CHECKER" "$WORK/cross_arm_layout.log" \
    >"$WORK/cross_arm_layout.out" 2>"$WORK/cross_arm_layout.err"
then
  echo "RAW-MOC-ULP TEST FAIL: cross-arm KEYFLX mismatch passed" >&2
  exit 1
fi
grep 'arm KEYFLX layouts differ' "$WORK/cross_arm_layout.err" >/dev/null
grep '^RAW-MOC-ULP NATIVE RAW-BRIDGE ROUNDED-TO-ZERO 1$' \
  "$WORK/raw_underflow.log" >/dev/null
grep '^RAW-MOC-ULP NATIVE RAW-BRIDGE ROUNDED-SUBNORMAL 1$' \
  "$WORK/raw_subnormal.log" >/dev/null

grep '^RAW-MOC-ULP NATIVE RAW-BRIDGE UNCHANGED 423$' \
  "$WORK/native_a.log" >/dev/null
grep '^RAW-MOC-ULP NATIVE RAW-BRIDGE RAW-EXACT 212$' \
  "$WORK/native_a.log" >/dev/null
grep '^RAW-MOC-ULP NATIVE RAW-BRIDGE ROUND-COLLAPSED-NONZERO 211$' \
  "$WORK/native_a.log" >/dev/null
grep '^RAW-MOC-ULP NATIVE RAW-BRIDGE MAX-STEPS 3$' \
  "$WORK/native_a.log" >/dev/null
grep '^RAW-MOC-ULP NATIVE PRODUCTION-STEP MAX-STEPS 4$' \
  "$WORK/native_a.log" >/dev/null
test "$(grep -c ' RAW-BRIDGE LEDGER ' "$WORK/native_a.log")" -eq 2960
test "$(grep -c ' PRODUCTION-STEP LEDGER ' "$WORK/native_a.log")" \
  -eq 2960

for mode in pre eval group ngind incomplete extra raw-type raw-nan \
  raw-inf raw-negative raw-overflow eval-zero eval-negative-zero \
  eval-nan eval-nonpromotion off-zero off-nan key-duplicate key-long \
  track-branch pre-type off-length eval-type raw-length qfr-type \
  src-length step-type role-length missing-audit
do
  mkdir "$WORK/$mode"
  "$WORK/fixture" "$WORK/$mode" 1 "$mode"
  if run_reader "$WORK/$mode" 1 "$WORK/$mode.log" \
      2>"$WORK/$mode.err"
  then
    echo "RAW-MOC-ULP TEST FAIL: tamper passed: $mode" >&2
    exit 1
  fi
done

grep 'EVAL differs from PRE' "$WORK/pre.err" >/dev/null
grep 'EVAL differs from PRE' "$WORK/eval.err" >/dev/null
grep 'audit group marker differs' "$WORK/group.err" >/dev/null
grep 'audit NGIND differs' "$WORK/ngind.err" >/dev/null
grep 'audit STATE-VECTOR differs' "$WORK/incomplete.err" >/dev/null
grep 'AUDIT ROOT census differs' "$WORK/extra.err" >/dev/null
grep 'record contract failure' "$WORK/raw-type.err" >/dev/null
grep 'audit contains nonfinite tuple' "$WORK/raw-nan.err" >/dev/null
grep 'audit contains nonfinite tuple' "$WORK/raw-inf.err" >/dev/null
grep 'bridge scalar input is not strictly positive' \
  "$WORK/raw-negative.err" >/dev/null
grep 'RAW conversion overflow' "$WORK/raw-overflow.err" >/dev/null
grep 'bridge scalar input is not strictly positive' \
  "$WORK/eval-zero.err" >/dev/null
grep 'bridge scalar input is not strictly positive' \
  "$WORK/eval-negative-zero.err" >/dev/null
grep 'audit contains nonfinite tuple' "$WORK/eval-nan.err" >/dev/null
grep 'EVAL is not an exact binary32 promotion' \
  "$WORK/eval-nonpromotion.err" >/dev/null
grep 'production scalar is not strictly positive' \
  "$WORK/off-zero.err" >/dev/null
grep 'OFF contains nonfinite FLUX' "$WORK/off-nan.err" >/dev/null
grep 'invalid KEYFLX layout' "$WORK/key-duplicate.err" >/dev/null
grep 'record contract failure' "$WORK/key-long.err" >/dev/null
grep 'TRACK dimensions or MCCG branch differ' \
  "$WORK/track-branch.err" >/dev/null
grep 'list item contract failure' "$WORK/pre-type.err" >/dev/null
grep 'list item contract failure' "$WORK/off-length.err" >/dev/null
grep 'record contract failure' "$WORK/eval-type.err" >/dev/null
grep 'record contract failure' "$WORK/raw-length.err" >/dev/null
grep 'record contract failure' "$WORK/qfr-type.err" >/dev/null
grep 'record contract failure' "$WORK/src-length.err" >/dev/null
grep 'record contract failure' "$WORK/step-type.err" >/dev/null
grep 'record contract failure' "$WORK/role-length.err" >/dev/null
grep 'record contract failure' "$WORK/missing-audit.err" >/dev/null

echo "RAW-MOC-ULP CHECKER TEST PASS"
