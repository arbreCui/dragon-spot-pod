#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a3"
A2="$ROOT/validation/iterative/real64_phase_a2"
RECEIPT="$HERE/phase_a3_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a3.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
CHECKED_FLAGS="-O0 -g -std=f2008 -Wall -Wextra -Werror"
CHECKED_FLAGS="$CHECKED_FLAGS -Wimplicit-interface -Wimplicit-procedure"
CHECKED_FLAGS="$CHECKED_FLAGS -Wconversion-extra -Warray-temporaries"
CHECKED_FLAGS="$CHECKED_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
CHECKED_FLAGS="$CHECKED_FLAGS -ffp-contract=off -fno-fast-math"
LEGACY_FLAGS="-O0 -std=legacy -ffixed-line-length-none"
GANLIB_MODULES="$ROOT/Ganlib/lib/Darwin_arm64/modules"

compile_checked()
{
  "$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"
}

compile_legacy()
{
  "$FC" $LEGACY_FLAGS -I"$GANLIB_MODULES" -c "$1" -o "$2"
}

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A3 RECEIPT PASS"

sh "$A2/run_phase_a2.sh"
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a3.py"

compile_checked "$HERE/SPOR64_A3.f90" "$BUILD_DIR/SPOR64_A3.o"
compile_checked "$HERE/compile_spor64_a3_anchor.f90" \
  "$BUILD_DIR/compile_spor64_a3_anchor.o"

if compile_checked "$HERE/compile_fail_real32_mutable.f90" \
  "$BUILD_DIR/compile_fail_real32_mutable.o" \
  >"$BUILD_DIR/compile_fail_real32_mutable.log" 2>&1
then
  echo "SPOR64 PHASE-A3 FAILURE: REAL32 mutable state compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*REAL\\(4\\).*REAL\\(8\\)" \
  "$BUILD_DIR/compile_fail_real32_mutable.log"
then
  echo "SPOR64 PHASE-A3 FAILURE: mutable kind mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_integer_kpsys.f90" \
  "$BUILD_DIR/compile_fail_integer_kpsys.o" \
  >"$BUILD_DIR/compile_fail_integer_kpsys.log" 2>&1
then
  echo "SPOR64 PHASE-A3 FAILURE: INTEGER KPSYS compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*INTEGER\\(4\\).*TYPE\\(c_ptr\\)" \
  "$BUILD_DIR/compile_fail_integer_kpsys.log"
then
  echo "SPOR64 PHASE-A3 FAILURE: KPSYS mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_flat_pjjind.f90" \
  "$BUILD_DIR/compile_fail_flat_pjjind.o" \
  >"$BUILD_DIR/compile_fail_flat_pjjind.log" 2>&1
then
  echo "SPOR64 PHASE-A3 FAILURE: flat PJJIND compiled" >&2
  exit 1
fi
if ! rg -q "Rank mismatch.*pjjind.*rank-2.*rank-1" \
  "$BUILD_DIR/compile_fail_flat_pjjind.log"
then
  echo "SPOR64 PHASE-A3 FAILURE: PJJIND rank mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_real64_operator.f90" \
  "$BUILD_DIR/compile_fail_real64_operator.o" \
  >"$BUILD_DIR/compile_fail_real64_operator.log" 2>&1
then
  echo "SPOR64 PHASE-A3 FAILURE: altered REAL64 operator input compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*REAL\\(8\\).*REAL\\(4\\)" \
  "$BUILD_DIR/compile_fail_real64_operator.log"
then
  echo "SPOR64 PHASE-A3 FAILURE: operator kind mismatch not diagnosed" >&2
  exit 1
fi

if "$FC" -std=f2008 -fdefault-real-8 -c "$HERE/SPOR64_A3.f90" \
  -J"$BUILD_DIR" -I"$BUILD_DIR" -o "$BUILD_DIR/default_real8.o" \
  >"$BUILD_DIR/default_real8.log" 2>&1
then
  echo "SPOR64 PHASE-A3 FAILURE: global default REAL promotion compiled" >&2
  exit 1
fi
if ! rg -q "Division by zero" "$BUILD_DIR/default_real8.log"
then
  echo "SPOR64 PHASE-A3 FAILURE: kind guard did not diagnose promotion" >&2
  exit 1
fi

for source in MCGFCF MCGFFIR MCGFFAR MCGFFAL MCGSCA MCGFST
do
  compile_legacy "$ROOT/src/$source.f" "$BUILD_DIR/$source.o"
done

nm -u "$BUILD_DIR/SPOR64_A3.o" >"$BUILD_DIR/unresolved.log"
for symbol in mcgfcf mcgffir mcgffar mcgffal mcgsca mcgfst \
  spor64_a3_compile_only_link_forbidden
do
  if ! rg -qi "(^|[[:space:]])_?${symbol}_$" "$BUILD_DIR/unresolved.log"
  then
    echo "SPOR64 PHASE-A3 FAILURE: missing unresolved $symbol" >&2
    exit 1
  fi
done

unresolved_count=0
runtime_symbol_count=0
while IFS= read -r unresolved_line
do
  test -n "$unresolved_line" || continue
  unresolved_symbol=$(printf '%s\n' "$unresolved_line" | awk '{print $NF}')
  unresolved_count=$((unresolved_count + 1))
  case "$unresolved_symbol" in
    mcgfcf_|_mcgfcf_|mcgffir_|_mcgffir_|mcgffar_|_mcgffar_|\
mcgffal_|_mcgffal_|mcgsca_|_mcgsca_|mcgfst_|_mcgfst_|\
spor64_a3_compile_only_link_forbidden_|\
_spor64_a3_compile_only_link_forbidden_)
      ;;
    _gfortran_runtime_error_at|__gfortran_runtime_error_at|\
___gfortran_runtime_error_at)
      runtime_symbol_count=$((runtime_symbol_count + 1))
      ;;
    *)
      echo "SPOR64 PHASE-A3 FAILURE: unexpected unresolved symbol" \
        "$unresolved_symbol" >&2
      exit 1
      ;;
  esac
done <"$BUILD_DIR/unresolved.log"

if test "$unresolved_count" -ne 8 || test "$runtime_symbol_count" -ne 1
then
  echo "SPOR64 PHASE-A3 FAILURE: unresolved symbol set is not exact" >&2
  exit 1
fi

if nm "$BUILD_DIR/SPOR64_A3.o" "$BUILD_DIR/compile_spor64_a3_anchor.o" |
  rg -i "(^|[[:space:]])(_?main|MAIN__)(_|$)"
then
  echo "SPOR64 PHASE-A3 FAILURE: executable entry point present" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a3_contract

echo "SPOR64 PHASE-A3 COMPILE-ONLY ABI PASS"
echo "SPOR64 PHASE-A3 LINKS=0 EXECUTABLES=0 A3-EXECUTIONS=0"
echo "SPOR64 PHASE-A3 TRANSPORT-APPLICATIONS=0 DRAGON-RUNS=0"
