#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
DRAGON="$ROOT/lib/$ARCH"
TRIVAC="$ROOT/Trivac/lib/$ARCH"
UTILIB="$ROOT/Utilib/lib/$ARCH"
GANLIB="$ROOT/Ganlib/lib/$ARCH"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/spot-a89-dims.XXXXXX")
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

FC=${FC:-gfortran}
FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math'

"$FC" $FFLAGS -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_A8.f90" -o "$TMP/SPOR64_A8.o"
"$FC" $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_A9.f90" -o "$TMP/SPOR64_A9.o"
"$FC" $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  "$ROOT/validation/iterative/test_a89_runtime_geometry.f90" \
  "$TMP/SPOR64_A9.o" "$TMP/SPOR64_A8.o" \
  "$DRAGON/libDragon.a" "$TRIVAC/libTrivac.a" \
  "$UTILIB/libUtilib.a" "$GANLIB/libGanlib.a" -lstdc++ \
  -o "$TMP/test_a89_runtime_geometry"

"$TMP/test_a89_runtime_geometry"
