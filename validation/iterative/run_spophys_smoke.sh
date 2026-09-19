#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
GANLIB="$ROOT/Ganlib/lib/$ARCH"
UTILIB="$ROOT/Utilib/lib/$ARCH"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-spophys.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math'
FFLAGS77='-O0 -g -Wall -Wextra -Werror -fcheck=all -ffp-contract=off -fno-fast-math -frecord-marker=4'

if [ ! -f "$GANLIB/libGanlib.a" ] || \
   [ ! -f "$GANLIB/modules/ganlib.mod" ] || \
   [ ! -f "$UTILIB/libUtilib.a" ]; then
  printf '%s\n' "SPOPHYS SMOKE FAIL: build Ganlib and Utilib first for $ARCH" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_spophys_contract.py"

"$FC" $FFLAGS -I "$GANLIB/modules" -J "$BUILD_DIR" \
  -c "$ROOT/src/SPOPHYS.f90" -o "$BUILD_DIR/SPOPHYS.o"
"$FC" $FFLAGS -I "$GANLIB/modules" -J "$BUILD_DIR" \
  -c "$ROOT/src/SPOT_LEAKAGE.f90" -o "$BUILD_DIR/SPOT_LEAKAGE.o"
"$FC" $FFLAGS -I "$GANLIB/modules" -J "$BUILD_DIR" \
  -c "$ROOT/src/SPOPOD.f90" -o "$BUILD_DIR/SPOPOD.o"
"$FC" $FFLAGS77 -I "$GANLIB/modules" -I "$BUILD_DIR" \
  -c "$ROOT/src/SPOASM.f" -o "$BUILD_DIR/SPOASM.o"
"$FC" $FFLAGS -I "$GANLIB/modules" -I "$BUILD_DIR" -J "$BUILD_DIR" \
  "$ROOT/validation/iterative/test_spophys.f90" \
  "$BUILD_DIR/SPOPHYS.o" "$BUILD_DIR/SPOASM.o" \
  "$BUILD_DIR/SPOT_LEAKAGE.o" "$BUILD_DIR/SPOPOD.o" \
  "$UTILIB/libUtilib.a" "$GANLIB/libGanlib.a" -lstdc++ \
  -o "$BUILD_DIR/test_spophys"

if ! (cd "$BUILD_DIR" && ./test_spophys > test_spophys.log 2>&1); then
  cat "$BUILD_DIR/test_spophys.log" >&2
  exit 1
fi
cat "$BUILD_DIR/test_spophys.log"
rg -F -x \
  'SPOPHYS SPOASM ROUND-TRIP PASS: full rank 3 exceeds 2 snapshots.' \
  "$BUILD_DIR/test_spophys.log" >/dev/null
rg -F -x \
  'SPOPHYS BEHAVIOR PASS: full physical fixed basis and metadata.' \
  "$BUILD_DIR/test_spophys.log" >/dev/null
