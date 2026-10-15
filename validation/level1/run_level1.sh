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

"$FC" \
  -O0 -g -std=gnu -Wall -Wextra -Wno-compare-reals \
  -fcheck=all -ffpe-trap=invalid,zero,overflow \
  -ffixed-line-length-none -ffree-line-length-none \
  "$ROOT/Utilib/src/ALSVDF.f" \
  "$ROOT/src/SPOPOD.f90" \
  "$ROOT/validation/level1/test_spopod_invalid.f90" \
  -o "$BUILD_DIR/test_spopod_invalid"

for entry in legacy real64; do
  for case_name in nan_phi inf_phi nan_vol inf_vol zero_vol negative_vol \
                   zero_flux negative_rank dimensions snapshot_shape; do
    case "$case_name" in
      nan_phi|inf_phi) expected='NONFINITE SNAPSHOT FLUX.' ;;
      nan_vol|inf_vol) expected='NONFINITE RADIAL VOLUME.' ;;
      zero_vol|negative_vol) expected='NONPOSITIVE RADIAL VOLUME.' ;;
      zero_flux) expected='NONPOSITIVE SNAPSHOT FLUX.' ;;
      negative_rank) expected='NEGATIVE RANK REQUEST.' ;;
      dimensions) expected='INVALID SNAPSHOT DIMENSIONS.' ;;
      snapshot_shape) expected='NREG2D MUST BE GREATER THAN OR EQUAL TO NSNAP.' ;;
    esac
    if "$BUILD_DIR/test_spopod_invalid" "$case_name" "$entry" \
        >"$BUILD_DIR/invalid.log" 2>&1; then
      echo "FAIL: $entry accepted $case_name" >&2
      exit 1
    fi
    if ! grep -F "XABORT: SPOPOD: $expected" "$BUILD_DIR/invalid.log" >/dev/null; then
      cat "$BUILD_DIR/invalid.log" >&2
      echo "FAIL: $entry did not reject $case_name through its input contract" >&2
      exit 1
    fi
    echo "PASS: $entry rejects $case_name before SVD."
  done
done
