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
NORMALIZED_SHA256=647785d00ed45d721860c6f4c8dbb84633526cbe2e042be42cb36ea85d9b39d9
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
