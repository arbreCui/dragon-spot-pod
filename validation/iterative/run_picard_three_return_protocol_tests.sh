#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$ROOT"

python3 validation/iterative/check_picard_three_return_protocol.py
python3 validation/iterative/check_picard_three_return_protocol.py --require-local
python3 -m unittest -v validation.iterative.test_picard_three_return_protocol

echo "PICARD-THREE-RETURN DESIGN TESTS PASS: TESTS=20 EXECUTION=NO-GO DRAGON-RUNS=0"
