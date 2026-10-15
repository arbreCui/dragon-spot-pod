"""Bind actual new moment-order AAA to complete original-gate CE reassessment.

Declaration requires the successful new prepared/status/build identities. It
copies audited scientific sources and records explicit binding-only patches;
preparation writes no observables and launches no computation. The one bounded
run exports the actual saved fine state, repeats its physical identity audit,
retains all fine checks, projects fixed 48-to-12 whole-cell integrals, and reads
all original 2000 active statepoints. Only the unchanged unanimous collector
may emit a new qualification receipt. No module identity is reassigned.
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
import stat
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path("/Users/wen/spot")
ART = ROOT / "validation/artifacts"
PROD = ART / "axial-material-production-qualified-AB-rank1-factor-cache-20261007"
COUPLING = ART / "axial-material-qualified-AB-rank1-factor-cache-admission-20261007"
SOURCE = ART / "axial-material-qualified-AAA-rank1-monitored-input-graph-reference-admission-20261007"
OUT = ART / "axial-material-qualified-AAA-rank1-monitored-input-graph-reference-20261007"
TERMINAL = ART / "axial-material-qualified-AAA-rank1-monitored-input-graph-reference-terminal-20261007"
CE = ART / "axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004"
OLD_SOURCE = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"
BUILD = ART / "axial-material-rank1-factor-cache-build-20261007"
BUILD_TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_production.py"
FULL_FACTORY = ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py"
PHYSICAL = ROOT / "validation/axial_material/review_qualified_AAA_refined_input_identity.py"
EXPORTER = ART / "axial-material-tools-20261003/export_observables"
EXPORT_SOURCE = ROOT / "validation/axial_material/export_observables.f90"
PYTHON = Path("/Users/wen/miniforge3/envs/openmc-dev/bin/python")
BUILD_SOURCE_SHA = "92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a"
COUPLING_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_coupling.py"
COUPLING_FACTORY_SHA = "96e54f36e1939a7edc7d112661c1e44066d7a3e869354a932ad9b967ec0d666d"
TEMPLATE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AAA_source_factor_reference_analysis.py"
TEMPLATE_FACTORY_SHA = "0fc9a674ff7579f8adaa21618cbb3aead028d2e216e7946964c5df90a1b39a99"
FULL_SOURCE_SHA = "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6"
RECIPE_SHA = "56ebbfcc334dc77b1134a218f46a60393503a79bd9b167f2ef2e74aba11e5806"
EXPORTER_SHA = "81da2ac2ea98009181cc54a1ab254c99d1cb362b4e89c468fe7bc44ea14e7524"
EXPORT_SOURCE_SHA = "fdfb6204a9661a38ba120387311136e0eba2959d54bd0bac6b594723b586ee35"
GATES = ("input_equivalence", "source_convergence", "block_stability", "statistical_resolution",
         "keff", "scalar_flux", "nu_fission", "currents_balance_symmetry")
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
TOTAL_WALL, RSS_CAP, RESERVE = 120, 512, 256 * 2**20
LABELS = ("fine/export", "fine/physical", "AAA/project", "AAA/statistics",
          "AAA/currents", "AAA/collect")
TERMINAL_SCHEMA = "AXMAT_RANK1_FACTOR_CACHE_CE_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
TAIL_FIELDS = ("full_closeout_tail_gate", "actual_elapsed_through_full_closeout_seconds",
               "actual_complete_archive_bytes", "resources_after_full_closeout")
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
ARCHIVE_ROOTS = (str(SOURCE), str(OUT))
ARCHIVE_SCOPE = "Combined SOURCE plus OUT apparent regular-file bytes; external TERMINAL remains in the 96GiB axial-family history scope"
GRAPH_HELPER = ROOT / "validation/axial_material/reference_verified_input_graph.py"
SCIENTIFIC_OWNER_HELPER = ROOT / "validation/axial_material/reference_scientific_input_owners.py"
TRANSITIVE_OWNER_HELPER = ROOT / "validation/axial_material/reference_transitive_input_owners.py"
CONSUMER_OWNER_HELPER = ROOT / "validation/axial_material/reference_consumer_input_owners.py"
GRAPH_HELPER_SHA = "a7d4fd313a7de9ecd81a5d656552189d77643f1c4d83bb7702c4dc645edba4b4"
SCIENTIFIC_OWNER_HELPER_SHA = "c590537d17d73669e324d872b6aa67ce79f67e963b980688c7883837bfdf0051"
TRANSITIVE_OWNER_HELPER_SHA = "111027cbfbc57bcdb5513a0802324b0ca84920728cb67a38f45fbf03ce410b67"
CONSUMER_OWNER_HELPER_SHA = "364ff57a87f43b250425da1759709fab334d849a1a4006004b9c584343d1e6af"
CONSUMER_PHASES = ("fine/physical", "AAA/project", "AAA/collect")
CONSUMER_SNAPSHOT_SCOPE = "ACTUAL_CONSUMER_INPUT_FIELDS_ONLY_NO_SCIENCE_OR_FULL_READY_RETURN_REPLAY"
INPUT_TERMINAL_SCHEMA = "AXMAT_REFERENCE_INPUT_GRAPH_ACTUAL_DECLARE_TERMINAL_RETURN_V1"
COLD_TERMINAL = ART / "axial-material-qualified-AAA-rank1-factor-cache-production-terminal-20261007"
COLD_TERMINAL_SHA = "942532d85e1b38c8eb74e63f9d442e717cc01e4d24ded8fa0ba5ac5be1cbeddc"
FAILED_REFERENCE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AAA_rank1_cache_reference_analysis.py"
FAILED_REFERENCE_FACTORY_SHA = "a937a7d246abf43709f135ba36cdda0e7c81cf5340847160b8e433bb72e65b7c"
FAILED_REFERENCE_TERMINAL = ART / "axial-material-qualified-AAA-rank1-factor-cache-reference-terminal-20261007"
FAILED_REFERENCE_TERMINAL_SHA = "6b268ee388687eb354ad56c187563f507be700ac7b8ed314489e3a9dff0abe5f"
FAILED_COLD_TERMINAL = ART / "axial-material-qualified-AAA-moment-order-production-terminal-20261006"
FAILED_COLD_TERMINAL_SHA = "4f7475d0a9056794650cb2647bb343dc722f1802aa07601993035f4daa485201"
FAILED_PERMISSION_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AAA_rank1_cache_graph_reference.py"
FAILED_PERMISSION_FACTORY_SHA = "35ad3a606d69c69041ffec22fe3f34bff115064976dc96f99bb6322e78a9f821"
FAILED_PERMISSION_TERMINAL = ART / "axial-material-qualified-AAA-rank1-input-graph-reference-terminal-20261007"
FAILED_PERMISSION_TERMINAL_SHA = "f7f09fa94c8a6bcb07f4e2b336e3b4291022b34d9277001486e6d227d9e68d0c"



def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, wanted=None):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or (wanted is not None and digest(path) != wanted):
        raise ValueError("missing or changed declared reference dependency: " + str(path))
    return path


def pin(path):
    path = require(Path(path).resolve())
    return dict(path=str(path), sha256=digest(path))


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def archive_bytes():
    """Count only the two fixed CE roots without following any symlinks."""
    builder = module(require(BUILD_FACTORY, BUILD_SOURCE_SHA), "rank1_factor_cache_reference_build_dependency")
    roots = builder.validate_history_roots(list(ARCHIVE_ROOTS), ART)
    total, stack = 0, list(roots)
    while stack:
        directory = stack.pop()
        try:
            descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                with os.scandir(descriptor) as entries:
                    for entry in entries:
                        try:
                            item = entry.stat(follow_symlinks=False)
                        except FileNotFoundError:
                            continue
                        if stat.S_ISDIR(item.st_mode):
                            stack.append(directory / entry.name)
                        elif stat.S_ISREG(item.st_mode):
                            total += item.st_size
            finally:
                os.close(descriptor)
        except FileNotFoundError:
            continue
    builder.validate_history_roots(list(ARCHIVE_ROOTS), ART)
    return total


def source_namespace():
    """Exact new SOURCE namespace, including empty directories; no aliases."""
    cursor = SOURCE
    while True:
        if cursor.is_symlink():
            raise ValueError("new SOURCE or an ancestor cannot be a symlink")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    if not SOURCE.is_dir() or SOURCE.resolve(strict=True) != SOURCE:
        raise ValueError("new SOURCE must be its exact canonical directory")
    files, directories, pending = set(), set(), [SOURCE]
    while pending:
        directory = pending.pop()
        descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            with os.scandir(descriptor) as entries:
                for entry in entries:
                    path = directory / entry.name
                    name = str(path.relative_to(SOURCE))
                    mode = entry.stat(follow_symlinks=False).st_mode
                    if stat.S_ISREG(mode):
                        files.add(name)
                    elif stat.S_ISDIR(mode):
                        directories.add(name)
                        pending.append(path)
                    else:
                        raise ValueError("new SOURCE contains an undeclared alias or nonregular endpoint")
        finally:
            os.close(descriptor)
    return dict(files=sorted(files), directories=sorted(directories), symlinks={})


def terminal_contract():
    """Root records the actual terminal return; this factory only consumes it."""
    return dict(schema=TERMINAL_SCHEMA, root=str(TERMINAL), receipt=str(TERMINAL / "terminal_return.json"),
        record_producer="root", full_stdout_is_retained=True, actual_tool_exit_zero_required=True,
        record_written_after_actual_terminal_return_required=True, tail_fields=list(TAIL_FIELDS),
        archive_reserve_bytes=RESERVE, archive_resource_roots=list(ARCHIVE_ROOTS), archive_byte_scope=ARCHIVE_SCOPE,
        resource_scope_policy=HISTORY_SCOPE_POLICY, tail_roots_are_dynamic_union=True,
        resource_scope_contract=module(require(BUILD_FACTORY, BUILD_SOURCE_SHA),
            "rank1_factor_cache_reference_build_dependency").resource_scope_contract(),
        actual_run_command=[str(PYTHON), str(Path(__file__).resolve()), "run", "--sha256", "__DECLARATION_SHA256__",
            "--input-terminal-evidence-sha256", "__INPUT_DECLARATION_TERMINAL_SHA256__"],
        evidence_producer_implemented_by_this_factory=False)


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def module(path, name):
    path = require(path).resolve()
    if name in sys.modules:
        obj = sys.modules[name]
        if Path(obj.__file__).resolve() != path:
            raise ValueError("imported reference dependency has a different actual source path")
        return obj
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    if Path(obj.__file__).resolve() != path:
        raise ValueError("actual imported source path differs")
    return obj


def controller():
    sys.path.insert(0, str(PROD / "runtime"))
    return module(PROD / "runtime/production_runner.py", "production_runner")


def environment(env=None):
    import numpy as np
    if (Path(sys.executable).resolve() != PYTHON.resolve() or sys.version_info[:2] != (3, 12)
            or np.__version__ != "2.4.3"
            or Path(np.__file__).parent.resolve() != Path("/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/site-packages/numpy")
            or any(os.environ.get(key) != "1" for key in THREADS)):
        raise ValueError("original separate CE Python3.12/NumPy2.4.3 and single-thread environment required")
    require(PYTHON.resolve(), "ba725dca52e02b5382d6acf3e6ac92afb0d65662f1ce8820d75a59a095490860")
    loader = {key: os.environ.get(key) for key in (
        "PYTHONPATH", "DYLD_LIBRARY_PATH", "DYLD_INSERT_LIBRARIES", "LD_LIBRARY_PATH")}
    if env is not None:
        verify(env["files"])
        if (platform.python_version() != env["python_version"] or np.__version__ != env["numpy_version"]
                or loader != env["loader_environment"]):
            raise ValueError("frozen CE analysis interpreter, packages or loader environment changed")
        return env
    causal = read(CAUSAL / "declaration.json")
    files = {path: sha for path, sha in causal["files"].items()
             if path.startswith("/Users/wen/miniforge3/envs/openmc-dev/")}
    files[str(PYTHON.resolve())] = digest(PYTHON.resolve())
    verify(files)
    # Original CE package roots are frozen for this reassessment before any
    # export or analysis; the producer's separate 3.14 replay stays unchanged.
    for name in ("numpy", "scipy", "h5py", "openmc"):
        package = __import__(name)
        base = Path(package.__file__).parent.resolve()
        for path in base.rglob("*"):
            if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                observed = digest(path)
                if str(path) in files and files[str(path)] != observed:
                    raise ValueError("original frozen CE numerical package changed")
                files[str(path)] = observed
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_SEPARATE_CE_ENVIRONMENT_V1",
        executable=str(PYTHON.resolve()), python_version=platform.python_version(), numpy_version=np.__version__,
        producer_environment_is_separate=True, files=files,
        thread_environment={key: "1" for key in THREADS}, loader_environment=loader)


def candidate_completion(c, info, status, allow_already_existing_ABA=False):
    """Read the complete actual coupled attempt and all sealed observer logs."""
    case = status["cases"]["AAA"]
    count = case["completed_maps"]
    claim_path = require(PROD / "AAA/run_claim.json")
    claim = read(claim_path)
    final_resources = status["final_resources"]
    if (type(count) is not int or not 1 <= count <= info["budgets"]["max_maps"]
            or info["budgets"]["max_maps"] != 100 or info["budgets"]["total_seconds"] != 43200
            or status["completed_maps"] != count or len(case["maps"]) != count
            or [row["epoch"] for row in case["maps"]] != list(range(1, count + 1))
            or [row["classification"] for row in case["maps"]] != ["VALID_NOT_MET"] * (count - 1) + ["VALID_MET"]
            or Path(case["final_directory"]) != PROD / "AAA" / f"map{count:03d}"
            or {path.name for path in (PROD / "AAA").glob("map*")} != {f"map{epoch:03d}" for epoch in range(1, count + 1)}
            or ((PROD / "ABA").exists() and not allow_already_existing_ABA) or status.get("error") is not None
            or claim["case"] != "AAA" or claim["prepared_sha256"] != status["prepared_sha256"]
            or type(claim["pid"]) is not int or claim["pid"] <= 0
            or type(status["finished_unix"]) not in (int, float) or not math.isfinite(status["finished_unix"])
            or not claim["started_unix"] <= status["finished_unix"]
            or status["reference_qualification"] is not None
            or final_resources["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or final_resources["artifact_budget_bytes"] != 96 * 2**30 or final_resources["min_free_bytes"] != 8 * 2**30
            or "reason" in final_resources):
        raise ValueError("complete consecutive original-budget AAA map history and this phase's ABA scope required")
    expected_labels = ["archives/pack_archives", "training/common_basis", "training/rank_precision",
        "AAA/bootstrap/case_setup", "AAA/bootstrap/white_tracking", "AAA/bootstrap/make_route_contract",
        "AAA/bootstrap/bootstrap_axial", "AAA/bootstrap/bootstrap_radial", "AAA/bootstrap/b2i_seal_bootstrap"]
    map_names = ("prepare_r64_next_projected", "picard_radial", "admit_candidate_radial", "picard_axial",
        "close_r64_returned", "checker_parent", "check_one_map_xsm", "check_convergence_gate")
    expected_labels += [f"AAA/map{epoch:03d}/" + name for epoch in range(1, count + 1) for name in map_names]
    stage_path = require(PROD / "AAA/stages.json")
    stages = read(stage_path)["stages"]
    if [stage["label"] for stage in stages] != expected_labels or any(stage["status"] != "PASS" for stage in stages):
        raise ValueError("all original actual complete coupled stages must pass in order")
    guard = module(PROD / "runtime/rank1_factor_cache_admission.py", "rank1_factor_cache_admission")
    expected_axial = {"AAA/bootstrap/bootstrap_axial"} | {f"AAA/map{epoch:03d}/picard_axial" for epoch in range(1, count + 1)}
    observers = []
    for stage in stages:
        log = require(PROD / (stage["label"] + ".log"), stage["log_sha256"])
        if stage["label"] in expected_axial:
            text = log.read_text(errors="replace")
            actual = guard.admit_actual_axial_selector(text, log)
            cached = guard.admit_actual_rank1_factor_cache(text, log, len(actual["actual_observers"]))
            if (stage["command"] != [str(PROD / "runtime/Dragon")]
                    or stage["transport_status_before_selector_guard"] != "PASS"
                    or stage["rank1_factor_cache_selector_guard"] != actual
                    or stage["rank1_factor_cache_guard"] != cached or cached["status"] != "PASS"
                    or actual["status"] != "PASS" or actual["expected"] != OBSERVER_EXPECTED
                    or not actual["actual_observers"]):
                raise ValueError("every actual bootstrap/map axial selector must have an exact archived PASS guard")
            observers.append(dict(label=stage["label"], guard=actual, factor_cache_guard=cached))
        elif "rank1_factor_cache_selector_guard" in stage or "rank1_factor_cache_guard" in stage:
            raise ValueError("unexpected axial selector guard on a non-axial stage")
    folders = [PROD / "archives", PROD / "training", PROD / "AAA/bootstrap"]
    folders += [PROD / "AAA" / f"map{epoch:03d}" for epoch in range(1, count + 1)]
    for folder in folders:
        c.verify_sealed_directory(folder)
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_COMPLETE_COUPLED_AAA_BINDING_V1", case="AAA",
        stages=pin(stage_path), completed_maps=count, continuous_map_epochs=list(range(1, count + 1)),
        actual_complete_run_claim=pin(claim_path), actual_finished_unix=status["finished_unix"],
        original_max_maps=100, original_total_seconds=43200,
        all_stage_logs={str(PROD / (s["label"] + ".log")): s["log_sha256"] for s in stages},
        complete_stage_seals=[pin(folder / "result.json") for folder in folders],
        actual_axial_selector_guards=observers, all_actual_axial_selectors_verified=True,
        all_actual_rank1_factor_cache_guards_verified=True,
        coupled_fixed_point_only=True, independent_accuracy_qualified=False, AAA_attempt_started_ABA=False)


def ready(prepared_sha, status_sha, build_seal_sha, build_terminal_evidence, build_terminal_evidence_sha256,
          allow_already_existing_ABA=False):
    require(TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA)
    require(COUPLING_FACTORY, COUPLING_FACTORY_SHA)
    require(BUILD_FACTORY, BUILD_SOURCE_SHA)
    builder = module(BUILD_FACTORY, "rank1_factor_cache_reference_build_dependency")
    build = builder.production_admission(build_seal_sha, build_terminal_evidence, build_terminal_evidence_sha256)
    if (build["schema"] != "AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or build["build_root"] != str(BUILD) or build["build_seal_sha256"] != build_seal_sha
            or build["actual_external_terminal_evidence"] != dict(path=str(BUILD_TERMINAL / "terminal_return.json"),
                sha256=build_terminal_evidence_sha256)
            or build["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or build["resource_scope_contract"] != builder.resource_scope_contract()
            or build["current_complete_history_admission_required"] is not True
            or build["rank1_factor_cache_budget_bytes"] != 536870912
            or any(build[key] is not True for key in ("rank1_factor_cache_controls_passed",
                "all_new_cache_outputs_bitwise_equal_to_uncached", "operator_identity_guard_negative_controls_passed",
                "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required"))
            or build["full_FLU_entry_execution_proved_by_build"] is not False
            or build["AAA_accuracy_qualified"] is not False or build["ABA_admitted"] is not False):
        raise ValueError("actual externally completed limited-scope moment-order build required")
    c = controller()
    info = c.verify_prepared(PROD / "prepared.json", prepared_sha)
    status = read(require(PROD / "AAA/run_status.json", status_sha))
    if (info["classification"] != "PREPARED_NO_TRANSPORT"
            or info["experiment_id"] != "axial-material-qualified-AB-rank1-factor-cache-20261007"
            or status["classification"] != "WAITING_REFERENCE" or status["case"] != "AAA"
            or status["prepared_sha256"] != prepared_sha
            or status["cases"].get("AAA", {}).get("classification") != "VALID_MET"
            or status["common_basis_sha256"] != digest(PROD / "training/common_basis.xsm")
            or info["runtime_sources"]["Dragon"] != build["corrected_runtime"]):
        raise ValueError("actual complete new moment-order AAA fixed point required")
    final = Path(status["cases"]["AAA"]["final_directory"])
    if final.parent != PROD / "AAA":
        raise ValueError("actual new AAA final stage must be in its own case")
    for folder in (PROD / "archives", PROD / "training", PROD / "AAA/bootstrap", final):
        c.verify_sealed_directory(folder)
    coupled = candidate_completion(c, info, status, allow_already_existing_ABA=allow_already_existing_ABA)
    declaration = read(require(info["declaration"]["path"], info["declaration"]["sha256"]))
    revision = declaration["rank1_factor_cache_revision"]
    metadata = read(require(revision["path"], revision["sha256"]))
    chain = dict(factory=pin(BUILD_FACTORY), declaration=pin(BUILD / "declaration.json"),
        build_seal=pin(BUILD / "seal.json"), driver_result=pin(BUILD / "driver_result.json"),
        full_stdout=build["actual_external_terminal_validation"]["full_stdout"],
        terminal_evidence=build["actual_external_terminal_evidence"])
    if (declaration["helper"] != pin(COUPLING_FACTORY) or metadata["build_admission"] != build
            or metadata["build_terminal_evidence"] != build["actual_external_terminal_evidence"]
            or metadata["build_terminal_validation"] != build["actual_external_terminal_validation"]
            or metadata["build_terminal_chain"] != chain or metadata["resource_scope_policy"] != HISTORY_SCOPE_POLICY):
        raise ValueError("actual candidate coupling must bind this exact completed build and full Root terminal chain")
    if metadata["resource_scope_contract"] != build["resource_scope_contract"]:
        raise ValueError("actual candidate retains the original axial-family storage contract")
    if status["final_resources"]["resource_scope_contract"] != build["resource_scope_contract"]:
        raise ValueError("actual completed candidate resource tail must retain the same inherited family scope")
    verify({item["path"]: item["sha256"] for item in chain.values()})
    coupled.update(coupling_declaration=info["declaration"], coupling_revision=revision,
        coupling_equivalence=declaration["rank1_factor_cache_equivalence"], actual_build_terminal_chain=chain)
    recipe = read(require(OLD_SOURCE / "refined_reference_analysis_recipe.json", RECIPE_SHA))
    if (tuple(recipe["original_eight_checks"]) != GATES or recipe["fixed_history"] != dict(
            inactive_batches=100, active_batches=2000, particles_per_generation=10000,
            generations_per_batch=10, first_active=101, last_active=2100,
            raw_generation_entries=21000, batched_generation_entries=2100)):
        raise ValueError("original eight gates and complete consecutive reference history required")
    for item in [recipe[key] for key in ("reference_execution", "complete_independent_native_sample",
            "original_candidate_assessment", "observation_projection_recipe", "projection_precheck",
            "native_export_source_proof", "physical_input_precheck")] + list(recipe["unchanged_reference_implementations"].values()):
        require(item["path"], item["sha256"])
    native = read(recipe["complete_independent_native_sample"]["path"])
    if (native["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS"
            or native["returncode"] != 0 or native["error"] is not None):
        raise ValueError("complete immutable independent CE sample required")
    expected = {f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)}
    if {name for name in native["outputs"] if name.startswith("statepoint.") and name.endswith(".h5")} != expected:
        raise ValueError("all original 2000 zero-padded active statepoint paths required")
    verify({str(CE / "AAA" / name): sha for name, sha in native["outputs"].items()})
    require(CE / "AAA/openmc.log", native["log_sha256"])
    execution = read(recipe["reference_execution"]["path"])
    verify(execution["files"])
    return c, info, status, final, recipe, native, execution, coupled, build


def patch(original_path, changes, target, allowed_functions=()):
    original = require(original_path).read_bytes().decode("utf-8")
    candidate = original
    for old, new, count in changes:
        if candidate.count(old) != count:
            raise ValueError("reference binding patch has an ambiguous source anchor: " + old[:100])
        candidate = candidate.replace(old, new)
    restored = candidate
    for old, new, count in reversed(changes):
        if restored.count(new) != count:
            raise ValueError("reference binding restoration has an ambiguous anchor")
        restored = restored.replace(new, old)
    if restored != original:
        raise ValueError("scientific implementation changed outside explicit bindings")
    def definitions(text):
        return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(text).body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    before, after = definitions(original), definitions(candidate)
    if before.keys() != after.keys() or any(before[key] != after[key] for key in before if key not in allowed_functions):
        raise ValueError("unlisted scientific/reference verification function changed")
    target.write_bytes(candidate.encode("utf-8"))
    target.with_suffix(".patch").write_text("".join(difflib.unified_diff(
        original.splitlines(True), candidate.splitlines(True), fromfile=str(original_path), tofile=str(target))))
    return dict(parent=pin(original_path), candidate=pin(target), changes=changes,
        original_source_restored_byte_exact=True, unchanged_function_AST=sorted(set(before) - set(allowed_functions)),
        allowed_binding_function_changes=list(allowed_functions), scientific_conditions_changed=False)


def live_guard_provenance(full, c, info):
    if (full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,)
            or Path(c.__file__).resolve() != PROD / "runtime/production_runner.py"
            or Path(full.__file__).resolve() != FULL_FACTORY):
        raise ValueError("live own-RSS supervisor has a different actual parent controller/source")
    declaration = read(require(info["declaration"]["path"], info["declaration"]["sha256"]))
    gate_item = declaration["rank1_factor_cache_equivalence"]
    gate = read(require(gate_item["path"], gate_item["sha256"]))
    source_item = gate["source_equivalence"]
    source = read(require(source_item["path"], source_item["sha256"]))
    proof = source["patches"]["production_runner.py"]
    require(proof["candidate"]["path"], proof["candidate"]["sha256"])
    if (source["schema"] != "AXMAT_RANK1_FACTOR_CACHE_PIPELINE_SOURCE_EQUIVALENCE_V1"
            or digest(c.__file__) != proof["candidate"]["sha256"]
            or not {"SerialExecutor", "qualify_aba"}.issubset(proof["unchanged_function_AST"])
            or set(proof["admitted_function_changes"]) != {"prepare", "run", "resource_monitor"}
            or source["run_AST_exact"] is not False or source["resource_monitor_AST_exact"] is not False
            or any(source[key] is not True for key in ("run_only_delta_is_actual_axial_selector_and_factor_cache_log_guards",
                "run_inverse_patch_restores_original_bytes_exactly", "resource_monitor_only_delta_is_dynamic_history_accounting",
                "resource_monitor_inverse_patch_restores_original_bytes_exactly", "qualify_ABA_and_serial_supervision_AST_exact",
                "selector_guard_failure_prevents_seal_and_next_stage", "rank1_factor_cache_guard_failure_prevents_seal_and_next_stage"))
            or source["actual_complete_log_each_selector_values_required"] != OBSERVER_EXPECTED
            or source["actual_factor_cache_observer_contract"] != dict(
                prefix="AXMAT-RANK1-CACHE TERMINAL ",
                columns=["builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes", "cap_bytes"],
                cap_bytes=536870912, exact_operator_identity_required=True,
                positive_build_reuse_and_validation_required=True, all_actual_full_logs_required=True)
            or source["resource_scope_policy"] != HISTORY_SCOPE_POLICY):
        raise ValueError("actual production supervisor differs from its exact source proof")
    revision = declaration["rank1_factor_cache_revision"]
    meta = read(require(revision["path"], revision["sha256"]))
    parent_item = meta["parent_prepared"]
    require(parent_item["path"], parent_item["sha256"])
    original = Path(parent_item["path"]).parent / "runtime/production_runner.py"
    require(original, proof["original_sha256"])
    def class_ast(path):
        tree = ast.parse(Path(path).read_bytes().decode("utf-8"))
        return ast.dump(next(node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "SerialExecutor"), include_attributes=False)
    if class_ast(original) != class_ast(c.__file__):
        raise ValueError("actual current production supervision changed from its frozen parent")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_CE_LIVE_GUARD_PROVENANCE_V1",
        own_RSS_source=pin(FULL_FACTORY), actual_parent_controller=pin(c.__file__),
        original_parent_controller=pin(original), coupling_gate_equivalence=gate_item,
        coupling_source_equivalence=source_item, actual_base_is_verified_current_SerialExecutor=True,
        original_parent_SerialExecutor_AST_exact=True,
        actual_controller_run_has_only_declared_selector_and_factor_cache_log_guards=True,
        actual_controller_factor_cache_observer_contract=source["actual_factor_cache_observer_contract"],
        actual_controller_resource_monitor_has_only_declared_dynamic_resource_guard=True,
        run_and_resource_monitor_AST_exact=False, resource_scope_policy=HISTORY_SCOPE_POLICY,
        module_identity_reassigned=False)


ADMISSION = '''"""Bind fresh moment-order measurement to the one bounded reassessment."""
import json
from pathlib import Path
import sys
PROD = Path(__PROD__)
OUT = Path(__OUT__)
FACTORY_PATH = Path(__FACTORY_PATH__)
FACTORY_SHA = __FACTORY_SHA__
sys.path.insert(0, str(PROD / "runtime"))
from production_runner import require_file, sha256, verify_sealed_directory


def verified_prepared_input_context(expected_prepared, phase, with_context=False):
    import importlib.util
    d = json.loads((OUT / "declaration.json").read_text())
    item = d["input_graph_factory"]
    if item != dict(path=str(FACTORY_PATH), sha256=FACTORY_SHA):
        raise ValueError("child input context has a different frozen factory binding")
    source = require_file(FACTORY_PATH, FACTORY_SHA)
    name = "actual_rank1_input_graph_reference_factory"
    if name in sys.modules:
        factory = sys.modules[name]
        if Path(factory.__file__).resolve() != source.resolve():
            raise ValueError("actual graph factory source path differs")
    else:
        spec = importlib.util.spec_from_file_location(name, source)
        factory = importlib.util.module_from_spec(spec)
        sys.modules[name] = factory
        spec.loader.exec_module(factory)
    expected = json.loads((OUT / "prepared.json").read_text())["declaration"]["sha256"]
    d, actual = factory.admission(expected, prepared=True, phase=phase)
    if d["production_prepared"]["sha256"] != expected_prepared:
        raise ValueError("fresh input graph belongs to a different prepared producer")
    return (actual[1], (d, actual)) if with_context else actual[1]


def verify_measurement_admission(prepared, expected, input_context):
    d, actual = input_context
    if d != json.loads(require_file(OUT / "declaration.json", expected).read_text()):
        raise ValueError("fresh collector context declaration differs")
    # The real full metadata API ran on the actual declaration, and this parent
    # passed its complete global input entry. This child freshly verifies its
    # complete scientific/code/proof input subset and receives only the prepared
    # fields it consumes. Read the current exact build/coupled metadata binding;
    # no whole full-ready return or numerical result is replayed in this child.
    item = d["coupling_completion"]["coupling_revision"]
    binding = json.loads(require_file(Path(item["path"]), item["sha256"]).read_text())
    if (binding["build_admission"] != d["build_admission"]
            or binding["build_terminal_chain"] != d["build_terminal_chain"]
            or binding["resource_scope_contract"] != d["resource_scope_contract"]
            or d["coupling_completion"]["all_actual_axial_selectors_verified"] is not True):
        raise ValueError("collector must consume the actual complete moment-order build/coupled bindings")
    status = json.loads(require_file(PROD / "AAA/run_status.json", d["AAA_status"]["sha256"]).read_text())
    claim = json.loads((OUT / "AAA/analysis_claim.json").read_text())
    if (d["schema"] != "AXMAT_RANK1_FACTOR_CACHE_COMPLETE_ORIGINAL_GATE_REFERENCE_V1"
            or claim["declaration_sha256"] != expected
            or status["classification"] != "WAITING_REFERENCE"
            or status["cases"]["AAA"]["classification"] != "VALID_MET"
            or d["production_prepared"]["sha256"] != __PREPARED_SHA__):
        raise ValueError("actual new complete AAA and bounded analysis declaration required")
    m = json.loads((OUT / "measurement_admission.json").read_text())
    if (m["classification"] != "FIXED_POINT_INPUTS_AND_COMPLETE_FINE_OBSERVATIONS_ADMITTED_TO_SAVED_REFERENCE"
            or m["production_prepared"] != d["production_prepared"] or m["AAA_status"] != d["AAA_status"]
            or m["case_spec"] != prepared["case_spec"] or m["build_admission"] != d["build_admission"]
            or m["common_basis_sha256"] != status["common_basis_sha256"]):
        raise ValueError("fresh candidate measurement bindings differ")
    for name, wanted in m["files"].items():
        require_file(Path(name), wanted)
    for folder in (PROD / "archives", PROD / "training", PROD / "AAA/bootstrap",
                   Path(status["cases"]["AAA"]["final_directory"])):
        verify_sealed_directory(folder)
    projection = json.loads((OUT / "observation/projection_receipt.json").read_text())
    if (projection["classification"] != "PASS_COMPLETE_FINE_AND_CONSERVATIVE_ORIGINAL_OBSERVATION_VIEW"
            or projection["native_axial_cells"] != 48 or projection["observation_cells"] != 12
            or len(projection["mapping"]) != 96 or len(projection["face_map"]) != 13
            or projection["local_or_binwise_normalization"] or projection["bins_removed"]):
        raise ValueError("complete conservative original observation view required")
    for key in ("original_checks_on_all_fine_entries", "original_checks_on_observation_view"):
        if any(value != "PASS" for value in projection[key]["checks"].values()):
            raise ValueError("original complete fine/view numerical checks failed")
    physical = json.loads((OUT / "input_equivalence_AAA.json").read_text())
    if (physical["status"] != "PASS" or physical["production_prepared"] != m["production_prepared"]
            or physical["AAA_status"] != m["AAA_status"]
            or physical["case_spec_sha256"] != prepared["case_spec"]["sha256"]
            or not physical["original_physical_and_independent_scientific_definitions_unchanged"]):
        raise ValueError("actual candidate physical input proof differs")
    binding = json.loads((OUT / "measurement_binding.json").read_text())
    if binding["declaration_sha256"] != expected:
        raise ValueError("actual completed projection binding differs")
    for name, wanted in binding["files"].items():
        require_file(Path(name), wanted)
    if binding["files"].get(str(OUT / "measurement_admission.json")) != sha256(OUT / "measurement_admission.json"):
        raise ValueError("actual completed measurement was not archived by its parent controller")
    return m
'''


def graph_helper():
    return module(require(GRAPH_HELPER, GRAPH_HELPER_SHA), "reference_verified_input_graph")


def cold_terminal_input(info, status):
    evidence = strict_terminal_json(require(COLD_TERMINAL / "terminal_return.json", COLD_TERMINAL_SHA))
    if (evidence["schema"] != "AXMAT_RANK1_FACTOR_CACHE_COLD_AAA_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
            or evidence["record_producer"] != "root" or evidence["returncode"] != 0
            or type(evidence["returncode"]) is not int
            or evidence["actual_tool_terminal_return_observed"] is not True
            or evidence["record_written_after_actual_terminal_return"] is not True
            or evidence["prepared"] != pin(PROD / "prepared.json")
            or evidence["run_status"] != pin(PROD / "AAA/run_status.json")
            or evidence["completed_maps"] != status["completed_maps"]
            or evidence["source"] != pin(require(COUPLING_FACTORY, COUPLING_FACTORY_SHA))
            or evidence["AAA_accuracy_qualified"] is not False or evidence["ABA_admitted"] is not False):
        raise ValueError("actual independent Root cold fixed-point exit-zero input witness required")
    stdout = require(evidence["full_stdout"]["path"], evidence["full_stdout"]["sha256"])
    if stdout.parent != COLD_TERMINAL or strict_terminal_json(stdout) != status:
        raise ValueError("cold fixed-point witness must retain the actual full returned status")
    return evidence


def declaration_terminal_admission(d, expected, expected_input_terminal_sha):
    if (not isinstance(expected_input_terminal_sha, str) or len(expected_input_terminal_sha) != 64
            or any(ch not in "0123456789abcdef" for ch in expected_input_terminal_sha)):
        raise ValueError("external actual input-declaration terminal SHA256 required")
    path = terminal_file(TERMINAL / "declaration_terminal_return.json", TERMINAL, expected_input_terminal_sha)
    receipt = strict_terminal_json(path)
    stdout = terminal_file(receipt["full_stdout"]["path"], TERMINAL, receipt["full_stdout"]["sha256"])
    if (receipt["schema"] != INPUT_TERMINAL_SCHEMA or receipt["record_producer"] != "root"
            or type(receipt["returncode"]) is not int or receipt["returncode"] != 0
            or receipt["actual_tool_terminal_return_observed"] is not True
            or receipt["record_written_after_actual_terminal_return"] is not True
            or receipt["source"] != d["input_graph_factory"]
            or receipt["source"] != pin(Path(__file__).resolve())
            or receipt["declaration"] != dict(path=str(SOURCE / "declaration.json"), sha256=expected)
            or receipt["input_graph"] != d["input_graph"]
            or receipt["scientific_predicates_evaluated"] is not False
            or receipt["AAA_accuracy_qualified"] is not False or receipt["ABA_admitted"] is not False
            or strict_terminal_json(stdout) != dict(
                classification="DECLARED_NEW_RANK1_INPUT_GRAPH_REFERENCE_NOT_PREPARED_OR_RUN",
                declaration=receipt["declaration"], input_graph=d["input_graph"], output=str(OUT),
                scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False)):
        raise ValueError("genuine external declaration exit-zero/full-stdout input witness required")
    if receipt["source_inventory"] != pin(require(SOURCE / "source_inventory.json", receipt["source_inventory"]["sha256"])):
        raise ValueError("external declaration witness must pin the complete SOURCE inventory")
    wanted_command = [str(PYTHON), str(Path(__file__).resolve()), "declare",
        "--prepared-sha256", d["production_prepared"]["sha256"],
        "--status-sha256", d["AAA_status"]["sha256"],
        "--build-seal-sha256", d["build_admission"]["build_seal_sha256"],
        "--build-terminal-evidence", d["actual_build_terminal_evidence"]["path"],
        "--build-terminal-evidence-sha256", d["actual_build_terminal_evidence"]["sha256"]]
    if receipt["command"] != wanted_command:
        raise ValueError("actual declaration terminal command differs from its bound original inputs")
    return receipt


def actual_system_identity():
    """Fresh kernel and macOS product identity, an INPUT environment condition."""
    actual = os.uname()
    processor = subprocess.check_output(["uname", "-p"], stderr=subprocess.DEVNULL,
        timeout=1, text=True, encoding="utf8").strip()
    return dict(system=actual.sysname, release=actual.release, version=actual.version,
                machine=actual.machine, mac_ver=json.loads(json.dumps(platform.mac_ver())),
                processor=processor, probe_path_environment=os.environ.get("PATH"),
                timezone_environment=os.environ.get("TZ"), timezone_names=list(time.tzname),
                timezone_offset=time.timezone, timezone_daylight=time.daylight)


def consumer_snapshot(info, status, recipe, system_identity, phase):
    """Expose only the audited fields consumed by this unchanged science body."""
    if phase not in CONSUMER_PHASES:
        raise ValueError("explicit original consumer phase required")
    keys = {"fine/physical": ("experiment_id", "case_spec"),
            "AAA/project": ("case_spec",),
            "AAA/collect": ("experiment_id", "case_spec", "rank_addendum")}[phase]
    return dict(scope=CONSUMER_SNAPSHOT_SCOPE, phase=phase,
        prepared={key:copy.deepcopy(info[key]) for key in keys},
        status={"common_basis_sha256": status["common_basis_sha256"]} if phase == "AAA/project" else {},
        recipe={key:copy.deepcopy(recipe[key]) for key in ("reference_execution", "complete_independent_native_sample")}
            if phase == "AAA/project" else {},
        common_guard_context=dict(declaration=copy.deepcopy(info["declaration"]),
            resource_roots=copy.deepcopy(info["resource_roots"]), artifact_root=info["artifact_root"],
            completed_maps=status["cases"]["AAA"]["completed_maps"],
            final_directory=status["cases"]["AAA"]["final_directory"],
            actual_system_identity=copy.deepcopy(system_identity)),
        full_original_input_semantics_replayed=False, complete_global_closure_claimed=False,
        scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def verified_input_state(d, expected, phase, allow_already_existing_ABA=False, input_terminal_sha=None,
                         verification_sink=None):
    input_terminal_sha = input_terminal_sha or os.environ.get("AXMAT_INPUT_GRAPH_DECLARE_TERMINAL_SHA256")
    declaration_terminal_admission(d, expected, input_terminal_sha)
    consumer = phase in CONSUMER_PHASES
    graph_item = d["consumer_input_graphs"][phase] if consumer else d["input_graph"]
    verified = graph_helper().verify_graph(graph_item["path"],
        expected_sha256=graph_item["sha256"], phase=phase)
    snapshot = verified["typed_snapshot"]
    if consumer:
        plan_item = d["consumer_input_source_plans"][phase]
        source_plan = read(require(plan_item["path"], plan_item["sha256"]))
        expected_paths = sorted(set(source_plan["selected_paths"]) | {d["input_graph"]["path"]})
        if (verified["consumer_selected_literal_and_canonical_paths"] != expected_paths
                or verified["consumer_complete_namespace_root_sequence"] != source_plan["selected_namespace_root_sequence"]):
            raise ValueError("consumer graph does not exactly cover its complete source-audited input plan")
    if (snapshot["scope"] != (CONSUMER_SNAPSHOT_SCOPE if consumer else "ORIGINAL_FULL_READY_INPUT_SEMANTICS_ONLY")
            or snapshot["scientific_predicates_evaluated"] is not False
            or snapshot["AAA_accuracy_qualified"] is not False or snapshot["ABA_admitted"] is not False):
        raise ValueError("an input snapshot cannot substitute a new scientific result")
    system = actual_system_identity()
    if consumer:
        if (verified["consumer_scope"]["phase"] != phase
                or verified["consumer_scope"]["parent_input_graph"] != d["input_graph"]
                or snapshot["phase"] != phase
                or snapshot["full_original_input_semantics_replayed"] is not False
                or snapshot["complete_global_closure_claimed"] is not False):
            raise ValueError("scientific handoff must consume only its actual declared input fields")
        info = read(require(PROD / "prepared.json", d["production_prepared"]["sha256"]))
        status = read(require(PROD / "AAA/run_status.json", d["AAA_status"]["sha256"]))
        recipe = read(require(OLD_SOURCE / "refined_reference_analysis_recipe.json", RECIPE_SHA))
        if consumer_snapshot(info, status, recipe, system, phase) != snapshot:
            raise ValueError("actual current metadata differs from this consumer's exact field snapshot")
    else:
        if verified["consumer_scope"] is not None:
            raise ValueError("global entry/final/qualification requires the complete original input graph")
        info, status = snapshot["info"], snapshot["status"]
        recipe = snapshot["recipe"]
    if system != (snapshot["common_guard_context"]["actual_system_identity"] if consumer else snapshot["actual_system_identity"]):
        raise ValueError("actual kernel or macOS product identity changed since input declaration")
    c = controller()
    final = Path(status["cases"]["AAA"]["final_directory"] if consumer else snapshot["final"])
    c.validate_resource_roots(info["resource_roots"], Path(info["artifact_root"]))
    if not any(PROD == Path(root) or PROD.is_relative_to(Path(root)) for root in info["resource_roots"]):
        raise ValueError("actual prepared runtime is outside its original live resource roots")
    count = status["cases"]["AAA"]["completed_maps"]
    if ({path.name for path in (PROD / "AAA").glob("map*")} != {f"map{n:03d}" for n in range(1, count+1)}
            or final != PROD / "AAA" / f"map{count:03d}"
            or ((PROD / "ABA").exists() and not allow_already_existing_ABA)):
        raise ValueError("actual complete map namespace or this phase's ABA lifecycle changed")
    environment(read(d["analysis_environment"]["path"]))
    build_declaration = read(BUILD / "declaration.json")
    loader = {key: value for key, value in os.environ.items() if key.startswith("DYLD_") or key == "OPENBLAS_CORETYPE"}
    expected_loader = {key: value for key, value in build_declaration["numerical_loader_environment"].items()
                       if key.startswith("DYLD_") or key == "OPENBLAS_CORETYPE"}
    if loader != expected_loader:
        raise ValueError("actual native loader/dispatch environment differs from full original input admission")
    for alias, target in build_declaration["native_library_aliases"].items():
        if str(Path(alias).resolve(strict=True)) != target:
            raise ValueError("live original native-library alias target changed")
    expected_statepoints = {f"statepoint.{n:04d}.h5" for n in range(101, 2101)}
    if {path.name for path in (CE / "AAA").glob("statepoint.*.h5")} != expected_statepoints:
        raise ValueError("the actual reference must retain exactly all original 2000 sample filenames")
    claim_path = OUT / "AAA/analysis_claim.json"
    if phase not in ("prepare", "run_entry"):
        claim = read(require(claim_path))
        if (claim["declaration_sha256"] != expected
                or claim["actual_input_declaration_terminal"] != pin(TERMINAL / "declaration_terminal_return.json")
                or type(claim["actual_run_pid"]) is not int or claim["actual_run_pid"] <= 0
                or claim["original_total_wall_seconds"] != TOTAL_WALL
                or claim["actual_run_command"] != [str(PYTHON), str(Path(__file__).resolve()), "run", "--sha256", expected,
                    "--input-terminal-evidence-sha256", input_terminal_sha]):
            raise ValueError("live analysis phase differs from the actual bounded parent claim")
        if phase in ("fine/physical", "AAA/project", "AAA/collect"):
            if os.getppid() != claim["actual_run_pid"] or time.monotonic()-claim["actual_run_started_monotonic"] >= TOTAL_WALL:
                raise ValueError("scientific child must belong to its current original-budget parent")
            entry = read(require(claim["actual_global_run_entry"]["path"], claim["actual_global_run_entry"]["sha256"]))
            if (entry["phase"] != "run_entry" or entry["actual_run_pid"] != claim["actual_run_pid"]
                    or entry["actual_run_started_monotonic"] != claim["actual_run_started_monotonic"]
                    or entry["declaration"] != dict(path=str(SOURCE / "declaration.json"), sha256=expected)
                    or entry["input_graph"] != d["input_graph"]
                    or entry["verification"]["consumer_scope"] is not None
                    or entry["verification"]["classification"] != "FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY"
                    or entry["scientific_predicates_evaluated"] is not False):
                raise ValueError("consumer input handoff requires this actual parent's complete global entry")
        elif phase == "run_final_immutable_input_closeout" and os.getpid() != claim["actual_run_pid"]:
            raise ValueError("the final closeout must belong to the actual original analysis parent")
    full = module(require(FULL_FACTORY, FULL_SOURCE_SHA), "rank1_factor_cache_reference_guard")
    if live_guard_provenance(full, c, info) != read(d["live_guard_provenance"]["path"]):
        raise ValueError("live controller/source/MRO or original supervision provenance changed")
    builder = module(require(BUILD_FACTORY, BUILD_SOURCE_SHA), "rank1_factor_cache_reference_build_dependency")
    builder.DynamicHistoryResources(ART, d["resource_roots"], d["min_free_bytes"],
        d["artifact_budget_bytes"], c.ResourceFailure).check()
    # These saved values are deterministic INPUT admission returns only.  The
    # complete unique input bytes and namespaces above were read again in this
    # call; no saved physics/statistics/current/qualification outcome is used.
    if consumer:
        if verification_sink is not None:
            raise ValueError("consumer handoff cannot mint a complete global entry witness")
        return c, snapshot["prepared"], snapshot["status"], final, snapshot["recipe"]
    actual = (c, info, status, final, recipe, snapshot["native"],
              snapshot["execution"], snapshot["coupled"], snapshot["build"])
    if (actual[-1] != d["build_admission"] or actual[-2] != d["coupling_completion"]
            or actual[-1]["actual_external_terminal_validation"] != d["actual_build_terminal_validation"]
            or actual[-2]["actual_build_terminal_chain"] != d["build_terminal_chain"]):
        raise ValueError("saved input-only returns differ from the immutable declared bindings")
    if verification_sink is not None:
        if phase != "run_entry" or type(verification_sink) is not list or verification_sink:
            raise ValueError("only the real complete run entry may supply one input verification witness")
        verification_sink.append({key:value for key,value in verified.items() if key != "typed_snapshot"})
    return actual


def prior_permission_failure_expected_files():
    """Exact opaque failed-history bytes; nested old bindings are not inputs."""
    return {
        str(FAILED_PERMISSION_TERMINAL / "terminal_return.json"): FAILED_PERMISSION_TERMINAL_SHA,
        str(FAILED_PERMISSION_TERMINAL / "analysis_full_stdout.json"):
            "ca5e4de2769f61761e2eb37d68230558ba512743b4369efc6341ed2ac47e719a",
        str(FAILED_PERMISSION_TERMINAL / "analysis_full_stderr.txt"):
            "78b9d8cc4246ca377f5aefe4c2861520dc6e44a4c066564d4cc5a883ce8cdbdd"}


def prior_permission_failure_input():
    """Verify actual failed supervision INPUT only, without old graph replay."""
    files = prior_permission_failure_expected_files()
    require(FAILED_PERMISSION_FACTORY, FAILED_PERMISSION_FACTORY_SHA)
    receipt_path = terminal_file(FAILED_PERMISSION_TERMINAL / "terminal_return.json",
        FAILED_PERMISSION_TERMINAL, FAILED_PERMISSION_TERMINAL_SHA)
    evidence = strict_terminal_json(receipt_path)
    if (evidence["schema"] != TERMINAL_SCHEMA or evidence["record_producer"] != "root"
            or type(evidence["returncode"]) is not int or evidence["returncode"] != 1
            or evidence["actual_tool_terminal_return_observed"] is not True
            or evidence["record_written_after_actual_terminal_return"] is not True
            or evidence["source"] != dict(path=str(FAILED_PERMISSION_FACTORY), sha256=FAILED_PERMISSION_FACTORY_SHA)
            or evidence["scientific_predicates_evaluated"] is not False
            or evidence["AAA_accuracy_qualified"] is not False or evidence["ABA_admitted"] is not False
            or evidence["classification"] != "RANK1_FACTOR_CACHE_REFERENCE_FAILED_NO_RETRY"
            or evidence["failed_eight_gate_or_runtime_witness_only"] is not True
            or evidence["no_qualification_from_this_receipt"] is not True):
        raise ValueError("actual Root permission-failure INPUT witness required; no qualification is inherited")
    stdout_path = FAILED_PERMISSION_TERMINAL / "analysis_full_stdout.json"
    stderr_path = FAILED_PERMISSION_TERMINAL / "analysis_full_stderr.txt"
    if (evidence["full_stdout"] != dict(path=str(stdout_path), sha256=files[str(stdout_path)])
            or evidence["full_stderr"] != dict(path=str(stderr_path), sha256=files[str(stderr_path)])):
        raise ValueError("complete original permission-failure stdout/stderr identity differs")
    terminal_file(stdout_path, FAILED_PERMISSION_TERMINAL, files[str(stdout_path)])
    terminal_file(stderr_path, FAILED_PERMISSION_TERMINAL, files[str(stderr_path)])
    returned = strict_terminal_json(stdout_path)
    if (returned["classification"] != "RANK1_FACTOR_CACHE_REFERENCE_FAILED_NO_RETRY"
            or type(returned["completed_commands"]) is not int or returned["completed_commands"] != 0
            or returned["error"] != "PermissionError(1, 'Operation not permitted')"
            or returned["AAA_accuracy_qualified"] is not False or returned["ABA_admitted"] is not False
            or returned["ABA_started"] is not False or returned["transport_launched"] is not False
            or any(key in returned for key in ("AAA_classification", "original_eight_checks",
                "reference_assessment", "reference_qualification"))):
        raise ValueError("the old permission failure did not stop before scientific assessment")
    stderr = stderr_path.read_text(encoding="utf-8")
    if ("subprocess.run(['/bin/ps'" not in stderr
            or "PermissionError: [Errno 1] Operation not permitted: '/bin/ps'" not in stderr
            or "self.bounded.terminate_group(process)" not in stderr
            or "os.killpg(pgid, signal.SIGTERM)" not in stderr
            or not stderr.rstrip().endswith("PermissionError: [Errno 1] Operation not permitted")):
        raise ValueError("actual ps sampling and own-group cleanup permission denial required")
    # No paths, old graph values, old output members, or old tail/resource PASS
    # enter the typed snapshot.  The three opaque proof files and old factory
    # remain fresh byte-verified owners; only the witnessed failure is saved.
    return dict(schema="AXMAT_PRIOR_SUPERVISOR_PERMISSION_FAILURE_INPUT_ONLY_V1",
        classification="RANK1_FACTOR_CACHE_REFERENCE_FAILED_NO_RETRY", actual_returncode=1,
        actual_completed_commands=0, supervisor_error_kind="PermissionError",
        ps_sampling_permission_denied=True, own_group_cleanup_permission_denied=True,
        old_nested_bindings_promoted_to_current_inputs=False, old_tail_is_scientific_evidence=False,
        scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def create_input_graph(snapshot, files, resource_roots, read_trace, with_consumer_plans=False):
    """Explicit transitive owners; actual fresh bytes, never a scientific PASS."""
    gm = graph_helper()
    transitive = module(require(TRANSITIVE_OWNER_HELPER, TRANSITIVE_OWNER_HELPER_SHA), "reference_transitive_input_owners")
    scientific = module(require(SCIENTIFIC_OWNER_HELPER, SCIENTIFIC_OWNER_HELPER_SHA), "reference_scientific_input_owners")
    def seed(path, category, wanted=None, owner=None):
        path = Path(path)
        item = dict(path=str(path), category=category, owner=owner or ("actual input seed " + str(path)),
                    kind="json" if path.suffix == ".json" else "file")
        if wanted is None:
            item["reason"] = "New explicit declaration of existing input bytes only; no old scientific PASS"
        else:
            item["sha256"] = wanted
        return item
    seeds = [seed(path, "code_environment", wanted) for path, wanted in (
        (Path(__file__).resolve(), digest(Path(__file__).resolve())),
        (GRAPH_HELPER, GRAPH_HELPER_SHA), (SCIENTIFIC_OWNER_HELPER, SCIENTIFIC_OWNER_HELPER_SHA),
        (TRANSITIVE_OWNER_HELPER, TRANSITIVE_OWNER_HELPER_SHA), (CONSUMER_OWNER_HELPER, CONSUMER_OWNER_HELPER_SHA),
        (FAILED_REFERENCE_FACTORY, FAILED_REFERENCE_FACTORY_SHA), (TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA),
        (FAILED_PERMISSION_FACTORY, FAILED_PERMISSION_FACTORY_SHA),
        (COUPLING_FACTORY, COUPLING_FACTORY_SHA), (BUILD_FACTORY, BUILD_SOURCE_SHA), (FULL_FACTORY, FULL_SOURCE_SHA))]
    seeds += [seed(PROD / "prepared.json", "production_prepared_layout", snapshot["cold_terminal_evidence"]["prepared"]["sha256"]),
        seed(PROD / "AAA/run_status.json", "completed_cold_case", snapshot["cold_terminal_evidence"]["run_status"]["sha256"]),
        seed(BUILD / "declaration.json", "cache_build", snapshot["coupled"]["actual_build_terminal_chain"]["declaration"]["sha256"]),
        seed(BUILD / "seal.json", "cache_build", snapshot["build"]["build_seal_sha256"]),
        seed(BUILD / "driver_result.json", "cache_build", snapshot["coupled"]["actual_build_terminal_chain"]["driver_result"]["sha256"]),
        seed(BUILD_TERMINAL / "terminal_return.json", "terminal_failure_proofs", snapshot["build"]["actual_external_terminal_evidence"]["sha256"]),
        seed(COLD_TERMINAL / "terminal_return.json", "completed_cold_case", COLD_TERMINAL_SHA),
        seed(FAILED_REFERENCE_TERMINAL / "terminal_return.json", "terminal_failure_proofs", FAILED_REFERENCE_TERMINAL_SHA),
        seed(FAILED_COLD_TERMINAL / "terminal_return.json", "terminal_failure_proofs", FAILED_COLD_TERMINAL_SHA),
        seed(FULL / "declaration.json", "code_environment"), seed(CAUSAL / "declaration.json", "code_environment"),
        seed(COUPLING / "declaration.json", "production_prepared_layout", snapshot["info"]["declaration"]["sha256"])]
    closure = transitive.transitive_input_owners(artifacts_root=ART, production_root=PROD,
        build_root=BUILD, typed_snapshot=snapshot, root_paths=seeds)
    extra = scientific.scientific_input_owners(ART, PROD, OUT / "fine", snapshot["info"])
    owners = list(closure["owners"]) + list(extra["owners"])
    owners.append(dict(owner="Opaque original Root permission-failure body and complete stdout/stderr; no nested old inputs or scientific outcome promoted",
        category="terminal_failure_proofs", expected_files=prior_permission_failure_expected_files()))
    owners.append(dict(owner="Actual factory declared original dependencies and newly generated byte-exact source bindings",
                       category="reference_scientific_dependencies", expected_files=dict(files)))
    owners.append(dict(owner="Actual separate CE environment complete numerical package files",
                       category="code_environment", expected_files=dict(snapshot["environment"]["files"])))
    # platform.mac_ver reads this exact macOS product metadata endpoint during
    # the original full input admission.  It is an explicit OS input owner,
    # never an allowance for arbitrary trace-discovered system files.
    system_version = Path("/System/Library/CoreServices/SystemVersion.plist")
    owners.append(dict(owner="Actual platform.mac_ver macOS product metadata input",
        category="code_environment", expected_files={str(system_version): digest(system_version)}))
    processor_probe = Path("/usr/bin/uname")
    if Path(shutil.which("uname") or "").resolve() != processor_probe:
        raise ValueError("actual OS processor probe must resolve to the explicitly declared uname endpoint")
    owners.append(dict(owner="Actual original platform.processor uname -p OS probe executable",
        category="code_environment", expected_files={str(processor_probe): digest(processor_probe)}))
    utc_metadata = Path("/usr/share/zoneinfo/UTC")
    owners.append(dict(owner="Actual original full input admission UTC timezone metadata read",
        category="code_environment", expected_files={str(utc_metadata): digest(utc_metadata)}))
    snapshot = dict(snapshot, actual_system_identity=actual_system_identity())
    live_io = [dict(kind="subprocess_stdio", owner="Actual original stdlib platform.processor OS probe stdio",
        reason="Exact uname -p processor query only; its pipe is live OS I/O, never scientific or immutable input bytes",
        scope=gm.LIVE_IO_SCOPE, command=dict(literal_executable="uname", executable=str(processor_probe),
            argv=["uname", "-p"], cwd=str(ROOT), environment=None, path_environment=os.environ.get("PATH", os.defpath))),
        gm.capture_live_character_device(os.devnull,
            owner="Actual original platform.processor null stderr device",
            reason="Exact actual stdlib OS-probe stdio device only; no file or scientific value is inherited")]
    wanted = {}
    for owner in owners:
        for name, value in owner["expected_files"].items():
            if name in wanted and wanted[name] != value:
                raise ValueError("conflicting actual transitive input owners: " + name)
            wanted[name] = value
    new_paths = dict(closure["new_decl_paths"])
    absence_inputs = {}
    def runtime_cache_candidate(path, owner, reason):
        path = Path(path)
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            mode = None
        if mode is not None and stat.S_ISREG(mode):
            if str(path) not in wanted:
                new_paths.setdefault(str(path), dict(owner=owner, category="code_environment", reason=reason))
            return True
        if mode is not None:
            raise ValueError("runtime cache candidate is not a regular file or genuinely absent: " + str(path))
        absence_inputs[str(path)] = dict(owner=owner, category="code_environment",
            reason=reason + "; explicitly absent at declaration and freshly checked before/after each phase")
        return False
    interpreter_zip = Path("/Users/wen/miniforge3/envs/openmc-dev/lib/python312.zip")
    if str(interpreter_zip) not in sys.path:
        raise ValueError("original interpreter optional zip search candidate changed")
    runtime_cache_candidate(interpreter_zip, "Actual explicit CPython3.12 optional interpreter zip search input",
        "Exact interpreter import-search endpoint, INPUT only; no arbitrary missing read is allowed")
    for record in extra["input_records"]:
        if record["newly_declared_pin_required"] and record["path"] not in wanted:
            new_paths[record["path"]] = dict(owner="; ".join(record["owners"]),
                category="reference_scientific_dependencies",
                reason="Explicit original child-read endpoint lacked an older digest; newly declared INPUT only")
    # An owner may require a new path even when another owner has an old pin.
    # Keep the role explicit in both cases; the phase rejects any SHA conflict.
    for owner in owners:
        for name in owner.get("newly_declared_input_paths", []):
            new_paths.setdefault(name, dict(owner=owner["owner"], category=owner["category"],
                reason="Explicit newly declared input role; another typed owner may also pin the same bytes"))
    specs = list(closure["namespace_specs"])
    specs += [dict(root=item["root"], owner=item["owner"], category="reference_scientific_dependencies",
        files={}, symlinks={}, manifest_is_namespace_exhaustive=False) for item in extra["namespace_requirements"]]
    # Cover late scientific imports too: complete numerical-package namespaces
    # include actual cache/extension bytes, with new cache pins INPUT_ONLY.
    numerical_import_roots = []
    for name in ("numpy", "scipy", "h5py", "openmc"):
        package = __import__(name)
        literal = Path(package.__file__).absolute().parent
        canonical = literal.resolve(strict=True)
        numerical_import_roots.append(str(literal))
        specs.append(dict(root=str(canonical), owner="Actual complete CE numerical package namespace " + name,
            category="code_environment", files={}, symlinks={}, manifest_is_namespace_exhaustive=False))
    # The original imports query installed distribution identities (for
    # example endf's METADATA). Own each actual distribution metadata scope
    # explicitly instead of allowing arbitrary trace-discovered package data.
    metadata_parent = Path("/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/site-packages")
    for metadata_root in sorted(metadata_parent.glob("*.dist-info")):
        if metadata_root.is_symlink() or not metadata_root.is_dir():
            raise ValueError("actual CE distribution metadata must be a canonical directory")
        specs.append(dict(root=str(metadata_root), owner="Actual CE installed distribution metadata " + metadata_root.name,
            category="code_environment", files={}, symlinks={}, manifest_is_namespace_exhaustive=False))
    specs.append(dict(root=str(PROD / "runtime"), owner="Actual immutable production runtime complete namespace",
        category="code_environment", files={}, symlinks={}, manifest_is_namespace_exhaustive=False))
    count = snapshot["coupled"]["completed_maps"]
    specs += [dict(root=str(root), owner="Complete actual new cold stage " + str(root), category="completed_cold_case",
                   files={}, symlinks={}, manifest_is_namespace_exhaustive=False)
              for root in [PROD / "archives", PROD / "training", PROD / "AAA/bootstrap",
                           *[PROD / "AAA" / f"map{n:03d}" for n in range(1, count+1)]]]
    # Only explicit immutable scopes are scanned. Dynamic axial-family resources
    # are checked live by the genuine original resource class, never snapshotted.
    namespace_inputs = []
    path_inputs = set(wanted) | set(new_paths) | set(numerical_import_roots)
    for alias_requirement in closure["alias_specs"]:
        alias_path = Path(alias_requirement["path"])
        if "text" in alias_requirement:
            if not alias_path.is_symlink() or os.readlink(alias_path) != alias_requirement["text"]:
                raise ValueError("original explicitly owned alias text differs: " + str(alias_path))
        if "expected_resolved_target" in alias_requirement:
            if str(alias_path.resolve(strict=True)) != alias_requirement["expected_resolved_target"]:
                raise ValueError("original native-library alias target differs: " + str(alias_path))
        path_inputs.add(str(alias_path))
    seen_specs = {}
    for spec in specs:
        root = Path(spec["root"])
        regular, links = {}, {}
        pending = [root]
        if root.is_symlink() or not root.is_dir():
            raise ValueError("immutable namespace root must be a canonical directory: " + str(root))
        while pending:
            directory = pending.pop()
            with os.scandir(directory) as entries:
                values = sorted(entries, key=lambda item: item.name)
            for entry in values:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                relative = str(path.relative_to(root))
                if stat.S_ISREG(mode):
                    old = wanted.get(str(path)) or spec.get("files", {}).get(relative)
                    if old is None:
                        old = gm.strict_pin(str(path))["sha256"]
                        new_paths[str(path)] = dict(owner=spec["owner"], category=spec["category"],
                            reason="Actual namespace member beyond an explicitly partial older manifest; new INPUT byte binding only")
                    regular[relative] = old
                    path_inputs.add(str(path))
                elif stat.S_ISLNK(mode):
                    actual_alias = next(value for value in gm.capture_aliases([str(path)]) if value["path"] == str(path))
                    links[relative] = {key: value for key, value in actual_alias.items() if key != "path"}
                    path_inputs.add(str(path))
                    if actual_alias["kind"] == "file":
                        old = wanted.get(str(path)) or wanted.get(actual_alias["target"])
                        if old is None:
                            new_paths[str(path)] = dict(owner=spec["owner"], category=spec["category"],
                                reason="Declared exact immutable namespace alias target, INPUT byte binding only")
                        else:
                            links[relative]["sha256"] = old
                elif stat.S_ISDIR(mode):
                    pending.append(path)
                else:
                    raise ValueError("immutable namespace contains a nonregular endpoint: " + str(path))
        if spec.get("manifest_is_namespace_exhaustive") is True:
            if set(regular) != set(spec["files"]) or {name: value["text"] for name,value in links.items()} != spec.get("symlinks", {}):
                raise ValueError("original exhaustive immutable namespace differs: " + str(root))
            for name, expected in spec["files"].items():
                if regular[name] != expected:
                    raise ValueError("original exhaustive namespace expected SHA differs: " + str(root / name))
        prior = seen_specs.get(str(root))
        this = (regular, links)
        if prior is not None and prior != this:
            raise ValueError("conflicting namespace owners for " + str(root))
        owners.append(dict(owner=spec["owner"] + " actual exhaustive regular namespace inputs",
            category=spec["category"], expected_files={str(root / name): sha for name,sha in regular.items()}))
        if prior is None:
            seen_specs[str(root)] = this
            namespace_inputs.append((spec, regular, links))
    # Explicit interpreter-library owners cover standard-library imports made
    # by later science stages. Third-party libraries are scoped separately above.
    standard_root = Path("/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12")
    pending_standard = [standard_root]
    while pending_standard:
        directory = pending_standard.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    if path != standard_root / "site-packages":
                        pending_standard.append(path)
                elif stat.S_ISREG(mode) or stat.S_ISLNK(mode):
                    if path.is_file() and str(path) not in wanted:
                        new_paths.setdefault(str(path), dict(owner="Actual explicit CE interpreter-library input",
                            category="code_environment", reason="New complete runtime byte binding; no prior source/bytecode reconstruction or science PASS"))
                        path_inputs.add(str(path))
                else:
                    raise ValueError("actual interpreter library contains a nonregular endpoint: " + str(path))
    # Modules loaded before the audit context are still explicit dependencies.
    # Bind both their source/extension and any real loader-selected cache bytes;
    # this makes no claim of reconstructing a historic bytecode compilation.
    runtime_root = Path("/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12")
    for original_source in sorted(wanted):
        source_path = Path(original_source)
        if source_path.suffix == ".py" and source_path.is_relative_to(ROOT / "validation"):
            cache_path = Path(importlib.util.cache_from_source(str(source_path)))
            if runtime_cache_candidate(cache_path, "Actual interpreter-selected cache for pinned source " + original_source,
                    "Explicit pinned-source-associated runtime cache INPUT; no historic bytecode reconstruction or science PASS"):
                path_inputs.add(str(cache_path))
    for loaded_name, loaded in sorted(sys.modules.items()):
        for attribute in ("__file__", "__cached__"):
            value = getattr(loaded, attribute, None)
            if not isinstance(value, str):
                continue
            path = Path(value).absolute()
            if (path.is_file() and (path.is_relative_to(runtime_root) or path.is_relative_to(ROOT / "validation"))
                    and str(path) not in wanted):
                new_paths.setdefault(str(path), dict(owner="Actual loaded CE runtime module " + loaded_name + "." + attribute,
                    category="code_environment", reason="Explicit actual runtime input bytes newly declared; no inherited science or source-to-bytecode reconstruction"))
                path_inputs.add(str(path))
    # Actual Python import-open paths need an explicit runtime input declaration.
    # Unknown scientific/data endpoints are never granted owners by the trace.
    runtime_root = Path("/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12")
    canonical_owned = {str(Path(name).resolve(strict=True)) for name in path_inputs if Path(name).is_file()}
    unowned_read_paths = set()
    for record in read_trace["records"]:
        name = record.get("path")
        if record.get("kind") == "descriptor":
            observed = record.get("descriptor_observation", {})
            if observed.get("kind") == "regular":
                name = observed.get("canonical_path")
            else:
                # The helper independently requires actual fstat, real stdlib
                # Popen/command ownership and an exact allowed stdio role.
                # This branch grants no byte owner or unresolved-FD allowance.
                continue
        if name is None:
            raise ValueError("unresolved read-open descriptor in actual original input admission")
        if name == os.devnull:
            # Only the separately declared, live, command-owned character
            # endpoint can satisfy this record in the helper's strict check.
            continue
        path = Path(name)
        if path.is_file() and name not in path_inputs and str(path.resolve(strict=True)) not in canonical_owned:
            if path.is_relative_to(runtime_root) and path.suffix in (".py", ".pyc", ".so", ".json"):
                new_paths[name] = dict(owner="Actual original full-ready Python runtime import-read endpoint",
                    category="code_environment", reason="New actual runtime bytes; no claim of historical bytecode reconstruction or science PASS")
                path_inputs.add(name)
                canonical_owned.add(str(path.resolve(strict=True)))
            else:
                unowned_read_paths.add(name)
    if unowned_read_paths:
        raise ValueError("actual original read-open files have no explicit transitive typed owner: "
                         + json.dumps(sorted(unowned_read_paths)))
    for absent_path in absence_inputs:
        ancestor = Path(absent_path).parent
        while not os.path.lexists(ancestor):
            ancestor = ancestor.parent
        path_inputs.add(str(ancestor))
    aliases = gm.capture_aliases(sorted(path_inputs | set(new_paths)))
    namespaces = [gm.explicit_sealed_namespace(str(spec["root"]), regular, links,
        owner=spec["owner"], category=spec["category"], aliases=aliases)
        for spec, regular, links in namespace_inputs]
    expected_points = {f"statepoint.{n:04d}.h5" for n in range(101, 2101)}
    if {path.name for path in (CE / "AAA").glob("statepoint.*.h5")} != expected_points:
        raise ValueError("actual original independent native sample glob must contain exactly all 2000 paths")
    coverage = {category:dict(minimum_files=1, minimum_bytes=0) for category in gm.CLOSURE_CATEGORIES}
    coverage["preserved_history"].update(minimum_files=719, minimum_bytes=26_531_360_918)
    coverage["completed_cold_case"].update(minimum_files=305, minimum_bytes=13_411_776_656)
    coverage["cache_build"].update(minimum_files=5148, minimum_bytes=137_556_759)
    coverage["capture"].update(minimum_files=1897)
    graph = gm.create_graph(typed_snapshot=snapshot, owners=owners, namespaces=namespaces,
        aliases=aliases, read_trace=read_trace, newly_declared_input_paths=new_paths,
        declared_new_source_roots=[str(SOURCE)], live_resource_roots=resource_roots,
        coverage_requirements=coverage, live_io_requirements=live_io, absence_inputs=absence_inputs)
    if not with_consumer_plans:
        return graph
    planner = module(require(CONSUMER_OWNER_HELPER, CONSUMER_OWNER_HELPER_SHA), "reference_consumer_input_owners")
    normalized = gm._expand_owner_table(graph["owners"], graph["requirements"])
    plans = {phase:planner.consumer_input_plan(phase=phase, full_graph=graph,
        normalized_owners=normalized, scientific_inventory=extra, declaration_files=files,
        parsed_metadata_documents=closure["parsed_json_documents"],
        production_runtime_root=str(PROD / "runtime")) for phase in CONSUMER_PHASES}
    return graph, plans


def declare(prepared_sha, status_sha, build_seal_sha, build_terminal_evidence, build_terminal_evidence_sha256):
    graph_module = graph_helper()
    with graph_module.ReadOpenAudit() as input_trace:
        env = environment()
        c, info, status, final, recipe, native, execution, coupled, build = ready(
            prepared_sha, status_sha, build_seal_sha, build_terminal_evidence, build_terminal_evidence_sha256)
        cold_evidence = cold_terminal_input(info, status)
        permission_failure_context = prior_permission_failure_input()
        require(FULL_FACTORY, FULL_SOURCE_SHA)
        full = module(FULL_FACTORY, "rank1_factor_cache_reference_guard")
        builder = module(BUILD_FACTORY, "rank1_factor_cache_reference_build_dependency")
        guard_files = builder.helper().guard_admission(full)
        guard_provenance = live_guard_provenance(full, c, info)
    read_trace = input_trace.snapshot()
    if SOURCE.exists() or OUT.exists() or TERMINAL.exists():
        raise ValueError("independent reference roots must be absent; no retry or overwrite")
    require(EXPORTER, EXPORTER_SHA)
    require(EXPORT_SOURCE, EXPORT_SOURCE_SHA)
    roots = sorted(set(info["resource_roots"]) | set(read(BUILD / "declaration.json")["resource_roots"])
        | set(read(FULL / "declaration.json")["resource_roots"])
        | set(read(CAUSAL / "declaration.json")["resource_roots"])
        | {str(path) for pattern in ("axial-material-*",) for path in ART.glob(pattern)}
        | {str(SOURCE), str(OUT), str(TERMINAL)})
    before = builder.DynamicHistoryResources(ART, roots, 8 * 2**30, 96 * 2**30, c.ResourceFailure).check()
    if before["artifact_bytes"] + RESERVE >= 96 * 2**30 or before["disk_free_bytes"] - RESERVE < 8 * 2**30:
        raise ValueError("complete history plus independent reassessment reserve exceeds unchanged caps")
    SOURCE.mkdir()
    write_new(SOURCE / "live_guard_provenance.json", guard_provenance)
    runtime = SOURCE / "runtime"
    runtime.mkdir()
    equivalence = {}
    for name in ("reference_statistics.py", "compare_balance_symmetry.py"):
        item = recipe["unchanged_reference_implementations"][name]
        shutil.copy2(item["path"], runtime / name)
        require(runtime / name, item["sha256"])
        equivalence[name] = dict(parent=item, candidate=pin(runtime / name), byte_exact=True)
    projection = read(recipe["observation_projection_recipe"]["path"])["helper"]
    require(projection["path"], projection["sha256"])
    shutil.copy2(projection["path"], runtime / "project_refined_observables.py")
    equivalence["projection"] = dict(parent=projection, candidate=pin(runtime / "project_refined_observables.py"), byte_exact=True)
    prior_review = read(recipe["physical_input_precheck"]["path"])["implementation"]
    require(PHYSICAL, prior_review["sha256"])
    equivalence["physical"] = patch(PHYSICAL, [
        ("PROD = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'",
         "PROD = Path(" + repr(str(PROD)) + ")", 1),
        ("OBS = ART / 'axial-material-qualified-AAA-white-trace-refined-observables-20261005'",
         "OBS = Path(" + repr(str(OUT / "fine")) + ")", 1),
        ("PREPARED_SHA = '024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'",
         "PREPARED_SHA = " + repr(prepared_sha), 1),
        ("    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)",
         "    from rank1_factor_cache_reference_admission import verified_prepared_input_context\n"
         "    info = verified_prepared_input_context(PREPARED_SHA, 'fine/physical')", 1)],
         runtime / "rank1_factor_cache_physical_identity.py", ("review",))
    original_collector = recipe["unchanged_reference_implementations"]["assess_qualified_AAA_white_trace_precision.py"]
    require(original_collector["path"], original_collector["sha256"])
    entry = '    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)'
    changes = [
        ("axial-material-production-qualified-AB-white-trace-20261004", PROD.name, 1),
        ("88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf", prepared_sha, 1),
        (entry, '    from rank1_factor_cache_reference_admission import verified_prepared_input_context, verify_measurement_admission\n'
         '    prepared, input_context = verified_prepared_input_context(PREPARED_SHA, "AAA/collect", with_context=True)\n'
         '    if len(sys.argv) != 2:\n        raise ValueError("explicit analysis declaration SHA256 required")\n'
         '    current_measurement = verify_measurement_admission(prepared, sys.argv[1], input_context)\n'
         '    analysis = Path(' + repr(str(OUT)) + ')', 1),
        ('    stats_path = case_dir / "statistics.json"', '    stats_path = analysis / "AAA/statistics.json"', 1),
        ('    currents_path = case_dir / "currents_balance_symmetry.json"', '    currents_path = analysis / "AAA/currents_balance_symmetry.json"', 1),
        ('    inputs_path = ce / "input_equivalence_AAA.json"', '    inputs_path = analysis / "input_equivalence_AAA.json"', 1),
        ('        measurement_admission=descriptor(case_dir / "measurement_admission.json"),',
         '        measurement_admission=descriptor(case_dir / "measurement_admission.json"),\n'
         '        rank1_factor_cache_measurement_admission=descriptor(analysis / "measurement_admission.json"),\n'
         '        complete_fine_observation_projection=descriptor(analysis / "observation/projection_receipt.json"),', 1),
        ('    write_new(case_dir / "reference_assessment.json", receipt)', '    write_new(analysis / "AAA/reference_assessment.json", receipt)', 1),
        ('        target = case_dir / "reference_qualification.json"', '        target = analysis / "AAA/reference_qualification.pending.json"', 1),
        ('        assessment=descriptor(case_dir / "reference_assessment.json")), indent=2))',
         '        assessment=descriptor(analysis / "AAA/reference_assessment.json")), indent=2))', 1)]
    equivalence["collector"] = patch(original_collector["path"], changes,
        runtime / "rank1_factor_cache_reference_collector.py", ("main",))
    host = ADMISSION
    for token, value in (("__PROD__", str(PROD)), ("__OUT__", str(OUT)), ("__PREPARED_SHA__", prepared_sha),
                         ("__FACTORY_PATH__", str(Path(__file__).resolve())),
                         ("__FACTORY_SHA__", digest(Path(__file__).resolve()))):
        if host.count(token) != 1:
            raise ValueError("reference admission template token ambiguous")
        host = host.replace(token, repr(value), 1)
    (runtime / "rank1_factor_cache_reference_admission.py").write_text(host)
    shutil.copy2(PROD / "runtime/run_bounded_dragon.py", runtime / "run_bounded_dragon.py")
    write_new(SOURCE / "source_equivalence.json", dict(
        schema="AXMAT_RANK1_FACTOR_CACHE_REFERENCE_SOURCE_EQUIVALENCE_V1", implementations=equivalence,
        exporter=pin(EXPORTER), exporter_source=pin(EXPORT_SOURCE), native_export_arithmetic_byte_exact=True,
        physical_review_precondition_binding_changed_only=True,
        all_original_physical_conditions_restored_byte_exact=True,
        physical_track_geometry_AST_exact=True, scientific_statistics_currents_and_projection_byte_exact=True,
        original_collector_scientific_conditions_restored_exactly=True,
        frozen_scientific_factory_template=pin(TEMPLATE_FACTORY),
        factory_revision_scope="Actual identity/terminal/coupled-log bindings, complete fresh input graph with real declaration-only input semantics, and live family resource guards; physical/statistical/projection/collector criteria unchanged",
        original_qualified_conditions_and_qualify_ABA_call_retained=True,
        frozen_module_identity_reassigned=False))
    write_new(SOURCE / "analysis_environment.json", env)
    view = copy.deepcopy(read(info["case_spec"]["path"]))
    view["geometry"]["cells_per_zone"] = 4
    view["observation_projection_view"] = dict(native_case_spec=info["case_spec"], native_cells=48,
        original_observation_cells=12, solver_not_changed_by_this_view=True,
        fixed_projection_recipe=recipe["observation_projection_recipe"])
    write_new(SOURCE / "observation_case_spec.json", view)
    inputs = {"track.xsm": PROD / "AAA/bootstrap/initial_axial_track.xsm",
              "axial.xsm": final / "closed_axial.xsm", "macro.xsm": PROD / "AAA/bootstrap/initial_axial_macrolib.xsm"}
    files = dict(execution["files"])
    files.update(env["files"])
    files.update(prior_permission_failure_expected_files())
    files[str(FAILED_PERMISSION_FACTORY)] = FAILED_PERMISSION_FACTORY_SHA
    files.update({str(CE / "AAA" / name): sha for name, sha in native["outputs"].items()})
    files.update({str(path): digest(path) for path in [Path(__file__).resolve(), TEMPLATE_FACTORY, COUPLING_FACTORY, BUILD_FACTORY, FULL_FACTORY,
        GRAPH_HELPER, SCIENTIFIC_OWNER_HELPER, TRANSITIVE_OWNER_HELPER, CONSUMER_OWNER_HELPER,
        PHYSICAL, EXPORTER, EXPORT_SOURCE, OLD_SOURCE / "refined_reference_analysis_recipe.json",
        PROD / "prepared.json", PROD / "AAA/run_status.json", final / "result.json",
        PROD / "archives/result.json", PROD / "training/result.json", PROD / "AAA/bootstrap/result.json",
        Path(info["case_spec"]["path"]), Path(info["rank_addendum"]["path"]), BUILD / "seal.json",
        CE / "AAA/native_result.json", CE / "AAA/execution.json", CE / "AAA/reference_contract.json",
        CE / "AAA/measurement_admission.json", CE / "AAA/openmc.log", CE / "statistical_rules.json",
        CE / "balance_symmetry_rules.json", *inputs.values(), *guard_files,
        *[path for path in SOURCE.rglob("*") if path.is_file()]]})
    for item in [recipe[key] for key in ("observation_projection_recipe", "projection_precheck", "native_export_source_proof", "physical_input_precheck")]:
        files[item["path"]] = item["sha256"]
    files.update({str(PROD / name): sha for name, sha in info["local_files"].items()})
    files.update(coupled["all_stage_logs"])
    for item in [coupled["stages"], coupled["actual_complete_run_claim"], coupled["coupling_declaration"], coupled["coupling_revision"],
            coupled["coupling_equivalence"], *coupled["complete_stage_seals"], *coupled["actual_build_terminal_chain"].values()]:
        files[item["path"]] = item["sha256"]
    verify(files)
    common = ["--case-spec", str(OUT / "observation_case_spec.json"), "--contract", str(CE / "AAA/reference_contract.json"),
        "--statepoints", str(CE / "AAA"), "--production-regions", str(OUT / "observation/observables.regions.csv"),
        "--production-summary", str(OUT / "observation/observables.summary.txt")]
    commands = [[str(EXPORTER), "track.xsm", "axial.xsm", "macro.xsm", "observables"],
        [str(PYTHON), str(OUT / "runtime/rank1_factor_cache_physical_identity.py")],
        [str(PYTHON), str(Path(__file__).resolve()), "project-worker", "--sha256", "__DECLARATION_SHA256__"],
        [str(PYTHON), str(OUT / "runtime/reference_statistics.py"), "analyze", "--rules", str(OUT / "statistical_rules.json"),
         *common, "--output", str(OUT / "AAA/statistics.json")],
        [str(PYTHON), str(OUT / "runtime/compare_balance_symmetry.py"), "compare", "--rules", str(OUT / "balance_symmetry_rules.json"),
         "--statistics-rules", str(OUT / "statistical_rules.json"), *common,
         "--production-faces", str(OUT / "observation/observables.faces.csv"), "--output", str(OUT / "AAA/currents_balance_symmetry.json")],
        [str(PYTHON), str(OUT / "runtime/rank1_factor_cache_reference_collector.py"), "__DECLARATION_SHA256__"]]
    d = dict(schema="AXMAT_RANK1_FACTOR_CACHE_COMPLETE_ORIGINAL_GATE_REFERENCE_V1", declared_unix=time.time(), files=files,
        production_prepared=pin(PROD / "prepared.json"), AAA_status=pin(PROD / "AAA/run_status.json"),
        final_stage_seal=pin(final / "result.json"), build_admission=build,
        actual_build_terminal_evidence=build["actual_external_terminal_evidence"],
        actual_build_terminal_validation=build["actual_external_terminal_validation"],
        build_terminal_chain=coupled["actual_build_terminal_chain"], coupling_completion=coupled,
        frozen_scientific_template=pin(TEMPLATE_FACTORY), actual_coupling_factory=pin(COUPLING_FACTORY),
        original_recipe_dependency=pin(OLD_SOURCE / "refined_reference_analysis_recipe.json"),
        old_recipe_is_dependency_only=True, actual_new_candidate_receipt_required=True,
        old_assessment_or_qualification_inherited=False,
        old_native_measurement_receipt_is_reference_sample_dependency_only=True,
        source_equivalence=pin(SOURCE / "source_equivalence.json"), analysis_environment=pin(SOURCE / "analysis_environment.json"),
        live_guard_provenance=pin(SOURCE / "live_guard_provenance.json"),
        exporter=pin(EXPORTER), exporter_source=pin(EXPORT_SOURCE), source_inputs={str(path): digest(path) for path in inputs.values()},
        staged_inputs={name: pin(path) for name, path in inputs.items()}, commands=commands, labels=list(LABELS),
        total_wall_seconds=TOTAL_WALL, native_export_stage_wall_seconds=60, rss_cap_mib=RSS_CAP,
        threads=1, retries=0, numeric_children_at_once=1, resource_roots=roots, resources_before=before,
        min_free_bytes=8 * 2**30, artifact_budget_bytes=96 * 2**30, archive_reserve_bytes=RESERVE,
        archive_resource_roots=list(ARCHIVE_ROOTS), archive_byte_scope=ARCHIVE_SCOPE,
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_guard_bound_to_actual_build_factory=pin(BUILD_FACTORY),
        resource_scope_contract=build["resource_scope_contract"],
        total_wall_scope="Run entry through actual complete closeout tail; all six stages and native export included",
        actual_external_terminal_return_contract=terminal_contract(),
        original_eight_gates=list(GATES), fixed_history=recipe["fixed_history"], transport_launched=False,
        AAA_accuracy_qualified=False, ABA_admitted=False,
        scope="Actual new moment-order AAA; complete saved fine fields and original physical bins, one global normalization, all original sample history and eight original scientific gates.")
    snapshot = dict(scope="ORIGINAL_FULL_READY_INPUT_SEMANTICS_ONLY", info=info, status=status,
        final=str(final), recipe=recipe, native=native, execution=execution, coupled=coupled, build=build,
        environment=env, cold_terminal_evidence=cold_evidence, prior_permission_failure_input=permission_failure_context,
        scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False)
    graph, consumer_plans = create_input_graph(snapshot, files, roots, read_trace, with_consumer_plans=True)
    # The graph is machine-read input evidence; compact encoding reduces parse
    # memory without removing any owner, byte digest, alias, trace, or snapshot.
    with (SOURCE / "input_graph.json").open("x") as stream:
        json.dump(graph, stream, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
    gm = graph_helper()
    parent_graph = pin(SOURCE / "input_graph.json")
    phase_graphs, plan_pins = {}, {}
    for phase in CONSUMER_PHASES:
        plan = consumer_plans[phase]
        plan_path = SOURCE / ("consumer_plan." + phase.replace("/", "-") + ".json")
        source_plan_receipt = {key:value for key,value in plan.items()
            if key not in ("owners", "newly_declared_input_paths", "new_input_pins", "namespaces")}
        source_plan_receipt["selected_namespace_root_sequence"] = [value["root"] for value in plan["namespaces"]]
        write_new(plan_path, source_plan_receipt)
        plan_pins[phase] = pin(plan_path)
        alias_inputs = set(plan["selected_paths"])
        alias_inputs.update(value["root"] for value in plan["namespaces"])
        for absent in graph["absence_inputs"]:
            ancestor = Path(absent).parent
            while not os.path.lexists(ancestor):
                ancestor = ancestor.parent
            alias_inputs.add(str(ancestor))
        aliases = gm.capture_aliases(sorted(alias_inputs))
        scope = dict(schema=gm.CONSUMER_CONTRACT_SCHEMA, phase=phase, parent_input_graph=parent_graph,
            dependency_selection=gm.CONSUMER_SELECTION,
            full_original_input_semantics_replayed=False, complete_global_closure_claimed=False)
        phase_snapshot = consumer_snapshot(info, status, recipe, graph["typed_snapshot"]["actual_system_identity"], phase)
        phase_owners = plan["owners"] + [dict(owner=gm.CONSUMER_PARENT_OWNER, category="code_environment",
            expected_files={parent_graph["path"]: parent_graph["sha256"]})]
        inputs = {path:{key:value for key,value in item.items() if key != "binding_role"}
            for path,item in plan["newly_declared_input_paths"].items()}
        absent_inputs = {path:{key:value for key,value in item.items() if key != "binding_role"}
            for path,item in graph["absence_inputs"].items()}
        phase_graph = gm.create_graph(typed_snapshot=phase_snapshot, owners=phase_owners,
            namespaces=plan["namespaces"], aliases=aliases, read_trace=(),
            newly_declared_input_paths=inputs,
            declared_new_source_roots=graph["declared_new_source_roots"], live_resource_roots=graph["live_resource_roots"],
            coverage_requirements={}, live_io_requirements=graph["live_io_requirements"],
            absence_inputs=absent_inputs, consumer_scope=scope)
        if phase_graph["newly_declared_input_pins"] != plan["new_input_pins"]:
            raise ValueError("consumer graph cannot manufacture a new interpretation of its parent's input bytes")
        if (phase_graph["requirements"]["paths"] != sorted(set(plan["selected_paths"]) | {parent_graph["path"]})
                or phase_graph["namespaces"] != plan["namespaces"]):
            raise ValueError("actual consumer declaration lost or added an explicit source input or namespace")
        path = SOURCE / ("input_graph." + phase.replace("/", "-") + ".json")
        with path.open("x") as stream:
            json.dump(phase_graph, stream, separators=(",", ":"), allow_nan=False)
            stream.write("\n")
        phase_graphs[phase] = pin(path)
    d.update(input_graph=pin(SOURCE / "input_graph.json"), input_graph_factory=pin(Path(__file__).resolve()),
        input_graph_helper=pin(GRAPH_HELPER), transitive_input_owner_helper=pin(TRANSITIVE_OWNER_HELPER),
        scientific_input_owner_helper=pin(SCIENTIFIC_OWNER_HELPER), consumer_input_owner_helper=pin(CONSUMER_OWNER_HELPER),
        consumer_input_graphs=phase_graphs, consumer_input_source_plans=plan_pins,
        input_graph_scope_protocol="COMPLETE_GLOBAL_ENTRY_FINAL_AND_EXPLICIT_CONSUMER_INPUTS_V1",
        full_original_input_semantics_executed_on_actual_declare=True,
        input_semantics_reuse_requires_actual_external_declaration_exit_zero=True,
        complete_global_input_graph_phase_labels=["prepare", "run_entry", "run_final_immutable_input_closeout", "completed_reference_qualification_handoff"],
        explicit_consumer_input_graph_phase_labels=list(CONSUMER_PHASES),
        consumer_handoff_returns_only_source_audited_consumed_fields=True,
        consumer_handoff_requires_this_actual_parent_complete_global_entry=True,
        graph_contains_no_new_scientific_PASS=True)
    write_new(SOURCE / "declaration.json", d)
    namespace = source_namespace()
    write_new(SOURCE / "source_inventory.json", dict(files={name:digest(SOURCE / name) for name in namespace["files"]},
        directories=namespace["directories"], symlinks=namespace["symlinks"]))
    if archive_bytes() >= RESERVE:
        raise ValueError("complete declared SOURCE plus OUT exceeds the unchanged 256MiB archive reserve")
    print(json.dumps(dict(classification="DECLARED_NEW_RANK1_INPUT_GRAPH_REFERENCE_NOT_PREPARED_OR_RUN",
        declaration=pin(SOURCE / "declaration.json"), input_graph=pin(SOURCE / "input_graph.json"), output=str(OUT),
        scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False)))


def admission(expected, prepared=False, allow_already_existing_ABA=False, phase="input_admission", input_terminal_sha=None,
              verification_sink=None):
    d = read(require(SOURCE / "declaration.json", expected))
    if (d["schema"] != "AXMAT_RANK1_FACTOR_CACHE_COMPLETE_ORIGINAL_GATE_REFERENCE_V1"
            or d["total_wall_seconds"] != TOTAL_WALL or d["rss_cap_mib"] != RSS_CAP
            or d["threads"] != 1 or d["retries"] != 0 or d["numeric_children_at_once"] != 1
            or d["min_free_bytes"] != 8 * 2**30 or d["artifact_budget_bytes"] != 96 * 2**30
            or d["archive_reserve_bytes"] != RESERVE or d["native_export_stage_wall_seconds"] != 60
            or d["archive_resource_roots"] != list(ARCHIVE_ROOTS) or d["archive_byte_scope"] != ARCHIVE_SCOPE
            or d["labels"] != list(LABELS) or d["original_eight_gates"] != list(GATES)
            or d["actual_external_terminal_return_contract"] != terminal_contract()
            or d["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or d["resource_scope_contract"] != module(require(BUILD_FACTORY, BUILD_SOURCE_SHA),
                "rank1_factor_cache_reference_build_dependency").resource_scope_contract()
            or d["resource_guard_bound_to_actual_build_factory"] != pin(require(BUILD_FACTORY, BUILD_SOURCE_SHA))
            or d["frozen_scientific_template"] != pin(require(TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA))
            or d["actual_coupling_factory"] != pin(require(COUPLING_FACTORY, COUPLING_FACTORY_SHA))
            or d["input_graph_scope_protocol"] != "COMPLETE_GLOBAL_ENTRY_FINAL_AND_EXPLICIT_CONSUMER_INPUTS_V1"
            or d["consumer_input_owner_helper"] != pin(require(CONSUMER_OWNER_HELPER, CONSUMER_OWNER_HELPER_SHA))
            or set(d["consumer_input_graphs"]) != set(CONSUMER_PHASES)
            or set(d["consumer_input_source_plans"]) != set(CONSUMER_PHASES)
            or d["explicit_consumer_input_graph_phase_labels"] != list(CONSUMER_PHASES)
            or d["complete_global_input_graph_phase_labels"] != ["prepare", "run_entry", "run_final_immutable_input_closeout", "completed_reference_qualification_handoff"]
            or d["consumer_handoff_returns_only_source_audited_consumed_fields"] is not True
            or d["consumer_handoff_requires_this_actual_parent_complete_global_entry"] is not True
            or str(TERMINAL) not in d["resource_roots"]):
        raise ValueError("frozen complete original-gate reference resource protocol differs")
    if archive_bytes() >= RESERVE:
        raise ValueError("complete SOURCE plus OUT exceeds the unchanged reference archive reserve")
    input_terminal_sha = input_terminal_sha or os.environ.get("AXMAT_INPUT_GRAPH_DECLARE_TERMINAL_SHA256")
    declaration_terminal_admission(d, expected, input_terminal_sha)
    inventory = read(SOURCE / "source_inventory.json")
    actual_namespace = source_namespace()
    if (set(actual_namespace["files"]) != set(inventory["files"]) | {"source_inventory.json"}
            or actual_namespace["directories"] != inventory["directories"]
            or actual_namespace["symlinks"] != inventory["symlinks"]):
        raise ValueError("reference source files/directories/aliases namespace changed")
    verify({str(SOURCE / name): sha for name, sha in inventory["files"].items()})
    if phase in CONSUMER_PHASES:
        if (d["consumer_input_graphs"][phase]["path"] != str(SOURCE / ("input_graph." + phase.replace("/", "-") + ".json"))
                or d["consumer_input_source_plans"][phase]["path"] != str(SOURCE / ("consumer_plan." + phase.replace("/", "-") + ".json"))):
            raise ValueError("consumer handoff must use its exact frozen SOURCE graph and source plan")
        plan = read(require(d["consumer_input_source_plans"][phase]["path"], d["consumer_input_source_plans"][phase]["sha256"]))
        if (plan["schema"] != "AXMAT_REFERENCE_CONSUMER_SOURCE_INPUT_PLAN_V1" or plan["phase"] != phase
                or plan["scope"] != "CONSERVATIVE_SOURCE_DECLARED_CONSUMER_INPUT_SUBSET_ONLY"):
            raise ValueError("consumer source plan is not its immutable explicit input-only declaration")
    actual = verified_input_state(d, expected, phase, allow_already_existing_ABA=allow_already_existing_ABA,
                                  input_terminal_sha=input_terminal_sha, verification_sink=verification_sink)
    if prepared:
        p = read(OUT / "prepared.json")
        if p["declaration"] != pin(SOURCE / "declaration.json"):
            raise ValueError("actual reference preparation differs")
        require(OUT / "declaration.json", expected)
        immutable_names = {"declaration.json", "observation_case_spec.json", "source_equivalence.json", "analysis_environment.json"}
        immutable_names |= {"runtime/" + path.name for path in (SOURCE / "runtime").iterdir() if path.is_file()}
        immutable_files = {name: digest(require(SOURCE / name)) for name in sorted(immutable_names)}
        if p["files"] != immutable_files:
            raise ValueError("prepared copy inventory must be the exact frozen SOURCE counterparts")
        verify({str(OUT / name): sha for name, sha in immutable_files.items()})
        copied_runtime = OUT / "runtime"
        if copied_runtime.is_symlink() or copied_runtime.resolve(strict=True) != copied_runtime:
            raise ValueError("immutable copied analysis runtime must be its canonical directory")
        with os.scandir(copied_runtime) as entries:
            actual_runtime = {}
            for entry in entries:
                mode = entry.stat(follow_symlinks=False).st_mode
                if not stat.S_ISREG(mode):
                    raise ValueError("immutable copied analysis runtime cannot acquire directories/aliases/special endpoints")
                actual_runtime["runtime/" + entry.name] = immutable_files.get("runtime/" + entry.name)
        expected_runtime = {name: sha for name, sha in immutable_files.items() if name.startswith("runtime/")}
        if actual_runtime != expected_runtime:
            raise ValueError("immutable copied analysis runtime namespace differs from its exact frozen SOURCE")
        if p["source_links"] != d["staged_inputs"]:
            raise ValueError("prepared native export input descriptors differ")
        for name, item in p["source_links"].items():
            path = OUT / "fine" / name
            if not path.is_symlink() or path.resolve(strict=True) != Path(item["path"]):
                raise ValueError("actual native export input link does not point to its bound new final state")
            require(item["path"], item["sha256"])
    return d, actual


def prepare(expected, input_terminal_sha):
    d, actual = admission(expected, phase="prepare", input_terminal_sha=input_terminal_sha)
    if OUT.exists():
        raise ValueError("new reference prepared root must be absent; no retry")
    c = actual[0]
    builder = module(require(BUILD_FACTORY, BUILD_SOURCE_SHA), "rank1_factor_cache_reference_build_dependency")
    resources = builder.DynamicHistoryResources(ART, d["resource_roots"], d["min_free_bytes"],
        d["artifact_budget_bytes"], c.ResourceFailure)
    before = resources.check()
    if before["artifact_bytes"] + RESERVE >= d["artifact_budget_bytes"] or before["disk_free_bytes"] - RESERVE < d["min_free_bytes"]:
        raise ValueError("fresh complete-history reference storage reservation no longer fits")
    OUT.mkdir()
    for name in ("runtime", "fine", "AAA"):
        (OUT / name).mkdir()
    for path in (SOURCE / "runtime").iterdir():
        shutil.copy2(path, OUT / "runtime" / path.name)
    for name in ("observation_case_spec.json", "source_equivalence.json", "analysis_environment.json", "declaration.json"):
        shutil.copy2(SOURCE / name, OUT / name)
    for name, item in d["staged_inputs"].items():
        (OUT / "fine" / name).symlink_to(item["path"])
    write_new(OUT / "prepared.json", dict(classification="PREPARED_RANK1_FACTOR_CACHE_REFERENCE_NO_ANALYSIS",
        declaration=pin(SOURCE / "declaration.json"), files={str(path.relative_to(OUT)): digest(path)
            for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()},
        source_links=d["staged_inputs"], transport_launched=False, analysis_started=False,
        AAA_accuracy_qualified=False, ABA_admitted=False, resources_before=before))
    if archive_bytes() >= RESERVE:
        raise ValueError("complete prepared SOURCE plus OUT exceeds the unchanged reference archive reserve")
    resources.check()
    print(json.dumps(dict(classification="PREPARED_RANK1_FACTOR_CACHE_REFERENCE_NO_ANALYSIS", prepared=pin(OUT / "prepared.json"))))


def export_receipt(d):
    log = OUT / "fine/export.log"
    if not any(line.startswith("AXMAT-OBSERVABLES-COMPLETE k64=") for line in log.read_text().splitlines()):
        raise ValueError("actual original native saved-state exporter did not complete")
    verify(d["source_inputs"])
    protocol = dict(schema="AXMAT_SAVED_MET_REAL64_OBSERVABLE_EXPORT_V1", implementation=pin(Path(__file__).resolve()),
        production_prepared=d["production_prepared"], AAA_status=d["AAA_status"], final_stage_seal=d["final_stage_seal"],
        exporter=d["exporter"], exporter_source=d["exporter_source"], source_inputs=d["source_inputs"],
        wall_seconds=60, threads=1, retries=0, native_arithmetic_unchanged=True)
    write_new(OUT / "fine/protocol.json", protocol)
    outputs = {"observables." + suffix: digest(require(OUT / "fine" / ("observables." + suffix)))
               for suffix in ("regions.csv", "faces.csv", "summary.txt")}
    write_new(OUT / "fine/export_receipt.json", dict(classification="SAVED_MET_REAL64_OBSERVABLES_EXPORTED",
        protocol=pin(OUT / "fine/protocol.json"), inputs_unchanged=True, implementation_unchanged=True,
        outputs=outputs, independent_accuracy_qualified=False, ABA_admitted=False))


def project_worker(expected):
    d, actual = admission(expected, prepared=True, phase="AAA/project")
    c, info, status, final, recipe = actual[:5]
    rs = module(OUT / "runtime/reference_statistics.py", "reference_statistics")
    cb = module(OUT / "runtime/compare_balance_symmetry.py", "rank1_factor_cache_current_checker")
    native_spec = Path(info["case_spec"]["path"])
    view_spec = OUT / "observation_case_spec.json"
    stat_rules, view_rules = rs.predeclared_rules(view_spec), cb.predeclared_rules(view_spec)
    fine_rules = cb.predeclared_rules(native_spec)
    for value, prior_path in ((stat_rules, CE / "statistical_rules.json"), (view_rules, CE / "balance_symmetry_rules.json")):
        prior = read(prior_path)
        if {key: val for key, val in value.items() if key != "case_spec_sha256"} != {key: val for key, val in prior.items() if key != "case_spec_sha256"}:
            raise ValueError("original statistical/current scientific thresholds changed")
    if (fine_rules["axial_cells"] != 48 or view_rules["axial_cells"] != 12
            or {key: value for key, value in fine_rules.items() if key not in ("axial_cells", "case_spec_sha256")}
               != {key: value for key, value in view_rules.items() if key not in ("axial_cells", "case_spec_sha256")}):
        raise ValueError("fine numerical rules changed outside the declared cell count")
    for name, rules in (("statistical_rules.json", stat_rules), ("balance_symmetry_rules.json", view_rules),
                        ("fine_balance_symmetry_rules.json", fine_rules)):
        write_new(OUT / name, rules)
    physical = read(OUT / "fine/input_equivalence_AAA.json")
    if (physical["status"] != "PASS" or physical["production_prepared"] != d["production_prepared"]
            or physical["AAA_status"] != d["AAA_status"] or physical["case_spec_sha256"] != info["case_spec"]["sha256"]):
        raise ValueError("actual new saved-state physical identity report required")
    verify(physical["input_identities"])
    projection = module(OUT / "runtime/project_refined_observables.py", "rank1_factor_cache_projection").project(
        OUT / "fine", OUT / "observation", cb, fine_rules)
    checks = projection["original_checks_on_all_fine_entries"]
    fine_paths = [OUT / "fine" / ("observables." + suffix) for suffix in ("regions.csv", "faces.csv", "summary.txt")]
    checks["input_identities"] = {str(path): digest(path) for path in [native_spec, *fine_paths]}
    write_new(OUT / "complete_fine_production_checks.json", checks)
    physical["refined_observation_projection"] = pin(OUT / "observation/projection_receipt.json")
    physical["input_identities"].update({str(path): digest(path) for path in [OUT / "observation/projection_receipt.json",
        OUT / "complete_fine_production_checks.json", view_spec, OUT / "fine/input_equivalence_AAA.json"]})
    write_new(OUT / "input_equivalence_AAA.json", physical)
    files = dict(d["files"])
    files.update({str(path): digest(path) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()
                  and path.name not in ("analysis_claim.json", "stages.json") and not path.name.endswith((".log", ".watchdog.json"))})
    files.update(physical["input_identities"])
    write_new(OUT / "measurement_admission.json", dict(
        classification="FIXED_POINT_INPUTS_AND_COMPLETE_FINE_OBSERVATIONS_ADMITTED_TO_SAVED_REFERENCE", case="AAA",
        production_prepared=d["production_prepared"], AAA_status=d["AAA_status"], case_spec=info["case_spec"],
        final_stage_seal=d["final_stage_seal"], common_basis_sha256=status["common_basis_sha256"], build_admission=d["build_admission"],
        original_reference_execution=recipe["reference_execution"], original_reference_native=recipe["complete_independent_native_sample"],
        complete_fine_checks=pin(OUT / "complete_fine_production_checks.json"),
        observation_projection=pin(OUT / "observation/projection_receipt.json"), physical_input_equivalence=pin(OUT / "input_equivalence_AAA.json"),
        files=files, AAA_accuracy_qualified=False, ABA_admitted=False, transport_launched=False))


def watch(stage):
    path = (OUT / (stage["label"] + ".log")).with_suffix(".watchdog.json")
    w = read(require(path))
    if (w["returncode"] != 0 or w["limit_failure"] is not None or w["command"] != stage["command"]
            or w["rss_cap_mib"] != RSS_CAP or not 0 < w["wall_cap_seconds"] <= stage["wall_cap_seconds"] <= TOTAL_WALL
            or not 0 <= w["sampled_peak_rss_mib"] < RSS_CAP or not 0 <= w["elapsed_seconds"] < w["wall_cap_seconds"]
            or (stage["label"] == LABELS[0] and stage["wall_cap_seconds"] > 60)
            or w["own_child_only"] is not True or w["liveness_group_cleanup"] is not True):
        raise ValueError("actual own-child analysis supervision failed")
    require(OUT / (stage["label"] + ".log"), stage["log_sha256"])
    return dict(path=str(path), sha256=digest(path), peak_rss_mib=w["sampled_peak_rss_mib"])


def reject_publication(result, error):
    target = OUT / "AAA/reference_qualification.json"
    if target.exists():
        failed_path = OUT / "AAA/reference_qualification.publication_failed.json"
        if failed_path.exists():
            raise ValueError("publication failure archive already exists")
        target.rename(failed_path)
        result["unadmitted_publication_artifact"] = pin(failed_path)
    result.pop("reference_qualification", None)
    result.update(classification="RANK1_FACTOR_CACHE_REFERENCE_PUBLICATION_FAILED", error=repr(error),
                  AAA_accuracy_qualified=False, ABA_admitted=False)


def run(expected, input_terminal_sha):
    started = time.monotonic()
    os.environ["AXMAT_INPUT_GRAPH_DECLARE_TERMINAL_SHA256"] = input_terminal_sha
    entry_verification = []
    d, actual = admission(expected, prepared=True, phase="run_entry", input_terminal_sha=input_terminal_sha,
        verification_sink=entry_verification)
    c = actual[0]
    if (OUT / "AAA/analysis_claim.json").exists():
        raise ValueError("one analysis attempt only; no retry")
    builder = module(require(BUILD_FACTORY, BUILD_SOURCE_SHA), "rank1_factor_cache_reference_build_dependency")
    resources = builder.DynamicHistoryResources(ART, d["resource_roots"], d["min_free_bytes"],
        d["artifact_budget_bytes"], c.ResourceFailure)
    before = resources.check()
    if before["artifact_bytes"] + RESERVE >= d["artifact_budget_bytes"] or before["disk_free_bytes"] - RESERVE < d["min_free_bytes"]:
        raise ValueError("actual remaining complete-history reference reservation no longer fits")
    if len(entry_verification) != 1:
        raise ValueError("actual complete global entry verification witness required before any analysis claim")
    entry_path = OUT / "AAA/run_entry_input_verification.json"
    write_new(entry_path, dict(phase="run_entry", actual_run_pid=os.getpid(), actual_run_started_monotonic=started,
        declaration=dict(path=str(SOURCE / "declaration.json"), sha256=expected), input_graph=d["input_graph"],
        verification=entry_verification[0], scientific_predicates_evaluated=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    write_new(OUT / "AAA/analysis_claim.json", dict(declaration_sha256=expected, started_unix=time.time(),
        prepared=d["production_prepared"], AAA_status=d["AAA_status"], own_child_only=True, retries=0,
        actual_run_pid=os.getpid(), actual_parent_pid=os.getppid(),
        actual_run_started_monotonic=started, original_total_wall_seconds=TOTAL_WALL,
        actual_input_declaration_terminal=pin(TERMINAL / "declaration_terminal_return.json"),
        actual_global_run_entry=pin(entry_path),
        actual_run_command=[str(PYTHON), str(Path(__file__).resolve()), "run", "--sha256", expected,
            "--input-terminal-evidence-sha256", input_terminal_sha]))
    full = module(require(FULL_FACTORY, FULL_SOURCE_SHA), "rank1_factor_cache_reference_guard")
    if live_guard_provenance(full, c, actual[1]) != read(d["live_guard_provenance"]["path"]):
        raise ValueError("actual own-child supervisor provenance changed")
    remaining = TOTAL_WALL - (time.monotonic() - started)
    if remaining <= 0:
        raise ValueError("whole reference wall budget exhausted before any numerical child")
    runner = full.OwnRSSSerialExecutor(OUT, remaining, "AAA", resources)
    result = dict(classification="RANK1_FACTOR_CACHE_REFERENCE_FAILED_NO_RETRY", completed_commands=0, error=None,
        transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False, ABA_started=False,
        archive_reserve_bytes=RESERVE, archive_resource_roots=list(ARCHIVE_ROOTS), archive_byte_scope=ARCHIVE_SCOPE,
        elapsed_seconds_scope="Through final immutable-input/resource admission, before formal receipt/result/seal publication. Final tail wall/archive/resource gates are mandatory after all those files are written.",
        mandatory_full_closeout_tail_gate=True)
    failed = None
    try:
        for index, (label, command) in enumerate(zip(LABELS, d["commands"], strict=True)):
            directory, name = label.split("/")
            cmd = [expected if value == "__DECLARATION_SHA256__" else value for value in command]
            runner.execute(OUT / directory, name, cmd, 60 if index == 0 else TOTAL_WALL)
            result["completed_commands"] = index + 1
            if index == 0:
                export_receipt(d)
            if index == 2:
                outputs = [OUT / "measurement_admission.json", OUT / "input_equivalence_AAA.json",
                    OUT / "complete_fine_production_checks.json", OUT / "statistical_rules.json",
                    OUT / "balance_symmetry_rules.json", OUT / "fine_balance_symmetry_rules.json"]
                outputs += [path for path in (OUT / "fine").iterdir() if path.is_file() and not path.is_symlink()
                            and not path.name.endswith((".log", ".watchdog.json"))]
                outputs += [path for path in (OUT / "observation").iterdir() if path.is_file()]
                write_new(OUT / "measurement_binding.json", dict(declaration_sha256=expected,
                    actual_completed_projection_stage=LABELS[index],
                    files={str(path): digest(path) for path in outputs}))
        assessment = read(OUT / "AAA/reference_assessment.json")
        stages = read(OUT / "AAA/stages.json")["stages"]
        if len(stages) != len(LABELS) or [stage["label"] for stage in stages] != list(LABELS) or any(stage["status"] != "PASS" for stage in stages):
            raise ValueError("complete six-stage actual export/physical/projection/reference analysis required")
        monitors = [watch(stage) for stage in stages]
        if (set(assessment["checks"]) != set(GATES) or assessment["prepared_sha256"] != d["production_prepared"]["sha256"]
                or assessment["aaa_run_status_sha256"] != d["AAA_status"]["sha256"]
                or assessment["case_spec_sha256"] != actual[1]["case_spec"]["sha256"]):
            raise ValueError("actual new candidate reference assessment differs")
        qualification = OUT / "AAA/reference_qualification.pending.json"
        if assessment["classification"] == "AAA_REFERENCE_QUALIFIED":
            c.qualify_aba(actual[1], PROD, d["production_prepared"]["sha256"], qualification, digest(require(qualification)))
        elif assessment["classification"] != "AAA_REFERENCE_NOT_QUALIFIED" or qualification.exists():
            raise ValueError("failed/inconclusive comparison cannot produce a qualification receipt")
        result.update(classification="COMPLETE_RANK1_FACTOR_CACHE_ORIGINAL_GATE_REFERENCE_REASSESSMENT",
            AAA_classification=assessment["classification"], original_eight_checks=assessment["checks"],
            AAA_accuracy_qualified=assessment["classification"] == "AAA_REFERENCE_QUALIFIED",
            ABA_admitted=assessment["ABA_admitted"], reference_assessment=pin(OUT / "AAA/reference_assessment.json"),
            watchdogs=monitors, maximum_sampled_rss_mib=max(read(item["path"])["sampled_peak_rss_mib"] for item in monitors))
    except BaseException as error:
        failed = error
        result["error"] = repr(error)
    finally:
        try:
            admission(expected, prepared=True, phase="run_final_immutable_input_closeout")
            resources.check()
            elapsed = time.monotonic() - started
            total_bytes = archive_bytes()
            if elapsed >= TOTAL_WALL or total_bytes >= RESERVE:
                raise ValueError("actual complete analysis exceeds original total wall or declared archive reserve")
            if (PROD / "ABA").exists():
                raise ValueError("reference reassessment must not execute or create ABA")
            result.update(elapsed_seconds=elapsed, actual_archive_bytes_before_closeout=total_bytes)
        except BaseException as error:
            failed = error
            result.update(classification="RANK1_FACTOR_CACHE_REFERENCE_INPUT_OR_RESOURCE_FAILED", error=repr(error),
                          AAA_accuracy_qualified=False, ABA_admitted=False)
        # The unchanged scientific collector/qualify_aba guard has already
        # checked these exact receipt bytes. Publish the formal path only after
        # complete supervision and final immutable-input/resource admission.
        if failed is None and result["AAA_accuracy_qualified"]:
            try:
                pending = require(OUT / "AAA/reference_qualification.pending.json")
                target = OUT / "AAA/reference_qualification.json"
                if target.exists():
                    raise ValueError("formal reference qualification already exists")
                with target.open("xb") as stream:
                    stream.write(pending.read_bytes())
                require(target, digest(pending))
                result["reference_qualification"] = pin(target)
            except BaseException as error:
                failed = error
                reject_publication(result, error)
        try:
            result["outputs"] = {str(path.relative_to(OUT)): digest(path) for path in OUT.rglob("*")
                if path.is_file() and not path.is_symlink() and path.name not in ("analysis_result.json", "seal.json")}
            write_new(OUT / "AAA/analysis_result.json", result)
            write_new(OUT / "seal.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_REFERENCE_SEAL_V1",
                files={str(path.relative_to(OUT)): digest(path) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()}))
            # These last checks include formal publication, output hashing,
            # analysis_result and seal writing. Keep the already sealed files
            # immutable; successful terminal measurements go to the return/
            # stdout record. A failure appends a new artifact and withdraws
            # the formal receipt, invalidating the prior success namespace.
            terminal_resources = resources.check()
            terminal_bytes = archive_bytes()
            terminal_elapsed = time.monotonic() - started
            if terminal_elapsed >= TOTAL_WALL or terminal_bytes >= RESERVE:
                raise ValueError("actual full closeout tail exceeds original total wall or complete archive reserve")
            result.update(full_closeout_tail_gate="PASS", actual_elapsed_through_full_closeout_seconds=terminal_elapsed,
                actual_complete_archive_bytes=terminal_bytes, resources_after_full_closeout=terminal_resources)
        except BaseException as error:
            failed = error
            reject_publication(result, error)
            # Retain the failed closeout without overwriting an earlier output.
            # Any incomplete/changed seal also fails qualification_admission.
            write_new(OUT / "AAA/publication_failure.json", result)
    print(json.dumps(result))
    if failed is not None:
        raise failed


def strict_terminal_json(path):
    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate key in actual terminal evidence JSON")
            value[key] = item
        return value

    def reject_constant(value):
        raise ValueError("nonfinite JSON constant in actual terminal evidence: " + value)

    value = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                       parse_constant=reject_constant)
    if type(value) is not dict:
        raise ValueError("the full retained terminal output must be one JSON object")
    return value


def terminal_file(value, expected_parent, wanted=None):
    """Reject evidence aliases, including symlinks in any ancestor."""
    if not isinstance(value, (str, Path)):
        raise ValueError("actual terminal evidence needs an absolute regular file path")
    path = Path(value)
    if (not path.is_absolute() or ".." in path.parts or str(value) != str(path)
            or path.parent != expected_parent or path.resolve(strict=True) != path):
        raise ValueError("actual terminal evidence path differs from the independent canonical root")
    cursor = path
    while True:
        if cursor.is_symlink():
            raise ValueError("terminal evidence or its ancestor is a symlink")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    return require(path, wanted)


def external_terminal_admission(d, declared_sha, expected_seal, sealed_result,
                                terminal_evidence, terminal_evidence_sha256):
    """Consume Root's actual exit-zero witness without producing one here.

    The reference success seal precedes the mandatory final tail checks. It is
    insufficient after an interruption; Root must retain the complete stdout
    and write this independent receipt only after the actual tool returns zero.
    """
    if (not isinstance(terminal_evidence_sha256, str) or len(terminal_evidence_sha256) != 64
            or any(char not in "0123456789abcdef" for char in terminal_evidence_sha256)):
        raise ValueError("the actual independent terminal-return receipt SHA256 is required")
    if (TERMINAL.parent != ART or TERMINAL in (SOURCE, OUT)
            or any(TERMINAL.is_relative_to(root) or root.is_relative_to(TERMINAL) for root in (SOURCE, OUT))
            or str(TERMINAL) not in d["resource_roots"]):
        raise ValueError("external actual terminal root must be independent and within the declared history scope")
    receipt = terminal_file(terminal_evidence, TERMINAL, terminal_evidence_sha256)
    if receipt != TERMINAL / "terminal_return.json":
        raise ValueError("only the independent actual terminal-return receipt is eligible")
    e = strict_terminal_json(receipt)
    factory = Path(__file__).resolve()
    input_terminal = e["input_declaration_terminal_evidence"]
    declaration_terminal_admission(d, declared_sha, input_terminal["sha256"])
    if input_terminal != pin(TERMINAL / "declaration_terminal_return.json"):
        raise ValueError("actual run witness does not bind its external input-declaration terminal")
    command = [str(PYTHON), str(factory), "run", "--sha256", declared_sha,
               "--input-terminal-evidence-sha256", input_terminal["sha256"]]
    if (e["schema"] != TERMINAL_SCHEMA or e["record_producer"] != "root"
            or e["actual_tool_terminal_return_observed"] is not True
            or e["record_written_after_actual_terminal_return"] is not True
            or type(e["returncode"]) is not int or e["returncode"] != 0
            or e["command"] != command or e["source"] != pin(factory)
            or d["files"].get(str(factory)) != e["source"]["sha256"]
            or e["declaration"] != dict(path=str(SOURCE / "declaration.json"), sha256=declared_sha)
            or e["reference_seal"] != dict(path=str(OUT / "seal.json"), sha256=expected_seal)):
        raise ValueError("actual Root exit-zero record does not bind this frozen source/declaration/reference seal")
    stdout = terminal_file(e["full_stdout"]["path"], TERMINAL, e["full_stdout"]["sha256"])
    if stdout == receipt or e["full_stdout"] != pin(stdout):
        raise ValueError("actual full stdout must be an independently retained file")
    returned = strict_terminal_json(stdout)
    tail = {key: returned[key] for key in TAIL_FIELDS}
    if any(e[key] != tail[key] for key in TAIL_FIELDS) or returned != dict(sealed_result, **tail):
        raise ValueError("the complete actual stdout and Root terminal record differ from the sealed scientific result")
    elapsed = tail["actual_elapsed_through_full_closeout_seconds"]
    reported_archive_bytes = tail["actual_complete_archive_bytes"]
    snapshot = tail["resources_after_full_closeout"]
    actual_bytes = archive_bytes()
    if (tail["full_closeout_tail_gate"] != "PASS" or type(elapsed) not in (int, float)
            or not math.isfinite(elapsed) or not sealed_result["elapsed_seconds"] <= elapsed < TOTAL_WALL
            or d["archive_reserve_bytes"] != RESERVE or d["archive_resource_roots"] != list(ARCHIVE_ROOTS)
            or d["archive_byte_scope"] != ARCHIVE_SCOPE
            or sealed_result["archive_reserve_bytes"] != RESERVE
            or sealed_result["archive_resource_roots"] != list(ARCHIVE_ROOTS) or sealed_result["archive_byte_scope"] != ARCHIVE_SCOPE
            or type(reported_archive_bytes) is not int or not 0 <= reported_archive_bytes < RESERVE
            or reported_archive_bytes != actual_bytes
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["artifact_budget_bytes"] != 96 * 2**30 or d["artifact_budget_bytes"] != 96 * 2**30
            or snapshot["min_free_bytes"] != 8 * 2**30 or d["min_free_bytes"] != 8 * 2**30
            or snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != d["resource_scope_contract"]
            or snapshot["declared_resource_roots"] != d["resource_roots"]
            or type(snapshot["resource_roots"]) is not list
            or not set(d["resource_roots"]).issubset(snapshot["resource_roots"])
            or type(snapshot["artifact_bytes"]) is not int
            or not reported_archive_bytes <= snapshot["artifact_bytes"] <= d["artifact_budget_bytes"]
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < d["min_free_bytes"]
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float)
            or not math.isfinite(snapshot["checked_unix"]) or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete closeout tail wall/archive/resource evidence failed")
    builder = module(require(BUILD_FACTORY, BUILD_SOURCE_SHA), "rank1_factor_cache_reference_build_dependency")
    builder.validate_history_roots(snapshot["resource_roots"], ART)
    return dict(receipt=pin(receipt), full_stdout=pin(stdout), command=command,
                schema=TERMINAL_SCHEMA, input_declaration_terminal_evidence=input_terminal, **tail)


def qualification_admission(expected_seal, expected_qualification, terminal_evidence, terminal_evidence_sha256):
    """Only complete seal, formal receipt and actual terminal return admit ABA."""
    seal = read(require(OUT / "seal.json", expected_seal))
    if seal["schema"] != "AXMAT_RANK1_FACTOR_CACHE_REFERENCE_SEAL_V1":
        raise ValueError("actual completed new reference seal required")
    actual = {str(path.relative_to(OUT)) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()}
    if actual != set(seal["files"]) | {"seal.json"}:
        raise ValueError("complete reference terminal seal namespace changed")
    verify({str(OUT / name): sha for name, sha in seal["files"].items()})
    result = read(OUT / "AAA/analysis_result.json")
    if (result["classification"] != "COMPLETE_RANK1_FACTOR_CACHE_ORIGINAL_GATE_REFERENCE_REASSESSMENT"
            or result["completed_commands"] != len(LABELS) or result["error"] is not None
            or result["AAA_accuracy_qualified"] is not True or result["ABA_admitted"] is not True
            or result["ABA_started"] is not False or result["transport_launched"] is not False
            or result["mandatory_full_closeout_tail_gate"] is not True
            or not 0 <= result["elapsed_seconds"] < TOTAL_WALL
            or result["actual_archive_bytes_before_closeout"] >= RESERVE
            or set(result["original_eight_checks"]) != set(GATES)
            or any(value != "PASS" for value in result["original_eight_checks"].values())):
        raise ValueError("actual complete bounded eight-gate qualification is not present")
    formal = require(OUT / "AAA/reference_qualification.json", expected_qualification)
    if result["reference_qualification"] != pin(formal):
        raise ValueError("only the successful formally published qualification is eligible")
    stages = read(OUT / "AAA/stages.json")["stages"]
    if len(stages) != len(LABELS) or [stage["label"] for stage in stages] != list(LABELS) or any(stage["status"] != "PASS" for stage in stages):
        raise ValueError("all actual reassessment stages must pass")
    declared = read(OUT / "prepared.json")["declaration"]
    if declared["path"] != str(SOURCE / "declaration.json"):
        raise ValueError("actual completed reference must bind its own immutable declaration")
    declared_sha = declared["sha256"]
    d = read(require(declared["path"], declared_sha))
    require(OUT / "declaration.json", declared_sha)
    commands = [[declared_sha if value == "__DECLARATION_SHA256__" else value for value in command]
                for command in d["commands"]]
    for stage, command in zip(stages, commands, strict=True):
        if stage["command"] != command:
            raise ValueError("actual completed reference command differs from its declaration")
        watch(stage)
    terminal = external_terminal_admission(d, declared_sha, expected_seal, result,
                                          terminal_evidence, terminal_evidence_sha256)
    require(PROD / "runtime/production_runner.py", d["files"][str(PROD / "runtime/production_runner.py")])
    qualified_controller = controller()
    qualified_info = qualified_controller.verify_prepared(PROD / "prepared.json", d["production_prepared"]["sha256"])
    qualified_controller.qualify_aba(qualified_info, PROD, d["production_prepared"]["sha256"], formal, expected_qualification)
    # Only this read-only API admits an already existing ABA directory. Its
    # complete formal scientific receipt and actual Root exit-zero/full-tail
    # witness have been checked above; every AAA/build/input pin is still
    # revalidated below. First-stage declare/prepare/run use the default False.
    d, ready_state = admission(declared_sha, prepared=True, allow_already_existing_ABA=True,
        phase="completed_reference_qualification_handoff",
        input_terminal_sha=terminal["input_declaration_terminal_evidence"]["sha256"])
    builder = module(require(BUILD_FACTORY, BUILD_SOURCE_SHA), "rank1_factor_cache_reference_build_dependency")
    builder.DynamicHistoryResources(ART, d["resource_roots"], d["min_free_bytes"], d["artifact_budget_bytes"],
        ready_state[0].ResourceFailure).check()
    if ready_state[0] is not qualified_controller or ready_state[1] != qualified_info:
        raise ValueError("complete candidate admission differs from the actual original qualification guard inputs")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_SEALED_REFERENCE_QUALIFICATION_ADMISSION_V1",
        reference_root=str(OUT), reference_seal_sha256=expected_seal, qualification=pin(formal),
        production_prepared=d["production_prepared"], AAA_status=d["AAA_status"],
        actual_external_terminal_evidence=terminal["receipt"], actual_external_terminal_validation=terminal,
        actual_build_terminal_evidence=d["actual_build_terminal_evidence"],
        actual_build_terminal_validation=d["actual_build_terminal_validation"],
        build_terminal_chain=d["build_terminal_chain"], coupling_completion=d["coupling_completion"],
        resource_scope_policy=HISTORY_SCOPE_POLICY, current_complete_history_admission_required=True,
        resource_scope_contract=d["resource_scope_contract"],
        archive_reserve_bytes=RESERVE, archive_resource_roots=list(ARCHIVE_ROOTS), archive_byte_scope=ARCHIVE_SCOPE,
        all_original_eight_checks=result["original_eight_checks"], original_qualify_aba_guard_passed=True,
        pending_receipt_eligible=False, this_API_launched_ABA=False,
        AAA_reference_run_started_ABA=False,
        ABA_directory_exists_at_admission=(PROD / "ABA").exists(),
        existing_ABA_allowed_only_after_completed_reference_terminal_admission=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("declare", "prepare", "run", "project-worker", "admit-qualification"))
    parser.add_argument("--sha256")
    parser.add_argument("--prepared-sha256")
    parser.add_argument("--status-sha256")
    parser.add_argument("--build-seal-sha256")
    parser.add_argument("--build-terminal-evidence", type=Path)
    parser.add_argument("--build-terminal-evidence-sha256")
    parser.add_argument("--qualification-sha256")
    parser.add_argument("--terminal-evidence", type=Path)
    parser.add_argument("--terminal-evidence-sha256")
    parser.add_argument("--input-terminal-evidence-sha256")
    args = parser.parse_args()
    if args.action == "declare":
        if not all((args.prepared_sha256, args.status_sha256, args.build_seal_sha256,
                args.build_terminal_evidence, args.build_terminal_evidence_sha256)):
            parser.error("declare requires actual prepared/status/build-seal SHA256 and both actual build-terminal inputs")
        declare(args.prepared_sha256, args.status_sha256, args.build_seal_sha256,
                args.build_terminal_evidence, args.build_terminal_evidence_sha256)
    elif not args.sha256:
        parser.error("the frozen declaration --sha256 is required")
    elif args.action == "admit-qualification":
        if not all((args.qualification_sha256, args.terminal_evidence, args.terminal_evidence_sha256)):
            parser.error("actual formal --qualification-sha256, reference seal --sha256 and both terminal-evidence inputs required")
        print(json.dumps(qualification_admission(args.sha256, args.qualification_sha256,
                                                args.terminal_evidence, args.terminal_evidence_sha256)))
    elif args.action in ("prepare", "run"):
        if not args.input_terminal_evidence_sha256:
            parser.error("prepare/run require the actual external --input-terminal-evidence-sha256")
        {"prepare": prepare, "run": run}[args.action](args.sha256, args.input_terminal_evidence_sha256)
    else:
        project_worker(args.sha256)
