#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
FROZEN_FC=/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15
FROZEN_FC_SHA256=0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492
GANLIB_MOD="$ROOT/Ganlib/lib/Darwin_arm64/modules"
GANLIB_LIB="$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB_LIB="$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"
GANLIB_MOD_SHA256=9ad2be2ae13310aa8273409d5cb3e70dfaa2201ada7bfc29a135bd566c4651d0
GANLIB_LIB_SHA256=204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c
UTILIB_LIB_SHA256=a6c5cca8825691fd1da7554acabe542ba9986aabdbc935ecc46d1993240244ca
BUILDER="$ROOT/validation/iterative/build_gmres_activity_overlay.sh"
TEST_SOURCE="$ROOT/validation/iterative/test_gmres_activity_state.f90"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-gmres-activity-state.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

if test "${FC+x}" = x && test "$FC" != "$FROZEN_FC"
then
  echo "unfrozen FC override rejected" >&2
  exit 2
fi
FC=$FROZEN_FC
test "$(uname -sm)" = "Darwin arm64"

for path in "$FC" "$GANLIB_MOD/ganlib.mod" "$GANLIB_LIB" "$UTILIB_LIB" \
  "$BUILDER" "$TEST_SOURCE"
do
  test -f "$path" || {
    echo "missing state-test dependency: $path" >&2
    exit 2
  }
  test ! -L "$path" || {
    echo "symlink state-test dependency: $path" >&2
    exit 2
  }
done
test "$(shasum -a 256 "$FC" | awk '{print $1}')" = "$FROZEN_FC_SHA256"
test "$(shasum -a 256 "$GANLIB_MOD/ganlib.mod" | awk '{print $1}')" = \
  "$GANLIB_MOD_SHA256"
test "$(shasum -a 256 "$GANLIB_LIB" | awk '{print $1}')" = \
  "$GANLIB_LIB_SHA256"
test "$(shasum -a 256 "$UTILIB_LIB" | awk '{print $1}')" = \
  "$UTILIB_LIB_SHA256"
test "$("$FC" --version | head -1)" = \
  "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"

test -z "$(git -C "$ROOT" status --short -- src)"
git -C "$ROOT" diff --quiet \
  4d7abb23ac7975d4146beaa3b0049e36cdad8776 -- src

"$BUILDER" "$WORK/tree" >"$WORK/build.log"
grep -q '^PASS: GMRES activity overlay built at ' "$WORK/build.log"
MODULE="$WORK/tree/src/SPOMGMR.f90"
test -f "$MODULE"

COMMON_FLAGS="-O0 -Wall -Wextra -Werror -fcheck=all -fbacktrace
  -ffp-contract=off -fno-fast-math -ffpe-summary=none"
"$FC" $COMMON_FLAGS -std=f2008 -I "$GANLIB_MOD" -J "$WORK" \
  -c "$MODULE" -o "$WORK/SPOMGMR.o"
"$FC" $COMMON_FLAGS -std=f2008 -I "$GANLIB_MOD" -I "$WORK" -J "$WORK" \
  -c "$TEST_SOURCE" -o "$WORK/test_gmres_activity_state.o"
"$FC" "$WORK/test_gmres_activity_state.o" "$WORK/SPOMGMR.o" \
  "$GANLIB_LIB" "$UTILIB_LIB" -lstdc++ \
  -o "$WORK/test_gmres_activity_state"

if nm -u "$WORK/SPOMGMR.o" | grep -Ei \
  'DOORFV|MCCGF|MCGFLX|MCGMRE|MCGFL1|MCGFCS|MCGSIG|MCGFCF|MOCFCF|MCGFST|MCGFCA|MCGSCR|FLUBAL|FLU2AC'
then
  echo "activity helper references a solver routine" >&2
  exit 1
fi

for mode in off valid zero-block zero-k
do
  "$WORK/test_gmres_activity_state" "$mode" >"$WORK/${mode}_a.log"
  "$WORK/test_gmres_activity_state" "$mode" >"$WORK/${mode}_b.log"
  cmp "$WORK/${mode}_a.log" "$WORK/${mode}_b.log"
done
test "$(cat "$WORK/off_a.log")" = "GMRES-ACTIVITY STATE OFF PASS"
test "$(cat "$WORK/valid_a.log")" = "GMRES-ACTIVITY STATE VALID PASS"
test "$(cat "$WORK/zero-block_a.log")" = \
  "GMRES-ACTIVITY STATE ZERO-BLOCK PASS"
test "$(cat "$WORK/zero-k_a.log")" = \
  "GMRES-ACTIVITY STATE ZERO-K PASS"

FAIL_MODES='
duplicate
no-moca
preexisting-sink
partial-finish
second-entry
open-block-exit
mask-rise
kmax-mismatch
wrong-door
wrong-type
wrong-ngrp
wrong-nun
wrong-nreg
wrong-maxout
wrong-maxinr
wrong-epsout
wrong-epsunk
wrong-epsinr
wrong-forward
wrong-ileak
wrong-rebalance
wrong-init
wrong-acce-left
wrong-acce-right
wrong-track-kryl
wrong-track-idifc
wrong-track-iaac
wrong-track-iscr
wrong-track-paca
wrong-track-maxi
wrong-track-stis
wrong-track-direct
wrong-track-errtol
actual-maxi
actual-errtol
actual-nstart
actual-ngroup
actual-ngeff
actual-nun
actual-ndim
actual-nlong
actual-nreg
actual-nsout
actual-nani
actual-nlin
actual-nfunl
actual-iaac
actual-iscr
actual-paca
actual-stis
actual-idir
actual-cyclic
actual-reverse
actual-ngind
'

for mode in $FAIL_MODES
do
  if "$WORK/test_gmres_activity_state" "$mode" \
       >"$WORK/$mode.log" 2>&1
  then
    echo "fail-closed mode unexpectedly passed: $mode" >&2
    exit 1
  fi
  grep -q 'SPOMGMR:' "$WORK/$mode.log"
done

grep -q 'duplicate GMRA keyword' "$WORK/duplicate.log"
grep -q 'GMRA requires MOCA 2' "$WORK/no-moca.log"
grep -q 'audit directory already exists' "$WORK/preexisting-sink.log"
grep -q 'exactly one MCGMRE entry and exit required' \
  "$WORK/partial-finish.log"
grep -q 'second MCGMRE entry' "$WORK/second-entry.log"
grep -q 'MCGMRE exit with open block' "$WORK/open-block-exit.log"
grep -q 'Krylov active mask changed 0 to 1' "$WORK/mask-rise.log"
grep -q 'KMAX does not close Krylov masks' "$WORK/kmax-mismatch.log"

test -z "$(git -C "$ROOT" status --short -- src)"
git -C "$ROOT" diff --quiet \
  4d7abb23ac7975d4146beaa3b0049e36cdad8776 -- src

echo "GMRES-ACTIVITY STATE TEST PASS"
