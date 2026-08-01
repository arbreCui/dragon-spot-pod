#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a9b_b2b_ingress"
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2a_selector/phase_a9b_b2a_selector_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2b_ingress_receipt.sha256"
EXPECTED_PARENT_HASH=cb9469efbe9e98669e57be686b9d1366a4570696d6941e5823ba16283293d2c4
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2b.XXXXXX")
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=/opt/homebrew/bin/gfortran
readonly FC
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
LC_ALL=C
export LC_ALL

if test ! -x "$FC"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: frozen compiler missing" >&2
  exit 1
fi
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: unaudited compiler" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: unaudited platform" >&2
  exit 1
fi

cd "$ROOT"
if test ! -f "$RECEIPT"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: implementation receipt missing" >&2
  exit 1
fi
shasum -a 256 -c "$RECEIPT" >/dev/null
PARENT_HASH=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
if test "$PARENT_HASH" != "$EXPECTED_PARENT_HASH"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: parent receipt changed" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-B2b RECEIPT PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2b_ingress.py"

PROD_DIR="$BUILD_DIR/production"
mkdir -p "$PROD_DIR"
cd "$PROD_DIR"

for source_name in filmod LCMAUX lcmmod LCMTLC OPNMOD XDREED ganlib
do
  "$FC" -O0 -g -std=legacy -ffp-contract=off -fno-fast-math \
    -I"$PROD_DIR" -J"$PROD_DIR" \
    -c "$ROOT/Ganlib/src/$source_name.f90" \
    -o "$PROD_DIR/$source_name.o"
done

FREE_FLAGS="-O0 -g -std=f2008 -pedantic-errors -fimplicit-none"
FREE_FLAGS="$FREE_FLAGS -fcheck=all -fbacktrace -ffp-contract=off"
FREE_FLAGS="$FREE_FLAGS -fno-fast-math"

compile_free()
{
  source_path=$1
  object_path=$2
  "$FC" $FREE_FLAGS -I"$PROD_DIR" -J"$PROD_DIR" \
    -c "$source_path" -o "$object_path"
}

compile_fixed()
{
  source_path=$1
  object_path=$2
  "$FC" -O0 -g -std=legacy -pedantic-errors -ffixed-line-length-72 \
    -fcheck=all -fbacktrace -ffp-contract=off -fno-fast-math \
    -I"$PROD_DIR" -J"$PROD_DIR" -c "$source_path" -o "$object_path"
}

compile_free "$ROOT/src/SPOMOC.f90" "$PROD_DIR/SPOMOC.o"
compile_free "$ROOT/src/SPOMOC_R64_BRIDGE.f90" \
  "$PROD_DIR/SPOMOC_R64_BRIDGE.o"
compile_free "$ROOT/src/SPOR64_A8_ACA.f90" "$PROD_DIR/SPOR64_A8_ACA.o"
compile_free "$ROOT/src/SPOR64_A8.f90" "$PROD_DIR/SPOR64_A8.o"
compile_free "$ROOT/src/MCGFFIR64_RANK_ADAPTER.f90" \
  "$PROD_DIR/MCGFFIR64_RANK_ADAPTER.o"
compile_free "$ROOT/src/SPOR64_A9.f90" "$PROD_DIR/SPOR64_A9.o"
compile_free "$ROOT/src/SPOR64_B2B.f90" "$PROD_DIR/SPOR64_B2B.o"
compile_fixed "$ROOT/src/FLUGPI.f" "$PROD_DIR/FLUGPI.o"
compile_fixed "$ROOT/src/FLU.f" "$PROD_DIR/FLU.o"
compile_fixed "$ROOT/src/XDRTA2.f" "$PROD_DIR/XDRTA2.o"

nm -g "$PROD_DIR/FLU.o" >"$PROD_DIR/flu.nm"
nm -g "$PROD_DIR/SPOR64_B2B.o" >"$PROD_DIR/b2b.nm"

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

for source_stem in b2b flu
do
  if test "$source_stem" = b2b
  then
    object="$PROD_DIR/SPOR64_B2B.o"
  else
    object="$PROD_DIR/FLU.o"
  fi
  extract_defined "$object" "$PROD_DIR/${source_stem}_defined.txt"
  extract_unresolved "$object" "$PROD_DIR/${source_stem}_unresolved.txt"
  for inventory in defined unresolved
  do
    if ! cmp -s "$HERE/expected_${source_stem}_${inventory}.txt" \
      "$PROD_DIR/${source_stem}_${inventory}.txt"
    then
      echo "SPOR64 PHASE-A9b-B2b FAILURE: $source_stem $inventory symbols" >&2
      diff -u "$HERE/expected_${source_stem}_${inventory}.txt" \
        "$PROD_DIR/${source_stem}_${inventory}.txt" >&2 || true
      exit 1
    fi
  done
done

if ! rg -qi 'spor64_b2b.*ingress' "$PROD_DIR/flu.nm"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: FLU lacks B2b ingress symbol" >&2
  exit 1
fi
if ! rg -qi 'xdrta2' "$PROD_DIR/b2b.nm" || \
  ! rg -qi 'spor64_a9.*flu2dr64_core' "$PROD_DIR/b2b.nm"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: ingress rendezvous symbols" >&2
  exit 1
fi
if rg -qi 'lcmput|lcmptc|lcmpdl|lcmppd|lcmlid|lcmdid|lcmdel|lcmdil' \
  "$PROD_DIR/b2b.nm"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: ingress exposes LCM mutation" >&2
  exit 1
fi
nm -g "$PROD_DIR"/*.o >"$PROD_DIR/all.nm"
if rg -i '(^|[[:space:]])(_?main|MAIN__)(_|$)' "$PROD_DIR/all.nm"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: production entry point present" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-B2b PRODUCTION COMPILE PASS"

ABI_DIR="$BUILD_DIR/xdrta2-abi"
mkdir -p "$ABI_DIR"
compile_free "$HERE/compile_xdrta2_zeroarg_positive.f90" \
  "$ABI_DIR/xdrta2_zeroarg_positive.o"
if compile_free "$HERE/compile_xdrta2_extra_actual_negative.f90" \
  "$ABI_DIR/xdrta2_extra_actual_negative.o" \
  >"$ABI_DIR/negative.log" 2>&1
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: extra XDRTA2 actual compiled" >&2
  exit 1
fi
if ! rg -qi 'more actual than formal|too many arguments' \
  "$ABI_DIR/negative.log"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: missing XDRTA2 diagnostic" >&2
  sed -n '1,80p' "$ABI_DIR/negative.log" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-B2b XDRTA2 ZERO-ARGUMENT ABI PASS"

SYN_DIR="$BUILD_DIR/synthetic"
mkdir -p "$SYN_DIR"
compile_free "$HERE/b2b_synthetic_dispatch.f90" \
  "$SYN_DIR/b2b_synthetic_dispatch.o"
compile_free "$HERE/b2b_synthetic_dispatch_driver.f90" \
  "$SYN_DIR/b2b_synthetic_dispatch_driver.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$SYN_DIR/b2b_synthetic_dispatch.o" \
  "$SYN_DIR/b2b_synthetic_dispatch_driver.o" \
  -o "$SYN_DIR/b2b_synthetic_dispatch"
nm -g "$SYN_DIR/b2b_synthetic_dispatch" >"$SYN_DIR/synthetic.nm"
if rg -qi 'xdrta2|flu2dr|doorfv|mccgf|dragon' "$SYN_DIR/synthetic.nm"
then
  echo "SPOR64 PHASE-A9b-B2b FAILURE: synthetic linked transport" >&2
  exit 1
fi
for scenario in off selected admission-fail core-fail
do
  "$SYN_DIR/b2b_synthetic_dispatch" "$scenario" \
    >"$SYN_DIR/$scenario.log" 2>&1
  if ! rg -q "^B2B-DISPATCH-PASS $scenario$" "$SYN_DIR/$scenario.log"
  then
    echo "SPOR64 PHASE-A9b-B2b FAILURE: synthetic case $scenario" >&2
    sed -n '1,80p' "$SYN_DIR/$scenario.log" >&2
    exit 1
  fi
done

cd "$ROOT"
PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a9b_b2b_ingress_contract

echo "SPOR64 PHASE-A9b-B2b INGRESS PASS"
echo "SPOR64 PHASE-A9b-B2b CONTRACT-TESTS=40"
echo "SPOR64 PHASE-A9b-B2b NEGATIVE-COMPILES=1 SYNTHETIC-EXECUTIONS=4"
echo "SPOR64 PHASE-A9b-B2b PRODUCTION-OBJECT-LINKS=0 PRODUCTION-EXECUTIONS=0"
echo "SPOR64 PHASE-A9b-B2b TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A9b-B2b ACCEPTED-PUBLICATION=false"
echo "SPOR64 PHASE-A9b-B2b RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A9b-B2b OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
