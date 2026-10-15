"""Fresh current-data finite-height responses for one declared original-ray batch.

This worker uses the unchanged sealed physical-source kernel.  It does not use
old Green responses, matched reference inflow, an inverse propagation rule,
POD source coefficients, or a scattering/fission iteration.  Every original
source coordinate and both independent positive controls are swept freshly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation/iterative"))

import numpy as np
from native_layered_cached import aggregate, basis, checks, transport
from native_layered_reference import packed
from native_layered_batch_storage import Collector, scientific
from native_oblique_streaming import ratio
from calibrate_native_oblique_streaming import read, save

OUT = ROOT / "validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005"
GROUPS = [51, 61, 98]
ORDERS = [16, 32]
ORIENTATIONS = [1, -1]
SIGNS = [-1, 1]
CHECK_KEYS = [
    "primitive_relative", "cell_relative", "global_relative", "minimum_angle",
    "minimum_integral", "shared_face_absolute", "geometry_relative",
    "represented_width_relative", "source_assembly_relative",
    "constant_relative", "vacuum_axial_incoming_absolute",
]
ACTION_LIMIT = 5e-12
WALL_LIMIT = 600
RSS_LIMIT_MIB = 512


def scales(response: np.ndarray, nz: int) -> np.ndarray:
    """Original per-coordinate scale over each complete physical output family."""
    result = np.empty_like(response)
    for lo, hi in [(0, 8 * nz), (8 * nz, 14 * nz), (14 * nz, 14 * nz + 16)]:
        result[lo:hi] = abs(response[lo:hi]).max(axis=0)
    return result


def _case(root: Path, case_id: str) -> dict:
    if root != OUT:
        raise ValueError("the declared current-data experiment root is required")
    plan_path = root / "plan.json"
    plan = json.loads(plan_path.read_text())
    matches = [case for case in plan["batches"] if case["id"] == case_id]
    if len(matches) != 1:
        raise ValueError("exactly one declared original-ray batch is required")
    case = matches[0]
    p, height, nz = case["polar"], case["height"], case["nz"]
    first, stop = case["first"], case["stop"]
    if (type(p) is not int or p not in range(4) or height != 20. or nz != 4
            or type(first) is not int or type(stop) is not int
            or first < 0 or stop > 11364 or stop <= first or stop - first > 256
            or first % 256 != 0 or stop != min(first + 256, 11364)
            or case.get("preflight") is not False
            or case_id != f"p{p}_h20_n4_b{first:05d}"):
        raise ValueError("batch dimensions or original index interval differ from declaration")
    admission_path = root / "admission.json"
    if admission_path.exists():
        admission = json.loads(admission_path.read_text())
        if (admission.get("full_execution_admitted") is not True
                or admission.get("plan_sha256") != hashlib.sha256(plan_path.read_bytes()).hexdigest()):
            raise ValueError("the declared full-inventory execution admission is required")
    else:
        # The driver charges this declared maximum-complexity batch exactly
        # once.  Its fresh primary/replay proves bounds before full admission.
        preflight_ids = plan["preflight_batch_ids"]
        if (not isinstance(preflight_ids, list) or len(preflight_ids) != 1
                or case_id != preflight_ids[0]):
            raise ValueError("only the declared admission batch may execute before full admission")
    return case


def _inventory(root: Path) -> dict:
    data = read(root / "inputs/inventory.npz")
    if (data["groups"].tolist() != GROUPS
            or not np.array_equal(data["original_track"], np.arange(11364))
            or not np.array_equal(data["original_record_multiplicity"], np.ones(11364, dtype="u1"))
            or data["group_totals"].shape != (3, 8)
            or not np.isfinite(data["group_totals"]).all()
            or data["group_totals"].min() < 0):
        raise ValueError("all original ray indices and the current three-group physical totals are required")
    return data


def main(root: Path, case_id: str, phase: str) -> None:
    tick = time.perf_counter()
    if phase not in ["primary", "replay"]:
        raise ValueError("primary or replay phase required")
    case = _case(root, case_id)
    data = _inventory(root)
    p, height, nz = case["polar"], case["height"], case["nz"]
    tracks = np.arange(case["first"], case["stop"], dtype=np.int64)
    nt = len(tracks)
    k, nout = 14 * nz + 10, 14 * nz + 16
    library = root / "runtime/cached.dylib"
    defaults = [basis(nz, sigma) for sigma in data["group_totals"]]
    declared_counts = read(root / f"inputs/counts_p{p}_h20_n4.npz")
    np.testing.assert_array_equal(declared_counts["original_tracks"], np.arange(11364))
    collectors = {(gi, oi, si): Collector()
                  for gi in range(3) for oi in range(2) for si in range(2)}
    check_values = np.zeros((nt, 3, 2, 2, 2, len(CHECK_KEYS)))
    convergence = np.zeros((nt, 3, 2, 2, 3))
    full_field_convergence = np.zeros((nt, 3, 2, 2))
    local_field_convergence_by_component = np.zeros((nt, 3, 2, 2, 9))
    operators = np.zeros((2, 3, 2, 2, nout, k))
    jx = np.zeros((2, 3, 2, 2, 8 * nz, k))
    abs_jx = np.zeros_like(jx)
    geometry_counts = np.zeros((nt, 2, 2, 2, 3), np.int64)
    physical_seconds = 0.
    updates = 0
    completed_states = 0

    for ti, track in enumerate(tracks):
        nr = int(data["nseg"][track] - 2)
        if nr < 1 or nr > 15:
            raise ValueError("invalid original ray region count")
        width = data["planar_widths"][track, :nr] * data["zmu"][p]
        regions = data["nom"][track, 1:nr + 1] - 1
        weight = data["wei"][track] * data["wzmu"][p] / 2
        mx = data["harm"][p, 2, data["angle"][track]]
        for oi, orientation in enumerate(ORIENTATIONS):
            entry = int(data["entry_surface"][track] if orientation == 1
                        else data["exit_surface"][track])
            exit_surface = int(data["exit_surface"][track] if orientation == 1
                               else data["entry_surface"][track])
            for si, sign in enumerate(SIGNS):
                mu = float(sign * np.sqrt(1 - 1 / data["zmu"][p] ** 2))
                low_fields = []
                low_responses = []
                # Geometry is the sealed library's single-entry cache key.
                # Keep the order outside the group loop so every fresh total
                # and source coordinate shares only its identical geometry.
                for qi, order in enumerate(ORDERS):
                    for gi, sigma in enumerate(data["group_totals"]):
                        started = time.perf_counter()
                        result = transport(library, width, regions, sigma, entry,
                                           height, nz, mu, orientation, order,
                                           *defaults[gi])
                        physical_seconds += time.perf_counter() - started
                        completed_states += 1
                        counts = result["geometry"][:3]
                        if (not np.isfinite(counts).all()
                                or not np.array_equal(counts, counts.astype(np.int64))
                                or counts.min() <= 0):
                            raise ValueError("original physical geometry counts are invalid")
                        if gi == 0:
                            geometry_counts[ti, oi, si, qi] = counts
                        else:
                            np.testing.assert_array_equal(counts, geometry_counts[ti, oi, si, qi])
                        if qi == 1:
                            expected = geometry_counts[ti, oi, si, 0].copy()
                            expected[1:] *= 2
                            np.testing.assert_array_equal(counts, expected)
                        independent_counts = declared_counts["counts"][si, oi, 1, track].copy()
                        independent_counts[1:] *= order // 16
                        np.testing.assert_array_equal(counts, independent_counts)
                        row = checks(result, width, regions, sigma, height, nz, mu)
                        if not row["passed"]:
                            save(root / "runs" / f"{phase}_{case_id}_failed.json",
                                 dict(track=int(track), group=GROUPS[gi],
                                      orientation=orientation, sign=sign, order=order, checks=row))
                            raise RuntimeError("unchanged original physical-coordinate gate failed")
                        check_values[ti, gi, oi, si, qi] = [row[key] for key in CHECK_KEYS]
                        response = packed(aggregate(result["fields"], regions, nz,
                                                    orientation, exit_surface))
                        if response.shape != (nout, k):
                            raise ValueError("complete physical output/source coordinate matrix required")
                        updates += int(counts[2]) * k
                        operators[qi, gi, si, oi] += weight * response
                        jx[qi, gi, si, oi] += weight * orientation * mx * response[:8 * nz]
                        abs_jx[qi, gi, si, oi] += weight * abs(mx) * response[:8 * nz]
                        if order == 16:
                            low_fields.append(result["fields"].copy())
                            low_responses.append(response.copy())
                        else:
                            error = ratio(response - low_responses[gi], scales(response, nz))
                            convergence[ti, gi, oi, si] = [
                                float(error[:8 * nz].max()),
                                float(error[8 * nz:14 * nz].max()),
                                float(error[14 * nz:].max()),
                            ]
                            # Every local region-layer and every input/output
                            # face is compared, before any geometric aggregation.
                            field_error = ratio(result["fields"] - low_fields[gi],
                                                abs(result["fields"]).max(axis=(0, 1)))
                            full_field_convergence[ti, gi, oi, si] = float(field_error.max())
                            local_field_convergence_by_component[ti, gi, oi, si] = field_error.max(axis=(0, 2))
                            if max(float(error.max()), float(field_error.max())) >= ACTION_LIMIT:
                                save(root / "runs" / f"{phase}_{case_id}_failed.json",
                                     dict(track=int(track), group=GROUPS[gi], orientation=orientation,
                                          sign=sign, packed_order_relative=float(error.max()),
                                          complete_local_field_order_relative=float(field_error.max())))
                                raise RuntimeError("unchanged whole-coordinate offset-order gate failed")
                            collectors[gi, oi, si].add(int(track), result, response, regions,
                                                       nz, entry, exit_surface, sign)
                if time.perf_counter() - tick >= WALL_LIMIT:
                    raise RuntimeError("original worker wall cap exceeded")

    if completed_states != nt * 3 * 2 * 2 * 2:
        raise ValueError("every declared original-index physical state must occur once per order")
    receipt = {}
    for (gi, oi, si), collector in collectors.items():
        arrays = collector.arrays()
        np.testing.assert_array_equal(arrays["original_tracks"], tracks)
        scientific(root, phase, case_id,
                   f"raw_g{GROUPS[gi]}_o{ORIENTATIONS[oi]}_m{SIGNS[si]}.npz", arrays, receipt)
        del arrays
    scientific(root, phase, case_id, "operators.npz",
               dict(original_tracks=tracks, operators=operators, jx=jx, abs_jx=abs_jx), receipt)
    scientific(root, phase, case_id, "controls.npz",
               dict(original_tracks=tracks, checks=check_values, convergence=convergence,
                    full_field_convergence=full_field_convergence,
                    local_field_convergence_by_component=local_field_convergence_by_component,
                    geometry_counts=geometry_counts), receipt)
    summary = dict(
        case=case,
        scope="Fresh current-data full physical source-coordinate finite-height responses only.",
        original_records=nt,
        physical_states=completed_states,
        physical_coordinate_evaluations=completed_states * k,
        physical_coordinates=14 * nz + 8,
        separately_swept_positive_controls=2,
        physical_piece_column_updates=updates,
        full_order32_responses_retained=True,
        all_declared_original_indices_once_per_group_direction_order=True,
        complete_local_fields_checked_before_aggregation=True,
        physical_gate_maxima={key: float(check_values[..., i].max())
                             for i, key in enumerate(CHECK_KEYS) if not key.startswith("minimum")},
        minimum_angle=float(check_values[..., 3].min()),
        minimum_integral=float(check_values[..., 4].min()),
        full_coordinate_order16_order32_relative=float(convergence.max()),
        complete_local_field_order16_order32_relative=float(full_field_convergence.max()),
        geometric_count_order_scaling_exact=True,
        current_totals_used=True,
        old_totals_reused=False,
        old_green_responses_reused=False,
        matched_reference_inflow_used=False,
        old_zero_gradient_regression_claimed=False,
        scattering_fission_iteration_qualified=False,
        axial_model_qualified=False,
        AAA_accuracy_qualified=False,
        ABA_admitted=False,
        all_checks_passed=bool(convergence.max() < ACTION_LIMIT
                               and full_field_convergence.max() < ACTION_LIMIT),
    )
    scientific(root, phase, case_id, "result.json", summary, receipt)
    folder = root / "receipts" / phase
    folder.mkdir(parents=True, exist_ok=True)
    save(folder / (case_id + ".json"),
         dict(files=receipt, all_scientific_bytes_identical=phase == "replay"))
    usage = dict(
        elapsed_seconds=time.perf_counter() - tick,
        peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 2,
        physical_kernel_seconds=physical_seconds,
        output_bytes=sum(item["bytes"] for item in receipt.values()),
    )
    save(root / "runs" / f"{phase}_{case_id}_resources.json", usage)
    if not summary["all_checks_passed"]:
        raise RuntimeError("declared complete-field convergence gate failed")
    if usage["elapsed_seconds"] >= WALL_LIMIT or usage["peak_rss_mib"] >= RSS_LIMIT_MIB:
        raise RuntimeError("unchanged original worker resource cap exceeded: " + repr(usage))
    print(case_id, phase, usage, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("case")
    parser.add_argument("phase", choices=["primary", "replay"])
    arguments = parser.parse_args()
    main(arguments.root.resolve(), arguments.case, arguments.phase)
