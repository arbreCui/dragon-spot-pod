#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a2"
A1="$ROOT/validation/iterative/real64_phase_a1"
RECEIPT="$HERE/phase_a2_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a2.XXXXXX")
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
echo "SPOR64 PHASE-A2 RECEIPT PASS"

sh "$A1/run_phase_a1.sh"
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a2.py"

"$FC" $FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" \
  "$A1/SPOR64_A1.f90" "$HERE/SPOR64_A2.f90" \
  "$HERE/test_spor64_a2.f90" -o "$BUILD_DIR/test_spor64_a2"

"$BUILD_DIR/test_spor64_a2"

if "$FC" $FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c \
  "$HERE/compile_fail_real32_actual.f90" \
  -o "$BUILD_DIR/compile_fail_real32_actual.o" \
  >"$BUILD_DIR/compile_fail_real32_actual.log" 2>&1
then
  echo "SPOR64 PHASE-A2 FAILURE: binary32 mutable actual compiled" >&2
  exit 1
fi

if ! rg -q "Type mismatch.*REAL\\(4\\).*REAL\\(8\\)" \
  "$BUILD_DIR/compile_fail_real32_actual.log"
then
  echo "SPOR64 PHASE-A2 FAILURE: mutable kind mismatch not diagnosed" >&2
  sed -n '1,160p' "$BUILD_DIR/compile_fail_real32_actual.log" >&2
  exit 1
fi

if "$FC" $FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c \
  "$HERE/compile_fail_real32_callback.f90" \
  -o "$BUILD_DIR/compile_fail_real32_callback.o" \
  >"$BUILD_DIR/compile_fail_real32_callback.log" 2>&1
then
  echo "SPOR64 PHASE-A2 FAILURE: binary32 callback compiled" >&2
  exit 1
fi

if ! rg -q "Interface mismatch.*primary_response|Type mismatch.*REAL\\(8\\).*REAL\\(4\\)" \
  "$BUILD_DIR/compile_fail_real32_callback.log"
then
  echo "SPOR64 PHASE-A2 FAILURE: callback kind mismatch not diagnosed" >&2
  sed -n '1,160p' "$BUILD_DIR/compile_fail_real32_callback.log" >&2
  exit 1
fi

nm -u "$BUILD_DIR/test_spor64_a2" >"$BUILD_DIR/unresolved.log"
if rg -i "DOORFV|MCCGF|MCGFLX|MCGMRE|MCGFL1|MCGFCS|MCGFCF|MCGFFIR|"\
"MCGSCA|MCGFST|MCGFCA|MCGFCR|MCGABG|MCGPRA|MSRLUS1|FLU2DR|FLUBAL|"\
"FLU2AC|LCMGET|LCMGPD|KDRCPU|XABORT" "$BUILD_DIR/unresolved.log"
then
  echo "SPOR64 PHASE-A2 FAILURE: transport symbol linked" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a2_contract

echo "SPOR64 PHASE-A2 TESTS PASS: PARTIAL-SLICE-ONLY"
echo "SPOR64 PHASE-A2 TRANSPORT-APPLICATIONS=0 DRAGON-RUNS=0"
