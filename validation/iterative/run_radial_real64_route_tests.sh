#!/bin/sh
set -eu

cd "$(dirname "$0")/../.."

python3 validation/iterative/check_radial_real64_route_protocol.py
python3 validation/iterative/check_radial_real64_route_protocol.py --require-local
python3 -m unittest -v validation/iterative/test_radial_real64_route_protocol.py

echo "RADIAL-REAL64 ROUTE TESTS PASS: TESTS=20 DRAGON-RUNS=0"
