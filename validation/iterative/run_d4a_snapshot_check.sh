#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RESULT_DIR=${RESULT_DIR:-}
CHECKER_SOURCE="$ROOT/validation/iterative/check_d4a_snapshot_archive.f90"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64"
FC=${FC:-gfortran}

fail() {
  echo "D4A SNAPSHOT CHECK FAIL: $*" >&2
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

test -n "$RESULT_DIR" || fail "set RESULT_DIR to the completed snapshot run"
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path" ;;
esac
test -d "$RESULT_DIR" || fail "RESULT_DIR does not exist"
test -f "$RESULT_DIR/d4a_snapshots.xsm" || fail "snapshot archive is missing"
test ! -L "$RESULT_DIR/d4a_snapshots.xsm" || fail "snapshot archive is a symlink"
test -s "$RESULT_DIR/d4a_snapshots.sha256" || fail "archive hash is missing"
test ! -L "$RESULT_DIR/d4a_snapshots.sha256" || fail "archive hash is a symlink"
test -f "$RESULT_DIR/d4a_three_snapshots.log" || fail "Dragon log is missing"
test ! -L "$RESULT_DIR/d4a_three_snapshots.log" || fail "Dragon log is a symlink"
test -s "$RESULT_DIR/d4a_three_snapshots.log" || fail "Dragon log is empty"
test -f "$RESULT_DIR/d4a_three_snapshots.err" || fail "Dragon stderr is missing"
test ! -L "$RESULT_DIR/d4a_three_snapshots.err" || fail "Dragon stderr is a symlink"
test ! -s "$RESULT_DIR/d4a_three_snapshots.err" || fail "Dragon stderr is not empty"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-d4a-snapshot-check.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

(
  cd "$RESULT_DIR"
  sha256sum -c executed_inputs.sha256 >/dev/null
  sha256sum -c dragon_executable.sha256 >/dev/null
  sha256sum -c d4a_snapshots.sha256 >/dev/null
)

LOG="$RESULT_DIR/d4a_three_snapshots.log"
if rg -i \
  'FLU2DR-DIAG|CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error|MAXIMUM NUMBER OF SELF-SHIELDING' \
  "$LOG" >/dev/null
then
  fail "Dragon log contains an abnormal terminal"
fi

expect_count '^>\|D4A-SNAPSHOT-STATE' 3 "$LOG"
expect_count '^>\|D4A-SNAPSHOT-COMPLETE' 3 "$LOG"
expect_count '^>\|D4A-THREE-SNAPSHOT-ARCHIVE-COMPLETE' 1 "$LOG"
expect_count 'CONVERGENCE REACHED AT TONE ITERATION' 3 "$LOG"
expect_count '^ FLU2DR-TERM OUTER-GATE=PASS ' 3 "$LOG"
expect_count '^ FLU2DR-TERM INNER-TERMINAL ' 3 "$LOG"
expect_count '^ FLU2DR-TERM INNER-TERMINAL .* STATE=1 NGRP= *370$' 3 "$LOG"
expect_count 'normal end of execution for dragon' 1 "$LOG"

"$FC" -std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror \
  -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$GANLIB/modules" "$CHECKER_SOURCE" "$GANLIB/libGanlib.a" \
  -lstdc++ -o "$WORK/check_d4a_snapshot_archive"

(
  cd "$RESULT_DIR"
  "$WORK/check_d4a_snapshot_archive" d4a_snapshots.xsm \
    > snapshot_check.log 2> snapshot_check.err
  test ! -s snapshot_check.err
  sha256sum -c d4a_snapshots.sha256 >/dev/null
)
expect_count '^D4A-SNAPSHOT K-EFFECTIVE ' 1 \
  "$RESULT_DIR/snapshot_check.log"
expect_count '^D4A-SNAPSHOT ACTIVE-FLUX MIN/MAX ' 1 \
  "$RESULT_DIR/snapshot_check.log"
expect_count '^D4A-SNAPSHOT TUPLE NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144$' 1 \
  "$RESULT_DIR/snapshot_check.log"
expect_count '^D4A-SNAPSHOT ARCHIVE GANLIB-ONLY PASS$' 1 \
  "$RESULT_DIR/snapshot_check.log"
if rg -F 'D4A-SNAPSHOT ARCHIVE FAIL:' "$RESULT_DIR/snapshot_check.log" >/dev/null
then
  fail "independent checker reported failure"
fi

(
  cd "$RESULT_DIR"
  sha256sum "$CHECKER_SOURCE" > snapshot_checker_source.sha256
  sha256sum d4a_snapshots.xsm snapshot_check.log \
    snapshot_check.err > admitted_snapshot_archive.sha256
)

echo "D4A PHYSICAL SNAPSHOT ARCHIVE ADMITTED: $RESULT_DIR/d4a_snapshots.xsm"
