#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a9b_b2a_selector"
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_spomoc_abi/phase_a9b_spomoc_abi_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2a_selector_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2a.XXXXXX")
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=/opt/homebrew/bin/gfortran
readonly FC
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
LC_ALL=C
export LC_ALL

if test ! -x "$FC"
then
  echo "SPOR64 PHASE-A9b-B2a FAILURE: frozen compiler missing" >&2
  exit 1
fi
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A9b-B2a FAILURE: unaudited compiler" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A9b-B2a FAILURE: unaudited platform" >&2
  exit 1
fi

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A9b-B2a RECEIPT PASS"

PARENT_HASH=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
if test "$PARENT_HASH" != eaa570a765afe5be29a71e554edade2ab515b1094d64d43bcfdcbb01f2082ef9
then
  echo "SPOR64 PHASE-A9b-B2a FAILURE: parent receipt changed" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2a_selector.py"

PROD_DIR="$BUILD_DIR/production"
mkdir -p "$PROD_DIR"
for source_name in filmod.f90 LCMAUX.f90 lcmmod.f90 LCMTLC.f90 \
  OPNMOD.f90 XDREED.f90 ganlib.f90
do
  cp "$ROOT/Ganlib/src/$source_name" "$PROD_DIR/$source_name"
done
cp "$ROOT/src/SPOMOC.f90" "$PROD_DIR/SPOMOC.f90"
cp "$ROOT/src/FLUGPI.f" "$PROD_DIR/FLUGPI.f"
cp "$ROOT/src/FLUDRV.f" "$PROD_DIR/FLUDRV.f"
cp "$ROOT/src/FLU.f" "$PROD_DIR/FLU.f"

cd "$PROD_DIR"
for source_stem in filmod LCMAUX lcmmod LCMTLC OPNMOD XDREED ganlib
do
  "$FC" -O0 -g -std=legacy -ffp-contract=off -fno-fast-math \
    -I"$PROD_DIR" -J"$PROD_DIR" -c "$source_stem.f90" \
    -o "$source_stem.o"
done
"$FC" -O0 -g -std=f2008 -pedantic-errors -ffp-contract=off \
  -fno-fast-math -I"$PROD_DIR" -J"$PROD_DIR" -c SPOMOC.f90 -o SPOMOC.o
for source_stem in FLUGPI FLUDRV FLU
do
  "$FC" -O0 -g -std=legacy -pedantic-errors -ffixed-line-length-72 \
    -fcheck=all -fbacktrace -ffp-contract=off -fno-fast-math \
    -I"$PROD_DIR" -J"$PROD_DIR" -c "$source_stem.f" \
    -o "$source_stem.o"
done

extract_defined()
{
  nm -g "$1" | awk 'NF >= 3 && $(NF-1) != "U" {print $(NF-1), $NF}' | \
    LC_ALL=C sort -u >"$2"
}

extract_unresolved()
{
  nm -g "$1" | awk 'NF >= 2 && $(NF-1) == "U" {print $NF}' | \
    LC_ALL=C sort -u >"$2"
}

for source_stem in flu flugpi fludrv
do
  upper=$(printf '%s' "$source_stem" | tr '[:lower:]' '[:upper:]')
  extract_defined "$PROD_DIR/$upper.o" "$PROD_DIR/${source_stem}_defined.txt"
  extract_unresolved "$PROD_DIR/$upper.o" "$PROD_DIR/${source_stem}_unresolved.txt"
  for inventory in defined unresolved
  do
    if ! cmp -s "$HERE/expected_${source_stem}_${inventory}.txt" \
      "$PROD_DIR/${source_stem}_${inventory}.txt"
    then
      echo "SPOR64 PHASE-A9b-B2a FAILURE: $source_stem $inventory symbols" >&2
      diff -u "$HERE/expected_${source_stem}_${inventory}.txt" \
        "$PROD_DIR/${source_stem}_${inventory}.txt" >&2 || true
      exit 1
    fi
  done
done

nm -g "$PROD_DIR/SPOMOC.o" "$PROD_DIR/FLUGPI.o" \
  "$PROD_DIR/FLUDRV.o" "$PROD_DIR/FLU.o" >"$PROD_DIR/all_nm.txt"
if rg -i '(^|[[:space:]])(_?main|MAIN__)(_|$)' "$PROD_DIR/all_nm.txt"
then
  echo "SPOR64 PHASE-A9b-B2a FAILURE: production entry point present" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-B2a PRODUCTION COMPILE PASS"

PARSER_DIR="$BUILD_DIR/parser"
mkdir -p "$PARSER_DIR"
cd "$PARSER_DIR"
CHECKED_FLAGS="-O0 -g -std=f2008 -pedantic-errors -Wall -Wextra -Werror"
CHECKED_FLAGS="$CHECKED_FLAGS -fimplicit-none -fcheck=all -fbacktrace"
CHECKED_FLAGS="$CHECKED_FLAGS -ffp-contract=off -fno-fast-math"
"$FC" $CHECKED_FLAGS -I"$PARSER_DIR" -J"$PARSER_DIR" \
  -c "$HERE/b2a_synthetic_ganlib.f90" -o b2a_synthetic_ganlib.o
"$FC" -O0 -g -std=legacy -pedantic-errors -ffixed-line-length-72 \
  -fcheck=all -fbacktrace -ffp-contract=off -fno-fast-math \
  -I"$PARSER_DIR" -J"$PARSER_DIR" -c "$ROOT/src/FLUGPI.f" -o FLUGPI.o
if nm -g FLUGPI.o | rg -i 'lcmput|lcmptc|lcmpdl|lcmppd|lcmlid|lcmdid'
then
  echo "SPOR64 PHASE-A9b-B2a FAILURE: parser exposes a write symbol" >&2
  exit 1
fi
"$FC" $CHECKED_FLAGS -I"$PARSER_DIR" -J"$PARSER_DIR" \
  -c "$HERE/b2a_parser_driver.f90" -o b2a_parser_driver.o
"$FC" -O0 -g -fcheck=all -fbacktrace b2a_synthetic_ganlib.o \
  FLUGPI.o b2a_parser_driver.o -o b2a_parser

for scenario in default r64 moca moca_r64 r64_moca lifetime rec_clean \
  rec_hete rec_r64_hete
do
  ./b2a_parser "$scenario" >"$scenario.log" 2>&1
  if ! rg -q '^B2A-PARSER-PASS ' "$scenario.log"
  then
    echo "SPOR64 PHASE-A9b-B2a FAILURE: parser case $scenario" >&2
    sed -n '1,80p' "$scenario.log" >&2
    exit 1
  fi
done

expect_parser_failure()
{
  scenario=$1
  pattern=$2
  if ./b2a_parser "$scenario" >"$scenario.log" 2>&1
  then
    echo "SPOR64 PHASE-A9b-B2a FAILURE: negative parser case returned" >&2
    exit 1
  fi
  if ! rg -q "$pattern" "$scenario.log"
  then
    echo "SPOR64 PHASE-A9b-B2a FAILURE: parser diagnostic $scenario" >&2
    sed -n '1,80p' "$scenario.log" >&2
    exit 1
  fi
  if rg -q '^B2A-PARSER-PASS ' "$scenario.log"
  then
    echo "SPOR64 PHASE-A9b-B2a FAILURE: failed parser case published PASS" >&2
    exit 1
  fi
}

expect_parser_failure duplicate \
  '^B2A-XABORT FLUGPI: DUPLICATE R64 KEYWORD\.$'
expect_parser_failure parameter \
  '^B2A-XABORT FLUGPI: READ ERROR - CHARACTER VARIABLE EXPECTED$'
expect_parser_failure bogus \
  '^B2A-XABORT FLUGPI: READ ERROR - ILLEGAL KEYWORD BOGU$'
echo "SPOR64 PHASE-A9b-B2a SYNTHETIC PARSER PASS"

ABI_DIR="$BUILD_DIR/abi"
mkdir -p "$ABI_DIR"
cd "$ABI_DIR"
"$FC" $CHECKED_FLAGS -I"$ABI_DIR" -J"$ABI_DIR" \
  -c "$HERE/B2A_SELECTOR_ABI.f90" -o B2A_SELECTOR_ABI.o
"$FC" $CHECKED_FLAGS -I"$ABI_DIR" -J"$ABI_DIR" \
  -c "$HERE/compile_b2a_selector_anchor.f90" \
  -o compile_b2a_selector_anchor.o

expect_compile_failure()
{
  source_file=$1
  object_file=$2
  log_file=$3
  diagnostic_pattern=$4
  if "$FC" $CHECKED_FLAGS -I"$ABI_DIR" -J"$ABI_DIR" \
    -c "$source_file" -o "$object_file" >"$log_file" 2>&1
  then
    echo "SPOR64 PHASE-A9b-B2a FAILURE: negative compiled $source_file" >&2
    exit 1
  fi
  if ! rg -qi "$diagnostic_pattern" "$log_file"
  then
    echo "SPOR64 PHASE-A9b-B2a FAILURE: negative diagnostic missing" >&2
    sed -n '1,80p' "$log_file" >&2
    exit 1
  fi
}

expect_compile_failure "$HERE/compile_fail_nonlogical_limerg.f90" \
  fail_nonlogical_limerg.o fail_nonlogical_limerg.log \
  'type mismatch.*integer.*logical'
expect_compile_failure "$HERE/compile_fail_nonlogical_lr64.f90" \
  fail_nonlogical_lr64.o fail_nonlogical_lr64.log \
  'type mismatch.*integer.*logical'
expect_compile_failure "$HERE/compile_fail_nonlogical_driver.f90" \
  fail_nonlogical_driver.o fail_nonlogical_driver.log \
  'type mismatch.*integer.*logical'
expect_compile_failure "$HERE/compile_fail_rank1_lr64.f90" \
  fail_rank1_lr64.o fail_rank1_lr64.log \
  'rank mismatch.*scalar and rank-1'

cd "$ROOT"
PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a9b_b2a_selector_contract

echo "SPOR64 PHASE-A9b-B2a SELECTOR PASS"
echo "SPOR64 PHASE-A9b-B2a MUTATION-TESTS=55 NEGATIVE-COMPILES=4"
echo "SPOR64 PHASE-A9b-B2a SYNTHETIC-PARSER-LINKS=1 PARSER-EXECUTIONS=12"
echo "SPOR64 PHASE-A9b-B2a PRODUCTION-OBJECT-LINKS=0 PRODUCTION-EXECUTIONS=0"
echo "SPOR64 PHASE-A9b-B2a TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A9b-B2a R64-KEYWORD-RECOGNIZED=true R64-DEFAULT=false"
echo "SPOR64 PHASE-A9b-B2a R64-ROUTE-EXECUTABLE=false"
echo "SPOR64 PHASE-A9b-B2a PRODUCTION-ROUTE-CONNECTED=false"
echo "SPOR64 PHASE-A9b-B2a CONTINUOUS-REAL64-LANE=false"
echo "SPOR64 PHASE-A9b-B2a RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A9b-B2a OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
