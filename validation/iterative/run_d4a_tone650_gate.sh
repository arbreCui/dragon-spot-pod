#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RESULT_DIR=${RESULT_DIR:-}
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
DLIB370=${DLIB370:-/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/pincell/DLIB_370}
RUN_D4A_TONE_GATE=${RUN_D4A_TONE_GATE:-0}
TIMEOUT_SECONDS=1500
DECK_SOURCE="$ROOT/validation/iterative/d4a_tone650_gate.x2m"
PROCEDURE_SOURCE="$ROOT/data/SpotD4Tone.c2m"
EXPECTED_DLIB_SHA=66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9

fail() {
  echo "D4A TONE650 GATE FAIL: $*" >&2
  exit 1
}

expect_count() {
  pattern=$1
  expected=$2
  file=$3
  count=$(rg -c "$pattern" "$file" || true)
  count=${count:-0}
  test "$count" = "$expected" ||
    fail "expected $expected matches for '$pattern' in $file; found $count"
}

test -f "$DECK_SOURCE" || fail "gate deck is missing"
test -f "$PROCEDURE_SOURCE" || fail "gate procedure is missing"
test -x "$DRAGON_BIN" || fail "Dragon executable is missing"
test -f "$DLIB370" || fail "370-group DLIB is missing"
(
  cd "$ROOT"
  sha256sum -c validation/iterative/d4a_snapshot_inputs.sha256 >/dev/null
) || fail "a frozen D4-A repository input changed"

dlib_sha=$(sha256sum "$DLIB370" | awk '{print $1}')
test "$dlib_sha" = "$EXPECTED_DLIB_SHA" ||
  fail "the 370-group DLIB hash changed: $dlib_sha"

expect_count '^MICROLIB2 := TONE: MICROLIB TRACK_T TRACK_T_f ::$' 1 \
  "$PROCEDURE_SOURCE"
expect_count '^    TISO 24 50\.0 LONG$' 1 "$PROCEDURE_SOURCE"
expect_count '^    EDIT 1 MXIT 20 EPS 1\.0E-5 TRAN PIJ ;$' 1 \
  "$PROCEDURE_SOURCE"
expect_count 'TISO 24 100\.0|MCCGT:|ASM:|FLU:|BACKUP:|XSM_FILE' 0 \
  "$PROCEDURE_SOURCE"
expect_count '^REAL T_comb := 650\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL T_clad := 620\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^REAL T_Na := 475\.0 ;$' 1 "$DECK_SOURCE"
expect_count '^MICROLIB2 := SpotD4Tone glow_rnr ::$' 1 "$DECK_SOURCE"
expect_count '^ECHO "D4A-TONE650-GATE-COMPLETE" ;$' 1 "$DECK_SOURCE"
expect_count 'XSM_FILE|MCCGT:|ASM:|FLU:|BACKUP:|SPOT:|SPOR|Picard|POD' 0 \
  "$DECK_SOURCE"

echo "D4A TONE650 STATIC PREFLIGHT PASS"
echo "D4A TONE650 STATE C: (650,620,475)"
echo "D4A TONE650 PHYSICS: LIB+SALT(TISO=50)+TONE(MXIT=20,EPS=1e-5)"
echo "D4A TONE650 EXCLUDED: MCCGT ASM FLU SNAPSHOT POD PICARD"
echo "D4A TONE650 HARD LIMIT: ${TIMEOUT_SECONDS}s, one run, no retry"

if [ "$RUN_D4A_TONE_GATE" != 1 ]; then
  echo "D4A TONE650 GATE DISABLED: set RUN_D4A_TONE_GATE=1 and an unused RESULT_DIR"
  exit 0
fi

test -n "$RESULT_DIR" || fail "set RESULT_DIR to a new absolute path"
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path" ;;
esac
test ! -e "$RESULT_DIR" || fail "refusing to overwrite RESULT_DIR"
mkdir -p "$(dirname -- "$RESULT_DIR")"
mkdir "$RESULT_DIR"

cp "$DECK_SOURCE" "$RESULT_DIR/d4a_tone650_gate.x2m"
cp "$PROCEDURE_SOURCE" "$RESULT_DIR/SpotD4Tone.c2m"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_cc.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/rnr_interpol.c2m" "$RESULT_DIR/"
cp "$ROOT/data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat" \
  "$RESULT_DIR/geometry.dat"
ln -s "$DLIB370" "$RESULT_DIR/DLIB8R1_370"

(
  cd "$RESULT_DIR"
  printf '%s\n' \
    'STATE_C=650,620,475' \
    'TONE_TRACK_TISO=50.0' \
    'TONE_MXIT=20' \
    'TONE_EPS=1.0E-5' \
    "WALL_LIMIT_SECONDS=$TIMEOUT_SECONDS" \
    'RETRY=0' > run_contract.txt
  sha256sum d4a_tone650_gate.x2m SpotD4Tone.c2m rnr_cc.c2m \
    rnr_interpol.c2m geometry.dat DLIB8R1_370 run_contract.txt \
    "$DRAGON_BIN" > executed_inputs.sha256
)

OMP_NUM_THREADS=1
export OMP_NUM_THREADS
echo "D4A TONE650 PHYSICAL GATE START"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  python3 -c \
  'import sys; from pathlib import Path; from run_bounded_dragon import run; run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), float(sys.argv[4]))' \
  "$DRAGON_BIN" "$RESULT_DIR/d4a_tone650_gate.x2m" \
  "$RESULT_DIR/d4a_tone650_gate.log" "$TIMEOUT_SECONDS" \
  > "$RESULT_DIR/runner.out" 2> "$RESULT_DIR/runner.err"
echo "D4A TONE650 PHYSICAL GATE END"

LOG="$RESULT_DIR/d4a_tone650_gate.log"
test ! -s "$RESULT_DIR/runner.out" || fail "bounded runner stdout is not empty"
test ! -s "$RESULT_DIR/runner.err" || fail "bounded runner stderr is not empty"
expect_count 'MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED' 0 "$LOG"
expect_count 'CONVERGENCE REACHED AT TONE ITERATION' 1 "$LOG"
expect_count '^>\|D4A-TONE650-GATE-COMPLETE' 1 "$LOG"
expect_count 'normal end of execution for dragon' 1 "$LOG"
expect_count '^->@BEGIN MODULE : TONE:' 1 "$LOG"
expect_count '^->@BEGIN MODULE : MCCGT:|^->@BEGIN MODULE : ASM:|^->@BEGIN MODULE : FLU:' 0 "$LOG"
if rg -i \
  'XABORT|ABORT:|FATAL|SIG(SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error' \
  "$LOG" >/dev/null
then
  fail "Dragon log contains an abnormal terminal"
fi

metrics=$(PYTHONDONTWRITEBYTECODE=1 python3 -c '
import re
import sys
text = open(sys.argv[1], errors="replace").read()
m = re.findall(
    r"CONVERGENCE REACHED AT TONE ITERATION\s*=\s*(\d+)\s+ERROR\s*=\s*([-+0-9.Ee]+)",
    text,
)
if len(m) != 1:
    raise SystemExit("expected exactly one parseable TONE terminal")
iteration = int(m[0][0])
error = float(m[0][1])
if not (1 <= iteration <= 20):
    raise SystemExit(f"invalid TONE iteration {iteration}")
if not (0.0 <= error <= 1.0e-5):
    raise SystemExit(f"TONE error {error:.17g} exceeds 1e-5")
print(f"iteration={iteration} error={error:.17g}")
' "$LOG") || fail "TONE terminal metrics were not admitted"

test ! -e "$RESULT_DIR/d4a_snapshots.xsm" ||
  fail "a snapshot archive was unexpectedly created"
(
  cd "$RESULT_DIR"
  sha256sum -c executed_inputs.sha256 >/dev/null
  sha256sum d4a_tone650_gate.log runner.out runner.err \
    executed_inputs.sha256 run_contract.txt > tone650_gate_result.sha256
)

echo "D4A TONE650 GATE PASS: $metrics"
echo "D4A TONE650 RESULT: $RESULT_DIR"
