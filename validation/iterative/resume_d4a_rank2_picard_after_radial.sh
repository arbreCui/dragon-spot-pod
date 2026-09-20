#!/bin/sh
set -eu

# Resume one corrected D4-A rank-two Picard map after its radial half-step has
# completed and been admitted.  The radial solve is never repeated here.

fail() {
  echo "resume_d4a_rank2_picard_after_radial: $*" >&2
  exit 2
}

exact_line() {
  file=$1
  expected=$2
  test "$(wc -l < "$file" | tr -d ' ')" = 1 &&
    test "$(cat "$file")" = "$expected"
}

if [ "$#" -ne 2 ]; then
  echo "usage: AXIAL_TIMEOUT_SECONDS=seconds $0 completed-radial-directory fresh-output-directory" >&2
  exit 2
fi
: "${AXIAL_TIMEOUT_SECONDS:?set an explicit bounded wall time for the axial half-step}"
case "$AXIAL_TIMEOUT_SECONDS" in
  ''|*[!0-9]*) fail "AXIAL_TIMEOUT_SECONDS must be a positive integer" ;;
  0) fail "AXIAL_TIMEOUT_SECONDS must be positive" ;;
esac

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd -P)
TOOLS=$HERE
DRAGON="$ROOT/bin/Darwin_arm64/Dragon"

test -d "$1" && test ! -L "$1" ||
  fail "radial source must be a regular directory"
RADIAL=$(CDPATH= cd -- "$1" && pwd -P)

UPSTREAM_NAMES='parent_axial_closed.xsm
parent_snapshots_closed.xsm
initial_radial_track.bin
initial_axial_track.xsm
initial_axial_macrolib.xsm
basis_reference.xsm
route_contract.xsm
projected_proposal.xsm
SpotStepR64.c2m
radial.x2m
prepare.log
radial.runner.log
radial.log
admission.log
candidate_system.xsm
candidate_radial.xsm'

# The seven parent inputs are symlinks in the normal one-map runner.  They may
# remain links here, but every link must resolve to a regular file.
PARENT_NAMES='parent_axial_closed.xsm
parent_snapshots_closed.xsm
initial_radial_track.bin
initial_axial_track.xsm
initial_axial_macrolib.xsm
basis_reference.xsm
route_contract.xsm'
for name in $PARENT_NAMES; do
  test -f "$RADIAL/$name" || fail "missing radial input: $RADIAL/$name"
done

# All products and text receipts created inside the radial work directory must
# be ordinary files.  This prevents a substituted log or candidate archive
# from being admitted through an external link.
RADIAL_REGULAR_NAMES='projected_proposal.xsm
SpotStepR64.c2m
radial.x2m
prepare.log
radial.runner.log
radial.log
admission.log
candidate_system.xsm
candidate_radial.xsm'
for name in $RADIAL_REGULAR_NAMES; do
  test -f "$RADIAL/$name" && test ! -L "$RADIAL/$name" ||
    fail "missing regular radial product: $RADIAL/$name"
done

RUNNER_PASS='RAW-MOC-CAPTURE PROCESS PASS'
ADMISSION_PASS='H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=3'
PREPARE_END='SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT'
exact_line "$RADIAL/radial.runner.log" "$RUNNER_PASS" ||
  fail "radial.runner.log is not the exact PASS receipt"
exact_line "$RADIAL/admission.log" "$ADMISSION_PASS" ||
  fail "admission.log is not the exact STATUS=3 receipt"
test "$(grep -Ec '^>\|D4A-PICARD-RADIAL-COMPLETE' \
  "$RADIAL/radial.log" || true)" = 1 ||
  fail "radial.log has no unique D4A-PICARD-RADIAL-COMPLETE terminus"
test "$(grep -Fc 'normal end of execution for dragon' "$RADIAL/radial.log" || true)" = 1 ||
  fail "radial.log has no unique normal Dragon end"
test "$(grep -Fxc "$PREPARE_END" "$RADIAL/prepare.log" || true)" = 1 &&
  test "$(tail -n 1 "$RADIAL/prepare.log")" = "$PREPARE_END" ||
  fail "prepare.log has no unique canonical terminus"
test "$(grep -Ec '^SPOT-R64 B2J CLOSED/[0-9]+ -> PROJECTED/[0-9]+$' \
  "$RADIAL/prepare.log" || true)" = 1 ||
  fail "prepare.log has no unique CLOSED-to-PROJECTED epoch receipt"
if test "$(grep -Fxc 'SPOT-R64 B2J CLOSED/0 -> PROJECTED/1' \
  "$RADIAL/prepare.log" || true)" = 1; then
  CHECK_MODE=--reencoded
else
  CHECK_MODE=--continued
fi

WORK_ARG=$2
test ! -e "$WORK_ARG" && test ! -L "$WORK_ARG" ||
  fail "output directory must be fresh: $WORK_ARG"
mkdir -p "$(dirname -- "$WORK_ARG")"
WORK_PARENT=$(CDPATH= cd -- "$(dirname -- "$WORK_ARG")" && pwd -P)
WORK="$WORK_PARENT/$(basename -- "$WORK_ARG")"
case "$WORK/" in
  "$RADIAL/"*) fail "output directory cannot be inside the radial source" ;;
esac
mkdir "$WORK"

for name in $PARENT_NAMES; do
  ln -s "$RADIAL/$name" "$WORK/$name"
done
COPY_NAMES='projected_proposal.xsm
SpotStepR64.c2m
radial.x2m
prepare.log
radial.runner.log
radial.log
admission.log
candidate_system.xsm
candidate_radial.xsm'
for name in $COPY_NAMES; do
  cp "$RADIAL/$name" "$WORK/$name"
done

printf 'UPSTREAM_RADIAL_DIRECTORY=%s\n' "$RADIAL" \
  > "$WORK/upstream_radial_source.txt"
(
  cd "$RADIAL"
  shasum -a 256 $UPSTREAM_NAMES
) > "$WORK/upstream_radial_manifest.sha256"
(
  cd "$RADIAL"
  shasum -a 256 -c "$WORK/upstream_radial_manifest.sha256" >/dev/null
) || fail "upstream radial files changed while their receipt was created"
(
  cd "$WORK"
  shasum -a 256 -c upstream_radial_manifest.sha256 >/dev/null
) || fail "staged radial files do not match the upstream receipt"

for name in d4a_rank2_picard_axial.x2m d4a_rank2_checker_parent.x2m; do
  test -f "$TOOLS/$name" && test ! -L "$TOOLS/$name" ||
    fail "missing current checkout deck: $TOOLS/$name"
done
cp "$TOOLS/d4a_rank2_picard_axial.x2m" "$WORK/axial.x2m"
cp "$TOOLS/d4a_rank2_checker_parent.x2m" "$WORK/checker_parent.x2m"
(
  cd "$WORK"
  shasum -a 256 axial.x2m checker_parent.x2m
) > "$WORK/recovery_decks.sha256"

make -C "$ROOT/src" -j2 >/dev/null
make -C "$TOOLS" -j2 >/dev/null
test -f "$DRAGON" && test ! -L "$DRAGON" && test -x "$DRAGON" ||
  fail "missing current Dragon executable: $DRAGON"
for tool in admit_candidate_radial close_r64_returned check_one_map_xsm \
  check_convergence_gate
do
  test -f "$TOOLS/$tool" && test ! -L "$TOOLS/$tool" &&
    test -x "$TOOLS/$tool" || fail "missing executable tool: $TOOLS/$tool"
done
test -f "$TOOLS/run_bounded_dragon.py" &&
  test ! -L "$TOOLS/run_bounded_dragon.py" ||
  fail "missing bounded Dragon runner"

cd "$WORK"
"$TOOLS/admit_candidate_radial" \
  candidate_radial.xsm route_contract.xsm > admission.replay.log
exact_line admission.replay.log "$ADMISSION_PASS" ||
  fail "replayed radial admission did not return STATUS=3"
cmp -s admission.log admission.replay.log ||
  fail "replayed radial admission differs from the upstream receipt"

OMP_NUM_THREADS=1 python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/axial.x2m" "$WORK/axial.log" \
  "$AXIAL_TIMEOUT_SECONDS" > axial.runner.log
exact_line axial.runner.log "$RUNNER_PASS" ||
  fail "axial.runner.log is not the exact PASS receipt"
test "$(grep -Ec '^>\|D4A-PICARD-AXIAL-COMPLETE' axial.log || true)" = 1 ||
  fail "axial.log has no unique D4A-PICARD-AXIAL-COMPLETE terminus"
test "$(grep -Fc 'normal end of execution for dragon' axial.log || true)" = 1 ||
  fail "axial.log has no unique normal Dragon end"
for name in candidate_axial.xsm candidate_snapshots.xsm; do
  test -s "$name" && test ! -L "$name" ||
    fail "missing regular axial product: $name"
done

"$TOOLS/close_r64_returned" \
  candidate_axial.xsm candidate_snapshots.xsm route_contract.xsm \
  closed_axial.xsm closed_snapshots.xsm > close.log
for name in closed_axial.xsm closed_snapshots.xsm; do
  test -s "$name" && test ! -L "$name" ||
    fail "missing regular closed product: $name"
done

python3 "$TOOLS/run_bounded_dragon.py" \
  "$DRAGON" "$WORK/checker_parent.x2m" "$WORK/checker_parent.log" 5 \
  > checker_parent.runner.log
exact_line checker_parent.runner.log "$RUNNER_PASS" ||
  fail "checker_parent.runner.log is not the exact PASS receipt"
test -s parent_for_checker.xsm && test ! -L parent_for_checker.xsm ||
  fail "checker parent was not produced"

"$TOOLS/check_one_map_xsm" "$CHECK_MODE" \
  basis_reference.xsm candidate_system.xsm parent_for_checker.xsm \
  candidate_axial.xsm candidate_snapshots.xsm > independent_check.log
test "$(grep -Fxc 'ONE-MAP-XSM COMPLETE' independent_check.log || true)" = 1 ||
  fail "independent one-map check has no unique complete terminus"
"$TOOLS/check_convergence_gate" closed_axial.xsm > gate.log
test "$(grep -Ec '^CLASSIFICATION=VALID_(MET|NOT_MET)$' gate.log || true)" = 1 ||
  fail "convergence gate has no valid classification"
test "$(grep -Fxc 'SPOT-GATE COMPLETE' gate.log || true)" = 1 &&
  test "$(tail -n 1 gate.log)" = 'SPOT-GATE COMPLETE' ||
  fail "convergence gate has no unique complete terminus"

# The axial half-step must not alter any accepted radial input or product.
shasum -a 256 -c upstream_radial_manifest.sha256 >/dev/null ||
  fail "an accepted radial file changed during axial recovery"
shasum -a 256 -c recovery_decks.sha256 >/dev/null ||
  fail "a recovery deck changed during axial recovery"

shasum -a 256 \
  parent_axial_closed.xsm parent_snapshots_closed.xsm \
  initial_radial_track.bin initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
  projected_proposal.xsm > input_manifest.sha256
shasum -a 256 \
  candidate_system.xsm candidate_radial.xsm candidate_axial.xsm \
  candidate_snapshots.xsm closed_axial.xsm closed_snapshots.xsm \
  > output_manifest.sha256

cat independent_check.log
cat gate.log
echo "D4A RANK-2 PICARD AXIAL RECOVERY COMPLETE: $WORK"
