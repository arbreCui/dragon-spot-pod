#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

PYTHONDONTWRITEBYTECODE=1 python3 \
  "$ROOT/validation/iterative/check_source_identity.py"

sh "$ROOT/validation/level2/run_level2.sh"
