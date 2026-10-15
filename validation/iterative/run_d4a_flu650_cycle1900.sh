#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PARENT="$ROOT/validation/artifacts/d4a-flu650-flu2ac1500-20260824"
RESULT_DIR=${RESULT_DIR:-}
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
RUN_D4A_FLU650_CYCLE1900=${RUN_D4A_FLU650_CYCLE1900:-0}
TIMEOUT_SECONDS=1900
RUNNER_SOURCE="$ROOT/validation/iterative/run_d4a_flu650_cycle1900.sh"
BOUNDED_HELPER="$ROOT/validation/iterative/run_bounded_dragon.py"
MCGMRE_SOURCE="$ROOT/src/MCGMRE.f"
EXPECTED_DRAGON_SHA=9c529a1c30b13485df55e934774bc9ad369ee58e2c89418376c7364dbd9042ea
EXPECTED_MCGMRE_SHA=f29c0325f2dce3a9c2a9bedc9d5b803154445e5b9c1a8382f8c930827c26b7a6
EXPECTED_DLIB_SHA=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9
EXPECTED_CONTRACT_SHA=45fec89fa782607a052ea457c8378df50ce87a94e072102679c746c7d1277acf

fail() {
  echo "D4A FLU650 CYCLE1900 FAIL: $*" >&2
  exit 1
}

expect_count() {
  pattern=$1
  expected=$2
  file=$3
  count=$(rg -c "$pattern" "$file" || true)
  count=${count:-0}
  test "$count" = "$expected" ||
    fail "expected $expected matches for '$pattern' in $file; found $count"
}

test -d "$PARENT" || fail "frozen 1500 s parent artifact is missing"
test -f "$RUNNER_SOURCE" || fail "runner source is missing"
test -f "$BOUNDED_HELPER" || fail "bounded runner helper is missing"
test -f "$MCGMRE_SOURCE" || fail "MCGMRE source is missing"
test -x "$DRAGON_BIN" || fail "Dragon executable is missing"
(
  cd "$PARENT"
  sha256sum -c executed_inputs.sha256 >/dev/null
  sha256sum -c dragon_executable.sha256 >/dev/null
  sha256sum -c diagnostic_capture_result.sha256 >/dev/null
) || fail "frozen 1500 s parent receipt failed"

dragon_sha=$(sha256sum "$DRAGON_BIN" | awk '{print $1}')
test "$dragon_sha" = "$EXPECTED_DRAGON_SHA" ||
  fail "Dragon hash changed: $dragon_sha"
mcgmre_sha=$(sha256sum "$MCGMRE_SOURCE" | awk '{print $1}')
test "$mcgmre_sha" = "$EXPECTED_MCGMRE_SHA" ||
  fail "MCGMRE hash changed: $mcgmre_sha"
dlib_sha=$(sha256sum "$PARENT/DLIB8R1_370" | awk '{print $1}')
test "$dlib_sha" = "$EXPECTED_DLIB_SHA" ||
  fail "370-group DLIB hash changed: $dlib_sha"

expect_count '^WALL_LIMIT_SECONDS=1500$' 1 "$PARENT/run_contract.txt"
expect_count '^RETRY=0$' 1 "$PARENT/run_contract.txt"
expect_count '^STATE_C=650,620,475$' 1 "$PARENT/run_contract.txt"
expect_count '^FLU_EPSOUT=5.0E-7$' 1 "$PARENT/run_contract.txt"
expect_count '^FLU_EPSUNK=5.0E-7$' 1 "$PARENT/run_contract.txt"
expect_count '^FLU_EPSINR=5.0E-7$' 1 "$PARENT/run_contract.txt"

echo "D4A FLU650 CYCLE1900 STATIC PREFLIGHT PASS"
echo "D4A FLU650 CYCLE1900 PARENT: frozen 1500 s trace artifact"
echo "D4A FLU650 CYCLE1900 ONLY CHANGE: wall limit 1500 -> 1900 s"
echo "D4A FLU650 CYCLE1900 OPERATOR/TOLERANCES: unchanged"
echo "D4A FLU650 CYCLE1900 EXECUTION: OMP=1, no retry"

if [ "$RUN_D4A_FLU650_CYCLE1900" != 1 ]; then
  echo "D4A FLU650 CYCLE1900 DISABLED: set RUN_D4A_FLU650_CYCLE1900=1 and an unused RESULT_DIR"
  exit 0
fi

test -n "$RESULT_DIR" || fail "set RESULT_DIR to a new absolute path"
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path" ;;
esac
test ! -e "$RESULT_DIR" || fail "refusing to overwrite RESULT_DIR"
mkdir -p "$(dirname -- "$RESULT_DIR")"
mkdir "$RESULT_DIR"

cp "$PARENT/d4a_flu650_diagnostic.x2m" "$RESULT_DIR/"
cp "$PARENT/SpotD4Snap.c2m" "$RESULT_DIR/"
cp "$PARENT/rnr_cc.c2m" "$RESULT_DIR/"
cp "$PARENT/rnr_interpol.c2m" "$RESULT_DIR/"
cp "$PARENT/geometry.dat" "$RESULT_DIR/"
dlib_target=$(readlink "$PARENT/DLIB8R1_370")
test -n "$dlib_target" || fail "parent DLIB link has no target"
ln -s "$dlib_target" "$RESULT_DIR/DLIB8R1_370"
sed 's/^WALL_LIMIT_SECONDS=1500$/WALL_LIMIT_SECONDS=1900/' \
  "$PARENT/run_contract.txt" > "$RESULT_DIR/run_contract.txt"

PYTHONDONTWRITEBYTECODE=1 python3 -c '
import sys
parent = open(sys.argv[1], encoding="utf-8").read()
child = open(sys.argv[2], encoding="utf-8").read()
old = "WALL_LIMIT_SECONDS=1500"
new = "WALL_LIMIT_SECONDS=1900"
if parent.count(old) != 1:
    raise SystemExit("parent wall-limit line is not unique")
if child != parent.replace(old, new):
    raise SystemExit("child contract differs beyond wall limit")
' "$PARENT/run_contract.txt" "$RESULT_DIR/run_contract.txt" ||
  fail "1900 s contract transformation is not exact"
contract_sha=$(sha256sum "$RESULT_DIR/run_contract.txt" | awk '{print $1}')
test "$contract_sha" = "$EXPECTED_CONTRACT_SHA" ||
  fail "1900 s contract hash changed: $contract_sha"

(
  cd "$RESULT_DIR"
  sha256sum d4a_flu650_diagnostic.x2m SpotD4Snap.c2m rnr_cc.c2m \
    rnr_interpol.c2m geometry.dat DLIB8R1_370 run_contract.txt \
    "$RUNNER_SOURCE" "$BOUNDED_HELPER" "$MCGMRE_SOURCE" \
    > executed_inputs.sha256
  sha256sum "$DRAGON_BIN" > dragon_executable.sha256
)

OMP_NUM_THREADS=1
GFORTRAN_UNBUFFERED_ALL=1
export OMP_NUM_THREADS GFORTRAN_UNBUFFERED_ALL
echo "D4A FLU650 CYCLE1900 START: 1900 s bound, no retry"
if PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  python3 -c \
  'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
  "$DRAGON_BIN" "$RESULT_DIR/d4a_flu650_diagnostic.x2m" \
  "$RESULT_DIR/d4a_flu650_diagnostic.log" "$TIMEOUT_SECONDS" \
  > "$RESULT_DIR/runner.out" 2> "$RESULT_DIR/runner.err"
then
  run_status=COMPLETED
else
  run_status=TIMEOUT
  expect_count \
    '^RAW-MOC-CAPTURE PROCESS FAIL: timeout after 1900 seconds; no scientific result$' \
    1 "$RESULT_DIR/runner.err"
fi
echo "D4A FLU650 CYCLE1900 END: $run_status"

LOG="$RESULT_DIR/d4a_flu650_diagnostic.log"
test ! -s "$RESULT_DIR/runner.out" || fail "bounded runner stdout is not empty"
expect_count 'MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED' 0 "$LOG"
expect_count 'CONVERGENCE REACHED AT TONE ITERATION' 1 "$LOG"
expect_count '^>\|D4A-FLU650-DIAGNOSTIC-STATE' 1 "$LOG"
expect_count '^->@BEGIN MODULE : FLU:' 1 "$LOG"
expect_count '750\.0|850\.0|D4A-SNAPSHOT-COMPLETE|D4A-THREE-SNAPSHOT' 0 "$LOG"
rg -q '^ MCGMRE-TRACE ITER=.* PHASE=INITIAL ' "$LOG" ||
  fail "initial GMRES residual trace is missing"
rg -q '^ MCGMRE-TRACE RHS-COMPLETE ITER=' "$LOG" ||
  fail "GMRES RHS-complete trace is missing"
rg -q '^ MCGMRE-TRACE ITER=.* PHASE=KRYLOV  ' "$LOG" ||
  fail "Krylov residual trace is missing"
if rg -i \
  'XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$LOG" >/dev/null
then
  fail "Dragon log contains an abnormal terminal"
fi

if [ "$run_status" = COMPLETED ]; then
  test ! -s "$RESULT_DIR/runner.err" || fail "completed run has runner stderr"
  expect_count '^>\|D4A-FLU650-DIAGNOSTIC-COMPLETE' 1 "$LOG"
  expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 1 "$LOG"
  expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 1 "$LOG"
  expect_count 'normal end of execution for dragon' 1 "$LOG"
else
  expect_count '^>\|D4A-FLU650-DIAGNOSTIC-COMPLETE' 0 "$LOG"
  expect_count 'normal end of execution for dragon' 0 "$LOG"
fi

test ! -e "$RESULT_DIR/d4a_snapshots.xsm" ||
  fail "a snapshot archive was unexpectedly created"
(
  cd "$RESULT_DIR"
  sha256sum -c executed_inputs.sha256 >/dev/null
  sha256sum -c dragon_executable.sha256 >/dev/null
  printf 'RUN_STATUS=%s\n' "$run_status" > diagnostic_status.txt
  sha256sum d4a_flu650_diagnostic.log runner.out runner.err \
    run_contract.txt executed_inputs.sha256 dragon_executable.sha256 \
    diagnostic_status.txt > diagnostic_capture_result.sha256
)

echo "D4A FLU650 CYCLE1900 CAPTURED: status=$run_status"
echo "D4A FLU650 CYCLE1900 RESULT: $RESULT_DIR"
