#!/usr/bin/env python3
"""Prepare or serially execute an explicitly declared AAA/ABA SPOT experiment.

Preflight is read-only. Preparation copies a pinned small runtime and writes new
decks. Only the explicit run subcommand starts calculation. No rebuild, retry,
tolerance change, damping, rank adaptation, or continuation past first MET.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import time

from production_inputs import ProductionConfig, write_inputs

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_ROOT = ROOT / "validation/artifacts"
RESOURCE_POLL_SECONDS = 1.0
RUNTIME_DIR = ROOT / "validation/artifacts/d4a-scattering-mesh12-picard-runtime-20260925"
BOOTSTRAP_DIR = ROOT / "validation/artifacts/d4a-scattering-mesh12-bootstrap-run-20260925"
RUNTIME_MANIFEST_SHA = "af7069315a59ae6de9c0bd3edd6f497bf4dcaef1140917b4239c32bcff8da12b"
BOOTSTRAP_MANIFEST_SHA = "805c06e1ec873809a890be3a90afe1b8c16ec57272c3eaa5c315aa8feb64b32f"
DRAGON_SHA = "873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef"
CONTRACT_SHA = "db66e520cb421188eb96fe85b0c022f2ab3746afb0a27ea66dec5d0a6b3d94fc"
RANK_RATIO_MIN = 9.5367431640625e-7  # 8 * epsilon(REAL32), predeclared before basis construction.
RUNTIME_NAMES = ("Dragon", "prepare_r64_next_projected", "admit_candidate_radial",
                 "close_r64_returned", "check_one_map_xsm", "check_convergence_gate",
                 "run_bounded_dragon.py", "SpotStepR64.c2m")
BOOTSTRAP_NAMES = ("b2i_seal_bootstrap", "SpotRefR64.c2m", "SpotPlaneR64.c2m")
INPUT_NAMES = ("snapshot_A", "snapshot_B", "radial_track_A", "radial_track_B",
               "snapshot_log_A", "snapshot_log_B", "material_manifest", "material_results")
ABNORMAL = re.compile(r"CONVERGENCE NOT REACHED|XABORT|ABORT:|FATAL|"
                      r"SIG(?:SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error", re.I)


class Refusal(RuntimeError):
    pass


class ResourceFailure(Refusal):
    def __init__(self, snapshot: dict):
        self.snapshot = snapshot
        super().__init__("FAIL_RESOURCE: " + snapshot["reason"])


def validate_resource_roots(values: list[str], artifacts_root: Path) -> list[Path]:
    """Admit explicit, disjoint directories without traversing any symlink."""
    base = artifacts_root.resolve(strict=True)
    if not isinstance(values, list) or not values:
        raise Refusal("resource_roots must explicitly list this experiment's artifact directories")
    roots = []
    for value in values:
        if not isinstance(value, str):
            raise Refusal("resource roots must be absolute directory paths")
        path = Path(value)
        if (not path.is_absolute() or ".." in path.parts or path == base
                or not path.is_relative_to(base)):
            raise Refusal("resource roots must be strict project validation/artifacts descendants")
        cursor = path
        while cursor != base:
            if cursor.is_symlink() or (cursor.exists() and not cursor.is_dir()):
                raise Refusal("resource root or ancestor is a symlink/non-directory")
            cursor = cursor.parent
        if any(path == old or path.is_relative_to(old) or old.is_relative_to(path) for old in roots):
            raise Refusal("resource roots overlap or repeat; specify disjoint experiment directories")
        roots.append(path)
    return roots


class DiskResources:
    """Budget regular-file apparent bytes; links to old immutable data cost zero."""

    def __init__(self, artifacts_root: Path, roots: list[str], min_free_bytes: int, max_bytes: int):
        self.artifacts_root = artifacts_root
        self.roots = validate_resource_roots(roots, artifacts_root)
        self.min_free_bytes, self.max_bytes = min_free_bytes, max_bytes
        self.latest = None

    def check(self) -> dict:
        snapshot = {"checked_unix": time.time(), "min_free_bytes": self.min_free_bytes,
                    "artifact_budget_bytes": self.max_bytes, "resource_roots": [str(p) for p in self.roots]}
        try:
            # Recheck root/ancestor aliases on every poll, not only at preparation.
            validate_resource_roots(snapshot["resource_roots"], self.artifacts_root)
            total, count = 0, 0
            stack = list(self.roots)
            while stack:
                directory = stack.pop()
                try:
                    # O_NOFOLLOW also closes the stat-to-traversal race if a
                    # directory is replaced with an immutable-input alias.
                    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                    try:
                        with os.scandir(descriptor) as entries:
                            for entry in entries:
                                try:
                                    item = entry.stat(follow_symlinks=False)
                                except FileNotFoundError:
                                    continue  # Atomic producer rename/removal during observation.
                                if stat.S_ISDIR(item.st_mode):
                                    stack.append(directory / entry.name)
                                elif stat.S_ISREG(item.st_mode):
                                    total += item.st_size
                                    count += 1
                    finally:
                        os.close(descriptor)
                except FileNotFoundError:
                    continue  # A predeclared future output root can be absent.
            snapshot.update(artifact_bytes=total, regular_files=count,
                            disk_free_bytes=shutil.disk_usage(self.artifacts_root).free)
            self.latest = snapshot
            reasons = []
            if snapshot["disk_free_bytes"] < self.min_free_bytes:
                reasons.append("free disk space below declared minimum")
            if total > self.max_bytes:
                reasons.append("experiment regular-file total exceeds declared artifact budget")
            if reasons:
                snapshot["reason"] = "; ".join(reasons)
                raise ResourceFailure(snapshot)
            return snapshot
        except ResourceFailure:
            raise
        except (OSError, Refusal) as error:
            snapshot["reason"] = f"cannot verify declared resource scope: {error}"
            self.latest = snapshot
            raise ResourceFailure(snapshot) from error


def resource_monitor(info: dict) -> DiskResources:
    spec = json.loads(Path(info["case_spec"]["path"]).read_text())
    caps = spec["resource_caps"]
    return DiskResources(Path(info["artifact_root"]), info["resource_roots"],
                         int(caps["disk_min_free_GiB"] * 2**30),
                         int(caps["new_case_artifact_budget_GiB"] * 2**30))


@dataclass(frozen=True)
class Budget:
    setup_seconds: int
    bootstrap_axial_seconds: int
    bootstrap_radial_seconds: int
    radial_seconds: int
    axial_seconds: int
    host_seconds: int
    max_maps: int  # Independent cap for each case; AAA cannot consume ABA's cap.
    total_seconds: int  # Independent per-case wall cap, including its setup.

    def validate(self) -> None:
        for name, value in asdict(self).items():
            if type(value) is not int or value <= 0:
                raise Refusal(f"budget {name} must be an explicit positive integer")


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def require_file(path: Path, expected: str | None = None, executable: bool = False) -> Path:
    if path.is_symlink() or not path.is_file():
        raise Refusal(f"regular file required: {path}")
    if executable and not os.access(path, os.X_OK):
        raise Refusal(f"executable required: {path}")
    if expected is not None and sha256(path) != expected:
        raise Refusal(f"content hash mismatch: {path}")
    return path.resolve()


def read_manifest(path: Path, expected: str) -> dict[str, str]:
    require_file(path, expected)
    values = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"([a-f0-9]{64})  ([^\n]+)", line)
        if not match:
            raise Refusal(f"invalid manifest line in {path}")
        digest, name = match.groups()
        if Path(name).name != name or name in values:
            raise Refusal("runtime manifest contains a path or duplicate")
        values[name] = digest
    return values


def pinned_runtime_files(runtime_dir: Path = RUNTIME_DIR,
                         bootstrap_dir: Path = BOOTSTRAP_DIR) -> dict[str, dict[str, str]]:
    result = {}
    for directory, manifest, digest, names in (
        (runtime_dir, "runtime.sha256", RUNTIME_MANIFEST_SHA, RUNTIME_NAMES),
        (bootstrap_dir, "result.sha256", BOOTSTRAP_MANIFEST_SHA, BOOTSTRAP_NAMES),
    ):
        hashes = read_manifest(directory / manifest, digest)
        for name in names:
            if name not in hashes:
                raise Refusal(f"unsealed runtime member: {name}")
            path = require_file(directory / name, hashes[name], "." not in name)
            result[name] = {"path": str(path), "sha256": hashes[name]}
    # This metadata-only host predates the scattering change; its source and
    # byte identity are separate from the transport executable identity.
    path = require_file(ROOT / "validation/iterative/make_route_contract", CONTRACT_SHA, True)
    result["make_route_contract"] = {"path": str(path), "sha256": CONTRACT_SHA}
    return result


def check_dragon_log(text: str, marker: str) -> None:
    # CLE lists source text as well as ECHO results. Only the executed >| line
    # can satisfy a stage marker; its appearance in an input listing cannot.
    if marker and not re.search(r"^>\|" + re.escape(marker) + r"(?:\s|$)", text, re.M):
        raise Refusal(f"missing executed completion marker: {marker}")
    if "normal end of execution for dragon" not in text:
        raise Refusal("missing normal Dragon terminal")
    # ECHO/ABORT statements in the CLE source listing are not failures. Native
    # diagnostics and executable lines remain covered after removing listings.
    diagnostics = "\n".join(line for line in text.splitlines()
                            if not line.startswith("<|")
                            and not (len(line) >= 120 and re.search(r"\s\d{4,}$", line)))
    if ABNORMAL.search(diagnostics):
        raise Refusal("abnormal Dragon terminal or convergence diagnostic")


def check_protocol(spec: dict, config: ProductionConfig, budget: Budget) -> None:
    """Bind supported physical/numerical choices to the predeclared experiment."""
    geometry, basis, production = (spec[k] for k in ("geometry", "basis", "production"))
    if (spec.get("schema_version") != 1
            or spec["cases"] != {"AAA": list("AAA"), "ABA": list("ABA")}
            or basis["training_slots"] != list("ABA")
            or type(basis["requested_rank"]) is not int or basis["requested_rank"] not in (1, 2)
            or basis["fixed_once_for_both_cases"] is not True):
        raise Refusal("case specification does not declare a supported common A/B/A fixed rank")
    if (geometry["radial_regions"] != 8
            or geometry["radii_inner_to_outer_cm"] != [.11, .308712, .381084, .412536, .4225, .435, .485]
            or geometry["hex_edge_cm"] != .61776479
            or geometry["radial_boundary"] != "white isotropic albedo one, NOT specular reflection"
            or geometry["axial_boundary"] != "vacuum at both ends"):
        raise Refusal("unsupported physical pin dimensions or boundary conditions")
    if geometry["physical_z_edges_cm"] != [i * config.zone_height_cm for i in range(4)]:
        raise Refusal("production zone heights differ from the physical case specification")
    radial, axial = production["radial_controls"], production["axial_controls"]
    expected = dict(cells_per_zone=geometry["cells_per_zone"], sn=production["sn"],
                    rank=basis["requested_rank"], eps_radial=radial["eps"], eps_axial=axial["eps"],
                    eps_mccg=radial["eps_mccg"], maxout=radial["maxout"], maxinr=radial["maxinr"],
                    radial_acce_free=radial["acce"][0], radial_acce_accel=radial["acce"][1],
                    axial_acce_free=axial["acce"][0], axial_acce_accel=axial["acce"][1])
    if any(getattr(config, key) != value for key, value in expected.items()):
        raise Refusal("production controls differ from case_spec")
    if (production["groups"] != 370 or production["fission_components"] != 32
            or production["scat"] != 3 or production["axial_spatial"] != "constant diamond"
            or production["picard_alpha"] != 1 or production["outer_gate_each"] != 5e-7
            or axial["rebalance"] != "OFF" or axial["maxout"] != config.maxout
            or axial["maxinr"] != config.maxinr or DRAGON_SHA not in production["implementation"]):
        raise Refusal("case_spec does not match the frozen production implementation")
    caps = spec["resource_caps"]
    limits = dict(setup_seconds=caps["common_basis_wall_s"],
                  bootstrap_axial_seconds=caps["axial_wall_s"],
                  bootstrap_radial_seconds=caps["bootstrap_radial_wall_s"],
                  radial_seconds=caps["map_radial_wall_s"], axial_seconds=caps["axial_wall_s"],
                  host_seconds=caps["postchecks_wall_s"], max_maps=caps["max_maps_per_case"],
                  total_seconds=caps["total_wall_s_per_spot_case"])
    if asdict(budget) != limits:
        raise Refusal("stage, map, or per-case wall caps differ from case_spec")
    if (caps["new_numeric_children_at_once"] != 1 or caps["new_child_threads"] != 1
            or caps["automatic_retries_after_solver_failure"] != 0):
        raise Refusal("only serial single-thread execution without retries is supported")


def check_material_manifest(manifest: dict, spec: dict) -> None:
    geometry, source_geometry = spec["geometry"], manifest["geometry"]
    if (source_geometry["regions"] != geometry["radial_regions"]
            or source_geometry["hex_side_cm"] != geometry["hex_edge_cm"]
            or source_geometry["radii_cm"] != geometry["radii_inner_to_outer_cm"]
            or manifest["cases"] != spec["cases"] or manifest["training_slots"] != list("ABA")):
        raise Refusal("material geometry/case layout differs from case_spec")
    m, c = spec["materials"], manifest["config"]
    offline = spec["production"]["offline_snapshot_controls"]
    expected = {"pu_A": m["A"]["rnr_cc_p_Pu"], "u_A": m["A"]["rnr_cc_p_U"],
                "pu_B": m["B"]["rnr_cc_p_Pu"], "u_B": m["B"]["rnr_cc_p_U"],
                "fuel_C": m["temperature_C_in_every_zone"]["fuel_and_hole"],
                "clad_C": m["temperature_C_in_every_zone"]["clad_and_gap"],
                "sodium_C": m["temperature_C_in_every_zone"]["sodium"],
                "snapshot_eps": offline["eps"], "mccg_eps": offline["eps_mccg"],
                "maxout": offline["maxout"], "track_angles": 48, "track_density": 100.0}
    if any(c.get(key) != value for key, value in expected.items()):
        raise Refusal("material composition, temperature or snapshot controls differ from case_spec")
    item = manifest["source_files"]["geometry.dat"]
    text = require_file(Path(item["path"]), item["sha256"]).read_text()
    boundary = re.search(r"boundaries conditions: defaul nbbcda allsur\s*\n\s*([^\n]+)", text)
    albedo = re.search(r"\* albedo\s*\n\s*([^\n]+)", text)
    if (not boundary or [int(x) for x in re.findall(r"\d+", boundary[1])] != [0, 0, 0]
            or not albedo or float(albedo[1]) != 1.0):
        raise Refusal("actual radial geometry does not encode white unit-albedo boundaries")
    circles = re.findall(r"\* ELEM\s+\d+\s+circle\n[^\n]+\n\*\n([^\n]+)", text)
    radii = sorted(float(row.split(",")[2]) for row in circles)
    if radii != geometry["radii_inner_to_outer_cm"]:
        raise Refusal("actual radial circle radii differ from case_spec")
    segments = re.findall(r"\* ELEM\s+\d+\s+line segment\n[^\n]+\n\*\n([^\n]+)", text)
    coordinates = [[float(x) for x in row.split(",")] for row in segments]
    if (len(coordinates) != 6
            or abs(max(abs(v) for row in coordinates for v in row[::2]) - geometry["hex_edge_cm"]) > 1e-8
            or abs(max(abs(v) for row in coordinates for v in row[1::2])
                   - geometry["hex_edge_cm"] * math.sqrt(3) / 2) > 1e-8):
        raise Refusal("actual outer hexagonal dimensions differ from case_spec")


def check_rank_addendum(addendum: dict, spec_sha: str, requested_rank: int) -> None:
    threshold_field = ("sigma2_over_sigma1_strict_min" if requested_rank == 2
                       else "selected_sigma_over_sigma1_strict_min")
    if (type(requested_rank) is not int or requested_rank not in (1, 2)
            or addendum.get("case_spec_sha256") != spec_sha
            or addendum.get(threshold_field) != RANK_RATIO_MIN
            or addendum.get("required_production_rank_each_group") != requested_rank
            or addendum.get("groups") != 370
            or addendum.get("failure_classification") != "INCONCLUSIVE_RANK_INPUT_PRECISION"):
        raise Refusal("rank input-precision addendum differs from the implemented admission rule")


def preflight(declaration_path: Path, expected_sha: str) -> dict:
    declaration_path = require_file(declaration_path, expected_sha)
    data = json.loads(declaration_path.read_text())
    if data.get("schema_version") != 1 or not data.get("experiment_id"):
        raise Refusal("declaration needs schema_version=1 and experiment_id")
    if data.get("cases") != ["AAA", "ABA"]:
        raise Refusal("declared case order must be AAA then ABA")
    config = ProductionConfig(**data["production_config"])
    config.validate()
    budget = Budget(**data["budgets"])
    budget.validate()
    protocol = {}
    for key in ("case_spec", "rank_addendum"):
        item = data[key]
        path = Path(item["path"])
        if not path.is_absolute():
            raise Refusal(f"absolute protocol path required: {key}")
        protocol[key] = {"path": str(require_file(path, item["sha256"])), "sha256": item["sha256"]}
    spec = json.loads(Path(protocol["case_spec"]["path"]).read_text())
    addendum = json.loads(Path(protocol["rank_addendum"]["path"]).read_text())
    check_protocol(spec, config, budget)
    resource_roots = [str(p) for p in validate_resource_roots(data["resource_roots"], ARTIFACTS_ROOT)]
    resource_info = {"artifact_root": str(ARTIFACTS_ROOT.resolve()), "resource_roots": resource_roots,
                     "case_spec": protocol["case_spec"]}
    resource_snapshot = resource_monitor(resource_info).check()
    if data["experiment_id"] != spec["experiment_id"]:
        raise Refusal("experiment identity differs from case_spec")
    check_rank_addendum(addendum, protocol["case_spec"]["sha256"], config.rank)
    inputs = data["inputs"]
    if set(inputs) != set(INPUT_NAMES):
        raise Refusal(f"exact input keys required: {INPUT_NAMES}")
    resolved = {}
    for key in INPUT_NAMES:
        item = inputs[key]
        path = Path(item["path"])
        if not path.is_absolute():
            raise Refusal(f"absolute input path required: {key}")
        resolved[key] = {"path": str(require_file(path, item["sha256"])),
                         "sha256": item["sha256"]}
    if resolved["radial_track_A"]["sha256"] != resolved["radial_track_B"]["sha256"]:
        raise Refusal("A/B radial track bytes differ; shared TRACK_f not admitted")
    if resolved["snapshot_A"]["sha256"] == resolved["snapshot_B"]["sha256"]:
        raise Refusal("A/B snapshots are identical; material variation absent")
    check_material_manifest(json.loads(Path(resolved["material_manifest"]["path"]).read_text()), spec)
    receipts = json.loads(Path(resolved["material_results"]["path"]).read_text())
    if receipts.get("schema_version") != 1 or receipts.get("classification") != "VALID_SNAPSHOTS":
        raise Refusal("completed material snapshot receipt is required")
    if receipts.get("runtime_sha256") != DRAGON_SHA:
        raise Refusal("material snapshots must use the repaired production runtime")
    if receipts.get("inputs_manifest_sha256") != resolved["material_manifest"]["sha256"]:
        raise Refusal("material input manifest identity differs")
    dims = {"groups": 370, "regions": 8, "fission_components": 32, "snapshots": 1}
    for case in ("A", "B"):
        state = receipts["states"][case]
        if any(state.get(k) != v for k, v in dims.items()):
            raise Refusal(f"material {case} dimensions not admitted")
        for field, key in (("archive_sha256", f"snapshot_{case}"),
                           ("radial_track_sha256", f"radial_track_{case}"),
                           ("snapshot_log_sha256", f"snapshot_log_{case}")):
            if state.get(field) != resolved[key]["sha256"]:
                raise Refusal(f"material {case} receipt does not bind {field}")
        check_dragon_log(Path(resolved[f"snapshot_log_{case}"]["path"]).read_text(errors="replace"),
                         f"AXMAT-SNAPSHOT-{case}-COMPLETE")
    # Resource-only consumers (including the frozen CE three-file bundle) do
    # not need this reader. Production preflight must fail closed without it.
    try:
        from snapshot_control_preflight import SnapshotControlError, audit_snapshot_controls
    except ImportError as error:
        raise Refusal("snapshot control preflight reader unavailable") from error
    control_audits = {}
    for case in ("A", "B"):
        try:
            control_audits[case] = audit_snapshot_controls(
                Path(resolved[f"snapshot_{case}"]["path"]), eps_radial=config.eps_radial,
                eps_axial=config.eps_axial, eps_mccg=config.eps_mccg)
        except (SnapshotControlError, OSError) as error:
            raise Refusal(f"snapshot {case} control records not admitted: {error}") from error
    if any(audit["classification"] != "PASS_SNAPSHOT_CONTROL_COMPATIBILITY"
           for audit in control_audits.values()):
        raise Refusal("snapshot control preflight failed: " + json.dumps(control_audits, sort_keys=True))
    runtime = pinned_runtime_files()
    return {"schema_version": 1, "experiment_id": data["experiment_id"],
            "cases": ["AAA", "ABA"], "production_config": asdict(config),
            "budgets": asdict(budget), "inputs": resolved, "runtime_sources": runtime, **protocol,
            "artifact_root": resource_info["artifact_root"], "resource_roots": resource_roots,
            "preflight_resources": resource_snapshot,
            "snapshot_control_audits": control_audits,
            "declaration": {"path": str(declaration_path), "sha256": expected_sha}}


def pack_archives_deck() -> str:
    lines = ["* Archive packaging only: RECOVER/BACKUP, no solver modules.",
             "XSM_FILE STATE_A :: FILE './snapshot_A.xsm' ;",
             "XSM_FILE STATE_B :: FILE './snapshot_B.xsm' ;",
             "XSM_FILE TRAIN_OUT :: FILE './training_snapshots.xsm' ;",
             "XSM_FILE AAA_OUT :: FILE './aaa_snapshots.xsm' ;",
             "XSM_FILE ABA_OUT :: FILE './aba_snapshots.xsm' ;",
             "LINKED_LIST SNAP TRACK MICROLIB2 SYSTEM FLUX ;",
             "MODULE RECOVER: BACKUP: DELETE: GREP: ABORT: END: ;",
             "INTEGER nsnap ;"]
    for state in ("A", "B"):
        lines += [f"GREP: STATE_{state} :: GETVAL 'LISTDIM' 1 >>nsnap<< ;",
                  "IF nsnap 1 <> THEN", "  ABORT: ;", "ENDIF ;"]
    for output, slots in (("TRAIN_OUT", "ABA"), ("AAA_OUT", "AAA"), ("ABA_OUT", "ABA")):
        for i, slot in enumerate(slots, 1):
            lines.append(f"TRACK MICROLIB2 SYSTEM FLUX := RECOVER: STATE_{slot} :: ITEM 1 ;")
            if i == 1:
                lines.append("SNAP := BACKUP: TRACK :: LIST 3 ITEM 1 ;")
            else:
                lines.append(f"SNAP := BACKUP: SNAP TRACK :: ITEM {i} ;")
            for name in ("MICROLIB2", "SYSTEM", "FLUX"):
                lines.append(f"SNAP := BACKUP: SNAP {name} :: ITEM {i} ;")
            lines.append("TRACK MICROLIB2 SYSTEM FLUX := DELETE: TRACK MICROLIB2 SYSTEM FLUX ;")
        lines += [f"{output} := SNAP ;", "SNAP := DELETE: SNAP ;"]
    return "\n".join(lines + ['ECHO "AXMAT-ARCHIVE-PACK-COMPLETE" ;',
                              "END: ;", 'QUIT "LIST" .', ""])


def dump_json(path: Path, data: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
    temporary.replace(path)


def rank_precision_deck(requested_rank: int = 2) -> str:
    # GREP reads the actual REAL64 POD-SIGMA-G record independently of SPOPOD's
    # requested/retained rank. Each group stores three contiguous singular values.
    if type(requested_rank) is not int or requested_rank not in (1, 2):
        raise Refusal("rank admission supports only declared uniform rank 1 or 2")
    selected = "sone" if requested_rank == 1 else "stwo"
    return f'''* No numerical solve: independent admission of the frozen basis records.
XSM_FILE BASIS :: FILE './common_basis.xsm' ;
MODULE GREP: END: ;
INTEGER igr idx rank ngroup ;
DOUBLE sone stwo sthree limit ;
LOGICAL allgood good ;
EVALUATE igr := 0 ;
GREP: BASIS :: GETVAL 'STATE-VECTOR' 8 >>ngroup<< ;
EVALUATE allgood := ngroup 370 = ;
WHILE igr 370 < DO
  EVALUATE igr := igr 1 + ;
  EVALUATE idx := igr 1 - 3 * 1 + ;
  GREP: BASIS :: GETVAL 'POD-RANK-G' <<igr>> >>rank<< ;
  GREP: BASIS :: GETVAL 'POD-SIGMA-G' <<idx>> >>sone<< ;
  EVALUATE idx := idx 1 + ;
  GREP: BASIS :: GETVAL 'POD-SIGMA-G' <<idx>> >>stwo<< ;
  EVALUATE idx := idx 1 + ;
  GREP: BASIS :: GETVAL 'POD-SIGMA-G' <<idx>> >>sthree<< ;
  EVALUATE limit := sone 9.5367431640625D-7 * ;
  EVALUATE good := rank {requested_rank} = sone 0.0D0 > * {selected} limit > *
    sone stwo >= * stwo sthree >= * sthree 0.0D0 >= * ;
  ECHO "AXMAT-RANK-SPECTRUM" igr rank sone stwo sthree good ;
  EVALUATE allgood := allgood good * ;
ENDWHILE ;
IF allgood THEN
  ECHO "AXMAT-RANK-INPUT-PRECISION-PASS" ;
ELSE
  ECHO "AXMAT-RANK-INPUT-PRECISION-FAIL" ;
ENDIF ;
ECHO "AXMAT-RANK-RECORD-CHECK-COMPLETE" ;
END: ;
QUIT "LIST" .
'''


def parse_rank_admission(text: str, requested_rank: int = 2) -> dict:
    if type(requested_rank) is not int or requested_rank not in (1, 2):
        raise Refusal("rank admission supports only declared uniform rank 1 or 2")
    number = r"([+-]?[\d.]+[EeDd][+-]?\d+)"
    pattern = (r"^>\|AXMAT-RANK-SPECTRUM\s+(\d+)\s+(\d+)\s+"
               + r"\s+".join([number] * 3) + r"\s+\.(TRUE|FALSE)\.")
    rows = re.findall(pattern, text, re.M)
    if len(rows) != 370 or [int(r[0]) for r in rows] != list(range(1, 371)):
        raise Refusal("rank record log must contain exactly 370 ordered group spectra")
    groups, all_good = [], True
    for group, rank, *fields in rows:
        sigma = [float(v.replace("D", "E").replace("d", "e")) for v in fields[:3]]
        good = (int(rank) == requested_rank and all(math.isfinite(v) for v in sigma)
                and sigma[0] >= sigma[1] >= sigma[2] >= 0 and sigma[0] > 0
                and sigma[requested_rank - 1] > RANK_RATIO_MIN * sigma[0])
        if good != (fields[3] == "TRUE"):
            raise Refusal("independent Python/CLE rank decisions differ; preserve evidence for review")
        all_good = all_good and good
        groups.append({"group": int(group), "production_rank": int(rank), "sigma": sigma,
                       "input_resolution_floor": RANK_RATIO_MIN * sigma[0], "pass": good})
    expected = "PASS" if all_good else "FAIL"
    labels = re.findall(r"^>\|AXMAT-RANK-INPUT-PRECISION-(PASS|FAIL)(?:\s|$)", text, re.M)
    if labels != [expected]:
        raise Refusal("rank input-precision classification is missing or inconsistent")
    threshold_field = ("sigma2_over_sigma1_strict_min" if requested_rank == 2
                       else "selected_sigma_over_sigma1_strict_min")
    return {"classification": "VALID_RANK_INPUT_PRECISION" if all_good else "INCONCLUSIVE_RANK_INPUT_PRECISION",
            "requested_rank": requested_rank, threshold_field: RANK_RATIO_MIN, "groups": groups}


def prepare(declaration: Path, expected_sha: str, output: Path) -> dict:
    info = preflight(declaration, expected_sha)
    output = output.resolve()
    if not any(output == Path(root) or output.is_relative_to(Path(root)) for root in info["resource_roots"]):
        raise Refusal("prepared output must be covered by a declared resource root")
    output.mkdir(parents=True, exist_ok=False)
    runtime = output / "runtime"
    runtime.mkdir()
    for name, item in info["runtime_sources"].items():
        shutil.copy2(item["path"], runtime / name)
        require_file(runtime / name, item["sha256"])
    shutil.copy2(__file__, runtime / "production_runner.py")
    shutil.copy2(Path(__file__).with_name("production_inputs.py"), runtime / "production_inputs.py")
    shutil.copy2(Path(__file__).with_name("snapshot_control_preflight.py"), runtime / "snapshot_control_preflight.py")
    config = ProductionConfig(**info["production_config"])
    write_inputs(output / "decks", config)
    # Save even a deficient production basis before independent record admission,
    # so rank failure retains its exact singular spectra for diagnosis. Case
    # setup keeps the original groupwise rank gate and cannot run before admission.
    common_path = output / "decks/common_basis.x2m"
    common_text = common_path.read_text()
    start = common_text.index("GREP: SYSTEM :: GETVAL 'STATE-VECTOR'")
    end = common_text.index("BASIS_ARCH := SYSTEM ;", start)
    common_path.write_text(common_text[:start] + common_text[end:])
    deck_manifest = output / "decks/production_inputs.json"
    manifest = json.loads(deck_manifest.read_text())
    # The runner inventory below seals the modified deck; record why it differs
    # from the generator-only staging manifest without silently leaving stale hashes.
    manifest["runner_common_basis_admission"] = "saved first, then independent rank_precision.x2m"
    manifest["rank_gate"] = (f"Every group must retain rank {config.rank} and sigma{config.rank} > "
                             "8*epsilon(REAL32)*sigma1 before case execution; retain all three singular values")
    manifest["deck_sha256"]["common_basis.x2m"] = sha256(common_path)
    dump_json(deck_manifest, manifest)
    (output / "decks/pack_archives.x2m").write_text(pack_archives_deck())
    (output / "decks/rank_precision.x2m").write_text(rank_precision_deck(config.rank))
    shutil.copy2(declaration, output / "declaration.json")
    info["classification"] = "PREPARED_NO_TRANSPORT"
    info["local_files"] = {str(p.relative_to(output)): sha256(p)
                           for folder in (runtime, output / "decks")
                           for p in sorted(folder.iterdir()) if p.is_file()}
    info["local_files"]["declaration.json"] = sha256(output / "declaration.json")
    dump_json(output / "prepared.json", info)
    try:
        resource_monitor(info).check()
    except ResourceFailure as error:
        dump_json(output / "prepare_failure.json", {"classification": "FAIL_RESOURCE", "resources": error.snapshot})
        raise
    return {"prepared": str((output / "prepared.json").resolve()),
            "sha256": sha256(output / "prepared.json"),
            "classification": "PREPARED_NO_TRANSPORT"}


def verify_prepared(prepared: Path, expected_sha: str) -> dict:
    prepared = require_file(prepared, expected_sha)
    data = json.loads(prepared.read_text())
    if data.get("classification") != "PREPARED_NO_TRANSPORT":
        raise Refusal("prepared input classification differs")
    for name, digest in data["local_files"].items():
        target = Path(name)
        if target.is_absolute() or ".." in target.parts:
            raise Refusal("invalid local inventory path")
        require_file(prepared.parent / target, digest)
    for item in data["inputs"].values():
        require_file(Path(item["path"]), item["sha256"])
    for key in ("case_spec", "rank_addendum"):
        item = data[key]
        require_file(Path(item["path"]), item["sha256"])
    check_protocol(json.loads(Path(data["case_spec"]["path"]).read_text()),
                   ProductionConfig(**data["production_config"]), Budget(**data["budgets"]))
    check_rank_addendum(json.loads(Path(data["rank_addendum"]["path"]).read_text()),
                        data["case_spec"]["sha256"], data["production_config"]["rank"])
    validate_resource_roots(data["resource_roots"], Path(data["artifact_root"]))
    if not any(prepared.parent == Path(root) or prepared.parent.is_relative_to(Path(root))
               for root in data["resource_roots"]):
        raise Refusal("prepared runtime is outside its declared resource roots")
    return data


def parse_gate(text: str) -> dict:
    result = {}
    for name in ("THRESHOLD", "RRHO", "RLEAK", "RA"):
        matches = re.findall(r"^SPOT-GATE " + name + r"\s+([\d+EeDd.\-]+)(?:\s|$)", text, re.M)
        if len(matches) != 1:
            raise Refusal(f"missing or duplicate gate field: {name}")
        result[name] = float(matches[0].replace("D", "E").replace("d", "e"))
        if not math.isfinite(result[name]) or result[name] < 0:
            raise Refusal("invalid gate number")
    if result["THRESHOLD"] != 5e-7:
        raise Refusal("outer gate differs from declared 5e-7")
    expected = "VALID_MET" if all(result[k] <= 5e-7 for k in ("RRHO", "RLEAK", "RA")) else "VALID_NOT_MET"
    labels = re.findall(r"^CLASSIFICATION=(\S+)$", text, re.M)
    if labels != [expected] or "SPOT-GATE COMPLETE" not in text.splitlines():
        raise Refusal("gate classification or terminal differs")
    return {"classification": expected, "defects": result}


class SerialExecutor:
    """One active solver/host at a time, with original bounded group cleanup."""

    def __init__(self, work: Path, total_seconds: int, case: str, resources: DiskResources):
        self.work = work
        self.stages_path = work / case / "stages.json"
        self.deadline = time.monotonic() + total_seconds
        self.records = []
        self.resources = resources
        spec = importlib.util.spec_from_file_location("axmat_bounded", work / "runtime/run_bounded_dragon.py")
        self.bounded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.bounded)
        self.env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                        MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")

    def execute(self, directory: Path, label: str, command: list[str], cap: int,
                marker: str | None = None, deck: str | None = None) -> str:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise Refusal("total wall-time budget exhausted; no next stage started")
        limit = min(float(cap), remaining)
        started = time.monotonic()
        record = {"label": str(directory.relative_to(self.work) / label), "command": command,
                  "wall_cap_seconds": limit, "status": "RUNNING", "started_unix": time.time()}
        self.records.append(record)
        dump_json(self.stages_path, {"stages": self.records})
        log = directory / f"{label}.log"
        try:
            record["resource_before"] = self.resources.check()
            process_limit = min(limit - (time.monotonic() - started), self.deadline - time.monotonic())
            if process_limit <= 0:
                raise Refusal("stage or total wall budget exhausted before child launch")
            if deck:
                with (directory / deck).open("rb") as stdin, log.open("xb") as out:
                    self._process(command, directory, stdin, out, process_limit)
            else:
                with log.open("xb") as out:
                    self._process(command, directory, subprocess.DEVNULL, out, process_limit)
            record["resource_after"] = self.resources.check()
            text = log.read_text(errors="replace")
            if deck:
                check_dragon_log(text, marker or "")
            elif marker and marker not in text.splitlines():
                raise Refusal(f"host marker missing: {marker}")
            record["status"] = "PASS"
            record["log_sha256"] = sha256(log)
            return text
        except BaseException as error:
            record["status"] = "FAIL_RESOURCE" if isinstance(error, ResourceFailure) else "FAILED"
            if isinstance(error, ResourceFailure):
                record["resources"] = error.snapshot
            record["error"] = str(error)
            raise
        finally:
            record["elapsed_seconds"] = time.monotonic() - started
            dump_json(self.stages_path, {"stages": self.records})

    def _process(self, command, directory, stdin, out, limit):
        process = subprocess.Popen(command, cwd=directory, stdin=stdin, stdout=out,
                                   stderr=subprocess.STDOUT, env=self.env, start_new_session=True)
        read_fd, write_fd = os.pipe()
        try:
            watchdog = self.bounded.start_liveness_watchdog(read_fd, process.pid,
                                                           self.bounded.TERM_GRACE_SECONDS)
        except BaseException:
            os.close(read_fd)
            os.close(write_fd)
            self.bounded.terminate_group(process)
            raise
        os.close(read_fd)
        try:
            try:
                deadline = time.monotonic() + limit
                while True:
                    self.resources.check()
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise subprocess.TimeoutExpired(command, limit)
                    try:
                        code = process.wait(timeout=min(RESOURCE_POLL_SECONDS, remaining))
                        self.resources.check()
                        break
                    except subprocess.TimeoutExpired:
                        continue
            except BaseException:
                self.bounded.terminate_group(process)
                raise
        finally:
            self.bounded.finish_liveness_watchdog(write_fd, watchdog)
        if code:
            raise Refusal(f"stage failed with exit status {code}; no retry")


def _link(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise Refusal(f"missing stage input: {source}")
    destination.symlink_to(source.resolve())


def verify_sealed_directory(directory: Path) -> None:
    seal = json.loads(require_file(directory / "result.json").read_text())
    if seal.get("classification") != "SEALED_STAGE_OUTPUTS":
        raise Refusal("stage output seal classification differs")
    for name, digest in seal["sha256"].items():
        if Path(name).name != name or sha256(directory / name) != digest:
            raise Refusal(f"sealed stage input/output changed: {directory / name}")


REFERENCE_CHECKS = ("input_equivalence", "source_convergence", "block_stability",
                    "statistical_resolution", "keff", "scalar_flux", "nu_fission",
                    "currents_balance_symmetry")


def qualify_aba(info: dict, work: Path, prepared_sha: str,
                qualification: Path | None, qualification_sha: str | None) -> dict:
    """Require independent accuracy qualification, not just SPOT fixed-point MET."""
    if qualification is None or qualification_sha is None:
        raise Refusal("ABA requires an explicit independent AAA reference qualification file and SHA256")
    qualification = require_file(qualification, qualification_sha)
    receipt = json.loads(qualification.read_text())
    if (receipt.get("schema_version") != 1 or receipt.get("case") != "AAA"
            or receipt.get("classification") != "AAA_REFERENCE_QUALIFIED"
            or receipt.get("method") != "independent_continuous_energy_openmc"
            or receipt.get("experiment_id") != info["experiment_id"]):
        raise Refusal("independent AAA reference qualification is not valid")
    status_path = work / "AAA/run_status.json"
    status = json.loads(require_file(status_path, receipt.get("aaa_run_status_sha256", "")).read_text())
    expected = {"prepared_sha256": prepared_sha,
                "case_spec_sha256": info["case_spec"]["sha256"],
                "rank_addendum_sha256": info["rank_addendum"]["sha256"],
                "common_basis_sha256": sha256(work / "training/common_basis.xsm")}
    if any(receipt.get(key) != value for key, value in expected.items()):
        raise Refusal("AAA reference qualification does not bind this frozen experiment")
    if (status.get("classification") != "WAITING_REFERENCE"
            or status.get("case") != "AAA" or status.get("prepared_sha256") != prepared_sha
            or status.get("common_basis_sha256") != expected["common_basis_sha256"]
            or status.get("cases", {}).get("AAA", {}).get("classification") != "VALID_MET"):
        raise Refusal("AAA has not reached the independently checked fixed point")
    for key in REFERENCE_CHECKS:
        if receipt.get("checks", {}).get(key) != "PASS":
            raise Refusal(f"AAA reference qualification did not pass {key}")
    evidence = receipt.get("evidence", {})
    if set(evidence) != {"statistics", "input_equivalence", "currents_balance_symmetry"}:
        raise Refusal("three independent reference evidence files are required")
    for label, item in evidence.items():
        evidence_path = Path(item["path"])
        if not evidence_path.is_absolute():
            raise Refusal("reference evidence paths must be absolute")
        report = json.loads(require_file(evidence_path, item["sha256"]).read_text())
        passed = (report.get("classification") == "STATISTICAL_COMPARISON_PASS"
                  if label == "statistics" and "classification" in report
                  else report.get("status") == "PASS")
        if not passed:
            raise Refusal(f"AAA reference evidence is not PASS: {label}")
    for directory in (work / "archives", work / "training", work / "AAA/bootstrap"):
        verify_sealed_directory(directory)
    final = Path(status["cases"]["AAA"]["final_directory"])
    if final.parent != work / "AAA":
        raise Refusal("AAA final state is outside its case directory")
    verify_sealed_directory(final)
    return {"path": str(qualification), "sha256": qualification_sha}


def run(prepared: Path, expected_sha: str, case: str = "AAA",
        reference_qualification: Path | None = None, reference_sha: str | None = None) -> dict:
    prepared = prepared.resolve()
    info = verify_prepared(prepared, expected_sha)
    work = prepared.parent
    if case not in ("AAA", "ABA"):
        raise Refusal("run accepts exactly one case: AAA or ABA")
    qualification = None
    if case == "ABA":
        qualification = qualify_aba(info, work, expected_sha, reference_qualification, reference_sha)
    elif reference_qualification is not None or reference_sha is not None:
        raise Refusal("reference qualification applies only to explicit ABA execution")
    budget = Budget(**info["budgets"])
    config = ProductionConfig(**info["production_config"])
    resources = resource_monitor(info)
    directory = work / case
    # The case directory is an exclusive permanent attempt claim. ABA can be
    # admitted later, while failure or interruption of either case is not retried.
    directory.mkdir()
    dump_json(directory / "run_claim.json", {"pid": os.getpid(), "case": case,
              "prepared_sha256": expected_sha, "started_unix": time.time()})
    executor = SerialExecutor(work, budget.total_seconds, case, resources)
    runtime, decks = work / "runtime", work / "decks"
    result = {"classification": "RUNNING", "prepared_sha256": expected_sha,
              "case": case, "cases": {}, "alpha": 1, "outer_gate": 5e-7,
              "max_maps_per_case": budget.max_maps, "wall_cap_seconds_per_case": budget.total_seconds,
              "completed_maps": 0, "reference_qualification": qualification,
              "resource_roots": info["resource_roots"],
              "case_spec_sha256": info["case_spec"]["sha256"],
              "rank_addendum_sha256": info["rank_addendum"]["sha256"]}
    old_handlers = {s: signal.signal(s, signal.default_int_handler)
                    for s in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT)}

    def verify_fixed_inputs():
        verify_prepared(prepared, expected_sha)
        if qualification:
            reference = json.loads(require_file(Path(qualification["path"]), qualification["sha256"]).read_text())
            for item in reference["evidence"].values():
                require_file(Path(item["path"]), item["sha256"])

    def deck(directory, name, cap, marker):
        shutil.copy2(decks / name, directory / name)
        return executor.execute(directory, Path(name).stem, [str(runtime / "Dragon")],
                                cap, marker, name)

    def host(directory, name, args, marker=None):
        return executor.execute(directory, name, [str(runtime / name), *args],
                                budget.host_seconds, marker)

    def base_inputs(directory, setup, parent=None):
        for name in ("initial_axial_track.xsm", "initial_axial_macrolib.xsm",
                     "basis_reference.xsm", "initial_radial_track.bin", "route_contract.xsm"):
            _link(setup / name, directory / name)
        shutil.copy2(runtime / "SpotStepR64.c2m", directory / "SpotStepR64.c2m")
        if parent:
            _link(parent / "closed_axial.xsm", directory / "parent_axial_closed.xsm")
            _link(parent / "closed_snapshots.xsm", directory / "parent_snapshots_closed.xsm")

    def seal_directory(directory):
        files = {p.name: sha256(p) for p in sorted(directory.iterdir()) if p.is_file()}
        dump_json(directory / "result.json", {"classification": "SEALED_STAGE_OUTPUTS", "sha256": files})

    status_path = directory / "run_status.json"
    dump_json(status_path, result)
    try:
        result["initial_resources"] = resources.check()
        archives, training = work / "archives", work / "training"
        common = training / "common_basis.xsm"
        if case == "AAA":
            archives.mkdir()
            for key in ("snapshot_A", "snapshot_B"):
                _link(Path(info["inputs"][key]["path"]), archives / f"{key}.xsm")
            deck(archives, "pack_archives.x2m", budget.setup_seconds, "AXMAT-ARCHIVE-PACK-COMPLETE")
            seal_directory(archives)
            training.mkdir()
            _link(archives / "training_snapshots.xsm", training / "training_snapshots.xsm")
            deck(training, "common_basis.x2m", budget.setup_seconds, "AXMAT-COMMON-BASIS-COMPLETE")
            rank_log = deck(training, "rank_precision.x2m", budget.host_seconds,
                            "AXMAT-RANK-RECORD-CHECK-COMPLETE")
            result["common_basis_sha256"] = sha256(common)
            rank_admission = parse_rank_admission(rank_log, config.rank)
            dump_json(training / "rank_admission.json", rank_admission)
            seal_directory(training)
            if rank_admission["classification"] == "INCONCLUSIVE_RANK_INPUT_PRECISION":
                result["classification"] = "INCONCLUSIVE_RANK_INPUT_PRECISION"
                return result
        else:
            verify_sealed_directory(archives)
            verify_sealed_directory(training)
        common_sha = sha256(common)
        result["common_basis_sha256"] = common_sha
        verify_fixed_inputs()
        setup = directory / "bootstrap"
        setup.mkdir()
        _link(archives / f"{case.lower()}_snapshots.xsm", setup / "case_snapshots.xsm")
        _link(Path(info["inputs"]["radial_track_A"]["path"]), setup / "initial_radial_track.bin")
        shutil.copy2(common, setup / "basis_reference.xsm")
        require_file(setup / "basis_reference.xsm", common_sha)
        for name in ("SpotRefR64.c2m", "SpotPlaneR64.c2m"):
            shutil.copy2(runtime / name, setup / name)
        deck(setup, "case_setup.x2m", budget.setup_seconds, "AXMAT-CASE-SETUP-COMPLETE")
        host(setup, "make_route_contract", config.contract_arguments(case))
        deck(setup, "bootstrap_axial.x2m", budget.bootstrap_axial_seconds,
             "AXMAT-BOOTSTRAP-AXIAL-COMPLETE")
        deck(setup, "bootstrap_radial.x2m", budget.bootstrap_radial_seconds,
             "AXMAT-BOOTSTRAP-RADIAL-COMPLETE")
        host(setup, "b2i_seal_bootstrap", ["seed_axial.xsm", "initial_axial_track.xsm",
             "refreshed_snapshots.xsm", "route_contract.xsm", "closed_axial.xsm",
             "closed_snapshots.xsm"], "SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0")
        require_file(setup / "basis_reference.xsm", common_sha)
        seal_directory(setup)
        parent = setup
        case_status = {"classification": "VALID_NOT_MET", "completed_maps": 0, "maps": []}
        result["cases"][case] = case_status
        for epoch in range(1, budget.max_maps + 1):
            verify_fixed_inputs()
            verify_sealed_directory(parent)
            require_file(setup / "basis_reference.xsm", common_sha)
            current = directory / f"map{epoch:03d}"
            current.mkdir()
            base_inputs(current, setup, parent)
            host(current, "prepare_r64_next_projected", ["parent_axial_closed.xsm",
                 "parent_snapshots_closed.xsm", "initial_axial_track.xsm", "route_contract.xsm",
                 "projected_proposal.xsm"],
                 "SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT")
            deck(current, "picard_radial.x2m", budget.radial_seconds, "AXMAT-PICARD-RADIAL-COMPLETE")
            host(current, "admit_candidate_radial", ["candidate_radial.xsm", "route_contract.xsm"])
            deck(current, "picard_axial.x2m", budget.axial_seconds, "AXMAT-PICARD-AXIAL-COMPLETE")
            host(current, "close_r64_returned", ["candidate_axial.xsm", "candidate_snapshots.xsm",
                 "route_contract.xsm", "closed_axial.xsm", "closed_snapshots.xsm"],
                 f"SPOT-R64 CLOSED/{epoch} COMPLETE NO-TRANSPORT")
            deck(current, "checker_parent.x2m", budget.host_seconds, "")
            host(current, "check_one_map_xsm", ["--reencoded" if epoch == 1 else "--continued",
                 "basis_reference.xsm", "candidate_system.xsm", "parent_for_checker.xsm",
                 "candidate_axial.xsm", "candidate_snapshots.xsm"], "ONE-MAP-XSM COMPLETE")
            gate = parse_gate(host(current, "check_convergence_gate", ["closed_axial.xsm"],
                                  "SPOT-GATE COMPLETE"))
            verify_fixed_inputs()
            verify_sealed_directory(parent)
            require_file(setup / "basis_reference.xsm", common_sha)
            seal_directory(current)
            case_status.update(classification=gate["classification"], completed_maps=epoch,
                               final_directory=str(current))
            case_status["maps"].append({"epoch": epoch, **gate})
            result["completed_maps"] += 1
            dump_json(status_path, result)
            if gate["classification"] == "VALID_MET":
                break
            parent = current
        if case_status["classification"] != "VALID_MET":
            case_status["classification"] = "MAP_CAP_NOT_MET"
            result["classification"] = "MAP_CAP_NOT_MET"
        else:
            result["classification"] = "WAITING_REFERENCE"
        verify_fixed_inputs()
        result["final_resources"] = resources.check()
    except BaseException as error:
        result["classification"] = "FAIL_RESOURCE" if isinstance(error, ResourceFailure) else "FAILED_NO_RETRY"
        if isinstance(error, ResourceFailure):
            result["resources"] = error.snapshot
        result["error"] = str(error)
        raise
    finally:
        result["finished_unix"] = time.time()
        dump_json(status_path, result)
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for action in ("preflight", "prepare"):
        sub = commands.add_parser(action)
        sub.add_argument("declaration", type=Path)
        sub.add_argument("--sha256", required=True)
        if action == "prepare":
            sub.add_argument("output", type=Path)
    sub = commands.add_parser("run")
    sub.add_argument("prepared", type=Path)
    sub.add_argument("--sha256", required=True)
    sub.add_argument("--case", choices=("AAA", "ABA"), default="AAA")
    sub.add_argument("--reference-qualification", type=Path)
    sub.add_argument("--reference-sha256")
    args = parser.parse_args()
    if args.action == "preflight":
        data = preflight(args.declaration, args.sha256)
        result = {"classification": "PREFLIGHT_PASS_NO_OUTPUT_NO_TRANSPORT",
                  "experiment_id": data["experiment_id"]}
    elif args.action == "prepare":
        result = prepare(args.declaration, args.sha256, args.output)
    else:
        result = run(args.prepared, args.sha256, args.case,
                     args.reference_qualification, args.reference_sha256)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
