#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a1"
RECEIPT="$HERE/phase_a1_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a1.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
FLAGS="-O0 -g -std=f2008 -Wall -Wextra -Werror"
FLAGS="$FLAGS -Wimplicit-interface -Wimplicit-procedure -Wconversion-extra"
FLAGS="$FLAGS -fimplicit-none -fcheck=all -fbacktrace"
FLAGS="$FLAGS -ffpe-trap=invalid,zero,overflow"
FLAGS="$FLAGS -ffp-contract=off -fno-fast-math -ffpe-summary=none"

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A1 RECEIPT PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a1.py"

"$FC" $FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" \
  "$HERE/SPOR64_A1.f90" "$HERE/test_spor64_a1.f90" \
  -o "$BUILD_DIR/test_spor64_a1"

"$BUILD_DIR/test_spor64_a1"

if "$FC" $FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" \
  "$HERE/SPOR64_A1.f90" "$HERE/compile_fail_real32_actual.f90" \
  -o "$BUILD_DIR/compile_fail_real32_actual" \
  >"$BUILD_DIR/compile_fail.log" 2>&1
then
  echo "SPOR64 PHASE-A1 FAILURE: binary32 mutable actual compiled" >&2
  exit 1
fi

if ! rg -q "Type mismatch.*REAL\\(4\\).*REAL\\(8\\)" \
  "$BUILD_DIR/compile_fail.log"
then
  echo "SPOR64 PHASE-A1 FAILURE: expected kind mismatch was not diagnosed" >&2
  sed -n '1,120p' "$BUILD_DIR/compile_fail.log" >&2
  exit 1
fi

nm -u "$BUILD_DIR/test_spor64_a1" >"$BUILD_DIR/unresolved.log"
if rg -i "DOORFV|MCCGF|MCGFLX|MCGMRE|FLU2AC|FLU2DR" \
  "$BUILD_DIR/unresolved.log"
then
  echo "SPOR64 PHASE-A1 FAILURE: transport symbol linked" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a1_contract

echo "SPOR64 PHASE-A1 TESTS PASS: PARTIAL-SLICE-ONLY DRAGON-RUNS=0"
