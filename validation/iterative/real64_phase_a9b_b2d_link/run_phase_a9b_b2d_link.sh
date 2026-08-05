#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PARENT_RECEIPT="$ROOT/validation/iterative/real64_phase_a9b_b2c_publication/phase_a9b_b2c_publication_receipt.sha256"
RECEIPT="$HERE/phase_a9b_b2d_link_receipt.sha256"
FC=/opt/homebrew/bin/gfortran
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/spot-b2d-link.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

fail()
{
  printf '%s\n' "SPOR64 PHASE-A9b-B2d LINK FAILURE: $*" >&2
  exit 1
}

count_exact()
{
  expected=$1
  pattern=$2
  file=$3
  found=$(grep -c -E "$pattern" "$file" || true)
  [ "$found" -eq "$expected" ] || fail "$file: expected $expected matches for $pattern, found $found"
}

[ "$(uname -s)" = Darwin ] || fail "frozen platform is Darwin"
[ "$(uname -m)" = arm64 ] || fail "frozen architecture is arm64"
[ -x "$FC" ] || fail "frozen compiler missing: $FC"
"$FC" --version | grep -Fq 'GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0' || \
  fail "frozen compiler banner differs"

printf '%s  %s\n' \
  a8038df5630a348004861cdb3e92ee6d2b032ccc5271076b76158c37dffa8bd0 \
  "$PARENT_RECEIPT" | shasum -a 256 -c - >/dev/null || fail "parent receipt drift"
git -C "$ROOT" merge-base --is-ancestor \
  bf6cb73a93903772c3e7d39a95c1d0a7de7e58d8 HEAD || fail "B2c parent commit absent"

[ -f "$RECEIPT" ] || fail "B2d receipt missing"
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2d_link.py"

# Treat only the bridge source as newer while holding the generated dependency
# inventory fixed.  This forces one production bridge compile, archive update,
# and Dragon link without rewriting a frozen parent-receipt input.
if ! make -C "$ROOT/src" -o .dragon_deps.mk \
  -W SPOR64_GANLIB_ABI.f90 Dragon >"$BUILD_DIR/production-build.log" 2>&1; then
  sed -n '1,240p' "$BUILD_DIR/production-build.log" >&2
  fail "production Dragon build failed"
fi
sed -n '1,240p' "$BUILD_DIR/production-build.log"
count_exact 1 '(^|[[:space:]])-o Dragon$' "$BUILD_DIR/production-build.log"
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a9b_b2d_link.py"

DRAGON="$ROOT/bin/Darwin_arm64/Dragon"
[ -x "$DRAGON" ] || fail "production Dragon executable missing"

ar t "$ROOT/src/libDragon.a" >"$BUILD_DIR/archive.txt"
for object in SPOR64_A8.o SPOR64_B2B.o SPOR64_B2C.o SPOR64_GANLIB_ABI.o; do
  count_exact 1 "^${object}$" "$BUILD_DIR/archive.txt"
done

nm -g "$ROOT/src/SPOR64_A8.o" >"$BUILD_DIR/a8-symbols.txt"
for symbol in _lcmlen_ _lcmgpd_ _lcmgil_; do
  count_exact 1 " U ${symbol}$" "$BUILD_DIR/a8-symbols.txt"
done

nm -g "$ROOT/src/libDragon.a" >"$BUILD_DIR/archive-symbols.txt"
for symbol in _lcmlen_ _lcmgpd_ _lcmgil_; do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/archive-symbols.txt"
  count_exact 1 " U ${symbol}$" "$BUILD_DIR/archive-symbols.txt"
done

nm -g "$DRAGON" >"$BUILD_DIR/dragon-symbols.txt"
for symbol in \
  ___spor64_a8_MOD_doorfv64 \
  ___spor64_b2b_MOD_spor64_b2b_ingress \
  ___spor64_b2c_MOD_spor64_b2c_publish \
  _lcmlen_ _lcmgpd_ _lcmgil_; do
  count_exact 1 " T ${symbol}$" "$BUILD_DIR/dragon-symbols.txt"
done
nm -u "$DRAGON" >"$BUILD_DIR/dragon-unresolved.txt"
if grep -Eiq '(^|_)lcm(len|gpd|gil)_?$' "$BUILD_DIR/dragon-unresolved.txt"; then
  fail "Dragon retains an unresolved A8 GANLIB ABI symbol"
fi

STRICT_FLAGS='-std=f2008 -pedantic -Wall -Wextra -Werror -fimplicit-none -fcheck=all -ffpe-trap=invalid,zero,overflow'
"$FC" $STRICT_FLAGS \
  -I "$ROOT/Ganlib/lib/Darwin_arm64/modules" \
  -c "$ROOT/src/SPOR64_GANLIB_ABI.f90" \
  -o "$BUILD_DIR/bridge.o"

nm -g "$BUILD_DIR/bridge.o" | awk '$2 == "T" { print $2, $3 }' | \
  grep -E ' T? ?_lcm(len|gpd|gil)_$' | LC_ALL=C sort -k2 \
  >"$BUILD_DIR/bridge-defined.txt"
cmp "$HERE/expected_bridge_defined.txt" "$BUILD_DIR/bridge-defined.txt" || \
  fail "bridge definition inventory differs"
nm -u "$BUILD_DIR/bridge.o" | \
  grep -E '^___lcmaux_MOD_lcm(len|gpd|gil)$' | LC_ALL=C sort \
  >"$BUILD_DIR/bridge-unresolved.txt"
cmp "$HERE/expected_bridge_unresolved.txt" "$BUILD_DIR/bridge-unresolved.txt" || \
  fail "bridge forward-target inventory differs"

"$FC" $STRICT_FLAGS \
  -I "$ROOT/Ganlib/lib/Darwin_arm64/modules" \
  -c "$HERE/test_spor64_ganlib_abi.f90" \
  -o "$BUILD_DIR/harness.o"
"$FC" $STRICT_FLAGS \
  "$BUILD_DIR/bridge.o" \
  "$BUILD_DIR/harness.o" \
  "$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a" \
  "$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a" \
  -o "$BUILD_DIR/test_spor64_ganlib_abi"
"$BUILD_DIR/test_spor64_ganlib_abi" >"$BUILD_DIR/harness.log" 2>&1
count_exact 1 '^SPOR64 B2D GANLIB ABI PASS$' "$BUILD_DIR/harness.log"

nm -u "$BUILD_DIR/test_spor64_ganlib_abi" >"$BUILD_DIR/harness-unresolved.txt"
if grep -Eiq 'dragon|doorfv|mccgf|spomoc|tracking|transport' \
  "$BUILD_DIR/harness-unresolved.txt"; then
  fail "GANLIB-only harness acquired a solver dependency"
fi

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$HERE" \
  python3 -m unittest -v test_phase_a9b_b2d_link_contract

printf '%s\n' 'SPOR64 PHASE-A9b-B2d LINK PASS'
printf '%s\n' 'MUTATION-TESTS=12'
printf '%s\n' 'FULL-DRAGON-BUILDS=1 FULL-DRAGON-LINKS=1 DRAGON-EXECUTIONS=0'
printf '%s\n' 'GANLIB-BRIDGE-LINKS=1 GANLIB-BRIDGE-SYNTHETIC-EXECUTIONS=1'
printf '%s\n' 'RECEIPT-CHECKS=2'
printf '%s\n' 'TRACKING-READS=0 TRANSPORT-SOLVES=0'
printf '%s\n' 'RUNTIME-PROVENANCE=NOT-EVALUATED'
printf '%s\n' 'RADIAL-CONVERGENCE=NOT-EVALUATED'
printf '%s\n' 'OUTER-PICARD-CONVERGENCE=NOT-EVALUATED'
