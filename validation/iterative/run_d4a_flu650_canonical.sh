#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RESULT_DIR=${RESULT_DIR:-}
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
DLIB370=${DLIB370:-/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell/DLIB_370}
RUN_D4A_FLU650_CANONICAL=${RUN_D4A_FLU650_CANONICAL:-0}
TIMEOUT_SECONDS=14400
DECK_SOURCE="$ROOT/validation/iterative/d4a_flu650_diagnostic.x2m"
PROCEDURE_SOURCE="$ROOT/data/SpotD4Snap.c2m"
RUNNER_SOURCE="$ROOT/validation/iterative/run_d4a_flu650_canonical.sh"
BOUNDED_HELPER="$ROOT/validation/iterative/run_bounded_dragon.py"
EXPECTED_DECK_SHA=746d06d399ac3762f2eb2ce8dc07bacdd8eda1d1291cd9b270c25409037c5307
EXPECTED_SNAPSHOT_INPUTS_SHA=342344e207c73a684718b6052521261a24febda84638eafb296686099fa8fdaa
EXPECTED_PROCEDURE_SHA=ac353b81c4de6b0d7f2cbf3b8ec1e4370a599335409c54a5997070334c35acf9
EXPECTED_GEOMETRY_SHA=ca46ef77ea769059ddc612f1a78e4b565c32990401b21652c822bf2e11497a3e
EXPECTED_RNR_CC_SHA=3f7583449d279614eff3b1f1fe6b9a2ca0832612e3b90f4f68d1c2995ce71c03
EXPECTED_RNR_INTERPOL_SHA=b09f93be0655d5ac017b3dc33a3b9d38c5dfb7f12ba70060ec2a050223895c6a
EXPECTED_HELPER_SHA=dc2695e22ad903b3fa729f689baf6995065661441213e7efaf344b4926255a94
EXPECTED_DRAGON_SHA=170fae8855a728ca6d86619a0572e3c0ac494a452110d02c4fdec0d2db50c981
EXPECTED_DLIB_SHA=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9

fail() {
  echo "D4A FLU650 CANONICAL FAIL: $*" >&2
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

require_sha() {
  expected=$1
  file=$2
  label=$3
  actual=$(sha256sum "$file" | awk '{print $1}')
  test "$actual" = "$expected" || fail "$label hash changed: $actual"
}

test -f "$DECK_SOURCE" || fail "single-state deck is missing"
test -f "$PROCEDURE_SOURCE" || fail "snapshot procedure is missing"
test -f "$BOUNDED_HELPER" || fail "bounded runner helper is missing"
test -x "$DRAGON_BIN" || fail "Dragon executable is missing"
test -f "$DLIB370" || fail "370-group DLIB is missing"
require_sha "$EXPECTED_HELPER_SHA" "$BOUNDED_HELPER" "bounded helper"
snapshot_inputs_sha=$(sha256sum \
  "$ROOT/validation/iterative/d4a_snapshot_inputs.sha256" | awk '{print $1}')
test "$snapshot_inputs_sha" = "$EXPECTED_SNAPSHOT_INPUTS_SHA" ||
  fail "frozen D4-A manifest hash changed: $snapshot_inputs_sha"
(
  cd "$ROOT"
  sha256sum -c validation/iterative/d4a_snapshot_inputs.sha256 >/dev/null
) || fail "a frozen D4-A repository input changed"

deck_sha=$(sha256sum "$DECK_SOURCE" | awk '{print $1}')
test "$deck_sha" = "$EXPECTED_DECK_SHA" ||
  fail "single-state deck hash changed: $deck_sha"
dragon_sha=$(sha256sum "$DRAGON_BIN" | awk '{print $1}')
test "$dragon_sha" = "$EXPECTED_DRAGON_SHA" ||
  fail "Dragon hash changed: $dragon_sha"
dlib_sha=$(sha256sum "$DLIB370" | awk '{print $1}')
test "$dlib_sha" = "$EXPECTED_DLIB_SHA" ||
  fail "370-group DLIB hash changed: $dlib_sha"

expect_count '^    EDIT 1 TYPE K EXTE 500 <<solver_eps>>$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    UNKT <<solver_eps>> THER <<solver_eps>> ;$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    EDIT 1 MXIT 20 EPS 1\.0E-5 TRAN PIJ ;$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    GAUS 4 AAC 80 TMT STIS 1 EPSI <<solver_eps>> MCU 10000$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^REAL T_comb := 650\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL T_clad := 620\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL T_Na := 475\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL solver_eps := 5\.0E-7 ;$' 1 "$DECK_SOURCE"
expect_count '^MICROLIB2 SYSTEM FLUX TRACK TRACK_f := SpotD4Snap glow_rnr ::$' 1 \
  "$DECK_SOURCE"
expect_count '^[^*].*(750\.0|850\.0|BACKUP:|XSM_FILE|SNAP|POD|Picard|SPOT:)' 0 \
  "$DECK_SOURCE"

echo "D4A FLU650 CANONICAL STATIC PREFLIGHT PASS"
echo "D4A FLU650 CANONICAL STATE C: (650,620,475)"
echo "D4A FLU650 CANONICAL OPERATOR: MCCGT+ASM:ARM+FLU TYPE K"
echo "D4A FLU650 CANONICAL TERMINALS: MCCG_EPSI/EXTE/UNKT/THER=5e-7"
echo "D4A FLU650 CANONICAL OUTPUT: EDIT 1, unbuffered"
echo "D4A FLU650 CANONICAL EXECUTION: ${TIMEOUT_SECONDS}s cap, OMP=1, no retry"

if [ "$RUN_D4A_FLU650_CANONICAL" != 1 ]; then
  echo "D4A FLU650 CANONICAL DISABLED: set RUN_D4A_FLU650_CANONICAL=1 and an unused RESULT_DIR"
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

cp "$DECK_SOURCE" "$RESULT_DIR/d4a_flu650_canonical.x2m"
cp "$PROCEDURE_SOURCE" "$RESULT_DIR/SpotD4Snap.c2m"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat" \
  "$RESULT_DIR/geometry.dat"
cp "$ROOT/validation/iterative/d4a_snapshot_inputs.sha256" \
  "$RESULT_DIR/frozen_repository_inputs.sha256"
cp "$RUNNER_SOURCE" "$RESULT_DIR/run_d4a_flu650_canonical.sh"
cp "$BOUNDED_HELPER" "$RESULT_DIR/run_bounded_dragon.py"
cp "$DRAGON_BIN" "$RESULT_DIR/Dragon"
ln -s "$DLIB370" "$RESULT_DIR/DLIB8R1_370"
require_sha "$EXPECTED_DECK_SHA" \
  "$RESULT_DIR/d4a_flu650_canonical.x2m" "staged deck"
require_sha "$EXPECTED_PROCEDURE_SHA" \
  "$RESULT_DIR/SpotD4Snap.c2m" "staged procedure"
require_sha "$EXPECTED_RNR_CC_SHA" "$RESULT_DIR/rnr_cc.c2m" "staged rnr_cc"
require_sha "$EXPECTED_RNR_INTERPOL_SHA" \
  "$RESULT_DIR/rnr_interpol.c2m" "staged rnr_interpol"
require_sha "$EXPECTED_GEOMETRY_SHA" "$RESULT_DIR/geometry.dat" "staged geometry"
require_sha "$EXPECTED_SNAPSHOT_INPUTS_SHA" \
  "$RESULT_DIR/frozen_repository_inputs.sha256" "staged frozen manifest"
require_sha "$EXPECTED_HELPER_SHA" \
  "$RESULT_DIR/run_bounded_dragon.py" "staged bounded helper"
require_sha "$EXPECTED_DRAGON_SHA" "$RESULT_DIR/Dragon" "staged Dragon"
require_sha "$EXPECTED_DLIB_SHA" "$RESULT_DIR/DLIB8R1_370" "staged DLIB"

(
  cd "$RESULT_DIR"
  printf '%s\n' \
    'RUN_CLASS=CANONICAL_SINGLE_STATE_GATE_NO_SNAPSHOT' \
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
    'FLU_EDIT=1' \
    'OMP_NUM_THREADS=1' \
    'GFORTRAN_UNBUFFERED_ALL=1' \
    "WALL_LIMIT_SECONDS=$TIMEOUT_SECONDS" \
    'RETRY=0' > run_contract.txt
  sha256sum d4a_flu650_canonical.x2m SpotD4Snap.c2m rnr_cc.c2m \
    rnr_interpol.c2m geometry.dat DLIB8R1_370 run_contract.txt \
    frozen_repository_inputs.sha256 run_d4a_flu650_canonical.sh \
    run_bounded_dragon.py Dragon > executed_inputs.sha256
  sha256sum Dragon > dragon_executable.sha256
)

OMP_NUM_THREADS=1
GFORTRAN_UNBUFFERED_ALL=1
export OMP_NUM_THREADS GFORTRAN_UNBUFFERED_ALL
echo "D4A FLU650 CANONICAL START: ${TIMEOUT_SECONDS}s cap, no retry"
if PYTHONDONTWRITEBYTECODE=1 python3 -c \
  'import importlib.util, sys; from pathlib import Path; p=Path(sys.argv[1]).resolve(); s=importlib.util.spec_from_file_location("spot_bounded_dragon",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.run(Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),float(sys.argv[5]))' \
  "$RESULT_DIR/run_bounded_dragon.py" "$RESULT_DIR/Dragon" \
  "$RESULT_DIR/d4a_flu650_canonical.x2m" \
  "$RESULT_DIR/d4a_flu650_canonical.log" "$TIMEOUT_SECONDS" \
  > "$RESULT_DIR/runner.out" 2> "$RESULT_DIR/runner.err"
then
  process_status=COMPLETED
else
  if rg -x \
    'RAW-MOC-CAPTURE PROCESS FAIL: timeout after 14400 seconds; no scientific result' \
    "$RESULT_DIR/runner.err" >/dev/null
  then
    process_status=TIMEOUT
  else
    process_status=FAILED
  fi
fi

LOG="$RESULT_DIR/d4a_flu650_canonical.log"
test -f "$LOG" || touch "$LOG"
(
  cd "$RESULT_DIR"
  sha256sum -c executed_inputs.sha256 >/dev/null
  sha256sum -c dragon_executable.sha256 >/dev/null
  printf 'PROCESS_STATUS=%s\n' "$process_status" > canonical_status.txt
  sha256sum d4a_flu650_canonical.log runner.out runner.err \
    run_contract.txt executed_inputs.sha256 dragon_executable.sha256 \
    canonical_status.txt > canonical_capture.sha256
)

if [ "$process_status" = COMPLETED ]; then
  if (
    test ! -s "$RESULT_DIR/runner.out" || fail "bounded runner stdout is not empty"
    expect_count 'MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED' 0 "$LOG"
    expect_count 'CONVERGENCE REACHED AT TONE ITERATION' 1 "$LOG"
    expect_count '^>\|D4A-FLU650-DIAGNOSTIC-STATE' 1 "$LOG"
    expect_count '^->@BEGIN MODULE : FLU:' 1 "$LOG"
    expect_count '750\.0|850\.0|D4A-SNAPSHOT-COMPLETE|D4A-THREE-SNAPSHOT' 0 "$LOG"
    if rg -i \
      'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
      "$LOG" >/dev/null
    then
      fail "Dragon log contains an abnormal terminal"
    fi
    test ! -s "$RESULT_DIR/runner.err" || fail "completed run has runner stderr"
    expect_count '^>\|D4A-FLU650-DIAGNOSTIC-COMPLETE' 1 "$LOG"
    expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 1 "$LOG"
    expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 1 "$LOG"
    expect_count '^ FLU2DR-TERM INNER-TERMINAL .* STATE=1 NGRP= *370$' 1 "$LOG"
    expect_count 'normal end of execution for dragon' 1 "$LOG"
    test ! -e "$RESULT_DIR/d4a_snapshots.xsm" ||
      fail "a snapshot archive was unexpectedly created"
  )
  then
    validation_status=PASS
    scientific_status=ACCEPTED
  else
    validation_status=FAILED
    scientific_status=NO_RESULT
  fi
else
  validation_status=NOT_RUN
  scientific_status=NO_RESULT
fi

(
  cd "$RESULT_DIR"
  printf 'SCIENTIFIC_STATUS=%s\n' "$scientific_status" \
    > scientific_status.txt
  printf 'VALIDATION_STATUS=%s\n' "$validation_status" \
    > validation_status.txt
  sha256sum d4a_flu650_canonical.log runner.out runner.err \
    run_contract.txt executed_inputs.sha256 dragon_executable.sha256 \
    canonical_status.txt canonical_capture.sha256 scientific_status.txt \
    validation_status.txt \
    > canonical_result.sha256
)

echo "D4A FLU650 CANONICAL END: $process_status/$validation_status/$scientific_status"
echo "D4A FLU650 CANONICAL RESULT: $RESULT_DIR"
case "$process_status" in
  COMPLETED)
    test "$validation_status" = PASS || exit 4
    exit 0
    ;;
  TIMEOUT) exit 2 ;;
  *) exit 3 ;;
esac
