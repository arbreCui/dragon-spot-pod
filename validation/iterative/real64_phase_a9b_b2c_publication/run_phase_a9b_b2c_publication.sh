#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a9b_b2c_publication"
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2b_ingress/phase_a9b_b2b_ingress_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2c_publication_receipt.sha256"
EXPECTED_PARENT_COMMIT=c00072ca7ba6cbd15f9494dfc943344ec325a21d
EXPECTED_PARENT_HASH=bfdcffd594ec69f0e259a621945dce3b9a551831c01e2fa7ee5bfcaab41dc2cc
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-a9b-b2c.XXXXXX")
trap 'cd /; rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=/opt/homebrew/bin/gfortran
readonly FC
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
LC_ALL=C
export LC_ALL

if test ! -x "$FC"
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: frozen compiler missing" >&2
  exit 1
fi
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: unaudited compiler" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: unaudited platform" >&2
  exit 1
fi

cd "$ROOT"
PARENT_HASH=$(shasum -a 256 "$PARENT_RECEIPT" | awk '{print $1}')
if test "$PARENT_HASH" != "$EXPECTED_PARENT_HASH"
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: parent receipt changed" >&2
  exit 1
fi
git cat-file -e "$EXPECTED_PARENT_COMMIT^{commit}"
if test ! -f "$RECEIPT"
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: implementation receipt missing" >&2
  exit 1
fi
shasum -a 256 -c "$RECEIPT" >/dev/null
echo "SPOR64 PHASE-A9b-B2c RECEIPT PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2c_publication.py"

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
compile_free "$ROOT/src/SPOMOC_R64_BRIDGE.f90" "$PROD_DIR/SPOMOC_R64_BRIDGE.o"
compile_free "$ROOT/src/SPOR64_A8_ACA.f90" "$PROD_DIR/SPOR64_A8_ACA.o"
compile_free "$ROOT/src/SPOR64_A8.f90" "$PROD_DIR/SPOR64_A8.o"
compile_free "$ROOT/src/MCGFFIR64_RANK_ADAPTER.f90" "$PROD_DIR/MCGFFIR64_RANK_ADAPTER.o"
compile_free "$ROOT/src/SPOR64_A9.f90" "$PROD_DIR/SPOR64_A9.o"
compile_free "$ROOT/src/SPOR64_B2C.f90" "$PROD_DIR/SPOR64_B2C.o"
compile_free "$ROOT/src/SPOR64_B2B.f90" "$PROD_DIR/SPOR64_B2B.o"
compile_fixed "$ROOT/src/FLUGPI.f" "$PROD_DIR/FLUGPI.o"
compile_fixed "$ROOT/src/FLU.f" "$PROD_DIR/FLU.o"
compile_fixed "$ROOT/src/XDRTA2.f" "$PROD_DIR/XDRTA2.o"

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

for source_stem in b2c b2b flu
do
  case "$source_stem" in
    b2c) object="$PROD_DIR/SPOR64_B2C.o" ;;
    b2b) object="$PROD_DIR/SPOR64_B2B.o" ;;
    flu) object="$PROD_DIR/FLU.o" ;;
  esac
  extract_defined "$object" "$PROD_DIR/${source_stem}_defined.txt"
  extract_unresolved "$object" "$PROD_DIR/${source_stem}_unresolved.txt"
  for inventory in defined unresolved
  do
    if ! cmp -s "$HERE/expected_${source_stem}_${inventory}.txt" \
      "$PROD_DIR/${source_stem}_${inventory}.txt"
    then
      echo "SPOR64 PHASE-A9b-B2c FAILURE: $source_stem $inventory symbols" >&2
      diff -u "$HERE/expected_${source_stem}_${inventory}.txt" \
        "$PROD_DIR/${source_stem}_${inventory}.txt" >&2 || true
      exit 1
    fi
  done
done
if ! nm -g "$PROD_DIR/SPOR64_B2C.o" | rg -qi 'spor64_b2c.*publish'
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: publisher symbol missing" >&2
  exit 1
fi
if nm -g "$PROD_DIR/SPOR64_B2C.o" | rg -qi 'flu2dr|xdrta2|doorfv|mccgf|dragon'
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: publisher exposes solver/transport" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-B2c PRODUCTION STRICT-C PASS"

ABI_DIR="$BUILD_DIR/abi"
mkdir -p "$ABI_DIR"
compile_free "$HERE/compile_b2c_positive.f90" "$ABI_DIR/b2c_positive.o"
if compile_free "$HERE/compile_fail_b2c_real32_terminal.f90" \
  "$ABI_DIR/b2c_real32_negative.o" >"$ABI_DIR/negative.log" 2>&1
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: REAL32 terminal ABI compiled" >&2
  exit 1
fi
if ! rg -qi 'type mismatch.*real\(4\).*real\(8\)|real\(4\).*real\(8\)' \
  "$ABI_DIR/negative.log"
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: missing REAL32 ABI diagnostic" >&2
  sed -n '1,80p' "$ABI_DIR/negative.log" >&2
  exit 1
fi
echo "SPOR64 PHASE-A9b-B2c ABI PASS"

SYN_DIR="$BUILD_DIR/synthetic"
mkdir -p "$SYN_DIR"
compile_free "$HERE/b2c_synthetic_publication.f90" "$SYN_DIR/state.o"
compile_free "$HERE/b2c_synthetic_publication_driver.f90" "$SYN_DIR/driver.o"
"$FC" -O0 -g -fcheck=all -fbacktrace "$SYN_DIR/state.o" \
  "$SYN_DIR/driver.o" -o "$SYN_DIR/b2c_state_machine"
if nm -g "$SYN_DIR/b2c_state_machine" | \
  rg -qi 'xdrta2|flu2dr|doorfv|mccgf|lcmput|lcmpdl|dragon'
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: state machine linked production work" >&2
  exit 1
fi
for scenario in wrong-token collision-spot collision-sour collision-aflux \
  collision-dflux collision-adflux nan-flux inf-source over-positive \
  over-negative boundary normal
do
  "$SYN_DIR/b2c_state_machine" "$scenario" >"$SYN_DIR/$scenario.log" 2>&1
  if ! rg -q "^B2C-SYNTHETIC-PASS $scenario$" "$SYN_DIR/$scenario.log"
  then
    echo "SPOR64 PHASE-A9b-B2c FAILURE: state-machine case $scenario" >&2
    sed -n '1,80p' "$SYN_DIR/$scenario.log" >&2
    exit 1
  fi
done
echo "SPOR64 PHASE-A9b-B2c STATE-MACHINE PASS"

HARNESS_DIR="$BUILD_DIR/publisher-harness"
mkdir -p "$HARNESS_DIR"
compile_free "$HERE/test_b2c_production_publisher.f90" "$HARNESS_DIR/harness.o"
"$FC" -O0 -g -fcheck=all -fbacktrace \
  "$PROD_DIR/SPOR64_B2C.o" "$HARNESS_DIR/harness.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$HARNESS_DIR/b2c_publisher_harness"
if nm -g "$HARNESS_DIR/b2c_publisher_harness" | \
  rg -qi 'xdrta2|flu2dr|doorfv|mccgf|dragon'
then
  echo "SPOR64 PHASE-A9b-B2c FAILURE: publisher harness linked solver/transport" >&2
  exit 1
fi
for scenario in valid wrong-token existing-spot nan range
do
  "$HARNESS_DIR/b2c_publisher_harness" "$scenario" \
    >"$HARNESS_DIR/$scenario.log" 2>&1
  if ! rg -q "^B2C-PRODUCTION-PUBLISHER-PASS $scenario$" \
    "$HARNESS_DIR/$scenario.log"
  then
    echo "SPOR64 PHASE-A9b-B2c FAILURE: publisher case $scenario" >&2
    sed -n '1,120p' "$HARNESS_DIR/$scenario.log" >&2
    exit 1
  fi
done
echo "SPOR64 PHASE-A9b-B2c PRODUCTION-PUBLISHER SYNTHETIC PASS"

cd "$ROOT"
PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a9b_b2c_publication_contract

echo "SPOR64 PHASE-A9b-B2c PUBLICATION PASS"
echo "SPOR64 PHASE-A9b-B2c MUTATION-TESTS=151"
echo "SPOR64 PHASE-A9b-B2c POSITIVE-ABI-COMPILES=1 NEGATIVE-ABI-COMPILES=1"
echo "SPOR64 PHASE-A9b-B2c VALIDATION-STATE-MACHINE-EXECUTIONS=12"
echo "SPOR64 PHASE-A9b-B2c PRODUCTION-PUBLISHER-SYNTHETIC-EXECUTIONS=5"
echo "SPOR64 PHASE-A9b-B2c PRODUCTION-SOLVER-EXECUTIONS=0"
echo "SPOR64 PHASE-A9b-B2c TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A9b-B2c RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A9b-B2c OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
