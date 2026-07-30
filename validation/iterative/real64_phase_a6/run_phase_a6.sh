#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a6"
A1="$ROOT/validation/iterative/real64_phase_a1"
A2="$ROOT/validation/iterative/real64_phase_a2"
A3="$ROOT/validation/iterative/real64_phase_a3"
A4="$ROOT/validation/iterative/real64_phase_a4"
A5="$ROOT/validation/iterative/real64_phase_a5"
A5_RECEIPT="$A5/phase_a5_implementation_receipt.sha256"
RECEIPT="$HERE/phase_a6_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a6.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
LC_ALL=C
export LC_ALL
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A6 FAILURE: unaudited compiler identity" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A6 FAILURE: unaudited platform identity" >&2
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
echo "SPOR64 PHASE-A6 RECEIPT PASS"

(
  cd "$ROOT"
  shasum -a 256 -c "$A5_RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A6 FROZEN PHASE-A5 RECEIPT PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a6.py"

compile_base "$A1/SPOR64_A1.f90" "$BUILD_DIR/SPOR64_A1.o"
compile_base "$A2/SPOR64_A2.f90" "$BUILD_DIR/SPOR64_A2.o"
compile_checked "$A3/SPOR64_A3.f90" "$BUILD_DIR/SPOR64_A3.o"
compile_checked "$A4/SPOR64_A4.f90" "$BUILD_DIR/SPOR64_A4.o"
compile_checked "$A5/SPOR64_A5.f90" "$BUILD_DIR/SPOR64_A5.o"
compile_checked "$HERE/SPOR64_A6.f90" "$BUILD_DIR/SPOR64_A6.o"
compile_checked "$HERE/compile_spor64_a6_host_callsite.f90" \
  "$BUILD_DIR/compile_spor64_a6_host_callsite.o"

if compile_checked "$HERE/compile_fail_nonlogical_enable.f90" \
  "$BUILD_DIR/compile_fail_nonlogical_enable.o" \
  >"$BUILD_DIR/compile_fail_nonlogical_enable.log" 2>&1
then
  echo "SPOR64 PHASE-A6 FAILURE: non-LOGICAL enable compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*INTEGER\\(4\\).*LOGICAL\\(4\\)" \
  "$BUILD_DIR/compile_fail_nonlogical_enable.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: enable mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_legacy_real32_host_state.f90" \
  "$BUILD_DIR/compile_fail_legacy_real32_host_state.o" \
  >"$BUILD_DIR/compile_fail_legacy_real32_host_state.log" 2>&1
then
  echo "SPOR64 PHASE-A6 FAILURE: legacy REAL32 host state compiled" >&2
  exit 1
fi
if ! rg -q "Type mismatch.*REAL\\(4\\).*REAL\\(8\\)" \
  "$BUILD_DIR/compile_fail_legacy_real32_host_state.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: host-state kind mismatch not diagnosed" >&2
  exit 1
fi

if compile_checked "$HERE/compile_fail_single_group_xssc.f90" \
  "$BUILD_DIR/compile_fail_single_group_xssc.o" \
  >"$BUILD_DIR/compile_fail_single_group_xssc.log" 2>&1
then
  echo "SPOR64 PHASE-A6 FAILURE: one-group XSSC compiled as SC bundle" >&2
  exit 1
fi
if ! rg -q "Rank mismatch.*rank-3 and rank-2" \
  "$BUILD_DIR/compile_fail_single_group_xssc.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: SC bundle rank mismatch not diagnosed" >&2
  exit 1
fi

if "$FC" -std=f2008 -fdefault-real-8 -J"$BUILD_DIR" -I"$BUILD_DIR" \
  -c "$HERE/SPOR64_A6.f90" -o "$BUILD_DIR/default_real8.o" \
  >"$BUILD_DIR/default_real8.log" 2>&1
then
  echo "SPOR64 PHASE-A6 FAILURE: global default REAL promotion compiled" >&2
  exit 1
fi
if ! rg -q "Division by zero" "$BUILD_DIR/default_real8.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: kind guard did not diagnose promotion" >&2
  exit 1
fi

nm -u "$BUILD_DIR/SPOR64_A3.o" >"$BUILD_DIR/a3_unresolved.log"
if ! rg -qi \
  "(^|[[:space:]])_?spor64_a3_compile_only_link_forbidden_$" \
  "$BUILD_DIR/a3_unresolved.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: A3 link barrier missing" >&2
  exit 1
fi
if test "$(wc -l <"$BUILD_DIR/a3_unresolved.log")" -ne 8
then
  echo "SPOR64 PHASE-A6 FAILURE: A3 unresolved count is not exact" >&2
  exit 1
fi

nm -u "$BUILD_DIR/SPOR64_A6.o" >"$BUILD_DIR/a6_unresolved.log"
for pattern in \
  '_?__spor64_a5_MOD_mcgfl1r64_host_shaped_population_compile_only_locked' \
  '_?_gfortran_runtime_error_at'
do
  if ! rg -q "(^|[[:space:]])${pattern}$" "$BUILD_DIR/a6_unresolved.log"
  then
    echo "SPOR64 PHASE-A6 FAILURE: missing A6 unresolved $pattern" >&2
    exit 1
  fi
done
if test "$(wc -l <"$BUILD_DIR/a6_unresolved.log")" -ne 2
then
  echo "SPOR64 PHASE-A6 FAILURE: A6 unresolved count is not exact" >&2
  exit 1
fi
a6_allowed='(^|[[:space:]])_?__spor64_a5_MOD_mcgfl1r64_host_shaped_population_compile_only_locked$|(^|[[:space:]])_?_gfortran_runtime_error_at$'
if rg -v "$a6_allowed" "$BUILD_DIR/a6_unresolved.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: unexpected A6 unresolved symbol" >&2
  exit 1
fi

nm -u "$BUILD_DIR/compile_spor64_a6_host_callsite.o" \
  >"$BUILD_DIR/host_callsite_unresolved.log"
for pattern in \
  '_?__spor64_a6_MOD_mcgfl1r64_default_off_host_adapter_compile_only_locked' \
  '_?_gfortran_ieee_procedure_entry' \
  '_?_gfortran_ieee_procedure_exit' \
  '_?_gfortran_runtime_error_at' \
  '_?memset'
do
  if ! rg -q "(^|[[:space:]])${pattern}$" \
    "$BUILD_DIR/host_callsite_unresolved.log"
  then
    echo "SPOR64 PHASE-A6 FAILURE: missing host-callsite unresolved $pattern" >&2
    exit 1
  fi
done
if test "$(wc -l <"$BUILD_DIR/host_callsite_unresolved.log")" -ne 5
then
  echo "SPOR64 PHASE-A6 FAILURE: host-callsite count is not exact" >&2
  exit 1
fi
host_allowed='(^|[[:space:]])_?__spor64_a6_MOD_mcgfl1r64_default_off_host_adapter_compile_only_locked$|(^|[[:space:]])_?(_gfortran_ieee_procedure_entry|_gfortran_ieee_procedure_exit|_gfortran_runtime_error_at)$|(^|[[:space:]])_?memset$'
if rg -v "$host_allowed" "$BUILD_DIR/host_callsite_unresolved.log"
then
  echo "SPOR64 PHASE-A6 FAILURE: unexpected host-callsite symbol" >&2
  exit 1
fi

if nm "$BUILD_DIR/SPOR64_A6.o" \
  "$BUILD_DIR/compile_spor64_a6_host_callsite.o" |
  rg -qi "spor64_a3_compile_only_link_forbidden"
then
  echo "SPOR64 PHASE-A6 FAILURE: A6 owns a second link barrier" >&2
  exit 1
fi
if nm "$BUILD_DIR/SPOR64_A6.o" \
  "$BUILD_DIR/compile_spor64_a6_host_callsite.o" |
  rg -i "(^|[[:space:]])(_?main|MAIN__)(_|$)"
then
  echo "SPOR64 PHASE-A6 FAILURE: executable entry point present" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a6_contract

echo "SPOR64 PHASE-A6 COMPILE-ONLY HOST-RENDEZVOUS READINESS PASS"
echo "SPOR64 PHASE-A6 FORTRAN-OBJECT-LINKS=0 FORTRAN-EXECUTABLES=0"
echo "SPOR64 PHASE-A6 FORTRAN-OBJECT-EXECUTIONS=0"
echo "SPOR64 PHASE-A6 PREREQUISITE-RUNNERS=0 SYNTHETIC-EXECUTIONS=0"
echo "SPOR64 PHASE-A6 HOST-RENDEZVOUS-EXECUTIONS=0"
echo "SPOR64 PHASE-A6 TRACKING-READS=0 TRANSPORT-APPLICATIONS=0"
echo "SPOR64 PHASE-A6 DRAGON-RUNS=0"
