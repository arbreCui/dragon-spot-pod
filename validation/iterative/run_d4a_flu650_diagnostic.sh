#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RESULT_DIR=${RESULT_DIR:-}
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
DLIB370=${DLIB370:-/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell/DLIB_370}
RUN_D4A_FLU650_DIAGNOSTIC=${RUN_D4A_FLU650_DIAGNOSTIC:-0}
TIMEOUT_SECONDS=600
DECK_SOURCE="$ROOT/validation/iterative/d4a_flu650_diagnostic.x2m"
PROCEDURE_SOURCE="$ROOT/data/SpotD4Snap.c2m"
RUNNER_SOURCE="$ROOT/validation/iterative/run_d4a_flu650_diagnostic.sh"
BOUNDED_HELPER="$ROOT/validation/iterative/run_bounded_dragon.py"
MCGMRE_SOURCE="$ROOT/src/MCGMRE.f"
EXPECTED_DLIB_SHA=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9
ORIGINAL_FLU_LINE='    EDIT 1 TYPE K EXTE 500 <<solver_eps>>'
DIAGNOSTIC_FLU_LINE='    EDIT 2 TYPE K EXTE 500 <<solver_eps>>'

fail() {
  echo "D4A FLU650 DIAGNOSTIC FAIL: $*" >&2
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

test -f "$DECK_SOURCE" || fail "diagnostic deck is missing"
test -f "$PROCEDURE_SOURCE" || fail "snapshot procedure is missing"
test -f "$BOUNDED_HELPER" || fail "bounded runner helper is missing"
test -f "$MCGMRE_SOURCE" || fail "MCGMRE source is missing"
test -x "$DRAGON_BIN" || fail "Dragon executable is missing"
test -f "$DLIB370" || fail "370-group DLIB is missing"
(
  cd "$ROOT"
  sha256sum -c validation/iterative/d4a_snapshot_inputs.sha256 >/dev/null
) || fail "a frozen D4-A repository input changed"

dlib_sha=$(sha256sum "$DLIB370" | awk '{print $1}')
test "$dlib_sha" = "$EXPECTED_DLIB_SHA" ||
  fail "the 370-group DLIB hash changed: $dlib_sha"

expect_count '^    EDIT 1 TYPE K EXTE 500 <<solver_eps>>$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    UNKT <<solver_eps>> THER <<solver_eps>> ;$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    EDIT 1 MXIT 20 EPS 1\.0E-5 TRAN PIJ ;$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    GAUS 4 AAC 80 TMT STIS 1 EPSI <<solver_eps>> MCU 10000$' 1 \
  "$PROCEDURE_SOURCE"
expect_count "^        IF\(IPRINT\.GE\.2\) WRITE\(6,300\) ITER,'INITIAL ',LNCONV,ERROR,$" 1 \
  "$MCGMRE_SOURCE"
expect_count '^          IF\(IPRINT\.GE\.2\) WRITE\(6,310\) ITER,LNCONV$' 1 \
  "$MCGMRE_SOURCE"
expect_count "^          IF\(IPRINT\.GE\.2\) WRITE\(6,300\) ITER,'KRYLOV  ',LNCONV,$" 1 \
  "$MCGMRE_SOURCE"
expect_count '^REAL T_comb := 650\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL T_clad := 620\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL T_Na := 475\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL solver_eps := 5\.0E-7 ;$' 1 "$DECK_SOURCE"
expect_count '^MICROLIB2 SYSTEM FLUX TRACK TRACK_f := SpotD4Snap glow_rnr ::$' 1 \
  "$DECK_SOURCE"
expect_count '^ECHO "D4A-FLU650-DIAGNOSTIC-COMPLETE" ;$' 1 "$DECK_SOURCE"
expect_count '^[^*].*(750\.0|850\.0|BACKUP:|XSM_FILE|SNAP|POD|Picard|SPOT:)' 0 \
  "$DECK_SOURCE"

echo "D4A FLU650 DIAGNOSTIC STATIC PREFLIGHT PASS"
echo "D4A FLU650 STATE C: (650,620,475)"
echo "D4A FLU650 OPERATOR: MCCGT+ASM:ARM+FLU TYPE K"
echo "D4A FLU650 TERMINALS: MCCG_EPSI/EXTE/UNKT/THER=5e-7"
echo "D4A FLU650 ONLY DELTA: FLU EDIT 1 -> EDIT 2"
echo "D4A FLU650 PASSIVE TRACE: MCGMRE ITER/ACTIVE/MAX-REPS"
echo "D4A FLU650 HARD LIMIT: ${TIMEOUT_SECONDS}s, OMP=1, no retry"

if [ "$RUN_D4A_FLU650_DIAGNOSTIC" != 1 ]; then
  echo "D4A FLU650 DIAGNOSTIC DISABLED: set RUN_D4A_FLU650_DIAGNOSTIC=1 and an unused RESULT_DIR"
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

cp "$DECK_SOURCE" "$RESULT_DIR/d4a_flu650_diagnostic.x2m"
sed "s|^$ORIGINAL_FLU_LINE\$|$DIAGNOSTIC_FLU_LINE|" \
  "$PROCEDURE_SOURCE" > "$RESULT_DIR/SpotD4Snap.c2m"
PYTHONDONTWRITEBYTECODE=1 python3 -c '
import sys
source = open(sys.argv[1], encoding="utf-8").read()
staged = open(sys.argv[2], encoding="utf-8").read()
old, new = sys.argv[3], sys.argv[4]
if source.count(old) != 1:
    raise SystemExit("source FLU line is not unique")
if staged != source.replace(old, new):
    raise SystemExit("staged builder differs beyond EDIT 1 -> EDIT 2")
' "$PROCEDURE_SOURCE" "$RESULT_DIR/SpotD4Snap.c2m" \
  "$ORIGINAL_FLU_LINE" "$DIAGNOSTIC_FLU_LINE" ||
  fail "diagnostic builder transformation is not exact"

cp "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat" \
  "$RESULT_DIR/geometry.dat"
ln -s "$DLIB370" "$RESULT_DIR/DLIB8R1_370"

(
  cd "$RESULT_DIR"
  printf '%s\n' \
    'RUN_CLASS=DIAGNOSTIC_ONLY_NO_SNAPSHOT' \
    'STATE_C=650,620,475' \
    'TONE_TRACK_TISO=50.0' \
    'TONE_MXIT=20' \
    'TONE_EPS=1.0E-5' \
    'MCCG_EPSI=5.0E-7' \
    'FLU_TYPE=K' \
    'FLU_MAXOUT=500' \
    'FLU_EPSOUT=5.0E-7' \
    'FLU_EPSUNK=5.0E-7' \
    'FLU_EPSINR=5.0E-7' \
    'FLU_EDIT=2' \
    'OMP_NUM_THREADS=1' \
    'GFORTRAN_UNBUFFERED_ALL=1' \
    'MCGMRE_TRACE=ITER,PHASE,ACTIVE_AFTER,MAX_REPS,EPSI' \
    "WALL_LIMIT_SECONDS=$TIMEOUT_SECONDS" \
    'RETRY=0' > run_contract.txt
  sha256sum d4a_flu650_diagnostic.x2m SpotD4Snap.c2m rnr_cc.c2m \
    rnr_interpol.c2m geometry.dat DLIB8R1_370 run_contract.txt \
    "$PROCEDURE_SOURCE" "$RUNNER_SOURCE" "$BOUNDED_HELPER" \
    "$MCGMRE_SOURCE" \
    > executed_inputs.sha256
  sha256sum "$DRAGON_BIN" > dragon_executable.sha256
)

OMP_NUM_THREADS=1
GFORTRAN_UNBUFFERED_ALL=1
export OMP_NUM_THREADS GFORTRAN_UNBUFFERED_ALL
echo "D4A FLU650 DIAGNOSTIC START: ${TIMEOUT_SECONDS}s bound, no retry"
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
    '^RAW-MOC-CAPTURE PROCESS FAIL: timeout after 600 seconds; no scientific result$' \
    1 "$RESULT_DIR/runner.err"
fi
echo "D4A FLU650 DIAGNOSTIC END: $run_status"

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

echo "D4A FLU650 DIAGNOSTIC CAPTURED: status=$run_status"
echo "D4A FLU650 DIAGNOSTIC RESULT: $RESULT_DIR"
