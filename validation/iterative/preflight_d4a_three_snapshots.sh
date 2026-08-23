#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRIVER="$ROOT/validation/iterative/d4a_three_snapshots.x2m"
BUILDER="$ROOT/data/SpotD4Snap.c2m"
MANIFEST="$ROOT/validation/iterative/d4a_snapshot_inputs.sha256"
DLIB370=${DLIB370:-/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell/DLIB_370}
EXPECTED_DLIB_SHA=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9

fail() {
  echo "D4A SNAPSHOT PREFLIGHT FAIL: $*" >&2
  exit 1
}

test -f "$DLIB370" || fail "370-group DLIB is missing: $DLIB370"
(
  cd "$ROOT"
  sha256sum -c "$MANIFEST"
) >/dev/null || fail "a frozen repository input changed"

test "$(grep -Fc ':= SpotD4Snap glow_rnr ::' "$DRIVER")" -eq 3 ||
  fail "the driver does not contain exactly three snapshot solves"
test "$(grep -Fc 'D4A-SNAPSHOT-STATE' "$DRIVER")" -eq 3 ||
  fail "the driver does not declare exactly three physical states"
grep -Fq 'ECHO "D4A-SNAPSHOT-STATE" 1 650.0 T_clad T_Na ;' "$DRIVER" ||
  fail "state 1 is not the frozen 650/620/475 C state"
grep -Fq 'ECHO "D4A-SNAPSHOT-STATE" 2 750.0 T_clad T_Na ;' "$DRIVER" ||
  fail "state 2 is not the frozen 750/620/475 C state"
grep -Fq 'ECHO "D4A-SNAPSHOT-STATE" 3 850.0 T_clad T_Na ;' "$DRIVER" ||
  fail "state 3 is not the frozen 850/620/475 C state"
grep -Fq 'REAL solver_eps := 5.0E-7 ;' "$DRIVER" ||
  fail "the strict snapshot solve tolerance changed"
grep -Fq 'SNAP := BACKUP: TRACK :: LIST 3 ITEM 1 ;' "$DRIVER" ||
  fail "the archive is not initialized with exactly three planes"
test "$(grep -c '^SNAP := BACKUP:' "$DRIVER")" -eq 12 ||
  fail "the archive does not contain four objects for each state"
for item in 1 2 3; do
  test "$(grep -Ec "ITEM $item ;$" "$DRIVER")" -eq 4 ||
    fail "snapshot $item does not contain TRACK/MICROLIB2/SYSTEM/FLUX"
done
grep -Fq 'SNAP_ARCH := SNAP ;' "$DRIVER" ||
  fail "the physical archive is not published"
if grep -Eqi 'eps_pod|rank_pod|SpotPod|SPOT:|SPOR64|Picard|Anderson|relax' "$DRIVER"; then
  fail "the offline snapshot deck contains POD, coupling or acceleration"
fi

grep -Fq 'NMIX 6' "$BUILDER" || fail "the D4-A builder is not six-medium"
test "$(grep -Fc 'TISO 24 50.0 LONG' "$BUILDER")" -eq 1 ||
  fail "the frozen historical TONE self-shielding quadrature changed"
test "$(grep -Fc 'TISO 24 100.0 LONG' "$BUILDER")" -eq 1 ||
  fail "the admitted production tracking discretization changed"
grep -Fq 'EDIT 1 MXIT 20 EPS 1.0E-5 TRAN PIJ ;' "$BUILDER" ||
  fail "TONE no longer uses its frozen criterion with an explicit terminal"
grep -Fq 'GAUS 4 AAC 80 TMT STIS 1 EPSI 1.0E-5 MCU 10000' "$BUILDER" ||
  fail "the admitted MCCG settings changed"
grep -Fq 'EDIT 0 TYPE K EXTE 500 <<solver_eps>>' "$BUILDER" ||
  fail "the radial eigenvalue solve is not strict and bounded"
grep -Fq 'UNKT <<solver_eps>> THER <<solver_eps>> ;' "$BUILDER" ||
  fail "the radial inner tolerances are not tied to solver_eps"
if grep -Eq 'EPSI[[:space:]]+1(E|\.0E)-6|EXTE[[:space:]]+30[[:space:]]+1\.0E-4' "$BUILDER"; then
  fail "a historical loose D4-A numerical setting returned"
fi

dlib_sha=$(sha256sum "$DLIB370" | awk '{print $1}')
test "$dlib_sha" = "$EXPECTED_DLIB_SHA" ||
  fail "the 370-group DLIB hash changed: $dlib_sha"

echo "D4A SNAPSHOT PREFLIGHT PASS"
echo "D4A PHYSICAL STATES C: (650,620,475) (750,620,475) (850,620,475)"
echo "D4A ARCHIVE: NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144"
echo "D4A DLIB SHA256=$dlib_sha"
echo "D4A TRANSPORT EXECUTED=0"
