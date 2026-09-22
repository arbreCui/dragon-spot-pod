#!/usr/bin/env python3
"""Expand diagnosed regional nu-fission rates without changing normalization.

This is a read-only postprocessor, not a convergence or physics-accuracy gate.
The geometric crosswalk must first pass build_d4a_pin_crosswalk.py.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from fractions import Fraction
import json
import math
from pathlib import Path
import struct


PIN_FIELDS = (
    "floor", "pin_index", "x_index", "alpha_index", "radial_region",
    "orbit_multiplicity", "volume", "nu_fission_rate", "global_fraction",
)


def rows(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        names = reader.fieldnames or []
        if len(names) != len(set(names)) or not required.issubset(names):
            raise ValueError(f"invalid CSV fields: {path}")
        result = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in result):
        raise ValueError(f"malformed CSV row: {path}")
    return result


def positive(value: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError("nonpositive or nonfinite physical value")
    return result


def real32(value: float) -> float:
    return struct.unpack("f", struct.pack("f", value))[0]


def divided(value: float, count: int) -> float:
    result = value / count
    if result <= 0 or not math.isfinite(result):
        raise ValueError("invalid per-pin quantity")
    # Exact rational comparison: only one correctly-rounded binary64 division.
    # This half-ULP bound is not an adjustable numerical or physical tolerance.
    error = abs(count * Fraction(result) - Fraction(value))
    bound = count * Fraction(math.ulp(result)) / 2
    if error > bound:
        raise ValueError("orbit distribution exceeds division roundoff")
    return result


def expand(crosswalk: Path, regional: Path) -> tuple[list[dict], dict]:
    pins = rows(crosswalk, {
        "radial_region", "pin_index", "x_index", "alpha_index",
        "orbit_multiplicity", "orbit_area", "per_pin_area",
    })
    rates = rows(regional, {
        "radial_region", "floor", "material", "volume",
        "nu_fission_rate", "global_fraction",
    })
    if len(pins) != 217 or len(rates) != 75:
        raise ValueError("expected 217 pins and 3 x 25 fuel-region rates")
    orbits = defaultdict(list)
    seen_pins, seen_coordinates = set(), set()
    for row in pins:
        region = int(row["radial_region"])
        pin = int(row["pin_index"])
        coordinate = (int(row["x_index"]), int(row["alpha_index"]))
        count = int(row["orbit_multiplicity"])
        area = positive(row["orbit_area"])
        if not 1 <= region <= 132 or count not in (1, 6, 12):
            raise ValueError("invalid D4-A radial region or symmetry multiplicity")
        if pin in seen_pins or coordinate in seen_coordinates:
            raise ValueError("duplicate pin or lattice coordinate")
        if real32(area) != area or positive(row["per_pin_area"]) != divided(area, count):
            raise ValueError("area is not the saved REAL32 orbit area divided by multiplicity")
        seen_pins.add(pin)
        seen_coordinates.add(coordinate)
        orbits[region].append((pin, coordinate, count, area))
    if seen_pins != set(range(217)) or len(orbits) != 25:
        raise ValueError("pin IDs or fuel orbit count are incomplete")
    for orbit in orbits.values():
        if any((item[2], item[3]) != (len(orbit), orbit[0][3]) for item in orbit):
            raise ValueError("orbit multiplicity or area is inconsistent")
    if sorted(map(len, orbits.values())) != [1] + [6] * 12 + [12] * 12:
        raise ValueError("unexpected D4-A symmetry orbit inventory")

    seen_rates = set()
    output = []
    original = defaultdict(list)
    for row in rates:
        region, floor = int(row["radial_region"]), int(row["floor"])
        key = (region, floor)
        if key in seen_rates or region not in orbits or floor not in (1, 2, 3):
            raise ValueError("duplicate or unmatched region/floor rate")
        if int(row["material"]) != 4 + 6 * (floor - 1):
            raise ValueError("incorrect floor fuel material")
        volume = positive(row["volume"])
        rate = positive(row["nu_fission_rate"])
        fraction = positive(row["global_fraction"])
        orbit = orbits[region]
        if volume != real32(orbit[0][3] * 50.0):
            raise ValueError("rate volume does not match saved orbit area x 50 cm")
        per_pin = tuple(divided(value, len(orbit)) for value in (volume, rate, fraction))
        seen_rates.add(key)
        original[floor].append((volume, rate, fraction))
        for pin, (x_index, alpha), count, _ in orbit:
            output.append(dict(zip(PIN_FIELDS, (
                floor, pin, x_index, alpha, region, count, *per_pin,
            ))))
    if seen_rates != {(region, floor) for region in orbits for floor in (1, 2, 3)}:
        raise ValueError("incomplete region/floor coverage")
    output.sort(key=lambda row: (row["floor"], row["pin_index"]))

    checks = []
    for floor in (1, 2, 3):
        after = [row for row in output if row["floor"] == floor]
        for column, name in enumerate(("volume", "nu_fission_rate", "global_fraction")):
            before_exact = sum((Fraction(row[column]) for row in original[floor]), Fraction())
            after_exact = sum((Fraction(row[name]) for row in after), Fraction())
            bound = sum((Fraction(math.ulp(row[name])) / 2 for row in after), Fraction())
            if abs(after_exact - before_exact) > bound:
                raise ValueError("floor conservation exceeds accumulated division roundoff")
            checks.append({"floor": floor, "quantity": name,
                           "before": float(before_exact), "after": float(after_exact),
                           "absolute_difference": float(abs(after_exact - before_exact)),
                           "division_roundoff_bound": float(bound)})
    return output, {
        "status": "DIAGNOSTIC_ONLY", "pins": 217, "floors": 3, "rows": len(output),
        "normalization": "unchanged regional global fractions; no renormalization",
        "quantity": "nu-fission, not absolute thermal power",
        "global_fraction_sum": math.fsum(row["global_fraction"] for row in output),
        "conservation": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("crosswalk", type=Path)
    parser.add_argument("regional_rates", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    output, checks = expand(args.crosswalk, args.regional_rates)
    with args.output_csv.open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=PIN_FIELDS)
        writer.writeheader()
        writer.writerows(output)
    print(json.dumps(checks, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
