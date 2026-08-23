#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
DRAGON="$ROOT/lib/$ARCH"
GANLIB="$ROOT/Ganlib/lib/$ARCH"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/spot-b2h-dims.XXXXXX")
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math'

gfortran $FFLAGS -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_SCHEMA.f90" -o "$TMP/SPOR64_SCHEMA.o"
gfortran $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_VERIFY.f90" -o "$TMP/SPOR64_VERIFY.o"
gfortran $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_B2H.f90" -o "$TMP/SPOR64_B2H.o"
gfortran $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_B2I.f90" -o "$TMP/SPOR64_B2I.o"
gfortran $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  -J "$TMP" -c "$ROOT/src/SPOR64_B2J.f90" -o "$TMP/SPOR64_B2J.o"
gfortran $FFLAGS -I "$TMP" -I "$DRAGON/modules" -I "$GANLIB/modules" \
  "$ROOT/validation/iterative/test_b2h_runtime_geometry.f90" \
  "$TMP/SPOR64_B2H.o" "$TMP/SPOR64_VERIFY.o" \
  "$DRAGON/libDragon.a" "$GANLIB/libGanlib.a" -lstdc++ \
  -o "$TMP/test_b2h_runtime_geometry"
"$TMP/test_b2h_runtime_geometry"
