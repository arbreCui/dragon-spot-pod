"""Declare and launch one qualified rank1-factor-cache ABA attempt.

Only a real bounded read-only call to the frozen rank1-factor-cache AAA reference
API can provide qualification. The exact producer environment then repeats
the original qualify_aba guard and directly calls the current frozen run body.
Its already-admitted axial selector/cache observers and dynamic family resource
monitor remain in place: no callable, prepared file or module identity is
reassigned. The entrance never creates PROD/ABA; only c.run may claim it.

Build, AAA, collector and external Root terminal evidence are revalidated.
A later completed-ABA reader may exclude only the explicit directory-existence
lifecycle field when comparing two whole actual API returns; launch itself
requires that field False and exact full-return equality. No anticipated
prepared, status, formal qualification or terminal hashes are supplied here.
"""

import argparse
import hashlib
import importlib.util
import inspect
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
PROD = ART / "axial-material-production-qualified-AB-rank1-factor-cache-20261007"
REFERENCE = ART / "axial-material-qualified-AAA-rank1-factor-cache-reference-20261007"
REFERENCE_SOURCE = ART / "axial-material-qualified-AAA-rank1-factor-cache-reference-admission-20261007"
TERMINAL_ROOT = ART / "axial-material-qualified-AAA-rank1-factor-cache-reference-terminal-20261007"
SOURCE = ART / "axial-material-qualified-ABA-rank1-factor-cache-execution-admission-20261007"
BUILD = ART / "axial-material-rank1-factor-cache-build-20261007"
BUILD_TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
CE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AAA_rank1_cache_reference_analysis.py"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_production.py"
FULL_FACTORY = ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py"
COUPLING_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_coupling.py"
TEMPLATE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_ABA_source_factor_execution.py"
FORMAL = REFERENCE / "AAA/reference_qualification.json"
BUILD_SEAL = "e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f"
BUILD_FACTORY_SHA = "92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a"
CE_FACTORY_SHA = "a937a7d246abf43709f135ba36cdda0e7c81cf5340847160b8e433bb72e65b7c"
COUPLING_FACTORY_SHA = "96e54f36e1939a7edc7d112661c1e44066d7a3e869354a932ad9b967ec0d666d"
TEMPLATE_FACTORY_SHA = "1dc0e3a1353e052a7f90144a21c357023bda753f203245920d74cbfa33e17641"
FULL_FACTORY_SHA = "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6"
CONTROLLER_SHA = "844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d"
# These bind the actual completed build and actual prepared controller.
# The real complete AAA scientific qualification remains mandatory.
EXPERIMENT = "axial-material-qualified-AB-rank1-factor-cache-20261007"
GATES = ("input_equivalence", "source_convergence", "block_stability", "statistical_resolution",
         "keff", "scalar_flux", "nu_fission", "currents_balance_symmetry")
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
BUDGET = dict(axial_seconds=4200, bootstrap_axial_seconds=4200, bootstrap_radial_seconds=600,
              host_seconds=120, max_maps=100, radial_seconds=300, setup_seconds=120, total_seconds=43200)
HISTORY_CAP, FREE_FLOOR = 96 * 2**30, 8 * 2**30
ADMISSION_RESERVE = 64 * 2**20
READ_ONLY_CAP, READ_ONLY_RSS = 120, 512
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
LIFECYCLE_FIELD = "ABA_directory_exists_at_admission"
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
CACHE_OBSERVER_CONTRACT = dict(prefix="AXMAT-RANK1-CACHE TERMINAL ",
    columns=["builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes", "cap_bytes"],
    cap_bytes=536870912, exact_operator_identity_required=True,
    positive_build_reuse_and_validation_required=True, all_actual_full_logs_required=True)


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, wanted=None):
    path = Path(path)
    if (not path.is_absolute() or path.is_symlink() or not path.is_file()
            or (wanted is not None and digest(path) != wanted)):
        raise ValueError("missing or changed actual ABA admission dependency: " + str(path))
    return path


def pin(path):
    path = require(path)
    return dict(path=str(path), sha256=digest(path))


def read(path):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError("duplicate actual admission JSON key")
            value[key] = item
        return value
    def nonfinite(value):
        raise ValueError("nonfinite actual admission JSON: " + value)
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=nonfinite)


def write_new(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def absent(path):
    if Path(path).exists() or Path(path).is_symlink():
        raise ValueError("exclusive future attempt path must be absent: " + str(path))


def load(path, name):
    path = require(path)
    if name in sys.modules:
        obj = sys.modules[name]
        if Path(obj.__file__).resolve() != path.resolve():
            raise ValueError("actual imported admission module has another source path")
        return obj
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    if Path(obj.__file__).resolve() != path.resolve():
        raise ValueError("actual module source path differs")
    return obj


def controller():
    if CONTROLLER_SHA == "0" * 64:
        raise ValueError("future source only: actual prepared rank-one-cache controller is not bound")
    path = require(PROD / "runtime/production_runner.py", CONTROLLER_SHA)
    sys.path.insert(0, str(path.parent))
    return load(path, "production_runner")


def bind_runtime_dependencies(raw_info):
    """Establish true canonical source paths before the older guard helper imports."""
    names = ("production_inputs", "snapshot_control_preflight", "analyze_r64_snapshot",
        "analyze_r64_tracking_moments", "check_r64_audit_rejections", "check_r64_normalization_rejections",
        "qualified_snapshot_ingestion", "numerical_layout_admission", "rank1_factor_cache_admission")
    result = {}
    for name in names:
        path = require(PROD / "runtime" / (name + ".py"), raw_info["local_files"]["runtime/" + name + ".py"])
        obj = load(path, name)
        result[name] = pin(Path(obj.__file__).resolve())
    return result


def producer_environment(info, expected=None):
    """Admit the actual original producer before any possible ABA creation."""
    import numpy as np
    declaration = read(require(info["declaration"]["path"], info["declaration"]["sha256"]))
    item = declaration["rank1_factor_cache_revision"]
    revision = read(require(item["path"], item["sha256"]))
    env_item = revision["producer_environment"]
    env = read(require(env_item["path"], env_item["sha256"]))
    if (env["schema"] != "AXMAT_EXACT_OFFLINE_REPLAY_ENVIRONMENT_V1"
            or env["python_version"] != "3.14.4" or env["numpy_version"] != "2.4.4"
            or str(Path(sys.executable).resolve()) != env["executable"]
            or platform.python_version() != env["python_version"] or np.__version__ != env["numpy_version"]
            or str(Path(np.__file__).parent.resolve()) != env["numpy_root"]
            or any(os.environ.get(key) != "1" for key in THREADS)):
        raise ValueError("the original exact producer Python3.14.4/NumPy2.4.4/single threads are required")
    verify(env["files"])
    result = dict(environment=env_item, executable=pin(Path(env["executable"])),
        python_version=platform.python_version(), numpy_version=np.__version__, numpy_root=env["numpy_root"],
        thread_environment={key: os.environ.get(key) for key in THREADS},
        loader_environment={key: value for key, value in os.environ.items()
            if key.startswith("DYLD_") or key.startswith("LD_") or key in ("PYTHONPATH", "OPENBLAS_CORETYPE")})
    if expected is not None and result != expected:
        raise ValueError("declared producer interpreter/package/loader environment changed")
    return result


def reference_environment():
    d = read(require(REFERENCE / "declaration.json"))
    item = d["analysis_environment"]
    env = read(require(item["path"], item["sha256"]))
    if (env["schema"] != "AXMAT_RANK1_FACTOR_CACHE_SEPARATE_CE_ENVIRONMENT_V1"
            or not env["python_version"].startswith("3.12.") or env["numpy_version"] != "2.4.3"
            or env["producer_environment_is_separate"] is not True
            or env["thread_environment"] != {key: "1" for key in THREADS}):
        raise ValueError("actual separately frozen CE analysis environment required")
    verify(env["files"])
    require(Path(env["executable"]), env["files"][env["executable"]])
    return item, env


def build_factory():
    return load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "rank1_factor_cache_ABA_build_dependency")


def stable_qualification_identity(api):
    """Retain every returned value except the sole documented lifecycle fact.

    A completed-case consumer must require launch False and current True before
    comparing these identities. This helper does not prove completion, create
    a qualification or excuse any other returned key/value difference.
    """
    if (type(api) is not dict or api.get("schema") != "AXMAT_RANK1_FACTOR_CACHE_SEALED_REFERENCE_QUALIFICATION_ADMISSION_V1"
            or type(api.get(LIFECYCLE_FIELD)) is not bool
            or api.get("existing_ABA_allowed_only_after_completed_reference_terminal_admission") is not True
            or api.get("this_API_launched_ABA") is not False or api.get("AAA_reference_run_started_ABA") is not False):
        raise ValueError("actual complete rank1-factor-cache qualification lifecycle contract required")
    identity = dict(api)
    del identity[LIFECYCLE_FIELD]
    return identity


def lifecycle_contract():
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_QUALIFICATION_LIFECYCLE_IDENTITY_V1",
        only_mutable_field=LIFECYCLE_FIELD, launch_required_value=False,
        completed_case_reader_required_value=True,
        stable_identity_function=callable_pin(stable_qualification_identity),
        all_other_actual_API_fields_compared_exactly=True, launch_full_API_returns_compared_exactly=True,
        existing_ABA_allowed_only_by_the_completed_read_only_reference_API=True,
        helper_does_not_admit_completed_ABA=True)


def roots_for(info, terminal_path):
    values = set(info["resource_roots"])
    for root in (BUILD, FULL, CAUSAL, REFERENCE):
        values.update(read(require(root / "declaration.json"))["resource_roots"])
    values.update(str(path) for path in ART.glob("axial-material-*") if path.is_dir())
    values.update((str(SOURCE), str(PROD), str(REFERENCE), str(REFERENCE_SOURCE), str(BUILD_TERMINAL)))
    terminal = Path(terminal_path)
    if terminal != TERMINAL_ROOT / "terminal_return.json":
        raise ValueError("actual reference terminal evidence must use its fixed independent artifact root")
    values.add(str(TERMINAL_ROOT))
    roots = sorted(values)
    build_factory().validate_history_roots(roots, ART)
    return roots


def current_resources(c, roots, reserve):
    if type(reserve) is not int or reserve < 0:
        raise ValueError("actual nonnegative integer archive reservation required")
    builder = build_factory()
    contract = builder.resource_scope_contract()
    resources = builder.DynamicHistoryResources(ART, list(roots), FREE_FLOOR, HISTORY_CAP, c.ResourceFailure)
    snapshot = resources.check()
    if (snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != contract
            or snapshot["artifact_bytes"] + reserve >= HISTORY_CAP
            or snapshot["disk_free_bytes"] - reserve < FREE_FLOOR):
        raise ValueError("complete current axial-family history plus fresh ABA reservation does not fit unchanged 96GiB/global-free8GiB caps")
    return resources, snapshot


def admission_archive_gate():
    size = regular_bytes(SOURCE)
    if size >= ADMISSION_RESERVE:
        raise ValueError("actual read-only ABA admission archive exceeds its separate 64MiB reservation")
    return size


def regular_bytes(folder):
    if Path(folder).is_symlink() or not Path(folder).is_dir():
        raise ValueError("sealed case output directory is absent or aliased")
    return sum(path.stat().st_size for path in Path(folder).rglob("*") if path.is_file() and not path.is_symlink())


def reservation(c, info, status):
    """Predict from qualified AAA; every later stage still enforces the fixed total cap."""
    case = status["cases"]["AAA"]
    count = case["completed_maps"]
    if (isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= BUDGET["max_maps"]
            or len(case["maps"]) != count or [row["epoch"] for row in case["maps"]] != list(range(1, count + 1))):
        raise ValueError("complete consecutive actual AAA map provenance required for reservation")
    bootstrap = PROD / "AAA/bootstrap"
    c.verify_sealed_directory(bootstrap)
    maps = []
    for epoch in range(1, count + 1):
        folder = PROD / "AAA" / f"map{epoch:03d}"
        c.verify_sealed_directory(folder)
        maps.append(dict(epoch=epoch, root=str(folder), seal=pin(folder / "result.json"), regular_bytes=regular_bytes(folder)))
    if Path(case["final_directory"]) != PROD / "AAA" / f"map{count:03d}":
        raise ValueError("actual qualified final state differs from full map sequence")
    base = regular_bytes(bootstrap)
    largest = max(row["regular_bytes"] for row in maps)
    if base <= 0 or largest <= 0:
        raise ValueError("actual sealed bootstrap/map storage witnesses must be nonempty")
    case_bytes = regular_bytes(PROD / "AAA")
    amount = math.ceil(1.5 * case_bytes) + 2**30 + ADMISSION_RESERVE
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_FRESH_ABA_RESERVATION_V1", method="1.5*actual_qualified_AAA_case_regular_bytes+1GiB+64MiB",
        actual_bootstrap=pin(bootstrap / "result.json"), actual_bootstrap_regular_bytes=base,
        actual_map_witnesses=maps, actual_largest_map_regular_bytes=largest, actual_completed_maps=count,
        actual_qualified_AAA_case_regular_bytes=case_bytes, original_iteration_cap=100,
        growth_factor=1.5, ABA_log_and_host_reserve_bytes=2**30, admission_reserve_bytes=ADMISSION_RESERVE,
        fresh_ABA_reserve_bytes=amount, forecast_only=True, production_dimensions_and_map_cap_unchanged=True,
        all_100_maps_storage_not_guaranteed=True, unchanged_every_stage_history_gate_may_fail_if_exhausted=True)


def callable_pin(function):
    source = inspect.getsource(function)
    path = Path(inspect.getsourcefile(function)).resolve()
    return dict(module=function.__module__, name=function.__qualname__, source_file=pin(path),
        function_source_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest())





def monitor_contract(c, info):
    """Pin the actual admitted monitor and current scientific entry callables.

    The current run has the previously frozen selector/cache observers; its monitor
    has the previously frozen dynamic history guard. Neither is overridden.
    """
    builder = build_factory()
    parent = builder.parent_factory()
    actual_class = parent.DynamicHistoryResources
    parent_source = require(builder.PARENT_FACTORY, builder.PARENT_FACTORY_SHA)
    monitor = c.resource_monitor(info)
    if (type(monitor).__name__ != "DynamicHistoryResources"
            or type(monitor) is not actual_class
            or Path(inspect.getsourcefile(type(monitor))).resolve() != parent_source
            or monitor.artifacts_root.resolve() != ART.resolve()
            or monitor.declared_roots != info["resource_roots"]
            or monitor.min_free_bytes != FREE_FLOOR or monitor.max_bytes != HISTORY_CAP):
        raise ValueError("actual frozen controller resource binding is not the admitted dynamic family monitor")
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_UNCHANGED_ACTUAL_RESOURCE_MONITOR_V1",
        actual_binding="production_runner.resource_monitor", original=callable_pin(c.resource_monitor),
        actual_resource_class=callable_pin(type(monitor)), actual_build_factory=pin(BUILD_FACTORY),
        actual_resource_class_factory=pin(parent_source), new_build_factory_is_lazy_class_constructor=True,
        frozen_scientific_callables={name: callable_pin(getattr(c, name)) for name in ("run", "qualify_aba", "SerialExecutor")},
        prepared_monitor_roots=info["resource_roots"], artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR,
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=builder.resource_scope_contract(),
        binding_method="direct use of the frozen current resource_monitor; no overlay or reassignment",
        actual_controller_run_has_only_the_previously_admitted_axial_selector_and_factor_cache_log_guards=True,
        actual_controller_resource_monitor_has_the_previously_admitted_dynamic_history_guard=True,
        whole_run_AST_exact_to_older_controller_claimed=False, scientific_arithmetic_or_budgets_changed_by_this_entry=False,
        prepared_or_runtime_files_changed=False, module_identity_reassigned=False)


def supervision(c, raw_info, ce_factory_sha):
    require(FULL_FACTORY, FULL_FACTORY_SHA)
    require(BUILD_FACTORY, BUILD_FACTORY_SHA)
    require(CE_FACTORY, CE_FACTORY_SHA)
    if ce_factory_sha != CE_FACTORY_SHA:
        raise ValueError("the actual frozen rank1-factor-cache AAA reference source is required")
    bind_runtime_dependencies(raw_info)
    ce = load(CE_FACTORY, "rank1_factor_cache_ABA_reference_dependency")
    full = load(FULL_FACTORY, "rank1_factor_cache_ABA_own_RSS_guard")
    builder = build_factory()
    proof = ce.live_guard_provenance(full, c, raw_info)
    files = builder.helper().guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,):
        raise ValueError("bounded read-only admission child has another actual production supervisor")
    return full, proof, {str(path): digest(path) for path in files}


def ce_command(env, ce_factory_sha, reference_seal_sha, qualification_sha, terminal_path, terminal_sha):
    # Argument names follow the current reference API; no pending path is accepted.
    require(CE_FACTORY, ce_factory_sha)
    return [env["executable"], str(CE_FACTORY), "admit-qualification",
        "--sha256", reference_seal_sha, "--qualification-sha256", qualification_sha,
        "--terminal-evidence", str(terminal_path), "--terminal-evidence-sha256", terminal_sha]


def bounded_reference_call(phase, c, raw_info, ce_factory_sha, reference_seal_sha,
                           qualification_sha, terminal_path, terminal_sha, resources):
    absent(PROD / "ABA")
    folder = SOURCE / phase
    absent(folder)
    full, guard, guard_files = supervision(c, raw_info, ce_factory_sha)
    env_item, env = reference_environment()
    command = ce_command(env, ce_factory_sha, reference_seal_sha, qualification_sha, terminal_path, terminal_sha)
    child_env = dict(os.environ)
    for key, value in env["loader_environment"].items():
        if value is None:
            child_env.pop(key, None)
        else:
            child_env[key] = value
    child_env.update({key: "1" for key in THREADS})
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    folder.mkdir()
    write_new(folder / "run_claim.json", dict(parent_pid=os.getpid(), phase=phase,
        read_only_API_only=True, extra_transport_calls=0, extra_linear_solves=0, retries=0))
    runner = full.OwnRSSSerialExecutor(SOURCE, READ_ONLY_CAP, phase, resources)
    runner.env = child_env
    try:
        runner.execute(folder, "sealed_reference_guard", command, READ_ONLY_CAP)
        records = read(folder / "stages.json")["stages"]
        if (len(records) != 1 or records[0]["label"] != phase + "/sealed_reference_guard"
                or records[0]["status"] != "PASS" or records[0]["command"] != command):
            raise ValueError("the single actual bounded CE API call did not pass")
        record = records[0]
        log = require(folder / "sealed_reference_guard.log", record["log_sha256"])
        watchdog = require(folder / "sealed_reference_guard.watchdog.json")
        w = read(watchdog)
        if (w["returncode"] != 0 or w["limit_failure"] is not None or w["command"] != command
                or w["rss_cap_mib"] != READ_ONLY_RSS or not 0 < w["wall_cap_seconds"] <= record["wall_cap_seconds"] <= READ_ONLY_CAP
                or not 0 <= w["elapsed_seconds"] < w["wall_cap_seconds"]
                or not 0 <= w["sampled_peak_rss_mib"] < READ_ONLY_RSS
                or w["own_child_only"] is not True or w["liveness_group_cleanup"] is not True):
            raise ValueError("actual read-only CE API watchdog failed")
        returned = read(log)
        write_new(folder / "ce_api_return.json", returned)
        stable_qualification_identity(returned)
        if returned[LIFECYCLE_FIELD] is not False or (PROD / "ABA").exists():
            raise ValueError("both actual launch qualification calls require ABA absent")
        receipt = dict(schema="AXMAT_RANK1_FACTOR_CACHE_BOUNDED_REFERENCE_API_RECEIPT_V1",
            classification="COMPLETE_READ_ONLY_REFERENCE_QUALIFICATION_API_CALL", phase=phase,
            command=command, returncode=0, stdout=pin(log), actual_API_return=pin(folder / "ce_api_return.json"),
            watchdog=pin(watchdog), stages=pin(folder / "stages.json"), guard=guard, guard_files=guard_files,
            analysis_environment=env_item, exact_child_loader_environment=env["loader_environment"],
            thread_environment={key: child_env[key] for key in THREADS}, wall_cap_seconds=READ_ONLY_CAP,
            rss_cap_mib=READ_ONLY_RSS, numeric_children_at_once=1, retries=0,
            extra_transport_calls=0, extra_linear_solves=0, AAA_scientific_stages_added=0, ABA_created=False,
            actual_qualification_lifecycle=lifecycle_contract(),
            actual_API_ABA_directory_exists_at_admission=False,
            resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=build_factory().resource_scope_contract())
        write_new(folder / "receipt.json", receipt)
        admission_archive_gate()
        resources.check()
        return returned, pin(folder / "receipt.json")
    except BaseException as error:
        write_new(folder / "failure.json", dict(classification="FAILED_READ_ONLY_REFERENCE_API_NO_RETRY", error=repr(error),
            production_ABA_created=(PROD / "ABA").exists(), extra_transport_calls=0, extra_linear_solves=0))
        raise


def actual_candidate(c, prepared_sha, status_sha, api, reference_seal_sha, qualification_sha,
                     build_seal_sha, terminal_path, terminal_sha):
    absent(PROD / "ABA")
    stable_qualification_identity(api)
    info = c.verify_prepared(PROD / "prepared.json", prepared_sha)
    status = read(require(PROD / "AAA/run_status.json", status_sha))
    builder = build_factory()
    scope = builder.resource_scope_contract()
    if (api["reference_root"] != str(REFERENCE) or api["reference_seal_sha256"] != reference_seal_sha
            or api["qualification"] != dict(path=str(FORMAL), sha256=qualification_sha)
            or api["production_prepared"] != dict(path=str(PROD / "prepared.json"), sha256=prepared_sha)
            or api["AAA_status"] != dict(path=str(PROD / "AAA/run_status.json"), sha256=status_sha)
            or api["actual_external_terminal_evidence"] != dict(path=str(terminal_path), sha256=terminal_sha)
            or Path(terminal_path) != TERMINAL_ROOT / "terminal_return.json"
            or api["original_qualify_aba_guard_passed"] is not True or api["pending_receipt_eligible"] is not False
            or api[LIFECYCLE_FIELD] is not False
            or api["resource_scope_policy"] != HISTORY_SCOPE_POLICY or api["resource_scope_contract"] != scope
            or api["current_complete_history_admission_required"] is not True
            or set(api["all_original_eight_checks"]) != set(GATES)
            or any(value != "PASS" for value in api["all_original_eight_checks"].values())
            or info["experiment_id"] != EXPERIMENT or info["classification"] != "PREPARED_NO_TRANSPORT"
            or info["cases"] != ["AAA", "ABA"] or info["budgets"] != BUDGET
            or status["classification"] != "WAITING_REFERENCE" or status["case"] != "AAA"
            or status["prepared_sha256"] != prepared_sha or status["cases"]["AAA"]["classification"] != "VALID_MET"
            or status.get("error") is not None
            or status["final_resources"]["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or status["final_resources"]["resource_scope_contract"] != scope):
        raise ValueError("actual sealed new qualification/prepared/status/original-budget identities differ")
    require(FORMAL, qualification_sha)
    require(terminal_path, terminal_sha)
    original_guard = c.qualify_aba(info, PROD, prepared_sha, FORMAL, qualification_sha)
    if original_guard != api["qualification"]:
        raise ValueError("original production ABA guard differs from actual sealed CE API")
    if build_seal_sha != BUILD_SEAL:
        raise ValueError("actual successful externally completed rank1-factor-cache build required")
    item = api["actual_build_terminal_evidence"]
    if Path(item["path"]) != BUILD_TERMINAL / "terminal_return.json":
        raise ValueError("actual build terminal evidence must come from the fixed independent Root record")
    build = builder.production_admission(build_seal_sha, item["path"], item["sha256"])
    chain = dict(factory=pin(BUILD_FACTORY), declaration=pin(BUILD / "declaration.json"),
        build_seal=pin(BUILD / "seal.json"), driver_result=pin(BUILD / "driver_result.json"),
        full_stdout=build["actual_external_terminal_validation"]["full_stdout"],
        terminal_evidence=build["actual_external_terminal_evidence"])
    declaration = read(require(info["declaration"]["path"], info["declaration"]["sha256"]))
    require(COUPLING_FACTORY, COUPLING_FACTORY_SHA)
    bind_runtime_dependencies(info)
    runtime_admission = load(PROD / "runtime/rank1_factor_cache_admission.py", "rank1_factor_cache_admission")
    metadata = runtime_admission.metadata(declaration["rank1_factor_cache_revision"])
    reference_prepared = read(require(REFERENCE / "prepared.json"))
    reference_declaration_item = reference_prepared["declaration"]
    if reference_declaration_item["path"] != str(REFERENCE_SOURCE / "declaration.json"):
        raise ValueError("actual new reference must bind its own frozen factory declaration")
    reference = read(require(reference_declaration_item["path"], reference_declaration_item["sha256"]))
    require(REFERENCE / "declaration.json", reference_declaration_item["sha256"])
    if (build["schema"] != "AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or build["build_root"] != str(BUILD) or build["build_seal_sha256"] != build_seal_sha
            or build["resource_scope_policy"] != HISTORY_SCOPE_POLICY or build["resource_scope_contract"] != scope
            or build["current_complete_history_admission_required"] is not True
            or build["full_FLU_entry_execution_proved_by_build"] is not False
            or build["AAA_accuracy_qualified"] is not False or build["ABA_admitted"] is not False
            or build["future_actual_FLU_observer_required"]["expected"] != OBSERVER_EXPECTED
            or build["future_actual_factor_cache_observer_required"] != CACHE_OBSERVER_CONTRACT
            or build["rank1_factor_cache_budget_bytes"] != 536870912
            or any(build[key] is not True for key in ("rank1_factor_cache_controls_passed",
                "all_new_cache_outputs_bitwise_equal_to_uncached", "operator_identity_guard_negative_controls_passed",
                "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required"))
            or info["runtime_sources"]["Dragon"] != build["corrected_runtime"]
            or digest(PROD / "runtime/Dragon") != build["corrected_runtime"]["sha256"]
            or declaration["helper"] != pin(COUPLING_FACTORY)
            or metadata["build_admission"] != build or reference["build_admission"] != build
            or api["actual_build_terminal_evidence"] != build["actual_external_terminal_evidence"]
            or api["actual_build_terminal_validation"] != build["actual_external_terminal_validation"]
            or api["build_terminal_chain"] != chain or metadata["build_terminal_chain"] != chain
            or metadata["build_terminal_evidence"] != api["actual_build_terminal_evidence"]
            or metadata["build_terminal_validation"] != api["actual_build_terminal_validation"]
            or metadata["resource_scope_policy"] != HISTORY_SCOPE_POLICY or metadata["resource_scope_contract"] != scope
            or reference["actual_build_terminal_evidence"] != item
            or reference["actual_build_terminal_validation"] != api["actual_build_terminal_validation"]
            or reference["build_terminal_chain"] != chain or reference["coupling_completion"] != api["coupling_completion"]
            or reference["production_prepared"] != api["production_prepared"] or reference["AAA_status"] != api["AAA_status"]
            or reference["original_eight_gates"] != list(GATES)
            or reference["actual_coupling_factory"] != pin(COUPLING_FACTORY)
            or reference["old_assessment_or_qualification_inherited"] is not False
            or api["coupling_completion"]["all_actual_axial_selectors_verified"] is not True
            or api["coupling_completion"]["all_actual_rank1_factor_cache_guards_verified"] is not True
            or api["coupling_completion"]["coupling_revision"] != declaration["rank1_factor_cache_revision"]):
        raise ValueError("actual runtime/build/Root terminal/coupling/measurement/collector ancestry differs")
    verify({value["path"]: value["sha256"] for value in chain.values()})
    verify(reference["files"])
    verify(metadata["files"])
    # The actual build API already rechecks every frozen predecessor file.
    # Keep these two explicit original scientific-contract identities too;
    # future_contract is a contract descriptor, not a files inventory.
    for key in ("original_prepared", "case_spec"):
        dependency = build["future_contract"][key]
        require(dependency["path"], dependency["sha256"])
    recipe = metadata["reference_analysis_recipe"]
    require(recipe["path"], recipe["sha256"])
    production = producer_environment(info)
    return info, status, build, production, original_guard


def original_command(info, prepared_sha, qualification_sha, producer):
    return [producer["executable"]["path"], str(PROD / "runtime/production_runner.py"), "run",
        str(PROD / "prepared.json"), "--sha256", prepared_sha, "--case", "ABA",
        "--reference-qualification", str(FORMAL), "--reference-sha256", qualification_sha]


def declare(prepared_sha, status_sha, reference_seal_sha, qualification_sha,
            terminal_path, terminal_sha, ce_factory_sha, build_seal_sha):
    absent(PROD / "ABA")
    absent(SOURCE)
    if BUILD_SEAL == "0" * 64 or CONTROLLER_SHA == "0" * 64:
        raise ValueError("future source only: actual successful build and prepared controller are not yet bound")
    require(TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA)
    require(COUPLING_FACTORY, COUPLING_FACTORY_SHA)
    if ce_factory_sha != CE_FACTORY_SHA or build_seal_sha != BUILD_SEAL:
        raise ValueError("actual frozen CE source and completed rank1-factor-cache build identities required")
    raw_info = read(require(PROD / "prepared.json", prepared_sha))
    producer_environment(raw_info)
    require(CE_FACTORY, ce_factory_sha)
    require(REFERENCE / "seal.json", reference_seal_sha)
    require(FORMAL, qualification_sha)
    if Path(terminal_path) != TERMINAL_ROOT / "terminal_return.json":
        raise ValueError("the actual external CE terminal record must use its fixed independent path")
    terminal = pin(require(terminal_path, terminal_sha))
    c = controller()
    roots = roots_for(raw_info, terminal_path)
    resources, before_API = current_resources(c, roots, ADMISSION_RESERVE)
    SOURCE.mkdir()
    (SOURCE / "runtime").mkdir()
    bounded = require(PROD / "runtime/run_bounded_dragon.py", raw_info["local_files"]["runtime/run_bounded_dragon.py"])
    shutil.copy2(bounded, SOURCE / "runtime/run_bounded_dragon.py")
    api, receipt = bounded_reference_call("DECLARE", c, raw_info, ce_factory_sha,
        reference_seal_sha, qualification_sha, terminal_path, terminal_sha, resources)
    info, status, build, producer, guard = actual_candidate(c, prepared_sha, status_sha, api,
        reference_seal_sha, qualification_sha, build_seal_sha, terminal_path, terminal_sha)
    reserve = reservation(c, info, status)
    roots = roots_for(info, terminal_path)
    _, before = current_resources(c, roots, reserve["fresh_ABA_reserve_bytes"])
    monitor = monitor_contract(c, info)
    files = {str(PROD / name): sha for name, sha in info["local_files"].items()}
    files.update({str(path): digest(path) for path in (Path(__file__).resolve(), TEMPLATE_FACTORY, CE_FACTORY,
        BUILD_FACTORY, COUPLING_FACTORY, FULL_FACTORY, PROD / "prepared.json", PROD / "AAA/run_status.json",
        BUILD / "seal.json", REFERENCE / "seal.json", FORMAL, Path(terminal_path),
        Path(info["declaration"]["path"]), Path(info["case_spec"]["path"]), Path(info["rank_addendum"]["path"]))})
    for value in api["build_terminal_chain"].values():
        files[value["path"]] = value["sha256"]
    files[api["actual_external_terminal_validation"]["full_stdout"]["path"]] = api["actual_external_terminal_validation"]["full_stdout"]["sha256"]
    files.update({str(path): digest(path) for path in SOURCE.rglob("*") if path.is_file() and not path.is_symlink()})
    verify(files)
    source_files = {str(path.relative_to(SOURCE)): digest(path) for path in SOURCE.rglob("*") if path.is_file() and not path.is_symlink()}
    admission_archive_gate()
    command = original_command(info, prepared_sha, qualification_sha, producer)
    declaration = dict(schema="AXMAT_RANK1_FACTOR_CACHE_SEALED_REFERENCE_TO_ABA_DECLARATION_V1",
        classification="DECLARED_QUALIFIED_RANK1_FACTOR_CACHE_ABA_HANDOFF_NOT_RUN", declared_unix=time.time(), files=files,
        declared_admission_files=source_files, frozen_template=pin(TEMPLATE_FACTORY),
        helper=pin(Path(__file__).resolve()), CE_factory=pin(CE_FACTORY), production_controller=pin(PROD / "runtime/production_runner.py"),
        production_prepared=pin(PROD / "prepared.json"), AAA_status=pin(PROD / "AAA/run_status.json"),
        reference_seal=pin(REFERENCE / "seal.json"), formal_qualification=pin(FORMAL), actual_external_terminal_evidence=terminal,
        actual_external_terminal_validation=api["actual_external_terminal_validation"],
        build_seal=pin(BUILD / "seal.json"), build_admission=build,
        actual_build_terminal_evidence=api["actual_build_terminal_evidence"],
        actual_build_terminal_validation=api["actual_build_terminal_validation"], build_terminal_chain=api["build_terminal_chain"],
        coupling_completion=api["coupling_completion"], actual_reference_API=api,
        declaration_read_only_API_receipt=receipt, original_production_qualify_aba=guard,
        actual_qualification_lifecycle=lifecycle_contract(), producer_environment=producer,
        reservation=reserve, resource_roots=roots, actual_resource_monitor=monitor,
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=build["resource_scope_contract"],
        current_complete_history_admission_required=True,
        resources_before_API=before_API, resources_after_actual_guards_and_reservation=before,
        production_command=command, original_case_budgets=BUDGET, original_gate_names=list(GATES),
        artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR, read_only_API_wall_seconds=READ_ONLY_CAP,
        read_only_API_rss_cap_mib=READ_ONLY_RSS, numeric_children_at_once=1, threads=1, retries=0,
        production_prepared_monitor_roots=info["resource_roots"], frozen_production_source_and_scientific_callables_changed=False,
        explicit_resource_monitor_binding_changed=False, pending_receipt_eligible=False,
        extra_transport_calls=0, extra_linear_solves=0, ABA_started=False)
    write_new(SOURCE / "declaration.json", declaration)
    admission_archive_gate()
    current_resources(c, roots, reserve["fresh_ABA_reserve_bytes"])
    print(json.dumps(dict(classification=declaration["classification"], declaration=pin(SOURCE / "declaration.json"), ABA_started=False)))


def run(expected):
    absent(PROD / "ABA")
    d = read(require(SOURCE / "declaration.json", expected))
    builder = build_factory()
    if (d["schema"] != "AXMAT_RANK1_FACTOR_CACHE_SEALED_REFERENCE_TO_ABA_DECLARATION_V1"
            or d["classification"] != "DECLARED_QUALIFIED_RANK1_FACTOR_CACHE_ABA_HANDOFF_NOT_RUN"
            or d["helper"] != pin(Path(__file__).resolve()) or d["frozen_template"] != pin(require(TEMPLATE_FACTORY, TEMPLATE_FACTORY_SHA))
            or d["CE_factory"] != pin(require(CE_FACTORY, CE_FACTORY_SHA))
            or d["build_seal"] != pin(require(BUILD / "seal.json", BUILD_SEAL))
            or d["artifact_budget_bytes"] != HISTORY_CAP or d["min_free_bytes"] != FREE_FLOOR
            or d["original_case_budgets"] != BUDGET or d["original_gate_names"] != list(GATES)
            or d["threads"] != 1 or d["numeric_children_at_once"] != 1 or d["retries"] != 0
            or d["read_only_API_wall_seconds"] != READ_ONLY_CAP or d["read_only_API_rss_cap_mib"] != READ_ONLY_RSS
            or d["pending_receipt_eligible"] is not False
            or d["frozen_production_source_and_scientific_callables_changed"] is not False
            or d["explicit_resource_monitor_binding_changed"] is not False
            or d["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or d["resource_scope_contract"] != builder.resource_scope_contract()
            or d["current_complete_history_admission_required"] is not True
            or d["actual_qualification_lifecycle"] != lifecycle_contract()):
        raise ValueError("the immutable qualified rank1-factor-cache ABA handoff contract differs")
    verify(d["files"])
    absent(SOURCE / "RUN")
    actual_files = {str(path.relative_to(SOURCE)) for path in SOURCE.rglob("*") if path.is_file()}
    if actual_files != set(d["declared_admission_files"]) | {"declaration.json"}:
        raise ValueError("the exclusive declared read-only admission namespace changed")
    verify({str(SOURCE / name): sha for name, sha in d["declared_admission_files"].items()})
    admission_archive_gate()
    raw_info = read(PROD / "prepared.json")
    producer_environment(raw_info, d["producer_environment"])
    c = controller()
    terminal = d["actual_external_terminal_evidence"]
    roots = roots_for(raw_info, terminal["path"])
    if not set(d["resource_roots"]).issubset(roots):
        raise ValueError("current complete-history roots lost a declared dependency")
    resources, _ = current_resources(c, roots, d["reservation"]["fresh_ABA_reserve_bytes"])
    api, receipt = bounded_reference_call("RUN", c, raw_info, d["CE_factory"]["sha256"],
        d["reference_seal"]["sha256"], d["formal_qualification"]["sha256"], terminal["path"], terminal["sha256"], resources)
    if api != d["actual_reference_API"]:
        raise ValueError("the two launch-time whole actual sealed CE API returns differ")
    info, status, build, producer, guard = actual_candidate(c, d["production_prepared"]["sha256"], d["AAA_status"]["sha256"], api,
        d["reference_seal"]["sha256"], d["formal_qualification"]["sha256"], d["build_seal"]["sha256"], terminal["path"], terminal["sha256"])
    if (build != d["build_admission"] or producer != d["producer_environment"]
            or reservation(c, info, status) != d["reservation"] or guard != d["original_production_qualify_aba"]
            or api["actual_external_terminal_validation"] != d["actual_external_terminal_validation"]
            or api["actual_build_terminal_evidence"] != d["actual_build_terminal_evidence"]
            or api["actual_build_terminal_validation"] != d["actual_build_terminal_validation"]
            or api["build_terminal_chain"] != d["build_terminal_chain"] or api["coupling_completion"] != d["coupling_completion"]):
        raise ValueError("current rank1-factor-cache runtime/Root terminal chain/producer/reservation/original guard changed")
    command = original_command(info, d["production_prepared"]["sha256"], d["formal_qualification"]["sha256"], producer)
    if command != d["production_command"] or monitor_contract(c, info) != d["actual_resource_monitor"]:
        raise ValueError("actual frozen production callables, dynamic monitor or original ABA CLI arguments changed")
    # The frozen current body repeats qualification/prepared checks before its
    # exclusive case claim. No local callable or resource binding is changed.
    verify(d["files"])
    absent(PROD / "ABA")
    _, snapshot = current_resources(c, roots, d["reservation"]["fresh_ABA_reserve_bytes"])
    frozen = {name: getattr(c, name) for name in ("run", "qualify_aba", "SerialExecutor", "resource_monitor")}
    write_new(SOURCE / "RUN/handoff.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_ACTUAL_ABA_HANDOFF_V1",
        classification="ALL_GUARDS_PASSED_CALL_FROZEN_RANK1_FACTOR_CACHE_ABA_RUN_WITH_EXISTING_DYNAMIC_MONITOR",
        declaration_sha256=expected, actual_repeated_CE_API_receipt=receipt,
        actual_external_terminal_evidence=terminal, actual_external_terminal_validation=d["actual_external_terminal_validation"],
        actual_build_terminal_evidence=d["actual_build_terminal_evidence"],
        actual_build_terminal_validation=d["actual_build_terminal_validation"], build_terminal_chain=d["build_terminal_chain"],
        coupling_completion=d["coupling_completion"], actual_launch_reference_API=api,
        actual_qualification_lifecycle=d["actual_qualification_lifecycle"],
        formal_qualification=d["formal_qualification"], production_prepared=d["production_prepared"], AAA_status=d["AAA_status"],
        original_guard=guard, current_resources=snapshot, fresh_ABA_reservation=d["reservation"],
        equivalent_original_CLI_arguments=command, producer_environment=producer, production_case_directory_created=False,
        actual_resource_monitor=d["actual_resource_monitor"], resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=d["resource_scope_contract"], scientific_callables_and_budgets_changed=False,
        resource_monitor_binding_changed=False, source_files_and_module_identity_changed=False,
        pending_receipt_eligible=False))
    absent(PROD / "ABA")
    admission_archive_gate()
    current_resources(c, roots, d["reservation"]["fresh_ABA_reserve_bytes"])
    if any(getattr(c, name) is not function for name, function in frozen.items()):
        raise ValueError("an actual frozen production callable changed before launch")
    if monitor_contract(c, info) != d["actual_resource_monitor"]:
        raise ValueError("actual admitted dynamic production monitor changed immediately before launch")
    result = c.run(PROD / "prepared.json", d["production_prepared"]["sha256"], "ABA",
        FORMAL, d["formal_qualification"]["sha256"])
    if any(getattr(c, name) is not function for name, function in frozen.items()):
        raise ValueError("an actual frozen production callable changed during the ABA attempt")
    # Root retains the actual tool return/stdout; handoff alone never proves
    # completion or independent ABA accuracy. Actual run_status/seals govern.
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("declare", "run"))
    parser.add_argument("--sha256")
    parser.add_argument("--prepared-sha256")
    parser.add_argument("--status-sha256")
    parser.add_argument("--reference-seal-sha256")
    parser.add_argument("--qualification-sha256")
    parser.add_argument("--terminal-evidence", type=Path)
    parser.add_argument("--terminal-evidence-sha256")
    parser.add_argument("--ce-factory-sha256")
    parser.add_argument("--build-seal-sha256")
    args = parser.parse_args()
    if args.action == "declare":
        required = (args.prepared_sha256, args.status_sha256, args.reference_seal_sha256,
            args.qualification_sha256, args.terminal_evidence, args.terminal_evidence_sha256,
            args.ce_factory_sha256, args.build_seal_sha256)
        if (not all(required) or any(not re.fullmatch(r"[0-9a-f]{64}", value)
                for value in required if not isinstance(value, Path))):
            parser.error("declare requires actual prepared/status/reference-seal/formal/terminal-evidence/CE-source/build SHA256 identities")
        declare(*required)
    elif not args.sha256 or not re.fullmatch(r"[0-9a-f]{64}", args.sha256):
        parser.error("run requires the actual immutable admission declaration --sha256")
    else:
        run(args.sha256)
