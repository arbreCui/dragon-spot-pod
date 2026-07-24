#!/usr/bin/env python3
"""Static and arithmetic checks for the read-only radial precision audit."""

from __future__ import annotations

import json
import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
RESULT = ITERATIVE / "radial_precision_result.txt"
PROTOCOL = ITERATIVE / "raw_moc_residual_protocol.json"
SOURCE = ITERATIVE / "check_radial_precision_xsm.f90"
RUNNER = ITERATIVE / "run_radial_precision_audit.sh"
RECEIPT = ITERATIVE / "radial_precision_receipt.sha256"
LOCAL_FULL = (
    ROOT
    / "validation"
    / "artifacts"
    / "iterative-radial-floor"
    / "radial_precision_xsm_full.log"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RADIAL-PRECISION CONTRACT FAIL: {message}")


def unique_value(lines: list[list[str]], arm: str, name: str) -> int:
    matches = [
        fields
        for fields in lines
        if len(fields) == 4
        and fields[:3] == ["RADIAL-PRECISION-XSM", arm, name]
    ]
    require(len(matches) == 1, f"{arm} {name} must occur exactly once")
    return int(matches[0][3])


receipt_rows = [
    row.split()
    for row in RECEIPT.read_text(encoding="ascii").splitlines()
    if row.strip()
]
require(
    len(receipt_rows) == 8
    and all(len(row) == 2 for row in receipt_rows)
    and len({row[1] for row in receipt_rows}) == 8
    and all(re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in receipt_rows),
    "precision receipt has an invalid census",
)
expected_receipt_paths = {
    "validation/artifacts/iterative-radial-floor/"
    "radial_precision_xsm_full.log",
    "validation/iterative/radial_floor_result_receipt.sha256",
    "validation/iterative/check_radial_precision_xsm.f90",
    "validation/iterative/run_radial_precision_audit.sh",
    "validation/iterative/check_radial_precision_contract.py",
    "validation/iterative/radial_precision_result.txt",
    "validation/iterative/radial_precision_result.md",
    "validation/iterative/raw_moc_residual_protocol.json",
}
require(
    {row[1] for row in receipt_rows} == expected_receipt_paths,
    "precision receipt path set changed",
)
for expected_hash, relative in receipt_rows:
    path = ROOT / relative
    if not path.exists() and relative.startswith("validation/artifacts/"):
        continue
    require(path.is_file() and not path.is_symlink(), f"invalid receipt file {relative}")
    require(
        hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
        f"receipt hash differs for {relative}",
    )


raw = RESULT.read_bytes()
require(raw.endswith(b"\n"), "result must end with a newline")
require(b"\r" not in raw, "result must use LF newlines")
text = raw.decode("ascii")
require(" LEDGER " not in text, "tracked result must be the compact summary")
split_lines = [line.split() for line in text.splitlines()]
require(
    split_lines[0] == ["RADIAL-PRECISION-XSM", "DIMS", "370", "8", "14"],
    "dimension line changed",
)
require(
    split_lines[-1] == ["RADIAL-PRECISION-XSM", "COMPLETE"],
    "completion line changed",
)

expected = {
    "NATIVE": {
        "TOTAL": 2960,
        "UNCHANGED": 288,
        "UPWARD": 136,
        "DOWNWARD": 2536,
        "ADJACENT": 265,
        "MAX-STEPS": 17,
    },
    "STATIONARY": {
        "TOTAL": 2960,
        "UNCHANGED": 272,
        "UPWARD": 88,
        "DOWNWARD": 2600,
        "ADJACENT": 220,
        "MAX-STEPS": 12,
    },
}

for arm, locked in expected.items():
    found = {name: unique_value(split_lines, arm, name) for name in locked}
    require(found == locked, f"{arm} locked summary changed")
    require(
        found["UNCHANGED"] + found["UPWARD"] + found["DOWNWARD"]
        == found["TOTAL"],
        f"{arm} direction census does not close",
    )

    histogram = [
        (int(fields[3]), int(fields[4]))
        for fields in split_lines
        if len(fields) == 5
        and fields[:3] == ["RADIAL-PRECISION-XSM", arm, "HIST"]
    ]
    require(histogram, f"{arm} histogram is missing")
    require(
        [step for step, _ in histogram]
        == sorted({step for step, _ in histogram}),
        f"{arm} histogram is not unique and ordered",
    )
    require(
        sum(count for _, count in histogram) == found["TOTAL"],
        f"{arm} histogram census does not close",
    )
    require(
        sum(count for step, count in histogram if step == 0)
        == found["UNCHANGED"],
        f"{arm} zero-step count differs",
    )
    require(
        sum(count for step, count in histogram if step > 0) == found["UPWARD"],
        f"{arm} upward count differs",
    )
    require(
        sum(count for step, count in histogram if step < 0)
        == found["DOWNWARD"],
        f"{arm} downward count differs",
    )
    require(
        sum(count for step, count in histogram if abs(step) == 1)
        == found["ADJACENT"],
        f"{arm} adjacent count differs",
    )
    require(
        max(abs(step) for step, _ in histogram) == found["MAX-STEPS"],
        f"{arm} maximum step differs",
    )

    ties = [
        (int(fields[3]), int(fields[4]), int(fields[5]))
        for fields in split_lines
        if len(fields) == 6
        and fields[:3] == ["RADIAL-PRECISION-XSM", arm, "MAX-TIE"]
    ]
    require(ties, f"{arm} maximum ties are missing")
    require(len(ties) == len(set(ties)), f"{arm} maximum ties are duplicated")
    require(
        all(abs(step) == found["MAX-STEPS"] for _, _, step in ties),
        f"{arm} maximum tie has the wrong step",
    )
    histogram_max_count = sum(
        count for step, count in histogram if abs(step) == found["MAX-STEPS"]
    )
    require(
        len(ties) == histogram_max_count,
        f"{arm} maximum ties do not cover every maximum",
    )

protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
require(
    protocol["status"] == "FROZEN-BEFORE-IMPLEMENTATION",
    "raw-MOC protocol is not frozen before implementation",
)
scope = protocol["scope"]
require(scope["transport_mode"] == "TYPE S", "protocol transport mode changed")
require(scope["door"] == "MCCG", "protocol door changed")
require(scope["terminal_inputs"] == ["NATIVE", "STATIONARY"], "arm set changed")
require(
    scope["operator_applications_added_by_instrumentation"] == 0,
    "protocol adds an operator application",
)
require(scope["diagnostic_default"] == "OFF", "diagnostic is not default-off")
require(
    scope["locked_solver_path"]
    == {
        "KRYL": 10,
        "STIS": 1,
        "IAAC": 80,
        "ISCR": 0,
        "IDIFC": 0,
        "PACA": 4,
        "IDIR": 0,
    },
    "locked MCCG branch changed",
)
capture = protocol["capture_point"]
require(
    capture["caller"] == "MCGMRE"
    and capture["role"] == "PRIMARY-FIXED-POINT-EVALUATION"
    and capture["epoch"] == 1
    and capture["flu_outer_iteration"] == 1
    and capture["flu_thermal_iteration"] == 1
    and capture["doorfv_serial"] == 1
    and capture["mccgf_serial"] == 1
    and capture["gmres_global_iteration"] == 1
    and capture["write_policy"] == "WRITE-ONCE",
    "primary GMRES capture role changed",
)
require(
    capture["required_active_set"]
    == {"NGEFF": 370, "NGIND": "1..370 in order", "NCONV": "all true"},
    "capture active set changed",
)
sink=protocol["audit_sink"]
require(
    sink["owner"] == "fresh writable L_FLUX output"
    and sink["directory"] == "SPOT-MOC-AUD"
    and sink["initial_status"] == "INCOMPLETE"
    and sink["published_status"] == "COMPLETE",
    "audit sink contract changed",
)
require(
    sink["state_vector_codes"]
    == {
        "schema-version": 1,
        "status": {"INCOMPLETE": 0, "COMPLETE": 1},
        "arm": {"NATIVE": 1, "STATIONARY": 2},
        "role": {"PRIMARY-FIXED-POINT-EVALUATION": 1},
        "phase": {
            "POST-STIS-OR-VOLUME-NORMALIZATION-PRE-ACA-SCR": 1
        },
    },
    "audit state-vector codebook changed",
)
root_records = {
    record["name"]: (record["lcm_type"], record["length"])
    for record in sink["root_records"]
}
require(
    root_records
    == {
        "STATE-VECTOR": (1, 24),
        "NGIND": (1, 370),
        "GROUP": (10, 370),
    },
    "audit root-record contract changed",
)
records = {
    record["name"]: (record["lcm_type"], record["length"])
    for record in protocol["records_per_audit_group"]
}
require(
    records
    == {
        "SPOT-M-QFR": (4, 14),
        "SPOT-M-EVAL": (4, 14),
        "SPOT-M-SRC": (4, 14),
        "SPOT-M-RAW": (4, 14),
        "SPOT-M-STEP": (1, 1),
        "SPOT-M-ROLE": (1, 1),
        "SPOT-M-GROUP": (1, 1),
    },
    "capture record contract changed",
)
checker = protocol["independent_checker"]
require(
    checker["arithmetic_contract"]
    == {
        "ledger_order": "group 1..370 outer, unknown 1..14 inner",
        "scalar_indices": "KEYFLX$ANIS(1..8) in region order",
        "weights": (
            "TRACK VOLUME(1..8), each binary32 value promoted exactly "
            "to binary64"
        ),
        "scalar_reduction_order": (
            "group 1..370 outer, region 1..8 inner, left-to-right accumulation"
        ),
        "relative_two_norm": (
            "sqrt(sum(((V * delta) * delta)) / "
            "sum(((V * eval) * eval)))"
        ),
        "input_normalized_global_max": (
            "max(abs(delta)) / max(abs(eval)); retain every exact "
            "binary64 numerator tie"
        ),
        "floating_point": (
            "IEEE binary64 for subtraction, products, sums, maxima, "
            "division and square root; no contraction or reassociation"
        ),
    },
    "independent checker arithmetic contract changed",
)
classification = protocol["classification"]
require(
    classification["acceptance_threshold"] is None,
    "protocol introduced an acceptance threshold",
)
require(
    not classification["stage4_authorization"]
    and not classification["stage5_authorization"]
    and not classification["outer_convergence_evaluated"],
    "protocol overstates qualification",
)

source = SOURCE.read_text(encoding="utf-8")
require(
    re.search(
        r"signed_positive_ulp_steps\s*=\s*"
        r"int\(real32_bits\(right\),int64\)\s*-\s*&\s*"
        r"\n\s*int\(real32_bits\(left\),int64\)",
        source,
    )
    is not None,
    "ULP step is not the exact signed encoding difference",
)
require("spacing(" not in source.lower(), "checker uses a spacing quotient")
require(
    re.search(
        r"\b(LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b",
        source,
        re.IGNORECASE,
    )
    is None,
    "checker source contains LCM mutation",
)
require(
    re.search(
        r"\bcall\s+(FLU2DR|FLU2AC|FLUBAL|DOORFV|MCCGF|MCGFLX|SPOT1P)\b",
        source,
        re.IGNORECASE,
    )
    is None,
    "checker source calls a production solver",
)

runner = RUNNER.read_text(encoding="utf-8")
for token in (
    "check_radial_floor_xsm",
    "inputs_before.sha256",
    "cmp \"$WORK/precision_a.log\" \"$WORK/precision_b.log\"",
    "shasum -a 256 -c \"$PRECISION_RECEIPT\"",
    "cmp \"$WORK/precision_a.log\" \"$PUBLISHED_FULL\"",
    "cmp \"$WORK/precision_compact.log\" \"$PUBLISHED_RESULT\"",
    "check_radial_precision_xsm.object.nm",
    "checker object references LCM mutation",
    "checker object references solver symbols",
    "-ffp-contract=off",
    "-fno-fast-math",
    "test \"$(grep -c ' LEDGER '",
):
    require(token in runner, f"runner lost required gate: {token}")
require(
    'ARTIFACT="$ROOT/validation/artifacts/iterative-radial-floor"' in runner
    and "ARTIFACT=${ARTIFACT:-" not in runner,
    "runner does not lock the canonical evidence directory",
)

if LOCAL_FULL.exists():
    require(not LOCAL_FULL.is_symlink(), "local full ledger is a symlink")
    full_bytes = LOCAL_FULL.read_bytes()
    full_lines = full_bytes.splitlines()
    compact = b"\n".join(
        line
        for line in full_lines
        if b" LEDGER " not in line
    ) + b"\n"
    require(compact == raw, "local full ledger does not reproduce result")
    require(
        sum(b" LEDGER " in line for line in full_lines) == 5920,
        "local full ledger census changed",
    )

    decoded_lines = [line.decode("ascii").split() for line in full_lines]
    for arm in ("NATIVE", "STATIONARY"):
        ledger = [
            fields
            for fields in decoded_lines
            if len(fields) >= 3
            and fields[:3] == ["RADIAL-PRECISION-XSM", arm, "LEDGER"]
        ]
        require(len(ledger) == 2960, f"{arm} ledger census changed")
        step_counts: Counter[int] = Counter()
        maximum_rows: set[tuple[int, int, int]] = set()
        for index, fields in enumerate(ledger):
            require(len(fields) == 10, f"{arm} malformed ledger row")
            expected_group=index // 8 + 1
            expected_region=index % 8 + 1
            group, region, key = map(int, fields[3:6])
            require(
                (group, region, key)
                == (expected_group, expected_region, expected_region),
                f"{arm} ledger layout/order differs at row {index + 1}",
            )
            require(
                re.fullmatch(r"[0-9A-F]{8}", fields[6]) is not None
                and re.fullmatch(r"[0-9A-F]{8}", fields[7]) is not None,
                f"{arm} ledger has noncanonical binary32 bits",
            )
            pre_bits=int(fields[6],16)
            post_bits=int(fields[7],16)
            require(
                0 < pre_bits < 0x7F800000
                and 0 < post_bits < 0x7F800000,
                f"{arm} ledger has nonpositive or nonfinite scalar flux",
            )
            signed_step=int(fields[8])
            absolute_step=int(fields[9])
            require(
                signed_step == post_bits-pre_bits,
                f"{arm} ledger signed step differs at row {index + 1}",
            )
            require(
                absolute_step == abs(signed_step),
                f"{arm} ledger absolute step differs at row {index + 1}",
            )
            step_counts[signed_step] += 1

        published_histogram = {
            int(fields[3]): int(fields[4])
            for fields in split_lines
            if len(fields) == 5
            and fields[:3] == ["RADIAL-PRECISION-XSM", arm, "HIST"]
        }
        require(
            dict(sorted(step_counts.items())) == published_histogram,
            f"{arm} ledger-derived histogram differs",
        )
        locked=expected[arm]
        require(step_counts[0] == locked["UNCHANGED"], f"{arm} unchanged differs")
        require(
            sum(count for step,count in step_counts.items() if step > 0)
            == locked["UPWARD"],
            f"{arm} ledger-derived upward count differs",
        )
        require(
            sum(count for step,count in step_counts.items() if step < 0)
            == locked["DOWNWARD"],
            f"{arm} ledger-derived downward count differs",
        )
        require(
            step_counts[1]+step_counts[-1] == locked["ADJACENT"],
            f"{arm} ledger-derived adjacent count differs",
        )
        max_step=max(abs(step) for step in step_counts)
        require(max_step == locked["MAX-STEPS"], f"{arm} ledger maximum differs")
        for fields in ledger:
            step=int(fields[8])
            if abs(step) == max_step:
                maximum_rows.add((int(fields[3]),int(fields[4]),step))
        published_ties = {
            (int(fields[3]),int(fields[4]),int(fields[5]))
            for fields in split_lines
            if len(fields) == 6
            and fields[:3] == ["RADIAL-PRECISION-XSM", arm, "MAX-TIE"]
        }
        require(
            maximum_rows == published_ties,
            f"{arm} ledger-derived maximum ties differ",
        )

print("RADIAL-PRECISION CONTRACT PASS")
