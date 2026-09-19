#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
GANLIB="$ROOT/Ganlib/lib/$ARCH"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-b1hom64.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -Wno-unused-dummy-argument -fcheck=all -ffp-contract=off -fno-fast-math'

if [ ! -f "$GANLIB/modules/ganlib.mod" ]; then
  printf '%s\n' "B1HOM64 FAIL: build Ganlib first for $ARCH" >&2
  exit 1
fi

"$FC" $FFLAGS -I "$GANLIB/modules" \
  "$ROOT/src/B1HOM64.f90" \
  "$ROOT/validation/iterative/test_b1hom64.f90" \
  -o "$BUILD_DIR/test_b1hom64"

"$BUILD_DIR/test_b1hom64"
