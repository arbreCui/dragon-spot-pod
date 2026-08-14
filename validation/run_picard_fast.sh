#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-picard-fast.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

CC=${CC:-cc}
FC=${FC:-gfortran}

PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/validation/check_method_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_spot_strict_inner.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_picard_control.py"
sh -n "$ROOT/validation/iterative/run_one_map_short.sh"
sh -n "$ROOT/validation/iterative/run_map2_short.sh"
sh -n "$ROOT/validation/iterative/run_map3_short.sh"
sh -n "$ROOT/validation/iterative/run_picard_direction_check.sh"
sh -n "$ROOT/validation/iterative/run_strict_leakage_faces.sh"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  python3 "$ROOT/validation/iterative/test_bounded_dragon.py"

"$CC" -std=c11 -pedantic -Wall -Wextra -Werror \
  -I "$ROOT/Ganlib/src" -c "$ROOT/validation/compile_c2m.c" \
  -o "$BUILD_DIR/compile_c2m.o"
"$FC" "$BUILD_DIR/compile_c2m.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  -o "$BUILD_DIR/compile_c2m"
for source in \
  "$ROOT/data/SpotPicard.c2m" \
  "$ROOT/validation/iterative/one_map_radial.x2m" \
  "$ROOT/validation/iterative/one_map_axial.x2m" \
  "$ROOT/validation/iterative/map2_radial.x2m" \
  "$ROOT/validation/iterative/map2_axial.x2m" \
  "$ROOT/validation/iterative/map3_radial.x2m" \
  "$ROOT/validation/iterative/map3_axial.x2m" \
  "$ROOT/validation/iterative/map4_radial.x2m" \
  "$ROOT/validation/iterative/map4_axial.x2m"
do
  stem=$(basename "$source")
  stem=${stem%.*}
  (
    cd "$BUILD_DIR"
    ./compile_c2m "$source" "$stem.o2m" >"$stem.compile.log" 2>&1
  )
  test -s "$BUILD_DIR/$stem.o2m"
done

"$FC" -O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror \
  -Wno-compare-reals -ffp-contract=off -fno-fast-math \
  -I "$ROOT/Ganlib/src" \
  "$ROOT/validation/iterative/check_one_map_xsm.f90" \
  "$ROOT/Ganlib/src/libGanlib.a" -lstdc++ \
  -o "$BUILD_DIR/check_one_map_xsm"

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
