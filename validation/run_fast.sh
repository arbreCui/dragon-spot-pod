#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/check_method_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_spot_strict_inner.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_picard_control.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_nonlinear_solver_contract.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT/validation/iterative" \
  python3 "$ROOT/validation/iterative/test_bounded_dragon.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_source_identity.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_fixed_basis_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_state_contract.py"
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/test_state_math.py"
sh "$ROOT/validation/iterative/run_b2c_runtime_dimensions.sh"
sh "$ROOT/validation/level1/run_level1.sh"
sh "$ROOT/validation/level2/run_level2.sh"

printf '%s\n' 'SPOT ACTIVE FAST PASS'
