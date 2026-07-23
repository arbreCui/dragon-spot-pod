#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-level2.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}

"$FC" \
  -O0 -g -std=gnu -Wall -Wextra -Wno-compare-reals \
  -fcheck=all -ffpe-trap=invalid,zero,overflow \
  -ffixed-line-length-none -ffree-line-length-none \
  "$ROOT/Utilib/src/ALSBD.f" \
  "$ROOT/src/SPOT1P.f90" \
  "$ROOT/validation/level2/test_spot1p.f90" \
  -o "$BUILD_DIR/test_spot1p"

"$BUILD_DIR/test_spot1p"

"$FC" \
  -O0 -g -std=gnu -Wall -Wextra -Wno-compare-reals \
  -fcheck=all -ffpe-trap=invalid,zero,overflow \
  -ffixed-line-length-none -ffree-line-length-none \
  "$ROOT/src/SPOT_LEAKAGE.f90" \
  "$ROOT/validation/level2/test_radial_closure.f90" \
  -o "$BUILD_DIR/test_radial_closure"

"$BUILD_DIR/test_radial_closure"

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/level2/check_final_source_audit.py"
