#!/bin/sh
set -eu

# Replay the canonical read-only D4-A observables extraction and require the
# two scientific records to be byte-identical to the saved Dragon listing.
# The caller supplies already-declared SHA-256 values; production acceptance
# supplies only repository-fixed paths and the corrected-build Dragon hash.

PATH=/usr/bin:/bin:/usr/sbin:/sbin
export PATH

fail() {
  echo "D4A CORRECTED OBSERVABLE REPLAY FAIL: $*" >&2
  exit 1
}

hash() {
  shasum -a 256 "$1" | awk '{print $1}'
}

require_hash() {
  path=$1
  expected=$2
  label=$3
  test -f "$path" && test ! -L "$path" ||
    fail "$label is not a regular non-symlink file"
  test "$(hash "$path")" = "$expected" || fail "$label SHA-256 differs"
}

test "$#" -eq 7 || {
  echo "usage: $0 dragon dragon-sha deck deck-sha bounded-runner runner-sha observables-directory" >&2
  exit 2
}

DRAGON=$1
DRAGON_SHA=$2
DECK=$3
DECK_SHA=$4
RUNNER=$5
RUNNER_SHA=$6
OBSERVABLES=$7

for value in "$DRAGON_SHA" "$DECK_SHA" "$RUNNER_SHA"; do
  echo "$value" | grep -Eq '^[0-9a-f]{64}$' || fail "invalid SHA-256 declaration"
done
require_hash "$DRAGON" "$DRAGON_SHA" "canonical Dragon"
test -x "$DRAGON" || fail "canonical Dragon is not executable"
require_hash "$DECK" "$DECK_SHA" "canonical observables deck"
require_hash "$RUNNER" "$RUNNER_SHA" "canonical bounded runner"

test -d "$OBSERVABLES" && test ! -L "$OBSERVABLES" ||
  fail "observables directory is not a regular directory"
OBSERVABLES=$(CDPATH= cd -- "$OBSERVABLES" && pwd -P)
for name in closed_axial.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm observables.x2m observables.log
do
  test -f "$OBSERVABLES/$name" && test ! -L "$OBSERVABLES/$name" ||
    fail "$name is not a regular non-symlink file"
done
cmp -s "$OBSERVABLES/observables.x2m" "$DECK" ||
  fail "saved observables deck is not the canonical deck"

SCRATCH=$(mktemp -d "${TMPDIR:-/tmp}/d4a-observable-replay.XXXXXX") ||
  fail "cannot create replay scratch directory"
cleanup() {
  rm -rf "$SCRATCH"
}
trap cleanup EXIT HUP INT TERM

cp "$OBSERVABLES/closed_axial.xsm" "$SCRATCH/closed_axial.xsm"
cp "$OBSERVABLES/initial_axial_track.xsm" "$SCRATCH/initial_axial_track.xsm"
cp "$OBSERVABLES/initial_axial_macrolib.xsm" \
  "$SCRATCH/initial_axial_macrolib.xsm"
cp "$DECK" "$SCRATCH/observables.x2m"

OMP_NUM_THREADS=1 PYTHONPATH= PYTHONHOME= PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/python3 "$RUNNER" "$DRAGON" "$SCRATCH/observables.x2m" \
  "$SCRATCH/replayed.log" 10 >/dev/null ||
  fail "canonical read-only replay failed"

extract_records() {
  listing=$1
  output=$2
  test "$(grep -c '^>|D4A-CORRECTED-K-EFFECTIVE ' "$listing" || true)" -eq 1 ||
    fail "listing does not contain exactly one corrected k record"
  test "$(grep -c '^SPORATE NU-FISSION-FRACTIONS ' "$listing" || true)" -eq 1 ||
    fail "listing does not contain exactly one floor-power record"
  {
    grep '^>|D4A-CORRECTED-K-EFFECTIVE ' "$listing"
    grep '^SPORATE NU-FISSION-FRACTIONS ' "$listing"
  } > "$output"
}

extract_records "$OBSERVABLES/observables.log" "$SCRATCH/saved.records"
extract_records "$SCRATCH/replayed.log" "$SCRATCH/replayed.records"
cmp -s "$SCRATCH/saved.records" "$SCRATCH/replayed.records" ||
  fail "saved k/power records differ byte-for-byte from the sealed XSM replay"

echo "D4A CORRECTED OBSERVABLE REPLAY PASS: canonical k/power records are byte-identical"
