#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-level1.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}

"$FC" \
  -O0 -g -std=gnu -Wall -Wextra -Wno-compare-reals \
  -fcheck=all -ffpe-trap=invalid,zero,overflow \
  -ffixed-line-length-none -ffree-line-length-none \
  "$ROOT/Utilib/src/ALSVDF.f" \
  "$ROOT/src/SPOPOD.f90" \
  "$ROOT/validation/level1/test_spopod.f90" \
  -o "$BUILD_DIR/test_spopod"

"$BUILD_DIR/test_spopod"
