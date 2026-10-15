"""Declare a fresh complete AAA trial using the sealed 1D source-factor fix.

This factory copies the actual environment-pinned production pipeline. It does
not mutate a frozen module's globals or __file__. Its only receiver changes are
explicit SHA bindings and extra source-factor admission. Offline producer
replays, raw BOOT ingress, geometry, basis, decks, iteration and scientific gates
are retained. 'declare' and 'prepare' never start transport; 'run-AAA' hands over
to the unchanged serial production controller for fresh training/bootstrap/maps.
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
import platform
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
OLD = ART / "axial-material-production-qualified-AB-white-trace-refined-envpin-20261005"
PARENT_SOURCE = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"
SOURCE = ART / "axial-material-qualified-AB-source-factor-admission-20261006"
OUTPUT = ART / "axial-material-production-qualified-AB-source-factor-20261006"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_source_factor_production.py"
BUILD = ART / "axial-material-source-factor-build-20261006"
CAPTURE = ART / "axial-material-AAA-production-angular-capture-20261006"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
PREPARED_SHA = "024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53"
CAPTURE_SEAL = "16f67ec74e41d3282a7e90fe342e0165c81a8fb97a6cfc1cd72615e6a9ac9c0a"
OLD_RUNTIME_SHA = "51b2d3ff947daa3ea523932bcc28276b054632f0bfc6cf76fa21ac458a4f7be4"
EXPERIMENT = "axial-material-qualified-AB-rank1-source-factor-20261006"
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
UNCHANGED_NAMES = ("production_inputs.py", "snapshot_control_preflight.py", "white_receiver_tracking.py",
    "analyze_r64_snapshot.py", "analyze_r64_tracking_moments.py", "check_r64_audit_rejections.py",
    "check_r64_normalization_rejections.py")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, wanted=None):
    path = Path(path)
    if not path.is_file() or (wanted is not None and digest(path) != wanted):
        raise ValueError("missing or changed source-factor pipeline dependency: " + str(path))
    return path


def pin(path):
    path = require(path).resolve()
    return dict(path=str(path), sha256=digest(path))


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, require(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != Path(path).resolve():
        raise ValueError("actual imported source path differs")
    return module


def producer_environment():
    import numpy as np
    old_info = read(require(OLD / "prepared.json", PREPARED_SHA))
    path = require(PARENT_SOURCE / "analysis_environment.json")
    env = read(path)
    if (env["schema"] != "AXMAT_EXACT_OFFLINE_REPLAY_ENVIRONMENT_V1"
            or env["python_version"] != "3.14.4" or env["numpy_version"] != "2.4.4"
            or str(Path(sys.executable).resolve()) != env["executable"]
            or platform.python_version() != env["python_version"] or np.__version__ != env["numpy_version"]
            or str(Path(np.__file__).parent.resolve()) != env["numpy_root"]
            or any(os.environ.get(k) != "1" for k in THREADS)):
        raise ValueError("original exact offline producer Python3.14.4/NumPy2.4.4 and single threads required")
    verify(env["files"])
    for name, wanted in old_info["local_files"].items():
        require(OLD / name, wanted)
    for item in old_info["inputs"].values():
        require(item["path"], item["sha256"])
    for key in ("case_spec", "rank_addendum"):
        require(old_info[key]["path"], old_info[key]["sha256"])
    return old_info, env, path


def restore_metadata(candidate, parent, allowed, added=()):
    restored = copy.deepcopy(candidate)
    for keys in allowed:
        a, b = restored, parent
        for key in keys[:-1]:
            a, b = a[key], b[key]
        a[keys[-1]] = b[keys[-1]]
    for keys in added:
        a = restored
        for key in keys[:-1]:
            a = a[key]
        del a[keys[-1]]
    if restored != parent:
        raise ValueError("pipeline metadata changed outside explicit source/runtime identity fields")


def patched(original, replacements, target, allowed_functions=()):
    result = original
    for old, new in replacements:
        if result.count(old) != 1:
            raise ValueError("pipeline source anchor absent or ambiguous: " + old[:120])
        result = result.replace(old, new, 1)
    restored = result
    for old, new in reversed(replacements):
        if restored.count(new) != 1:
            raise ValueError("pipeline source restoration anchor is ambiguous")
        restored = restored.replace(new, old, 1)
    if restored != original:
        raise ValueError("source changed outside explicit admission additions")
    def definitions(text):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body
                if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    before, after = definitions(original), definitions(result)
    if (before.keys() != after.keys()
            or any(before[k] != after[k] for k in before if k not in allowed_functions)):
        raise ValueError("unlisted pipeline function or supervision/scientific gate changed")
    target.write_text(result)
    target.with_suffix(target.suffix + ".patch").write_text("".join(difflib.unified_diff(
        original.splitlines(True), result.splitlines(True),
        fromfile="frozen-actual-production-runtime", tofile="explicit-source-factor-admission")))
    return dict(candidate=pin(target), original_sha256=hashlib.sha256(original.encode()).hexdigest(),
        replacements=replacements, full_text_restored_byte_exact=True,
        unchanged_function_AST=sorted(set(before) - set(allowed_functions)),
        admitted_function_changes=list(allowed_functions))


ADMISSION_HOST = '''"""Explicit admission of a separately sealed 1D source-factor runtime."""
import copy
import hashlib
import json
from pathlib import Path

EXPECTED_BUILD_ROOT = __BUILD_ROOT__
EXPECTED_BUILD_SEAL = __BUILD_SEAL__
EXPECTED_RUNTIME_SHA = __RUNTIME_SHA__
EXPECTED_PARENT_PREPARED_SHA = __PREPARED_SHA__


def require(path, wanted):
    path = Path(path)
    with path.open("rb") as stream:
        observed = hashlib.file_digest(stream, "sha256").hexdigest()
    if observed != wanted:
        raise ValueError("source-factor admission dependency changed: " + str(path))
    return path


def metadata(item):
    path = require(item["path"], item["sha256"])
    local = require(Path(__file__).with_name("source_factor_admission.json"), item["sha256"])
    data = json.loads(local.read_text())
    if (data["schema"] != "AXMAT_SOURCEFACTOR_COUPLING_ADMISSION_V1"
            or data["build_admission"]["schema"] != "AXMAT_SOURCEFACTOR_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or data["build_admission"]["build_root"] != EXPECTED_BUILD_ROOT
            or data["build_admission"]["build_seal_sha256"] != EXPECTED_BUILD_SEAL
            or data["build_admission"]["corrected_runtime"]["sha256"] != EXPECTED_RUNTIME_SHA
            or data["parent_prepared"]["sha256"] != EXPECTED_PARENT_PREPARED_SHA
            or data["source_fix_scope"] != "Only SPOT NDIM1 off-diagonal group raw Legendre source moments; two alternative sender branches."
            or any(data[k] is not True for k in ("physical_inputs_unchanged", "common_training_unchanged",
                "white_closure_unchanged", "radial_arithmetic_unchanged", "collision_self_operator_unchanged",
                "original_controls_and_gates_unchanged", "fresh_training_bootstrap_and_maps_required",
                "reference_reassessment_pending", "old_reference_recipe_is_dependency_only",
                "new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required"))
            or any(data[k] is not False for k in ("old_moment_closure_numerical_replay_claimed",
                "CE_fitting", "reference_qualification_created", "AAA_accuracy_qualified", "ABA_admitted"))):
        raise ValueError("explicit limited source-factor admission contract differs")
    for name, wanted in data["files"].items():
        require(name, wanted)
    root = Path(EXPECTED_BUILD_ROOT)
    seal = json.loads(require(root / "seal.json", EXPECTED_BUILD_SEAL).read_text())
    if {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} != set(seal["files"]) | {"seal.json"}:
        raise ValueError("complete source-factor build seal namespace changed")
    for name,wanted in seal["files"].items():
        require(root / name,wanted)
    driver = json.loads((root / "driver_result.json").read_text())
    audit = json.loads((root / "audit/result.json").read_text())
    if (driver["classification"] != "COMPLETE_SOURCEFACTOR_BUILD_AND_INTERFACE_CONTROLS_ONLY"
            or driver["error"] is not None or audit["source_control_status"] != "PASS"
            or audit["interface_control_status"] != "PASS"):
        raise ValueError("actual completed compiled source/receiver controls required")
    return data


def admit_source_factor_variant(variant):
    revision = variant.get("source_factor_revision", {})
    data = metadata(revision["admission"])
    if (variant["candidate_runtime"] != data["build_admission"]["corrected_runtime"]
            or revision.get("fresh_complete_coupling_required") is not True
            or revision.get("physical_inputs_changed") is not False
            or revision.get("white_closure_changed") is not False
            or revision.get("original_thresholds_changed") is not False):
        raise ValueError("new runtime variant differs from source-factor build admission")
    parent_item = data["parent_variant"]
    parent = json.loads(require(parent_item["path"], parent_item["sha256"]).read_text())
    restored = copy.deepcopy(variant)
    for key in ("candidate_runtime", "files"):
        restored[key] = parent[key]
    del restored["source_factor_revision"]
    if restored != parent:
        raise ValueError("original layout, white-trace operator or parent admissions changed")
    return dict(status="PASS_SEALED_SOURCEFACTOR_RUNTIME_INPUT_ONLY", scientific_qualification=False)


def admit_source_factor_receiver(receipts, resolved, spec):
    data = metadata(receipts["source_factor_revision"])
    if receipts["online_receiver_sha256"] != EXPECTED_RUNTIME_SHA:
        raise ValueError("new receiver identity is not the independently controlled runtime")
    old_item = data["parent_producer_receipt"]
    old = json.loads(require(old_item["path"], old_item["sha256"]).read_text())
    restored = copy.deepcopy(receipts)
    for key in ("online_receiver_sha256", "conditional_white_receiver_variant", "scope"):
        restored[key] = old[key]
    del restored["source_factor_revision"]
    if restored != old:
        raise ValueError("original offline producer, payload, mirror or training records changed")
    for name, pin in data["original_inputs"].items():
        if name != "material_results" and resolved[name] != pin:
            raise ValueError("physical/material input changed: " + name)
    if (spec["production"]["groups"] != 370 or spec["production"]["scat"] != 3
            or spec["production"]["sn"] != 32 or spec["geometry"]["cells_per_zone"] != 16
            or spec["basis"]["requested_rank"] != 1 or spec["basis"]["training_slots"] != list("ABA")):
        raise ValueError("source-factor runtime cannot substitute a proxy geometry or training set")
    return dict(status="PASS_SAME_OFFLINE_PRODUCERS_AND_LEGACY_BOOT_INPUTS", source_fix_is_online_only=True)
'''


def declare(build_seal_sha):
    info, producer_env, env_path = producer_environment()
    builder = load(BUILD_FACTORY, "source_factor_build_dependency")
    admitted = builder.production_admission(build_seal_sha)
    if (admitted["schema"] != "AXMAT_SOURCEFACTOR_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or Path(admitted["build_root"]).resolve() != BUILD
            or admitted["capture_dependency"]["seal_sha256"] != CAPTURE_SEAL
            or any(admitted[k] is not True for k in ("white_closure_unchanged",
                "collision_self_operator_unchanged", "angle_grid_unchanged", "physical_data_unchanged"))):
        raise ValueError("actual sealed capture and bounded build/control admission required")
    contract = admitted["future_contract"]
    if (contract["original_prepared"] != pin(OLD / "prepared.json")
            or contract["production_config"] != info["production_config"]
            or contract["budgets"] != info["budgets"] or contract["inputs"] != info["inputs"]
            or contract["retained_reference"]["active_batches"] != 2000
            or contract["retained_reference"]["active_statepoints"] != [
                f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)]
            or contract["producer_environment"]["path"] != str(env_path)
            or contract["producer_environment"]["sha256"] != digest(env_path)):
        raise ValueError("original production input/configuration/budget and full reference contract required")
    runtime = admitted["corrected_runtime"]
    require(runtime["path"], runtime["sha256"])
    parent_variant = read(OLD / "runtime/conditional_white_receiver_variant.json")
    parent_receipt = read(info["inputs"]["material_results"]["path"])
    parent_spec = read(info["case_spec"]["path"])
    parent_resource_addendum = parent_spec["conditional_white_trace_trial"]["resource_addendum"]
    parent_resource = read(require(parent_resource_addendum["path"], parent_resource_addendum["sha256"]))
    if (parent_spec["resource_caps"]["new_case_artifact_budget_GiB"] != 96
            or parent_spec["resource_caps"]["disk_min_free_GiB"] != 8
            or parent_resource["prior_storage_budget_GiB"] != 40
            or parent_resource["new_storage_budget_GiB"] != 96 or parent_resource["min_free_GiB"] != 8):
        raise ValueError("actual complete-history 96 GiB/free8 GiB production specification required")
    parent_declaration = read(OLD / "declaration.json")
    if parent_declaration["production_config"] != info["production_config"] or parent_declaration["budgets"] != info["budgets"]:
        raise ValueError("actual parent declaration differs from sealed preparation")
    roots = sorted(set(info["resource_roots"]) | set(read(BUILD / "declaration.json")["resource_roots"])
        | set(read(FULL / "declaration.json")["resource_roots"])
        | set(read(CAUSAL / "declaration.json")["resource_roots"])
        | {str(p.resolve()) for p in ART.glob("axial-material-*") if p.is_dir()} | {str(SOURCE), str(OUTPUT)})
    sys.path.insert(0, str(OLD / "runtime"))
    controller = load(OLD / "runtime/production_runner.py", "source_factor_parent_controller")
    resources = controller.DiskResources(ART, roots, 8 * 2**30, 96 * 2**30)
    before = resources.check()
    parent_bytes = sum(p.stat().st_size for p in OLD.rglob("*") if p.is_file() and not p.is_symlink())
    # AAA is the presently executable case. Later ABA remains independently
    # gated and must receive a fresh storage admission after its CE guard.
    reserve = math.ceil(1.5 * parent_bytes) + 2**30
    if before["artifact_bytes"] + reserve >= 96 * 2**30 or before["disk_free_bytes"] - reserve < 8 * 2**30:
        raise ValueError("fresh complete AAA reservation exceeds unchanged history/free-space caps")
    SOURCE.mkdir(exist_ok=False)
    source_proofs = {}
    for name in UNCHANGED_NAMES:
        shutil.copy2(OLD / "runtime" / name, SOURCE / name)
        if digest(SOURCE / name) != digest(OLD / "runtime" / name):
            raise ValueError("unchanged pipeline component copy differs")
    shutil.copy2(env_path, SOURCE / "analysis_environment.json")
    generated_host = ADMISSION_HOST
    for token, value in [("__BUILD_ROOT__", str(BUILD)), ("__BUILD_SEAL__", build_seal_sha),
                         ("__RUNTIME_SHA__", runtime["sha256"]), ("__PREPARED_SHA__", PREPARED_SHA)]:
        if generated_host.count(token) != 1:
            raise ValueError("admission template token is ambiguous")
        generated_host = generated_host.replace(token, repr(value), 1)
    (SOURCE / "source_factor_admission.py").write_text(generated_host)
    original_runner = (OLD / "runtime/production_runner.py").read_bytes().decode("utf-8")
    anchor = '    shutil.copy2(Path(__file__).with_name("numerical_layout_admission.py"), runtime / "numerical_layout_admission.py")'
    runner_changes = [('DRAGON_SHA = "' + OLD_RUNTIME_SHA + '"', 'DRAGON_SHA = "' + runtime["sha256"] + '"'),
        (anchor, anchor + '\n    shutil.copy2(Path(__file__).with_name("source_factor_admission.py"), runtime / "source_factor_admission.py")'
         '\n    shutil.copy2(Path(__file__).with_name("source_factor_admission.json"), runtime / "source_factor_admission.json")')]
    source_proofs["production_runner.py"] = patched(original_runner, runner_changes,
        SOURCE / "production_runner.py", ("prepare",))
    original_ingestion = (OLD / "runtime/qualified_snapshot_ingestion.py").read_bytes().decode("utf-8")
    ingestion_changes = [("ONLINE_SHA = '" + OLD_RUNTIME_SHA + "'", "ONLINE_SHA = '" + runtime["sha256"] + "'"),
        ('def admit_snapshots(receipts, resolved, spec):\n',
         'def admit_snapshots(receipts, resolved, spec):\n'
         '    from source_factor_admission import admit_source_factor_receiver\n'
         '    admit_source_factor_receiver(receipts, resolved, spec)\n')]
    source_proofs["qualified_snapshot_ingestion.py"] = patched(original_ingestion, ingestion_changes,
        SOURCE / "qualified_snapshot_ingestion.py", ("admit_snapshots",))
    original_layout = (OLD / "runtime/numerical_layout_admission.py").read_bytes().decode("utf-8")
    layout_changes = [('def admit_layout_variant(variant):\n', 'def admit_layout_variant(variant):\n'
        '    from source_factor_admission import admit_source_factor_variant\n'
        '    admit_source_factor_variant(variant)\n')]
    source_proofs["numerical_layout_admission.py"] = patched(original_layout, layout_changes,
        SOURCE / "numerical_layout_admission.py", ("admit_layout_variant",))
    write_new(SOURCE / "source_equivalence.json", dict(
        schema="AXMAT_SOURCEFACTOR_PIPELINE_SOURCE_EQUIVALENCE_V1", patches=source_proofs,
        unchanged_files={name: dict(parent=pin(OLD / "runtime" / name), candidate=pin(SOURCE / name)) for name in UNCHANGED_NAMES},
        original_offline_replay_body_restored_exactly=True, original_native_ingress_body_restored_exactly=True,
        original_layout_body_restored_exactly=True, production_config_and_deck_generator_byte_exact=True,
        run_and_qualify_ABA_and_serial_supervision_AST_exact=True, frozen_module_identity_reassigned=False,
        existing_pipeline_sources_changed=False, candidate_output_numerical_replay_to_old_closure_claimed=False))
    build_seal = read(require(BUILD / "seal.json", build_seal_sha))
    dependencies = {str(BUILD / name): sha for name, sha in build_seal["files"].items()}
    dependencies.update(parent_variant["files"])
    dependencies.update({str(p): digest(p) for p in [Path(__file__).resolve(), BUILD_FACTORY, BUILD / "seal.json",
        CAPTURE / "seal.json", OLD / "prepared.json", OLD / "declaration.json", env_path,
        FULL / "declaration.json", CAUSAL / "declaration.json",
        Path(contract["reference_analysis_recipe"]["path"]),
        Path(parent_resource_addendum["path"]),
        Path(info["case_spec"]["path"]), Path(info["inputs"]["material_results"]["path"]),
        OLD / "runtime/conditional_white_receiver_variant.json", *[p for p in SOURCE.iterdir() if p.is_file()]]})
    verify(dependencies)
    write_new(SOURCE / "source_factor_admission.json", dict(
        schema="AXMAT_SOURCEFACTOR_COUPLING_ADMISSION_V1", build_admission=admitted, files=dependencies,
        parent_prepared=pin(OLD / "prepared.json"), parent_variant=pin(OLD / "runtime/conditional_white_receiver_variant.json"),
        parent_producer_receipt=pin(info["inputs"]["material_results"]["path"]), original_inputs=info["inputs"],
        producer_environment=pin(SOURCE / "analysis_environment.json"), reference_analysis_recipe=contract["reference_analysis_recipe"],
        source_fix_scope="Only SPOT NDIM1 off-diagonal group raw Legendre source moments; two alternative sender branches.",
        physical_inputs_unchanged=True, common_training_unchanged=True, white_closure_unchanged=True,
        radial_arithmetic_unchanged=True, collision_self_operator_unchanged=True,
        original_controls_and_gates_unchanged=True, fresh_training_bootstrap_and_maps_required=True,
        reference_reassessment_pending=True, old_reference_recipe_is_dependency_only=True,
        new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required=True,
        reference_qualification_created=False,
        old_moment_closure_numerical_replay_claimed=False, CE_fitting=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    admission = pin(SOURCE / "source_factor_admission.json")
    variant = copy.deepcopy(parent_variant)
    variant.update(candidate_runtime=runtime, source_factor_revision=dict(admission=admission,
        fresh_complete_coupling_required=True, physical_inputs_changed=False,
        white_closure_changed=False, original_thresholds_changed=False,
        old_moment_closure_numerical_replay_claimed=False))
    variant["files"].update(dependencies)
    variant["files"][admission["path"]] = admission["sha256"]
    write_new(SOURCE / "conditional_white_receiver_variant.json", variant)
    receipt = copy.deepcopy(parent_receipt)
    receipt.update(online_receiver_sha256=runtime["sha256"],
        conditional_white_receiver_variant=pin(SOURCE / "conditional_white_receiver_variant.json"),
        source_factor_revision=admission,
        scope="Same audited A/B offline producer archives and exact REAL32 BOOT mirror. Only the online SPOT 1D "
              "off-diagonal group Legendre source multiplier changes; all fixed-point and independent gates remain mandatory.")
    restore_metadata(receipt, parent_receipt, [(k,) for k in (
        "online_receiver_sha256", "conditional_white_receiver_variant", "scope")], [("source_factor_revision",)])
    write_new(SOURCE / "producer_ingestion_receipt.json", receipt)
    spec = copy.deepcopy(parent_spec)
    spec.update(experiment_id=EXPERIMENT, status="PREDECLARED_SOURCEFACTOR_FULL_COUPLED_TRIAL")
    spec["production"]["implementation"] = "Same production physics/layout/white/radial arithmetic; correct SPOT NDIM1 off-diagonal source factor only; SHA256 " + runtime["sha256"]
    spec["qualified_snapshot_producers"].update(receiver_sha256=runtime["sha256"],
        receipt=pin(SOURCE / "producer_ingestion_receipt.json"))
    spec["conditional_white_trace_trial"]["variant"] = pin(SOURCE / "conditional_white_receiver_variant.json")
    spec["source_factor_trial"] = dict(admission=admission, fresh_complete_coupling_required=True,
        reused_training_or_bootstrap_or_maps=False, white_trace_K_changed=False, original_four_thresholds_changed=False,
        original_independent_eight_gates_required=True, complete_original_2000_active_reference_batches_required=True,
        reference_reassessment_pending=True, old_reference_recipe_is_dependency_only=True,
        new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required=True,
        reference_qualification_created=False,
        old_AAA_outputs_are_not_equivalent=True, CE_fitting=False)
    restore_metadata(spec, parent_spec, [("experiment_id",), ("status",), ("production", "implementation"),
        ("qualified_snapshot_producers", "receiver_sha256"), ("qualified_snapshot_producers", "receipt"),
        ("conditional_white_trace_trial", "variant")], [("source_factor_trial",)])
    write_new(SOURCE / "case_spec.json", spec)
    rank = read(info["rank_addendum"]["path"])
    parent_rank = copy.deepcopy(rank)
    rank.update(experiment_id=EXPERIMENT, case_spec_sha256=digest(SOURCE / "case_spec.json"))
    restore_metadata(rank, parent_rank, [("experiment_id",), ("case_spec_sha256",)])
    write_new(SOURCE / "rank_addendum.json", rank)
    write_new(SOURCE / "resource_admission.json", dict(
        schema="AXMAT_SOURCEFACTOR_FRESH_AAA_STORAGE_ADMISSION_V1", resources_before=before,
        parent_resource_addendum=parent_resource_addendum, initial_history_cap_GiB=40,
        inherited_complete_history_cap_GiB=96, inherited_free_floor_GiB=8,
        resource_roots=roots, complete_history_scope_extended_to_new_family=True,
        unchanged_history_cap_bytes=96 * 2**30, unchanged_min_free_bytes=8 * 2**30,
        original_complete_12_map_case_bytes=parent_bytes, fresh_AAA_reserve_bytes=reserve,
        forecast_bytes=before["artifact_bytes"] + reserve, original_case_budgets=info["budgets"],
        original_max_maps=100, planning_previous_maps=12, complete_native_convergence_required=True,
        retries=0, threads=1, numeric_children_at_once=1,
        later_ABA_requires_fresh_storage_check=True, resource_caps_changed=False))
    write_new(SOURCE / "input_and_gate_equivalence.json", dict(
        schema="AXMAT_SOURCEFACTOR_INPUT_AND_GATE_EQUIVALENCE_V1", parent_case_spec=pin(info["case_spec"]["path"]),
        candidate_case_spec=pin(SOURCE / "case_spec.json"), all_unlisted_spec_fields_exact=True,
        physical_material_snapshot_and_tracking_input_descriptors_exact=True,
        producer_receipt_restore_to_parent_exact=True, production_config=info["production_config"], budgets=info["budgets"],
        four_thresholds=dict(radial=2.5e-7, axial=5e-8, MCCG=2.5e-8, coupled_outer=5e-7),
        fresh_common_ABA_training_and_cold_bootstrap_and_full_maps=True,
        complete_independent_reference_recipe=contract["reference_analysis_recipe"],
        reference_reassessment_pending=True, old_reference_recipe_is_dependency_only=True,
        new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required=True,
        reference_qualification_created=False,
        original_2000_batch_history_mandatory=True, producer_environment=pin(SOURCE / "analysis_environment.json"),
        source_equivalence=pin(SOURCE / "source_equivalence.json"),
        old_source_moment_closure_numerical_replay_claimed=False, AAA_accuracy_qualified=False, ABA_admitted=False))
    declaration = copy.deepcopy(parent_declaration)
    declaration.update(experiment_id=EXPERIMENT, case_spec=pin(SOURCE / "case_spec.json"),
        rank_addendum=pin(SOURCE / "rank_addendum.json"), resource_roots=roots,
        conditional_white_receiver_variant=pin(SOURCE / "conditional_white_receiver_variant.json"),
        helper=pin(Path(__file__).resolve()), source_factor_revision=admission,
        source_factor_equivalence=pin(SOURCE / "input_and_gate_equivalence.json"),
        source_factor_resource_admission=pin(SOURCE / "resource_admission.json"))
    declaration["inputs"]["material_results"] = pin(SOURCE / "producer_ingestion_receipt.json")
    restore_metadata(declaration, parent_declaration, [("experiment_id",), ("case_spec",), ("rank_addendum",),
        ("resource_roots",), ("conditional_white_receiver_variant",), ("helper",), ("inputs", "material_results")],
        [("source_factor_revision",), ("source_factor_equivalence",), ("source_factor_resource_admission",)])
    write_new(SOURCE / "declaration.json", declaration)
    write_new(SOURCE / "factory_seal.json", dict(schema="AXMAT_SOURCEFACTOR_COUPLING_FACTORY_SEAL_V1",
        files={p.name: digest(p) for p in SOURCE.iterdir() if p.is_file()}))
    print(json.dumps(dict(classification="DECLARED_SOURCEFACTOR_FULL_AAA_NOT_RUN",
        declaration=pin(SOURCE / "declaration.json"), output=str(OUTPUT),
        factory_seal=pin(SOURCE / "factory_seal.json"), source_equivalence=pin(SOURCE / "source_equivalence.json"))))


def verify_factory(expected_declaration):
    require(SOURCE / "declaration.json", expected_declaration)
    seal = read(require(SOURCE / "factory_seal.json"))
    if seal["schema"] != "AXMAT_SOURCEFACTOR_COUPLING_FACTORY_SEAL_V1":
        raise ValueError("complete source-factor pipeline source inventory required")
    if {p.name for p in SOURCE.iterdir() if p.is_file()} != set(seal["files"]) | {"factory_seal.json"}:
        raise ValueError("source-factor pipeline source namespace changed")
    verify({str(SOURCE / name): wanted for name, wanted in seal["files"].items()})
    declaration = read(SOURCE / "declaration.json")
    item = declaration["source_factor_revision"]
    metadata = read(require(item["path"], item["sha256"]))
    verify(metadata["files"])
    for key in ("source_factor_equivalence", "source_factor_resource_admission", "case_spec", "rank_addendum",
                "conditional_white_receiver_variant", "helper"):
        item = declaration[key]
        require(item["path"], item["sha256"])
    return declaration


def prepare(expected_declaration):
    producer_environment()
    verify_factory(expected_declaration)
    if OUTPUT.exists():
        raise ValueError("new independent prepared root must be absent; no retry or overwrite")
    # A true process handoff gives the copied factory its own actual __file__ and
    # normal sibling imports. The original controller records/prepares its exact
    # local inventory and performs the unchanged offline numerical admission.
    env = dict(os.environ, **{name: "1" for name in THREADS}, PYTHONDONTWRITEBYTECODE="1")
    python = read(SOURCE / "analysis_environment.json")["executable"]
    os.execve(python, [python, str(SOURCE / "production_runner.py"), "prepare",
        str(SOURCE / "declaration.json"), "--sha256", expected_declaration, str(OUTPUT)], env)


def run_AAA(expected_prepared):
    producer_environment()
    info = read(require(OUTPUT / "prepared.json", expected_prepared))
    verify_factory(info["declaration"]["sha256"])
    if (info["classification"] != "PREPARED_NO_TRANSPORT" or info["experiment_id"] != EXPERIMENT
            or info["production_config"] != read(OLD / "prepared.json")["production_config"]
            or info["budgets"] != read(OLD / "prepared.json")["budgets"]):
        raise ValueError("new original-control cold production preparation required")
    if any((OUTPUT / name).exists() for name in ("AAA", "archives", "training")):
        raise ValueError("fresh complete AAA attempt required; no old training/bootstrap/maps or retry")
    for name, wanted in info["local_files"].items():
        require(OUTPUT / name, wanted)
    env = dict(os.environ, **{name: "1" for name in THREADS}, PYTHONDONTWRITEBYTECODE="1")
    python = read(SOURCE / "analysis_environment.json")["executable"]
    os.execve(python, [python, str(OUTPUT / "runtime/production_runner.py"), "run",
        str(OUTPUT / "prepared.json"), "--sha256", expected_prepared, "--case", "AAA"], env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("declare", "prepare", "run-AAA"))
    parser.add_argument("--sha256", required=True,
        help="Completed build seal for declare; declaration for prepare; prepared file for run-AAA")
    args = parser.parse_args()
    {"declare": lambda: declare(args.sha256), "prepare": lambda: prepare(args.sha256),
     "run-AAA": lambda: run_AAA(args.sha256)}[args.action]()
