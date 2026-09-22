#!/usr/bin/env python3
"""Map and check saved D4-A SAL topology against the frozen CE integer lattice.

No tracking or transport is performed. The coordinate admission resolution is
the frozen SAL input's existing endpoint-unification EPS, never a fitted
nearest-neighbour tolerance. It is not a floating-point propagation bound.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[2]
GEOMETRY = ROOT / "data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat"
GEOMETRY_SHA = "ca46ef77ea769059ddc612f1a78e4b565c32990401b21652c822bf2e11497a3e"


class CrosswalkFailure(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CrosswalkFailure(message)


def read_saved(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "D4A_SAVED_PIN_GEOMETRY_V1" and lines[-1] == "END",
            "incomplete saved geometry export")
    snapshots = []
    for line in lines[1:-1]:
        p = line.split()
        if p[0] == "SNAPSHOT":
            require(list(map(int, p[2:])) == [2268, 132, 3, 6], "unexpected saved geometry dimensions")
            require(int(p[1]) == len(snapshots) + 1, "snapshot sequence mismatch")
            snapshots.append({"regions": {}, "elements": []})
        elif p[0] == "REGION":
            require(len(p) == 7 and snapshots, "malformed REGION")
            region, material, merge = map(int, p[1:4])
            values = tuple(map(float, p[4:]))
            require(region not in snapshots[-1]["regions"], "duplicate region")
            require(all(math.isfinite(v) and v > 0 for v in values), "invalid region area")
            snapshots[-1]["regions"][region] = (material, merge, *values)
        elif p[0] == "ELEMENT":
            require(len(p) == 11 and snapshots, "malformed ELEMENT")
            element, kind, left, right = map(int, p[1:5])
            values = tuple(map(float, p[5:]))
            require(element == len(snapshots[-1]["elements"]) + 1, "element sequence mismatch")
            require(all(map(math.isfinite, values)), "nonfinite geometry descriptor")
            snapshots[-1]["elements"].append((element, kind, left, right, *values))
        else:
            raise CrosswalkFailure("unexpected export record")
    require(len(snapshots) == 3, "expected three saved TRACK snapshots")
    require(snapshots[0] == snapshots[1] == snapshots[2], "saved radial geometry changes between floors")
    snapshot = snapshots[0]
    require(set(snapshot["regions"]) == set(range(1, 133)), "incomplete region coverage")
    require(len(snapshot["elements"]) == 2268, "incomplete active element coverage")
    for region, (_, merge, volume, nodevol, mergevol) in snapshot["regions"].items():
        require(merge == region, "nonidentity NumMerge is outside this frozen crosswalk")
        require(nodevol == mergevol, "VOL_NODE/VolMerge mismatch")
        require(struct.unpack("f", struct.pack("f", nodevol))[0] == volume,
                "TRACK VOLUME is not the saved node area rounded to REAL32")
    return snapshot


def reference_and_resolution(geometry=GEOMETRY):
    data = geometry.read_bytes()
    require(hashlib.sha256(data).hexdigest() == GEOMETRY_SHA, "frozen geometry hash mismatch")
    match = re.search(rb"\*\s+eps\s+eps0\s*\n\s*([0-9.E+\-]+)\s+([0-9.E+\-]+)", data)
    require(match is not None, "missing declared SAL EPS")
    eps = float(match[1])
    require(eps > 0 and eps == float(match[2]), "unexpected frozen EPS/eps0")
    # SAL100 reads DATARE and stores EPS as default REAL (REAL32).
    eps = struct.unpack("f", struct.pack("f", eps))[0]
    spec = importlib.util.spec_from_file_location("d4a_ce_crosswalk_reference",
                                                Path(__file__).with_name("build_d4a_ce_reference.py"))
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    return reference, eps


def unique_lattice_center(x, y, candidates, resolution):
    matches = [key for key, record in candidates.items()
               if math.hypot(x - record["sal_x"], y - record["sal_y"]) <= resolution]
    require(len(matches) == 1, f"saved center ({x}, {y}) has {len(matches)} admitted lattice candidates")
    return matches[0]


def sal_boundary_area(part):
    """Independent transcription of saved-surface integral SAL161 (no solve)."""
    _, kind, _, _, _, yc, radius_or_dx, phi1_or_dy, phi2, _ = part
    if kind == 1:
        return radius_or_dx * (yc + phi1_or_dy / 2)
    if kind == 2:
        # precision_and_kinds.f90 declares double PI with an unsuffixed
        # literal, hence the real32-rounded literal is promoted to double.
        # Reproduce that saved-geometry convention, not the CE ideal area.
        sal_pi = struct.unpack("f", struct.pack("f", 3.14159265358979))[0]
        return sal_pi * radius_or_dx**2
    require(kind == 3, "unknown SAL surface type")
    radius, phi1 = radius_or_dx, phi1_or_dy
    c1, c2 = math.cos(phi1), math.cos(phi2)
    return radius * (yc * (c1 - c2) + radius / 2 *
                     (phi2 - phi1 + math.sin(phi1) * c1 - math.sin(phi2) * c2))


def verify_circle(parts, radius, resolution):
    """Require one complete boundary using the same declared length resolution."""
    angle_bound = 2 * math.asin(resolution / radius)
    if any(p[1] == 2 for p in parts):
        require(len(parts) == 1 and parts[0][1] == 2, "duplicate full circle boundary")
        return
    intervals = sorted((p[7], p[8]) for p in parts)
    require(intervals and all(0 <= b - a <= 2 * math.pi + angle_bound for a, b in intervals),
            "invalid arc span")
    previous = intervals[0][0]
    for start, end in intervals:
        require(abs(start - previous) <= angle_bound,
                f"gap or overlap in saved pin boundary: {intervals}")
        previous = end
    require(abs(previous - intervals[0][0] - 2 * math.pi) <= angle_bound,
            "saved pin boundary does not close")


def build_crosswalk(snapshot, reference, resolution):
    regions, elements = snapshot["regions"], snapshot["elements"]
    fuel = {region for region, values in regions.items() if values[0] == 4}
    require(len(fuel) == 25, "expected 25 material-4 fuel regions")
    require(2 * resolution < reference.PIN_PITCH_CM, "declared resolution cannot distinguish pin centers")
    # The unique minimum fuel orbit area identifies the one-pin center; the
    # saved boundary closure and full 217-site coverage below independently
    # test this choice, rather than trusting a hard-coded central region.
    center_region = min(fuel, key=lambda region: regions[region][2])
    require(sum(regions[r][2] == regions[center_region][2] for r in fuel) == 1,
            "ambiguous central fuel orbit")
    central_parts = [p for p in elements if center_region in p[2:4]]
    require(central_parts and all(p[1] in (2, 3) for p in central_parts), "noncircular central fuel topology")
    center = tuple((min(p[4 + axis] for p in central_parts) +
                    max(p[4 + axis] for p in central_parts)) / 2 for axis in range(2))
    indices = reference.lattice_index_map(reference.PIN_RINGS + 1)
    candidates = {}
    pin_index = 0
    for openmc_ring in range(reference.PIN_RINGS + 1):
        for within in range(max(6 * (reference.PIN_RINGS - openmc_ring), 1)):
            x_index, alpha, ring = indices[(openmc_ring, within)]
            ce_x = math.sqrt(0.75) * reference.PIN_PITCH_CM * x_index
            ce_y = (0.5 * x_index + alpha) * reference.PIN_PITCH_CM
            # Explicit orientation: CE = rotate(+90 degrees) * (SAL-center).
            candidates[(x_index, alpha)] = dict(pin_index=pin_index, x_index=x_index,
                alpha_index=alpha, openmc_ring_index=openmc_ring, openmc_i_within=within,
                ring_from_center=ring, ce_x_cm=ce_x, ce_y_cm=ce_y,
                sal_x=center[0] + ce_y, sal_y=center[1] - ce_x)
            pin_index += 1
    require(pin_index == 217, "CE reference is not a 217-pin lattice")
    grouped = defaultdict(lambda: defaultdict(list))
    owners = {}
    maximum_residual = 0.0
    for part in elements:
        adjacent_fuel = fuel.intersection(part[2:4])
        if not adjacent_fuel:
            continue
        require(len(adjacent_fuel) == 1 and part[1] in (2, 3), "unexpected fuel boundary topology")
        region = next(iter(adjacent_fuel))
        # IPAR(2) is the circle interior; IPAR(3) is the exterior.
        outer = part[2] == region
        expected_radius = reference.R_FUEL_CM if outer else reference.R_HOLE_CM
        require(abs(part[6] - expected_radius) <= resolution, "fuel boundary radius mismatch")
        key = unique_lattice_center(part[4], part[5], candidates, resolution)
        maximum_residual = max(maximum_residual,
            math.hypot(part[4] - candidates[key]["sal_x"], part[5] - candidates[key]["sal_y"]))
        require(key not in owners or owners[key] == region, "one physical pin has two radial fuel labels")
        owners[key] = region
        grouped[(region, key)][outer].append(part)
    require(set(owners) == set(candidates), "saved topology does not cover all 217 CE sites")
    require({r for r, _ in grouped} == fuel, "fuel orbit is absent from saved geometry")
    multiplicities = Counter(owners.values())
    require(multiplicities[center_region] == 1, "minimum-area region is not the central pin")
    require(Counter(multiplicities.values()) == Counter({12: 12, 6: 12, 1: 1}),
            "saved topology has unexpected symmetry orbit multiplicities")
    for (_, _), boundaries in grouped.items():
        require(set(boundaries) == {False, True}, "missing inner or outer fuel boundary")
        verify_circle(boundaries[True], reference.R_FUEL_CM, resolution)
        verify_circle(boundaries[False], reference.R_HOLE_CM, resolution)
    reconstructed = defaultdict(list)
    for part in elements:
        integral = sal_boundary_area(part)
        if part[2] in fuel:
            reconstructed[part[2]].append(integral)
        if part[3] in fuel:
            reconstructed[part[3]].append(-integral)
    maximum_area_residual = 0.0
    for region in fuel:
        area = math.fsum(reconstructed[region])
        require(struct.unpack("f", struct.pack("f", area))[0] == regions[region][2],
                "independent saved-boundary area does not reproduce TRACK REAL32 area")
        maximum_area_residual = max(maximum_area_residual, abs(area - regions[region][3]))
    rows = []
    for key, record in sorted(candidates.items(), key=lambda item: item[1]["pin_index"]):
        region = owners[key]
        area = regions[region][2]
        rows.append(dict(radial_region=region, **record, orbit_multiplicity=multiplicities[region],
                         orbit_area=area, per_pin_area=area / multiplicities[region]))
    orbit_area = math.fsum(regions[r][2] for r in fuel)
    expanded_area = math.fsum(row["per_pin_area"] for row in rows)
    require(abs(expanded_area - orbit_area) <= math.ulp(orbit_area), "pin expansion does not conserve TRACK area")
    checks = dict(classification="SAVED_GEOMETRY_CROSSWALK_DIAGNOSTIC_ONLY",
        source_state="not inferred from geometry; diagnostic only",
        snapshots_identical=True, active_elements=2268, fuel_orbits=25, physical_pins=217,
        orbit_multiplicities={str(r): multiplicities[r] for r in sorted(fuel)},
        geometry_input_sha256=GEOMETRY_SHA, coordinate_resolution_cm=resolution,
        coordinate_input_printed_eps_cm=1e-5,
        coordinate_resolution_origin="frozen .dat EPS; SAL100 endpoint unification and SAL128 geometry adjustment",
        coordinate_resolution_caveat="existing geometric resolution, not a proved floating-point propagation error bound",
        matching="unique admission within declared SAL EPS; no nearest-neighbour fallback",
        coordinate_transform="x_CE = -(y_SAL-center_y); y_CE = x_SAL-center_x (rotation +90 degrees)",
        center_radial_region=center_region, saved_center_cm=center,
        maximum_center_residual_cm=maximum_residual,
        minimum_lattice_center_separation_cm=reference.PIN_PITCH_CM,
        all_inner_and_outer_pin_boundaries_closed=True,
        track_fuel_orbit_area_sum=orbit_area, expanded_pin_area_sum=expanded_area,
        geometry_fuel_node_area_sum=math.fsum(regions[r][3] for r in fuel),
        nominal_ce_fuel_area_sum=217 * math.pi * (reference.R_FUEL_CM**2 - reference.R_HOLE_CM**2),
        volume_semantics="TRACK VOLUME is full unfolded orbit area; per_pin_area=VOLUME/multiplicity; never multiply by 12",
        track_volume_is_real32_rounded_node_area=True, node_volume_equals_volmerge=True)
    checks["independent_surface_area_reproduces_track_real32"] = True
    checks["maximum_surface_area_vs_vol_node_residual_cm2"] = maximum_area_residual
    checks["surface_area_pi_convention"] = "SAL REAL32 literal PI promoted to REAL64, matching precision_and_kinds.f90"
    return rows, checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry-export", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    reference, resolution = reference_and_resolution()
    rows, checks = build_crosswalk(read_saved(args.geometry_export), reference, resolution)
    checks["geometry_export_sha256"] = hashlib.sha256(args.geometry_export.read_bytes()).hexdigest()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "pin_crosswalk.csv"
    checks_path = args.output_dir / "geometry_checks.json"
    require(not csv_path.exists() and not checks_path.exists(), "refusing to replace existing crosswalk outputs")
    with csv_path.open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with checks_path.open("x") as stream:
        stream.write(json.dumps(checks, indent=2, sort_keys=True) + "\n")
    print("D4A SAVED GEOMETRY CROSSWALK: 25 orbits -> 217 unique CE pins; diagnostic only")


if __name__ == "__main__":
    try:
        main()
    except (CrosswalkFailure, OSError, ValueError, IndexError) as exc:
        raise SystemExit(f"D4A PIN CROSSWALK FAIL: {exc}") from exc
