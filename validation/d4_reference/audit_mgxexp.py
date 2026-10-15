#!/usr/bin/env python3
"""Report raw MGXEXP scattering consistency without changing cross sections.

This diagnostic uses only the standard library. It neither builds an OpenMC
model nor imports a transport solver. SCATTER records are (source, destination).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


class Reader:
    def __init__(self, text: str):
        self.lines = iter(text.splitlines())

    def line(self) -> str:
        try:
            return next(self.lines).strip()
        except StopIteration as exc:
            raise ValueError("truncated MGXEXP input") from exc

    def expect(self, expected: str) -> None:
        actual = self.line()
        if actual != expected:
            raise ValueError(f"expected {expected!r}, found {actual!r}")

    def values(self, count: int) -> list[float]:
        values = []
        while len(values) < count:
            values.extend(float(x.replace("D", "E")) for x in self.line().split())
        if len(values) != count or not all(math.isfinite(x) for x in values):
            raise ValueError("invalid vector length or nonfinite input")
        return values


def audit(text: str) -> tuple[dict, list[dict]]:
    reader = Reader(text)
    reader.expect("MGXEXP 1")
    tag, *dims = reader.line().split()
    if tag != "DIM" or len(dims) != 4:
        raise ValueError("invalid dimension record")
    groups, mixtures, orders, fissions = map(int, dims)
    if min(groups, mixtures, orders) < 1 or fissions < 0:
        raise ValueError("invalid dimensions")
    reader.expect("ENERGY_EV_DESCENDING")
    energy = reader.values(groups + 1)
    if not all(a > b >= 0 for a, b in zip(energy, energy[1:])):
        raise ValueError("energy boundaries must decrease")
    rows, negative_count, negative_mass = [], 0, []
    for material in range(1, mixtures + 1):
        if reader.line().split() != ["MATERIAL", str(material)]:
            raise ValueError("invalid material order")
        vectors = {}
        for key in ("TOTAL", "ABSORPTION", "SCATTER_SUM", "EXCESS_MULTIPLICITY"):
            reader.expect(key)
            vectors[key] = reader.values(groups)
        for component in range(1, fissions + 1):
            if reader.line().split() != ["FISSION_COMPONENT", str(component)]:
                raise ValueError("invalid fission component")
            for key in ("NU_SIGF", "CHI"):
                reader.expect(key)
                reader.values(groups)
        outgoing = [[] for _ in range(groups)]
        incoming = [[] for _ in range(groups)]
        for order in range(orders):
            if reader.line().split() != ["SCATTER", str(order)]:
                raise ValueError("invalid scattering order")
            seen = set()
            while (line := reader.line()) != "END_SCATTER":
                source, destination, raw = line.split()
                source, destination = int(source), int(destination)
                value = float(raw.replace("D", "E"))
                if not (1 <= source <= groups and 1 <= destination <= groups):
                    raise ValueError("scattering index outside group range")
                if not math.isfinite(value) or (source, destination) in seen:
                    raise ValueError("nonfinite or duplicate scattering entry")
                seen.add((source, destination))
                if order == 0:
                    outgoing[source - 1].append(value)
                    incoming[destination - 1].append(value)
                    if value < 0:
                        negative_count += 1
                        negative_mass.append(-value)
        reader.expect("END_MATERIAL")
        for group in range(groups):
            declared = vectors["SCATTER_SUM"][group]
            production = math.fsum(outgoing[group])
            delta = production - declared
            excess = vectors["EXCESS_MULTIPLICITY"][group]
            rows.append({
                "material": material, "source_group": group + 1,
                "energy_upper_eV": energy[group], "energy_lower_eV": energy[group + 1],
                "total": vectors["TOTAL"][group], "sigs00": declared,
                "p0_outgoing_sum": production, "p0_incoming_sum": math.fsum(incoming[group]),
                "p0_minus_sigs00": delta,
                "relative_difference": delta / max(abs(declared), 1e-12),
                "excess_multiplicity": excess,
                "delta_minus_excess": delta - excess, "delta_plus_excess": delta + excess,
                "absorption": vectors["ABSORPTION"][group],
                "absorption_identity_difference": vectors["ABSORPTION"][group] -
                    (vectors["TOTAL"][group] - declared + excess),
            })
    reader.expect("END_MGXEXP")
    if any(line.strip() for line in reader.lines):
        raise ValueError("trailing MGXEXP data")
    worst = max(rows, key=lambda row: abs(row["p0_minus_sigs00"]))
    relative = max(rows, key=lambda row: abs(row["relative_difference"]))
    summary = {
        "classification": "RAW_DATA_DIAGNOSTIC_ONLY",
        "groups": groups, "mixtures": mixtures, "orders": orders,
        "fission_components": fissions, "rows": len(rows),
        "maximum_absolute_difference": abs(worst["p0_minus_sigs00"]),
        "maximum_relative_difference": abs(relative["relative_difference"]),
        "worst_absolute_row": worst, "worst_relative_row": relative,
        "maximum_difference_if_transposed": max(abs(r["p0_incoming_sum"] - r["sigs00"]) for r in rows),
        "maximum_delta_minus_excess": max(abs(r["delta_minus_excess"]) for r in rows),
        "maximum_delta_plus_excess": max(abs(r["delta_plus_excess"]) for r in rows),
        "negative_p0_entries": negative_count, "negative_p0_absolute_sum": math.fsum(negative_mass),
        "limits": "No renormalization, clipping, model construction, transport, or accuracy gate. "
                  "Multiplicity and transpose comparisons are diagnostics, not corrections.",
    }
    return summary, rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, help="new diagnostic directory")
    args = parser.parse_args()
    raw = args.input.read_bytes()
    summary, rows = audit(raw.decode("ascii"))
    summary["input_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.mkdir(parents=True, exist_ok=False)
    with (args.output / "group_balance.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = json.dumps(summary, indent=2, allow_nan=False) + "\n"
    (args.output / "summary.json").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
