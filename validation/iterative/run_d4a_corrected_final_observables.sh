#!/bin/sh
set -eu

# Extract only final k and globally normalized bottom/middle/top nu-fission
# production.  The accepted final CLOSED state is read but never modified.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DECK="$ROOT/validation/iterative/d4a_corrected_final_observables.x2m"
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
TIMEOUT_SECONDS=${TIMEOUT_SECONDS:-10}
BOUNDED_DIR="$ROOT/validation/iterative"
RUNTIME=
BOOTSTRAP_RECEIPT=d4a_bootstrap_result.sha256
REPAIRED_DRAGON_SHA=873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef
REPAIRED_RUNTIME_SHA=8888d5772c39472fe4d4895120737370fd471200c4ace9e7bf41ed8c7e74db1b
REPAIRED_BOOTSTRAP_SHA=acab72a87521339f9eb0540130d0fc4ea1946b59df6bb5db4fcb83cd3528eb1c
MESH12_RUNTIME_SHA=af7069315a59ae6de9c0bd3edd6f497bf4dcaef1140917b4239c32bcff8da12b
MESH12_BOOTSTRAP_SHA=805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f
OBSERVABLE_DECK_SHA=46a70e2e1ed83b37b03d6a472bf94224557119c358a27fdc1875115f0f569259

fail() {
  echo "D4A CORRECTED OBSERVABLES FAIL: $*" >&2
  exit 1
}

hash() {
  shasum -a 256 "$1" | awk '{print $1}'
}

same() {
  test -f "$1" && test -f "$2" && test "$(hash "$1")" = "$(hash "$2")"
}

if [ "${1:-}" = --repaired-runtime ]; then
  test "$#" -ge 2 || fail "--repaired-runtime requires a directory"
  RUNTIME=$(CDPATH= cd -- "$2" 2>/dev/null && pwd -P) || fail "repaired runtime is missing"
  test "$DRAGON_BIN" = "$ROOT/bin/Darwin_arm64/Dragon" ||
    fail "DRAGON_BIN override is not allowed with --repaired-runtime"
  DRAGON_BIN="$RUNTIME/Dragon"
  BOUNDED_DIR=$RUNTIME
  BOOTSTRAP_RECEIPT=result.sha256
  shift 2
fi

test "$#" -eq 3 || {
  echo "usage: $0 [--repaired-runtime directory] corrected-bootstrap final-map fresh-output-directory" >&2
  exit 2
}

BUILD=$(CDPATH= cd -- "$1" 2>/dev/null && pwd) || fail "corrected build is missing"
FINAL=$(CDPATH= cd -- "$2" 2>/dev/null && pwd) || fail "final map is missing"
OUTPUT=$3

test -x "$DRAGON_BIN" || fail "Dragon executable is missing"
test -f "$DECK" || fail "read-only observables deck is missing"
grep -Fxq 'MODULE SPORATE: GREP: END: ;' "$DECK" ||
  fail "observables deck is not limited to GREP and SPORATE"
test "$(grep -c '^SPORATE: AX TRK MAC ;$' "$DECK" || true)" -eq 1 ||
  fail "observables deck does not contain exactly one SPORATE call"
test "$(grep -c '^GREP: AX :: GETVAL' "$DECK" || true)" -eq 1 ||
  fail "observables deck does not contain exactly one k read"
test "$(grep -c '^PROCEDURE ' "$DECK" || true)" -eq 0 ||
  fail "observables deck must not call a procedure"
case "$TIMEOUT_SECONDS" in
  ''|*[!0-9]*|0) fail "TIMEOUT_SECONDS must be a positive integer" ;;
esac
test ! -e "$OUTPUT" && test ! -L "$OUTPUT" || fail "output directory must be fresh"

if [ -n "$RUNTIME" ]; then
  # A fine-mesh runtime must use its independently verified fine-mesh seed.
  if [ "$(hash "$RUNTIME/runtime.sha256")" = "$MESH12_RUNTIME_SHA" ]; then
    REPAIRED_RUNTIME_SHA=$MESH12_RUNTIME_SHA
    REPAIRED_BOOTSTRAP_SHA=$MESH12_BOOTSTRAP_SHA
  fi
  # Explicitly select the already verified repair epoch. Do not relabel the
  # old bootstrap or install/replace the canonical executable.
  test -f "$DRAGON_BIN" && test ! -L "$DRAGON_BIN" &&
    test "$(hash "$DRAGON_BIN")" = "$REPAIRED_DRAGON_SHA" ||
    fail "repaired Dragon identity differs"
  test "$(hash "$RUNTIME/runtime.sha256")" = "$REPAIRED_RUNTIME_SHA" ||
    fail "repaired runtime manifest identity differs"
  (cd "$RUNTIME" && shasum -a 256 -c runtime.sha256 >/dev/null) ||
    fail "repaired runtime does not verify"
  test "$(hash "$BUILD/result.sha256")" = "$REPAIRED_BOOTSTRAP_SHA" ||
    fail "repaired bootstrap identity differs"
  test "$(hash "$DECK")" = "$OBSERVABLE_DECK_SHA" ||
    fail "read-only observables deck identity differs"
  test -s "$FINAL/result.sha256" || fail "final repaired result manifest is missing"
  for name in runtime/Dragon runtime/runtime.sha256 input_manifest.sha256 \
    output_manifest.sha256 independent_check.log gate.log
  do
    awk -v name="$name" '$2 == name && NF == 2 && length($1) == 64 &&
      $1 !~ /[^0-9a-f]/ {n++} END {exit n != 1}' "$FINAL/result.sha256" ||
      fail "final repaired result does not manifest $name"
  done
  (cd "$FINAL" && shasum -a 256 -c result.sha256 >/dev/null) ||
    fail "final repaired result does not verify"
  same "$FINAL/runtime/Dragon" "$DRAGON_BIN" &&
    same "$FINAL/runtime/runtime.sha256" "$RUNTIME/runtime.sha256" ||
    fail "final result belongs to a different runtime"
fi

for receipt in "$BOOTSTRAP_RECEIPT"; do
  test -s "$BUILD/$receipt" || fail "$receipt is missing"
  (cd "$BUILD" && shasum -a 256 -c "$receipt" >/dev/null) ||
    fail "$receipt does not verify"
done
for receipt in input_manifest.sha256 output_manifest.sha256; do
  test -s "$FINAL/$receipt" || fail "$receipt is missing"
  (cd "$FINAL" && shasum -a 256 -c "$receipt" >/dev/null) ||
    fail "$receipt does not verify"
done

for name in closed_axial.xsm initial_axial_track.xsm \
  initial_axial_macrolib.xsm basis_reference.xsm route_contract.xsm \
  independent_check.log gate.log
do
  test -f "$FINAL/$name" || fail "final map is missing $name"
done
grep -Eq '^[0-9a-f]{64} [ *]closed_axial\.xsm$' \
  "$FINAL/output_manifest.sha256" || fail "final axial state is not manifested"
for name in initial_axial_track.xsm initial_axial_macrolib.xsm \
  basis_reference.xsm route_contract.xsm
do
  grep -Eq "^[0-9a-f]{64} [ *]$name\$" "$FINAL/input_manifest.sha256" ||
    fail "$name is not manifested"
done

same "$FINAL/basis_reference.xsm" "$BUILD/basis_reference.xsm" ||
  fail "final basis is not the corrected bootstrap basis"
same "$FINAL/route_contract.xsm" "$BUILD/route_contract.xsm" ||
  fail "final route contract is not the corrected bootstrap contract"
same "$FINAL/initial_axial_track.xsm" "$BUILD/initial_axial_track.xsm" ||
  fail "final axial track is not the corrected bootstrap track"
same "$FINAL/initial_axial_macrolib.xsm" \
  "$BUILD/initial_axial_macrolib.xsm" ||
  fail "final axial macrolib is not the corrected bootstrap macrolib"

grep -Fxq 'ONE-MAP-XSM COMPLETE' "$FINAL/independent_check.log" ||
  fail "final independent one-map check is incomplete"
grep -Fxq 'CLASSIFICATION=VALID_MET' "$FINAL/gate.log" ||
  fail "final map is not VALID_MET"
grep -Fxq 'SPOT-GATE COMPLETE' "$FINAL/gate.log" ||
  fail "final three-defect gate is incomplete"
test "$(grep -Ec '^SPOT-GATE (RRHO|RLEAK|RA) +[^ ]+ +PASS +$' \
  "$FINAL/gate.log" || true)" -eq 3 ||
  fail "not all three final defects pass"

mkdir -p "$(dirname -- "$OUTPUT")"
mkdir "$OUTPUT"
OUTPUT=$(CDPATH= cd -- "$OUTPUT" && pwd)
cp "$FINAL/closed_axial.xsm" "$OUTPUT/closed_axial.xsm"
cp "$FINAL/initial_axial_track.xsm" "$OUTPUT/initial_axial_track.xsm"
cp "$FINAL/initial_axial_macrolib.xsm" \
  "$OUTPUT/initial_axial_macrolib.xsm"
cp "$DECK" "$OUTPUT/observables.x2m"

AX_BEFORE=$(hash "$OUTPUT/closed_axial.xsm")
TRK_BEFORE=$(hash "$OUTPUT/initial_axial_track.xsm")
MAC_BEFORE=$(hash "$OUTPUT/initial_axial_macrolib.xsm")

OMP_NUM_THREADS=1
export OMP_NUM_THREADS
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$BOUNDED_DIR" \
  python3 -c \
  'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
  "$DRAGON_BIN" "$OUTPUT/observables.x2m" \
  "$OUTPUT/observables.log" "$TIMEOUT_SECONDS"

test "$(hash "$OUTPUT/closed_axial.xsm")" = "$AX_BEFORE" ||
  fail "closed axial state changed during extraction"
test "$(hash "$OUTPUT/initial_axial_track.xsm")" = "$TRK_BEFORE" ||
  fail "axial track changed during extraction"
test "$(hash "$OUTPUT/initial_axial_macrolib.xsm")" = "$MAC_BEFORE" ||
  fail "axial macrolib changed during extraction"
if [ -n "$RUNTIME" ]; then
  (cd "$BUILD" && shasum -a 256 -c result.sha256 >/dev/null) &&
    (cd "$FINAL" && shasum -a 256 -c result.sha256 >/dev/null) &&
    (cd "$RUNTIME" && shasum -a 256 -c runtime.sha256 >/dev/null) ||
    fail "sealed repaired inputs changed during extraction"
fi

LOG="$OUTPUT/observables.log"
test "$(grep -c '^>|D4A-CORRECTED-K-EFFECTIVE ' "$LOG" || true)" -eq 1 ||
  fail "expected exactly one corrected k"
test "$(grep -c '^SPORATE NU-FISSION-FRACTIONS ' "$LOG" || true)" -eq 1 ||
  fail "expected exactly one nu-fission fraction line"
test "$(grep -c 'normal end of execution for dragon' "$LOG" || true)" -eq 1 ||
  fail "Dragon did not end normally"
if grep -Eiq \
  'D4A-MAP8|LEGACY|XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$LOG"
then
  fail "observables log contains a legacy marker or abnormal terminal"
fi
awk '/^>\|D4A-CORRECTED-K-EFFECTIVE / {
       n++; if (!($2 > 0.0)) bad=1
     }
     END {exit !(n == 1 && !bad)}' "$LOG" || fail "invalid corrected k"
awk '/^SPORATE NU-FISSION-FRACTIONS / {
       n++; if (NF != 5) bad=1; s=$3+$4+$5;
       if ($3 < 0.0 || $4 < 0.0 || $5 < 0.0) bad=1
     }
     END {exit !(n == 1 && !bad && s >= 0.99999995 && s <= 1.00000005)}' \
  "$LOG" || fail "invalid normalized three-floor nu-fission production"

(
  cd "$OUTPUT"
  shasum -a 256 closed_axial.xsm initial_axial_track.xsm \
    initial_axial_macrolib.xsm observables.x2m observables.log \
    > observables.sha256
)

grep '^>|D4A-CORRECTED-K-EFFECTIVE ' "$LOG"
grep '^SPORATE NU-FISSION-FRACTIONS ' "$LOG"
echo "D4A CORRECTED FINAL OBSERVABLES PASS: $OUTPUT"
