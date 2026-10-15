"""Prepare one future independent native ABA reference after real ABA MET.

No anticipated qualification, terminal, prepared or ABA-status hashes exist in
this entrance.  declare, prepare, run and analyze are separate exclusive
claims.  The staged ABA XML and ordinary 100/2000 x 10000 x 10 sampling are
unchanged.  The original native 64800-second cap is retained; direct native
PID RSS supervision at 2048 MiB and a frozen loader are explicit new controls.
The old AAA sample is only an immutable storage forecast witness.  It cannot
be a new ABA sample.  Nothing runs merely by importing this source.
"""

import argparse
import ast
import copy
import csv
import difflib
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
PROD = ART / "axial-material-production-qualified-AB-rank1-factor-cache-20261007"
AAA_REFERENCE = ART / "axial-material-qualified-AAA-rank1-factor-cache-reference-20261007"
AAA_TERMINAL = ART / "axial-material-qualified-AAA-rank1-factor-cache-reference-terminal-20261007"
ABA_ENTRY = ART / "axial-material-qualified-ABA-rank1-factor-cache-execution-admission-20261007"
SOURCE = ART / "axial-material-qualified-ABA-rank1-factor-cache-ce-reference-admission-20261007"
OUT = ART / "axial-material-ce-qualified-ABA-rank1-factor-cache-reference-20261007"
TERMINAL = ART / "axial-material-qualified-ABA-rank1-factor-cache-ce-reference-terminal-20261007"
CE = ART / "axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004"
STAGED = ART / "axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004/aba_reference_inputs"
ORIGINAL_ABA = ART / "axial-material-ce-v2-20261003/ABA"
OLD_PROD = ART / "axial-material-production-qualified-AB-white-trace-20261004"
BUILD = ART / "axial-material-rank1-factor-cache-build-20261007"
BUILD_TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
CE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AAA_rank1_cache_reference_analysis.py"
ABA_FACTORY = ROOT / "validation/axial_material/prepare_qualified_ABA_rank1_cache_execution.py"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_production.py"
TEMPLATE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_ABA_moment_order_ce_reference.py"
FULL_FACTORY = ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py"
PHYSICAL = ROOT / "validation/axial_material/review_qualified_AAA_refined_input_identity.py"
PROJECT = ART / "axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005/runtime/project_refined_observables.py"
EXPORTER = ART / "axial-material-tools-20261003/export_observables"
EXPORT_SOURCE = ROOT / "validation/axial_material/export_observables.f90"
FORMAL = AAA_REFERENCE / "AAA/reference_qualification.json"
PYTHON = Path("/Users/wen/miniforge3/envs/openmc-dev/bin/python")
OPENMC = Path("/Users/wen/miniforge3/envs/openmc-dev/bin/openmc")
CONTROLLER_SHA = "844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d"
BUILD_SEAL = "e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f"
BUILD_FACTORY_SHA = "92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a"
CE_FACTORY_SHA = "a937a7d246abf43709f135ba36cdda0e7c81cf5340847160b8e433bb72e65b7c"
ABA_FACTORY_SHA = "384133fc0bcbd1488a0b5b6b22842939f57743074de00a08b79b60e7de5eff00"
TEMPLATE_FACTORY_SHA = "3bfbaff4b4618102e34e172ddadb8f4eab33d25188b42d791b770a76fdfb8ca8"
FULL_SHA = "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6"
EXPORTER_SHA = "81da2ac2ea98009181cc54a1ab254c99d1cb362b4e89c468fe7bc44ea14e7524"
EXPORT_SOURCE_SHA = "fdfb6204a9661a38ba120387311136e0eba2959d54bd0bac6b594723b586ee35"
OPENMC_SHA = "10a5d41fd8a1bf8dfed4c2779e3d782803e92c6a919f2a6acf4302878b2001af"
OPENMC_LIBRARY_SHA = "4020c9462b1fa07aade09900e04809fa02a5c6fb31b599432d61cd0ce8a903e5"
XS_SHA = "b8ffb6104a946bf951dc0f3b9a1f57a60f7f57c4b308cd66df4fd3dd4bc557ce"
HISTORY_CAP, FREE_FLOOR = 96 * 2**30, 8 * 2**30
NATIVE_WALL, NATIVE_RSS = 64800, 2048
PREPARE_WALL, ANALYSIS_WALL, HOST_RSS = 120, 120, 512
HOST_MARGIN = 2**30
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
GATES = ("input_equivalence", "source_convergence", "block_stability", "statistical_resolution",
         "keff", "scalar_flux", "nu_fission", "currents_balance_symmetry")
SAMPLING = dict(particles_per_generation=10000, generations_per_batch=10,
    inactive_batches=100, active_batches=2000, total_histories=210000000, seed=310033)
INPUTS = ("materials.xml", "geometry.xml", "tallies.xml", "settings.xml", "reference_contract.json")
TRACK_RECORDS = ("STATE-VECTOR", "MAT1D", "MATCOD", "KEYFLX", "AREA2D", "VOL1D", "VOLUME",
                 "NCODE", "ICODE", "ZCODE", "U", "W", "PL", "KEYFLX$ANIS")
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
ANALYSIS_TAIL_FIELDS = ("actual_full_closeout_tail_gate", "actual_elapsed_through_full_closeout_seconds",
    "actual_complete_archive_bytes", "resources_after_full_closeout")
ARCHIVE_ROOTS = (str(SOURCE), str(OUT))


def combined_archive_bytes():
    builder = load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "rank1_factor_cache_ABA_actual_build")
    roots = builder.validate_history_roots(list(ARCHIVE_ROOTS), ART)
    total, stack = 0, list(roots)
    while stack:
        directory = stack.pop()
        try:
            fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                with os.scandir(fd) as entries:
                    for entry in entries:
                        value = entry.stat(follow_symlinks=False)
                        if stat.S_ISDIR(value.st_mode):
                            stack.append(directory / entry.name)
                        elif stat.S_ISREG(value.st_mode):
                            total += value.st_size
            finally:
                os.close(fd)
        except FileNotFoundError:
            continue
    builder.validate_history_roots(list(ARCHIVE_ROOTS), ART)
    return total


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, wanted=None):
    path = Path(path)
    if (not path.is_absolute() or path.is_symlink() or not path.is_file()
            or (wanted is not None and digest(path) != wanted)):
        raise ValueError("missing, aliased or changed reference dependency: " + str(path))
    return path


def pin(path):
    path = require(path)
    return dict(path=str(path), sha256=digest(path))


def read(path):
    return json.loads(Path(path).read_text())


def strict_json(path):
    def invalid_constant(value):
        raise ValueError("nonfinite external terminal JSON")
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate external terminal JSON key")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), parse_constant=invalid_constant, object_pairs_hook=unique)


def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def absent(path):
    if Path(path).exists() or Path(path).is_symlink():
        raise ValueError("exclusive new reference path already exists; no retry: " + str(path))


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def regular_files(folder):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("actual reference directory is missing or aliased")
    return {str(path.relative_to(folder)): digest(path) for path in sorted(folder.rglob("*"))
            if path.is_file() and not path.is_symlink()}


def regular_bytes(folder):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("actual regular-byte witness directory is missing or aliased")
    return sum(path.stat().st_size for path in folder.rglob("*") if path.is_file() and not path.is_symlink())


def load(path, name):
    path = require(path)
    if name in sys.modules:
        obj = sys.modules[name]
        if Path(obj.__file__).resolve() != path.resolve():
            raise ValueError("actual imported module is bound to another source: " + name)
        return obj
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    if Path(obj.__file__).resolve() != path.resolve():
        raise ValueError("actual module source identity differs")
    return obj


def binding(prepared_sha, ce_factory_sha, aba_factory_sha):
    """Establish true canonical producer sources in the separate CE environment."""
    require(TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA)
    require(BUILD_FACTORY, BUILD_FACTORY_SHA)
    if ce_factory_sha != CE_FACTORY_SHA or aba_factory_sha != ABA_FACTORY_SHA:
        raise ValueError("the actual frozen complete rank1-factor-cache AAA qualification factory is required")
    raw = read(require(PROD / "prepared.json", prepared_sha))
    entry = load(require(ABA_FACTORY, aba_factory_sha), "rank1_factor_cache_ABA_completed_entry")
    entry.bind_runtime_dependencies(raw)
    load(require(PROD / "runtime/white_receiver_tracking.py", raw["local_files"]["runtime/white_receiver_tracking.py"]),
         "white_receiver_tracking")
    c = entry.controller()
    require(c.__file__, CONTROLLER_SHA)
    ce = load(require(CE_FACTORY, ce_factory_sha), "rank1_factor_cache_ABA_reference_AAA_gate")
    return c, ce, entry, raw


def stable_qualification_identity(api):
    if (api["schema"] != "AXMAT_RANK1_FACTOR_CACHE_SEALED_REFERENCE_QUALIFICATION_ADMISSION_V1"
            or type(api["ABA_directory_exists_at_admission"]) is not bool):
        raise ValueError("explicit actual AAA qualification lifecycle field required")
    stable = copy.deepcopy(api)
    del stable["ABA_directory_exists_at_admission"]
    return stable


def build_binding(api):
    builder = load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "rank1_factor_cache_ABA_actual_build")
    terminal = api["actual_build_terminal_evidence"]
    if Path(terminal["path"]) != BUILD_TERMINAL / "terminal_return.json":
        raise ValueError("actual Root rank1-factor-cache build terminal evidence required")
    build = builder.production_admission(BUILD_SEAL, terminal["path"], terminal["sha256"])
    if (build["schema"] != "AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or build["rank1_factor_cache_budget_bytes"] != 512 * 2**20
            or any(build[key] is not True for key in ("rank1_factor_cache_controls_passed",
                "all_new_cache_outputs_bitwise_equal_to_uncached", "operator_identity_guard_negative_controls_passed",
                "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required"))
            or api["coupling_completion"]["all_actual_axial_selectors_verified"] is not True
            or api["coupling_completion"]["all_actual_rank1_factor_cache_guards_verified"] is not True
            or api["build_terminal_chain"]["build_seal"] != pin(BUILD / "seal.json")
            or api["actual_build_terminal_validation"] != build["actual_external_terminal_validation"]
            or api["build_terminal_chain"] != api["coupling_completion"]["actual_build_terminal_chain"]
            or api["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or api["resource_scope_contract"] != builder.resource_scope_contract()
            or api["resource_scope_contract"] != build["resource_scope_contract"]):
        raise ValueError("complete actual build/Root terminal/family resource contract differs")
    verify({item["path"]: item["sha256"] for item in api["build_terminal_chain"].values()})
    return builder, build


def actual_completed_aba(params):
    """Completed-case guard; intentionally does not call entry.actual_candidate."""
    c, ce, entry, raw = binding(params["prepared_sha256"], params["ce_factory_sha256"], params["aba_factory_sha256"])
    api = ce.qualification_admission(params["AAA_reference_seal_sha256"], params["qualification_sha256"],
        params["terminal_evidence"], params["terminal_evidence_sha256"])
    formal = dict(path=str(FORMAL), sha256=params["qualification_sha256"])
    if (api["qualification"] != formal or api["production_prepared"] != pin(PROD / "prepared.json")
            or api["reference_root"] != str(AAA_REFERENCE)
            or api["reference_seal_sha256"] != params["AAA_reference_seal_sha256"]
            or api["actual_external_terminal_evidence"] != dict(path=params["terminal_evidence"], sha256=params["terminal_evidence_sha256"])
            or Path(params["terminal_evidence"]) != AAA_TERMINAL / "terminal_return.json"
            or api["ABA_directory_exists_at_admission"] is not True
            or api["this_API_launched_ABA"] is not False or api["AAA_reference_run_started_ABA"] is not False
            or api["pending_receipt_eligible"] is not False or api["original_qualify_aba_guard_passed"] is not True
            or set(api["all_original_eight_checks"]) != set(GATES)
            or any(value != "PASS" for value in api["all_original_eight_checks"].values())):
        raise ValueError("actual sealed AAA qualification and external terminal bindings differ")
    env = ce.environment()
    info = c.verify_prepared(PROD / "prepared.json", params["prepared_sha256"])
    guard = c.qualify_aba(info, PROD, params["prepared_sha256"], FORMAL, params["qualification_sha256"])
    builder, actual_build = build_binding(api)
    status_path = require(PROD / "ABA/run_status.json", params["ABA_status_sha256"])
    status = read(status_path)
    state = status.get("cases", {}).get("ABA", {})
    count = state.get("completed_maps")
    if (info["experiment_id"] != "axial-material-qualified-AB-rank1-factor-cache-20261007"
            or info["budgets"] != entry.BUDGET or info["production_config"]["cells_per_zone"] != 16
            or info["production_config"]["sn"] != 32
            or status.get("classification") != "WAITING_REFERENCE" or status.get("case") != "ABA"
            or status.get("prepared_sha256") != params["prepared_sha256"]
            or status.get("reference_qualification") != formal
            or status.get("common_basis_sha256") != digest(PROD / "training/common_basis.xsm")
            or status.get("alpha") != 1 or status.get("outer_gate") != 5e-7
            or status.get("max_maps_per_case") != 100 or status.get("wall_cap_seconds_per_case") != 43200
            or state.get("classification") != "VALID_MET"
            or type(count) is not int or not 1 <= count <= 100
            or status.get("completed_maps") != count or len(state.get("maps", [])) != count
            or [row["epoch"] for row in state["maps"]] != list(range(1, count + 1))
            or status.get("error") is not None or not math.isfinite(status["finished_unix"])
            or status["final_resources"]["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or status["final_resources"]["resource_scope_contract"] != actual_build["resource_scope_contract"]):
        raise ValueError("actual complete rank1-factor-cache ABA fixed point and original guards required")
    final = PROD / "ABA" / f"map{count:03d}"
    if Path(state["final_directory"]) != final:
        raise ValueError("actual ABA final directory is outside its consecutive own maps")
    if {p.name for p in (PROD / "ABA").glob("map*")} != {f"map{i:03d}" for i in range(1, count + 1)}:
        raise ValueError("exact continuous ABA map namespace required")
    claim = read(require(PROD / "ABA/run_claim.json"))
    if (claim["case"] != "ABA" or claim["prepared_sha256"] != params["prepared_sha256"]
            or type(claim["pid"]) is not int or claim["pid"] <= 0 or claim["started_unix"] > status["finished_unix"]):
        raise ValueError("actual ABA run claim differs")
    stages = read(require(PROD / "ABA/stages.json"))["stages"]
    if not stages or any(row["status"] != "PASS" for row in stages):
        raise ValueError("all real ABA production stages must pass")
    bootstrap_labels = ["case_setup", "white_tracking", "make_route_contract", "bootstrap_axial", "bootstrap_radial", "b2i_seal_bootstrap"]
    map_labels = ["prepare_r64_next_projected", "picard_radial", "admit_candidate_radial", "picard_axial", "close_r64_returned",
                  "checker_parent", "check_one_map_xsm", "check_convergence_gate"]
    expected_labels = ["ABA/bootstrap/"+label for label in bootstrap_labels]
    expected_labels += [f"ABA/map{i:03d}/"+label for i in range(1, count+1) for label in map_labels]
    if [row["label"] for row in stages] != expected_labels:
        raise ValueError("complete original ABA bootstrap and eight stages per actual map required")
    axial_labels = {"ABA/bootstrap/bootstrap_axial"} | {f"ABA/map{i:03d}/picard_axial" for i in range(1, count + 1)}
    observer_guard = load(PROD / "runtime/rank1_factor_cache_admission.py", "rank1_factor_cache_admission")
    for row in stages:
        log = require(PROD / (row["label"] + ".log"), row["log_sha256"])
        if row["label"] in axial_labels:
            text = log.read_text(errors="replace")
            actual_selector = observer_guard.admit_actual_axial_selector(text, log)
            actual_cache = observer_guard.admit_actual_rank1_factor_cache(text, log,
                len(actual_selector["actual_observers"]))
            if (row["command"] != [str(PROD / "runtime/Dragon")]
                    or row["transport_status_before_selector_guard"] != "PASS"
                    or row["rank1_factor_cache_selector_guard"] != actual_selector
                    or row["rank1_factor_cache_guard"] != actual_cache or actual_cache["status"] != "PASS"
                    or actual_selector["status"] != "PASS"
                    or actual_selector["expected"] != OBSERVER_EXPECTED or not actual_selector["actual_observers"]):
                raise ValueError("all complete actual ABA axial logs must prove every original selector and exact rank1 cache guard")
        elif "rank1_factor_cache_selector_guard" in row or "rank1_factor_cache_guard" in row:
            raise ValueError("unexpected axial selector or factor-cache guard on a non-axial stage")
        if (not 0 <= row["elapsed_seconds"] < row["wall_cap_seconds"]
                or row["resource_after"]["artifact_budget_bytes"] != HISTORY_CAP
                or row["resource_after"]["min_free_bytes"] != FREE_FLOOR
                or row["resource_after"]["resource_scope_policy"] != HISTORY_SCOPE_POLICY
                or row["resource_after"]["resource_scope_contract"] != actual_build["resource_scope_contract"]):
            raise ValueError("actual production stage elapsed/storage limits differ")
    for folder in (PROD / "archives", PROD / "training", PROD / "ABA/bootstrap",
                   *[PROD / "ABA" / f"map{i:03d}" for i in range(1, count + 1)]):
        c.verify_sealed_directory(folder)
    c.require_file(PROD / "ABA/bootstrap/basis_reference.xsm", status["common_basis_sha256"])
    gate = c.parse_gate((final / "check_convergence_gate.log").read_text())
    if gate["classification"] != "VALID_MET" or gate["defects"] != state["maps"][-1]["defects"]:
        raise ValueError("actual final raw convergence gate differs from ABA status")
    for i, row in enumerate(state["maps"], 1):
        previous = c.parse_gate((PROD / "ABA" / f"map{i:03d}/check_convergence_gate.log").read_text())
        if previous["classification"] != row["classification"] or previous["defects"] != row["defects"]:
            raise ValueError("actual raw map gate differs from the full consecutive status ledger")
        if i < count and previous["classification"] != "VALID_NOT_MET":
            raise ValueError("original first-MET stopping rule changed")
    from numerical_layout_admission import verify_common_basis
    if read(PROD / "ABA/numerical_layout_basis_admission.json") != verify_common_basis(PROD / "training/common_basis.xsm"):
        raise ValueError("actual ABA common-basis numerical layout proof differs")
    launch = read(require(ABA_ENTRY / "declaration.json", params["ABA_execution_declaration_sha256"]))
    verify(launch["files"])
    if (launch["schema"] != "AXMAT_RANK1_FACTOR_CACHE_SEALED_REFERENCE_TO_ABA_DECLARATION_V1"
            or launch["production_prepared"] != pin(PROD / "prepared.json")
            or launch["formal_qualification"] != formal or launch["reference_seal"] != pin(AAA_REFERENCE / "seal.json")
            or launch["actual_external_terminal_evidence"] != api["actual_external_terminal_evidence"]
            or launch["helper"] != pin(ABA_FACTORY) or launch["CE_factory"] != pin(CE_FACTORY)
            or launch["production_controller"] != pin(c.__file__) or launch["original_case_budgets"] != entry.BUDGET
            or launch["original_gate_names"] != list(GATES)
            or launch["original_production_qualify_aba"] != guard
            or launch["actual_reference_API"]["ABA_directory_exists_at_admission"] is not False
            or stable_qualification_identity(launch["actual_reference_API"]) != stable_qualification_identity(api)
            or entry.stable_qualification_identity(api) != stable_qualification_identity(api)
            or launch["actual_qualification_lifecycle"] != entry.lifecycle_contract()
            or launch["actual_resource_monitor"] != entry.monitor_contract(c, info)
            or launch["explicit_resource_monitor_binding_changed"] is not False
            or launch["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or launch["resource_scope_contract"] != actual_build["resource_scope_contract"]
            or launch["pending_receipt_eligible"] is not False):
        raise ValueError("real ABA execution declaration is not bound to the same qualification")
    handoff_path = require(ABA_ENTRY / "RUN/handoff.json")
    handoff = read(handoff_path)
    if (handoff["schema"] != "AXMAT_RANK1_FACTOR_CACHE_ACTUAL_ABA_HANDOFF_V1"
            or handoff["classification"] != "ALL_GUARDS_PASSED_CALL_FROZEN_RANK1_FACTOR_CACHE_ABA_RUN_WITH_EXISTING_DYNAMIC_MONITOR"
            or handoff["declaration_sha256"] != params["ABA_execution_declaration_sha256"]
            or handoff["formal_qualification"] != formal or handoff["production_prepared"] != pin(PROD / "prepared.json")
            or handoff["AAA_status"] != api["AAA_status"] or handoff["original_guard"] != guard
            or handoff["actual_external_terminal_evidence"] != api["actual_external_terminal_evidence"]
            or handoff["equivalent_original_CLI_arguments"] != launch["production_command"]
            or handoff["scientific_callables_and_budgets_changed"] is not False
            or handoff["actual_launch_reference_API"] != launch["actual_reference_API"]
            or handoff["actual_launch_reference_API"]["ABA_directory_exists_at_admission"] is not False
            or handoff["actual_qualification_lifecycle"] != entry.lifecycle_contract()
            or handoff["actual_resource_monitor"] != launch["actual_resource_monitor"]
            or handoff["resource_monitor_binding_changed"] is not False
            or handoff["source_files_and_module_identity_changed"] is not False
            or handoff["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or handoff["resource_scope_contract"] != actual_build["resource_scope_contract"]
            or handoff["actual_build_terminal_evidence"] != api["actual_build_terminal_evidence"]
            or handoff["actual_build_terminal_validation"] != api["actual_build_terminal_validation"]
            or handoff["build_terminal_chain"] != api["build_terminal_chain"]
            or handoff["pending_receipt_eligible"] is not False):
        raise ValueError("actual guarded ABA handoff and qualification lineage differ")
    receipt_item = handoff["actual_repeated_CE_API_receipt"]
    if Path(receipt_item["path"]) != ABA_ENTRY / "RUN/receipt.json":
        raise ValueError("actual launch must bind its own repeated read-only API call")
    receipt = read(require(receipt_item["path"], receipt_item["sha256"]))
    for key in ("stdout", "actual_API_return", "watchdog", "stages"):
        require(receipt[key]["path"], receipt[key]["sha256"])
    w = read(receipt["watchdog"]["path"])
    expected_API_command = [env["executable"], str(CE_FACTORY), "admit-qualification",
        "--sha256", params["AAA_reference_seal_sha256"], "--qualification-sha256", params["qualification_sha256"],
        "--terminal-evidence", params["terminal_evidence"], "--terminal-evidence-sha256", params["terminal_evidence_sha256"]]
    actual_API_stages = read(receipt["stages"]["path"])["stages"]
    if (receipt["phase"] != "RUN" or receipt["classification"] != "COMPLETE_READ_ONLY_REFERENCE_QUALIFICATION_API_CALL"
            or receipt["returncode"] != 0 or receipt["extra_transport_calls"] != 0 or receipt["extra_linear_solves"] != 0
            or receipt["command"] != expected_API_command
            or len(actual_API_stages) != 1 or actual_API_stages[0]["command"] != expected_API_command
            or actual_API_stages[0]["status"] != "PASS" or actual_API_stages[0]["label"] != "RUN/sealed_reference_guard"
            or read(receipt["actual_API_return"]["path"])["ABA_directory_exists_at_admission"] is not False
            or strict_json(receipt["stdout"]["path"]) != read(receipt["actual_API_return"]["path"])
            or read(receipt["actual_API_return"]["path"]) != handoff["actual_launch_reference_API"]
            or stable_qualification_identity(read(receipt["actual_API_return"]["path"])) != stable_qualification_identity(api)
            or w["command"] != receipt["command"] or w["returncode"] != 0 or w["limit_failure"] is not None
            or w["rss_cap_mib"] != 512 or not 0 <= w["sampled_peak_rss_mib"] < 512
            or not 0 < w["wall_cap_seconds"] <= 120 or not 0 <= w["elapsed_seconds"] < w["wall_cap_seconds"]
            or w["own_child_only"] is not True or w["liveness_group_cleanup"] is not True):
        raise ValueError("real launch API return/watchdog evidence did not pass")
    build = launch["build_admission"]
    if (build != actual_build or build["build_seal_sha256"] != BUILD_SEAL
            or info["runtime_sources"]["Dragon"] != build["corrected_runtime"]
            or launch["actual_build_terminal_evidence"] != api["actual_build_terminal_evidence"]
            or launch["build_terminal_chain"] != api["build_terminal_chain"]):
        raise ValueError("actual ABA runtime differs from the completed rank1-factor-cache build")
    declared_receipt = read(require(launch["declaration_read_only_API_receipt"]["path"], launch["declaration_read_only_API_receipt"]["sha256"]))
    if (Path(launch["declaration_read_only_API_receipt"]["path"]) != ABA_ENTRY / "DECLARE/receipt.json"
            or strict_json(require(declared_receipt["stdout"]["path"], declared_receipt["stdout"]["sha256"])) != launch["actual_reference_API"]
            or read(require(declared_receipt["actual_API_return"]["path"], declared_receipt["actual_API_return"]["sha256"])) != launch["actual_reference_API"]):
        raise ValueError("actual launch declaration stdout must preserve the complete False lifecycle return")
    return c, ce, entry, info, status, final, api, env


def storage(c, roots, reservation=0):
    builder = load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "rank1_factor_cache_ABA_actual_build")
    actual_roots = sorted(set(roots) | {str(p) for p in ART.glob("axial-material-*")} | {str(SOURCE), str(OUT), str(TERMINAL)})
    resources = builder.DynamicHistoryResources(ART, actual_roots, FREE_FLOOR, HISTORY_CAP, c.ResourceFailure)
    snap = resources.check()
    if snap["artifact_bytes"] + reservation >= HISTORY_CAP or snap["disk_free_bytes"] - reservation < FREE_FLOOR:
        raise ValueError("complete history plus independent ABA reference reservation exceeds 96GiB/free8GiB")
    return resources, snap, actual_roots


def source_protocol(execution):
    staged = read(require(STAGED / "declaration.json"))
    if (staged["schema"] != "AXMAT_ABA_INDEPENDENT_REFERENCE_INPUT_STAGING_V1"
            or staged["case"] != "ABA" or staged["native_transport_started"] is not False
            or staged["sampling"] != SAMPLING):
        raise ValueError("original full ordinary ABA sample definition required")
    verify(staged["files"])
    verify(staged["inherited_physical_source_pins"])
    for name in INPUTS[:3]:
        if (STAGED / name).read_bytes() != (ORIGINAL_ABA / name).read_bytes():
            raise ValueError("original ABA physical or tally XML changed")
    settings = ET.parse(STAGED / "settings.xml").getroot()
    for name, value in (("seed", 310033), ("inactive", 100), ("particles", 10000),
                        ("generations_per_batch", 10), ("batches", 2100)):
        if int(settings.findtext(name)) != value:
            raise ValueError("exact original ABA sampling settings differ: " + name)
    if [int(x) for x in settings.findtext("state_point/batches").split()] != list(range(101, 2101)):
        raise ValueError("all 2000 original consecutive zero-padded statepoints required")
    contract = read(STAGED / "reference_contract.json")
    if (contract["schema"] != "AXMAT_CE_INPUT_V2" or contract["case"] != "ABA"
            or len(contract["region_layer_bins"]) != 96 or len(contract["layer_bins"]) != 12
            or len(contract["plane_bins"]) != 13
            or contract["directional_current_filter"]["raw_bin_order"] != ["positive_z", "negative_z"]
            or contract["directional_current_filter"]["signed_score"] is not True):
        raise ValueError("original complete ABA physical observation/current contract differs")
    verify({str(STAGED / name): sha for name, sha in contract["input_hashes"].items()})
    require(OPENMC, OPENMC_SHA)
    require(OPENMC.parent.parent / "lib/libopenmc.dylib", OPENMC_LIBRARY_SHA)
    require(contract["cross_sections"]["path"], XS_SHA)
    verify(execution["files"])
    data = {path: sha for path, sha in execution["files"].items()
            if path.startswith("/Users/wen/openmc-workspace/data/") and path.endswith(".h5")}
    if len(data) != 34:
        raise ValueError("all original 34 native nuclide data files required")
    return staged, contract, data


def loader_files(env, execution):
    """Resolve and pin native load commands in the future declaration, read-only."""
    bases = (OPENMC.parent.parent / "lib",)
    queue = [OPENMC, OPENMC.parent.parent / "lib/libopenmc.dylib"]
    files, commands, aliases, rpaths = {}, {}, {}, {}
    while queue:
        path = queue.pop(0).resolve(strict=True)
        if str(path) in files:
            continue
        files[str(path)] = digest(require(path))
        text = subprocess.run(["/usr/bin/otool", "-L", str(path)], check=True, capture_output=True, text=True, timeout=30).stdout
        commands[str(path)] = text
        metadata = subprocess.run(["/usr/bin/otool", "-l", str(path)], check=True, capture_output=True, text=True, timeout=30).stdout
        rpaths[str(path)] = re.findall(r"cmd LC_RPATH\s+cmdsize \d+\s+path (.*?) \(offset \d+\)", metadata)
        for line in text.splitlines()[1:]:
            library = line.strip().split(" (", 1)[0]
            if library.startswith(("/usr/lib/", "/System/Library/")):
                continue
            if library.startswith("@loader_path/"):
                dep = path.parent / library.removeprefix("@loader_path/")
            elif library.startswith("@executable_path/"):
                dep = OPENMC.parent / library.removeprefix("@executable_path/")
            elif library.startswith("@rpath/"):
                options = [base / library.removeprefix("@rpath/") for base in bases]
                options = [p.resolve(strict=True) for p in options if p.is_file()]
                if len(set(options)) != 1:
                    raise ValueError("native library rpath resolution is ambiguous: " + library)
                dep = options[0]
            elif library.startswith("/"):
                dep = Path(library)
            else:
                raise ValueError("unsupported native library load command: " + library)
            canonical = dep.resolve(strict=True)
            aliases[str(dep)] = dict(canonical=str(canonical), sha256=digest(require(canonical)))
            queue.append(canonical)
    verify(files)
    loader = {key: value for key, value in os.environ.items() if key.startswith(("DYLD_", "LD_"))
              or key in ("PYTHONPATH", "OPENBLAS_CORETYPE", "OPENMC_CROSS_SECTIONS")}
    if (any(value for key, value in loader.items() if key.startswith(("DYLD_", "LD_")))
            or rpaths[str(OPENMC.resolve())] != [str(OPENMC.parent.parent / "lib"), "/Users/wen/openmc/build/lib"]):
        raise ValueError("native default loader path must be the actual original first conda rpath without injection/override")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_ABA_FROZEN_NATIVE_LOADER_V1", files=files,
        load_commands=commands, library_aliases=aliases, actual_LC_RPATH=rpaths,
        executable_rpath_first_match_resolution=str(bases[0]), environment=loader, thread_environment={key: "1" for key in THREADS},
        original_native_argv=[str(OPENMC), "-s", "1"], original_loader_was_not_archived=True,
        additional_frozen_loader_control=True, native_RSS_control_is_new=True)


def replace_function(source, name, body):
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    lines = source.splitlines(True)
    return "".join(lines[:node.lineno-1]) + body.rstrip() + "\n" + "".join(lines[node.end_lineno:])


NATIVE_LOAD = '''def load_contract(manifest, expected_sha256):
    manifest = Path(manifest).resolve(strict=True)
    if digest(manifest) != expected_sha256:
        raise RuntimeError('execution declaration identity changed')
    contract = json.loads(manifest.read_text())
    item = contract['actual_factory']
    if digest(item['path']) != item['sha256']:
        raise RuntimeError('actual new ABA reference factory changed')
    spec = importlib.util.spec_from_file_location('actual_ABA_native_reference_guard', item['path'])
    actual = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(actual)
    return actual.native_contract_admission(manifest, expected_sha256)
'''


NATIVE_EXECUTE = '''def execute(manifest, expected_sha256):
    contract, folder, resources, before_resources = load_contract(manifest, expected_sha256)
    cap = contract['wall_seconds']
    rss_cap = contract['native_rss_cap_mib']
    helper = load_watchdog(contract['watchdog_source'])
    env = dict(os.environ)
    for key in tuple(env):
        if key.startswith(('DYLD_', 'LD_')) or key in ('PYTHONPATH', 'OPENBLAS_CORETYPE', 'OPENMC_CROSS_SECTIONS'):
            env.pop(key)
    env.update(contract['native_loader']['environment'])
    env.update(contract['native_loader']['thread_environment'])
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    started = time.monotonic()
    command = [contract['executable'], '-s', '1']
    with (folder/'run_claim.json').open('x') as stream:
        json.dump(dict(schema='AXMAT_RANK1_FACTOR_CACHE_ABA_NATIVE_ATTEMPT_V1',
            parent_pid=os.getpid(), started_monotonic=started, started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            manifest_sha256=expected_sha256, wall_seconds=cap, native_rss_cap_mib=rss_cap,
            command=command, retries=0, threads=1, numeric_children_at_once=1,
            native_loader=contract['native_loader'], actual_factory=contract['actual_factory']), stream, indent=2, allow_nan=False)
        stream.flush()
        os.fsync(stream.fileno())
    process = watchdog = None
    write_fd = None
    peak = 0.0
    samples = 0
    last_disk = 0.0
    result = dict(status='FAILED', returncode=None, error=None, scientific_acceptance=False,
                  resources_before=before_resources, command=command, direct_native_PID=True,
                  wall_cap_seconds=cap, native_rss_cap_mib=rss_cap, retries=0)
    handlers = {sig: signal.signal(sig, signal.default_int_handler)
                for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    def rss_sample():
        nonlocal peak, samples
        if process.poll() is not None:
            return
        observed = subprocess.run(['/bin/ps', '-o', 'rss=', '-p', str(process.pid)],
            capture_output=True, text=True, timeout=5.0)
        if not observed.stdout.strip():
            if process.poll() is not None:
                return
            raise RuntimeError('cannot sample the active direct native PID RSS')
        if observed.returncode != 0 or not observed.stdout.strip().isdigit():
            raise RuntimeError('invalid direct native PID RSS observation')
        actual = int(observed.stdout.strip()) / 1024.0
        peak = max(peak, actual)
        samples += 1
        if actual >= rss_cap:
            result['limit_failure'] = 'DIRECT_NATIVE_RSS'
            raise RuntimeError('direct native RSS cap exceeded')
    try:
        with (folder/'openmc.log').open('xb') as log:
            result['resources_latest'] = resources.check()
            if time.monotonic() - started >= cap:
                raise subprocess.TimeoutExpired(command, cap)
            process = subprocess.Popen(command, cwd=folder, stdout=log, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL, env=env, start_new_session=True)
            result['native_pid'] = process.pid
            read_fd, write_fd = os.pipe()
            try:
                watchdog = helper.start_liveness_watchdog(read_fd, process.pid, 5.0)
            finally:
                os.close(read_fd)
            while True:
                if time.monotonic()-last_disk >= 5.0:
                    result['resources_latest'] = resources.check()
                    last_disk = time.monotonic()
                rss_sample()
                remaining = cap - (time.monotonic() - started)
                if remaining <= 0:
                    result['limit_failure'] = 'DIRECT_NATIVE_WALL'
                    raise subprocess.TimeoutExpired(command, cap)
                try:
                    result['returncode'] = process.wait(timeout=min(0.2, remaining))
                    break
                except subprocess.TimeoutExpired:
                    continue
            result['resources_latest'] = resources.check()
            if result['returncode'] != 0:
                raise RuntimeError('OpenMC nonzero exit')
            if samples == 0:
                raise RuntimeError('no actual direct native RSS witness')
            result['status'] = 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS'
    except BaseException as exc:
        result['error'] = repr(exc)
        if isinstance(exc, ResourceFailure):
            result['status'] = 'FAIL_RESOURCE'
            result['resources_failure'] = exc.snapshot
        if process is not None and process.poll() is None:
            helper.terminate_process_group(process.pid, 5.0, process)
            result['returncode'] = process.wait()
    finally:
        cleanup = True
        try:
            if write_fd is not None:
                if watchdog is not None:
                    helper.finish_liveness_watchdog(write_fd, watchdog)
                else:
                    os.close(write_fd)
        except BaseException as cleanup_error:
            cleanup = False
            result.update(status='FAILED', error=result['error'] or repr(cleanup_error), limit_failure='LIVENESS_CLEANUP')
        for sig, handler in handlers.items():
            signal.signal(sig, handler)
        # Preserve raw files and full native stdout identities before end,
        # completeness, resource or elapsed acceptance gates.
        result['log_sha256'] = digest(folder/'openmc.log') if (folder/'openmc.log').is_file() else None
        result['outputs'] = {p.name:digest(p) for p in sorted(folder.glob('*.h5'))}
        result['output_sizes'] = {p.name:p.stat().st_size for p in sorted(folder.glob('*.h5'))}
        result['sampled_peak_native_rss_mib'] = peak
        result['native_rss_samples'] = samples
        result['liveness_group_cleanup'] = cleanup
        result['elapsed_seconds'] = time.monotonic() - started
        if result['elapsed_seconds'] >= cap:
            result.update(status='FAILED', limit_failure='DIRECT_NATIVE_WALL_THROUGH_RAW_INVENTORY',
                          error=result['error'] or 'native wall cap exhausted during raw closeout')
        watch = dict(schema='AXMAT_RANK1_FACTOR_CACHE_DIRECT_NATIVE_WATCHDOG_V1', command=command,
            native_pid=result.get('native_pid'), direct_native_PID=True, native_rss_cap_mib=rss_cap,
            wall_cap_seconds=cap, sampled_peak_native_rss_mib=peak, native_rss_samples=samples,
            returncode=result['returncode'], limit_failure=result.get('limit_failure'),
            elapsed_seconds=result['elapsed_seconds'], liveness_group_cleanup=cleanup,
            native_loader=contract['native_loader'], actual_parent_pid=os.getpid())
        with (folder/'native.watchdog.json').open('x') as stream:
            json.dump(watch, stream, indent=2, allow_nan=False)
            stream.write('\\n')
        result['watchdog_sha256'] = digest(folder/'native.watchdog.json')
        with (folder/'native_result.json').open('x') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write('\\n')
    return result
'''


def render_native(target):
    parent = CE / "runtime/ce_execution.py"
    old = require(parent).read_text()
    new = replace_function(old, "load_contract", NATIVE_LOAD)
    new = replace_function(new, "execute", NATIVE_EXECUTE)
    anchor = "import production_inputs\nimport production_runner"
    replacement = "import sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, " + repr(str(PROD / "runtime")) + ")\n" + anchor
    if new.count(anchor) != 1:
        raise ValueError("native canonical producer import anchor is ambiguous")
    new = new.replace(anchor, replacement)
    before = {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(old).body if isinstance(n, ast.FunctionDef)}
    after = {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(new).body if isinstance(n, ast.FunctionDef)}
    if before.keys() != after.keys() or any(before[n] != after[n] for n in before if n not in ("load_contract", "execute")):
        raise ValueError("native helper changed outside explicit admission/direct-RSS lifecycle")
    target.write_text(new)
    target.with_suffix(".patch").write_text("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
        fromfile=str(parent), tofile=str(target))))
    return dict(parent=pin(parent), candidate=pin(target), unchanged_functions=["digest", "load_watchdog", "main"],
        admission_changed=True, explicit_direct_native_RSS_lifecycle_changed=True, additional_native_RSS_cap_mib=2048,
        original_wall_cap_seconds=64800, original_native_argv_unchanged=True, original_sampler_unchanged=True,
        original_native_lifecycle_word_exact_claimed=False, loader_control_is_new=True, module_identity_reassigned=False)


def factory_source_equivalence():
    """Preserve the old scientific functions and literal native lifecycle."""
    old = require(TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA).read_text()
    current = Path(__file__).read_text()
    restored = current.replace("rank1-factor-cache", "moment-order").replace("rank1_factor_cache", "moment_order").replace("RANK1_FACTOR_CACHE", "MOMENT_ORDER").replace("20261007", "20261006")
    def definitions(text):
        return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(text).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    before, after = definitions(old), definitions(restored)
    exact = ("source_protocol", "loader_files", "physical_worker", "project_worker", "render_native",
             "scientific_decision", "scientific_source_proof", "validate_physical_outputs")
    if any(before[name] != after[name] for name in exact):
        raise ValueError("scientific/native source changed outside reversible rank1-factor-cache identity names")
    def literals(text):
        return {node.targets[0].id: ast.literal_eval(node.value) for node in ast.parse(text).body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in ("NATIVE_LOAD", "NATIVE_EXECUTE")}
    if literals(old) != literals(restored):
        raise ValueError("literal direct-native execution arithmetic/loader/lifecycle changed")
    preserved_constants = {"HISTORY_CAP", "FREE_FLOOR", "NATIVE_WALL", "NATIVE_RSS", "PREPARE_WALL",
        "ANALYSIS_WALL", "HOST_RSS", "HOST_MARGIN", "THREADS", "GATES", "SAMPLING", "INPUTS",
        "TRACK_RECORDS", "HISTORY_SCOPE_POLICY", "OBSERVER_EXPECTED", "ANALYSIS_TAIL_FIELDS"}
    def constants(text):
        result = {}
        for node in ast.parse(text).body:
            if isinstance(node, ast.Assign):
                names = {item.id for target in node.targets for item in ast.walk(target) if isinstance(item, ast.Name)}
                if names & preserved_constants:
                    result[tuple(sorted(names))] = ast.dump(node.value, include_attributes=False)
        return result
    if constants(old) != constants(restored):
        raise ValueError("original sampling, eight gates, threads, wall/RSS/archive/family caps or complete-tail fields changed")
    return dict(parent=pin(TEMPLATE_FACTORY), candidate=pin(Path(__file__).resolve()),
        identity_inverse_restored_scientific_function_AST_exact=list(exact),
        literal_native_callbacks_identity_inverse_restored_exact=True,
        original_sampling_gate_resource_and_tail_constant_AST_exact=sorted(preserved_constants),
        scientific_source_protocol_loader_projection_and_eight_checks_unchanged=True,
        revision_scope="Actual rank1-factor-cache completed/build/terminal identities, complete selector/cache log guards, dynamic family resources, retained completed API stdout and read-only final terminal qualification gate",
        entire_factory_AST_exact_claimed=False, original_sampler_and_native_argv_unchanged=True)


def completed_api_command(params, env):
    return [env["executable"], str(CE_FACTORY), "admit-qualification", "--sha256", params["AAA_reference_seal_sha256"],
        "--qualification-sha256", params["qualification_sha256"], "--terminal-evidence", params["terminal_evidence"],
        "--terminal-evidence-sha256", params["terminal_evidence_sha256"]]


def completed_api_proof(item, api, params, env):
    folder = SOURCE / "COMPLETED_QUALIFICATION"
    if Path(item["path"]) != folder / "receipt.json":
        raise ValueError("only this actual exclusive completed qualification API archive is eligible")
    receipt = read(require(item["path"], item["sha256"]))
    for key in ("stdout", "actual_API_return", "watchdog", "stages"):
        require(receipt[key]["path"], receipt[key]["sha256"])
    command = completed_api_command(params, env)
    stages = read(receipt["stages"]["path"])["stages"]
    w = read(receipt["watchdog"]["path"])
    returned = strict_json(receipt["stdout"]["path"])
    if (receipt["classification"] != "COMPLETE_READ_ONLY_COMPLETED_REFERENCE_QUALIFICATION_API_CALL"
            or receipt["command"] != command or receipt["returncode"] != 0
            or receipt["extra_transport_calls"] != 0 or receipt["extra_linear_solves"] != 0
            or returned != api or read(receipt["actual_API_return"]["path"]) != returned
            or returned["ABA_directory_exists_at_admission"] is not True
            or len(stages) != 1 or stages[0]["label"] != "COMPLETED_QUALIFICATION/sealed_reference_guard"
            or stages[0]["command"] != command or stages[0]["status"] != "PASS"
            or receipt["stdout"] != pin(folder / "sealed_reference_guard.log")
            or stages[0]["log_sha256"] != receipt["stdout"]["sha256"]
            or w["command"] != command or w["returncode"] != 0 or w["limit_failure"] is not None
            or w["rss_cap_mib"] != HOST_RSS or not 0 <= w["sampled_peak_rss_mib"] < HOST_RSS
            or not 0 < w["wall_cap_seconds"] <= 120 or not 0 <= w["elapsed_seconds"] < w["wall_cap_seconds"]
            or w["own_child_only"] is not True or w["liveness_group_cleanup"] is not True):
        raise ValueError("actual completed qualification stdout/direct child supervision failed")
    return receipt


def retain_completed_api(actual, params, resources):
    c, ce, entry, info, status, final, api, env = actual
    folder = SOURCE / "COMPLETED_QUALIFICATION"
    absent(folder)
    folder.mkdir()
    full = load(require(FULL_FACTORY, FULL_SHA), "rank1_factor_cache_ABA_reference_ownRSS")
    ce.live_guard_provenance(full, c, info)
    supervisor = full.OwnRSSSerialExecutor(SOURCE, 120, "COMPLETED_QUALIFICATION", resources)
    supervisor.env = dict(os.environ, **{key: "1" for key in THREADS}, PYTHONDONTWRITEBYTECODE="1")
    command = completed_api_command(params, env)
    supervisor.execute(folder, "sealed_reference_guard", command, 120)
    stdout = folder / "sealed_reference_guard.log"
    returned = strict_json(stdout)
    if returned != api or returned["ABA_directory_exists_at_admission"] is not True:
        raise ValueError("actual completed qualification CLI return differs from the independently revalidated API")
    write_new(folder / "ce_api_return.json", returned)
    write_new(folder / "receipt.json", dict(classification="COMPLETE_READ_ONLY_COMPLETED_REFERENCE_QUALIFICATION_API_CALL",
        command=command, returncode=0, extra_transport_calls=0, extra_linear_solves=0,
        stdout=pin(stdout), actual_API_return=pin(folder / "ce_api_return.json"),
        watchdog=pin(folder / "sealed_reference_guard.watchdog.json"), stages=pin(folder / "stages.json")))
    item = pin(folder / "receipt.json")
    completed_api_proof(item, api, params, env)
    return item


def declare(params):
    absent(SOURCE)
    absent(OUT)
    absent(TERMINAL)
    actual = actual_completed_aba(params)
    c, ce, entry, info, status, final, api, env = actual
    execution = read(require(CE / "AAA/execution.json"))
    staged, contract, data = source_protocol(execution)
    native = read(require(CE / "AAA/native_result.json"))
    names = {f"statepoint.{b:04d}.h5" for b in range(101, 2101)}
    if (native["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS" or native["returncode"] != 0
            or native["error"] is not None or {n for n in native["outputs"] if n.startswith("statepoint.")} != names):
        raise ValueError("actual old complete AAA sample required solely for storage forecast")
    verify({str(CE / "AAA" / name): sha for name, sha in native["outputs"].items()})
    sample_bytes = regular_bytes(CE / "AAA")
    if sample_bytes != 443783974:
        raise ValueError("immutable measured old AAA forecast namespace/footprint differs")
    reserve = math.ceil(sample_bytes * 1.5) + HOST_MARGIN
    roots = set(info["resource_roots"]) | set(read(ABA_ENTRY / "declaration.json")["resource_roots"])
    for folder in (BUILD, FULL, CAUSAL, AAA_REFERENCE):
        roots.update(read(require(folder / "declaration.json"))["resource_roots"])
    resources, snap, roots = storage(c, roots, reserve)
    loader = loader_files(env, execution)
    full = load(require(FULL_FACTORY, FULL_SHA), "rank1_factor_cache_ABA_reference_ownRSS")
    guard = ce.live_guard_provenance(full, c, info)
    require(EXPORTER, EXPORTER_SHA)
    require(EXPORT_SOURCE, EXPORT_SOURCE_SHA)
    SOURCE.mkdir()
    (SOURCE / "runtime").mkdir()
    equivalents = {}
    for name in ("reference_statistics.py", "compare_balance_symmetry.py"):
        parent = CE / "runtime" / name
        target = SOURCE / "runtime" / name
        shutil.copy2(require(parent), target)
        require(target, digest(parent))
        equivalents[name] = dict(parent=pin(parent), candidate=pin(target), byte_exact=True)
    target = SOURCE / "runtime/project_refined_observables.py"
    shutil.copy2(require(PROJECT), target)
    require(target, digest(PROJECT))
    equivalents["projection"] = dict(parent=pin(PROJECT), candidate=pin(target), byte_exact=True)
    equivalents["native"] = render_native(SOURCE / "runtime/ce_execution.py")
    equivalents["scientific_decision"] = scientific_source_proof()
    equivalents["factory_binding_revision"] = factory_source_equivalence()
    shutil.copy2(require(PROD / "runtime/run_bounded_dragon.py"), SOURCE / "runtime/run_bounded_dragon.py")
    completed_qualification = retain_completed_api(actual, params, resources)
    write_new(SOURCE / "source_equivalence.json", equivalents)
    write_new(SOURCE / "analysis_environment.json", env)
    write_new(SOURCE / "live_guard_provenance.json", guard)
    view = copy.deepcopy(read(info["case_spec"]["path"]))
    view["geometry"]["cells_per_zone"] = 4
    view["observation_projection_view"] = dict(native_case_spec=info["case_spec"], native_cells=48,
        original_observation_cells=12, solver_not_changed_by_this_view=True, one_original_global_normalizer=True)
    write_new(SOURCE / "observation_case_spec.json", view)
    files = dict(execution["files"])
    files.update(staged["files"])
    files.update(staged["inherited_physical_source_pins"])
    files.update(env["files"])
    files.update(loader["files"])
    files.update({str(PROD / name): sha for name, sha in info["local_files"].items()})
    for path in (Path(__file__).resolve(), TEMPLATE_FACTORY, BUILD_FACTORY, CE_FACTORY, ABA_FACTORY, FULL_FACTORY, PHYSICAL, PROJECT,
            EXPORTER, EXPORT_SOURCE, PROD / "prepared.json", PROD / "ABA/run_status.json", PROD / "ABA/run_claim.json",
            PROD / "ABA/stages.json", PROD / "ABA/numerical_layout_basis_admission.json", PROD / "archives/result.json",
            PROD / "training/result.json", PROD / "ABA/bootstrap/result.json", final / "result.json",
            final / "check_convergence_gate.log", PROD / "ABA/bootstrap/initial_axial_track.xsm",
            PROD / "ABA/bootstrap/initial_axial_track_unmarked.xsm", PROD / "ABA/bootstrap/initial_axial_macrolib.xsm",
            final / "closed_axial.xsm", PROD / "archives/aba_snapshots.xsm", PROD / "AAA/bootstrap/initial_axial_track_unmarked.xsm",
            OLD_PROD / "AAA/bootstrap/initial_axial_track.xsm", STAGED / "declaration.json", BUILD / "seal.json",
            FORMAL, AAA_REFERENCE / "seal.json", Path(params["terminal_evidence"]), ABA_ENTRY / "declaration.json",
            ABA_ENTRY / "RUN/handoff.json", ABA_ENTRY / "RUN/receipt.json", CE / "AAA/native_result.json", CE / "AAA/openmc.log",
            ART / "axial-material-tools-20261003/input_equivalence.json", *[SOURCE / name for name in regular_files(SOURCE)]):
        files[str(path)] = digest(require(path))
    files.update(data)
    for stage in read(PROD / "ABA/stages.json")["stages"]:
        files[str(PROD / (stage["label"] + ".log"))] = stage["log_sha256"]
    count = status["cases"]["ABA"]["completed_maps"]
    for epoch in range(1, count + 1):
        files[str(PROD / "ABA" / f"map{epoch:03d}/result.json")] = digest(PROD / "ABA" / f"map{epoch:03d}/result.json")
    for item in api["build_terminal_chain"].values():
        files[item["path"]] = item["sha256"]
    for phase in ("DECLARE", "RUN"):
        receipt = read(ABA_ENTRY / phase / "receipt.json")
        files[str(ABA_ENTRY / phase / "receipt.json")] = digest(ABA_ENTRY / phase / "receipt.json")
        for key in ("stdout", "actual_API_return", "watchdog", "stages"):
            files[receipt[key]["path"]] = receipt[key]["sha256"]
    files.update({str(CE / "AAA" / name): sha for name, sha in regular_files(CE / "AAA").items()})
    verify(files)
    d = dict(schema="AXMAT_RANK1_FACTOR_CACHE_ABA_INDEPENDENT_NATIVE_REFERENCE_DECLARATION_V1", case="ABA",
        classification="DECLARED_AFTER_ACTUAL_QUALIFIED_AAA_AND_SEALED_ABA_MET_NOT_PREPARED_OR_RUN",
        declared_unix=time.time(), actual_parameters=params, files=files, actual_factory=pin(Path(__file__).resolve()),
        production_prepared=pin(PROD / "prepared.json"), ABA_status=pin(PROD / "ABA/run_status.json"),
        final_stage_seal=pin(final / "result.json"), actual_AAA_qualification_API_return=api,
        all_actual_ABA_axial_selectors_verified=True, all_actual_ABA_rank1_factor_cache_guards_verified=True,
        actual_completed_AAA_qualification_CLI=completed_qualification,
        stable_AAA_qualification_identity=stable_qualification_identity(api),
        build_admission=build_binding(api)[1], actual_build_terminal_evidence=api["actual_build_terminal_evidence"],
        actual_build_terminal_validation=api["actual_build_terminal_validation"], build_terminal_chain=api["build_terminal_chain"],
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=api["resource_scope_contract"],
        actual_ABA_execution_declaration=pin(ABA_ENTRY / "declaration.json"), actual_ABA_handoff=pin(ABA_ENTRY / "RUN/handoff.json"),
        sampling=SAMPLING, original_staging=pin(STAGED / "declaration.json"), native_loader=loader,
        native_argv=[str(OPENMC), "-s", "1"], native_wall_seconds=64800, additional_direct_native_rss_cap_mib=2048,
        original_native_RSS_limit_existed=False, native_RSS_supervision_is_new=True,
        prepare_wall_seconds=PREPARE_WALL, analysis_wall_seconds=ANALYSIS_WALL, saved_export_wall_seconds=60,
        host_rss_cap_mib=512, threads=1, numeric_children_at_once=1, retries=0,
        artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR, resource_roots=roots, resources_before=snap,
        storage_reservation=dict(method="ceil(1.5*measured_old_complete_AAA_sample)+1GiB",
            measured_old_AAA_regular_bytes=sample_bytes, forecast_native_result=pin(CE / "AAA/native_result.json"),
            forecast_only=True, old_AAA_sample_used_as_ABA=False, growth_factor=1.5,
            log_export_analysis_margin_bytes=HOST_MARGIN, reserved_bytes=reserve),
        analysis_environment=pin(SOURCE / "analysis_environment.json"), source_equivalence=pin(SOURCE / "source_equivalence.json"),
        live_guard_provenance=pin(SOURCE / "live_guard_provenance.json"), original_eight_checks=list(GATES),
        physical_inputs_changed=False, scientific_acceptance_thresholds_changed=False,
        transport_launched=False, independent_ABA_accuracy_qualified=False)
    d["actual_external_terminal_contract"] = dict(schema="AXMAT_RANK1_FACTOR_CACHE_ABA_REFERENCE_ACTUAL_TERMINAL_RETURN_V1",
        root=str(TERMINAL), actual_root_record_producer_required=True, no_record_producer_in_this_factory=True,
        prepare_record=str(TERMINAL / "prepare_terminal_return.json"), native_record=str(TERMINAL / "native_terminal_return.json"),
        prepare_full_stdout=str(TERMINAL / "prepare_stdout.json"), native_full_stdout=str(TERMINAL / "native_stdout.json"),
        analysis_schema="AXMAT_RANK1_FACTOR_CACHE_ABA_ANALYSIS_ACTUAL_TERMINAL_RETURN_V1",
        analysis_record=str(TERMINAL / "analysis_terminal_return.json"), analysis_full_stdout=str(TERMINAL / "analysis_stdout.json"),
        analysis_tail_fields=list(ANALYSIS_TAIL_FIELDS), analysis_qualification_is_read_only_admission_only=True,
        sealed_OUT_is_never_modified_by_qualification=True, host_archive_resource_roots=list(ARCHIVE_ROOTS),
        required_before_next_phase=True)
    write_new(SOURCE / "declaration.json", d)
    write_new(SOURCE / "source_inventory.json", dict(files=regular_files(SOURCE)))
    if combined_archive_bytes() >= HOST_MARGIN:
        raise ValueError("declared SOURCE plus OUT exceeds original 1GiB host archive margin")
    storage(c, roots, reserve)
    return dict(classification=d["classification"], declaration=pin(SOURCE / "declaration.json"), output=str(OUT))


def admission(expected, prepared=False):
    d = read(require(SOURCE / "declaration.json", expected))
    if (d["schema"] != "AXMAT_RANK1_FACTOR_CACHE_ABA_INDEPENDENT_NATIVE_REFERENCE_DECLARATION_V1" or d["case"] != "ABA"
            or d["actual_factory"] != pin(Path(__file__).resolve()) or d["sampling"] != SAMPLING
            or d["native_argv"] != [str(OPENMC), "-s", "1"] or d["native_wall_seconds"] != NATIVE_WALL
            or d["additional_direct_native_rss_cap_mib"] != NATIVE_RSS
            or d["original_native_RSS_limit_existed"] is not False or d["native_RSS_supervision_is_new"] is not True
            or d["prepare_wall_seconds"] != PREPARE_WALL or d["analysis_wall_seconds"] != ANALYSIS_WALL
            or d["saved_export_wall_seconds"] != 60 or d["host_rss_cap_mib"] != HOST_RSS
            or d["threads"] != 1 or d["numeric_children_at_once"] != 1 or d["retries"] != 0
            or d["artifact_budget_bytes"] != HISTORY_CAP or d["min_free_bytes"] != FREE_FLOOR
            or d["original_eight_checks"] != list(GATES)
            or d["all_actual_ABA_axial_selectors_verified"] is not True
            or d["all_actual_ABA_rank1_factor_cache_guards_verified"] is not True
            or d["actual_external_terminal_contract"]["analysis_schema"] != "AXMAT_RANK1_FACTOR_CACHE_ABA_ANALYSIS_ACTUAL_TERMINAL_RETURN_V1"
            or d["actual_external_terminal_contract"]["analysis_record"] != str(TERMINAL / "analysis_terminal_return.json")
            or d["actual_external_terminal_contract"]["analysis_full_stdout"] != str(TERMINAL / "analysis_stdout.json")
            or d["actual_external_terminal_contract"]["analysis_tail_fields"] != list(ANALYSIS_TAIL_FIELDS)
            or d["actual_external_terminal_contract"]["host_archive_resource_roots"] != list(ARCHIVE_ROOTS)
            or d["actual_external_terminal_contract"]["sealed_OUT_is_never_modified_by_qualification"] is not True
            or d["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or d["resource_scope_contract"] != load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "rank1_factor_cache_ABA_actual_build").resource_scope_contract()
            or d["physical_inputs_changed"] is not False or d["scientific_acceptance_thresholds_changed"] is not False):
        raise ValueError("frozen native ABA reference protocol differs")
    inventory = read(require(SOURCE / "source_inventory.json"))["files"]
    if set(regular_files(SOURCE)) != set(inventory) | {"source_inventory.json"}:
        raise ValueError("declared native-reference source namespace changed")
    verify({str(SOURCE / name): sha for name, sha in inventory.items()})
    verify(d["files"])
    actual = actual_completed_aba(d["actual_parameters"])
    if actual[6] != d["actual_AAA_qualification_API_return"]:
        raise ValueError("actual repeated AAA API qualification differs")
    completed_api_proof(d["actual_completed_AAA_qualification_CLI"], actual[6], d["actual_parameters"], actual[7])
    if (stable_qualification_identity(actual[6]) != d["stable_AAA_qualification_identity"]
            or build_binding(actual[6])[1] != d["build_admission"]
            or actual[6]["build_terminal_chain"] != d["build_terminal_chain"]):
        raise ValueError("actual complete stable qualification/build lineage changed")
    actual[1].environment(read(d["analysis_environment"]["path"]))
    verify(d["native_loader"]["files"])
    for name, item in d["native_loader"]["library_aliases"].items():
        if str(Path(name).resolve(strict=True)) != item["canonical"]:
            raise ValueError("native library alias resolution changed")
        require(item["canonical"], item["sha256"])
    actual_loader = {key: value for key, value in os.environ.items() if key.startswith(("DYLD_", "LD_"))
                    or key in ("PYTHONPATH", "OPENBLAS_CORETYPE", "OPENMC_CROSS_SECTIONS")}
    if actual_loader != d["native_loader"]["environment"] or any(os.environ.get(key) != "1" for key in THREADS):
        raise ValueError("actual frozen native loader or thread environment changed")
    if prepared:
        p = read(require(OUT / "prepared.json"))
        if p["classification"] != "PREPARED_INDEPENDENT_ABA_REFERENCE_NO_NATIVE_TRANSPORT" or p["declaration"] != pin(SOURCE / "declaration.json"):
            raise ValueError("actual exclusive reference preparation differs")
        verify({str(OUT / name): sha for name, sha in p["files"].items()})
        for name, item in p["source_links"].items():
            path = OUT / "fine" / name
            if not path.is_symlink() or path.resolve(strict=True) != Path(item["path"]):
                raise ValueError("actual saved-state input link differs")
            require(item["path"], item["sha256"])
    return d, actual


def runner(d, actual, phase, cap):
    if not 0 < cap <= 120:
        raise ValueError("host phase has no positive remaining whole-phase 120-second budget")
    full = load(require(FULL_FACTORY, FULL_SHA), "rank1_factor_cache_ABA_reference_ownRSS")
    actual[1].live_guard_provenance(full, actual[0], actual[3])
    resources, _, _ = storage(actual[0], d["resource_roots"])
    obj = full.OwnRSSSerialExecutor(OUT, cap, phase, resources)
    obj.env = dict(os.environ, **{key: "1" for key in THREADS}, PYTHONDONTWRITEBYTECODE="1")
    return obj


def watch_phase(phase, commands):
    stages = read(require(OUT / phase / "stages.json"))["stages"]
    if len(stages) != len(commands) or any(row["status"] != "PASS" for row in stages):
        raise ValueError("every actual bounded reference host stage must pass")
    for row, command in zip(stages, commands, strict=True):
        if row["command"] != command:
            raise ValueError("actual bounded host command differs")
        log = OUT / (row["label"] + ".log")
        require(log, row["log_sha256"])
        w = read(require(log.with_suffix(".watchdog.json")))
        if (w["command"] != command or w["returncode"] != 0 or w["limit_failure"] is not None
                or w["rss_cap_mib"] != 512 or not 0 <= w["sampled_peak_rss_mib"] < 512
                or not 0 < w["wall_cap_seconds"] <= row["wall_cap_seconds"] <= 120
                or not 0 <= w["elapsed_seconds"] < w["wall_cap_seconds"]
                or w["own_child_only"] is not True or w["liveness_group_cleanup"] is not True):
            raise ValueError("actual bounded host resource supervision failed")
    return pin(OUT / phase / "stages.json")


def worker_admission(expected, label):
    d, actual = admission(expected)
    claim = read(require(OUT / "prepare_claim.json"))
    rows = read(require(OUT / "prepare/stages.json"))["stages"]
    if (claim["parent_pid"] != os.getppid() or claim["declaration"] != pin(SOURCE / "declaration.json")
            or not rows or rows[-1]["status"] != "RUNNING" or rows[-1]["label"] != label
            or rows[-1]["command"] != [sys.executable, *sys.argv]):
        raise ValueError("only the actual serial preparation child may perform this worker")
    return d, actual


def physical_worker(expected):
    d, actual = worker_admission(expected, "prepare/physical")
    c, ce, entry, info, status, final = actual[:6]
    helper = load(PHYSICAL, "rank1_factor_cache_ABA_original_track_geometry")
    from white_receiver_tracking import verify_white_tracking_copy
    from qualified_snapshot_ingestion import list_handles
    from snapshot_control_preflight import _open_xsm
    definition = read(ART / "axial-material-tools-20261003/input_equivalence.json")
    verify(definition["input_sha256"])
    physical = definition["cases"]["ABA"]
    if (definition["status"] != "PHYSICAL_INPUT_DEFINITION_AND_CE_MAPPING_CHECKED_PENDING_SPOT_AXIAL_RECORDS"
            or physical["composition_by_physical_zone"] != list("ABA") or physical["white_side_surfaces"] != 6
            or physical["axial_end_vacuum_planes"] != [0, 150]):
        raise ValueError("original ABA density/formula/XML-only physical definition required")
    old_info = read(OLD_PROD / "prepared.json")
    spec, old_spec = read(info["case_spec"]["path"]), read(old_info["case_spec"]["path"])
    if (dict(spec["geometry"], cells_per_zone=4) != old_spec["geometry"]
            or any(spec[k] != old_spec[k] for k in ("materials", "cases", "reference", "predeclared_decisions"))):
        raise ValueError("physical/reference definitions changed beyond declared refinement")
    bootstrap = PROD / "ABA/bootstrap"
    track = bootstrap / "initial_axial_track.xsm"
    unmarked = bootstrap / "initial_axial_track_unmarked.xsm"
    baseline = PROD / "AAA/bootstrap/initial_axial_track_unmarked.xsm"
    marker = verify_white_tracking_copy(unmarked, track)
    geometry = helper.track_geometry(track, OLD_PROD / "AAA/bootstrap/initial_axial_track.xsm")
    identities = {}
    with _open_xsm(unmarked) as new, _open_xsm(baseline) as old:
        for name in TRACK_RECORDS:
            value = helper.scalar(new, new.root, name)
            if value != helper.scalar(old, old.root, name):
                raise ValueError("new fine ABA vs same-study fine AAA geometric words differ: " + name)
            identities[name] = dict(length_words=value[0][0], type=value[0][1], sha256=hashlib.sha256(value[1]).hexdigest())
    checked = ("ISOTOPERNAME", "ISOTOPESMIX", "ISOTOPESDENS", "ISOTOPESTEMP",
               "ISOTOPESUSED", "ISOTOPESVOL", "MIXTURESVOL", "ENERGY")
    radial = ("MATCOD", "KEYFLX", "VOLUME", "NZON$MCCG", "V$MCCG", "ZMU$MCCG", "WZMU$MCCG", "XMU$MCCG")
    archive = PROD / "archives/aba_snapshots.xsm"
    if (bootstrap / "case_snapshots.xsm").resolve(strict=True) != archive:
        raise ValueError("actual ABA bootstrap did not consume its declared A/B/A archive")
    records = []
    with _open_xsm(archive) as new:
        for obj, names in (("MICROLIB2", checked), ("TRACK", radial)):
            handles = list_handles(new, new.root, obj, 3)
            if len(handles) != 3 or any(handle[1:] != (-1, 0) for handle in handles):
                raise ValueError("all A/B/A packed objects must be real directories")
            for slot, (handle, composition) in enumerate(zip(handles, "ABA", strict=True), 1):
                original = ART / "axial-material-inputs-20261003" / composition / ("snapshot_" + composition + ".xsm")
                with _open_xsm(original) as old:
                    new_dir, old_dir = new.directory(handle[0]), old.object(obj)
                    for name in names:
                        value = helper.scalar(new, new_dir, name)
                        if value != helper.scalar(old, old_dir, name):
                            raise ValueError(f"actual packed ABA input changed: {obj}/{slot}/{name}")
                        records.append(dict(object=obj, slot=slot, composition=composition, record=name,
                            original=pin(original), length_words=value[0][0], type=value[0][1],
                            sha256=hashlib.sha256(value[1]).hexdigest()))
    if len(records) != 48:
        raise ValueError("complete 48-record independent A/B/A audit required")
    contract = read(OUT / "ABA/reference_contract.json")
    with (OUT / "fine/observables.regions.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    keys = {(int(row["radial_region"]), int(row["axial_cell"])): row for row in rows}
    if len(rows) != 384 or len(keys) != 384 or set(keys) != {(r, c) for r in range(1, 9) for c in range(1, 49)}:
        raise ValueError("complete 384 native fine-field physical mapping required")
    bins = []
    for row in contract["region_layer_bins"]:
        region, cell = row["region"], row["production_axial_cell"]
        if (row["composition"] != "ABA"[(cell-1)//4] or row["physical_zone"] != (cell-1)//4+1
                or row["z_low_cm"] != 12.5*(cell-1) or row["z_high_cm"] != 12.5*cell):
            raise ValueError("original independent ABA observation-bin composition/edges differ")
        volume = math.fsum(float(keys[region, i]["volume_cm3"]) for i in range(4*(cell-1)+1, 4*cell+1))
        error = abs(volume-row["volume_cm3"])/row["volume_cm3"]
        if not math.isfinite(error) or error > 5e-6:
            raise ValueError("original 5e-6 physical volume gate failed")
        bins.append(dict(region=region, original_cell=cell, composition=row["composition"], volume=volume, relative_error=error))
    if (len(bins) != 96 or {(b["region"], b["original_cell"]) for b in bins} != {(r, c) for r in range(1, 9) for c in range(1, 13)}
            or [row["z_cm"] for row in contract["plane_bins"]] != [12.5*i for i in range(13)]):
        raise ValueError("all original 96 bins and 13 planes required")
    paths = [PHYSICAL, Path(__file__).resolve(), PROD / "prepared.json", PROD / "ABA/run_status.json", final / "result.json",
        track, unmarked, baseline, archive, OUT / "fine/export_receipt.json", OUT / "fine/observables.regions.csv",
        OUT / "ABA/reference_contract.json", ART / "axial-material-tools-20261003/input_equivalence.json"]
    value = dict(schema_version=1, case="ABA", status="PASS", implementation=pin(Path(__file__).resolve()),
        experiment_id=info["experiment_id"], case_spec_sha256=info["case_spec"]["sha256"],
        production_prepared=d["production_prepared"], ABA_status=d["ABA_status"], actual_archives=pin(archive),
        actual_axial_track=pin(track), actual_track_record_identity=identities, exact_initial_ABA_physical_records=48,
        actual_physical_records=records, conditional_marker_review=marker, refined_geometry_review=geometry,
        original_observation_bin_count=96, original_observation_plane_count=13, actual_bin_volume_checks=bins,
        original_volume_tolerance=5e-6, CE_inputs={name: pin(OUT / "ABA" / name) for name in INPUTS},
        input_identities={str(path): digest(path) for path in paths}, original_density_formula_and_XML_audit_reused_by_identity=True,
        old_AAA_physical_PASS_claimed_as_ABA=False, reference_sample_reused_by_identity=False,
        independent_ABA_accuracy_qualified=False, new_transport_launched=False)
    write_new(OUT / "fine/input_equivalence_ABA.json", value)
    return dict(status="PASS", case="ABA", report=pin(OUT / "fine/input_equivalence_ABA.json"))


def project_worker(expected):
    d, actual = worker_admission(expected, "prepare/project")
    rs = load(OUT / "runtime/reference_statistics.py", "reference_statistics")
    cb = load(OUT / "runtime/compare_balance_symmetry.py", "rank1_factor_cache_ABA_current_checker")
    view_spec, native_spec = OUT / "observation_case_spec.json", Path(actual[3]["case_spec"]["path"])
    stat, view, fine = rs.predeclared_rules(view_spec), cb.predeclared_rules(view_spec), cb.predeclared_rules(native_spec)
    for value, name in ((stat, "statistical_rules.json"), (view, "balance_symmetry_rules.json")):
        old = read(CE / name)
        if {k: v for k, v in value.items() if k != "case_spec_sha256"} != {k: v for k, v in old.items() if k != "case_spec_sha256"}:
            raise ValueError("original independent scientific rules changed")
        write_new(OUT / name, value)
    if (fine["axial_cells"] != 48 or view["axial_cells"] != 12
            or {k: v for k, v in fine.items() if k not in ("axial_cells", "case_spec_sha256")}
               != {k: v for k, v in view.items() if k not in ("axial_cells", "case_spec_sha256")}):
        raise ValueError("fine rules differ beyond declared layer count")
    write_new(OUT / "fine_balance_symmetry_rules.json", fine)
    projection = load(OUT / "runtime/project_refined_observables.py", "rank1_factor_cache_ABA_projection").project(
        OUT / "fine", OUT / "observation", cb, fine)
    if (len(projection["mapping"]) != 96 or len(projection["face_map"]) != 13
            or projection["local_or_binwise_normalization"] is not False):
        raise ValueError("complete original-bin conservative projection required")
    physical = read(OUT / "fine/input_equivalence_ABA.json")
    physical["refined_observation_projection"] = pin(OUT / "observation/projection_receipt.json")
    physical["input_identities"].update({str(path): digest(path) for path in (OUT / "fine/input_equivalence_ABA.json",
        OUT / "observation/projection_receipt.json", OUT / "observation_case_spec.json")})
    write_new(OUT / "input_equivalence_ABA.json", physical)
    write_new(OUT / "complete_fine_production_checks.json", projection["original_checks_on_all_fine_entries"])
    write_new(OUT / "production_checks.json", projection["original_checks_on_observation_view"])
    return dict(status="PASS", projection=pin(OUT / "observation/projection_receipt.json"))


def prepare(expected):
    started = time.monotonic()
    d, actual = admission(expected)
    absent(OUT)
    resources, before, roots = storage(actual[0], d["resource_roots"], d["storage_reservation"]["reserved_bytes"])
    OUT.mkdir()
    for name in ("runtime", "fine", "ABA", "prepare", "analysis"):
        (OUT / name).mkdir()
    write_new(OUT / "prepare_claim.json", dict(parent_pid=os.getpid(), declaration=pin(SOURCE / "declaration.json"),
        started_unix=time.time(), retries=0, native_transport_started=False))
    result = dict(classification="PREPARATION_FAILED_NO_RETRY", error=None, native_transport_started=False)
    try:
        for path in (SOURCE / "runtime").iterdir():
            shutil.copy2(path, OUT / "runtime" / path.name)
        for name in ("declaration.json", "source_equivalence.json", "analysis_environment.json", "observation_case_spec.json"):
            shutil.copy2(SOURCE / name, OUT / name)
        for name in INPUTS[:4]:
            shutil.copy2(STAGED / name, OUT / "ABA" / name)
            require(OUT / "ABA" / name, digest(STAGED / name))
        contract = read(STAGED / "reference_contract.json")
        old = copy.deepcopy(contract)
        contract["sampling_addendum"] = str(SOURCE / "declaration.json")
        restored = copy.deepcopy(contract)
        restored["sampling_addendum"] = old["sampling_addendum"]
        if restored != old:
            raise ValueError("ABA source contract changed outside actual sampling declaration binding")
        write_new(OUT / "ABA/reference_contract.json", contract)
        final = actual[5]
        links = {"track.xsm": PROD / "ABA/bootstrap/initial_axial_track.xsm",
                 "axial.xsm": final / "closed_axial.xsm", "macro.xsm": PROD / "ABA/bootstrap/initial_axial_macrolib.xsm"}
        for name, path in links.items():
            (OUT / "fine" / name).symlink_to(path)
        commands = [[str(EXPORTER), "track.xsm", "axial.xsm", "macro.xsm", "observables"],
            [str(PYTHON), str(Path(__file__).resolve()), "physical-worker", "--sha256", expected],
            [str(PYTHON), str(Path(__file__).resolve()), "project-worker", "--sha256", expected]]
        host = runner(d, actual, "prepare", PREPARE_WALL-(time.monotonic()-started))
        host.execute(OUT / "fine", "export", commands[0], 60)
        if not any(line.startswith("AXMAT-OBSERVABLES-COMPLETE k64=") for line in (OUT / "fine/export.log").read_text().splitlines()):
            raise ValueError("actual byte-identical native saved-state export did not finish")
        source_inputs = {str(path): digest(path) for path in links.values()}
        write_new(OUT / "fine/export_protocol.json", dict(production_prepared=d["production_prepared"], ABA_status=d["ABA_status"],
            final_stage_seal=d["final_stage_seal"], exporter=pin(EXPORTER), exporter_source=pin(EXPORT_SOURCE),
            source_inputs=source_inputs, wall_seconds=60, retries=0, threads=1, native_arithmetic_unchanged=True))
        write_new(OUT / "fine/export_receipt.json", dict(classification="SAVED_MET_REAL64_ABA_OBSERVABLES_EXPORTED",
            protocol=pin(OUT / "fine/export_protocol.json"), outputs={"observables."+suffix: digest(OUT / "fine" / ("observables."+suffix))
                for suffix in ("regions.csv", "faces.csv", "summary.txt")}, inputs_unchanged=True,
            implementation_unchanged=True, independent_ABA_accuracy_qualified=False))
        host.execute(OUT / "prepare", "physical", commands[1], 120)
        host.execute(OUT / "prepare", "project", commands[2], 120)
        stage_pin = watch_phase("prepare", commands)
        fields = regular_files(OUT)
        # Native manifest pins complete prepared physical fields before any
        # transport.  Future mutable native outputs are deliberately absent.
        files = dict(d["files"])
        files.update({str(OUT / name): sha for name, sha in fields.items()})
        execution = dict(schema="AXMAT_RANK1_FACTOR_CACHE_ABA_NATIVE_EXECUTION_V1", case="ABA", actual_factory=d["actual_factory"],
            declaration=pin(SOURCE / "declaration.json"), executable=str(OPENMC), files=files,
            case_spec=actual[3]["case_spec"], wall_seconds=NATIVE_WALL, native_rss_cap_mib=NATIVE_RSS,
            threads=1, retries=0, numeric_children_at_once=1, artifact_root=str(ART), resource_roots=roots,
            artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR,
            resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=d["resource_scope_contract"],
            watchdog_source=str(PROD / "runtime/run_bounded_dragon.py"), native_loader=d["native_loader"],
            resource_addendum=str(OUT / "resource_addendum.json"))
        write_new(OUT / "resource_addendum.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_ABA_NATIVE_RESOURCE_ADDENDUM_V1",
            native_wall_seconds=NATIVE_WALL, native_rss_cap_mib=NATIVE_RSS, original_native_RSS_limit_existed=False,
            native_RSS_supervision_is_new=True, artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR,
            resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=d["resource_scope_contract"],
            resource_roots=roots, storage_reservation=d["storage_reservation"], threads=1, numeric_children_at_once=1, retries=0))
        execution["files"][str(OUT / "resource_addendum.json")] = digest(OUT / "resource_addendum.json")
        write_new(OUT / "ABA/execution.json", execution)
        write_new(OUT / "ABA/measurement_admission.json", dict(classification="FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE", case="ABA",
            prepared=d["production_prepared"], ABA_status=d["ABA_status"], final_seal=d["final_stage_seal"],
            AAA_qualification=pin(FORMAL), actual_external_terminal_evidence=d["actual_AAA_qualification_API_return"]["actual_external_terminal_evidence"],
            input_equivalence=pin(OUT / "input_equivalence_ABA.json"), production_checks=pin(OUT / "production_checks.json"),
            complete_fine_checks=pin(OUT / "complete_fine_production_checks.json"), observation_projection=pin(OUT / "observation/projection_receipt.json"),
            CE_manifest=pin(OUT / "ABA/execution.json"), implementation=pin(Path(__file__).resolve()), independent_ABA_accuracy_qualified=False))
        result.update(classification="PREPARED_INDEPENDENT_ABA_REFERENCE_NO_NATIVE_TRANSPORT", execution=pin(OUT / "ABA/execution.json"),
            actual_saved_prepare_stages=stage_pin, error=None, resources_after=resources.check(), elapsed_seconds=time.monotonic()-started)
        if result["elapsed_seconds"] >= PREPARE_WALL:
            raise ValueError("complete saved-state preparation exceeded its declared total cap")
        write_new(OUT / "prepared.json", dict(classification=result["classification"], declaration=pin(SOURCE / "declaration.json"),
            files=regular_files(OUT), source_links={name: pin(path) for name, path in links.items()}, native_transport_started=False))
    except BaseException as error:
        result.update(classification="PREPARATION_FAILED_NO_RETRY", error=repr(error))
        raise
    finally:
        write_new(OUT / "prepare_result.json", result)
    try:
        resources.check()
        archive_bytes = combined_archive_bytes()
        if archive_bytes >= HOST_MARGIN or time.monotonic()-started >= PREPARE_WALL:
            raise ValueError("complete preparation closeout exceeded its 120s/1GiB host margin")
    except BaseException as error:
        write_new(OUT / "prepare_closeout_failure.json", dict(error=repr(error), native_reference_eligible=False))
        raise
    result["actual_prepare_closeout_tail_gate"] = "PASS"
    result["actual_elapsed_through_prepare_closeout_seconds"] = time.monotonic()-started
    result["actual_complete_preparation_archive_bytes"] = archive_bytes
    return result


def validate_physical_outputs(d):
    physical = read(require(OUT / "input_equivalence_ABA.json"))
    verify(physical["input_identities"])
    if (physical["status"] != "PASS" or physical["case"] != "ABA" or physical["production_prepared"] != d["production_prepared"]
            or physical["ABA_status"] != d["ABA_status"] or physical["exact_initial_ABA_physical_records"] != 48
            or len(physical["actual_physical_records"]) != 48 or set(physical["actual_track_record_identity"]) != set(TRACK_RECORDS)
            or physical["old_AAA_physical_PASS_claimed_as_ABA"] is not False):
        raise ValueError("actual independent fine ABA physical identity audit required")
    for name in ("production_checks.json", "complete_fine_production_checks.json"):
        checks = read(require(OUT / name))
        if not checks["checks"] or any(value != "PASS" for value in checks["checks"].values()):
            raise ValueError("all original fine and observation producer checks required")
    projection = read(OUT / "observation/projection_receipt.json")
    if (projection["classification"] != "PASS_COMPLETE_FINE_AND_CONSERVATIVE_ORIGINAL_OBSERVATION_VIEW"
            or len(projection["mapping"]) != 96 or len(projection["face_map"]) != 13
            or projection["local_or_binwise_normalization"] is not False or projection["bins_removed"] is not False):
        raise ValueError("complete fixed conservative projection required")


def native_contract_admission(manifest, expected):
    manifest = require(manifest, expected)
    if manifest != OUT / "ABA/execution.json":
        raise ValueError("only the new declared ABA native execution path is accepted")
    execution = read(manifest)
    d, actual = admission(execution["declaration"]["sha256"], prepared=True)
    run_admission = read(require(OUT / "native_launch_admission.json"))
    if (run_admission["declaration"] != pin(SOURCE / "declaration.json")
            or run_admission["actual_parent_pid"] != os.getpid()
            or run_admission["execution"] != pin(manifest)):
        raise ValueError("only the actual factory run may launch this direct native child")
    external_phase_return(d, "prepare", run_admission["actual_prepare_terminal"]["path"],
                          run_admission["actual_prepare_terminal"]["sha256"])
    absent(OUT / "prepare_closeout_failure.json")
    prep = read(require(OUT / "prepare_result.json"))
    if (prep["classification"] != "PREPARED_INDEPENDENT_ABA_REFERENCE_NO_NATIVE_TRANSPORT"
            or prep["error"] is not None or not 0 <= prep["elapsed_seconds"] < PREPARE_WALL):
        raise ValueError("actual saved-state preparation failed")
    for name in ("run_claim.json", "native_result.json", "openmc.log", "native.watchdog.json"):
        absent(manifest.parent / name)
    if any(manifest.parent.glob("*.h5")):
        raise ValueError("native H5 outputs already exist; no reuse/retry")
    verify(execution["files"])
    if (execution["schema"] != "AXMAT_RANK1_FACTOR_CACHE_ABA_NATIVE_EXECUTION_V1" or execution["case"] != "ABA"
            or execution["actual_factory"] != pin(Path(__file__).resolve()) or execution["executable"] != str(OPENMC)
            or execution["case_spec"] != actual[3]["case_spec"] or execution["wall_seconds"] != NATIVE_WALL
            or execution["native_rss_cap_mib"] != NATIVE_RSS or execution["native_loader"] != d["native_loader"]
            or execution["threads"] != 1 or execution["numeric_children_at_once"] != 1 or execution["retries"] != 0
            or execution["artifact_budget_bytes"] != HISTORY_CAP or execution["min_free_bytes"] != FREE_FLOOR):
        raise ValueError("actual native reference resource/source contract differs")
    if (execution["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or execution["resource_scope_contract"] != d["resource_scope_contract"]):
        raise ValueError("actual native input must retain the original axial-family resource contract")
    validate_physical_outputs(d)
    measure = read(OUT / "ABA/measurement_admission.json")
    if (measure["classification"] != "FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE" or measure["case"] != "ABA"
            or measure["CE_manifest"] != pin(manifest) or measure["prepared"] != d["production_prepared"]
            or measure["ABA_status"] != d["ABA_status"] or measure["AAA_qualification"] != pin(FORMAL)):
        raise ValueError("actual ABA measurement admission differs")
    for key in ("prepared", "ABA_status", "final_seal", "AAA_qualification", "actual_external_terminal_evidence", "input_equivalence",
                "production_checks", "complete_fine_checks", "observation_projection", "implementation", "CE_manifest"):
        require(measure[key]["path"], measure[key]["sha256"])
    resources, before, roots = storage(actual[0], execution["resource_roots"], d["storage_reservation"]["reserved_bytes"])
    if not set(execution["resource_roots"]).issubset(roots):
        raise ValueError("original declared extras must remain in the actual dynamic axial-family scope")
    return execution, manifest.parent, resources, before


def complete_native(expected):
    d, actual = admission(expected, prepared=True)
    folder = OUT / "ABA"
    manifest = read(folder / "execution.json")
    verify(manifest["files"])
    raw = read(require(folder / "native_result.json"))
    claim = read(require(folder / "run_claim.json"))
    watch = read(require(folder / "native.watchdog.json", raw["watchdog_sha256"]))
    if (raw["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS" or raw["returncode"] != 0 or raw["error"] is not None
            or raw["command"] != d["native_argv"] or claim["command"] != d["native_argv"]
            or claim["manifest_sha256"] != digest(folder / "execution.json")
            or raw["direct_native_PID"] is not True or watch["direct_native_PID"] is not True
            or watch["native_pid"] != raw["native_pid"] or watch["command"] != d["native_argv"]
            or watch["returncode"] != 0 or watch["limit_failure"] is not None
            or watch["wall_cap_seconds"] != NATIVE_WALL or watch["native_rss_cap_mib"] != NATIVE_RSS
            or not 0 <= watch["elapsed_seconds"] < NATIVE_WALL or not 0 <= raw["elapsed_seconds"] < NATIVE_WALL
            or not 0 <= watch["sampled_peak_native_rss_mib"] < NATIVE_RSS or watch["native_rss_samples"] <= 0
            or watch["liveness_group_cleanup"] is not True or watch["native_loader"] != d["native_loader"]):
        raise ValueError("actual direct native lifecycle did not complete within its declared wall/RSS limits")
    require(folder / "openmc.log", raw["log_sha256"])
    names = {f"statepoint.{b:04d}.h5" for b in range(101, 2101)}
    if set(raw["outputs"]) != names | {"summary.h5"} or {p.name for p in folder.glob("*.h5")} != set(raw["outputs"]):
        raise ValueError("complete new ABA 2000 statepoints plus summary required, without foreign H5")
    verify({str(folder / name): sha for name, sha in raw["outputs"].items()})
    if raw["output_sizes"] != {name: (folder / name).stat().st_size for name in raw["outputs"]}:
        raise ValueError("actual native field inventories changed")
    log = (folder / "openmc.log").read_text()
    if (log.count("Creating state point statepoint.2100.h5") != 1 or "TIMING STATISTICS" not in log
            or "RESULTS" not in log or "Combined k-effective" not in log):
        raise ValueError("actual native final statepoint/end/results markers required")
    storage(actual[0], d["resource_roots"])
    return d, actual, raw


def external_phase_return(d, phase, evidence, evidence_sha):
    """Consume root's actual terminal exit and retained whole stdout; never produce one."""
    if phase not in ("prepare", "native"):
        raise ValueError("analysis has its own complete sealed-result terminal consumer")
    record_path = TERMINAL / (phase + "_terminal_return.json")
    stdout_path = TERMINAL / (phase + "_stdout.json")
    if Path(evidence) != record_path:
        raise ValueError("actual phase terminal receipt must use its fixed independent path")
    record = strict_json(require(record_path, evidence_sha))
    command_action = "run" if phase == "native" else "prepare"
    command = [str(PYTHON), str(Path(__file__).resolve()), command_action, "--sha256", digest(SOURCE / "declaration.json")]
    if phase == "native":
        launch = read(require(OUT / "native_launch_admission.json"))
        item = launch["actual_prepare_terminal"]
        command += ["--prepare-terminal-evidence", item["path"], "--prepare-terminal-evidence-sha256", item["sha256"]]
    if (record["schema"] != "AXMAT_RANK1_FACTOR_CACHE_ABA_REFERENCE_ACTUAL_TERMINAL_RETURN_V1" or record["phase"] != phase
            or record["actual_tool_terminal_return_observed"] is not True
            or record["record_written_after_actual_terminal_return"] is not True or record["record_producer"] != "root"
            or type(record["returncode"]) is not int or record["returncode"] != 0
            or record["command"] != command or record["source"] != d["actual_factory"]
            or record["declaration"] != pin(SOURCE / "declaration.json") or record["full_stdout"]["path"] != str(stdout_path)):
        raise ValueError("actual prior phase source/argv/terminal exit proof differs")
    require(stdout_path, record["full_stdout"]["sha256"])
    returned = strict_json(stdout_path)
    base_path = OUT / ("prepare_result.json" if phase == "prepare" else "native_completion.json")
    base = read(require(base_path))
    if any(key not in returned or returned[key] != value for key, value in base.items()):
        raise ValueError("retained complete stdout differs from the actual archived prior result")
    if phase == "prepare":
        if (returned["actual_prepare_closeout_tail_gate"] != "PASS"
                or not 0 <= returned["actual_elapsed_through_prepare_closeout_seconds"] < PREPARE_WALL
                or type(returned["actual_complete_preparation_archive_bytes"]) is not int
                or not 0 <= returned["actual_complete_preparation_archive_bytes"] < HOST_MARGIN):
            raise ValueError("actual complete preparation tail failed")
        tails = ("actual_prepare_closeout_tail_gate", "actual_elapsed_through_prepare_closeout_seconds",
                 "actual_complete_preparation_archive_bytes")
    else:
        if (returned["actual_full_native_closeout_tail_gate"] != "PASS"
                or not 0 <= returned["actual_elapsed_through_native_closeout_seconds"] < NATIVE_WALL
                or returned["resources_after_full_native_closeout"]["artifact_budget_bytes"] != HISTORY_CAP
                or returned["resources_after_full_native_closeout"]["min_free_bytes"] != FREE_FLOOR):
            raise ValueError("actual complete native return/resource tail failed")
        tails = ("actual_full_native_closeout_tail_gate", "actual_elapsed_through_native_closeout_seconds",
                 "resources_after_full_native_closeout")
    if any(record[key] != returned[key] for key in tails) or set(returned) != set(base) | set(tails):
        raise ValueError("actual terminal record must bind exactly every complete stdout tail field")
    return pin(record_path)


def run(expected, prepare_terminal, prepare_terminal_sha):
    d, actual = admission(expected, prepared=True)
    terminal = external_phase_return(d, "prepare", prepare_terminal, prepare_terminal_sha)
    absent(OUT / "native_launch_admission.json")
    validate_physical_outputs(d)
    execution = pin(OUT / "ABA/execution.json")
    storage(actual[0], d["resource_roots"], d["storage_reservation"]["reserved_bytes"])
    write_new(OUT / "native_launch_admission.json", dict(declaration=pin(SOURCE / "declaration.json"), execution=execution,
        actual_prepare_terminal=terminal, actual_parent_pid=os.getpid(), native_transport_started=False,
        actual_AAA_qualification_API_return=actual[6], AAA_qualification=pin(FORMAL), ABA_status=d["ABA_status"]))
    executor = load(OUT / "runtime/ce_execution.py", "rank1_factor_cache_actual_ABA_native_executor")
    result = executor.execute(Path(execution["path"]), execution["sha256"])
    # Native raw archives were already written even if these post-return gates
    # refuse.  No next transport or retry is possible for this claimed folder.
    if result["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS":
        raise ValueError("native ABA reference failed; raw attempt remains preserved")
    _, _, raw = complete_native(expected)
    receipt = dict(classification="COMPLETE_NEW_ABA_NATIVE_REFERENCE_PENDING_ORIGINAL_EIGHT_GATES", case="ABA",
        declaration=pin(SOURCE / "declaration.json"), execution=execution, native_result=pin(OUT / "ABA/native_result.json"),
        native_watchdog=pin(OUT / "ABA/native.watchdog.json"), native_stdout=pin(OUT / "ABA/openmc.log"),
        statepoint_count=2000, raw_outputs=raw["outputs"], actual_direct_native_rss_cap_mib=2048,
        original_native_wall_seconds=64800, independent_ABA_accuracy_qualified=False,
        old_AAA_sample_used_as_ABA=False, retries=0)
    write_new(OUT / "native_completion.json", receipt)
    try:
        _, snapshot, _ = storage(actual[0], d["resource_roots"])
        claim = read(OUT / "ABA/run_claim.json")
        elapsed = time.monotonic()-claim["started_monotonic"]
        if elapsed >= NATIVE_WALL:
            raise ValueError("full actual native return/archive closeout exceeded original 64800s")
    except BaseException as error:
        write_new(OUT / "native_closeout_failure.json", dict(error=repr(error), independent_ABA_reference_eligible=False))
        raise
    receipt["actual_full_native_closeout_tail_gate"] = "PASS"
    receipt["actual_elapsed_through_native_closeout_seconds"] = elapsed
    receipt["resources_after_full_native_closeout"] = snapshot
    return receipt


def scientific_decision(stats, currents, inputs, folder):
    # This block is copied literally from the frozen original collector.
    case_dir = folder
    sha256 = digest
    expected_statepoints = [case_dir / f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)]
    expected_identities = [dict(path=str(path), sha256=sha256(path)) for path in expected_statepoints]
    if (stats.get("statepoint_identities") != expected_identities
            or currents.get("statepoint_identities") != expected_identities):
        raise ValueError("both analyses must bind every original active-batch statepoint")
    import numpy as np
    history = stats.get("source_generation_history", {})
    for label in ("k_generation", "entropy"):
        raw = np.asarray(history.get("raw_" + label, []), dtype=float)
        batched = np.asarray(history.get(label, []), dtype=float)
        if raw.shape != (21000,) or batched.shape != (2100,) or not np.isfinite(raw).all():
            raise ValueError("complete native raw and batched generation histories required")
        if not np.array_equal(raw.reshape(2100,10).mean(axis=1), batched):
            raise ValueError("history aggregation differs from the declared consecutive batches")
    if stats.get("generation_history_aggregation", {}).get("generations_per_batch") != 10:
        raise ValueError("actual ten-generation batch analysis required")
    mapping = {"source_convergence": "source_convergence_screen", "block_stability": "block_stability",
        "statistical_resolution": "statistical_resolution", "keff": "keff", "scalar_flux": "scalar_flux", "nu_fission": "nu_fission"}
    checks = {key: stats["checks"][name] for key, name in mapping.items()}
    checks.update(input_equivalence=inputs["status"], currents_balance_symmetry=currents["status"])
    qualified = (stats["classification"] == "STATISTICAL_COMPARISON_PASS"
                 and stats["status"] == "PASS" and all(value == "PASS" for value in checks.values()))
    return checks, qualified


def scientific_source_proof():
    """Future declaration audit of the literal original eight-gate decision."""
    original = CE / "runtime/assess_qualified_AAA_white_trace_precision.py"
    main = next(n for n in ast.parse(require(original).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "main")
    current = next(n for n in ast.parse(Path(__file__).read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "scientific_decision")
    def segment(body):
        names = [n.targets[0].id if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) else None for n in body]
        return ast.dump(ast.Module(body=body[names.index("expected_statepoints"):names.index("qualified")+1], type_ignores=[]), include_attributes=False)
    if segment(main.body) != segment(current.body):
        raise ValueError("original complete-history and eight-gate decision changed")
    return dict(parent=pin(original), candidate=pin(Path(__file__).resolve()), decision_AST_exact=True,
        original_eight_checks=list(GATES), no_threshold_change=True)


def analyze(expected, native_terminal, native_terminal_sha):
    started = time.monotonic()
    absent(OUT / "native_closeout_failure.json")
    d, actual, native = complete_native(expected)
    terminal = external_phase_return(d, "native", native_terminal, native_terminal_sha)
    require(OUT / "native_completion.json")
    absent(OUT / "analysis_claim.json")
    proof = scientific_source_proof()
    storage(actual[0], d["resource_roots"], HOST_MARGIN)
    write_new(OUT / "analysis_claim.json", dict(parent_pid=os.getpid(), declaration=pin(SOURCE / "declaration.json"),
        native_result=pin(OUT / "ABA/native_result.json"), actual_native_terminal=terminal,
        started_unix=time.time(), retries=0, native_transport_started=False))
    common = ["--case-spec", str(OUT / "observation_case_spec.json"), "--contract", str(OUT / "ABA/reference_contract.json"),
        "--statepoints", str(OUT / "ABA"), "--production-regions", str(OUT / "observation/observables.regions.csv"),
        "--production-summary", str(OUT / "observation/observables.summary.txt")]
    commands = [[str(PYTHON), str(OUT / "runtime/reference_statistics.py"), "analyze", "--rules", str(OUT / "statistical_rules.json"),
         *common, "--output", str(OUT / "ABA/statistics.json")],
        [str(PYTHON), str(OUT / "runtime/compare_balance_symmetry.py"), "compare", "--rules", str(OUT / "balance_symmetry_rules.json"),
         "--statistics-rules", str(OUT / "statistical_rules.json"), *common, "--production-faces", str(OUT / "observation/observables.faces.csv"),
         "--output", str(OUT / "ABA/currents_balance_symmetry.json")]]
    result = dict(classification="ABA_REFERENCE_ANALYSIS_FAILED_NO_RETRY", case="ABA", error=None,
        independent_ABA_accuracy_qualified=False, original_eight_checks={}, native_transport_started=False,
        host_archive_resource_roots=list(ARCHIVE_ROOTS), host_archive_margin_bytes=HOST_MARGIN,
        host_archive_scope="Combined SOURCE plus OUT regular bytes less the exact archived native H5 output bytes",
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=d["resource_scope_contract"],
        final_qualification_requires_actual_external_terminal_admission=True,
        formal_qualification_published=False, pending_receipt_eligible=False)
    try:
        host = runner(d, actual, "analysis", ANALYSIS_WALL-(time.monotonic()-started))
        for label, command in zip(("statistics", "currents"), commands, strict=True):
            host.execute(OUT / "analysis", label, command, ANALYSIS_WALL)
        watch_phase("analysis", commands)
        reports = {}
        for label, path in (("statistics", OUT / "ABA/statistics.json"), ("currents", OUT / "ABA/currents_balance_symmetry.json"),
                            ("inputs", OUT / "input_equivalence_ABA.json")):
            report = read(require(path))
            if report.get("case") != "ABA":
                raise ValueError("each actual reference report must describe new ABA")
            verify(report.get("input_identities", {}))
            for item in report.get("statepoint_identities", []):
                require(item["path"], item["sha256"])
            reports[label] = report
        if reports["statistics"].get("method") != "independent_continuous_energy_openmc":
            raise ValueError("independent native continuous-energy analysis required")
        checks, qualified = scientific_decision(reports["statistics"], reports["currents"], reports["inputs"], OUT / "ABA")
        assessment = dict(schema_version=1, case="ABA", method="independent_continuous_energy_openmc",
            classification="ABA_REFERENCE_QUALIFIED" if qualified else "ABA_REFERENCE_NOT_QUALIFIED",
            experiment_id=actual[3]["experiment_id"], prepared_sha256=d["production_prepared"]["sha256"],
            case_spec_sha256=actual[3]["case_spec"]["sha256"], rank_addendum_sha256=actual[3]["rank_addendum"]["sha256"],
            common_basis_sha256=actual[4]["common_basis_sha256"], aba_run_status_sha256=d["ABA_status"]["sha256"],
            checks=checks, evidence={"statistics": pin(OUT / "ABA/statistics.json"), "input_equivalence": pin(OUT / "input_equivalence_ABA.json"),
                "currents_balance_symmetry": pin(OUT / "ABA/currents_balance_symmetry.json")},
            AAA_qualification=pin(FORMAL), actual_external_AAA_terminal_evidence=d["actual_AAA_qualification_API_return"]["actual_external_terminal_evidence"],
            CE_execution=pin(OUT / "ABA/execution.json"), CE_native_result=pin(OUT / "ABA/native_result.json"),
            implementation=pin(Path(__file__).resolve()), scientific_decision_source_proof=proof,
            independent_ABA_accuracy_qualified=qualified, original_scientific_thresholds_changed=False,
            full_neutron_balance="NOT_ASSESSED: current telescoping is an accounting identity; no independent absorption/source tally.")
        write_new(OUT / "ABA/reference_assessment.json", assessment)
        if qualified:
            write_new(OUT / "ABA/reference_qualification.pending.json", assessment)
        resources, snap, _ = storage(actual[0], d["resource_roots"])
        elapsed = time.monotonic()-started
        if elapsed >= ANALYSIS_WALL:
            raise ValueError("complete original-gate analysis exceeded total 120-second cap")
        result.update(classification="COMPLETE_ABA_ORIGINAL_EIGHT_GATE_ASSESSMENT", independent_ABA_accuracy_qualified=qualified,
            original_eight_checks=checks, assessment=pin(OUT / "ABA/reference_assessment.json"), elapsed_seconds=elapsed,
            resources_after=snap, error=None, pending_receipt_eligible=False)
        write_new(OUT / "analysis_result.json", result)
        write_new(OUT / "seal.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_ABA_NATIVE_REFERENCE_SEAL_V1",
            declaration=pin(SOURCE / "declaration.json"), files=regular_files(OUT), independent_ABA_accuracy_qualified=qualified,
            formal_qualification_published=False, external_actual_terminal_witness_required_for_future_publication=True))
        # Keep the science result pending. This source provides no fake terminal
        # producer and no automatic qualification publication after a seal.
        tail_resources = resources.check()
        tail_bytes = combined_archive_bytes()
        if tail_bytes-sum(native["output_sizes"].values()) >= HOST_MARGIN:
            raise ValueError("complete reference host/archive closeout exceeded its separate 1GiB margin")
        if time.monotonic()-started >= ANALYSIS_WALL:
            raise ValueError("mandatory complete closeout tail exhausted analysis wall cap")
        result["actual_full_closeout_tail_gate"] = "PASS"
        result["actual_elapsed_through_full_closeout_seconds"] = time.monotonic()-started
        result["actual_complete_archive_bytes"] = tail_bytes
        result["resources_after_full_closeout"] = tail_resources
    except BaseException as error:
        if not (OUT / "analysis_result.json").exists():
            result.update(error=repr(error), independent_ABA_accuracy_qualified=False)
            write_new(OUT / "analysis_result.json", result)
        else:
            write_new(OUT / "analysis_closeout_failure.json", dict(error=repr(error), formal_receipt_eligible=False,
                independent_ABA_accuracy_qualified=False))
        raise
    return result


def external_analysis_return(d, expected_seal, result, native, evidence, evidence_sha):
    """Read Root's actual final analysis return; never edit sealed outputs."""
    receipt = TERMINAL / "analysis_terminal_return.json"
    stdout = TERMINAL / "analysis_stdout.json"
    if Path(evidence) != receipt or str(TERMINAL) not in d["resource_roots"]:
        raise ValueError("fixed independent actual analysis terminal receipt required")
    for path in (receipt, stdout):
        cursor = path
        while cursor != cursor.parent:
            if cursor.is_symlink():
                raise ValueError("analysis terminal evidence or ancestor is aliased")
            cursor = cursor.parent
    e = strict_json(require(receipt, evidence_sha))
    claim = read(require(OUT / "analysis_claim.json"))
    prior = claim["actual_native_terminal"]
    command = [str(PYTHON), str(Path(__file__).resolve()), "analyze", "--sha256", digest(SOURCE / "declaration.json"),
        "--native-terminal-evidence", prior["path"], "--native-terminal-evidence-sha256", prior["sha256"]]
    if (e["schema"] != "AXMAT_RANK1_FACTOR_CACHE_ABA_ANALYSIS_ACTUAL_TERMINAL_RETURN_V1"
            or e["phase"] != "analysis" or e["record_producer"] != "root"
            or e["actual_tool_terminal_return_observed"] is not True
            or e["record_written_after_actual_terminal_return"] is not True
            or type(e["returncode"]) is not int or e["returncode"] != 0
            or e["command"] != command or e["source"] != d["actual_factory"]
            or e["declaration"] != pin(SOURCE / "declaration.json")
            or e["reference_seal"] != dict(path=str(OUT / "seal.json"), sha256=expected_seal)
            or e["full_stdout"]["path"] != str(stdout) or e["full_stdout"] != pin(require(stdout, e["full_stdout"]["sha256"]))):
        raise ValueError("actual Root analysis exit-zero/source/argv/declaration/seal chain differs")
    returned = strict_json(stdout)
    tail = {key: returned[key] for key in ANALYSIS_TAIL_FIELDS}
    if returned != dict(result, **tail) or any(e[key] != tail[key] for key in ANALYSIS_TAIL_FIELDS):
        raise ValueError("full actual analysis stdout/four tails differ from the sealed result")
    elapsed = tail["actual_elapsed_through_full_closeout_seconds"]
    actual_bytes = tail["actual_complete_archive_bytes"]
    snapshot = tail["resources_after_full_closeout"]
    if (tail["actual_full_closeout_tail_gate"] != "PASS" or type(elapsed) not in (int, float)
            or not math.isfinite(elapsed) or not result["elapsed_seconds"] <= elapsed < ANALYSIS_WALL
            or type(actual_bytes) is not int or actual_bytes != combined_archive_bytes()
            or not 0 <= actual_bytes-sum(native["output_sizes"].values()) < HOST_MARGIN
            or result["host_archive_resource_roots"] != list(ARCHIVE_ROOTS)
            or result["host_archive_margin_bytes"] != HOST_MARGIN
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != d["resource_scope_contract"]
            or snapshot["artifact_budget_bytes"] != HISTORY_CAP or snapshot["min_free_bytes"] != FREE_FLOOR
            or not set(d["resource_roots"]).issubset(snapshot["declared_resource_roots"])
            or not set(snapshot["declared_resource_roots"]).issubset(snapshot["resource_roots"])
            or type(snapshot["artifact_bytes"]) is not int or not actual_bytes <= snapshot["artifact_bytes"] <= HISTORY_CAP
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < FREE_FLOOR
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float) or not math.isfinite(snapshot["checked_unix"])
            or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete analysis wall/archive/family resource tail failed")
    load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "rank1_factor_cache_ABA_actual_build").validate_history_roots(snapshot["resource_roots"], ART)
    return dict(receipt=pin(receipt), full_stdout=pin(stdout), command=command, **tail)


def qualification_admission(expected_seal, analysis_terminal, analysis_terminal_sha):
    """Only actual complete science plus Root terminal evidence admit ABA accuracy.

    This is a read-only formal admission, not a file publisher. The sealed
    pending receipt is only one scientific component. No output, seal or
    historical terminal record is modified; no transport or statistics/current
    child commands run. The saved complete-history decision is verified again.
    """
    seal = read(require(OUT / "seal.json", expected_seal))
    if (seal["schema"] != "AXMAT_RANK1_FACTOR_CACHE_ABA_NATIVE_REFERENCE_SEAL_V1"
            or seal["independent_ABA_accuracy_qualified"] is not True
            or seal["formal_qualification_published"] is not False
            or seal["external_actual_terminal_witness_required_for_future_publication"] is not True
            or set(regular_files(OUT)) != set(seal["files"]) | {"seal.json"}):
        raise ValueError("complete successful scientific seal namespace is required")
    verify({str(OUT / name): sha for name, sha in seal["files"].items()})
    result = read(require(OUT / "analysis_result.json"))
    if (result["classification"] != "COMPLETE_ABA_ORIGINAL_EIGHT_GATE_ASSESSMENT" or result["error"] is not None
            or result["independent_ABA_accuracy_qualified"] is not True
            or result["native_transport_started"] is not False or result["formal_qualification_published"] is not False
            or result["pending_receipt_eligible"] is not False
            or result["final_qualification_requires_actual_external_terminal_admission"] is not True
            or set(result["original_eight_checks"]) != set(GATES)
            or any(value != "PASS" for value in result["original_eight_checks"].values())
            or not 0 <= result["elapsed_seconds"] < ANALYSIS_WALL):
        raise ValueError("pending or incomplete science cannot be a final ABA qualification")
    for name in ("prepare_closeout_failure.json", "native_closeout_failure.json", "analysis_closeout_failure.json"):
        absent(OUT / name)
    declaration = read(require(OUT / "prepared.json"))["declaration"]
    if declaration != seal["declaration"] or declaration["path"] != str(SOURCE / "declaration.json"):
        raise ValueError("sealed analysis must bind its exact real preparation/declaration")
    d, actual, native = complete_native(declaration["sha256"])
    claim = read(require(OUT / "analysis_claim.json"))
    prior = claim["actual_native_terminal"]
    external_phase_return(d, "native", prior["path"], prior["sha256"])
    validate_physical_outputs(d)
    proof = scientific_source_proof()
    common = ["--case-spec", str(OUT / "observation_case_spec.json"), "--contract", str(OUT / "ABA/reference_contract.json"),
        "--statepoints", str(OUT / "ABA"), "--production-regions", str(OUT / "observation/observables.regions.csv"),
        "--production-summary", str(OUT / "observation/observables.summary.txt")]
    commands = [[str(PYTHON), str(OUT / "runtime/reference_statistics.py"), "analyze", "--rules", str(OUT / "statistical_rules.json"),
        *common, "--output", str(OUT / "ABA/statistics.json")],
        [str(PYTHON), str(OUT / "runtime/compare_balance_symmetry.py"), "compare", "--rules", str(OUT / "balance_symmetry_rules.json"),
        "--statistics-rules", str(OUT / "statistical_rules.json"), *common, "--production-faces", str(OUT / "observation/observables.faces.csv"),
        "--output", str(OUT / "ABA/currents_balance_symmetry.json")]]
    watch_phase("analysis", commands)
    stats, currents, inputs = (read(OUT / "ABA/statistics.json"), read(OUT / "ABA/currents_balance_symmetry.json"), read(OUT / "input_equivalence_ABA.json"))
    for report in (stats, currents, inputs):
        if report["case"] != "ABA":
            raise ValueError("all final independent reports must describe the actual new ABA")
        verify(report.get("input_identities", {}))
    checks, qualified = scientific_decision(stats, currents, inputs, OUT / "ABA")
    assessment = read(require(OUT / "ABA/reference_assessment.json"))
    pending = require(OUT / "ABA/reference_qualification.pending.json")
    if (not qualified or checks != result["original_eight_checks"] or assessment["checks"] != checks
            or assessment["classification"] != "ABA_REFERENCE_QUALIFIED" or assessment["case"] != "ABA"
            or assessment["independent_ABA_accuracy_qualified"] is not True
            or stats["method"] != "independent_continuous_energy_openmc"
            or assessment["method"] != "independent_continuous_energy_openmc"
            or assessment["experiment_id"] != actual[3]["experiment_id"]
            or assessment["prepared_sha256"] != d["production_prepared"]["sha256"]
            or assessment["aba_run_status_sha256"] != d["ABA_status"]["sha256"]
            or assessment["case_spec_sha256"] != actual[3]["case_spec"]["sha256"]
            or assessment["rank_addendum_sha256"] != actual[3]["rank_addendum"]["sha256"]
            or assessment["common_basis_sha256"] != actual[4]["common_basis_sha256"]
            or assessment["AAA_qualification"] != pin(FORMAL)
            or assessment["CE_execution"] != pin(OUT / "ABA/execution.json")
            or assessment["CE_native_result"] != pin(OUT / "ABA/native_result.json")
            or assessment["evidence"] != dict(statistics=pin(OUT / "ABA/statistics.json"),
                input_equivalence=pin(OUT / "input_equivalence_ABA.json"),
                currents_balance_symmetry=pin(OUT / "ABA/currents_balance_symmetry.json"))
            or result["assessment"] != pin(OUT / "ABA/reference_assessment.json")
            or result["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or result["resource_scope_contract"] != d["resource_scope_contract"]
            or assessment["implementation"] != d["actual_factory"] or assessment["scientific_decision_source_proof"] != proof
            or pending.read_bytes() != (OUT / "ABA/reference_assessment.json").read_bytes()):
        raise ValueError("actual original full-history/eight-gate pending scientific component differs")
    terminal = external_analysis_return(d, expected_seal, result, native, analysis_terminal, analysis_terminal_sha)
    storage(actual[0], d["resource_roots"])
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_COMPLETE_ORIGINAL_GATE_ABA_QUALIFICATION_ADMISSION_V1",
        classification="ADMITTED_COMPLETE_ORIGINAL_GATE_ABA_QUALIFICATION", case="ABA",
        independent_ABA_accuracy_qualified=True,
        reference_root=str(OUT), reference_seal=pin(OUT / "seal.json"), declaration=pin(SOURCE / "declaration.json"),
        production_prepared=d["production_prepared"], ABA_status=d["ABA_status"], final_stage_seal=d["final_stage_seal"],
        actual_completed_AAA_qualification_CLI=d["actual_completed_AAA_qualification_CLI"],
        actual_AAA_qualification_API_return=d["actual_AAA_qualification_API_return"],
        all_actual_ABA_axial_selectors_verified=True, all_actual_ABA_rank1_factor_cache_guards_verified=True,
        build_admission=d["build_admission"], build_terminal_chain=d["build_terminal_chain"],
        native_result=pin(OUT / "ABA/native_result.json"), assessment=pin(OUT / "ABA/reference_assessment.json"),
        pending_scientific_component=pin(pending), actual_external_analysis_terminal=terminal,
        all_original_eight_checks=checks, sampling=SAMPLING, resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=d["resource_scope_contract"], host_archive_resource_roots=list(ARCHIVE_ROOTS),
        formal_qualification_admitted_by_read_only_API=True, formal_qualification_file_published=False,
        pending_receipt_eligible=False, sealed_OUT_modified=False, transport_launched_by_this_API=False,
        repeated_statistics_or_current_commands_started=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("declare", "prepare", "run", "analyze", "physical-worker", "project-worker", "admit-qualification"))
    parser.add_argument("--sha256")
    parser.add_argument("--prepared-sha256")
    parser.add_argument("--aba-status-sha256")
    parser.add_argument("--aaa-reference-seal-sha256")
    parser.add_argument("--qualification-sha256")
    parser.add_argument("--terminal-evidence", type=Path)
    parser.add_argument("--terminal-evidence-sha256")
    parser.add_argument("--ce-factory-sha256")
    parser.add_argument("--aba-factory-sha256")
    parser.add_argument("--aba-execution-declaration-sha256")
    parser.add_argument("--prepare-terminal-evidence", type=Path)
    parser.add_argument("--prepare-terminal-evidence-sha256")
    parser.add_argument("--native-terminal-evidence", type=Path)
    parser.add_argument("--native-terminal-evidence-sha256")
    parser.add_argument("--analysis-terminal-evidence", type=Path)
    parser.add_argument("--analysis-terminal-evidence-sha256")
    args = parser.parse_args()
    if args.action == "declare":
        keys = dict(prepared_sha256=args.prepared_sha256, ABA_status_sha256=args.aba_status_sha256,
            AAA_reference_seal_sha256=args.aaa_reference_seal_sha256, qualification_sha256=args.qualification_sha256,
            terminal_evidence=str(args.terminal_evidence) if args.terminal_evidence else None,
            terminal_evidence_sha256=args.terminal_evidence_sha256, ce_factory_sha256=args.ce_factory_sha256,
            aba_factory_sha256=args.aba_factory_sha256, ABA_execution_declaration_sha256=args.aba_execution_declaration_sha256)
        if not all(keys.values()) or any(not re.fullmatch(r"[0-9a-f]{64}", value) for key, value in keys.items() if key != "terminal_evidence"):
            parser.error("declare requires all actual prepared, ABA MET, AAA seal/formal/terminal, source and launch-declaration hashes")
        returned = declare(keys)
    else:
        if not args.sha256 or not re.fullmatch(r"[0-9a-f]{64}", args.sha256):
            parser.error("the actual frozen native-reference declaration --sha256 is required")
        if args.action == "admit-qualification":
            if not args.analysis_terminal_evidence or not args.analysis_terminal_evidence_sha256:
                parser.error("final qualification requires the actual complete analysis exit0/full-stdout four-tail witness")
            returned = qualification_admission(args.sha256, args.analysis_terminal_evidence, args.analysis_terminal_evidence_sha256)
        elif args.action == "run":
            if not args.prepare_terminal_evidence or not args.prepare_terminal_evidence_sha256:
                parser.error("run requires actual prepare exit0/full-stdout terminal evidence and its SHA256")
            returned = run(args.sha256, args.prepare_terminal_evidence, args.prepare_terminal_evidence_sha256)
        elif args.action == "analyze":
            if not args.native_terminal_evidence or not args.native_terminal_evidence_sha256:
                parser.error("analyze requires actual native exit0/full-stdout terminal evidence and its SHA256")
            returned = analyze(args.sha256, args.native_terminal_evidence, args.native_terminal_evidence_sha256)
        else:
            returned = {"prepare": prepare, "physical-worker": physical_worker, "project-worker": project_worker}[args.action](args.sha256)
    print(json.dumps(returned, indent=2, allow_nan=False), flush=True)
