#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a5"
A1="$ROOT/validation/iterative/real64_phase_a1"
A2="$ROOT/validation/iterative/real64_phase_a2"
A3="$ROOT/validation/iterative/real64_phase_a3"
A4="$ROOT/validation/iterative/real64_phase_a4"
A4_RECEIPT="$A4/phase_a4_implementation_receipt.sha256"
RECEIPT="$HERE/phase_a5_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a5.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
LC_ALL=C
export LC_ALL
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A5 FAILURE: unaudited compiler identity" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A5 FAILURE: unaudited platform identity" >&2
  exit 1
fi
BASE_FLAGS="-O0 -g -std=f2008 -pedantic-errors -Wall -Wextra -Werror"
BASE_FLAGS="$BASE_FLAGS -Wimplicit-interface -Wimplicit-procedure"
BASE_FLAGS="$BASE_FLAGS -Wconversion-extra -fimplicit-none"
BASE_FLAGS="$BASE_FLAGS -fcheck=all -fbacktrace"
BASE_FLAGS="$BASE_FLAGS -ffp-contract=off -fno-fast-math"
CHECKED_FLAGS="$BASE_FLAGS -Warray-temporaries"

compile_base()
{
  "$FC" $BASE_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"
}

compile_checked()
{
  "$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"
}

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A5 RECEIPT PASS"

(
  cd "$ROOT"
  shasum -a 256 -c "$A4_RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A5 FROZEN PHASE-A4 RECEIPT PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a5.py"

compile_base "$A1/SPOR64_A1.f90" "$BUILD_DIR/SPOR64_A1.o"
compile_base "$A2/SPOR64_A2.f90" "$BUILD_DIR/SPOR64_A2.o"
compile_checked "$A3/SPOR64_A3.f90" "$BUILD_DIR/SPOR64_A3.o"
compile_checked "$A4/SPOR64_A4.f90" "$BUILD_DIR/SPOR64_A4.o"
compile_checked "$HERE/SPOR64_A5.f90" "$BUILD_DIR/SPOR64_A5.o"
compile_checked "$HERE/compile_spor64_a5_anchor.f90" \
  "$BUILD_DIR/compile_spor64_a5_anchor.o"

if compile_checked "$HERE/compile_fail_real32_lane.f90" \
  "$BUILD_DIR/compile_fail_real32_lane.o" \
  >"$BUILD_DIR/compile_fail_real32_lane.log" 2>&1
then
  echo "SPOR64 PHASE-A5 FAILURE: REAL32 mutable lane compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*REAL\\(4\\).*REAL\\(8\\)" \
  "$BUILD_DIR/compile_fail_real32_lane.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: mutable kind mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_integer_kpsys.f90" \
  "$BUILD_DIR/compile_fail_integer_kpsys.o" \
  >"$BUILD_DIR/compile_fail_integer_kpsys.log" 2>&1
then
  echo "SPOR64 PHASE-A5 FAILURE: INTEGER KPSYS compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*INTEGER\\(4\\).*TYPE\\(c_ptr\\)" \
  "$BUILD_DIR/compile_fail_integer_kpsys.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: KPSYS mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_real32_caz.f90" \
  "$BUILD_DIR/compile_fail_real32_caz.o" \
  >"$BUILD_DIR/compile_fail_real32_caz.log" 2>&1
then
  echo "SPOR64 PHASE-A5 FAILURE: REAL32 CAZ compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*REAL\\(4\\).*REAL\\(8\\)" \
  "$BUILD_DIR/compile_fail_real32_caz.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: CAZ kind mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_real64_operator_data.f90" \
  "$BUILD_DIR/compile_fail_real64_operator_data.o" \
  >"$BUILD_DIR/compile_fail_real64_operator_data.log" 2>&1
then
  echo "SPOR64 PHASE-A5 FAILURE: REAL64 frozen operator data compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*REAL\\(8\\).*REAL\\(4\\)" \
  "$BUILD_DIR/compile_fail_real64_operator_data.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: operator kind mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_noncontiguous_population_actual.f90" \
  "$BUILD_DIR/compile_fail_noncontiguous_population_actual.o" \
  >"$BUILD_DIR/compile_fail_noncontiguous_population_actual.log" 2>&1
then
  echo "SPOR64 PHASE-A5 FAILURE: noncontiguous population input compiled" >&2
  exit 1
fi
if ! rg -q "Creating array temporary" \
  "$BUILD_DIR/compile_fail_noncontiguous_population_actual.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: array temporary not diagnosed" >&2
  exit 1
fi

if "$FC" -std=f2008 -fdefault-real-8 -J"$BUILD_DIR" -I"$BUILD_DIR" \
  -c "$HERE/SPOR64_A5.f90" -o "$BUILD_DIR/default_real8.o" \
  >"$BUILD_DIR/default_real8.log" 2>&1
then
  echo "SPOR64 PHASE-A5 FAILURE: global default REAL promotion compiled" >&2
  exit 1
fi
if ! rg -q "Division by zero" "$BUILD_DIR/default_real8.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: kind guard did not diagnose promotion" >&2
  exit 1
fi

nm -u "$BUILD_DIR/SPOR64_A3.o" >"$BUILD_DIR/a3_unresolved.log"
for symbol in mcgfcf mcgffir mcgffar mcgffal mcgsca mcgfst \
  spor64_a3_compile_only_link_forbidden
do
  if ! rg -qi "(^|[[:space:]])_?${symbol}_$" \
    "$BUILD_DIR/a3_unresolved.log"
  then
    echo "SPOR64 PHASE-A5 FAILURE: missing A3 unresolved $symbol" >&2
    exit 1
  fi
done
if test "$(wc -l <"$BUILD_DIR/a3_unresolved.log")" -ne 8
then
  echo "SPOR64 PHASE-A5 FAILURE: A3 unresolved count is not exact" >&2
  exit 1
fi
a3_allowed='(^|[[:space:]])_?(mcgfcf|mcgffir|mcgffar|mcgffal|mcgsca|mcgfst)_$|(^|[[:space:]])_?spor64_a3_compile_only_link_forbidden_$|(^|[[:space:]])_?_gfortran_runtime_error_at$'
if rg -v "$a3_allowed" "$BUILD_DIR/a3_unresolved.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: unexpected A3 unresolved symbol" >&2
  exit 1
fi

nm -u "$BUILD_DIR/SPOR64_A4.o" >"$BUILD_DIR/a4_unresolved.log"
for pattern in \
  '_?__gcc_nested_func_ptr_created' \
  '_?__gcc_nested_func_ptr_deleted' \
  '_?__spor64_a2_MOD_mcgfl1r64_post_stis_raw_facade_locked' \
  '_?__spor64_a3_MOD_mcgfcf_mcgfst_r64_compile_only_locked' \
  '_?_gfortran_os_error_at' \
  '_?_gfortran_runtime_error_at' \
  '_?free' '_?malloc' '_?memcpy' '_?realloc'
do
  if ! rg -q "(^|[[:space:]])${pattern}$" "$BUILD_DIR/a4_unresolved.log"
  then
    echo "SPOR64 PHASE-A5 FAILURE: missing A4 unresolved $pattern" >&2
    exit 1
  fi
done
if test "$(wc -l <"$BUILD_DIR/a4_unresolved.log")" -ne 10
then
  echo "SPOR64 PHASE-A5 FAILURE: A4 unresolved count is not exact" >&2
  exit 1
fi
a4_allowed='(^|[[:space:]])_?(__gcc_nested_func_ptr_created|__gcc_nested_func_ptr_deleted|__spor64_a2_MOD_mcgfl1r64_post_stis_raw_facade_locked|__spor64_a3_MOD_mcgfcf_mcgfst_r64_compile_only_locked)$|(^|[[:space:]])_?(_gfortran_os_error_at|_gfortran_runtime_error_at)$|(^|[[:space:]])_?(free|malloc|memcpy|realloc)$'
if rg -v "$a4_allowed" "$BUILD_DIR/a4_unresolved.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: unexpected A4 unresolved symbol" >&2
  exit 1
fi

nm -u "$BUILD_DIR/SPOR64_A5.o" >"$BUILD_DIR/a5_unresolved.log"
for pattern in \
  '_?__spor64_a4_MOD_mcgfl1r64_a2_a3_host_closure_compile_only_locked' \
  '_?_gfortran_runtime_error_at' \
  '_?free' '_?malloc' '_?memcpy' '_?realloc'
do
  if ! rg -q "(^|[[:space:]])${pattern}$" "$BUILD_DIR/a5_unresolved.log"
  then
    echo "SPOR64 PHASE-A5 FAILURE: missing A5 unresolved $pattern" >&2
    exit 1
  fi
done
if test "$(wc -l <"$BUILD_DIR/a5_unresolved.log")" -ne 6
then
  echo "SPOR64 PHASE-A5 FAILURE: A5 unresolved count is not exact" >&2
  exit 1
fi
a5_allowed='(^|[[:space:]])_?__spor64_a4_MOD_mcgfl1r64_a2_a3_host_closure_compile_only_locked$|(^|[[:space:]])_?_gfortran_runtime_error_at$|(^|[[:space:]])_?(free|malloc|memcpy|realloc)$'
if rg -v "$a5_allowed" "$BUILD_DIR/a5_unresolved.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: unexpected A5 unresolved symbol" >&2
  exit 1
fi

nm -u "$BUILD_DIR/compile_spor64_a5_anchor.o" \
  >"$BUILD_DIR/anchor_unresolved.log"
for pattern in \
  '_?__spor64_a5_MOD_mcgfl1r64_host_shaped_population_compile_only_locked' \
  '_?_gfortran_ieee_procedure_entry' \
  '_?_gfortran_ieee_procedure_exit' \
  '_?_gfortran_runtime_error_at' \
  '_?memset'
do
  if ! rg -q "(^|[[:space:]])${pattern}$" \
    "$BUILD_DIR/anchor_unresolved.log"
  then
    echo "SPOR64 PHASE-A5 FAILURE: missing anchor unresolved $pattern" >&2
    exit 1
  fi
done
if test "$(wc -l <"$BUILD_DIR/anchor_unresolved.log")" -ne 5
then
  echo "SPOR64 PHASE-A5 FAILURE: anchor unresolved count is not exact" >&2
  exit 1
fi
anchor_allowed='(^|[[:space:]])_?__spor64_a5_MOD_mcgfl1r64_host_shaped_population_compile_only_locked$|(^|[[:space:]])_?(_gfortran_ieee_procedure_entry|_gfortran_ieee_procedure_exit|_gfortran_runtime_error_at)$|(^|[[:space:]])_?memset$'
if rg -v "$anchor_allowed" "$BUILD_DIR/anchor_unresolved.log"
then
  echo "SPOR64 PHASE-A5 FAILURE: unexpected anchor unresolved symbol" >&2
  exit 1
fi

if ! nm "$BUILD_DIR/SPOR64_A5.o" | rg -q "populate_context"
then
  echo "SPOR64 PHASE-A5 FAILURE: private population routine missing" >&2
  exit 1
fi
if nm "$BUILD_DIR/SPOR64_A5.o" |
  rg -qi "spor64_a3_compile_only_link_forbidden"
then
  echo "SPOR64 PHASE-A5 FAILURE: A5 owns a second link barrier" >&2
  exit 1
fi
if nm "$BUILD_DIR/SPOR64_A3.o" "$BUILD_DIR/SPOR64_A4.o" \
  "$BUILD_DIR/SPOR64_A5.o" "$BUILD_DIR/compile_spor64_a5_anchor.o" |
  rg -i "(^|[[:space:]])(_?main|MAIN__)(_|$)"
then
  echo "SPOR64 PHASE-A5 FAILURE: executable entry point present" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a5_contract

echo "SPOR64 PHASE-A5 COMPILE-ONLY PRIVATE-POPULATION PASS"
echo "SPOR64 PHASE-A5 FORTRAN-OBJECT-LINKS=0 FORTRAN-EXECUTABLES=0"
echo "SPOR64 PHASE-A5 FORTRAN-OBJECT-EXECUTIONS=0"
echo "SPOR64 PHASE-A5 PREREQUISITE-RUNNERS=0 SYNTHETIC-EXECUTIONS=0"
echo "SPOR64 PHASE-A5 CONTEXT-POPULATION-EXECUTIONS=0"
echo "SPOR64 PHASE-A5 TRACKING-READS=0 TRANSPORT-APPLICATIONS=0"
echo "SPOR64 PHASE-A5 DRAGON-RUNS=0"
