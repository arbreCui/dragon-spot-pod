#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/src/Dragon"}
WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-d4-density.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

fail() {
  echo "D4-A MATERIAL EPOCH FAIL: $*" >&2
  exit 1
}

test -x "$DRAGON_BIN" || fail "Dragon executable is missing: $DRAGON_BIN"
test "$(sha256sum "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" | awk '{print $1}')" = \
  594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5 ||
  fail "rnr_cc.c2m is not the reviewed physical version"
test "$(sha256sum "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" | awk '{print $1}')" = \
  255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2 ||
  fail "rnr_interpol.c2m is not the reviewed physical version"

cp "$ROOT/validation/d4_reference/d4a_material_density_audit.x2m" "$WORK/audit.x2m"
ln -s "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$WORK/rnr_cc.c2m"
ln -s "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$WORK/rnr_interpol.c2m"
(
  cd "$WORK"
  "$DRAGON_BIN" < audit.x2m > audit.log 2>&1
) || fail "density-only Dragon execution failed"

for anchor in \
  "N_Na=  2.237345e-02" \
  "N_U8=  1.881861e-02" \
  "N_Pu39=  2.747854e-03" \
  "N_O=  4.719196e-02" \
  "N_Fe56_AIM1=  5.000890e-02"
do
  grep -Fq "$anchor" "$WORK/audit.log" || fail "missing reviewed anchor: $anchor"
done
grep -Fq "D4A-NDENS-END" "$WORK/audit.log" || fail "density audit did not terminate"

echo "D4-A MATERIAL EPOCH PASS"
echo "STATE C: fuel=750 clad=620 sodium=475"
echo "NDENS: Na=2.237345e-02 U8=1.881861e-02 Pu39=2.747854e-03 O=4.719196e-02 Fe56_AIM1=5.000890e-02"
echo "NO LIBRARY OR TRANSPORT EXECUTED"
