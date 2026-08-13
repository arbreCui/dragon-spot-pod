#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

sh "$ROOT/validation/run_picard_fast.sh"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_source_identity.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_fixed_basis_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_state_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_state_math.py"
sh "$ROOT/validation/level1/run_level1.sh"
sh "$ROOT/validation/level2/run_level2.sh"
