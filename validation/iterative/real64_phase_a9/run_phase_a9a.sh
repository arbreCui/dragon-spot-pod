#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a9"
A8="$ROOT/validation/iterative/real64_phase_a8"
A8_RECEIPT="$A8/phase_a8_implementation_receipt.sha256"
RECEIPT="$HERE/phase_a9a_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a9a.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
LC_ALL=C
export LC_ALL
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A9a FAILURE: unaudited compiler identity" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A9a FAILURE: unaudited platform identity" >&2
  exit 1
fi

CHECKED_FLAGS="-O0 -g -std=f2008 -pedantic-errors -Wall -Wextra -Werror"
CHECKED_FLAGS="$CHECKED_FLAGS -Wimplicit-interface -Wimplicit-procedure"
CHECKED_FLAGS="$CHECKED_FLAGS -Wconversion-extra -Warray-temporaries"
CHECKED_FLAGS="$CHECKED_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
CHECKED_FLAGS="$CHECKED_FLAGS -ffp-contract=off -fno-fast-math"
LEGACY_FLAGS="-O0 -std=legacy -ffixed-line-length-none"

compile_checked()
{
  "$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"
}

compile_legacy()
{
  "$FC" $LEGACY_FLAGS -c "$1" -o "$2"
}

expect_compile_failure()
{
  source_file=$1
  object_file=$2
  log_file=$3
  diagnostic_pattern=$4
  if compile_checked "$source_file" "$object_file" >"$log_file" 2>&1
  then
    echo "SPOR64 PHASE-A9a FAILURE: negative fixture compiled: $source_file" >&2
    exit 1
  fi
  if ! rg -qi "$diagnostic_pattern" "$log_file"
  then
    echo "SPOR64 PHASE-A9a FAILURE: expected diagnostic missing: $source_file" >&2
    sed -n '1,80p' "$log_file" >&2
    exit 1
  fi
}

capture_nm()
{
  nm -g "$1" >"$2"
}

audit_nm_lines()
{
  if ! awk '
    NF == 0 {next}
    NF >= 2 && $(NF-1) == "U" {next}
    NF >= 3 && $(NF-1) != "U" {next}
    {bad=1}
    END {exit bad}
  ' "$1"
  then
    echo "SPOR64 PHASE-A9a FAILURE: unclassified global nm line: $1" >&2
    exit 1
  fi
}

extract_unresolved()
(
  raw_file=$1
  output_file=$2
  awk 'NF >= 2 && $(NF-1) == "U" {print $NF}' "$raw_file" \
    >"$output_file.unsorted"
  LC_ALL=C sort -u "$output_file.unsorted" -o "$output_file"
)

extract_defined()
(
  raw_file=$1
  output_file=$2
  awk 'NF >= 3 && $(NF-1) != "U" {print $(NF-1), $NF}' "$raw_file" \
    >"$output_file.unsorted"
  LC_ALL=C sort -u "$output_file.unsorted" -o "$output_file"
)

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A9a RECEIPT PASS"

A8_RECEIPT_SHA256=$(shasum -a 256 "$A8_RECEIPT" | awk '{print $1}')
if test "$A8_RECEIPT_SHA256" != \
  5c5d0b118269d111360536d8dc6bdead23ad56b22220cc8ace3e4282ee8377fa
then
  echo "SPOR64 PHASE-A9a FAILURE: frozen A8 receipt identity changed" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9a FROZEN A8 RECEIPT IDENTITY PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9.py"

compile_checked "$A8/SPOR64_A8_ACA.f90" "$BUILD_DIR/SPOR64_A8_ACA.o"
compile_checked "$A8/SPOR64_A8.f90" "$BUILD_DIR/SPOR64_A8.o"
compile_checked "$HERE/SPOR64_A9.f90" "$BUILD_DIR/SPOR64_A9.o"
compile_checked "$HERE/SPOR64_A9_HOST.f90" "$BUILD_DIR/SPOR64_A9_HOST.o"
compile_checked "$HERE/compile_spor64_a9_anchor.f90" \
  "$BUILD_DIR/compile_spor64_a9_anchor.o"
compile_legacy "$ROOT/Utilib/src/ALSBD.f" "$BUILD_DIR/ALSBD.o"

expect_compile_failure "$HERE/compile_fail_real32_state.f90" \
  "$BUILD_DIR/fail_real32_state.o" "$BUILD_DIR/fail_real32_state.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_real32_terminal.f90" \
  "$BUILD_DIR/fail_real32_terminal.o" \
  "$BUILD_DIR/fail_real32_terminal.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_real64_operator.f90" \
  "$BUILD_DIR/fail_real64_operator.o" "$BUILD_DIR/fail_real64_operator.log" \
  'type mismatch.*real\(8\).*real\(4\)'
expect_compile_failure "$HERE/compile_fail_noncontiguous_state.f90" \
  "$BUILD_DIR/fail_noncontiguous_state.o" \
  "$BUILD_DIR/fail_noncontiguous_state.log" \
  'array temporary|noncontiguous|contiguous'
expect_compile_failure "$HERE/compile_fail_flu2ac_element.f90" \
  "$BUILD_DIR/fail_flu2ac_element.o" "$BUILD_DIR/fail_flu2ac_element.log" \
  'rank mismatch'
expect_compile_failure "$HERE/compile_fail_int32_cutoff.f90" \
  "$BUILD_DIR/fail_int32_cutoff.o" "$BUILD_DIR/fail_int32_cutoff.log" \
  'type mismatch.*integer\(4\).*integer\(8\)'
expect_compile_failure "$HERE/compile_fail_nonlogical_selector.f90" \
  "$BUILD_DIR/fail_nonlogical_selector.o" \
  "$BUILD_DIR/fail_nonlogical_selector.log" \
  'type mismatch.*integer\(4\).*logical\(4\)'

DEFAULT_REAL8_DIR="$BUILD_DIR/default-real8"
mkdir -p "$DEFAULT_REAL8_DIR"
for source_stem in SPOR64_A9 SPOR64_A9_HOST
do
  if "$FC" -std=f2008 -fdefault-real-8 -J"$DEFAULT_REAL8_DIR" \
    -I"$BUILD_DIR" -c "$HERE/$source_stem.f90" \
    -o "$DEFAULT_REAL8_DIR/$source_stem.o" \
    >"$DEFAULT_REAL8_DIR/$source_stem.log" 2>&1
  then
    echo "SPOR64 PHASE-A9a FAILURE: default REAL promotion compiled: $source_stem" >&2
    exit 1
  fi
  if ! rg -q "Division by zero" "$DEFAULT_REAL8_DIR/$source_stem.log"
  then
    echo "SPOR64 PHASE-A9a FAILURE: kind guard did not reject: $source_stem" >&2
    exit 1
  fi
done

capture_nm "$BUILD_DIR/SPOR64_A9.o" "$BUILD_DIR/core_nm.txt"
capture_nm "$BUILD_DIR/SPOR64_A9_HOST.o" "$BUILD_DIR/host_nm.txt"
capture_nm "$BUILD_DIR/compile_spor64_a9_anchor.o" "$BUILD_DIR/anchor_nm.txt"
audit_nm_lines "$BUILD_DIR/core_nm.txt"
audit_nm_lines "$BUILD_DIR/host_nm.txt"
audit_nm_lines "$BUILD_DIR/anchor_nm.txt"

for stem in core host anchor
do
  extract_unresolved "$BUILD_DIR/${stem}_nm.txt" \
    "$BUILD_DIR/${stem}_unresolved.txt"
  extract_defined "$BUILD_DIR/${stem}_nm.txt" \
    "$BUILD_DIR/${stem}_defined.txt"
  for class in unresolved defined
  do
    if ! cmp -s "$HERE/expected_${stem}_${class}.txt" \
      "$BUILD_DIR/${stem}_${class}.txt"
    then
      echo "SPOR64 PHASE-A9a FAILURE: exact symbol inventory changed: ${stem}_${class}" >&2
      diff -u "$HERE/expected_${stem}_${class}.txt" \
        "$BUILD_DIR/${stem}_${class}.txt" >&2 || true
      exit 1
    fi
  done
done

nm -g "$BUILD_DIR/SPOR64_A9.o" "$BUILD_DIR/SPOR64_A9_HOST.o" \
  "$BUILD_DIR/compile_spor64_a9_anchor.o" >"$BUILD_DIR/a9a_all_nm.txt"
if rg -i '(^|[[:space:]])(_?main|MAIN__)(_|$)' "$BUILD_DIR/a9a_all_nm.txt"
then
  echo "SPOR64 PHASE-A9a FAILURE: executable entry point present" >&2
  exit 1
fi
if rg -i '(^|[[:space:]])_?(doorfv|flubal|flu2ac|alsb|spomoc_capture)_$' \
  "$BUILD_DIR/core_nm.txt"
then
  echo "SPOR64 PHASE-A9a FAILURE: forbidden legacy symbol present" >&2
  exit 1
fi
if rg -i '__spor64_a[1-7]_MOD_' "$BUILD_DIR/core_nm.txt"
then
  echo "SPOR64 PHASE-A9a FAILURE: dependency below frozen A8 boundary" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a9_contract

echo "SPOR64 PHASE-A9a COMPILE-ONLY OUTER CLOSURE PASS"
echo "SPOR64 PHASE-A9a NEGATIVE-COMPILES=7 MUTATION-SUITE=PASS"
echo "SPOR64 PHASE-A9a OBJECT-LINKS=0 EXECUTABLES=0 OBJECT-EXECUTIONS=0"
echo "SPOR64 PHASE-A9a PREREQUISITE-RUNNERS=0 SYNTHETIC-EXECUTIONS=0"
echo "SPOR64 PHASE-A9a TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A9a PRODUCTION-ROUTE-CONNECTED=false CONTINUOUS-REAL64-LANE=false"
echo "SPOR64 PHASE-A9a RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A9a OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
