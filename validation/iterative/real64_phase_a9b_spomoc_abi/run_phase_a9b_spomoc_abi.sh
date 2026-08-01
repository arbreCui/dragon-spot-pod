#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a9b_spomoc_abi"
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_promotion/phase_a9b_promotion_receipt.sha256"
RECEIPT="$HERE/phase_a9b_spomoc_abi_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-spomoc-abi.XXXXXX")
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=/opt/homebrew/bin/gfortran
LC_ALL=C
export LC_ALL
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
if test ! -x "$FC"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: frozen compiler missing" >&2
  exit 1
fi
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: unaudited compiler" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: unaudited platform" >&2
  exit 1
fi
CHECKED_FLAGS="-O0 -g -std=f2008 -pedantic-errors -Wall -Wextra -Werror"
CHECKED_FLAGS="$CHECKED_FLAGS -Wimplicit-interface -Wimplicit-procedure"
CHECKED_FLAGS="$CHECKED_FLAGS -Wconversion-extra -Warray-temporaries"
CHECKED_FLAGS="$CHECKED_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
CHECKED_FLAGS="$CHECKED_FLAGS -ffp-contract=off -fno-fast-math"

compile_checked()
{
  "$FC" $CHECKED_FLAGS -I"$BUILD_DIR" -J"$BUILD_DIR" -c "$1" -o "$2"
}

compile_bootstrap()
{
  "$FC" -O0 -g -std=legacy -ffp-contract=off -fno-fast-math -I"$BUILD_DIR" -J"$BUILD_DIR" -c "$1" -o "$2"
}

expect_compile_failure()
{
  source_file=$1
  object_file=$2
  log_file=$3
  diagnostic_pattern=$4
  if compile_checked "$source_file" "$object_file" >"$log_file" 2>&1
  then
    echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: negative compiled: $source_file" >&2
    exit 1
  fi
  if ! rg -qi "$diagnostic_pattern" "$log_file"
  then
    echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: diagnostic missing" >&2
    sed -n '1,80p' "$log_file" >&2
    exit 1
  fi
}

extract_defined()
{
  nm -g "$1" | awk 'NF >= 3 && $(NF-1) != "U" {print $(NF-1), $NF}' | LC_ALL=C sort -u >"$2"
}

extract_unresolved()
{
  nm -g "$1" | awk 'NF >= 2 && $(NF-1) == "U" {print $NF}' | LC_ALL=C sort -u >"$2"
}

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A9b SPOMOC-ABI RECEIPT PASS"

PARENT_HASH=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
if test "$PARENT_HASH" != cddf3cf36c7f1f180b441b785c0efcacd4d4bbfb2709ebb804f5da0933be3c18
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: parent receipt changed" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_spomoc_abi.py"

PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/script/make_depend.py" \
  --make-deps "$ROOT/src/SPOMOC.f90" "$ROOT/src/SPOMOC_R64_BRIDGE.f90" \
  >"$BUILD_DIR/module_dependencies.txt" 2>"$BUILD_DIR/module_dependencies.err"
if test -s "$BUILD_DIR/module_dependencies.err" || \
    ! cmp -s "$HERE/expected_module_dependencies.txt" "$BUILD_DIR/module_dependencies.txt"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: dependency edge changed" >&2
  diff -u "$HERE/expected_module_dependencies.txt" "$BUILD_DIR/module_dependencies.txt" >&2 || true
  exit 1
fi

cd "$BUILD_DIR"

for source_name in filmod.f90 LCMAUX.f90 lcmmod.f90 LCMTLC.f90 \
  OPNMOD.f90 XDREED.f90 ganlib.f90
do
  cp "$ROOT/Ganlib/src/$source_name" "$BUILD_DIR/$source_name"
done
for source_stem in filmod LCMAUX lcmmod LCMTLC OPNMOD XDREED ganlib
do
  compile_bootstrap "$BUILD_DIR/$source_stem.f90" "$BUILD_DIR/$source_stem.o"
done

for source_name in SPOMOC.f90 SPOMOC_R64_BRIDGE.f90 SPOR64_A8_ACA.f90 \
  SPOR64_A8.f90
do
  cp "$ROOT/src/$source_name" "$BUILD_DIR/$source_name"
done
compile_checked "$BUILD_DIR/SPOMOC.f90" "$BUILD_DIR/SPOMOC.o"
compile_checked "$BUILD_DIR/SPOMOC_R64_BRIDGE.f90" "$BUILD_DIR/SPOMOC_R64_BRIDGE.o"
compile_checked "$BUILD_DIR/SPOR64_A8_ACA.f90" "$BUILD_DIR/SPOR64_A8_ACA.o"
compile_checked "$BUILD_DIR/SPOR64_A8.f90" "$BUILD_DIR/SPOR64_A8.o"

expect_compile_failure "$HERE/compile_fail_real32_capture.f90" \
  "$BUILD_DIR/fail_real32_capture.o" "$BUILD_DIR/fail_real32_capture.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_rank1_capture.f90" \
  "$BUILD_DIR/fail_rank1_capture.o" "$BUILD_DIR/fail_rank1_capture.log" \
  'rank mismatch|array temporary|assumed-shape'
expect_compile_failure "$HERE/compile_fail_real32_bridge.f90" \
  "$BUILD_DIR/fail_real32_bridge.o" "$BUILD_DIR/fail_real32_bridge.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_real32_source.f90" \
  "$BUILD_DIR/fail_real32_source.o" "$BUILD_DIR/fail_real32_source.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_integer_nconv.f90" \
  "$BUILD_DIR/fail_integer_nconv.o" "$BUILD_DIR/fail_integer_nconv.log" \
  'type mismatch.*integer.*logical'
expect_compile_failure "$HERE/compile_fail_int64_ngind.f90" \
  "$BUILD_DIR/fail_int64_ngind.o" "$BUILD_DIR/fail_int64_ngind.log" \
  'type mismatch.*integer\(8\).*integer\(4\)'
expect_compile_failure "$HERE/compile_fail_integer_cyclic.f90" \
  "$BUILD_DIR/fail_integer_cyclic.o" "$BUILD_DIR/fail_integer_cyclic.log" \
  'type mismatch.*integer.*logical'

DEFAULT_INT8_DIR="$BUILD_DIR/default-integer8"
mkdir -p "$DEFAULT_INT8_DIR"
if "$FC" $CHECKED_FLAGS -fdefault-integer-8 -I"$BUILD_DIR" -J"$DEFAULT_INT8_DIR" -c "$BUILD_DIR/SPOMOC.f90" -o "$DEFAULT_INT8_DIR/SPOMOC.o" >"$DEFAULT_INT8_DIR/SPOMOC.log" 2>&1
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: default INTEGER promotion compiled" >&2
  exit 1
fi
if ! rg -qi 'type mismatch.*integer\(8\).*integer\(4\)' "$DEFAULT_INT8_DIR/SPOMOC.log"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: default INTEGER diagnostic missing" >&2
  sed -n '1,80p' "$DEFAULT_INT8_DIR/SPOMOC.log" >&2
  exit 1
fi

extract_defined "$BUILD_DIR/SPOMOC.o" "$BUILD_DIR/spomoc_defined.txt"
extract_unresolved "$BUILD_DIR/SPOMOC.o" "$BUILD_DIR/spomoc_unresolved.txt"
extract_defined "$BUILD_DIR/SPOMOC_R64_BRIDGE.o" "$BUILD_DIR/bridge_defined.txt"
extract_unresolved "$BUILD_DIR/SPOMOC_R64_BRIDGE.o" "$BUILD_DIR/bridge_unresolved.txt"
for item in spomoc_defined spomoc_unresolved bridge_defined bridge_unresolved
do
  if ! cmp -s "$HERE/expected_${item}.txt" "$BUILD_DIR/${item}.txt"
  then
    echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: symbol inventory $item" >&2
    diff -u "$HERE/expected_${item}.txt" "$BUILD_DIR/${item}.txt" >&2 || true
    exit 1
  fi
done

extract_unresolved "$BUILD_DIR/SPOR64_A8.o" "$BUILD_DIR/a8_unresolved_all.txt"
rg '^_spomoc_' "$BUILD_DIR/a8_unresolved_all.txt" >"$BUILD_DIR/a8_spomoc_unresolved.txt"
if ! cmp -s "$HERE/expected_a8_spomoc_unresolved.txt" "$BUILD_DIR/a8_spomoc_unresolved.txt"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: A8 seam inventory" >&2
  exit 1
fi
awk '{print $2}' "$HERE/expected_bridge_defined.txt" >"$BUILD_DIR/bridge_symbols.txt"
if ! cmp -s "$BUILD_DIR/bridge_symbols.txt" "$BUILD_DIR/a8_spomoc_unresolved.txt"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: A8/bridge seam sets differ" >&2
  exit 1
fi

nm -g "$BUILD_DIR/SPOMOC.o" "$BUILD_DIR/SPOMOC_R64_BRIDGE.o" \
  "$BUILD_DIR/SPOR64_A8_ACA.o" "$BUILD_DIR/SPOR64_A8.o" \
  >"$BUILD_DIR/all_nm.txt"
if rg -i '(^|[[:space:]])(_?main|MAIN__)(_|$)' "$BUILD_DIR/all_nm.txt"
then
  echo "SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: entry point present" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a9b_spomoc_abi_contract

echo "SPOR64 PHASE-A9b SPOMOC-ABI COMPILE-ONLY PASS"
echo "SPOR64 PHASE-A9b SPOMOC-ABI NEGATIVE-COMPILES=8 MUTATION-SUITE=PASS"
echo "SPOR64 PHASE-A9b SPOMOC-ABI OBJECT-LINKS=0 EXECUTABLES=0 OBJECT-EXECUTIONS=0"
echo "SPOR64 PHASE-A9b SPOMOC-ABI TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A9b SPOMOC-ABI PRODUCTION-ROUTE-CONNECTED=false"
echo "SPOR64 PHASE-A9b SPOMOC-ABI CONTINUOUS-REAL64-LANE=false"
echo "SPOR64 PHASE-A9b SPOMOC-ABI RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A9b SPOMOC-ABI OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
