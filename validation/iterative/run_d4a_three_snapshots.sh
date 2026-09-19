#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
DLIB370=${DLIB370:-/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell/DLIB_370}
RUN_D4A_SNAPSHOTS=${RUN_D4A_SNAPSHOTS:-0}
TIMEOUT_SECONDS=${TIMEOUT_SECONDS:-}

fail() {
  echo "D4A SNAPSHOT BUILD FAIL: $*" >&2
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

DLIB370="$DLIB370" sh "$ROOT/validation/iterative/preflight_d4a_three_snapshots.sh"

if [ "$RUN_D4A_SNAPSHOTS" != 1 ]; then
  echo "D4A SNAPSHOT BUILD DISABLED: set RUN_D4A_SNAPSHOTS=1, TIMEOUT_SECONDS, and an unused RESULT_DIR"
  exit 0
fi

test -x "$DRAGON_BIN"
test -f "$DLIB370"
case "$TIMEOUT_SECONDS" in
  ''|*[!0-9]*|0) fail "set TIMEOUT_SECONDS to an explicit positive wall limit" ;;
esac
test -n "${RESULT_DIR:-}"
case "$RESULT_DIR" in
  /*) ;;
  *) echo "RESULT_DIR must be an absolute path" >&2; exit 1 ;;
esac
test ! -e "$RESULT_DIR"
mkdir -p "$(dirname -- "$RESULT_DIR")"
mkdir "$RESULT_DIR"

cp "$ROOT/validation/iterative/d4a_three_snapshots.x2m" "$RESULT_DIR/"
cp "$ROOT/data/SpotD4Snap.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat" \
  "$RESULT_DIR/geometry.dat"
cp "$ROOT/validation/iterative/d4a_snapshot_inputs.sha256" \
  "$RESULT_DIR/frozen_repository_inputs.sha256"
ln -s "$DLIB370" "$RESULT_DIR/DLIB8R1_370"

(
  cd "$RESULT_DIR"
  printf '%s\n' \
    'STATES_C=650,620,475;750,620,475;850,620,475' \
    'NSNAP=3' \
    'TONE_TRACK_TISO=50.0' \
    'TONE_MXIT=20' \
    'TONE_EPS=1.0E-5' \
    'MCCG_EPSI=2.0E-6' \
    'FLU_SOLVER_EPS=2.0E-6' \
    'OMP_NUM_THREADS=1' \
    "WALL_LIMIT_SECONDS=$TIMEOUT_SECONDS" \
    'RETRY=0' > run_contract.txt
  sha256sum d4a_three_snapshots.x2m SpotD4Snap.c2m rnr_cc.c2m \
    rnr_interpol.c2m geometry.dat DLIB8R1_370 run_contract.txt \
    frozen_repository_inputs.sha256 \
    "$ROOT/validation/iterative/run_d4a_three_snapshots.sh" \
    "$ROOT/validation/iterative/run_bounded_dragon.py" \
    > executed_inputs.sha256
  sha256sum "$DRAGON_BIN" > dragon_executable.sha256
)

OMP_NUM_THREADS=1
export OMP_NUM_THREADS
echo "D4A THREE-SNAPSHOT PHYSICAL BUILD START: ${TIMEOUT_SECONDS}s bound, no retry"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  python3 -c \
  'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
  "$DRAGON_BIN" "$RESULT_DIR/d4a_three_snapshots.x2m" \
  "$RESULT_DIR/d4a_three_snapshots.log" "$TIMEOUT_SECONDS" \
  > "$RESULT_DIR/runner.out" 2> "$RESULT_DIR/runner.err"
echo "D4A THREE-SNAPSHOT PHYSICAL BUILD END"

test ! -s "$RESULT_DIR/runner.out"
test ! -s "$RESULT_DIR/runner.err"
test -f "$RESULT_DIR/d4a_snapshots.xsm"
test ! -L "$RESULT_DIR/d4a_snapshots.xsm"
test -s "$RESULT_DIR/d4a_snapshots.xsm"
LOG="$RESULT_DIR/d4a_three_snapshots.log"
expect_count 'MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED' 0 "$LOG"
expect_count 'CONVERGENCE REACHED AT TONE ITERATION' 3 "$LOG"
expect_count '^>\|D4A-SNAPSHOT-COMPLETE' 3 "$LOG"
expect_count '^>\|D4A-THREE-SNAPSHOT-ARCHIVE-COMPLETE' 1 "$LOG"
expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 3 "$LOG"
expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 3 "$LOG"
expect_count '^ FLU2DR-TERM INNER-TERMINAL .* STATE=1 NGRP= *370$' 3 "$LOG"
expect_count 'normal end of execution for dragon' 1 "$LOG"
if rg -i \
  'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$LOG" >/dev/null
then
  fail "Dragon log contains an abnormal terminal"
fi

tone_metrics=$(PYTHONDONTWRITEBYTECODE=1 python3 -c '
import re
import sys
text = open(sys.argv[1], errors="replace").read()
matches = re.findall(
    r"CONVERGENCE REACHED AT TONE ITERATION\s*=\s*(\d+)\s+ERROR\s*=\s*([-+0-9.Ee]+)",
    text,
)
if len(matches) != 3:
    raise SystemExit("expected three parseable TONE terminals")
values = [(int(i), float(e)) for i, e in matches]
if any(not (1 <= i <= 20 and 0.0 <= e <= 1.0e-5) for i, e in values):
    raise SystemExit(f"inadmissible TONE terminals: {values}")
print(" ".join(f"state{n}=iteration{i},error={e:.17g}" for n, (i, e) in enumerate(values, 1)))
' "$LOG") || fail "TONE terminal metrics were not admitted"
(
  cd "$RESULT_DIR"
  sha256sum -c executed_inputs.sha256 >/dev/null
  sha256sum -c dragon_executable.sha256 >/dev/null
  sha256sum d4a_snapshots.xsm > d4a_snapshots.sha256
  sha256sum d4a_snapshots.xsm d4a_three_snapshots.log \
    runner.out runner.err run_contract.txt executed_inputs.sha256 \
    dragon_executable.sha256 frozen_repository_inputs.sha256 \
    > snapshot_build_result.sha256
)
echo "D4A THREE-SNAPSHOT TONE PASS: $tone_metrics"
echo "D4A THREE-SNAPSHOT ARCHIVE BUILT: $RESULT_DIR/d4a_snapshots.xsm"
