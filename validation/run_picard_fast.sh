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
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_nonlinear_solver_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_continuation_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_rank2_map_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_rank2_axial_only_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_rank2_next_map_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_rank2_modal_aa1_candidate_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_rank2_modal_aa1_map_contract.py"
sh -n "$ROOT/validation/iterative/run_continuation_short.sh"
sh -n "$ROOT/validation/iterative/run_rank2_map.sh"
sh -n "$ROOT/validation/iterative/run_rank2_axial_only.sh"
sh -n "$ROOT/validation/iterative/run_rank2_next_map.sh"
sh -n "$ROOT/validation/iterative/run_rank2_modal_aa1_candidate.sh"
sh -n "$ROOT/validation/iterative/run_rank2_modal_aa1_next_candidate.sh"
sh -n "$ROOT/validation/iterative/run_rank2_modal_aa1_map.sh"
sh -n "$ROOT/validation/iterative/run_rank2_modal_aa1_next_map.sh"
sh -n "$ROOT/validation/iterative/run_residual_direction_audit.sh"
sh -n "$ROOT/validation/iterative/run_rank_census.sh"
continuation_default=$(RUN_CONTINUATION=0 \
  DRAGON_BIN="$BUILD_DIR/must-not-run" \
  PARENT_MANIFEST="$BUILD_DIR/must-not-read-parent" \
  RESULT_DIR="$BUILD_DIR/must-not-create-result" \
  GANLIB_LIB="$BUILD_DIR/must-not-read-ganlib" \
  GANLIB_MOD="$BUILD_DIR/must-not-read-modules" \
  TMPDIR="$BUILD_DIR/must-not-use-tmp" \
  sh "$ROOT/validation/iterative/run_continuation_short.sh")
test "$continuation_default" = \
  'SPOT-CONTINUATION DEFAULT-OFF: no Dragon process started.'
rank2_default=$(RUN_RANK2_MAP=0 \
  DRAGON_BIN="$BUILD_DIR/must-not-run" \
  RESULT_DIR="$BUILD_DIR/must-not-create-result" \
  TMPDIR="$BUILD_DIR/must-not-use-tmp" \
  sh "$ROOT/validation/iterative/run_rank2_map.sh")
test "$rank2_default" = \
  'SPOT-RANK2-MAP DEFAULT-OFF: no Dragon process started.'
rank2_axial_default=$(RUN_RANK2_AXIAL_ONLY=0 \
  DRAGON_BIN="$BUILD_DIR/must-not-run" \
  RESULT_DIR="$BUILD_DIR/must-not-create-result" \
  sh "$ROOT/validation/iterative/run_rank2_axial_only.sh")
test "$rank2_axial_default" = \
  'SPOT-RANK2-AXIAL-ONLY DEFAULT-OFF: no Dragon process started.'
rank2_next_default=$(RUN_RANK2_NEXT_MAP=0 \
  DRAGON_BIN="$BUILD_DIR/must-not-run" \
  RESULT_DIR="$BUILD_DIR/must-not-create-result" \
  sh "$ROOT/validation/iterative/run_rank2_next_map.sh")
test "$rank2_next_default" = \
  'SPOT-RANK2-NEXT-MAP DEFAULT-OFF: no Dragon process started.'
rank2_aa1_map_default=$(RUN_RANK2_MODAL_AA1_MAP=0 \
  DRAGON_BIN="$BUILD_DIR/must-not-run" \
  RESULT_DIR="$BUILD_DIR/must-not-create-result" \
  TMPDIR="$BUILD_DIR/must-not-use-tmp" \
  sh "$ROOT/validation/iterative/run_rank2_modal_aa1_map.sh")
test "$rank2_aa1_map_default" = \
  'SPOT-RANK2-MODAL-AA1-MAP DEFAULT-OFF: no Dragon process started.'
rank2_aa1_next_map_default=$(RUN_RANK2_MODAL_AA1_NEXT_MAP=0 \
  DRAGON_BIN="$BUILD_DIR/must-not-run" \
  RESULT_DIR="$BUILD_DIR/must-not-create-result" \
  TMPDIR="$BUILD_DIR/must-not-use-tmp" \
  sh "$ROOT/validation/iterative/run_rank2_modal_aa1_next_map.sh")
test "$rank2_aa1_next_map_default" = \
  'SPOT-RANK2-MODAL-AA1-NEXT-MAP DEFAULT-OFF: no Dragon process started.'
if continuation_invalid=$(RUN_CONTINUATION=2 \
    DRAGON_BIN="$BUILD_DIR/must-not-run" \
    sh "$ROOT/validation/iterative/run_continuation_short.sh" 2>&1)
then
  printf '%s\n' \
    'SPOT-CONTINUATION invalid activation unexpectedly passed.' >&2
  exit 1
fi
test "$continuation_invalid" = \
  'SPOT-CONTINUATION ERROR: RUN_CONTINUATION must be 0 or 1.'
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
  "$ROOT/validation/iterative/continuation_radial.x2m" \
  "$ROOT/validation/iterative/continuation_axial.x2m" \
  "$ROOT/validation/iterative/continuation_rank2_radial.x2m" \
  "$ROOT/validation/iterative/continuation_rank2_axial.x2m" \
  "$ROOT/validation/iterative/continuation_rank2_continued_radial.x2m"
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
  -ffp-contract=off -fno-fast-math \
  -I "$ROOT/Ganlib/src" \
  "$ROOT/validation/iterative/check_rank_census_xsm.f90" \
  "$ROOT/Ganlib/src/libGanlib.a" -lstdc++ \
  -o "$BUILD_DIR/check_rank_census_xsm"
"$FC" -O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror \
  -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$ROOT/Ganlib/src" \
  "$ROOT/validation/iterative/build_rank2_modal_aa1_candidate.f90" \
  "$ROOT/Ganlib/src/libGanlib.a" -lstdc++ \
  -o "$BUILD_DIR/build_rank2_modal_aa1_candidate"
"$FC" -O0 -g -std=f2008 -pedantic -Wall -Wextra -Werror \
  -Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math \
  -I "$ROOT/Ganlib/src" \
  "$ROOT/validation/iterative/check_rank2_modal_aa1_candidate.f90" \
  "$ROOT/Ganlib/src/libGanlib.a" -lstdc++ \
  -o "$BUILD_DIR/check_rank2_modal_aa1_candidate"
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
