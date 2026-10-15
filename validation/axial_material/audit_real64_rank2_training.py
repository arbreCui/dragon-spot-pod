#!/usr/bin/env python3
"""Read the closed REAL64 training and replay all 370 spectra independently.

The actual tool's nonzero return and its metadata-reader error are retained.
This audit does not execute Dragon, train another basis or start a case solve.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct

import numpy as np

from production_runner import require_file, sha256, parse_rank_admission, dump_json
from snapshot_control_preflight import _open_xsm
from run_real64_common_rank2_training import check_provenance


def items(a, directory, name, count):
    raw = a.record(directory, name, count, 10)
    return [a.directory(offset) for offset in struct.unpack(f"<{count}i", raw)]


def slots(a, directory, name, count):
    result = []
    for item in items(a, directory, name, count):
        handle = item["***HANDLE***"]
        if handle[1:] != (-1, 0):
            raise ValueError(f"{name}: expected directory-valued slot")
        result.append(a.directory(handle[0]))
    return result


def audit(build_root: Path, training_root: Path, output: Path) -> dict:
    if output.exists():
        raise ValueError("fresh audit result required")
    closed = json.loads((build_root / "Root_actual_experiment_tool_terminal_return.json").read_text())
    if (closed["closed"] is not True or closed["session_repolled_after_close"] is not False
            or closed["terminal_tool_return"].get("exit_code") != 2
            or "session_id" in closed["terminal_tool_return"]):
        raise ValueError("actual closed exit2 is required, never replaced by an inferred zero")
    original = json.loads((training_root / "run_status.json").read_text())
    stage = json.loads((training_root / "training/stages.json").read_text())["stages"]
    if [(r["label"], r["status"]) for r in stage] != [
        ("archives/pack_archives", "PASS"), ("training/common_basis", "PASS"),
        ("training/rank_precision", "PASS")]:
        raise ValueError("all three actual native stages must have passed")
    for folder in ("archives", "training"):
        sealed = json.loads((training_root / folder / "result.json").read_text())
        if sealed["classification"] != "SEALED_STAGE_OUTPUTS":
            raise ValueError("closed stage seal required")
        for name, digest in sealed["sha256"].items():
            require_file(training_root / folder / name, digest)
    fixed = {}
    for item in original["runtime_and_input_pins"].values():
        require_file(Path(item["path"]), item["sha256"])
        fixed[item["path"]] = item["sha256"]
    for name in ("SPOASM.f", "SPOPOD.f90", "run_real64_rank2_experiment.py",
                 "run_real64_common_rank2_training.py"):
        saved = build_root / "actual_executed_source" / name
        original_path = (Path("/Users/wen/spot/src") / name if name.endswith((".f", ".f90"))
                         else Path("/Users/wen/spot/validation/axial_material") / name)
        digest = json.loads((build_root / "experiment.json").read_text())["full_input_sha256"][str(original_path)]
        require_file(saved, digest)
        fixed[str(saved)] = digest
    basis_path = training_root / "training/common_basis.xsm"
    archive_path = training_root / "archives/training_snapshots.xsm"
    log_path = training_root / "training/rank_precision.log"
    for p in (basis_path, archive_path, log_path):
        fixed[str(p)] = sha256(p)
    log = log_path.read_text()
    check_provenance(log)
    admission = parse_rank_admission(log, 2)
    with _open_xsm(archive_path) as a:
        if struct.unpack("<i", a.record(a.root, "LISTDIM", 1, 1))[0] != 3:
            raise ValueError("exact A/B/A three training slots required")
        tracks = slots(a, a.root, "TRACK", 3)
        fluxes = slots(a, a.root, "FLUX", 3)
        phi = np.empty((370, 8, 3), dtype=np.float64)
        volume_bits = a.record(tracks[0], "VOLUME", 8, 2)
        volume = np.frombuffer(volume_bits, "<f4").astype(np.float64)
        if not np.isfinite(volume).all() or np.any(volume <= 0):
            raise ValueError("positive original volume metric required")
        for islot, letter in enumerate(("A", "B", "A")):
            if a.record(tracks[islot], "VOLUME", 8, 2) != volume_bits:
                raise ValueError("slot volume bits differ")
            key = np.frombuffer(a.record(tracks[islot], "KEYFLX", 8, 1), "<i4") - 1
            if len(set(key)) != 8 or np.any((key < 0) | (key >= 14)):
                raise ValueError("scalar region/unknown mapping differs")
            fields = items(a, fluxes[islot], "FLUX64", 370)
            old_path = Path(original["runtime_and_input_pins"][f"{letter}_archive"]["path"])
            with _open_xsm(old_path) as old:
                old_fields = items(old, old.object("FLUX"), "FLUX64", 370)
                for group, (field, old_field) in enumerate(zip(fields, old_fields)):
                    raw = a.record(field, "***HANDLE***", 28, 4) if "***HANDLE***" in field else None
                    # A list item is an array handle, rather than a directory.
                    if raw is None:
                        raise ValueError("invalid REAL64 array handle")
                    if raw != old.record(old_field, "***HANDLE***", 28, 4):
                        raise ValueError("packed FLUX64 differs from original A/B/A bytes")
                    values = np.frombuffer(raw, "<f8")
                    if not np.isfinite(values).all() or np.any(values[key] <= 0):
                        raise ValueError("invalid genuine scalar flux")
                    phi[group, :, islot] = values[key]
    weight = volume / volume.sum()
    groups = []
    with _open_xsm(basis_path) as basis:
        root = basis.root
        if struct.unpack("<i", basis.record(root, "POD-INPUT-TY", 1, 1))[0] != 4:
            raise ValueError("native basis has no genuine REAL64 training marker")
        if basis.record(root, "POD-IN-SRC", 3, 3).decode("ascii").strip() != "ROOT-FLUX64":
            raise ValueError("native basis trained from another authority")
        sigma = np.frombuffer(basis.record(root, "POD-SIGMA-G", 2220, 4), "<f8").reshape(370, 3)
        ranks = np.frombuffer(basis.record(root, "POD-RANK-G", 370, 1), "<i4")
        for group in range(370):
            shape = phi[group] / (weight @ phi[group])
            replay = np.linalg.svd(np.sqrt(weight[:, None]) * shape, compute_uv=False)
            bound = 64 * np.finfo(np.float64).eps * 8 * replay[0]
            if not np.isfinite(sigma[group]).all() or np.max(np.abs(sigma[group] - replay)) > bound:
                raise ValueError(f"group {group+1}: genuine REAL64 snapshot SVD replay differs")
            row = admission["groups"][group]
            if ranks[group] != row["production_rank"] or not np.allclose(
                    sigma[group], row["sigma"], rtol=2e-15, atol=2e-30):
                raise ValueError("independent GREP output differs from raw basis records")
            groups.append(dict(group=group+1, sigma=sigma[group].tolist(),
                sigma2_over_sigma1=float(sigma[group, 1]/sigma[group, 0]),
                original_gate_pass=row["pass"], independent_svd_max_abs_error=float(np.max(np.abs(sigma[group]-replay))),
                independent_svd_roundoff_bound=float(bound)))
    for p in (build_root / "Root_actual_experiment_tool_terminal_return.json",
              training_root / "run_status.json", training_root / "training/stages.json"):
        fixed[str(p)] = sha256(p)
    for name, digest in fixed.items():
        require_file(Path(name), digest)
    result = dict(schema="AXMAT_CLOSED_REAL64_COMMON_RANK2_INDEPENDENT_REPLAY_V1",
        classification=admission["classification"], actual_original_tool_exit_code=2,
        original_metadata_reader_failure=original["error"], numerical_stages_reexecuted=False,
        genuine_REAL64_consumption_verified=True, all_370_raw_basis_GREP_and_SVD_replays_agree=True,
        requested_rank=2, training_slots=["A", "B", "A"], original_volume_metric_preserved=True,
        sigma2_over_sigma1_strict_min=admission["sigma2_over_sigma1_strict_min"],
        failed_groups=[g["group"] for g in groups if not g["original_gate_pass"]],
        common_rank2_admitted=admission["classification"] == "VALID_RANK_INPUT_PRECISION",
        full_input_sha256=fixed, groups=groups, AAA_accuracy_qualified=False, ABA_started=False,
        coupled_or_physics_qualification=False, goal_complete=False)
    dump_json(output, result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--build-root", required=True, type=Path)
    p.add_argument("--training-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    r = audit(a.build_root, a.training_root, a.output)
    print(json.dumps({k: r[k] for k in ("classification", "genuine_REAL64_consumption_verified",
        "all_370_raw_basis_GREP_and_SVD_replays_agree", "failed_groups")}, sort_keys=True))


if __name__ == "__main__":
    main()
