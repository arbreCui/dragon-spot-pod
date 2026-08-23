#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
DRAGON="$ROOT/lib/$ARCH"
GANLIB="$ROOT/Ganlib/lib/$ARCH"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/spot-b2c-dims.XXXXXX")
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math'

gfortran $FFLAGS -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_B2C.f90" -o "$TMP/SPOR64_B2C.o"
gfortran $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  "$ROOT/validation/iterative/test_b2c_runtime_dimensions.f90" \
  "$TMP/SPOR64_B2C.o" "$DRAGON/libDragon.a" "$GANLIB/libGanlib.a" \
  -lstdc++ -o "$TMP/test_b2c_runtime_dimensions"
"$TMP/test_b2c_runtime_dimensions"
