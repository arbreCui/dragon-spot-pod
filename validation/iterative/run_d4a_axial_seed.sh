#!/bin/sh
set -eu

# Mint the first D4-A canonical axial state from an admitted snapshot
# RESULT_DIR (which must already hold d4a_snapshots.xsm and the three
# d4a_rank2_basis products).  Bounded, no retry, receipts hashed.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
DRAGON_BIN=${DRAGON_BIN:-"$ROOT/bin/Darwin_arm64/Dragon"}
TIMEOUT_SECONDS=${TIMEOUT_SECONDS:-43200}

fail() {
  echo "D4A AXIAL SEED FAIL: $*" >&2
  exit 1
}

test -n "${RESULT_DIR:-}" || fail "set RESULT_DIR to the admitted snapshot run"
case "$RESULT_DIR" in
  /*) ;;
  *) fail "RESULT_DIR must be an absolute path" ;;
esac
for f in d4a_snapshots.xsm d4a_axial_track.xsm d4a_axial_macrolib.xsm \
  d4a_rank2_basis.xsm
do
  test -f "$RESULT_DIR/$f" || fail "$f is missing from RESULT_DIR"
done
test ! -f "$RESULT_DIR/d4a_seed_axial.xsm" ||
  fail "d4a_seed_axial.xsm already exists; refuse to overwrite"

cp "$ROOT/validation/iterative/d4a_axial_seed.x2m" "$RESULT_DIR/"
cp "$ROOT/validation/iterative/run_bounded_dragon.py" "$RESULT_DIR/" \
  2>/dev/null || true

cd "$RESULT_DIR"
rm -rf _main001 _DUMMY
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 - "$DRAGON_BIN" \
  "$TIMEOUT_SECONDS" <<'PYEOF'
import sys
from pathlib import Path
sys.path.insert(0, '.')
import run_bounded_dragon as rbd
rbd.run(Path(sys.argv[1]), Path('d4a_axial_seed.x2m'),
        Path('d4a_axial_seed.log'), timeout_seconds=int(sys.argv[2]))
PYEOF

rg -q "D4A-AXIAL-SEED-COMPLETE" d4a_axial_seed.log ||
  fail "seed deck did not complete"
test -s d4a_seed_axial.xsm || fail "seed axial state was not produced"
test -s d4a_seed_snapshots.xsm || fail "seed snapshot archive was not produced"

rg ">\|D4A-AXIAL-SEED-(CANDIDATE|LEAKAGE)" d4a_axial_seed.log \
  > d4a_axial_seed_receipt.txt
shasum -a 256 "$DRAGON_BIN" > d4a_axial_seed_dragon.sha256
shasum -a 256 d4a_seed_axial.xsm d4a_seed_snapshots.xsm \
  d4a_axial_seed.x2m > d4a_axial_seed_products.sha256

echo "D4A AXIAL SEED PASS"
cat d4a_axial_seed_receipt.txt
