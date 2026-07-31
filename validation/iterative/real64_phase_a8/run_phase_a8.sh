#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a8"
A7_RECEIPT="$ROOT/validation/iterative/real64_phase_a7/phase_a7_implementation_receipt.sha256"
A6_RECEIPT="$ROOT/validation/iterative/real64_phase_a6/phase_a6_implementation_receipt.sha256"
RECEIPT="$HERE/phase_a8_implementation_receipt.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-real64-phase-a8.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

FC=${FC:-gfortran}
LC_ALL=C
export LC_ALL
EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
FC_BANNER=$("$FC" --version | sed -n '1p')
if test "$FC_BANNER" != "$EXPECTED_FC_BANNER"
then
  echo "SPOR64 PHASE-A8 FAILURE: unaudited compiler identity" >&2
  exit 1
fi
if test "$(uname -s)" != Darwin || test "$(uname -m)" != arm64
then
  echo "SPOR64 PHASE-A8 FAILURE: unaudited platform identity" >&2
  exit 1
fi

CHECKED_FLAGS="-O0 -g -std=f2008 -pedantic-errors -Wall -Wextra -Werror"
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

expect_compile_failure()
{
  source_file=$1
  object_file=$2
  log_file=$3
  diagnostic_pattern=$4
  if compile_checked "$source_file" "$object_file" >"$log_file" 2>&1
  then
    echo "SPOR64 PHASE-A8 FAILURE: negative fixture compiled: $source_file" >&2
    exit 1
  fi
  if ! rg -qi "$diagnostic_pattern" "$log_file"
  then
    echo "SPOR64 PHASE-A8 FAILURE: expected diagnostic missing: $source_file" >&2
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
    echo "SPOR64 PHASE-A8 FAILURE: unclassified global nm line: $1" >&2
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
echo "SPOR64 PHASE-A8 RECEIPT PASS"

A7_RECEIPT_SHA256=$(shasum -a 256 "$A7_RECEIPT" | awk '{print $1}')
A6_RECEIPT_SHA256=$(shasum -a 256 "$A6_RECEIPT" | awk '{print $1}')
if test "$A7_RECEIPT_SHA256" != \
  c744a413f1b75d23ed0f9344a31d3269c4f76051af54e7e4100f3f808d8093e1
then
  echo "SPOR64 PHASE-A8 FAILURE: frozen A7 receipt identity changed" >&2
  exit 1
fi
if test "$A6_RECEIPT_SHA256" != \
  d250afba106b0cc55bb77abd78157ffd856f77ecbb1e40a618902633813a0958
then
  echo "SPOR64 PHASE-A8 FAILURE: frozen A6 receipt identity changed" >&2
  exit 1
fi
echo "SPOR64 PHASE-A8 FROZEN PREREQUISITE RECEIPT IDENTITIES PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a8.py"

compile_checked "$HERE/SPOR64_A8_ACA.f90" "$BUILD_DIR/SPOR64_A8_ACA.o"
compile_checked "$HERE/SPOR64_A8.f90" "$BUILD_DIR/SPOR64_A8.o"
compile_checked "$HERE/MCGFFIR64_RANK_ADAPTER.f90" \
  "$BUILD_DIR/MCGFFIR64_RANK_ADAPTER.o"
compile_checked "$HERE/compile_spor64_a8_anchor.f90" \
  "$BUILD_DIR/compile_spor64_a8_anchor.o"

expect_compile_failure "$HERE/compile_fail_real32_mutable_tail.f90" \
  "$BUILD_DIR/fail_real32_mutable.o" "$BUILD_DIR/fail_real32_mutable.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_real64_operator.f90" \
  "$BUILD_DIR/fail_real64_operator.o" "$BUILD_DIR/fail_real64_operator.log" \
  'type mismatch.*real\(8\).*real\(4\)'
expect_compile_failure "$HERE/compile_fail_noncontiguous_mutable.f90" \
  "$BUILD_DIR/fail_noncontiguous.o" "$BUILD_DIR/fail_noncontiguous.log" \
  'array temporary|noncontiguous|contiguous'
expect_compile_failure "$HERE/compile_fail_keyflx_rank.f90" \
  "$BUILD_DIR/fail_keyflx_rank.o" "$BUILD_DIR/fail_keyflx_rank.log" \
  'rank mismatch'
expect_compile_failure "$HERE/compile_fail_flat_pjjind.f90" \
  "$BUILD_DIR/fail_flat_pjjind.o" "$BUILD_DIR/fail_flat_pjjind.log" \
  'rank mismatch'
expect_compile_failure "$HERE/compile_fail_real32_capture.f90" \
  "$BUILD_DIR/fail_real32_capture.o" "$BUILD_DIR/fail_real32_capture.log" \
  'type mismatch.*real\(4\).*real\(8\)'
expect_compile_failure "$HERE/compile_fail_cf_n1_not_lc.f90" \
  "$BUILD_DIR/fail_cf_extent.o" "$BUILD_DIR/fail_cf_extent.log" \
  'too few elements|actual argument'
expect_compile_failure "$HERE/compile_fail_im_n_not_nplus1.f90" \
  "$BUILD_DIR/fail_im_extent.o" "$BUILD_DIR/fail_im_extent.log" \
  'too few elements|actual argument'
expect_compile_failure "$HERE/compile_fail_int32_cutoff.f90" \
  "$BUILD_DIR/fail_int32_cutoff.o" "$BUILD_DIR/fail_int32_cutoff.log" \
  'type mismatch.*integer\(4\).*integer\(8\)'

DEFAULT_REAL8_DIR="$BUILD_DIR/default-real8"
mkdir -p "$DEFAULT_REAL8_DIR"
for source_stem in SPOR64_A8_ACA SPOR64_A8 MCGFFIR64_RANK_ADAPTER
do
  if "$FC" -std=f2008 -fdefault-real-8 -J"$DEFAULT_REAL8_DIR" \
    -I"$BUILD_DIR" \
    -c "$HERE/$source_stem.f90" \
    -o "$DEFAULT_REAL8_DIR/$source_stem.o" \
    >"$DEFAULT_REAL8_DIR/$source_stem.log" 2>&1
  then
    echo "SPOR64 PHASE-A8 FAILURE: default REAL promotion compiled: $source_stem" >&2
    exit 1
  fi
  if ! rg -q "Division by zero" \
    "$DEFAULT_REAL8_DIR/$source_stem.log"
  then
    echo "SPOR64 PHASE-A8 FAILURE: kind guard did not reject: $source_stem" >&2
    exit 1
  fi
done

for source in MCGSIG MOCIK3 MCGFCF MCGFFIR MCGFFAR MCGFFAL MCGSCA MCGFST
do
  compile_legacy "$ROOT/src/$source.f" "$BUILD_DIR/$source.o"
done
for source in PRINAM MSRLUS1 DDOT
do
  compile_legacy "$ROOT/Utilib/src/$source.f" "$BUILD_DIR/$source.o"
done

capture_nm "$BUILD_DIR/SPOR64_A8.o" "$BUILD_DIR/a8_nm.txt"
capture_nm "$BUILD_DIR/SPOR64_A8_ACA.o" "$BUILD_DIR/aca_nm.txt"
capture_nm "$BUILD_DIR/MCGFFIR64_RANK_ADAPTER.o" \
  "$BUILD_DIR/adapter_nm.txt"
capture_nm "$BUILD_DIR/compile_spor64_a8_anchor.o" \
  "$BUILD_DIR/anchor_nm.txt"
audit_nm_lines "$BUILD_DIR/a8_nm.txt"
audit_nm_lines "$BUILD_DIR/aca_nm.txt"
audit_nm_lines "$BUILD_DIR/adapter_nm.txt"
audit_nm_lines "$BUILD_DIR/anchor_nm.txt"

extract_unresolved "$BUILD_DIR/a8_nm.txt" "$BUILD_DIR/a8_unresolved.txt"
extract_unresolved "$BUILD_DIR/aca_nm.txt" "$BUILD_DIR/aca_unresolved.txt"
extract_unresolved "$BUILD_DIR/adapter_nm.txt" \
  "$BUILD_DIR/adapter_unresolved.txt"
extract_unresolved "$BUILD_DIR/anchor_nm.txt" \
  "$BUILD_DIR/anchor_unresolved.txt"
extract_defined "$BUILD_DIR/a8_nm.txt" "$BUILD_DIR/a8_defined.txt"
extract_defined "$BUILD_DIR/aca_nm.txt" "$BUILD_DIR/aca_defined.txt"
extract_defined "$BUILD_DIR/adapter_nm.txt" "$BUILD_DIR/adapter_defined.txt"
extract_defined "$BUILD_DIR/anchor_nm.txt" "$BUILD_DIR/anchor_defined.txt"

for stem in a8_unresolved aca_unresolved adapter_unresolved \
  anchor_unresolved a8_defined aca_defined adapter_defined anchor_defined
do
  if ! cmp -s "$HERE/expected_${stem}.txt" "$BUILD_DIR/${stem}.txt"
  then
    echo "SPOR64 PHASE-A8 FAILURE: exact symbol inventory changed: $stem" >&2
    diff -u "$HERE/expected_${stem}.txt" "$BUILD_DIR/${stem}.txt" >&2 || true
    exit 1
  fi
done

nm -g "$BUILD_DIR/SPOR64_A8.o" "$BUILD_DIR/SPOR64_A8_ACA.o" \
  "$BUILD_DIR/MCGFFIR64_RANK_ADAPTER.o" \
  "$BUILD_DIR/compile_spor64_a8_anchor.o" >"$BUILD_DIR/a8_all_nm.txt"
if rg -i '(^|[[:space:]])(_?main|MAIN__)(_|$)' "$BUILD_DIR/a8_all_nm.txt"
then
  echo "SPOR64 PHASE-A8 FAILURE: executable entry point present" >&2
  exit 1
fi
if rg -i '(^|[[:space:]])_?(prinam|mcgpra|spomoc_capture)_$' \
  "$BUILD_DIR/a8_nm.txt" "$BUILD_DIR/aca_nm.txt"
then
  echo "SPOR64 PHASE-A8 FAILURE: forbidden legacy symbol present" >&2
  exit 1
fi
if rg -i '__spor64_a[1-7]_MOD_' \
  "$BUILD_DIR/a8_nm.txt" "$BUILD_DIR/aca_nm.txt"
then
  echo "SPOR64 PHASE-A8 FAILURE: dependency on earlier validation module" >&2
  exit 1
fi

PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_phase_a8_contract

echo "SPOR64 PHASE-A8 COMPILE-ONLY INNER CLOSURE PASS"
echo "SPOR64 PHASE-A8 OBJECT-LINKS=0 EXECUTABLES=0 OBJECT-EXECUTIONS=0"
echo "SPOR64 PHASE-A8 PREREQUISITE-RUNNERS=0 SYNTHETIC-EXECUTIONS=0"
echo "SPOR64 PHASE-A8 TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0"
