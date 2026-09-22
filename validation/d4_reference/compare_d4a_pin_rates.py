#!/usr/bin/env python3
"""Read-only SPOT/CE pin-fraction comparison, not a receipt or accuracy gate.

Inputs are aligned by (floor, pin_index), never by row position. No transport,
normalization, clipping, calibration, uncertainty conversion, or source
authentication is performed. All reported differences are SPOT minus CE.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

KEYS = {(floor, pin) for floor in (1, 2, 3) for pin in range(217)}
FIELDS = ("floor", "pin_index", "spot_global_fraction", "ce_global_fraction",
          "spot_minus_ce", "absolute_difference")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonnegative(value, label):
    require(not isinstance(value, bool), f"boolean {label}")
    number = float(value)
    require(math.isfinite(number) and number >= 0, f"nonfinite or negative {label}")
    return number


def integer(value, label, *, json_value=False):
    if json_value:
        require(type(value) is int, f"noninteger {label}")
    return int(value)


def complete(records, label):
    require(set(records) == KEYS, f"{label} must cover exactly 3 floors x 217 pins")


def read_spot(path):
    required = {"floor", "pin_index", "nu_fission_rate", "global_fraction"}
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        header = reader.fieldnames or []
        require(len(header) == len(set(header)) and required.issubset(header), "invalid SPOT CSV header")
        result = {}
        for row in reader:
            require(None not in row and all(value is not None for value in row.values()), "malformed SPOT row")
            key = (integer(row["floor"], "SPOT floor"), integer(row["pin_index"], "SPOT pin_index"))
            require(key not in result, "duplicate SPOT floor/pin_index")
            rate = nonnegative(row["nu_fission_rate"], "SPOT nu_fission_rate")
            fraction = nonnegative(row["global_fraction"], "SPOT global_fraction")
            require(fraction <= 1, "SPOT global_fraction exceeds one")
            result[key] = {"rate": rate, "fraction": fraction}
    complete(result, "SPOT")
    require(math.fsum(row["rate"] for row in result.values()) > 0, "zero SPOT total rate")
    require(math.fsum(row["fraction"] for row in result.values()) > 0, "zero SPOT total fraction")
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"nonfinite JSON constant: {value}")


def read_ce(path):
    with path.open() as stream:
        data = json.load(stream, object_pairs_hook=unique_object, parse_constant=reject_constant)
    require(isinstance(data, dict) and data.get("schema") == "D4A_CORRECTED_CE_RESULT_V1", "wrong CE schema")
    nonnegative(data["keff"], "CE keff")
    nonnegative(data["keff_standard_deviation"], "CE keff_standard_deviation")
    total = nonnegative(data["global_nu_fission"], "CE global_nu_fission")
    require(total > 0, "zero CE total rate")
    require(isinstance(data["bins"], list), "CE bins is not a list")
    result, cells = {}, set()
    for row in data["bins"]:
        require(isinstance(row, dict), "malformed CE bin")
        key = (integer(row["floor"], "CE floor", json_value=True),
               integer(row["pin_index"], "CE pin_index", json_value=True))
        require(key not in result, "duplicate CE floor/pin_index")
        cell = integer(row["fuel_cell_id"], "CE fuel_cell_id", json_value=True)
        ring = integer(row["ring_from_center"], "CE ring_from_center", json_value=True)
        require(cell > 0 and cell not in cells, "duplicate or invalid CE fuel_cell_id")
        require(0 <= ring <= 8, "invalid CE ring_from_center")
        cells.add(cell)
        mean = nonnegative(row["nu_fission"], "CE nu_fission")
        nonnegative(row["nu_fission_std_dev"], "CE nu_fission_std_dev")
        fraction = nonnegative(row["global_fraction"], "CE global_fraction")
        # extract_result writes this single binary64 division to round-trip
        # JSON. Recompute that operation; no adjustable epsilon is needed.
        require(fraction == mean / total, "CE bin global_fraction disagrees with mean / total")
        result[key] = {"rate": mean, "fraction": fraction}
    complete(result, "CE")
    require(total == math.fsum(row["rate"] for row in result.values()),
            "CE global_nu_fission disagrees with math.fsum(bin means)")
    floor_fractions = data["floor_nu_fission_fractions"]
    require(isinstance(floor_fractions, list) and len(floor_fractions) == 3, "invalid CE floor fractions")
    for floor, raw_fraction in enumerate(floor_fractions, 1):
        fraction = nonnegative(raw_fraction, "CE floor fraction")
        floor_rate = math.fsum(row["rate"] for key, row in result.items() if key[0] == floor)
        require(fraction == floor_rate / total, "CE floor fraction disagrees with math.fsum(floor means) / total")
    return result


def compare(spot_path, ce_path):
    spot, ce = read_spot(spot_path), read_ce(ce_path)
    rows = []
    for floor, pin in sorted(KEYS):
        spot_fraction = spot[(floor, pin)]["fraction"]
        ce_fraction = ce[(floor, pin)]["fraction"]
        difference = spot_fraction - ce_fraction
        rows.append(dict(zip(FIELDS, (floor, pin, spot_fraction, ce_fraction, difference, abs(difference)))))
    maximum = max(row["absolute_difference"] for row in rows)
    positions = [row for row in rows if row["absolute_difference"] == maximum]
    floor_summaries = []
    for floor in (1, 2, 3):
        selected = [row for row in rows if row["floor"] == floor]
        floor_summaries.append({
            "floor": floor,
            "spot_global_fraction_sum": math.fsum(row["spot_global_fraction"] for row in selected),
            "ce_global_fraction_sum": math.fsum(row["ce_global_fraction"] for row in selected),
            "spot_minus_ce_sum": math.fsum(row["spot_minus_ce"] for row in selected),
            "maximum_absolute_difference": max(row["absolute_difference"] for row in selected),
        })
    summary = {
        "schema": "D4A_PIN_COMPARISON_DIAGNOSTIC_V1",
        "status": "DIAGNOSTIC_ONLY",
        "accuracy_assessment": "REPORTED_ONLY",
        "rows": len(rows),
        "alignment": "unique complete (floor, pin_index); independent of row order",
        "difference_definition": "SPOT global_fraction minus CE global_fraction",
        "normalization": "input fractions unchanged; no renormalization, clipping, or correction",
        "maximum_absolute_difference": maximum,
        "maximum_absolute_difference_position": {name: positions[0][name] for name in ("floor", "pin_index")},
        "maximum_absolute_difference_ties": len(positions),
        "rms_difference": math.sqrt(math.fsum(row["spot_minus_ce"]**2 for row in rows) / len(rows)),
        "spot_global_fraction_sum": math.fsum(row["spot_global_fraction"] for row in rows),
        "ce_global_fraction_sum": math.fsum(row["ce_global_fraction"] for row in rows),
        "floors": floor_summaries,
        "ce_consistency_method": "exact binary64 equality after replaying producer math.fsum and division; no epsilon",
        "spot_consistency_scope": "IDs and finite nonnegative nu_fission_rate/global_fraction only; first use the existing extraction/conservation chain; no normalization or rate-fraction authentication",
        "uncertainty": "not evaluated: raw nu_fission_std_dev is not normalized-fraction uncertainty; shared-denominator covariance is unavailable",
        "source_authentication": "NOT_PERFORMED; this tool does not replace receipt checks or establish convergence",
        "input_sha256": {"spot_pin_rates": hashlib.sha256(spot_path.read_bytes()).hexdigest(),
                         "ce_reference_result": hashlib.sha256(ce_path.read_bytes()).hexdigest()},
    }
    return rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spot_pin_rates", type=Path)
    parser.add_argument("ce_reference_result", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    rows, summary = compare(args.spot_pin_rates, args.ce_reference_result)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    with (args.output_dir / "pin_comparison.csv").open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    with (args.output_dir / "comparison_summary.json").open("x") as stream:
        json.dump(summary, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print("DIAGNOSTIC_ONLY / REPORTED_ONLY: 651 aligned pin fractions; no accuracy verdict or fraction sigma")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, OverflowError) as exc:
        raise SystemExit(f"D4A PIN COMPARISON INPUT ERROR: {exc}") from exc
