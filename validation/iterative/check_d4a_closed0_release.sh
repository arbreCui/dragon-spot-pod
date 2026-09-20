#!/bin/sh
set -eu

# Check the corrected CLOSED/0 release boundary and print its exact SHA-256
# inventory.  This script never copies, changes or executes the payload.

fail() {
  echo "D4A CLOSED0 RELEASE FAIL: $*" >&2
  exit 2
}

EXPECTED_DRAGON_SHA=2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db
EXPECTED_DLIB_SHA=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9

hash() {
  shasum -a 256 "$1" | awk '{print $1}'
}

release_files() {
  directory=$1
  {
    printf '%s\n' rnr_cc.c2m rnr_interpol.c2m \
      admitted_snapshot_archive.sha256 d4a_rank2_admitted.sha256 \
      d4a_bootstrap_result.sha256
    for receipt in admitted_snapshot_archive.sha256 \
      d4a_rank2_admitted.sha256 d4a_bootstrap_result.sha256
    do
      awk '{print $2}' "$directory/$receipt"
    done
  } | LC_ALL=C sort -u
}

if [ "${1:-}" = --verify ]; then
  test "$#" -eq 2 || fail "usage: $0 --verify release-directory"
  test -d "$2" && test ! -L "$2" || fail "release must be a regular directory"
  RELEASE=$(CDPATH= cd -- "$2" && pwd -P)
  MANIFEST=$RELEASE/d4a_closed0_release.sha256
  test -f "$MANIFEST" && test ! -L "$MANIFEST" ||
    fail "release manifest must be a regular file"
  for receipt in admitted_snapshot_archive.sha256 d4a_rank2_admitted.sha256 \
    d4a_bootstrap_result.sha256
  do
    test -f "$RELEASE/$receipt" && test ! -L "$RELEASE/$receipt" ||
      fail "release is missing regular $receipt"
  done
  if grep -Eqv '^[0-9a-f]{64}  [A-Za-z0-9_.-]+$' "$MANIFEST"; then
    fail "release manifest contains a non-local or malformed entry"
  fi
  test "$(wc -l < "$MANIFEST" | tr -d ' ')" -eq 38 ||
    fail "release manifest does not contain exactly 38 payload files"
  EXPECTED_NAMES=$(
    { release_files "$RELEASE"; printf '%s\n' Dragon; } | LC_ALL=C sort
  )
  ACTUAL_NAMES=$(awk '{print $2}' "$MANIFEST" | LC_ALL=C sort)
  test "$ACTUAL_NAMES" = "$EXPECTED_NAMES" ||
    fail "release manifest has the wrong payload inventory"
  test -z "$(find "$RELEASE" -type l -print -quit)" ||
    fail "release contains a symbolic link"
  for name in $EXPECTED_NAMES; do
    test -f "$RELEASE/$name" && test ! -L "$RELEASE/$name" ||
      fail "release is missing regular $name"
  done
  EXPECTED_DIRECTORY=$(
    { printf '%s\n' "$EXPECTED_NAMES"; printf '%s\n' d4a_closed0_release.sha256; } |
      LC_ALL=C sort
  )
  ACTUAL_DIRECTORY=$(
    find "$RELEASE" -mindepth 1 -maxdepth 1 -type f -exec basename {} \; |
      LC_ALL=C sort
  )
  test "$ACTUAL_DIRECTORY" = "$EXPECTED_DIRECTORY" ||
    fail "release directory contains a missing or extra top-level file"
  test -z "$(find "$RELEASE" -mindepth 1 -maxdepth 1 ! -type f -print -quit)" ||
    fail "release directory contains a non-regular top-level entry"
  test -x "$RELEASE/Dragon" || fail "canonical Dragon is not executable"
  (cd "$RELEASE" && shasum -a 256 -c d4a_closed0_release.sha256 >/dev/null) ||
    fail "release manifest does not verify"
  echo "D4A CLOSED0 RELEASE VERIFY PASS: 38 regular payload files" >&2
  exit 0
fi

test "$#" -eq 2 || {
  echo "usage: $0 corrected-closed0-directory canonical-Dragon" >&2
  echo "       $0 --verify release-directory" >&2
  exit 2
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)
test -d "$1" && test ! -L "$1" || fail "bundle must be a regular directory"
BUNDLE=$(CDPATH= cd -- "$1" && pwd -P)
DRAGON=$2
test -f "$DRAGON" && test ! -L "$DRAGON" && test -x "$DRAGON" ||
  fail "canonical Dragon must be an executable regular file"

test "$(hash "$DRAGON")" = "$EXPECTED_DRAGON_SHA" ||
  fail "canonical Dragon content hash differs"

# The source archive has one machine-local link.  It was consumed only by the
# completed snapshot-generation lane; its executed hash remains provenance.
link_count=$(find "$BUNDLE" -type l | wc -l | tr -d ' ')
test "$link_count" -eq 1 || fail "expected exactly one symlink in the bundle"
DLIB="$BUNDLE/DLIB8R1_370"
test -L "$DLIB" || fail "the unique symlink is not DLIB8R1_370"
case "$(readlink "$DLIB")" in
  /*) ;;
  *) fail "DLIB8R1_370 is not an absolute provenance link" ;;
esac
test -f "$DLIB" || fail "DLIB8R1_370 target is unavailable"
test "$(hash "$DLIB")" = "$EXPECTED_DLIB_SHA" ||
  fail "DLIB8R1_370 content hash differs"
test "$(grep -Fxc "$EXPECTED_DLIB_SHA  DLIB8R1_370" \
  "$BUNDLE/executed_inputs.sha256" 2>/dev/null || true)" -eq 1 ||
  fail "executed_inputs.sha256 does not seal DLIB8R1_370 exactly once"

for receipt in "$BUNDLE"/*.sha256; do
  test "$(basename -- "$receipt")" = executed_inputs.sha256 && continue
  if grep -Eq 'DLIB8R1_370|DLIB_370' "$receipt"; then
    fail "$(basename -- "$receipt") unexpectedly names the upstream DLIB"
  fi
done

for receipt in admitted_snapshot_archive.sha256 d4a_rank2_admitted.sha256 \
  d4a_bootstrap_result.sha256
do
  test -s "$BUNDLE/$receipt" && test ! -L "$BUNDLE/$receipt" ||
    fail "missing regular $receipt"
  (cd "$BUNDLE" && shasum -a 256 -c "$receipt" >/dev/null) ||
    fail "$receipt does not verify"
done

# Guard the audited boundary: snapshot generation consumes the DLIB; the
# admitted bootstrap, Picard map, portable freezer and acceptance do not.
grep -q 'DLIB8R1_370' "$ROOT/validation/iterative/run_d4a_three_snapshots.sh" ||
  fail "snapshot runner no longer declares the upstream DLIB input"
for route in \
  run_d4a_rank2_bootstrap.sh \
  run_d4a_rank2_picard_map.sh \
  resume_d4a_rank2_picard_after_radial.sh \
  freeze_d4a_corrected_map.sh \
  check_d4a_corrected_acceptance.sh \
  run_d4a_corrected_final_observables.sh \
  verify_d4a_corrected_observables.sh
do
  test -f "$ROOT/validation/iterative/$route" || fail "missing route $route"
  if grep -Eq 'DLIB8R1_370|DLIB_370' \
    "$ROOT/validation/iterative/$route"
  then
    fail "$route now reads or names the upstream DLIB"
  fi
done

# The exact runtime payload is the union of the three verified receipts plus
# their receipt files and the two material inputs read directly by acceptance.
# Duplicate byte-identical aliases may be archive hard links; none are made
# here.  Dragon is supplied separately because it is outside Git.
RELEASE_FILES=$(release_files "$BUNDLE")
test "$(printf '%s\n' "$RELEASE_FILES" | wc -l | tr -d ' ')" -eq 37 ||
  fail "release payload inventory is not the canonical 37 data files"

for name in $RELEASE_FILES; do
  case "$name" in ''|*/*) fail "non-local release name: $name" ;; esac
  test -f "$BUNDLE/$name" && test ! -L "$BUNDLE/$name" ||
    fail "release payload is missing regular $name"
done

for name in $RELEASE_FILES; do
  shasum -a 256 "$BUNDLE/$name" |
    awk -v name="$name" '{print $1 "  " name}'
done
printf '%s  Dragon\n' "$EXPECTED_DRAGON_SHA"

echo "D4A CLOSED0 RELEASE PASS: 38 regular files; DLIB is provenance-only" >&2
