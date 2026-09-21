#!/bin/sh
set -eu

# Thin serial owner for the corrected D4-A direct-Picard route.  It owns no
# physics or solver controls: one-map evaluation and portable admission remain
# delegated to the existing audited programs beside this script.

fail() {
  echo "D4A PICARD SERIES FAIL: $*" >&2
  exit 2
}

verify_portable_parent() {
  python3 - "$1" <<'PY'
from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys


root = Path(sys.argv[1])
required = {
    "portable_classification.txt",
    "closed_axial.xsm",
    "closed_snapshots.xsm",
    "gate.log",
    "prepare.log",
    "admission.log",
    "close.log",
    "independent_check.log",
    "input_manifest.sha256",
    "output_manifest.sha256",
}


def reject(message: str) -> None:
    print(f"portable parent reject: {message}", file=sys.stderr)
    raise SystemExit(1)


try:
    children = list(root.iterdir())
except OSError as exc:
    reject(f"cannot inspect directory: {exc}")
for child in children:
    if child.is_symlink():
        reject(f"symbolic link present: {child.name}")
    if not child.is_file():
        reject(f"non-regular entry present: {child.name}")

receipt = root / "result.sha256"
if not receipt.is_file() or receipt.is_symlink():
    reject("result.sha256 is not a regular file")
try:
    lines = receipt.read_text(encoding="ascii").splitlines()
except (OSError, UnicodeError) as exc:
    reject(f"cannot read result.sha256: {exc}")
if not lines:
    reject("result.sha256 is empty")

entries: dict[str, str] = {}
for line in lines:
    match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
    if match is None:
        reject("malformed result.sha256 line")
    expected, raw_name = match.groups()
    relative = Path(raw_name)
    name = relative.name
    if (
        relative.is_absolute()
        or name in {"", ".", ".."}
        or raw_name not in {name, f"./{name}"}
    ):
        reject(f"unsafe receipt path: {raw_name}")
    if name == "result.sha256" or name in entries:
        reject(f"duplicate or recursive receipt entry: {name}")
    target = root / name
    if not target.is_file() or target.is_symlink():
        reject(f"receipt entry is not a regular file: {name}")
    digest = hashlib.sha256()
    try:
        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        reject(f"cannot hash {name}: {exc}")
    if digest.hexdigest() != expected:
        reject(f"receipt hash mismatch: {name}")
    entries[name] = expected

inventory = {child.name for child in children}
if inventory != set(entries) | {"result.sha256"}:
    reject("receipt entries do not exactly match the directory inventory")
missing = sorted(required - set(entries))
if missing:
    reject("receipt omits required evidence: " + ", ".join(missing))
PY
}

if [ "$#" -ne 4 ]; then
  echo "usage: $0 corrected-build initial-parent fresh-output-root max-maps" >&2
  exit 2
fi

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
RUN_ONE="$HERE/run_d4a_rank2_picard_map.sh"
FREEZE="$HERE/freeze_d4a_corrected_map.sh"

for tool in "$RUN_ONE" "$FREEZE"; do
  test -f "$tool" && test ! -L "$tool" && test -x "$tool" ||
    fail "missing regular executable: $tool"
done

: "${RADIAL_TIMEOUT_SECONDS:?set an explicit bounded radial wall time}"
: "${AXIAL_TIMEOUT_SECONDS:?set an explicit bounded axial wall time}"

BUILD_ARG=$1
PARENT_ARG=$2
OUTPUT_ARG=$3
MAX_MAPS=$4

case "$MAX_MAPS" in
  ''|*[!0-9]*|0) fail "max-maps must be a positive integer" ;;
esac

test -d "$BUILD_ARG" && test ! -L "$BUILD_ARG" ||
  fail "corrected build must be a regular directory"
BUILD=$(CDPATH= cd -- "$BUILD_ARG" && pwd -P)
test -f "$BUILD/d4a_bootstrap_result.sha256" &&
  test ! -L "$BUILD/d4a_bootstrap_result.sha256" ||
  fail "corrected build is missing regular d4a_bootstrap_result.sha256"
(cd "$BUILD" && shasum -a 256 -c d4a_bootstrap_result.sha256 >/dev/null) ||
  fail "corrected build bootstrap receipt does not verify"

test -d "$PARENT_ARG" && test ! -L "$PARENT_ARG" ||
  fail "initial parent must be a regular directory"
PARENT=$(CDPATH= cd -- "$PARENT_ARG" && pwd -P)

# A series may start only at the admitted bootstrap or at a frozen,
# unconverged map.  Raw map directories are deliberately not restart inputs.
if [ "$PARENT" = "$BUILD" ]; then
  :
else
  test -f "$PARENT/result.sha256" && test ! -L "$PARENT/result.sha256" ||
    fail "non-bootstrap parent is not a portable map"
  verify_portable_parent "$PARENT" ||
    fail "portable parent inventory or receipt is invalid"
  test -f "$PARENT/portable_classification.txt" &&
    test ! -L "$PARENT/portable_classification.txt" ||
    fail "portable parent has no regular classification"
  EXPECTED_PARENT=$(printf '%s\n%s\n%s' \
    'MAP_CLASSIFICATION=VALID_NOT_MET' \
    'PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY' \
    'FINAL_CONVERGENCE=NOT_CLAIMED')
  test "$(cat "$PARENT/portable_classification.txt")" = "$EXPECTED_PARENT" ||
    fail "portable parent is not NEXT_MAP_PARENT_ONLY"
fi

for name in closed_axial.xsm closed_snapshots.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm
do
  test -f "$PARENT/$name" && test ! -L "$PARENT/$name" ||
    fail "initial parent is missing regular $name"
done
for name in initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm
do
  test -f "$BUILD/$name" && test ! -L "$BUILD/$name" ||
    fail "corrected build is missing regular $name"
  cmp -s "$PARENT/$name" "$BUILD/$name" ||
    fail "initial parent $name differs from the corrected build"
done

test ! -e "$OUTPUT_ARG" && test ! -L "$OUTPUT_ARG" ||
  fail "output root must be fresh"
OUTPUT=$(python3 - "$OUTPUT_ARG" <<'PY'
import os
import sys

print(os.path.realpath(os.path.abspath(sys.argv[1])))
PY
) || fail "cannot normalize output root"
case "$OUTPUT" in
  "$BUILD"|"$BUILD"/*)
    fail "output root cannot be the corrected build or lie inside it" ;;
esac
case "$BUILD" in
  "$OUTPUT"|"$OUTPUT"/*)
    fail "output root cannot contain the corrected build" ;;
esac
case "$OUTPUT" in
  "$PARENT"|"$PARENT"/*)
    fail "output root cannot be the initial parent or lie inside it" ;;
esac
case "$PARENT" in
  "$OUTPUT"|"$OUTPUT"/*)
    fail "output root cannot contain the initial parent" ;;
esac

test ! -e "$OUTPUT" && test ! -L "$OUTPUT" ||
  fail "output root must be fresh"
mkdir -p "$(dirname -- "$OUTPUT")"
mkdir "$OUTPUT"
OUTPUT=$(CDPATH= cd -- "$OUTPUT" && pwd -P)
printf 'step\tepoch\tclassification\traw\tportable\n' \
  > "$OUTPUT/picard_series.tsv"

step=1
while [ "$step" -le "$MAX_MAPS" ]; do
  tag=$(printf '%03d' "$step")
  RAW="$OUTPUT/map-$tag.raw"
  PORTABLE="$OUTPUT/map-$tag.portable"
  test ! -e "$RAW" && test ! -L "$RAW" ||
    fail "raw map path is not fresh: $RAW"
  test ! -e "$PORTABLE" && test ! -L "$PORTABLE" ||
    fail "portable map path is not fresh: $PORTABLE"

  echo "D4A PICARD SERIES MAP START: step=$step parent=$PARENT raw=$RAW"
  "$RUN_ONE" "$PARENT" "$RAW"

  for log in prepare.log close.log; do
    test -f "$RAW/$log" && test ! -L "$RAW/$log" ||
      fail "one-map runner produced no regular $log at step $step"
  done
  PREPARE_COUNT=$(grep -Ec \
    '^SPOT-R64 B2J CLOSED/(0|[1-9][0-9]*) -> PROJECTED/(0|[1-9][0-9]*)$' \
    "$RAW/prepare.log" || true)
  test "$PREPARE_COUNT" -eq 1 ||
    fail "step $step has $PREPARE_COUNT canonical prepare epochs"
  PREPARE_EPOCHS=$(sed -nE \
    's#^SPOT-R64 B2J CLOSED/(0|[1-9][0-9]*) -> PROJECTED/(0|[1-9][0-9]*)$#\1 \2#p' \
    "$RAW/prepare.log")
  CLOSED_EPOCH=${PREPARE_EPOCHS%% *}
  PROJECTED_EPOCH=${PREPARE_EPOCHS#* }
  test "$PROJECTED_EPOCH" -eq $((CLOSED_EPOCH + 1)) ||
    fail "step $step prepare epoch is not CLOSED/n -> PROJECTED/n+1"

  CLOSE_COUNT=$(grep -Ec \
    '^SPOT-R64 CLOSED/(0|[1-9][0-9]*) COMPLETE NO-TRANSPORT$' \
    "$RAW/close.log" || true)
  test "$CLOSE_COUNT" -eq 1 ||
    fail "step $step has $CLOSE_COUNT canonical close epochs"
  CLOSE_EPOCH=$(sed -nE \
    's#^SPOT-R64 CLOSED/(0|[1-9][0-9]*) COMPLETE NO-TRANSPORT$#\1#p' \
    "$RAW/close.log")
  test "$CLOSE_EPOCH" -eq "$PROJECTED_EPOCH" ||
    fail "step $step close epoch differs from projected epoch"

  test -f "$RAW/gate.log" && test ! -L "$RAW/gate.log" ||
    fail "one-map runner produced no regular gate.log at step $step"
  CLASS_COUNT=$(grep -c '^CLASSIFICATION=' "$RAW/gate.log" || true)
  CANONICAL_CLASS_COUNT=$(grep -Ec '^CLASSIFICATION=VALID_(MET|NOT_MET)$' \
    "$RAW/gate.log" || true)
  test "$CLASS_COUNT" -eq 1 && test "$CANONICAL_CLASS_COUNT" -eq 1 ||
    fail "step $step has $CLASS_COUNT classification lines and "\
"$CANONICAL_CLASS_COUNT canonical classifications"
  test "$(grep -Fxc 'SPOT-GATE COMPLETE' "$RAW/gate.log" || true)" -eq 1 &&
    test "$(tail -n 1 "$RAW/gate.log")" = 'SPOT-GATE COMPLETE' ||
    fail "step $step has no unique canonical gate terminus"
  CLASSIFICATION=$(grep -E '^CLASSIFICATION=VALID_(MET|NOT_MET)$' \
    "$RAW/gate.log")

  "$FREEZE" "$BUILD" "$RAW" "$PORTABLE"
  test -d "$PORTABLE" && test ! -L "$PORTABLE" ||
    fail "freezer produced no regular portable directory at step $step"
  test -f "$PORTABLE/result.sha256" &&
    test ! -L "$PORTABLE/result.sha256" ||
    fail "portable map has no regular result receipt at step $step"
  (cd "$PORTABLE" && shasum -a 256 -c result.sha256 >/dev/null) ||
    fail "portable map receipt does not verify at step $step"
  test -z "$(find "$PORTABLE" -type l -print -quit)" ||
    fail "portable map contains a symbolic link at step $step"

  case "$CLASSIFICATION" in
    CLASSIFICATION=VALID_NOT_MET)
      EXPECTED_PORTABLE=$(printf '%s\n%s\n%s' \
        'MAP_CLASSIFICATION=VALID_NOT_MET' \
        'PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY' \
        'FINAL_CONVERGENCE=NOT_CLAIMED')
      ;;
    CLASSIFICATION=VALID_MET)
      EXPECTED_PORTABLE=$(printf '%s\n%s' \
        'MAP_CLASSIFICATION=VALID_MET' \
        'PORTABLE_ROLE=CONVERGED_MAP')
      ;;
    *) fail "internal classification error at step $step" ;;
  esac
  test -f "$PORTABLE/portable_classification.txt" &&
    test ! -L "$PORTABLE/portable_classification.txt" ||
    fail "portable map has no regular classification at step $step"
  test "$(cat "$PORTABLE/portable_classification.txt")" = \
    "$EXPECTED_PORTABLE" ||
    fail "portable classification disagrees with raw gate at step $step"

  printf '%s\t%s\t%s\t%s\t%s\n' "$step" "$CLOSE_EPOCH" \
    "${CLASSIFICATION#CLASSIFICATION=}" "$RAW" "$PORTABLE" \
    >> "$OUTPUT/picard_series.tsv"

  if [ "$CLASSIFICATION" = 'CLASSIFICATION=VALID_MET' ]; then
    echo "D4A PICARD SERIES CONVERGED: step=$step portable=$PORTABLE"
    exit 0
  fi

  PARENT=$PORTABLE
  step=$((step + 1))
done

echo "D4A PICARD SERIES STOP: MAX_MAPS_REACHED=$MAX_MAPS "\
"NO_CONVERGENCE_CLAIM" >&2
exit 3
