#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-picard-fast.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

CC=${CC:-cc}
FC=${FC:-gfortran}

PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/validation/check_method_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_picard_control.py"

"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$ROOT/validation/compile_c2m.c" \
  -o "$BUILD_DIR/compile_c2m.o"
"$FC" "$BUILD_DIR/compile_c2m.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  -o "$BUILD_DIR/compile_c2m"
(
  cd "$BUILD_DIR"
  ./compile_c2m "$ROOT/data/SpotPicard.c2m" SpotPicard.o2m \
    >SpotPicard.compile.log 2>&1
)
test -s "$BUILD_DIR/SpotPicard.o2m"

"$FC" -O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror \
  -fimplicit-none -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$ROOT/Ganlib/lib/Darwin_arm64/modules" -J "$BUILD_DIR" \
  -c "$ROOT/src/SPOMOC.f90" -o "$BUILD_DIR/SPOMOC.o"
"$FC" -O0 -g -std=legacy -Wall -Wextra -Werror -Wno-compare-reals \
  -ffixed-line-length-none -ffp-contract=off -fno-fast-math \
  -I "$ROOT/Ganlib/lib/Darwin_arm64/modules" -I "$BUILD_DIR" \
  -J "$BUILD_DIR" -c "$ROOT/src/FLU2DR.f" \
  -o "$BUILD_DIR/FLU2DR.o"

printf '%s\n' "SPOT PICARD FAST PASS"
