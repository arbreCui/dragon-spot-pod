#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
ITERATIVE="$ROOT/validation/iterative"
PROTOCOL_CHECKER="$ITERATIVE/check_gmres_activity_protocol.py"
IMPLEMENTATION_CHECKER="$ITERATIVE/check_gmres_activity_implementation.py"
IMPLEMENTATION_MANIFEST="$ITERATIVE/gmres_activity_implementation.sha256"
STATE_RUNNER="$ITERATIVE/run_gmres_activity_state_test.sh"
LEDGER_RUNNER="$ITERATIVE/run_gmres_activity_checker_test.sh"
NORMALIZER="$ITERATIVE/normalize_gmres_activity_log.py"
LEGACY_LOG="$ROOT/validation/artifacts/raw-moc-capture/stationary_on/probe.log"
PARENT=4d7abb23ac7975d4146beaa3b0049e36cdad8776
FROZEN_FC=/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15
NORMALIZED_SHA256=ff07ead583c85e5fc983e64d6a1d26cada7c1bb8836db11f1185fc637fc4ba39
WORK=$(mktemp -d "${TMPDIR:-/tmp}/spot-gmres-activity-preflight.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

fail()
{
  echo "GMRES-ACTIVITY PREFLIGHT FAIL: $*" >&2
  exit 2
}

if test "${RUN_GMRES_ACTIVITY+x}" = x
then
  case ${RUN_GMRES_ACTIVITY-} in
    1)
      fail "production execution requires a separate frozen run protocol"
      ;;
    *)
      fail "RUN_GMRES_ACTIVITY has an invalid value"
      ;;
  esac
fi

if test "${FC+x}" = x && test "$FC" != "$FROZEN_FC"
then
  fail "unfrozen FC override"
fi
FC=$FROZEN_FC
export FC

for path in "$PROTOCOL_CHECKER" "$IMPLEMENTATION_CHECKER" \
  "$IMPLEMENTATION_MANIFEST" \
  "$STATE_RUNNER" "$LEDGER_RUNNER" "$NORMALIZER" "$LEGACY_LOG"
do
  test -f "$path" || fail "missing dependency: $path"
  test ! -L "$path" || fail "symlink dependency: $path"
done

test -z "$(git -C "$ROOT" status --short -- src)" ||
  fail "live src has uncommitted state"
git -C "$ROOT" diff --quiet "$PARENT" -- src ||
  fail "live src differs from the frozen parent"

(cd "$ROOT" && shasum -a 256 -c "$IMPLEMENTATION_MANIFEST" >/dev/null)
python3 "$IMPLEMENTATION_CHECKER"
python3 "$PROTOCOL_CHECKER"
python3 "$PROTOCOL_CHECKER" --freeze-audit
sh "$STATE_RUNNER"
sh "$LEDGER_RUNNER"

python3 "$NORMALIZER" --mode legacy "$LEGACY_LOG" \
  >"$WORK/legacy.normalized.log"
sed 's/ MOCA 2 ;     / MOCA 2 GMRA ;/' "$LEGACY_LOG" \
  >"$WORK/gmra.synthetic.log"
test "$(grep -c 'GMRA' "$WORK/gmra.synthetic.log")" -eq 2 ||
  fail "synthetic GMRA token census differs"
test "$(awk 'index($0,"GMRA") { print length($0) }' \
  "$WORK/gmra.synthetic.log" | sort -u | tr '\n' ' ')" = "127 128 " ||
  fail "synthetic fixed-width GMRA line lengths differ"
python3 "$NORMALIZER" --mode gmra "$WORK/gmra.synthetic.log" \
  >"$WORK/gmra.normalized.log"
cmp "$WORK/legacy.normalized.log" "$WORK/gmra.normalized.log"
test "$(shasum -a 256 "$WORK/legacy.normalized.log" | awk '{print $1}')" \
  = "$NORMALIZED_SHA256" || fail "normalized legacy log hash differs"
test "$(grep -c '<MODULE-TIME>' "$WORK/legacy.normalized.log")" -eq 1 ||
  fail "normalized module-time marker census differs"
test "$(grep -c '<MEM-TELE>' "$WORK/legacy.normalized.log")" -eq 1 ||
  fail "normalized module-memory marker census differs"
test "$(grep -c '<CLE-CPU>' "$WORK/legacy.normalized.log")" -eq 1 ||
  fail "normalized CLE CPU marker census differs"

sed '/^-->>MODULE FLU:/d' "$LEGACY_LOG" >"$WORK/missing-module.log"
if python3 "$NORMALIZER" --mode legacy "$WORK/missing-module.log" \
     >"$WORK/missing-module.normalized" 2>"$WORK/missing-module.err"
then
  fail "normalizer accepted a missing FLU module receipt"
fi
grep -q 'module receipt census differs' "$WORK/missing-module.err"

awk '
  { print }
  /^-->>MODULE FLU:/ {
    print "-->>MODULE ASM:        : TIME SPENT=" \
      "        0.000 MEMORY USAGE= 1.000E+06"
  }
' "$LEGACY_LOG" >"$WORK/extra-module.log"
if python3 "$NORMALIZER" --mode legacy "$WORK/extra-module.log" \
     >"$WORK/extra-module.normalized" 2>"$WORK/extra-module.err"
then
  fail "normalizer accepted an extra module receipt"
fi
grep -q 'module receipt census differs' "$WORK/extra-module.err"

sed 's/MEMORY USAGE= 2.268E+07/MEMORY USAGE=-2.268E+07/' \
  "$LEGACY_LOG" >"$WORK/bad-memory.log"
if python3 "$NORMALIZER" --mode legacy "$WORK/bad-memory.log" \
     >"$WORK/bad-memory.normalized" 2>"$WORK/bad-memory.err"
then
  fail "normalizer accepted malformed module memory telemetry"
fi
grep -q 'module memory telemetry grammar differs' "$WORK/bad-memory.err"

sed 's/cle2000_c: cpu time= 0.00 second/cle2000_c: cpu time= -0.00 second/' \
  "$LEGACY_LOG" >"$WORK/bad-cle-cpu.log"
if python3 "$NORMALIZER" --mode legacy "$WORK/bad-cle-cpu.log" \
     >"$WORK/bad-cle-cpu.normalized" 2>"$WORK/bad-cle-cpu.err"
then
  fail "normalizer accepted malformed CLE CPU telemetry"
fi
grep -q 'CLE CPU telemetry census differs' "$WORK/bad-cle-cpu.err"

if python3 "$NORMALIZER" --mode legacy "$WORK/gmra.synthetic.log" \
     >"$WORK/wrong-legacy.log" 2>"$WORK/wrong-legacy.err"
then
  fail "legacy mode accepted a GMRA log"
fi
grep -q 'legacy log contains GMRA' "$WORK/wrong-legacy.err"
if python3 "$NORMALIZER" --mode gmra "$LEGACY_LOG" \
     >"$WORK/missing-gmra.log" 2>"$WORK/missing-gmra.err"
then
  fail "GMRA mode accepted a legacy log"
fi
grep -q 'GMRA token census differs' "$WORK/missing-gmra.err"

sh -n "$STATE_RUNNER"
sh -n "$LEDGER_RUNNER"
sh -n "$ITERATIVE/build_gmres_activity_overlay.sh"
git -C "$ROOT" diff --check

test -z "$(git -C "$ROOT" status --short -- src)" ||
  fail "live src changed during preflight"
git -C "$ROOT" diff --quiet "$PARENT" -- src ||
  fail "live src changed from the frozen parent"

echo "GMRES-ACTIVITY PREFLIGHT PASS"
echo "GMRES-ACTIVITY PRODUCTION NOT AUTHORIZED"
