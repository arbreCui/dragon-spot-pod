#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RESULT_DIR=${RESULT_DIR:-}
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
TIMEOUT_SECONDS=${TIMEOUT_SECONDS:-120}
DECK_SOURCE="$ROOT/validation/iterative/d4a_rank2_basis.x2m"
CHECKER_SOURCE="$ROOT/validation/iterative/check_d4a_rank2_basis.f90"
GANLIB="$ROOT/Ganlib/lib/Darwin_arm64"
FC=${FC:-gfortran}

fail() {
  echo "D4A RANK2 BUILD FAIL: $*" >&2
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

test -n "$RESULT_DIR" || fail "set RESULT_DIR to the admitted snapshot run"
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path" ;;
esac
test -d "$RESULT_DIR" || fail "RESULT_DIR does not exist"
test -x "$DRAGON_BIN" || fail "Dragon executable is missing"
test -s "$RESULT_DIR/d4a_snapshots.xsm" || fail "snapshot archive is missing"
test ! -L "$RESULT_DIR/d4a_snapshots.xsm" || fail "snapshot archive is a symlink"
test -s "$RESULT_DIR/admitted_snapshot_archive.sha256" ||
  fail "admitted snapshot receipt is missing"
test ! -L "$RESULT_DIR/admitted_snapshot_archive.sha256" ||
  fail "admitted snapshot receipt is a symlink"
test -s "$RESULT_DIR/snapshot_checker_source.sha256" ||
  fail "snapshot checker receipt is missing"
test ! -L "$RESULT_DIR/snapshot_checker_source.sha256" ||
  fail "snapshot checker receipt is a symlink"
test -f "$RESULT_DIR/snapshot_check.err" || fail "snapshot checker stderr is missing"
test ! -L "$RESULT_DIR/snapshot_check.err" ||
  fail "snapshot checker stderr is a symlink"
test ! -s "$RESULT_DIR/snapshot_check.err" ||
  fail "snapshot checker stderr is not empty"
expect_count '^D4A-SNAPSHOT ARCHIVE GANLIB-ONLY PASS$' 1 \
  "$RESULT_DIR/snapshot_check.log"
(
  cd "$RESULT_DIR"
  sha256sum -c d4a_snapshots.sha256 >/dev/null
  sha256sum -c admitted_snapshot_archive.sha256 >/dev/null
  sha256sum -c snapshot_checker_source.sha256 >/dev/null
)

for output in d4a_rank2_basis.xsm d4a_axial_track.xsm \
  d4a_axial_macrolib.xsm d4a_rank2_basis.log d4a_rank2_check.log \
  d4a_rank2_check.err d4a_rank2_sources.sha256 \
  d4a_rank2_admitted.sha256
do
  test ! -e "$RESULT_DIR/$output" || fail "refusing to overwrite $output"
done
test ! -e "$RESULT_DIR/d4a_rank2_basis.x2m" ||
  fail "refusing to overwrite staged rank2 deck"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-d4a-rank2-check.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

cp "$DECK_SOURCE" "$RESULT_DIR/d4a_rank2_basis.x2m"
(
  cd "$RESULT_DIR"
  sha256sum d4a_rank2_basis.x2m d4a_snapshots.xsm \
    "$CHECKER_SOURCE" "$DRAGON_BIN" > d4a_rank2_sources.sha256
)

"$FC" -std=f2008 -O2 -march=native -g -pedantic -Wall -Wextra -Werror \
  -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$GANLIB/modules" "$CHECKER_SOURCE" "$GANLIB/libGanlib.a" \
  -lstdc++ -o "$WORK/check_d4a_rank2_basis"
(
  cd "$RESULT_DIR"
  sha256sum -c d4a_rank2_sources.sha256 >/dev/null
)

OMP_NUM_THREADS=1
export OMP_NUM_THREADS
echo "D4A RANK2 STATIC BUILD START: ${TIMEOUT_SECONDS}s bound, no retry"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  python3 -c \
  'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
  "$DRAGON_BIN" "$RESULT_DIR/d4a_rank2_basis.x2m" \
  "$RESULT_DIR/d4a_rank2_basis.log" "$TIMEOUT_SECONDS"
echo "D4A RANK2 STATIC BUILD END"

LOG="$RESULT_DIR/d4a_rank2_basis.log"
if rg -i \
  'XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error|CONVERGENCE NOT REACHED' \
  "$LOG" >/dev/null
then
  fail "Dragon log contains an abnormal terminal"
fi
expect_count '^>\|D4A-RANK2-BASIS-COMPLETE' 1 "$LOG"
expect_count 'normal end of execution for dragon' 1 "$LOG"
expect_count 'FLU2DR' 0 "$LOG"

for output in d4a_rank2_basis.xsm d4a_axial_track.xsm \
  d4a_axial_macrolib.xsm
do
  test -s "$RESULT_DIR/$output" || fail "$output is missing or empty"
  test ! -L "$RESULT_DIR/$output" || fail "$output is a symlink"
done

(
  cd "$RESULT_DIR"
  "$WORK/check_d4a_rank2_basis" d4a_snapshots.xsm \
    d4a_axial_track.xsm d4a_rank2_basis.xsm \
    > d4a_rank2_check.log 2> d4a_rank2_check.err
  test ! -s d4a_rank2_check.err
  sha256sum -c d4a_snapshots.sha256 >/dev/null
  sha256sum -c admitted_snapshot_archive.sha256 >/dev/null
  sha256sum -c snapshot_checker_source.sha256 >/dev/null
  sha256sum -c d4a_rank2_sources.sha256 >/dev/null
)

expect_count '^D4A-RANK2 DIMENSIONS NGRP=370 NREG2D=132 NSNAP=3 NMODE=2$' 1 \
  "$RESULT_DIR/d4a_rank2_check.log"
expect_count '^D4A-RANK2 STORED-DIAGNOSTICS BITWISE PASS$' 1 \
  "$RESULT_DIR/d4a_rank2_check.log"
expect_count '^D4A-RANK2 CLASSIFICATION OFFLINE_AXIAL_GEOMETRY_AND_FIXED_BASIS_BUILT$' 1 \
  "$RESULT_DIR/d4a_rank2_check.log"
expect_count '^D4A-RANK2 GANLIB-ONLY PASS$' 1 \
  "$RESULT_DIR/d4a_rank2_check.log"

(
  cd "$RESULT_DIR"
  sha256sum d4a_snapshots.xsm d4a_rank2_basis.xsm \
    d4a_axial_track.xsm d4a_axial_macrolib.xsm \
    d4a_rank2_basis.log d4a_rank2_check.log d4a_rank2_check.err \
    d4a_rank2_sources.sha256 \
    > d4a_rank2_admitted.sha256
)

echo "D4A RANK2 FIXED BASIS ADMITTED: $RESULT_DIR/d4a_rank2_basis.xsm"
