#!/bin/sh
set -eu

# Copy one completed corrected D4-A map into a fresh, self-contained directory.
# This is packaging only: the seven map-parent links are copied by value and
# every regular file is sealed in result.sha256.

fail() {
  echo "freeze_d4a_corrected_map: $*" >&2
  exit 2
}

RUNTIME=
REPAIRED_DRAGON_SHA=873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef
REPAIRED_RUNTIME_SHA=8888d5772c39472fe4d4895120737370fd471200c4ace9e7bf41ed8c7e74db1b
REPAIRED_BOOTSTRAP_SHA=acab72a87521339f9eb0540130d0fc4ea1946b59df6bb5db4fcb83cd3528eb1c
MESH12_RUNTIME_SHA=af7069315a59ae6de9c0bd3edd6f497bf4dcaef1140917b4239c32bcff8da12b
MESH12_BOOTSTRAP_SHA=805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f
hash() { shasum -a 256 "$1" | awk '{print $1}'; }
if [ "${1:-}" = --repaired-runtime ]; then
  [ "$#" -ge 2 ] || fail "missing repaired runtime directory"
  RUNTIME=$(CDPATH= cd -- "$2" && pwd -P) || fail "repaired runtime is missing"
  shift 2
fi
if [ "$#" -ne 3 ]; then
  echo "usage: $0 [--repaired-runtime directory] corrected-bootstrap-directory completed-map-directory fresh-portable-directory" >&2
  exit 2
fi

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
CHECKER_DIR=$HERE
if [ -n "$RUNTIME" ]; then
  # Preserve the old epoch; select the new runtime and seed only as a pair.
  if [ "$(hash "$RUNTIME/runtime.sha256")" = "$MESH12_RUNTIME_SHA" ]; then
    REPAIRED_RUNTIME_SHA=$MESH12_RUNTIME_SHA
    REPAIRED_BOOTSTRAP_SHA=$MESH12_BOOTSTRAP_SHA
  fi
  test "$(hash "$RUNTIME/runtime.sha256")" = "$REPAIRED_RUNTIME_SHA" ||
    fail "repaired runtime manifest identity differs"
  (cd "$RUNTIME" && shasum -a 256 -c runtime.sha256 >/dev/null) ||
    fail "repaired runtime does not verify"
  test "$(hash "$RUNTIME/Dragon")" = "$REPAIRED_DRAGON_SHA" ||
    fail "repaired Dragon identity differs"
  CHECKER_DIR=$RUNTIME
fi
test -d "$CHECKER_DIR" && test ! -L "$CHECKER_DIR" ||
  fail "CHECKER_DIR must be a regular directory"
CHECKER_DIR=$(CDPATH= cd -- "$CHECKER_DIR" && pwd -P)
for checker in check_one_map_xsm check_convergence_gate; do
  test -f "$CHECKER_DIR/$checker" && test ! -L "$CHECKER_DIR/$checker" &&
    test -x "$CHECKER_DIR/$checker" || fail "missing executable $checker"
done

test -d "$1" && test ! -L "$1" ||
  fail "corrected build must be a regular directory"
BUILD=$(CDPATH= cd -- "$1" && pwd -P)

# The bootstrap receipt is the corrected-lineage authority. Check it before
# reading any claim made by the completed map.
BOOTSTRAP_RECEIPT=d4a_bootstrap_result.sha256
if [ -n "$RUNTIME" ]; then
  BOOTSTRAP_RECEIPT=result.sha256
  test "$(hash "$BUILD/$BOOTSTRAP_RECEIPT")" = "$REPAIRED_BOOTSTRAP_SHA" ||
    fail "repaired bootstrap identity differs"
fi
test -f "$BUILD/$BOOTSTRAP_RECEIPT" && test ! -L "$BUILD/$BOOTSTRAP_RECEIPT" ||
  fail "corrected bootstrap receipt is missing or a symlink"
BOOTSTRAP_NAMES='d4a_seed_axial.xsm
d4a_seed_snapshots.xsm
initial_radial_track.bin
initial_axial_track.xsm
initial_axial_macrolib.xsm
basis_reference.xsm
route_contract.xsm
d4a_refreshed_snapshots.xsm
closed_axial.xsm
closed_snapshots.xsm
d4a_axial_seed.log
d4a_refresh_r64.log
route_contract.log
b2i_bootstrap.log'

manifest_names() {
  receipt=$1
  pattern='^[0-9a-f]{64}  [A-Za-z0-9_.-]+$'
  if [ "${2:-}" = repaired ]; then
    pattern='^[0-9a-f]{64}  (runtime/)?[A-Za-z0-9_.-]+$'
  fi
  LC_ALL=C grep -Eqv "$pattern" "$receipt" &&
    return 1
  sed -E 's/^[0-9a-f]{64}  //' "$receipt"
}

if [ -z "$RUNTIME" ]; then
  test "$(manifest_names "$BUILD/$BOOTSTRAP_RECEIPT")" = \
    "$BOOTSTRAP_NAMES" || fail "corrected bootstrap receipt has the wrong inventory"
fi
(cd "$BUILD" && shasum -a 256 -c "$BOOTSTRAP_RECEIPT" >/dev/null) ||
  fail "corrected bootstrap receipt does not verify"

test -d "$2" && test ! -L "$2" || fail "map source must be a regular directory"
SOURCE=$(CDPATH= cd -- "$2" && pwd -P)
test "$SOURCE" != "$BUILD" || fail "corrected build and map source must differ"
if [ -n "$RUNTIME" ]; then
  test -f "$SOURCE/result.sha256" && test ! -L "$SOURCE/result.sha256" ||
    fail "repaired source has no regular result manifest"
  names=$(manifest_names "$SOURCE/result.sha256" repaired) ||
    fail "repaired source manifest contains unsupported paths"
  actual=$(cd "$SOURCE" && find . \( -type f -o -type l \) ! -path ./result.sha256 -print |
    sed 's|^./||' | LC_ALL=C sort)
  test "$actual" = "$(printf '%s\n' "$names" | LC_ALL=C sort)" ||
    fail "repaired source inventory differs from its manifest"
  test "$(find "$SOURCE" -mindepth 1 -type d -print)" = "$SOURCE/runtime" ||
    fail "repaired source must contain only the runtime subdirectory"
  test "$(hash "$SOURCE/runtime/runtime.sha256")" = "$REPAIRED_RUNTIME_SHA" ||
    fail "source belongs to a different runtime"
  (cd "$SOURCE" && shasum -a 256 -c result.sha256 >/dev/null) &&
    (cd "$SOURCE/runtime" && shasum -a 256 -c runtime.sha256 >/dev/null) ||
    fail "repaired source receipt does not verify"
fi
DEST_ARG=$3
test ! -e "$DEST_ARG" && test ! -L "$DEST_ARG" || fail "output must be fresh"
if [ -n "$RUNTIME" ]; then
  # Resolve before creating parents: rejecting a destination must not add
  # even an empty directory beneath sealed inputs or the running runtime.
  prospective=$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve())' "$DEST_ARG")
  case "$prospective/" in "$SOURCE/"*|"$BUILD/"*|"$RUNTIME/"*)
    fail "output cannot be inside an input directory" ;;
  esac
fi
mkdir -p "$(dirname -- "$DEST_ARG")"
DEST_PARENT=$(CDPATH= cd -- "$(dirname -- "$DEST_ARG")" && pwd -P)
DEST="$DEST_PARENT/$(basename -- "$DEST_ARG")"
case "$DEST/" in "$SOURCE/"*|"$BUILD/"*)
  fail "output cannot be inside an input directory" ;;
esac

INPUT_NAMES='parent_axial_closed.xsm
parent_snapshots_closed.xsm
initial_radial_track.bin
initial_axial_track.xsm
initial_axial_macrolib.xsm
basis_reference.xsm
route_contract.xsm
projected_proposal.xsm'
OUTPUT_NAMES='candidate_system.xsm
candidate_radial.xsm
candidate_axial.xsm
candidate_snapshots.xsm
closed_axial.xsm
closed_snapshots.xsm'

for receipt in input_manifest.sha256 output_manifest.sha256; do
  test -f "$SOURCE/$receipt" && test ! -L "$SOURCE/$receipt" ||
    fail "missing regular $receipt"
done
test "$(manifest_names "$SOURCE/input_manifest.sha256")" = "$INPUT_NAMES" ||
  fail "input_manifest.sha256 must contain exactly the eight canonical inputs"
test "$(manifest_names "$SOURCE/output_manifest.sha256")" = "$OUTPUT_NAMES" ||
  fail "output_manifest.sha256 must contain exactly the six canonical outputs"
for receipt in input_manifest.sha256 output_manifest.sha256; do
  (cd "$SOURCE" && shasum -a 256 -c "$receipt" >/dev/null) ||
    fail "$receipt does not verify"
done

for log in independent_check.log gate.log; do
  test -f "$SOURCE/$log" && test ! -L "$SOURCE/$log" ||
    fail "missing regular $log"
done
test -f "$SOURCE/parent_for_checker.xsm" &&
  test ! -L "$SOURCE/parent_for_checker.xsm" ||
  fail "missing regular parent_for_checker.xsm"
for line in \
  'ONE-MAP-XSM POD-PACKAGE BITWISE PASS' \
  'ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS' \
  'ONE-MAP-XSM RAW-RADIAL-POSITIVITY PASS' \
  'ONE-MAP-XSM CANONICAL-LAYOUT BITWISE PASS' \
  'ONE-MAP-XSM RAW-DEFECT BITWISE PASS' \
  'ONE-MAP-XSM RESTART-ARCHIVE BITWISE PASS'
do
  test "$(grep -Fxc "$line" "$SOURCE/independent_check.log")" -eq 1 ||
    fail "independent check is incomplete: $line"
done
test "$(grep -Fxc 'ONE-MAP-XSM COMPLETE' "$SOURCE/independent_check.log")" -eq 1 &&
  test "$(tail -n 1 "$SOURCE/independent_check.log")" = 'ONE-MAP-XSM COMPLETE' ||
  fail "independent check has no complete terminus"

for prefix in 'SPOT-GATE THRESHOLD ' 'SPOT-GATE RRHO ' \
  'SPOT-GATE RLEAK ' 'SPOT-GATE RA ' 'SPOT-GATE DLEAK ' \
  'GATE=(Rrho,RL,Ra) '
do
  test "$(grep -c "^$prefix" "$SOURCE/gate.log")" -eq 1 ||
    fail "convergence gate is incomplete: $prefix"
done
classification_count=$(grep -Ec '^CLASSIFICATION=VALID_(MET|NOT_MET)$' \
  "$SOURCE/gate.log" || true)
test "$classification_count" -eq 1 || fail "convergence classification is not unique"
CLASSIFICATION=$(grep -E '^CLASSIFICATION=VALID_(MET|NOT_MET)$' \
  "$SOURCE/gate.log")
test "$(grep -Fxc 'SPOT-GATE COMPLETE' "$SOURCE/gate.log")" -eq 1 &&
  test "$(tail -n 1 "$SOURCE/gate.log")" = 'SPOT-GATE COMPLETE' ||
  fail "convergence gate has no complete terminus"

test -f "$SOURCE/prepare.log" && test ! -L "$SOURCE/prepare.log" ||
  fail "missing regular prepare.log"
test "$(grep -Ec '^SPOT-R64 B2J CLOSED/[0-9]+ -> PROJECTED/[0-9]+$' \
  "$SOURCE/prepare.log" || true)" -eq 1 ||
  fail "prepare.log has no unique CLOSED-to-PROJECTED epoch receipt"
if test "$(grep -Fxc 'SPOT-R64 B2J CLOSED/0 -> PROJECTED/1' \
  "$SOURCE/prepare.log" || true)" -eq 1; then
  CHECK_MODE=--reencoded
else
  CHECK_MODE=--continued
fi

# Do not trust copied text receipts. Re-read the XSM state with the same two
# independent checkers used by the map runner, and require byte-identical logs.
VERIFY=$(mktemp -d "${TMPDIR:-/tmp}/d4a-freezer-check.XXXXXX") ||
  fail "cannot create checker scratch directory"
STAGE=
cleanup() {
  test -z "$VERIFY" || rm -rf "$VERIFY"
  test -z "$STAGE" || rm -rf "$STAGE"
}
trap cleanup EXIT HUP INT TERM
(
  cd "$SOURCE"
  "$CHECKER_DIR/check_one_map_xsm" "$CHECK_MODE" \
    basis_reference.xsm candidate_system.xsm parent_for_checker.xsm \
    candidate_axial.xsm candidate_snapshots.xsm \
    > "$VERIFY/independent_check.log"
) || fail "independent XSM recheck rejected the map"
cmp -s "$VERIFY/independent_check.log" "$SOURCE/independent_check.log" ||
  fail "independent_check.log does not match the XSM recheck"
(
  cd "$SOURCE"
  "$CHECKER_DIR/check_convergence_gate" closed_axial.xsm \
    > "$VERIFY/gate.log"
) || fail "convergence XSM recheck rejected the map"
cmp -s "$VERIFY/gate.log" "$SOURCE/gate.log" ||
  fail "gate.log does not match the XSM recheck"

for log in prepare.log admission.log close.log; do
  test -f "$SOURCE/$log" && test ! -L "$SOURCE/$log" ||
    fail "missing regular $log"
done
PREPARE_END='SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT'
ADMISSION_END='H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=3'
test "$(grep -Fxc "$PREPARE_END" "$SOURCE/prepare.log")" -eq 1 &&
  test "$(tail -n 1 "$SOURCE/prepare.log")" = "$PREPARE_END" ||
  fail "prepare.log has no unique canonical terminus"
test "$(grep -Fxc "$ADMISSION_END" "$SOURCE/admission.log")" -eq 1 &&
  test "$(tail -n 1 "$SOURCE/admission.log")" = "$ADMISSION_END" ||
  fail "admission.log has no unique canonical terminus"
test "$(grep -Ec '^SPOT-R64 CLOSED/[0-9]+ COMPLETE NO-TRANSPORT$' \
  "$SOURCE/close.log")" -eq 1 &&
  tail -n 1 "$SOURCE/close.log" |
    grep -Eq '^SPOT-R64 CLOSED/[0-9]+ COMPLETE NO-TRANSPORT$' ||
  fail "close.log has no unique canonical terminus"

# These five inputs define the fixed corrected route. A self-consistent map
# receipt is not sufficient: every byte must also match the admitted build.
FIXED_INPUTS='initial_radial_track.bin
initial_axial_track.xsm
initial_axial_macrolib.xsm
basis_reference.xsm
route_contract.xsm'
for name in $FIXED_INPUTS; do
  test -f "$BUILD/$name" && test ! -L "$BUILD/$name" ||
    fail "corrected build has no regular $name"
  cmp -s "$SOURCE/$name" "$BUILD/$name" ||
    fail "$name does not match the corrected build"
done

if [ -z "$RUNTIME" ]; then
  test ! -e "$SOURCE/result.sha256" || fail "source is already frozen"
fi
test ! -e "$SOURCE/source_result.sha256" || fail "source is already a portable copy"
test ! -e "$SOURCE/symlink_provenance.tsv" || fail "source already has link provenance"
test ! -e "$SOURCE/portable_classification.txt" ||
  fail "source already has a portable classification"

INPUT_LINKS='parent_axial_closed.xsm
parent_snapshots_closed.xsm
initial_radial_track.bin
initial_axial_track.xsm
initial_axial_macrolib.xsm
basis_reference.xsm
route_contract.xsm'

link_count=$(find "$SOURCE" -type l | wc -l | tr -d ' ')
test "$link_count" -eq 7 || fail "expected exactly seven input symlinks"
for name in $INPUT_LINKS; do
  test -L "$SOURCE/$name" || fail "$name is not an input symlink"
  target=$(readlink "$SOURCE/$name")
  case "$target" in /*) ;; *) fail "$name is not an absolute symlink" ;; esac
  test -f "$SOURCE/$name" || fail "$name has no regular resolved source"
done

STAGE=$(mktemp -d "$DEST.tmp.XXXXXX") || fail "cannot create staging directory"
cp -R "$SOURCE/." "$STAGE/"
if [ -n "$RUNTIME" ]; then
  # Preserve the original map receipt byte-for-byte. The new outer receipt
  # additionally seals materialized links and the portable classification.
  cp "$SOURCE/result.sha256" "$STAGE/source_result.sha256"
fi
printf 'name\timmediate_target\tresolved_source\n' > "$STAGE/symlink_provenance.tsv"

for name in $INPUT_LINKS; do
  target=$(readlink "$SOURCE/$name")
  resolved=$(realpath "$SOURCE/$name")
  before=$(shasum -a 256 "$SOURCE/$name" | awk '{print $1}')
  cp "$SOURCE/$name" "$STAGE/$name.materialized"
  rm "$STAGE/$name"
  mv "$STAGE/$name.materialized" "$STAGE/$name"
  after=$(shasum -a 256 "$STAGE/$name" | awk '{print $1}')
  test "$before" = "$after" || fail "$name changed while materializing"
  printf '%s\t%s\t%s\n' "$name" "$target" "$resolved" \
    >> "$STAGE/symlink_provenance.tsv"
done

case "$CLASSIFICATION" in
  CLASSIFICATION=VALID_MET)
    printf '%s\n%s\n' \
      'MAP_CLASSIFICATION=VALID_MET' \
      'PORTABLE_ROLE=CONVERGED_MAP' > "$STAGE/portable_classification.txt"
    ROLE=CONVERGED_MAP
    ;;
  CLASSIFICATION=VALID_NOT_MET)
    printf '%s\n%s\n%s\n' \
      'MAP_CLASSIFICATION=VALID_NOT_MET' \
      'PORTABLE_ROLE=NEXT_MAP_PARENT_ONLY' \
      'FINAL_CONVERGENCE=NOT_CLAIMED' > "$STAGE/portable_classification.txt"
    ROLE=NEXT_MAP_PARENT_ONLY
    ;;
  *) fail "internal classification error" ;;
esac

test -z "$(find "$STAGE" -type l -print -quit)" ||
  fail "a symlink remains in the portable copy"
(cd "$STAGE" && shasum -a 256 -c input_manifest.sha256 >/dev/null &&
  shasum -a 256 -c output_manifest.sha256 >/dev/null) ||
  fail "copied map no longer matches its original receipts"
for name in $FIXED_INPUTS; do
  cmp -s "$STAGE/$name" "$BUILD/$name" ||
    fail "$name changed while packaging"
done
if [ -n "$RUNTIME" ]; then
  (cd "$SOURCE" && shasum -a 256 -c result.sha256 >/dev/null) &&
    (cd "$STAGE" && shasum -a 256 -c source_result.sha256 >/dev/null) &&
    (cd "$BUILD" && shasum -a 256 -c result.sha256 >/dev/null) &&
    (cd "$RUNTIME" && shasum -a 256 -c runtime.sha256 >/dev/null) ||
    fail "repaired source, copied payload or pinned inputs changed during packaging"
fi
(cd "$STAGE" &&
  find . -type f ! -name result.sha256 -print | LC_ALL=C sort |
    while IFS= read -r file; do shasum -a 256 "${file#./}"; done > result.sha256 &&
  shasum -a 256 -c result.sha256 >/dev/null) ||
  fail "portable receipt verification failed"

mv "$STAGE" "$DEST"
STAGE=
rm -rf "$VERIFY"
VERIFY=
trap - EXIT HUP INT TERM
echo "D4A CORRECTED MAP PORTABLE PASS: $CLASSIFICATION ROLE=$ROLE PATH=$DEST"
