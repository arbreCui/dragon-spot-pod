#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARTIFACTS=${ARTIFACTS:-"$ROOT/validation/artifacts"}
LOCK=${LOCK:-"$ROOT/validation/iterative/anderson1_trial_scientific.sha256"}
GANLIB_LIB=${GANLIB_LIB:-"$ROOT/Ganlib/src/libGanlib.a"}
GANLIB_MOD=${GANLIB_MOD:-"$ROOT/Ganlib/src"}
FC=${FC:-gfortran}

test -f "$LOCK"
test -f "$GANLIB_LIB"
test -f "$GANLIB_MOD/ganlib.mod"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-anderson1-trial.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

verify_locked() {
  relative=$1
  expected=$(awk -v file="$relative" '$2 == file { print $1 }' "$LOCK")
  actual=$(shasum -a 256 "$ARTIFACTS/$relative" | awk '{ print $1 }')
  test -n "$expected"
  test "$actual" = "$expected"
}

verify_locked iterative-map4-axial-80s/state4_axial.xsm
verify_locked iterative-map5-axial-80s/state5_axial.xsm
verify_locked iterative-map6-axial-80s/state6_axial.xsm
verify_locked iterative-map6-axial-80s/state6_snapshots.xsm

cp "$ARTIFACTS/iterative-map4-axial-80s/state4_axial.xsm" "$WORK/x4.xsm"
cp "$ARTIFACTS/iterative-map5-axial-80s/state5_axial.xsm" "$WORK/x5.xsm"
cp "$ARTIFACTS/iterative-map6-axial-80s/state6_axial.xsm" "$WORK/x6.xsm"
cp "$ARTIFACTS/iterative-map6-axial-80s/state6_snapshots.xsm" \
  "$WORK/snap6.xsm"

"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -fcheck=all -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/prepare_anderson1_trial.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/prepare_anderson1_trial"
"$FC" -std=f2008 -O0 -Wall -Wextra -Werror -Wno-compare-reals \
  -ffp-contract=off -fno-fast-math -fcheck=all -I "$GANLIB_MOD" \
  "$ROOT/validation/iterative/check_anderson1_trial_xsm.f90" \
  "$GANLIB_LIB" -lstdc++ -o "$WORK/check_anderson1_trial_xsm"

BUILD_RESULT=$(
  cd "$WORK"
  ./prepare_anderson1_trial \
    x4.xsm x5.xsm x6.xsm snap6.xsm trial_ax.xsm trial_snap.xsm
)
printf '%s\n' "$BUILD_RESULT"
printf '%s\n' "$BUILD_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL AX=TRIAL CARRIER=X6-RAW-FLUX'
printf '%s\n' "$BUILD_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL SNAPSHOT-L PUBLISHED'
printf '%s\n' "$BUILD_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL NO-DRAGON NO-MAP'

CHECK_RESULT=$(
  cd "$WORK"
  ./check_anderson1_trial_xsm \
    x4.xsm x5.xsm x6.xsm snap6.xsm trial_ax.xsm trial_snap.xsm
)
printf '%s\n' "$CHECK_RESULT"
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL FIXED-BUNDLE BITWISE PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL A/RHO/L PUBLICATION BITWISE PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL X6 RAW-FLUX CARRIER BITWISE PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL LAGGED SYSTEM LEAKAGE RECORDS PRESERVED PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL STALE-DIAGNOSTICS ABSENT PASS'
printf '%s\n' "$CHECK_RESULT" | grep -Fqx \
  'ANDERSON1-TRIAL COMPLETE NO-DRAGON NO-MAP'

verify_locked iterative-map4-axial-80s/state4_axial.xsm
verify_locked iterative-map5-axial-80s/state5_axial.xsm
verify_locked iterative-map6-axial-80s/state6_axial.xsm
verify_locked iterative-map6-axial-80s/state6_snapshots.xsm

rm -f "$WORK/trial_ax.xsm" "$WORK/trial_snap.xsm"
test ! -e "$WORK/trial_ax.xsm"
test ! -e "$WORK/trial_snap.xsm"

printf '%s\n' \
  'ANDERSON1-TRIAL INPUT-HASH PASS' \
  'ANDERSON1-TRIAL TEMPORARY-OUTPUT CLEANUP PASS' \
  'ANDERSON1-TRIAL NO-DRAGON PASS'
