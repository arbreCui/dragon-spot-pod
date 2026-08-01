#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a9b_promotion"
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9/phase_a9a_implementation_receipt.sha256"
RECEIPT="$HERE/phase_a9b_promotion_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a9b-promotion.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
LC_ALL=C
export LC_ALL
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A9b-P FAILURE: unaudited compiler identity" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A9b-P FAILURE: unaudited platform identity" >&2
  exit 1
fi

CHECKED_FLAGS="-O0 -g -std=f2008 -pedantic-errors -Wall -Wextra -Werror"
CHECKED_FLAGS="$CHECKED_FLAGS -Wimplicit-interface -Wimplicit-procedure"
CHECKED_FLAGS="$CHECKED_FLAGS -Wconversion-extra -Warray-temporaries"
CHECKED_FLAGS="$CHECKED_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
CHECKED_FLAGS="$CHECKED_FLAGS -ffp-contract=off -fno-fast-math"

compile_checked()
{
  "$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"
}

expect_compile_failure()
{
  source_file=$1
  object_file=$2
  log_file=$3
  diagnostic_pattern=$4
  if compile_checked "$source_file" "$object_file" >"$log_file" 2>&1
  then
    echo "SPOR64 PHASE-A9b-P FAILURE: negative fixture compiled: $source_file" >&2
    exit 1
  fi
  if ! rg -qi "$diagnostic_pattern" "$log_file"
  then
    echo "SPOR64 PHASE-A9b-P FAILURE: expected diagnostic missing: $source_file" >&2
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
    echo "SPOR64 PHASE-A9b-P FAILURE: unclassified global nm line: $1" >&2
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
echo "SPOR64 PHASE-A9b-P RECEIPT PASS"

PARENT_RECEIPT_SHA256=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
if test "$PARENT_RECEIPT_SHA256" != \
  1251ec474b13ce036ed1c530da71e0de33f27e0c39f7fbaa3b4335b0f01a6c10
then
  echo "SPOR64 PHASE-A9b-P FAILURE: frozen A9a receipt identity changed" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-P FROZEN A9a RECEIPT IDENTITY PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_promotion.py"

PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/script/make_depend.py" \
  --make-deps "$ROOT/src/SPOR64_A8_ACA.f90" \
  "$ROOT/src/SPOR64_A8.f90" \
  "$ROOT/src/MCGFFIR64_RANK_ADAPTER.f90" \
  "$ROOT/src/SPOR64_A9.f90" \
  >"$BUILD_DIR/module_dependencies.txt" \
  2>"$BUILD_DIR/module_dependencies.err"
if test -s "$BUILD_DIR/module_dependencies.err" || \
    ! cmp -s "$HERE/expected_module_dependencies.txt" \
      "$BUILD_DIR/module_dependencies.txt"
then
  echo "SPOR64 PHASE-A9b-P FAILURE: generated dependency edges changed" >&2
  diff -u "$HERE/expected_module_dependencies.txt" \
    "$BUILD_DIR/module_dependencies.txt" >&2 || true
  exit 1
fi
echo "SPOR64 PHASE-A9b-P GENERATED DEPENDENCIES PASS"

compile_checked "$ROOT/src/SPOR64_A8_ACA.f90" \
  "$BUILD_DIR/SPOR64_A8_ACA.o"
compile_checked "$ROOT/src/SPOR64_A8.f90" "$BUILD_DIR/SPOR64_A8.o"
compile_checked "$ROOT/src/MCGFFIR64_RANK_ADAPTER.f90" \
  "$BUILD_DIR/MCGFFIR64_RANK_ADAPTER.o"
compile_checked "$ROOT/src/SPOR64_A9.f90" "$BUILD_DIR/SPOR64_A9.o"
compile_checked "$HERE/compile_spor64_a9b_promotion_anchor.f90" \
  "$BUILD_DIR/compile_spor64_a9b_promotion_anchor.o"

expect_compile_failure "$HERE/compile_fail_real32_state.f90" \
  "$BUILD_DIR/fail_real32_state.o" "$BUILD_DIR/fail_real32_state.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_real64_operator.f90" \
  "$BUILD_DIR/fail_real64_operator.o" \
  "$BUILD_DIR/fail_real64_operator.log" \
  'type mismatch.*real\(8\).*real\(4\)'
expect_compile_failure "$HERE/compile_fail_noncontiguous_state.f90" \
  "$BUILD_DIR/fail_noncontiguous_state.o" \
  "$BUILD_DIR/fail_noncontiguous_state.log" \
  'array temporary|noncontiguous|contiguous'
expect_compile_failure "$HERE/compile_fail_int32_counter.f90" \
  "$BUILD_DIR/fail_int32_counter.o" "$BUILD_DIR/fail_int32_counter.log" \
  'type mismatch.*integer\(4\).*integer\(8\)'
expect_compile_failure "$HERE/compile_fail_flat_keyflx.f90" \
  "$BUILD_DIR/fail_flat_keyflx.o" "$BUILD_DIR/fail_flat_keyflx.log" \
  'rank mismatch'
expect_compile_failure "$HERE/compile_fail_aca_im_extent.f90" \
  "$BUILD_DIR/fail_aca_im_extent.o" "$BUILD_DIR/fail_aca_im_extent.log" \
  'too few elements|actual argument'

DEFAULT_REAL8_DIR="$BUILD_DIR/default-real8"
mkdir -p "$DEFAULT_REAL8_DIR"
for source_stem in SPOR64_A8_ACA SPOR64_A8 MCGFFIR64_RANK_ADAPTER SPOR64_A9
do
  if "$FC" -std=f2008 -fdefault-real-8 -J"$DEFAULT_REAL8_DIR" \
    -I"$BUILD_DIR" -c "$ROOT/src/$source_stem.f90" \
    -o "$DEFAULT_REAL8_DIR/$source_stem.o" \
    >"$DEFAULT_REAL8_DIR/$source_stem.log" 2>&1
  then
    echo "SPOR64 PHASE-A9b-P FAILURE: default REAL promotion compiled: $source_stem" >&2
    exit 1
  fi
  if ! rg -q "Division by zero" "$DEFAULT_REAL8_DIR/$source_stem.log"
  then
    echo "SPOR64 PHASE-A9b-P FAILURE: kind guard did not reject: $source_stem" >&2
    exit 1
  fi
done

for item in aca:SPOR64_A8_ACA a8:SPOR64_A8 \
  adapter:MCGFFIR64_RANK_ADAPTER a9:SPOR64_A9 \
  anchor:compile_spor64_a9b_promotion_anchor
do
  stem=${item%%:*}
  object_stem=${item##*:}
  capture_nm "$BUILD_DIR/$object_stem.o" "$BUILD_DIR/${stem}_nm.txt"
  audit_nm_lines "$BUILD_DIR/${stem}_nm.txt"
  extract_unresolved "$BUILD_DIR/${stem}_nm.txt" \
    "$BUILD_DIR/${stem}_unresolved.txt"
  extract_defined "$BUILD_DIR/${stem}_nm.txt" \
    "$BUILD_DIR/${stem}_defined.txt"
  for symbol_class in unresolved defined
  do
    if ! cmp -s "$HERE/expected_${stem}_${symbol_class}.txt" \
      "$BUILD_DIR/${stem}_${symbol_class}.txt"
    then
      echo "SPOR64 PHASE-A9b-P FAILURE: exact symbol inventory changed: ${stem}_${symbol_class}" >&2
      diff -u "$HERE/expected_${stem}_${symbol_class}.txt" \
        "$BUILD_DIR/${stem}_${symbol_class}.txt" >&2 || true
      exit 1
    fi
  done
done

nm -g "$BUILD_DIR/SPOR64_A8_ACA.o" "$BUILD_DIR/SPOR64_A8.o" \
  "$BUILD_DIR/MCGFFIR64_RANK_ADAPTER.o" "$BUILD_DIR/SPOR64_A9.o" \
  "$BUILD_DIR/compile_spor64_a9b_promotion_anchor.o" \
  >"$BUILD_DIR/a9b_promotion_all_nm.txt"
if rg -i '(^|[[:space:]])(_?main|MAIN__)(_|$)' \
  "$BUILD_DIR/a9b_promotion_all_nm.txt"
then
  echo "SPOR64 PHASE-A9b-P FAILURE: executable entry point present" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a9b_promotion_contract

echo "SPOR64 PHASE-A9b-P PRODUCTION OBJECT PROMOTION PASS"
echo "SPOR64 PHASE-A9b-P NEGATIVE-COMPILES=6 MUTATION-SUITE=PASS"
echo "SPOR64 PHASE-A9b-P OBJECT-LINKS=0 EXECUTABLES=0 OBJECT-EXECUTIONS=0"
echo "SPOR64 PHASE-A9b-P TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A9b-P PRODUCTION-ROUTE-CONNECTED=false"
echo "SPOR64 PHASE-A9b-P CONTINUOUS-REAL64-LANE=false"
echo "SPOR64 PHASE-A9b-P RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A9b-P OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
