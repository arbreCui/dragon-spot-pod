#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
ARCH=$(uname -s)_$(uname -m)
GANLIB="$ROOT/Ganlib/lib/$ARCH"
UTILIB="$ROOT/Utilib/lib/$ARCH"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-full-rank-cycle.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
FFLAGS='-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror -Wno-compare-reals -Wno-unused-dummy-argument -fcheck=all -ffp-contract=off -fno-fast-math'

if [ ! -f "$GANLIB/libGanlib.a" ] || \
   [ ! -f "$GANLIB/modules/ganlib.mod" ] || \
   [ ! -f "$UTILIB/libUtilib.a" ]; then
  printf '%s\n' \
    "FULL-RANK PICARD CYCLE FAIL: build Ganlib and Utilib first for $ARCH" >&2
  exit 1
fi

compile_module() {
  source_file=$1
  object_name=$2
  "$FC" $FFLAGS -I "$GANLIB/modules" -I "$BUILD_DIR" \
    -J "$BUILD_DIR" -c "$ROOT/$source_file" -o "$BUILD_DIR/$object_name"
}

compile_module src/SPOT_LEAKAGE.f90 SPOT_LEAKAGE.o
compile_module src/SPOPHYS.f90 SPOPHYS.o
compile_module src/SPOSTATE.f90 SPOSTATE.o
compile_module src/SPOR64_SCHEMA.f90 SPOR64_SCHEMA.o
compile_module src/SPOR64_VERIFY.f90 SPOR64_VERIFY.o
compile_module src/SPOR64_RCONTRACT.f90 SPOR64_RCONTRACT.o
compile_module src/SPOR64_B2H.f90 SPOR64_B2H.o
compile_module src/SPOR64_B2I.f90 SPOR64_B2I.o
compile_module src/SPOR64_B2J.f90 SPOR64_B2J.o
compile_module src/SPOR64_B2W.f90 SPOR64_B2W.o

"$FC" $FFLAGS -I "$GANLIB/modules" -I "$BUILD_DIR" -J "$BUILD_DIR" \
  "$ROOT/validation/iterative/test_full_rank_picard_cycle.f90" \
  "$BUILD_DIR/SPOT_LEAKAGE.o" \
  "$BUILD_DIR/SPOPHYS.o" \
  "$BUILD_DIR/SPOSTATE.o" \
  "$BUILD_DIR/SPOR64_SCHEMA.o" \
  "$BUILD_DIR/SPOR64_VERIFY.o" \
  "$BUILD_DIR/SPOR64_RCONTRACT.o" \
  "$BUILD_DIR/SPOR64_B2H.o" \
  "$BUILD_DIR/SPOR64_B2I.o" \
  "$BUILD_DIR/SPOR64_B2J.o" \
  "$BUILD_DIR/SPOR64_B2W.o" \
  "$UTILIB/libUtilib.a" "$GANLIB/libGanlib.a" -lstdc++ \
  -o "$BUILD_DIR/test_full_rank_picard_cycle"

if ! (cd "$BUILD_DIR" && \
  ./test_full_rank_picard_cycle > test_full_rank_picard_cycle.log 2>&1); then
  cat "$BUILD_DIR/test_full_rank_picard_cycle.log" >&2
  exit 1
fi

cat "$BUILD_DIR/test_full_rank_picard_cycle.log"
rg -F -x \
  'B2I PROJECTION PASS: REAL64 AUTHORITY RETAINED; R32 1-ULP TAMPER REFUSED' \
  "$BUILD_DIR/test_full_rank_picard_cycle.log" >/dev/null
rg -F -x \
  'FULL-RANK REAL64 K CONTRACT PASS: B2J/B2W REJECT R64 DRIFT IN ONE R32 BIN' \
  "$BUILD_DIR/test_full_rank_picard_cycle.log" >/dev/null
rg -F -x \
  'ROUTE-CONTRACT NEGATIVE PASS: TAMPERED CONTRACT REFUSED' \
  "$BUILD_DIR/test_full_rank_picard_cycle.log" >/dev/null
rg -F -x \
  'FULL-RANK PICARD CYCLE PASS: NREG2D=4 NSNAP=3 RANK=4 EPOCH=0->1->2' \
  "$BUILD_DIR/test_full_rank_picard_cycle.log" >/dev/null
