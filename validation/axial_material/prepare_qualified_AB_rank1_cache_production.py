"""One future bounded rank-one factor-cache build; no import-time experiment.

The genuine completed moment-order build is the compulsory predecessor.
The cold AAA timeout is retained failure evidence, never qualification. Only
the SPOT1P64 and FLU2DR64 objects may change; the completed FLU override and
every other production link input remain exact. Root alone records actual
terminal exits. This factory cannot publish its own external exit witness.
"""

import argparse
import ast
import copy
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
import struct
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
SOURCE = ART / "axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007"
OUT = ART / "axial-material-rank1-factor-cache-build-20261007"
TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007"
PARENT = ART / "axial-material-moment-order-build-20261006"
PARENT_SOURCE = ART / "axial-material-qualified-AB-moment-order-build-admission-20261006"
PARENT_TERMINAL = ART / "axial-material-qualified-AB-moment-order-build-terminal-20261006"
PARENT_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_moment_order_production.py"
PARENT_FACTORY_SHA = "fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41"
PARENT_SEAL = "e00c2250fc06133d46ace1326702110861b0bd92bd409b6a2c5478e465b3bcc4"
PARENT_RUNTIME_SHA = "a769c215a5a34f471ce1d744080c457cc4e54998256b73f6d081abfd5c63019e"
PARENT_TERMINAL_SHA = "90d699593344d63857b582e8f25bc439d6510483b8f5ce84a10ebe9e7fb739c2"
ANG = ART / "axial-material-AAA-white-trace-angular-convergence-20261005/build"
KERNEL_SOURCE = ANG / "SPOT1P64.f90"
KERNEL_SOURCE_SHA = "7544212ac8419f9c73688c12339c8779358a24f4065523fbbf891cc4fe1c79e0"
KERNEL_OBJECT = ANG / "SPOT1P64.o"
KERNEL_OBJECT_SHA = "562f30660153711828aca6753fa5512cc74c70c7a770172fcf2c5abf6950ab23"
WHITE_SOURCE = ANG / "axmat_white_trace_model.f90"
WHITE_SOURCE_SHA = "5ff57deb56ffec2ed74fd7efe023e5245432fbee6c42abc7ddba7dd9b7d01adc"
WHITE_OBJECT = ANG / "axmat_white_trace_model.o"
WHITE_OBJECT_SHA = "3a0a2517c086f91c79f770cfb6c44f2c04104510ded5e990c464d18a0375e4e2"
SENDER_SOURCE = ART / "axial-material-source-factor-build-20261006/build/FLU2DR64.f"
SENDER_SOURCE_SHA = "15b0a314886ed224204a53dc77e52fe79114ef00eee81230f80d28eaed4a8316"
SENDER_OBJECT = SENDER_SOURCE.with_suffix(".o")
SENDER_OBJECT_SHA = "46431a2490c23b28a91b49eaf455b28a59ed2c64e10523b2fc3985df8a595458"
PATCH_HELPER = ROOT / "validation/axial_material/rank1_factor_cache_patch.py"
CONTROL_SOURCE = ROOT / "validation/axial_material/rank1_factor_cache_controls.f90"
PATCH_HELPER_SHA = "c309a37bad260ebdf377370689b3295476c31fefde8269257c597666f6f78f3e"
CONTROL_SOURCE_SHA = "377e5b3c8f183763fa2749dcfee6090c553283ae2f58a7d725ab653fc5b2210b"
COLD = ART / "axial-material-production-qualified-AB-moment-order-20261006"
COLD_TERMINAL = ART / "axial-material-qualified-AAA-moment-order-production-terminal-20261006"
COLD_TERMINAL_SHA = "4f7475d0a9056794650cb2647bb343dc722f1802aa07601993035f4daa485201"
COLD_STATUS_SHA = "baffb23ffe1299b22f1e609491df6003c3777ef57291e18185550b4c758ddff9"
COLD_STAGES_SHA = "7fdb1307eacaef4d10d07c0ac2fbf2c47e1f23c34c3f118ab9a5c008997b8d27"
COLD_LOG_SHA = "7cedd8558ae6fdb2e976efb6aee254f61998f93ed89f00745a3df1306843322b"
TOTAL_WALL, STAGE_WALL, RSS_CAP = 1800, 600, 512
ARCHIVE_RESERVE = 2 * 2**30
HISTORY_CAP, FREE_FLOOR = 96 * 2**30, 8 * 2**30
FAMILY = "RANK1_FACTOR_CACHE_BUILD"
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
TERMINAL_SCHEMA = "AXMAT_RANK1_FACTOR_CACHE_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
TAIL_FIELDS = ("actual_tail_check", "actual_elapsed_seconds", "actual_archive_bytes", "actual_resources")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, expected=None):
    path = Path(path)
    if (not path.is_absolute() or path.is_symlink() or not path.is_file()
            or (expected is not None and digest(path) != expected)):
        raise ValueError("missing, aliased or changed rank-one build input: " + str(path))
    return path


def pin(path):
    return dict(path=str(require(path)), sha256=digest(path))


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def absent(path):
    if Path(path).exists() or Path(path).is_symlink():
        raise ValueError("exclusive new build root or claim exists; no overwrite/retry: " + str(path))


def load(path, name):
    path = require(path)
    if name in sys.modules:
        result = sys.modules[name]
        if Path(result.__file__).resolve() != path.resolve():
            raise ValueError("actual imported source identity differs: " + name)
        return result
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    if Path(result.__file__).resolve() != path.resolve():
        raise ValueError("actual module identity differs")
    return result


def parent_factory():
    return load(require(PARENT_FACTORY, PARENT_FACTORY_SHA), "rank1_cache_actual_moment_build")


def helper():
    return parent_factory().helper()


def resource_scope_contract():
    return parent_factory().resource_scope_contract()


def history_roots(declared, artifacts_root):
    return parent_factory().history_roots(declared, artifacts_root)


def validate_history_roots(values, artifacts_root):
    return parent_factory().validate_history_roots(values, artifacts_root)


def DynamicHistoryResources(artifacts_root, roots, min_free_bytes, max_bytes, failure_type=None):
    """Lazy public constructor; return the genuine inherited resource class."""
    return parent_factory().DynamicHistoryResources(
        artifacts_root, roots, min_free_bytes, max_bytes, failure_type)


def resources_for(roots, failure=None):
    return DynamicHistoryResources(ART, roots, FREE_FLOOR, HISTORY_CAP, failure)


def archive_bytes():
    roots = validate_history_roots([str(SOURCE), str(OUT)], ART)
    total, stack = 0, list(roots)
    while stack:
        path = stack.pop()
        try:
            fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                with os.scandir(fd) as entries:
                    for entry in entries:
                        value = entry.stat(follow_symlinks=False)
                        if stat.S_ISDIR(value.st_mode):
                            stack.append(path / entry.name)
                        elif stat.S_ISREG(value.st_mode):
                            total += value.st_size
            finally:
                os.close(fd)
        except FileNotFoundError:
            continue
    validate_history_roots([str(SOURCE), str(OUT)], ART)
    return total


def resource_admission(resources):
    snapshot = resources.check()
    if snapshot["artifact_bytes"] + ARCHIVE_RESERVE >= HISTORY_CAP or snapshot["disk_free_bytes"] - ARCHIVE_RESERVE < FREE_FLOOR:
        raise ValueError("complete axial family plus fresh 2GiB build exceeds original 96GiB/free8GiB")
    return snapshot


def predecessor_admission(seal, terminal, terminal_sha):
    if (seal != PARENT_SEAL or Path(terminal) != PARENT_TERMINAL / "terminal_return.json"
            or terminal_sha != PARENT_TERMINAL_SHA):
        raise ValueError("actual completed moment-order seal and Root terminal descriptor are mandatory")
    result = parent_factory().production_admission(seal, terminal, terminal_sha)
    if (result["schema"] != "AXMAT_MOMENT_ORDER_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or result["corrected_runtime"] != dict(path=str(PARENT / "runtime/Dragon"), sha256=PARENT_RUNTIME_SHA)
            or result["actual_control_rows"] != 112 or result["actual_selector_invocations"] != 224
            or result["actual_source_unit_invocations"] != 192 or result["inherited_native_receiver_calls"] != 14
            or result["full_FLU_entry_execution_proved_by_build"] is not False
            or result["AAA_accuracy_qualified"] is not False or result["ABA_admitted"] is not False
            or result["resource_scope_contract"] != resource_scope_contract()):
        raise ValueError("actual immutable prior build inputs differ; no inherited scientific qualification")
    return result


def cold_failure_admission(terminal_sha):
    if terminal_sha != COLD_TERMINAL_SHA:
        raise ValueError("Root's actual failed cold-run terminal hash is mandatory")
    receipt = read(require(COLD_TERMINAL / "terminal_return.json", terminal_sha))
    for key in ("source", "prepared", "actual_controller", "actual_run_claim", "launch_record", "run_status", "stages", "full_stdout", "full_stderr"):
        require(receipt[key]["path"], receipt[key]["sha256"])
    status = read(require(COLD / "AAA/run_status.json", COLD_STATUS_SHA))
    stages = read(require(COLD / "AAA/stages.json", COLD_STAGES_SHA))["stages"]
    log = require(COLD / "AAA/bootstrap/bootstrap_axial.log", COLD_LOG_SHA)
    if (receipt["schema"] != "AXMAT_MOMENT_ORDER_COLD_AAA_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
            or receipt["record_producer"] != "root" or receipt["actual_tool_terminal_return_observed"] is not True
            or receipt["record_written_after_actual_terminal_return"] is not True
            or type(receipt["returncode"]) is not int or receipt["returncode"] != 1
            or receipt["classification"] != "ACTUAL_FAILED_NO_RETRY_BOOTSTRAP_AXIAL_TIMEOUT"
            or receipt["run_status"] != pin(COLD / "AAA/run_status.json")
            or receipt["stages"] != pin(COLD / "AAA/stages.json")
            or receipt["completed_maps"] != 0 or receipt["passed_stages"] != 6
            or receipt["failed_stage"] != "AAA/bootstrap/bootstrap_axial"
            or receipt["AAA_accuracy_qualified"] is not False or receipt["ABA_admitted"] is not False
            or status["classification"] != "FAILED_NO_RETRY" or status["completed_maps"] != 0
            or len(stages) != 7 or any(row["status"] != "PASS" for row in stages[:-1])
            or stages[-1]["label"] != "AAA/bootstrap/bootstrap_axial" or stages[-1]["status"] != "FAILED"
            or stages[-1]["wall_cap_seconds"] != 4200 or "timed out" not in stages[-1]["error"]
            or status["error"] != receipt["actual_error"] or status["error"] != stages[-1]["error"]
            or (COLD / "AAA/bootstrap/result.json").exists() or list((COLD / "AAA").glob("map*"))):
        raise ValueError("preserved actual cold timeout is not the declared failure-only predecessor")
    return dict(terminal=pin(COLD_TERMINAL / "terminal_return.json"), run_status=pin(COLD / "AAA/run_status.json"),
        stages=pin(COLD / "AAA/stages.json"), terminated_complete_log=pin(log),
        terminal_returncode=1, scientific_success=False, qualified=False,
        incomplete_XSM_used_as_scientific_result=False, raw_terminal_chain={key:receipt[key] for key in (
            "source", "prepared", "actual_controller", "actual_run_claim", "launch_record", "full_stdout", "full_stderr")})


def terminal_contract(python):
    return dict(schema=TERMINAL_SCHEMA, root=str(TERMINAL), receipt=str(TERMINAL / "terminal_return.json"),
        record_producer="root", full_stdout_is_retained=True, actual_tool_exit_zero_required=True,
        record_written_after_actual_terminal_return_required=True, tail_fields=list(TAIL_FIELDS),
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=resource_scope_contract(),
        tail_roots_are_dynamic_union=True, actual_run_command=[python, str(Path(__file__).resolve()),
            "run-build", "--sha256", "__DECLARATION_SHA256__"],
        archive_bytes_scope="Complete SOURCE plus OUT; external terminal root also belongs to complete axial-family history",
        evidence_producer_implemented_by_this_factory=False)


def source_inputs():
    expected = {KERNEL_SOURCE:KERNEL_SOURCE_SHA, KERNEL_OBJECT:KERNEL_OBJECT_SHA,
        WHITE_SOURCE:WHITE_SOURCE_SHA, WHITE_OBJECT:WHITE_OBJECT_SHA,
        SENDER_SOURCE:SENDER_SOURCE_SHA, SENDER_OBJECT:SENDER_OBJECT_SHA}
    for path, wanted in expected.items():
        require(path, wanted)
    old = read(require(PARENT / "declaration.json"))
    link = old["build_commands"][1]
    if (link.count(str(KERNEL_OBJECT)) != 1 or link.count(str(SENDER_OBJECT)) != 1
            or link.count(str(WHITE_OBJECT)) != 1 or link.count(str(PARENT / "build/FLU.o")) != 1
            or link.index(str(WHITE_OBJECT)) >= link.index(str(KERNEL_OBJECT))
            or link.index(str(SENDER_OBJECT)) >= link.index(str(PARENT / "build/FLU.o"))
            or link[-2:] != ["-o", str(PARENT / "runtime/Dragon")]):
        raise ValueError("genuine actual compiled parent override order differs")
    return old, {str(path):wanted for path,wanted in expected.items()}


def cache_observer_contract():
    return dict(prefix="AXMAT-RANK1-CACHE TERMINAL ",
        columns=["builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes", "cap_bytes"],
        cap_bytes=536870912, exact_operator_identity_required=True,
        positive_build_reuse_and_validation_required=True, all_actual_full_logs_required=True)


def patch_admission(helper_sha, controls_sha):
    if helper_sha != PATCH_HELPER_SHA or controls_sha != CONTROL_SOURCE_SHA:
        raise ValueError("both actual independently reviewed new source hashes are mandatory")
    patch = load(require(PATCH_HELPER, helper_sha), "rank1_cache_actual_patch")
    require(CONTROL_SOURCE, controls_sha)
    original_kernel = require(KERNEL_SOURCE, KERNEL_SOURCE_SHA).read_text()
    original_sender = require(SENDER_SOURCE, SENDER_SOURCE_SHA).read_text()
    changed = patch.patch_sources(original_kernel, original_sender)
    if set(changed) != {"kernel", "sender", "reference_kernel", "proof"}:
        raise ValueError("explicit kernel/lifecycle/reference source proof is required")
    contract = patch.control_contract()
    if (contract["schema"] != "AXMAT_RANK1_FACTOR_CACHE_CONTROL_CONTRACT_V1"
            or contract["cache_byte_cap"] != 536870912
            or contract["geometry"] != dict(height_cm=150, axial_cells=48, radial_regions=8,
                total_regions=384, sn=32, scat=3, rank=1)
            or contract["all_energy_groups"] != list(range(1, 371))
            or contract["all_fields_bitwise_required"] != ["flux", "cour", "xnei"]
            or contract["nonunit_Gram_required"] is not True or contract["signed_basis_required"] is not True
            or contract["changing_RHS_required"] is not True or contract["raw_before_numeric_gates"] is not True
            or not contract["positive_command_args"] or not contract["negative_cases"]):
        raise ValueError("complete independently audited rank-one production-shape control contract required")
    # All arithmetic/source-restoration witnesses are declared inputs. Actual
    # numerical equivalence is earned only by raw independent field audits.
    json.dumps(changed["proof"], allow_nan=False)
    json.dumps(contract, allow_nan=False)
    if any(type(changed[key]) is not str for key in ("kernel", "sender", "reference_kernel")):
        raise ValueError("the real complete source strings are required")
    proof = changed["proof"]
    if (proof["original_kernel_sha256"] != KERNEL_SOURCE_SHA or proof["original_sender_sha256"] != SENDER_SOURCE_SHA
            or proof["source_projection_and_all_matrix_RHS_factor_solve_arithmetic_unchanged"] is not True
            or proof["legacy_physical_enable_semantics_preserved"] is not True
            or proof["legacy_dense_and_translation_algorithms_preserved"] is not True
            or proof["temporary_key_element_bytes_included"] is not True
            or proof["cache_element_cap_bytes"] != 536870912 or proof["cache_descriptor_bytes_per_group"] != 4096
            or proof["controls_executed"] is not False or proof["production_transport_executed"] is not False
            or not proof["progress_observer_only"]):
        raise ValueError("the full inverse source proof must explicitly separate unchanged mathematics and bounded observers")
    expected_fixtures = [("production_white_370", 370, 8, 48, 32, 1, True, True),
        ("signed_nonunit", 2, 8, 48, 32, 1, False, True),
        ("lifecycle_reset_1", 2, 8, 48, 32, 1, False, True),
        ("lifecycle_reset_2", 2, 8, 48, 32, 1, False, True),
        ("legacy_physical", 2, 2, 3, 8, 2, False, False),
        ("legacy_dense", 2, 2, 3, 8, 2, False, False),
        ("legacy_translation", 2, 8, 3, 8, 1, False, False)]
    independent_fixtures = [dict(name=name, groups=groups, nrhs=3, nreg2d=nr, nfloor=nh,
        npq=nq, nsct=3, nmode=nm, white=white, rank1=rank1)
        for name, groups, nr, nh, nq, nm, white, rank1 in expected_fixtures]
    if contract["positive_fixtures"] != independent_fixtures or [item["name"] for item in contract["negative_cases"]] != [
            "total", "selfscat", "radial", "basis", "mesh", "du", "weights", "pl", "boundary", "signed_zero",
            "white_on", "white_row", "white_perimeter", "dims"]:
        raise ValueError("the actual fixed complete fixture/negative coverage must be independently declared")
    if contract["cap_negative_cases"] != [dict(name=name, args=["cap-negative", name],
            expected_message="SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.")
            for name in ("cap_reserve", "cap_factor_dimensions")]:
        raise ValueError("both actual pre-allocation and overflow-safe cache-cap rejection controls are mandatory")
    return changed, contract


def archive_forecast(contract, changed):
    """Exact raw binary counts plus explicit bounded nonraw allowance."""
    def input_bytes(fixture, modes=None):
        nr, nh, nq, nl, nm = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct", "nmode")]
        nm = nm if modes is None else modes
        return 96+4*(nh+nh*nr+nh+4+4*nl+nr*nm+nr+2+2+2*nq+nl*nq)+8*(nr*3+1)
    fixture_parts, raw_bytes, manifest_rows = [], 0, 0
    for fixture in contract["positive_fixtures"]:
        nr, nh, nq, nl = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct")]
        calls = fixture["groups"]*fixture["nrhs"]*2
        result_bytes = 96+8*(nr*nh*nl+nr*(nh+1)+nr*nq)
        q_bytes = 8*nr*nh*nl
        total = calls*(result_bytes+q_bytes)+(fixture["groups"]+1)*input_bytes(fixture)
        fixture_parts.append(dict(name=fixture["name"], actual_returned_call_archives=calls,
            complete_binary_bytes=total))
        raw_bytes += total
        manifest_rows += calls+1
    prime = contract["positive_fixtures"][0]
    returned_prime_bytes = 96+8*(8*48*3+8*49+8*32)+8*8*48*3
    negative_parts = []
    for case in contract["negative_cases"]:
        total = returned_prime_bytes+input_bytes(prime)+input_bytes(prime, 2 if case["name"] == "dims" else None)
        total += len((case["expected_message"]+"\n").encode())
        negative_parts.append(dict(name=case["name"], complete_binary_and_actual_message_bytes=total))
        raw_bytes += total
        manifest_rows += 2
    for case in contract["cap_negative_cases"]:
        total = 96+len((case["expected_message"]+"\n").encode())
        negative_parts.append(dict(name=case["name"], complete_binary_and_actual_message_bytes=total))
        raw_bytes += total
        manifest_rows += 1
    raw_bytes += 28*8+104+104+184
    manifest_rows += 2
    complete_source_bytes = sum(len(changed[key].encode()) for key in ("kernel", "sender", "reference_kernel"))
    complete_source_bytes += require(CONTROL_SOURCE).stat().st_size
    nonraw_allowance = 1 * 2**30
    manifest_allowance = manifest_rows*2048
    forecast = raw_bytes+complete_source_bytes+manifest_allowance+nonraw_allowance
    if forecast >= ARCHIVE_RESERVE:
        raise ValueError("exact planned raw controls plus explicit build/metadata allowance exceed the original 2GiB archive")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_COMPLETE_ARCHIVE_FORECAST_V1", complete_scope_roots=[str(SOURCE), str(OUT)],
        exact_control_raw_binary_and_abort_message_bytes=raw_bytes, exact_copied_source_bytes=complete_source_bytes,
        declared_manifest_rows=manifest_rows, manifest_json_allowance_bytes=manifest_allowance,
        nonraw_binary_diff_watch_log_and_metadata_allowance_bytes=nonraw_allowance,
        forecast_complete_bytes=forecast, original_archive_reserve_bytes=ARCHIVE_RESERVE,
        positive_fixtures=fixture_parts, negative_controls=negative_parts,
        actual_complete_archive_cap_remains_mandatory=True, actual_production_transport_outputs_not_in_this_build=True)


def production_cache_shape_forecast(parent, contract):
    """Stored TRACK dimensions inform memory only; the fixture stays synthetic."""
    witness = parent["dispatch_evidence"]
    reviewed = read(require(witness["path"], witness["sha256"]))
    state = reviewed["actual_TRACK_contract"]["state_vector"]
    if len(state) != 40 or [state[index] for index in (0, 3, 5, 6, 7, 14, 15, 26)] != [384, 24, 8, 48, 3, 32, 3, 1]:
        raise ValueError("the actual stored TRACK material-bound and production geometry witness differs")
    fixture = contract["positive_fixtures"][0]
    synthetic = cache_accounting(fixture)
    material_bound = cache_accounting(fixture, nmat=24)
    predicted_peak = material_bound["final_retained_bytes"]+max(material_bound["raw_key_bytes"], material_bound["projected_key_bytes"])
    if predicted_peak >= 536870912:
        raise ValueError("production-shape complete cache memory forecast must fit the declared accounted cap")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_STORED_TRACK_MEMORY_FORECAST_V1", actual_stored_TRACK_review=witness,
        actual_stored_TRACK_state_vector=state, NREG2D=8, NFLOOR=48, total_regional_cells=384, NSNAP=3, NPQ=32, NSCT=3,
        TRACK_material_bound=24, synthetic_controls_NMAT=3, cache_mode_rank=1,
        synthetic_cache_accounting=synthetic, material_bound_cache_accounting=material_bound,
        all370_extra_retained_key_bytes=material_bound["final_retained_bytes"]-synthetic["final_retained_bytes"],
        predicted_peak_with_one_live_temporary_key_bytes=predicted_peak, accounted_cache_cap_bytes=536870912,
        actual_runtime_array_sizes_and_preallocation_guard_still_required=True,
        forecast_is_not_actual_production_RSS_measurement=True, synthetic_materials_are_not_actual_physical_inputs=True)


def stage_commands(d, expected):
    commands = list(d["build_commands"])
    commands.append([str(OUT / "runtime/rank1_factor_cache_controls"), *d["control_contract"]["positive_command_args"]])
    commands.extend([str(OUT / "runtime/rank1_factor_cache_controls"), *case["args"]]
        for case in [*d["control_contract"]["negative_cases"], *d["control_contract"]["cap_negative_cases"]])
    commands.append([d["build_python_executable"], str(Path(__file__).resolve()), "audit-build", "--sha256", expected])
    return commands


def stage_labels(d):
    return [f"build/build_{index:02d}" for index in range(len(d["build_commands"]))] + ["controls/positive/execute"] + [
        "controls/negative_" + case["name"] + "/execute" for case in [*d["control_contract"]["negative_cases"],
        *d["control_contract"]["cap_negative_cases"]]] + ["audit/audit"]


def prepare_build(parent_seal, parent_terminal, parent_terminal_sha, cold_terminal_sha, patch_sha, controls_sha):
    for path in (SOURCE, OUT, TERMINAL):
        absent(path)
    parent = predecessor_admission(parent_seal, parent_terminal, parent_terminal_sha)
    cold = cold_failure_admission(cold_terminal_sha)
    old, originals = source_inputs()
    changed, contract = patch_admission(patch_sha, controls_sha)
    forecast = archive_forecast(contract, changed)
    cache_forecast = production_cache_shape_forecast(parent, contract)
    h = helper()
    full, production = h.modules()
    guard_files = h.guard_admission(full)
    h.environment(old)
    compiler = old["build_commands"][0][0]
    link = list(old["build_commands"][1])
    link[link.index(str(KERNEL_OBJECT))] = str(OUT / "build/SPOT1P64.o")
    link[link.index(str(SENDER_OBJECT))] = str(OUT / "build/FLU2DR64.o")
    link[-1] = str(OUT / "runtime/Dragon")
    common = [compiler, "-O2", "-march=native", "-ffp-contract=off", "-g", "-fPIC", "-frecord-marker=4",
        "-ffixed-line-length-none", "-I" + str(OUT / "build"), "-I" + str(ANG),
        "-I" + str(ROOT / "lib/Darwin_arm64/modules"), "-I" + str(ROOT / "Ganlib/lib/Darwin_arm64/modules"),
        "-J" + str(OUT / "build")]
    commands = [[*common, "-c", str(SOURCE / "SPOT1P64.f90"), "-o", str(OUT / "build/SPOT1P64.o")],
        [*common, "-c", str(SOURCE / "FLU2DR64.f"), "-o", str(OUT / "build/FLU2DR64.o")], link,
        [*common, "-c", str(SOURCE / "SPOT1P64.original_reference.f90"), "-o", str(OUT / "build/SPOT1P64.original_reference.o")],
        [*common, "-c", str(SOURCE / "rank1_factor_cache_controls.f90"), "-o", str(OUT / "build/rank1_factor_cache_controls.o")],
        [compiler, "-O2", "-march=native", "-ffp-contract=off", "-g", str(OUT / "build/rank1_factor_cache_controls.o"),
            str(OUT / "build/SPOT1P64.o"), str(OUT / "build/SPOT1P64.original_reference.o"), str(WHITE_OBJECT),
            str(ROOT / "lib/Darwin_arm64/libDragon.a"), str(ROOT / "Trivac/lib/Darwin_arm64/libTrivac.a"),
            str(ROOT / "Utilib/lib/Darwin_arm64/libUtilib.a"), str(ROOT / "Ganlib/lib/Darwin_arm64/libGanlib.a"),
            "-o", str(OUT / "runtime/rank1_factor_cache_controls")]]
    restored_link = list(link)
    restored_link[restored_link.index(str(OUT / "build/SPOT1P64.o"))] = str(KERNEL_OBJECT)
    restored_link[restored_link.index(str(OUT / "build/FLU2DR64.o"))] = str(SENDER_OBJECT)
    restored_link[-1] = str(PARENT / "runtime/Dragon")
    if restored_link != old["build_commands"][1]:
        raise ValueError("entire actual production link recipe must restore exactly outside the two new overrides")
    files = dict(old["files"])
    files.update(originals)
    files.update({str(PARENT / name):sha for name,sha in read(PARENT / "seal.json")["files"].items()})
    for item in (cold["terminal"], cold["run_status"], cold["stages"], cold["terminated_complete_log"],
                 *cold["raw_terminal_chain"].values(), parent["actual_external_terminal_evidence"],
                 parent["actual_external_terminal_validation"]["full_stdout"]):
        files[item["path"]] = item["sha256"]
    for path in (Path(__file__).resolve(), PARENT_FACTORY, PARENT / "seal.json", PATCH_HELPER, CONTROL_SOURCE,
                 Path("/usr/bin/nm"), Path("/usr/bin/otool"), Path("/usr/bin/dwarfdump"), Path("/bin/ps"), *guard_files):
        files[str(path)] = digest(require(path))
    roots = history_roots(sorted(set(old["resource_roots"]) | set(read(COLD / "prepared.json")["resource_roots"])
        | {str(SOURCE), str(OUT), str(TERMINAL), str(COLD_TERMINAL)}), ART)
    resources = resources_for(roots, production.ResourceFailure)
    before = resource_admission(resources)
    preserved = copy.deepcopy(old["preserved_predecessors"])
    preserved.append(dict(root=str(PARENT), inventory=h.inventory(PARENT)))
    SOURCE.mkdir()
    OUT.mkdir()
    for name in ("build", "runtime", "controls", "audit", FAMILY):
        (OUT / name).mkdir()
    for name in ["positive", *["negative_" + item["name"] for item in [*contract["negative_cases"], *contract["cap_negative_cases"]]]]:
        (OUT / "controls" / name).mkdir()
    for name, content in (("SPOT1P64.f90", changed["kernel"]), ("FLU2DR64.f", changed["sender"]),
                          ("SPOT1P64.original_reference.f90", changed["reference_kernel"])):
        (SOURCE / name).write_text(content)
    shutil.copy2(require(CONTROL_SOURCE, controls_sha), SOURCE / "rank1_factor_cache_controls.f90")
    for name, before_source, after_source in (("SPOT1P64", KERNEL_SOURCE.read_text(), changed["kernel"]),
                                            ("FLU2DR64", SENDER_SOURCE.read_text(), changed["sender"])):
        (SOURCE / (name + ".patch")).write_text("".join(difflib.unified_diff(before_source.splitlines(True),
            after_source.splitlines(True), fromfile=str(KERNEL_SOURCE if name == "SPOT1P64" else SENDER_SOURCE),
            tofile=str(SOURCE / (name + (".f90" if name == "SPOT1P64" else ".f"))))))
    shutil.copy2(require(PARENT / "runtime/run_bounded_dragon.py"), OUT / "runtime/run_bounded_dragon.py")
    write_new(SOURCE / "source_admission.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_SOURCE_ADMISSION_V1",
        actual_original_compiled_source_and_object_inputs=originals, source_patch_proof=changed["proof"],
        sole_new_production_objects=["SPOT1P64.o", "FLU2DR64.o"],
        original_reference_scope="Actual pinned 754421 source independently compiled with unit-only symbol/module renaming; historical 562f object is provenance input, not this unit executable",
        unchanged_Flu_selector_override=pin(PARENT / "build/FLU.o"), unchanged_white_object=pin(WHITE_OBJECT),
        whole_link_inverse_restoration_exact=True, control_contract=contract,
        original_source_factor_and_moment_selector_corrections_retained=True,
        source_progress_observer=changed["proof"]["progress_observer_only"],
        actual_runtime_geometry_scope="NREG2D8 x NFLOOR48 = 384 regional cells; synthetic NMAT3 controls, NSNAP3. No NR384 kernel input claim.",
        cache_arithmetic_and_RHS_order_change_claimed=False, scientific_qualification=False))
    inventory = h.inventory(SOURCE)
    files.update({str(SOURCE / name):sha for name,sha in inventory["files"].items()})
    files[str(OUT / "runtime/run_bounded_dragon.py")] = digest(OUT / "runtime/run_bounded_dragon.py")
    d = dict(schema="AXMAT_RANK1_FACTOR_CACHE_BUILD_DECLARATION_V1", family=FAMILY,
        source_root=str(SOURCE), source_inventory=inventory, files=files, build_commands=commands,
        inherited_moment_order_admission=parent, actual_failed_cold_AAA_evidence=cold,
        patch_helper=pin(PATCH_HELPER), controls_source=pin(CONTROL_SOURCE), control_contract=contract,
        complete_archive_forecast=forecast,
        stored_production_shape_cache_forecast=cache_forecast,
        preserved_predecessors=preserved, build_python_executable=old["build_python_executable"],
        native_library_aliases=old["native_library_aliases"], numerical_loader_environment=old["numerical_loader_environment"],
        resource_roots=roots, resources_before=before, artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR,
        archive_reserve_bytes=ARCHIVE_RESERVE, total_wall_seconds=TOTAL_WALL, stage_wall_seconds=STAGE_WALL,
        rss_cap_mib=RSS_CAP, threads=1, numeric_children_at_once=1, retries=0,
        rank1_factor_cache_budget_bytes=536870912, resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=resource_scope_contract(), actual_external_terminal_return_contract=terminal_contract(old["build_python_executable"]),
        future_actual_factor_cache_observer_required=cache_observer_contract(),
        actual_full_FLU_entry_executed=False, transport_launched=False, inherited_moment_order_controls_not_newly_executed=True,
        white_closure_unchanged=True, physical_data_unchanged=True, radial_arithmetic_unchanged=True, angle_grid_unchanged=True,
        original_accuracy_thresholds_changed=False, coefficient_fitting=False,
        fresh_cold_AAA_required=True, AAA_accuracy_qualified=False, ABA_admitted=False)
    h.environment(d)
    write_new(OUT / "declaration.json", d)
    if archive_bytes() >= ARCHIVE_RESERVE:
        raise ValueError("SOURCE plus OUT already exceeds its original 2GiB archive reservation")
    resources.check()
    print(json.dumps(dict(declaration=str(OUT / "declaration.json"), declaration_sha256=digest(OUT / "declaration.json"),
        source_root=str(SOURCE), classification="DECLARED_RANK1_FACTOR_CACHE_BUILD_ONLY"), allow_nan=False))


def environment(d, require_build_interpreter=True):
    helper().environment(d, require_build_interpreter=require_build_interpreter)
    if d["resource_scope_policy"] != HISTORY_SCOPE_POLICY or d["resource_scope_contract"] != resource_scope_contract():
        raise ValueError("actual inherited axial-family policy differs")
    validate_history_roots(history_roots(d["resource_roots"], ART), ART)


def declaration_admission(expected, require_build_interpreter=True):
    d = read(require(OUT / "declaration.json", expected))
    if (not re.fullmatch(r"[0-9a-f]{64}", expected or "")
            or d["schema"] != "AXMAT_RANK1_FACTOR_CACHE_BUILD_DECLARATION_V1" or d["family"] != FAMILY
            or d["source_root"] != str(SOURCE) or d["total_wall_seconds"] != TOTAL_WALL
            or d["stage_wall_seconds"] != STAGE_WALL or d["rss_cap_mib"] != RSS_CAP
            or d["archive_reserve_bytes"] != ARCHIVE_RESERVE or d["artifact_budget_bytes"] != HISTORY_CAP
            or d["min_free_bytes"] != FREE_FLOOR or d["threads"] != 1 or d["numeric_children_at_once"] != 1
            or d["retries"] != 0 or d["rank1_factor_cache_budget_bytes"] != 536870912
            or d["future_actual_factor_cache_observer_required"] != cache_observer_contract()
            or d["actual_external_terminal_return_contract"] != terminal_contract(d["build_python_executable"])
            or str(TERMINAL) not in d["resource_roots"]
            or d["actual_full_FLU_entry_executed"] is not False or d["transport_launched"] is not False
            or d["fresh_cold_AAA_required"] is not True or d["AAA_accuracy_qualified"] is not False
            or d["ABA_admitted"] is not False):
        raise ValueError("immutable rank-one build/control/resource contract differs")
    environment(d, require_build_interpreter)
    helper().verify_inventory(SOURCE, d["source_inventory"])
    parent = d["inherited_moment_order_admission"]
    if predecessor_admission(PARENT_SEAL, parent["actual_external_terminal_evidence"]["path"],
            parent["actual_external_terminal_evidence"]["sha256"]) != parent:
        raise ValueError("actual completed moment-order predecessor return changed")
    if cold_failure_admission(COLD_TERMINAL_SHA) != d["actual_failed_cold_AAA_evidence"]:
        raise ValueError("actual preserved cold failure evidence changed")
    changed, contract = patch_admission(d["patch_helper"]["sha256"], d["controls_source"]["sha256"])
    if d["complete_archive_forecast"] != archive_forecast(contract, changed):
        raise ValueError("the exact raw archive forecast and complete SOURCE+OUT reservation differ")
    if d["stored_production_shape_cache_forecast"] != production_cache_shape_forecast(parent, contract):
        raise ValueError("stored actual production memory geometry and hard array-count guard forecast differ")
    if contract != d["control_contract"] or (SOURCE / "SPOT1P64.f90").read_text() != changed["kernel"] or (
            SOURCE / "FLU2DR64.f").read_text() != changed["sender"] or (
            SOURCE / "SPOT1P64.original_reference.f90").read_text() != changed["reference_kernel"]:
        raise ValueError("actual private full-source and independent reference restoration differs")
    if (SOURCE / "rank1_factor_cache_controls.f90").read_bytes() != CONTROL_SOURCE.read_bytes():
        raise ValueError("actual reviewed Fortran controls differ")
    return d


def check_watch(stage):
    item = helper().check_watch(OUT, stage)
    watch = read(item["path"])
    if not 0 <= watch["elapsed_seconds"] < watch["wall_cap_seconds"] <= stage["wall_cap_seconds"] <= STAGE_WALL:
        raise ValueError("actual and recorded positive stage wall caps must both hold")
    return item


def raw_inventory(folder):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("actual raw control directory missing or aliased")
    files = {}
    for parent, dirs, names in os.walk(folder, followlinks=False):
        if any((Path(parent) / name).is_symlink() for name in [*dirs, *names]):
            raise ValueError("no raw control entry may be a symlink")
        for name in names:
            path = Path(parent) / name
            if not path.is_file():
                raise ValueError("no special raw control file is eligible")
            files[str(path.relative_to(OUT))] = digest(path)
    return files


def control_file(folder, name):
    if type(name) is not str or Path(name).name != name or name in ("", ".", ".."):
        raise ValueError("a raw control filename must be one literal basename")
    return require(Path(folder) / name)


def unpack_finite(raw, code, count):
    size = struct.calcsize("<" + code)
    if len(raw) != size * count:
        raise ValueError("actual raw field has an incorrect byte count")
    values = struct.unpack("<" + str(count) + code, raw)
    if code in ("f", "d") and any(not math.isfinite(item) for item in values):
        raise ValueError("an archived raw control field is nonfinite")
    return values


def input_record(path):
    """Read only one actual primitive fixture; preserve IEEE field bytes."""
    raw = require(path).read_bytes()
    if len(raw) < 96:
        raise ValueError("incomplete primitive input header")
    header = struct.unpack("<12q", raw[:96])
    version, nr, nh, nq, nl, nm, nmat, nsnap, row, white, z0, z1 = header
    if (version != 1 or z0 != 0 or z1 != 0 or white not in (0, 1) or not 1 <= row <= nr
            or any(value <= 0 for value in (nr, nh, nq, nl, nm, nmat, nsnap))
            or max(nr, nh, nq, nl, nm, nmat, nsnap) > 384):
        raise ValueError("unsupported primitive input dimensions/version")
    layout = [("mat1d", "i", nh), ("mat", "i", nh*nr), ("dz", "f", nh),
        ("total", "f", nmat+1), ("sgas", "f", (nmat+1)*nl), ("basis", "f", nr*nm),
        ("volume", "f", nr), ("radial", "d", nr*nsnap), ("ncode", "i", 2),
        ("zcode", "f", 2), ("du", "f", nq), ("w", "f", nq), ("pl", "f", nl*nq),
        ("white_perimeter", "d", 1)]
    offset, fields, values = 96, {}, {}
    for name, code, count in layout:
        length = struct.calcsize("<" + code) * count
        fields[name] = raw[offset:offset+length]
        values[name] = unpack_finite(fields[name], code, count)
        offset += length
    if offset != len(raw):
        raise ValueError("unexpected trailing or missing primitive input bytes")
    return dict(header=header, raw=raw, fields=fields, values=values)


def field_record(folder, record, fixture):
    """One complete returned field, never an assembled surrogate result."""
    path = control_file(folder, record["file"])
    raw = path.read_bytes()
    nr, nh, nq, nl, nm = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct", "nmode")]
    counts = (nr*nh*nl, nr*(nh+1), nr*nq)
    expected = (1, nr, nh, nq, nl, nm, record["group"], record["rhs"], *counts, 0)
    if len(raw) < 96 or struct.unpack("<12q", raw[:96]) != expected:
        raise ValueError("actual source/layer/angle returned field header differs")
    unpack_finite(raw[96:], "d", sum(counts))
    q_path = control_file(folder, record["q_file"])
    q = q_path.read_bytes()
    unpack_finite(q, "d", counts[0])
    # The source family is independently constructed in the external auditor,
    # in Fortran q(1,moment,floor,region) storage order, for every actual call.
    independent_q = b"".join(struct.pack("<3d",
        0.125 + record["rhs"]/32.0 + (region+floor)/1024.0,
        record["rhs"]/512.0, -record["rhs"]/1024.0)
        for region in range(1, nr+1) for floor in range(1, nh+1))
    if nl != 3 or q != independent_q:
        raise ValueError("actual independently stored raw P0/P1/P2 source family differs")
    return raw, q


def json_lines(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate actual control manifest key")
            value[key] = item
        return value
    rows = []
    with require(path).open() as stream:
        for line in stream:
            value = json.loads(line, object_pairs_hook=unique,
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite manifest value")))
            if type(value) is not dict:
                raise ValueError("actual manifest must consist solely of JSON object rows")
            rows.append(value)
    return rows


def cache_accounting(fixture, nmat=3):
    """Independent int64 element-count arithmetic, including temporary keys."""
    nr, nh, nq, nl, nm = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct", "nmode")]
    nsnap = 3
    raw_count = 17+nh+nh*nr+nh+(nmat+1)+(nmat+1)*nl+nr*nm+nr+nr*nsnap+2*nq+nl*nq+2
    projected_count = 2+nr+nm*nm+2*nm*nm*nh+nm*nm*nl*nh+2*nq*nl
    if fixture["white"]:
        projected_count += nq*nq+nm*nm
    factor_bytes = (24*nq*nq+12*nq)*(nh+1)
    return dict(descriptor_bytes=fixture["groups"]*4096, raw_key_bytes=raw_count*8,
        projected_key_bytes=projected_count*8, factor_bytes_per_group=factor_bytes,
        persistent_bytes_per_group=(raw_count+projected_count)*8+factor_bytes,
        final_retained_bytes=fixture["groups"]*(4096+(raw_count+projected_count)*8+factor_bytes))


def check_counters(record, state, fixture, update):
    keys = ("built", "reused", "hits", "live", "peak", "cap", "legacy_built", "legacy_reused")
    if any(type(record[key]) is not int or record[key] < 0 for key in keys):
        raise ValueError("actual cache counters must be nonnegative integers")
    account = cache_accounting(fixture)
    if fixture["rank1"]:
        if update:
            if record["rhs"] == 1:
                before = state["live"]
                first = before+2*account["raw_key_bytes"]
                second = before+account["raw_key_bytes"]+2*account["projected_key_bytes"]
                state["live"] += account["persistent_bytes_per_group"]
                state["peak"] = max(state["peak"], first, second, state["live"])
                state["built"] += fixture["nfloor"]+1
            else:
                state["peak"] = max(state["peak"], state["live"]+max(
                    account["raw_key_bytes"], account["projected_key_bytes"]))
                state["reused"] += fixture["nfloor"]+1
                state["hits"] += 1
        # Ordinary POD previously had its legacy cache disabled. Its ABI stays
        # at zero; the new rank-one counters are independent int64 values.
        expected = dict(state, cap=536870912, legacy_built=0, legacy_reused=0)
    else:
        if fixture["name"] == "legacy_physical" and update:
            if record["rhs"] == 1:
                state["legacy_built"] += fixture["nmode"]*(fixture["nfloor"]+1)
            else:
                state["legacy_reused"] += fixture["nmode"]*(fixture["nfloor"]+1)
        elif update:
            # The enabled rank-one pool checks raw identity before declining
            # an ineligible dense/translation first call. Its one temporary
            # raw key is accounted even though no plan/factor is retained.
            state["peak"] = max(state["peak"], state["live"]+account["raw_key_bytes"])
        expected = dict(state, cap=536870912)
    if any(record[key] != expected[key] for key in keys):
        raise ValueError("actual cache allocation/build/reuse/identity counters do not match independent accounting")
    if not record["live"] <= record["peak"] <= record["cap"]:
        raise ValueError("cache retained/peak accounted bytes exceed their explicitly new 512MiB cap")


def input_fixture_audit(folder, fixture):
    nr, nh, nq, nl, nm = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct", "nmode")]
    name = fixture["name"]
    base = input_record(control_file(folder, name+".inputs.bin"))
    if base["header"] != (1, nr, nh, nq, nl, nm, 3, 3, 1, int(fixture["white"]), 0, 0):
        raise ValueError("actual fixture primitive dimensions/white closure metadata differs")
    values = base["values"]
    if sum(values["dz"]) != 150.0 or values["ncode"] != ((4, 4) if name == "legacy_translation" else (1, 1)):
        raise ValueError("actual full-height mesh or original boundary control differs")
    if (sum(value > 0 for value in values["du"]) != nq//2
            or sum(value < 0 for value in values["du"]) != nq//2
            or any(value <= 0 for value in values["w"])):
        raise ValueError("actual original ALGPT angular coverage is incomplete")
    for index, direction in enumerate(values["du"]):
        matches = [j for j, other in enumerate(values["du"]) if struct.pack("<f", other) == struct.pack("<f", -direction)]
        if len(matches) != 1 or struct.pack("<f", values["w"][index]) != struct.pack("<f", values["w"][matches[0]]):
            raise ValueError("actual SN directions/weights do not have an exact paired involution")
    if any(values["pl"][nl*index] != 1.0 or values["pl"][nl*index+1] != values["du"][index] for index in range(nq)):
        raise ValueError("actual source-moment angular mapping is not complete P0/P1/P2")
    volume_sum = sum(values["volume"])
    if volume_sum <= 0 or any(value <= 0 for value in values["volume"]):
        raise ValueError("actual radial volumes must be positive")
    gram = [[sum(values["volume"][region]/volume_sum * values["basis"][region+nr*a]
        * values["basis"][region+nr*b] for region in range(nr)) for b in range(nm)] for a in range(nm)]
    if fixture["rank1"] and (gram[0][0] == 1.0 or not any(value < 0 for value in values["basis"])
            or not any(value > 0 for value in values["basis"])):
        raise ValueError("the actual ordinary rank-one fixture must expose signed nonunit Gram coordinates")
    for group in range(1, fixture["groups"]+1):
        changed = input_record(control_file(folder, name+"_g"+str(group)+".inputs.bin"))
        if changed["header"] != base["header"] or any(changed["fields"][key] != base["fields"][key]
                for key in base["fields"] if key != "total"):
            raise ValueError("a group's actual raw operator changed outside the declared total entry")
        variant = 1 if name == "lifecycle_reset_2" else 0
        wanted = base["fields"]["total"][:4]+struct.pack("<f", 1.125+0.0625*variant+group/8192.0)+base["fields"]["total"][8:]
        if changed["fields"]["total"] != wanted:
            raise ValueError("actual group-specific primitive operator/source coverage differs")
    return dict(weighted_Gram=gram, actual_signed_basis=any(value < 0 for value in values["basis"]),
        actual_geometry=[nr, nh, nq, nl, nm], archived_group_inputs=fixture["groups"])


def control_audit(d):
    """Independent streaming audit; all raw files were already hashed first."""
    receipt = read(require(OUT / "raw_controls_receipt.json"))
    if receipt["before_numeric_gates"] is not True or receipt["files"] != raw_inventory(OUT / "controls"):
        raise ValueError("complete original raw bytes/hashes must precede every numerical gate")
    c = d["control_contract"]
    if (c["raw_header"] != ["version", "nreg2d", "nfloor", "npq", "nsct", "nmode", "group", "rhs",
            "flux_count", "cour_count", "xnei_count", "reserved_zero"]
            or c["roles"] != ["original", "build", "reuse"] or c["descriptor_bytes_per_group"] != 4096
            or len(c["positive_fixtures"]) != 7 or len(c["negative_cases"]) != 14):
        raise ValueError("actual complete independently interpretable raw control protocol differs")
    folder = OUT / "controls/positive"
    rows = json_lines(control_file(folder, "manifest.jsonl"))
    cursor, pairs, scalar_fields, data_bytes = 0, 0, 0, 0
    seen_files = {"manifest.jsonl", "execute.log", "execute.watchdog.json"}
    fixture_results = []
    expected_terminals = []
    for fixture in c["positive_fixtures"]:
        witness = input_fixture_audit(folder, fixture)
        name = fixture["name"]
        seen_files.add(name+".inputs.bin")
        seen_files.update(name+"_g"+str(group)+".inputs.bin" for group in range(1, fixture["groups"]+1))
        account = cache_accounting(fixture)
        live = account["descriptor_bytes"] if name != "legacy_physical" else 0
        state = dict(built=0, reused=0, hits=0, live=live, peak=live)
        if not fixture["rank1"]:
            state.update(legacy_built=0, legacy_reused=0)
        q_by_rhs = {}
        for group in range(1, fixture["groups"]+1):
            for rhs in range(1, fixture["nrhs"]+1):
                original, cached = rows[cursor:cursor+2]
                cursor += 2
                expected_role = "build" if rhs == 1 else "reuse"
                for record, role, update in ((original, "original", False), (cached, expected_role, True)):
                    stem = name+"_g"+str(group)+"_r"+str(rhs)+"_"+role
                    if (record["kind"] != "field" or record["case"] != name or record["role"] != role
                            or record["group"] != group or record["rhs"] != rhs
                            or record["file"] != stem+".bin" or record["q_file"] != stem+".q.bin"
                            or record["input_file"] != name+"_g"+str(group)+".inputs.bin"):
                        raise ValueError("actual all-group/all-RHS/original-build-hit manifest order differs")
                    check_counters(record, state, fixture, update)
                    seen_files.update((record["file"], record["q_file"]))
                reference_raw, reference_q = field_record(folder, original, fixture)
                cached_raw, cached_q = field_record(folder, cached, fixture)
                if reference_raw != cached_raw or reference_q != cached_q:
                    raise ValueError("actual returned flux/cour/xnei fields or source differ bitwise from the uncached original source")
                if rhs in q_by_rhs and reference_q != q_by_rhs[rhs]:
                    raise ValueError("same declared source RHS must remain identical across all groups")
                q_by_rhs[rhs] = reference_q
                pairs += 1
                scalar_fields += (len(reference_raw)-96)//8
                data_bytes += len(reference_raw)+len(cached_raw)+len(reference_q)+len(cached_q)
        if len(set(q_by_rhs.values())) != 3:
            raise ValueError("all three independent changing raw RHS sources must actually occur")
        final_state = dict(state)
        clear = rows[cursor]
        cursor += 1
        if clear != dict(kind="clear", case=name, built=0, reused=0, hits=0, live=0, peak=0):
            raise ValueError("actual lifecycle CLEAR must reset all new counters and all retained cache bytes")
        if fixture["rank1"] and final_state["live"] != account["final_retained_bytes"]:
            raise ValueError("all actually filled group plans must equal independent complete allocation accounting")
        fixture_results.append(dict(name=name, source_pairs=fixture["groups"]*fixture["nrhs"],
            primitive_witness=witness, independent_accounting=account, actual_final_counters=final_state,
            all_fields_bitwise_equal=True, lifecycle_zero_verified=True))
        if fixture["rank1"]:
            expected_terminals.append([final_state["built"], final_state["reused"], final_state["hits"],
                final_state["peak"], 536870912])
    pivot = rows[cursor]
    cursor += 1
    if pivot != dict(kind="pivot", original="pivot_original.bin", split="pivot_split.bin", factors="pivot_factors.bin", rows=4, rhs=3):
        raise ValueError("independent pivot/tie/multiple RHS control must be actually archived")
    pivot_inputs = control_file(folder, "pivot_inputs.bin").read_bytes()
    unpack_finite(pivot_inputs, "d", 28)
    matrix_rows = [[0.0, 2.0, 1.0, 0.0], [2.0, 1.0, 0.0, 1.0],
        [-2.0, 0.0, 3.0, 1.0], [1.0, 1.0, 1.0, 4.0]]
    independent_pivot_input = b"".join(struct.pack("<d", matrix_rows[row][column])
        for column in range(4) for row in range(4))
    independent_pivot_input += b"".join(struct.pack("<d", (row-column)/8.0)
        for column in range(1, 4) for row in range(1, 5))
    if pivot_inputs != independent_pivot_input:
        raise ValueError("actual first-tie matrix and all three independent pivot RHS columns differ")
    original = control_file(folder, "pivot_original.bin").read_bytes()
    split = control_file(folder, "pivot_split.bin").read_bytes()
    factors = control_file(folder, "pivot_factors.bin").read_bytes()
    if len(original) != 104 or len(split) != 104 or original[:8] != struct.pack("<q", 0) or split != original:
        raise ValueError("the actual split pivot solver and original ALSBD fields must succeed and be bitwise identical")
    unpack_finite(original[8:], "d", 12)
    if len(factors) != 184 or factors[:8] != struct.pack("<q", 0):
        raise ValueError("actual factorization raw fields/info incomplete")
    unpack_finite(factors[8:136], "d", 16)
    pivot_rows = struct.unpack("<4i", factors[136:152])
    unpack_finite(factors[152:], "d", 4)
    if any(not index+1 <= value <= 4 for index, value in enumerate(pivot_rows)) or pivot_rows[0] != 2:
        raise ValueError("actual strict-first pivot/tie choice differs from original ALSBD")
    seen_files.update(("pivot_inputs.bin", "pivot_original.bin", "pivot_factors.bin", "pivot_split.bin"))
    if rows[cursor:] != [dict(kind="clear", built=0, reused=0, hits=0, live=0, peak=0)]:
        raise ValueError("all actual manifest rows must have been independently interpreted once")
    if {path.name for path in folder.iterdir()} != seen_files:
        raise ValueError("positive complete raw archive namespace differs from the independent expected coverage")
    actual_log = (folder / "execute.log").read_text()
    if "RAW_CONTROLS_COMPLETE" not in actual_log:
        raise ValueError("the complete real positive child return marker is missing")
    terminal_rows = []
    for line in actual_log.splitlines():
        if "AXMAT-RANK1-CACHE TERMINAL" in line:
            match = re.fullmatch(r"\s*AXMAT-RANK1-CACHE TERMINAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*", line)
            if match is None:
                raise ValueError("the actual cache-terminal observer has a malformed five-int64 record")
            terminal_rows.append([int(value) for value in match.groups()])
    if terminal_rows != expected_terminals:
        raise ValueError("every actual unit cache terminal must equal independently counted build/reuse/identity/peak/cap state")
    negative_results = []
    mutation_field = dict(total="total", selfscat="sgas", radial="radial", basis="basis", mesh="dz",
        du="du", weights="w", pl="pl", boundary="ncode", signed_zero="total", white_perimeter="white_perimeter")
    prime_fixture = dict(name="negative", nreg2d=8, nfloor=48, npq=32, nsct=3, nmode=1, groups=2, white=True, rank1=True)
    for case in c["negative_cases"]:
        name = case["name"]
        folder = OUT / "controls" / ("negative_"+name)
        rows = json_lines(control_file(folder, "manifest.jsonl"))
        stem = "negative_"+name
        if len(rows) != 2 or rows[1] != dict(kind="negative_expected", case=name, expected_XABORT=case["expected_message"]):
            raise ValueError("the actual independent negative attempt metadata differs")
        prime = rows[0]
        if (prime["kind"] != "field" or prime["case"] != stem or prime["role"] != "prime"
                or prime["group"] != 1 or prime["rhs"] != 1
                or prime["file"] != stem+"_g1_r1_prime.bin" or prime["q_file"] != stem+"_g1_r1_prime.q.bin"
                or prime["input_file"] != stem+"_prime.inputs.bin"):
            raise ValueError("an actual cached production-shape call must prime each independent negative process")
        account = cache_accounting(prime_fixture)
        state = dict(built=0, reused=0, hits=0, live=account["descriptor_bytes"], peak=account["descriptor_bytes"])
        check_counters(prime, state, prime_fixture, True)
        field_record(folder, prime, prime_fixture)
        first = input_record(control_file(folder, stem+"_prime.inputs.bin"))
        changed = input_record(control_file(folder, stem+"_mutated.inputs.bin"))
        if first["header"] != (1, 8, 48, 32, 3, 1, 3, 3, 1, 1, 0, 0):
            raise ValueError("each negative's actual priming operator must have the declared full production shape")
        if first["raw"] == changed["raw"]:
            raise ValueError("a negative control must actually change raw operator identity")
        if name in mutation_field:
            target = mutation_field[name]
            if first["header"] != changed["header"] or any(first["fields"][key] != changed["fields"][key]
                    for key in first["fields"] if key != target) or first["fields"][target] == changed["fields"][target]:
                raise ValueError("the negative operator mutation is outside its exact declared field")
            if name == "signed_zero" and (first["fields"]["total"][:4] != b"\x00\x00\x00\x00"
                    or changed["fields"]["total"][:4] != b"\x00\x00\x00\x80"):
                raise ValueError("the actual IEEE signed-zero identity mutation is missing")
        elif name in ("white_on", "white_row"):
            index, wanted = (9, 0) if name == "white_on" else (8, 2)
            independent_header = list(first["header"])
            independent_header[index] = wanted
            if tuple(independent_header) != changed["header"] or first["fields"] != changed["fields"]:
                raise ValueError("the actual white metadata mutation differs from its declared single-entry control")
        elif name == "dims":
            if first["header"][5] != 1 or changed["header"][5] != 2:
                raise ValueError("the actual mode-count mutation was not independently witnessed")
            wanted = list(first["header"])
            wanted[5] = 2
            if tuple(wanted) != changed["header"] or any(first["fields"][key] != changed["fields"][key]
                    for key in first["fields"] if key != "basis"):
                raise ValueError("the actual dimension guard changed unrelated primitive inputs")
        else:
            raise ValueError("a negative mutation has no independent raw interpretation")
        message = control_file(folder, "actual_XABORT.txt").read_text()
        if message != case["expected_message"]+"\n" or "RAW_ACTUAL_UNIT_XABORT "+case["expected_message"] not in (folder / "execute.log").read_text():
            raise ValueError("the actual kernel guard must refuse through the exact archived expected unit XABORT")
        expected_files = {"manifest.jsonl", "execute.log", "execute.watchdog.json", "actual_XABORT.txt",
            prime["file"], prime["q_file"], stem+"_prime.inputs.bin", stem+"_mutated.inputs.bin"}
        if {path.name for path in folder.iterdir()} != expected_files:
            raise ValueError("each negative must preserve exactly its raw prime/mutation/rejection archive, with no normal return")
        negative_results.append(dict(name=name, actual_message=message.rstrip("\n"),
            raw_prime=pin(folder / (stem+"_prime.inputs.bin")), raw_mutation=pin(folder / (stem+"_mutated.inputs.bin")),
            archived_actual_XABORT=pin(folder / "actual_XABORT.txt"), expected_rejection=True))
    cap_results = []
    for case in c["cap_negative_cases"]:
        name = case["name"]
        folder = OUT / "controls" / ("negative_"+name)
        raw_request = control_file(folder, "cap_request.bin").read_bytes()
        if len(raw_request) != 96:
            raise ValueError("the actual pre-allocation cap request must retain all twelve int64 values")
        request = struct.unpack("<12q", raw_request)
        live = 370*4096
        operation = 1 if name == "cap_reserve" else 2
        asked = 536870912-live+1 if operation == 1 else 0
        expected = (1, operation, 370, 0 if operation == 1 else 2147483647,
            0 if operation == 1 else 49, asked, 0, 0, 0, live, live, 536870912)
        if request != expected:
            raise ValueError("the actual cap negative dimensions/remaining-byte request differ from independent int64 accounting")
        rows = json_lines(control_file(folder, "manifest.jsonl"))
        if rows != [dict(kind="resource_negative_expected", case=name, file="cap_request.bin",
                expected_XABORT=case["expected_message"], operation=operation,
                requested_bytes=asked, live=live, peak=live, cap=536870912)]:
            raise ValueError("actual cap negative metadata must bind the exact archived pre-allocation request")
        message = control_file(folder, "actual_XABORT.txt").read_text()
        if (message != case["expected_message"]+"\n"
                or "RAW_ACTUAL_UNIT_XABORT "+case["expected_message"] not in (folder / "execute.log").read_text()
                or {path.name for path in folder.iterdir()} != {"manifest.jsonl", "execute.log", "execute.watchdog.json",
                    "cap_request.bin", "actual_XABORT.txt"}):
            raise ValueError("the actual guarded cap call must refuse with its exact raw command-specific unit message and no normal return")
        cap_results.append(dict(name=name, raw_request=pin(folder / "cap_request.bin"),
            actual_XABORT=pin(folder / "actual_XABORT.txt"), expected_rejection=True,
            cache_accounting_preallocation_guard=True, actual_OwnRSS_oversize_child_test=False))
    actual_raw_bytes = sum(require(OUT / name).stat().st_size for name in receipt["files"]
        if name.endswith(".bin") or Path(name).name == "actual_XABORT.txt")
    if actual_raw_bytes != d["complete_archive_forecast"]["exact_control_raw_binary_and_abort_message_bytes"]:
        raise ValueError("all actual complete binary/control-message archive bytes must match the pre-create exact forecast")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_RAW_CONTROLS_AUDIT_V1", status="PASS",
        counts=dict(fixtures=7, actual_returned_unit_kernel_calls=pairs*2+14,
            actual_guard_rejected_unit_kernel_calls=14, actual_total_unit_kernel_invocations=pairs*2+28, bitwise_source_pairs=pairs,
            independent_pivot_rhs=3, negative_calls=14, cache_cap_negative_calls=2, production_groups=370,
            production_layers=48, production_angles=32, source_moments=3,
            bitwise_compared_output_scalars=scalar_fields, compared_actual_field_and_source_bytes=data_bytes),
        fixtures=fixture_results, negative_controls=negative_results, cache_cap_negative_controls=cap_results,
        actual_first_tie_pivot=pivot_rows[0], actual_complete_raw_binary_and_abort_message_bytes=actual_raw_bytes,
        actual_cache_terminal_observer_rows=terminal_rows,
        complete_raw_receipt=pin(OUT / "raw_controls_receipt.json"),
        all_actual_outputs_finite=True, all_flux_cour_xnei_bitwise_equal=True,
        all_sources_independently_reconstructed=True, all370_plans_retained_and_accounted=True,
        all_lifecycle_clears_zero=True, signed_nonunit_Gram_controls=True,
        physical_dense_translation_outputs_bitwise_unchanged=True,
        actual_guard_rejections=True, independent_complete_LU_reconstruction_claimed=False,
        cache_accounting_preallocation_guard_rejections=True, new_OwnRSS_oversize_child_test_claimed=False,
        historical_object_used_in_unit_baseline=False, actual_full_FLU_entry_executed=False,
        original_moment_selector_controls_newly_executed=False,
        scientific_accuracy_or_performance_qualified=False)


def binary_audit(d):
    paths = {"new_kernel": OUT / "build/SPOT1P64.o", "new_sender": OUT / "build/FLU2DR64.o",
        "reference_kernel": OUT / "build/SPOT1P64.original_reference.o", "actual_Dragon": OUT / "runtime/Dragon"}
    raw = {}
    for name, path in paths.items():
        require(path)
        for tool, args in (("symbols", ["/usr/bin/nm", "-gU", str(path)]),
                           ("instructions", ["/usr/bin/otool", "-tV", str(path)]),
                           ("debug", ["/usr/bin/dwarfdump", "--debug-info", str(path)])):
            result = subprocess.run(args, capture_output=True, check=True, timeout=60)
            target = OUT / "audit" / (name + "_" + tool + ".txt")
            with target.open("xb") as stream:
                stream.write(result.stdout)
            raw[name + "_" + tool] = pin(target)
    write_new(OUT / "audit/raw_binary_receipt.json", dict(files=raw, before_binary_gates=True))
    # Source/command identities and actual defined symbols prove normal private
    # compilation/linking; this is not an independent complete instruction or
    # LU reconstruction claim.
    def symbols(name):
        return [line.split()[-1] for line in Path(raw[name + "_symbols"]["path"]).read_text().splitlines() if line.split()]
    for name, symbol in (("new_kernel", "_spot1p64_"), ("new_sender", "_flu2dr64_"),
                         ("reference_kernel", "_spot1p64_original_")):
        if symbols(name).count(symbol) != 1:
            raise ValueError("actual separately compiled expected routine is missing/duplicated: " + symbol)
    for symbol in ("_spot1p64_", "_flu2dr64_", "_flu_"):
        if symbols("actual_Dragon").count(symbol) != 1:
            raise ValueError("actual new executable has missing/duplicate production definition")
    if (digest(paths["new_kernel"]) == KERNEL_OBJECT_SHA or digest(paths["new_sender"]) == SENDER_OBJECT_SHA
            or digest(paths["actual_Dragon"]) == PARENT_RUNTIME_SHA):
        raise ValueError("genuine new compiled objects and executable must differ from prior binaries")
    for name, source in (("new_kernel", "SPOT1P64.f90"), ("new_sender", "FLU2DR64.f"),
                         ("reference_kernel", "SPOT1P64.original_reference.f90")):
        if str(SOURCE / source) not in Path(raw[name + "_debug"]["path"]).read_text():
            raise ValueError("actual debug compilation unit does not name its declared private source")
    old = read(PARENT / "declaration.json")["build_commands"][1]
    link = list(d["build_commands"][2])
    if str(KERNEL_OBJECT) in link or str(SENDER_OBJECT) in link:
        raise ValueError("the replaced old explicit objects must not remain in the new link")
    for old_path, new_path in ((KERNEL_OBJECT, OUT / "build/SPOT1P64.o"), (SENDER_OBJECT, OUT / "build/FLU2DR64.o")):
        if link.count(str(new_path)) != 1 or link.index(str(new_path)) >= link.index(str(ROOT / "lib/Darwin_arm64/libDragon.a")):
            raise ValueError("both actual private overrides must precede the unchanged archive")
        link[link.index(str(new_path))] = str(old_path)
    link[-1] = str(PARENT / "runtime/Dragon")
    if link != old:
        raise ValueError("entire genuine parent link chain fails inverse restoration")
    return dict(status="PASS", source_and_command_identity_verified=True,
        exact_parent_link_inverse_restoration=True, actual_private_object_definitions_verified=True,
        executable_definitions_verified=True, raw_metadata=raw, actual_objects={key:pin(path) for key,path in paths.items()},
        entire_historical_compiled_source_reconstruction_claimed=False,
        independent_complete_instruction_equivalence_claimed=False, independent_LU_reconstruction_claimed=False)


def audit_build(expected):
    d = declaration_admission(expected)
    claim = read(require(OUT / "execution_claim.json"))
    stages = read(require(OUT / FAMILY / "stages.json"))["stages"]
    labels, commands = stage_labels(d), stage_commands(d, expected)
    if (claim["parent_pid"] != os.getppid() or claim["declaration_sha256"] != expected
            or len(stages) != len(labels) or [row["label"] for row in stages] != labels
            or [row["command"] for row in stages] != commands or stages[-1]["command"] != [sys.executable, *sys.argv]
            or stages[-1]["status"] != "RUNNING" or any(row["status"] != "PASS" for row in stages[:-1])):
        raise ValueError("only the actual serial last audit child may accept complete previous stages")
    watches = [check_watch(row) for row in stages[:-1]]
    raw = read(require(OUT / "raw_controls_receipt.json"))
    if raw["files"] != raw_inventory(OUT / "controls") or raw["before_numeric_gates"] is not True:
        raise ValueError("all actual raw controls must be archived before numerical acceptance")
    identity = read(require(OUT / "runtime/build_identity.json"))
    helper().verify({str(OUT / name):sha for name,sha in identity["files"].items()})
    controls = control_audit(d)
    write_new(OUT / "audit/controls.json", controls)
    binary = binary_audit(d)
    write_new(OUT / "audit/binary_identity.json", binary)
    write_new(OUT / "audit/result.json", dict(classification="PASS_RANK1_FACTOR_CACHE_BUILD_CONTROLS_ONLY",
        declaration_sha256=expected, control_status=controls["status"], binary_status=binary["status"],
        rank1_factor_cache_controls_passed=True, all_new_cache_outputs_bitwise_equal_to_uncached=True,
        operator_identity_guard_negative_controls_passed=True, rank1_factor_cache_math_and_rhs_order_unchanged=True,
        control_counts=controls["counts"], previous_stage_watchdogs=watches,
        inherited_moment_order_admission=d["inherited_moment_order_admission"],
        actual_failed_cold_AAA_evidence=d["actual_failed_cold_AAA_evidence"],
        inherited_moment_order_controls_not_newly_executed=True, newly_executed_original_interface_receiver_calls=0,
        newly_executed_native_receiver_calls=controls["counts"]["actual_total_unit_kernel_invocations"],
        actual_full_FLU_entry_executed=False, transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False,
        future_actual_factor_cache_observer_required=cache_observer_contract(),
        fresh_cold_AAA_required=True, coefficient_fitting=False))
    print("AXMAT-RANK1-CACHE-BUILD-AUDITED", flush=True)


def run_build(expected):
    started = time.monotonic()
    d = declaration_admission(expected)
    h = helper()
    full, production = h.modules()
    h.guard_admission(full)
    resources = resources_for(d["resource_roots"], production.ResourceFailure)
    resource_admission(resources)
    write_new(OUT / "execution_claim.json", dict(parent_pid=os.getpid(), declaration_sha256=expected,
        started_unix=time.time(), started_monotonic=started, retries=0))
    remaining = TOTAL_WALL - (time.monotonic()-started)
    if remaining <= 0:
        raise ValueError("whole build budget already exhausted before the first real compilation")
    runner = full.OwnRSSSerialExecutor(OUT, remaining, FAMILY, resources)
    result = dict(classification="FAILED_RANK1_FACTOR_CACHE_BUILD_NO_RETRY", error=None,
        actual_full_FLU_entry_executed=False, transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False)
    try:
        for index, command in enumerate(d["build_commands"]):
            environment(d)
            runner.execute(OUT / "build", f"build_{index:02d}", command, STAGE_WALL)
        names = ("runtime/Dragon", "runtime/rank1_factor_cache_controls", "build/SPOT1P64.o", "build/FLU2DR64.o",
            "build/SPOT1P64.original_reference.o", "build/rank1_factor_cache_controls.o")
        write_new(OUT / "runtime/build_identity.json", dict(files={name:digest(require(OUT / name)) for name in names},
            sole_new_production_overrides=["SPOT1P64.o", "FLU2DR64.o"], inherited_Flu_override=pin(PARENT / "build/FLU.o")))
        try:
            environment(d)
            command = [str(OUT / "runtime/rank1_factor_cache_controls"), *d["control_contract"]["positive_command_args"]]
            runner.execute(OUT / "controls/positive", "execute", command, STAGE_WALL)
            for case in [*d["control_contract"]["negative_cases"], *d["control_contract"]["cap_negative_cases"]]:
                environment(d)
                runner.execute(OUT / "controls" / ("negative_" + case["name"]), "execute",
                    [str(OUT / "runtime/rank1_factor_cache_controls"), *case["args"]], STAGE_WALL)
        finally:
            # Preserve all returned/partial raw files and actual stdout before
            # any independent finite/bitwise or expected-negative-message gate.
            write_new(OUT / "raw_controls_receipt.json", dict(files=raw_inventory(OUT / "controls"),
                before_numeric_gates=True, declared_control_contract=d["control_contract"]))
        runner.execute(OUT / "audit", "audit", stage_commands(d, expected)[-1], STAGE_WALL,
                       "AXMAT-RANK1-CACHE-BUILD-AUDITED")
        stages = read(OUT / FAMILY / "stages.json")["stages"]
        if (len(stages) != len(stage_labels(d)) or [row["label"] for row in stages] != stage_labels(d)
                or [row["command"] for row in stages] != stage_commands(d, expected)
                or any(row["status"] != "PASS" for row in stages)):
            raise ValueError("all declared build/control/audit stages must actually pass exactly once")
        audit = read(OUT / "audit/result.json")
        if (audit["classification"] != "PASS_RANK1_FACTOR_CACHE_BUILD_CONTROLS_ONLY"
                or audit["control_status"] != "PASS" or audit["binary_status"] != "PASS"
                or any(audit[key] is not True for key in ("rank1_factor_cache_controls_passed",
                    "all_new_cache_outputs_bitwise_equal_to_uncached", "operator_identity_guard_negative_controls_passed",
                    "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required"))):
            raise ValueError("actual complete raw cache controls and compiled override identity must pass")
        result.update(classification="COMPLETE_RANK1_FACTOR_CACHE_BUILD_CONTROLS_ONLY", watchdogs=[check_watch(row) for row in stages],
            control_counts=audit["control_counts"], runtime_sha256=digest(OUT / "runtime/Dragon"),
            rank1_factor_cache_budget_bytes=536870912, source_root=str(SOURCE),
            all_new_cache_outputs_bitwise_equal_to_uncached=True, fresh_cold_AAA_required=True)
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        try:
            environment(d)
            h.verify_inventory(SOURCE, d["source_inventory"])
            result["resources"] = resources.check()
            actual_size, elapsed = archive_bytes(), time.monotonic()-started
            if actual_size >= ARCHIVE_RESERVE or elapsed >= TOTAL_WALL:
                raise ValueError("complete SOURCE plus OUT or whole build wall budget exceeded")
            result.update(elapsed_seconds=elapsed, archive_bytes_before_closeout=actual_size)
        except BaseException as error:
            result.update(classification="FAILED_RANK1_FACTOR_CACHE_BUILD_NO_RETRY", error=repr(error),
                elapsed_seconds=time.monotonic()-started)
            write_new(OUT / "driver_result.json", result)
            raise
        write_new(OUT / "driver_result.json", result)
    write_new(OUT / "seal.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_BUILD_SEAL_V1", files={
        str(path.relative_to(OUT)):digest(path) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()}))
    try:
        final_resources = resources.check()
        final_size, final_elapsed = archive_bytes(), time.monotonic()-started
        if final_size >= ARCHIVE_RESERVE or final_elapsed >= TOTAL_WALL:
            raise ValueError("mandatory complete post-seal tail failed")
    except BaseException as error:
        write_new(OUT / "closeout_failure.json", dict(error=repr(error), complete=False,
            AAA_accuracy_qualified=False, ABA_admitted=False))
        raise
    print(json.dumps(dict(result=result, actual_tail_check="PASS", actual_elapsed_seconds=final_elapsed,
        actual_archive_bytes=final_size, actual_resources=final_resources), allow_nan=False), flush=True)


def strict_terminal_json(path):
    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate key in actual external terminal JSON")
            value[key] = item
        return value
    def reject_constant(value):
        raise ValueError("nonfinite JSON constant in actual external terminal JSON: " + value)
    result = json.loads(Path(path).read_text(), object_pairs_hook=unique_object, parse_constant=reject_constant)
    if type(result) is not dict:
        raise ValueError("the full actual terminal output must be one JSON object")
    return result


def terminal_file(value, expected_sha=None):
    if not isinstance(value, (str, Path)):
        raise ValueError("actual external terminal evidence requires an absolute canonical regular path")
    path = Path(value)
    if (not path.is_absolute() or ".." in path.parts or str(value) != str(path)
            or path.parent != TERMINAL or path.resolve(strict=True) != path):
        raise ValueError("actual external terminal path is outside its independent fixed root")
    cursor = path
    while True:
        if cursor.is_symlink():
            raise ValueError("external terminal evidence or ancestor is a symlink")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    return require(path, expected_sha)


def external_terminal_admission(d, declared_sha, expected_seal, sealed_result,
                                terminal_evidence, terminal_evidence_sha256):
    """Require Root's retained real exit-zero proof after all closeout work.

    A success seal can exist while this parent still runs or after interruption.
    It is never sufficient without this independently produced terminal record.
    This factory neither creates that record nor infers exit zero from a flag.
    """
    if (not isinstance(terminal_evidence_sha256, str) or len(terminal_evidence_sha256) != 64
            or any(c not in "0123456789abcdef" for c in terminal_evidence_sha256)):
        raise ValueError("actual independent terminal-return receipt SHA256 is mandatory")
    if (TERMINAL.parent != ART or TERMINAL in (SOURCE, OUT)
            or any(TERMINAL.is_relative_to(root) or root.is_relative_to(TERMINAL) for root in (SOURCE, OUT))
            or str(TERMINAL) not in d["resource_roots"]):
        raise ValueError("external terminal root must be independent and within the declared total-history scope")
    receipt = terminal_file(terminal_evidence, terminal_evidence_sha256)
    if receipt != TERMINAL / "terminal_return.json":
        raise ValueError("only the fixed actual external terminal-return record is eligible")
    e = strict_terminal_json(receipt)
    factory = Path(__file__).resolve()
    source_pin = dict(path=str(factory), sha256=digest(require(factory)))
    command = [d["build_python_executable"], str(factory), "run-build", "--sha256", declared_sha]
    if (e["schema"] != TERMINAL_SCHEMA or e["record_producer"] != "root"
            or e["actual_tool_terminal_return_observed"] is not True
            or e["record_written_after_actual_terminal_return"] is not True
            or type(e["returncode"]) is not int or e["returncode"] != 0
            or e["command"] != command or e["source"] != source_pin
            or d["files"].get(str(factory)) != source_pin["sha256"]
            or e["declaration"] != dict(path=str(OUT / "declaration.json"), sha256=declared_sha)
            or e["build_seal"] != dict(path=str(OUT / "seal.json"), sha256=expected_seal)):
        raise ValueError("actual Root exit-zero evidence must bind this exact source/declaration/build seal")
    stdout = terminal_file(e["full_stdout"]["path"], e["full_stdout"]["sha256"])
    stdout_pin = dict(path=str(stdout), sha256=digest(stdout))
    if stdout == receipt or e["full_stdout"] != stdout_pin:
        raise ValueError("full actual stdout must be a separately retained regular file")
    returned = strict_terminal_json(stdout)
    tail = {key: returned[key] for key in TAIL_FIELDS}
    if returned != dict(result=sealed_result, **tail) or any(e[key] != tail[key] for key in TAIL_FIELDS):
        raise ValueError("full actual stdout, sealed result and Root terminal-tail values differ")
    elapsed, retained_bytes, snapshot = tail["actual_elapsed_seconds"], tail["actual_archive_bytes"], tail["actual_resources"]
    actual_bytes = archive_bytes()
    if (tail["actual_tail_check"] != "PASS" or type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not sealed_result["elapsed_seconds"] <= elapsed < TOTAL_WALL
            or type(retained_bytes) is not int or not 0 <= retained_bytes < ARCHIVE_RESERVE or retained_bytes != actual_bytes
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["artifact_budget_bytes"] != 96 * 2**30 or snapshot["min_free_bytes"] != 8 * 2**30
            or snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != d["resource_scope_contract"]
            or snapshot["declared_resource_roots"] != d["resource_roots"]
            or type(snapshot["resource_roots"]) is not list
            or not set(d["resource_roots"]).issubset(snapshot["resource_roots"])
            or type(snapshot["artifact_bytes"]) is not int
            or not retained_bytes <= snapshot["artifact_bytes"] <= d["artifact_budget_bytes"]
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < d["min_free_bytes"]
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float) or not math.isfinite(snapshot["checked_unix"])
            or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete terminal-tail wall/archive/resource gates must hold")
    validate_history_roots(snapshot["resource_roots"], ART)
    return dict(receipt=dict(path=str(receipt), sha256=digest(receipt)), full_stdout=stdout_pin,
                command=command, schema=TERMINAL_SCHEMA, **tail)


def production_admission(build_seal_sha, terminal_evidence, terminal_evidence_sha256):
    """Future read-only runtime input admission, with no AAA/ABA launch."""
    if not re.fullmatch(r"[0-9a-f]{64}", build_seal_sha or ""):
        raise ValueError("the actual new rank-one-cache build seal hash is mandatory")
    seal = read(require(OUT / "seal.json", build_seal_sha))
    if seal["schema"] != "AXMAT_RANK1_FACTOR_CACHE_BUILD_SEAL_V1":
        raise ValueError("the actual complete new rank-one-cache build seal is required")
    actual = {}
    for root, folders, names in os.walk(OUT, followlinks=False):
        if any((Path(root) / name).is_symlink() for name in [*folders, *names]):
            raise ValueError("the final sealed build namespace may contain no symlinks")
        for name in names:
            path = require(Path(root) / name)
            actual[str(path.relative_to(OUT))] = digest(path)
    if set(actual) != set(seal["files"]) | {"seal.json"} or any(actual[name] != sha for name, sha in seal["files"].items()):
        raise ValueError("every final raw/control/watch/binary file must belong to the exact successful sealed namespace")
    declared_sha = digest(OUT / "declaration.json")
    d = declaration_admission(declared_sha, require_build_interpreter=False)
    result = read(require(OUT / "driver_result.json"))
    audit = read(require(OUT / "audit/result.json"))
    flags = ("rank1_factor_cache_controls_passed", "all_new_cache_outputs_bitwise_equal_to_uncached",
        "operator_identity_guard_negative_controls_passed", "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required")
    if (result["classification"] != "COMPLETE_RANK1_FACTOR_CACHE_BUILD_CONTROLS_ONLY" or result["error"] is not None
            or audit["classification"] != "PASS_RANK1_FACTOR_CACHE_BUILD_CONTROLS_ONLY"
            or audit["declaration_sha256"] != declared_sha or audit["control_status"] != "PASS" or audit["binary_status"] != "PASS"
            or any(audit[key] is not True for key in flags)
            or audit["inherited_moment_order_admission"] != d["inherited_moment_order_admission"]
            or audit["actual_failed_cold_AAA_evidence"] != d["actual_failed_cold_AAA_evidence"]
            or audit["future_actual_factor_cache_observer_required"] != cache_observer_contract()
            or audit["inherited_moment_order_controls_not_newly_executed"] is not True
            or audit["newly_executed_original_interface_receiver_calls"] != 0
            or audit["newly_executed_native_receiver_calls"] != result["control_counts"]["actual_total_unit_kernel_invocations"]
            or result["actual_full_FLU_entry_executed"] is not False or audit["actual_full_FLU_entry_executed"] is not False
            or any(result[key] is not False or audit[key] is not False for key in ("transport_launched", "AAA_accuracy_qualified", "ABA_admitted"))
            or result["rank1_factor_cache_budget_bytes"] != 536870912
            or result["runtime_sha256"] != digest(OUT / "runtime/Dragon")
            or result["control_counts"] != audit["control_counts"]):
        raise ValueError("only complete raw cache controls and genuine compiled overrides may admit this runtime as an input")
    controls = control_audit(d)
    if controls != read(OUT / "audit/controls.json") or controls["counts"] != result["control_counts"]:
        raise ValueError("actual full raw finite/bitwise/coverage/allocation audit differs from its sealed result")
    binary = read(require(OUT / "audit/binary_identity.json"))
    if (binary["status"] != "PASS" or binary["source_and_command_identity_verified"] is not True
            or binary["exact_parent_link_inverse_restoration"] is not True
            or binary["actual_private_object_definitions_verified"] is not True
            or binary["executable_definitions_verified"] is not True):
        raise ValueError("actual normal compiled-source/object/link provenance is required")
    for value in [*binary["raw_metadata"].values(), *binary["actual_objects"].values()]:
        require(value["path"], value["sha256"])
    identity = read(require(OUT / "runtime/build_identity.json"))
    if (identity["sole_new_production_overrides"] != ["SPOT1P64.o", "FLU2DR64.o"]
            or identity["inherited_Flu_override"] != pin(PARENT / "build/FLU.o")):
        raise ValueError("the actual compiled 15/16 selector object and sole new override set must remain exact")
    helper().verify({str(OUT / name):sha for name,sha in identity["files"].items()})
    stages = read(require(OUT / FAMILY / "stages.json"))["stages"]
    if (len(stages) != len(stage_labels(d)) or [row["label"] for row in stages] != stage_labels(d)
            or [row["command"] for row in stages] != stage_commands(d, declared_sha)
            or any(row["status"] != "PASS" for row in stages)):
        raise ValueError("all actual original serial guarded build/control/audit stages must pass once")
    watches = [check_watch(row) for row in stages]
    if watches != result["watchdogs"] or watches[:-1] != audit["previous_stage_watchdogs"]:
        raise ValueError("actual final watchdogs must match both independent child and parent verification")
    terminal = external_terminal_admission(d, declared_sha, build_seal_sha, result,
        terminal_evidence, terminal_evidence_sha256)
    # Admit the current complete family history, including legitimate future
    # family roots, without introducing a changing snapshot into this immutable
    # runtime identity that a consuming pipeline must compare exactly.
    resources_for(d["resource_roots"]).check()
    prior = d["inherited_moment_order_admission"]
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1",
        admission="RANK1_FACTOR_CACHE_RUNTIME_INPUT_ONLY", build_root=str(OUT), source_root=str(SOURCE),
        build_seal_sha256=build_seal_sha, corrected_runtime=pin(OUT / "runtime/Dragon"),
        source_admission=pin(SOURCE / "source_admission.json"),
        inherited_moment_order_admission=prior, actual_failed_cold_AAA_evidence=d["actual_failed_cold_AAA_evidence"],
        actual_external_terminal_evidence=terminal["receipt"], actual_external_terminal_validation=terminal,
        future_contract=prior["future_contract"], capture_dependency=prior["capture_dependency"],
        source_and_receiver_controls=prior["source_and_receiver_controls"],
        source_and_receiver_controls_inherited_not_newly_executed=True,
        dispatch_evidence=prior["dispatch_evidence"], predecessor=prior,
        inherited_selector_and_source_unit_controls=dict(compiled_selector=prior["compiled_selector"],
            compiled_unit_controls=prior["compiled_unit_controls"], rows=112, selector_invocations=224,
            source_unit_invocations=192, actual_native_receiver_calls=14, newly_executed=False),
        compiled_selector=prior["compiled_selector"], compiled_unit_controls=pin(OUT / "audit/controls.json"),
        compiled_cache_identity=pin(OUT / "audit/binary_identity.json"),
        actual_control_rows=prior["actual_control_rows"], actual_selector_invocations=prior["actual_selector_invocations"],
        actual_source_unit_invocations=prior["actual_source_unit_invocations"],
        inherited_native_receiver_calls=14, newly_executed_original_interface_receiver_calls=0,
        newly_executed_native_receiver_calls=controls["counts"]["actual_total_unit_kernel_invocations"],
        cache_unit_control_counts=controls["counts"], inherited_moment_order_controls_not_newly_executed=True,
        rank1_factor_cache_controls_passed=True, all_new_cache_outputs_bitwise_equal_to_uncached=True,
        operator_identity_guard_negative_controls_passed=True, rank1_factor_cache_math_and_rhs_order_unchanged=True,
        rank1_factor_cache_budget_bytes=536870912, fresh_cold_AAA_required=True,
        future_actual_factor_cache_observer_required=cache_observer_contract(),
        future_actual_FLU_observer_required=prior["future_actual_FLU_observer_required"],
        future_bounded_progress_observer=dict(prefix="AXMAT-RANK1-CACHE PROGRESS ",
            columns=["IT", "JT", "IGDEB", "EINN", "builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes"],
            frequency="First and every 32nd completed inner iteration, ordinary rank-one built pool only",
            scientific_gate=False, iteration_algorithm_and_IPRT_unchanged=True),
        corrected_sender_retained=True, white_closure_unchanged=True, collision_self_operator_unchanged=True,
        angle_grid_unchanged=True, radial_arithmetic_unchanged=True, physical_data_unchanged=True,
        original_accuracy_thresholds_changed=False, no_CE_fitting=True,
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=d["resource_scope_contract"],
        current_complete_history_admission_required=True,
        inherited_physical_flags_scope="Actual completed source-factor/moment-order input controls; no new transport or CE qualification",
        actual_full_FLU_entry_executed=False, full_FLU_entry_execution_proved_by_build=False,
        production_pipeline_prepared=False, AAA_accuracy_qualified=False, ABA_admitted=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare-build", "run-build", "audit-build", "admit"))
    parser.add_argument("--moment-order-build-seal-sha256")
    parser.add_argument("--moment-order-terminal-evidence")
    parser.add_argument("--moment-order-terminal-evidence-sha256")
    parser.add_argument("--failed-cold-terminal-evidence-sha256")
    parser.add_argument("--patch-helper-sha256")
    parser.add_argument("--controls-source-sha256")
    parser.add_argument("--sha256")
    parser.add_argument("--terminal-evidence")
    parser.add_argument("--terminal-evidence-sha256")
    args = parser.parse_args()
    {"prepare-build": lambda: prepare_build(args.moment_order_build_seal_sha256, args.moment_order_terminal_evidence,
        args.moment_order_terminal_evidence_sha256, args.failed_cold_terminal_evidence_sha256,
        args.patch_helper_sha256, args.controls_source_sha256),
     "run-build": lambda: run_build(args.sha256), "audit-build": lambda: audit_build(args.sha256),
     "admit": lambda: print(json.dumps(production_admission(args.sha256, args.terminal_evidence,
        args.terminal_evidence_sha256), allow_nan=False))}[args.action]()
