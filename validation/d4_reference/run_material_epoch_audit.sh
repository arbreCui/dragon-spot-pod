#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CANONICAL_DRAGON="$ROOT/bin/Darwin_arm64/Dragon"
DRAGON_BIN=${DRAGON_BIN:-"$CANONICAL_DRAGON"}
PYTHON=${OPENMC_PYTHON:-python3}
WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-d4-density.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

fail() {
  echo "D4-A MATERIAL EPOCH FAIL: $*" >&2
  exit 1
}

test -x "$DRAGON_BIN" || fail "Dragon executable is missing: $DRAGON_BIN"
test "$DRAGON_BIN" = "$CANONICAL_DRAGON" || fail "only canonical Dragon is admitted"
test "$(shasum -a 256 "$DRAGON_BIN" | awk '{print $1}')" = \
  2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db ||
  fail "canonical Dragon identity changed"
"$PYTHON" -c 'import openmc' || fail "set OPENMC_PYTHON to the existing OpenMC Python"
test "$(sha256sum "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" | awk '{print $1}')" = \
  594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5 ||
  fail "rnr_cc.c2m is not the reviewed physical version"
test "$(sha256sum "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" | awk '{print $1}')" = \
  255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2 ||
  fail "rnr_interpol.c2m is not the reviewed physical version"

cp "$ROOT/validation/d4_reference/d4a_material_density_audit.x2m" "$WORK/audit.x2m"
ln -s "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$WORK/rnr_cc.c2m"
ln -s "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$WORK/rnr_interpol.c2m"
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  "$PYTHON" -c 'import sys; from pathlib import Path; import run_bounded_dragon as bounded; bounded.TERM_GRACE_SECONDS=0.0; bounded.run(*(Path(p) for p in sys.argv[1:]), timeout_seconds=10.0)' \
  "$DRAGON_BIN" "$WORK/audit.x2m" "$WORK/audit.log" || {
    tail -n 30 "$WORK/audit.log" >&2
    fail "density-only Dragon execution failed (10-second hard cap)"
  }
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
  "$ROOT/validation/d4_reference/compare_d4a_material_density.py" "$WORK/audit.log" ||
  fail "density inventory, legacy anchors, or CE formula check failed"
test "$(shasum -a 256 "$DRAGON_BIN" | awk '{print $1}')" = \
  2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db ||
  fail "canonical Dragon identity changed during audit"

echo "D4-A MATERIAL EPOCH PASS"
echo "STATE C: fuel=650,750,850 clad=620 sodium=475"
echo "NDENS: Na=2.237345e-02 U8=1.881861e-02 Pu39=2.747854e-03 O=4.719196e-02 Fe56_AIM1=5.000890e-02"
echo "NO LIBRARY OR TRANSPORT EXECUTED"
echo "PASS SCOPE: complete density inventory and unchanged legacy anchors; CE differences are reported-only"
