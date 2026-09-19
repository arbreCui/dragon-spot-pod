#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
REPLAY="$HERE/verify_d4a_corrected_observables.sh"
ACCEPTANCE="$HERE/check_d4a_corrected_acceptance.sh"
RUNNER="$HERE/run_bounded_dragon.py"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/d4a-observable-replay-test.XXXXXX")
cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT HUP INT TERM

hash() {
  shasum -a 256 "$1" | awk '{print $1}'
}

fail() {
  echo "D4A OBSERVABLE REPLAY TEST FAIL: $*" >&2
  exit 1
}

cat > "$TMP/fake_dragon" <<'EOF'
#!/bin/sh
cat >/dev/null
printf '%s\n' '>|D4A-CORRECTED-K-EFFECTIVE   1.234567890123456E+00'
printf '%s\n' 'SPORATE NU-FISSION-FRACTIONS   2.00000000E-01  3.00000000E-01  5.00000000E-01'
printf '%s\n' ' normal end of execution for dragon 5  Version 5.1.0'
EOF
chmod +x "$TMP/fake_dragon"

cat > "$TMP/canonical.x2m" <<'EOF'
* synthetic read-only observables deck
EOF

make_observables() {
  directory=$1
  k_value=$2
  deck=$3
  mkdir "$directory"
  printf '%s\n' AXIAL > "$directory/closed_axial.xsm"
  printf '%s\n' TRACK > "$directory/initial_axial_track.xsm"
  printf '%s\n' MACRO > "$directory/initial_axial_macrolib.xsm"
  cp "$deck" "$directory/observables.x2m"
  {
    printf '>|D4A-CORRECTED-K-EFFECTIVE   %s\n' "$k_value"
    printf '%s\n' 'SPORATE NU-FISSION-FRACTIONS   2.00000000E-01  3.00000000E-01  5.00000000E-01'
    printf '%s\n' ' normal end of execution for dragon 5  Version 5.1.0'
  } > "$directory/observables.log"
}

GOOD="$TMP/good"
make_observables "$GOOD" 1.234567890123456E+00 "$TMP/canonical.x2m"
"$REPLAY" \
  "$TMP/fake_dragon" "$(hash "$TMP/fake_dragon")" \
  "$TMP/canonical.x2m" "$(hash "$TMP/canonical.x2m")" \
  "$RUNNER" "$(hash "$RUNNER")" "$GOOD" >/dev/null ||
  fail "matching sealed-XSM replay was rejected"

BAD_LOG="$TMP/bad-log"
make_observables "$BAD_LOG" 9.999999999999999E+00 "$TMP/canonical.x2m"
if "$REPLAY" \
  "$TMP/fake_dragon" "$(hash "$TMP/fake_dragon")" \
  "$TMP/canonical.x2m" "$(hash "$TMP/canonical.x2m")" \
  "$RUNNER" "$(hash "$RUNNER")" "$BAD_LOG" >/dev/null 2>&1
then
  fail "forged saved k record was accepted"
fi

cp "$TMP/canonical.x2m" "$TMP/tampered.x2m"
printf '%s\n' '* unauthorized change' >> "$TMP/tampered.x2m"
BAD_DECK="$TMP/bad-deck"
make_observables "$BAD_DECK" 1.234567890123456E+00 "$TMP/tampered.x2m"
if "$REPLAY" \
  "$TMP/fake_dragon" "$(hash "$TMP/fake_dragon")" \
  "$TMP/tampered.x2m" "$(hash "$TMP/canonical.x2m")" \
  "$RUNNER" "$(hash "$RUNNER")" "$BAD_DECK" >/dev/null 2>&1
then
  fail "tampered deck was accepted against the canonical SHA-256"
fi

if CHECKER_DIR="$TMP/fake-checkers" sh "$ACCEPTANCE" >/dev/null 2>"$TMP/checker.err"
then
  fail "CHECKER_DIR environment replacement was accepted"
fi
grep -Fxq 'D4A-CORRECTED-ACCEPT CONFIG FAIL: CHECKER_DIR override refused' \
  "$TMP/checker.err" || fail "CHECKER_DIR refusal was not fail-closed"

if DRAGON_BIN="$TMP/fake_dragon" sh "$ACCEPTANCE" >/dev/null 2>"$TMP/dragon.err"
then
  fail "DRAGON_BIN environment replacement was accepted"
fi
grep -Fxq 'D4A-CORRECTED-ACCEPT CONFIG FAIL: DRAGON_BIN override refused' \
  "$TMP/dragon.err" || fail "DRAGON_BIN refusal was not fail-closed"

echo "D4A OBSERVABLE REPLAY TEST PASS: exact replay accepted; forged log, tampered deck, and environment replacement refused"
