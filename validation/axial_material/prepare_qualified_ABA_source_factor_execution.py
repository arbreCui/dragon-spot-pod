"""Declare and hand off one future source-factor ABA attempt.

This entrance is deliberately separate from every frozen production source.
Each declaration and launch first makes a real, bounded, read-only call to the
new sealed CE qualification API in its own Python 3.12 environment. The parent
uses the unchanged producer Python 3.14 environment, repeats the original ABA
guard, and admits the complete history plus a fresh measured-case reservation.
It calls the frozen production run body with an explicitly declared temporary
resource-monitor binding that adds the complete current artifact history.
Physics, iteration and budget callables are unchanged. No ABA path is created
by the entrance; only the original run body can claim that case directory.
There are no default or anticipated reference/qualification/terminal hashes.
"""

import argparse
import functools
import hashlib
import importlib.util
import inspect
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
PROD = ART / "axial-material-production-qualified-AB-source-factor-20261006"
REFERENCE = ART / "axial-material-qualified-AAA-source-factor-reference-20261006"
REFERENCE_SOURCE = ART / "axial-material-qualified-AAA-source-factor-reference-admission-20261006"
TERMINAL_ROOT = ART / "axial-material-qualified-AAA-source-factor-reference-terminal-20261006"
SOURCE = ART / "axial-material-qualified-ABA-source-factor-execution-admission-20261006"
BUILD = ART / "axial-material-source-factor-build-20261006"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
CE_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AAA_source_factor_reference_analysis.py"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_source_factor_production.py"
FULL_FACTORY = ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py"
FORMAL = REFERENCE / "AAA/reference_qualification.json"
BUILD_SEAL = "2a005852d49e4929e05b6835d5b8a51f9ce68afb6f15fc665fb5e7bd7547ed1e"
BUILD_FACTORY_SHA = "619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743"
FULL_FACTORY_SHA = "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6"
CONTROLLER_SHA = "de1046ccd43a6053c3fd6accf13ab967f4ea4043c180e78bda962e3ebf166d7b"
EXPERIMENT = "axial-material-qualified-AB-rank1-source-factor-20261006"
GATES = ("input_equivalence", "source_convergence", "block_stability", "statistical_resolution",
         "keff", "scalar_flux", "nu_fission", "currents_balance_symmetry")
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
BUDGET = dict(axial_seconds=4200, bootstrap_axial_seconds=4200, bootstrap_radial_seconds=600,
              host_seconds=120, max_maps=100, radial_seconds=300, setup_seconds=120, total_seconds=43200)
HISTORY_CAP, FREE_FLOOR = 96 * 2**30, 8 * 2**30
ADMISSION_RESERVE = 64 * 2**20
READ_ONLY_CAP, READ_ONLY_RSS = 120, 512


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
    return json.loads(Path(path).read_text())


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
    path = require(PROD / "runtime/production_runner.py", CONTROLLER_SHA)
    sys.path.insert(0, str(path.parent))
    return load(path, "production_runner")


def bind_runtime_dependencies(raw_info):
    """Establish true canonical source paths before the older guard helper imports."""
    names = ("production_inputs", "snapshot_control_preflight", "analyze_r64_snapshot",
        "analyze_r64_tracking_moments", "check_r64_audit_rejections", "check_r64_normalization_rejections",
        "qualified_snapshot_ingestion", "numerical_layout_admission", "source_factor_admission")
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
    item = declaration["source_factor_revision"]
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
    if (env["schema"] != "AXMAT_SOURCEFACTOR_SEPARATE_CE_ENVIRONMENT_V1"
            or not env["python_version"].startswith("3.12.") or env["numpy_version"] != "2.4.3"
            or env["producer_environment_is_separate"] is not True
            or env["thread_environment"] != {key: "1" for key in THREADS}):
        raise ValueError("actual separately frozen CE analysis environment required")
    verify(env["files"])
    require(Path(env["executable"]), env["files"][env["executable"]])
    return item, env


def roots_for(info, terminal_path):
    values = set(info["resource_roots"])
    for root in (BUILD, FULL, CAUSAL, REFERENCE):
        values.update(read(require(root / "declaration.json"))["resource_roots"])
    values.update(str(path) for path in ART.glob("axial-material-*") if path.is_dir())
    values.update((str(SOURCE), str(PROD), str(REFERENCE), str(REFERENCE_SOURCE)))
    terminal = Path(terminal_path)
    if not terminal.is_absolute() or ".." in terminal.parts or not terminal.is_relative_to(ART):
        raise ValueError("actual external terminal evidence must be in a separate project artifact root")
    root = ART / terminal.relative_to(ART).parts[0]
    if root in (PROD, REFERENCE, REFERENCE_SOURCE, SOURCE):
        raise ValueError("actual terminal evidence must remain in an independent artifact root")
    values.add(str(root))
    return sorted(values)


def current_resources(c, roots, reserve):
    resources = c.DiskResources(ART, roots, FREE_FLOOR, HISTORY_CAP)
    snapshot = resources.check()
    if snapshot["artifact_bytes"] + reserve >= HISTORY_CAP or snapshot["disk_free_bytes"] - reserve < FREE_FLOOR:
        raise ValueError("complete current history plus fresh ABA reservation does not fit unchanged 96GiB/free8GiB caps")
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
    return dict(schema="AXMAT_SOURCEFACTOR_FRESH_ABA_RESERVATION_V1", method="1.5*actual_qualified_AAA_case_regular_bytes+1GiB+64MiB",
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


def complete_history_resource_monitor(c, original_monitor, admitted_roots, info):
    """Explicit resource-only overlay; no prepared metadata or scientific callable mutation."""
    original = original_monitor(info)
    if (original.artifacts_root.resolve() != ART.resolve() or original.min_free_bytes != FREE_FLOOR
            or original.max_bytes != HISTORY_CAP or not set(info["resource_roots"]).issubset(admitted_roots)):
        raise ValueError("original producer resource scope/caps differ from the declared overlay")
    return c.DiskResources(ART, list(admitted_roots), FREE_FLOOR, HISTORY_CAP)


def monitor_contract(c, roots):
    return dict(schema="AXMAT_SOURCEFACTOR_EXPLICIT_RESOURCE_SCOPE_OVERLAY_V1",
        actual_binding="production_runner.resource_monitor", original=callable_pin(c.resource_monitor),
        overlay=callable_pin(complete_history_resource_monitor),
        frozen_scientific_callables={name: callable_pin(getattr(c, name)) for name in ("run", "qualify_aba", "SerialExecutor")},
        admitted_complete_history_roots=roots, artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR,
        binding_method="temporary functools.partial; try/finally restore the original callable",
        resources_only=True, controller_execution_behavior_word_exact_claimed=False,
        prepared_or_runtime_files_changed=False, module_identity_reassigned=False)


def supervision(c, raw_info, ce_factory_sha):
    require(FULL_FACTORY, FULL_FACTORY_SHA)
    require(BUILD_FACTORY, BUILD_FACTORY_SHA)
    bind_runtime_dependencies(raw_info)
    ce = load(require(CE_FACTORY, ce_factory_sha), "source_factor_ABA_reference_dependency")
    full = load(FULL_FACTORY, "source_factor_ABA_own_RSS_guard")
    builder = load(BUILD_FACTORY, "source_factor_ABA_build_dependency")
    proof = ce.live_guard_provenance(full, c, raw_info)
    files = builder.guard_admission(full)
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
        returned = json.loads(log.read_text())
        write_new(folder / "ce_api_return.json", returned)
        receipt = dict(schema="AXMAT_SOURCEFACTOR_BOUNDED_REFERENCE_API_RECEIPT_V1",
            classification="COMPLETE_READ_ONLY_REFERENCE_QUALIFICATION_API_CALL", phase=phase,
            command=command, returncode=0, stdout=pin(log), actual_API_return=pin(folder / "ce_api_return.json"),
            watchdog=pin(watchdog), stages=pin(folder / "stages.json"), guard=guard, guard_files=guard_files,
            analysis_environment=env_item, exact_child_loader_environment=env["loader_environment"],
            thread_environment={key: child_env[key] for key in THREADS}, wall_cap_seconds=READ_ONLY_CAP,
            rss_cap_mib=READ_ONLY_RSS, numeric_children_at_once=1, retries=0,
            extra_transport_calls=0, extra_linear_solves=0, AAA_scientific_stages_added=0, ABA_created=False)
        write_new(folder / "receipt.json", receipt)
        return returned, pin(folder / "receipt.json")
    except BaseException as error:
        write_new(folder / "failure.json", dict(classification="FAILED_READ_ONLY_REFERENCE_API_NO_RETRY", error=repr(error),
            production_ABA_created=(PROD / "ABA").exists(), extra_transport_calls=0, extra_linear_solves=0))
        raise


def actual_candidate(c, prepared_sha, status_sha, api, reference_seal_sha, qualification_sha,
                     build_seal_sha, terminal_path, terminal_sha):
    absent(PROD / "ABA")
    info = c.verify_prepared(PROD / "prepared.json", prepared_sha)
    status = read(require(PROD / "AAA/run_status.json", status_sha))
    if (api["schema"] != "AXMAT_SOURCEFACTOR_SEALED_REFERENCE_QUALIFICATION_ADMISSION_V1"
            or api["reference_root"] != str(REFERENCE) or api["reference_seal_sha256"] != reference_seal_sha
            or api["qualification"] != dict(path=str(FORMAL), sha256=qualification_sha)
            or api["production_prepared"] != dict(path=str(PROD / "prepared.json"), sha256=prepared_sha)
            or api["AAA_status"] != dict(path=str(PROD / "AAA/run_status.json"), sha256=status_sha)
            or api["actual_external_terminal_evidence"] != dict(path=str(terminal_path), sha256=terminal_sha)
            or Path(terminal_path) != TERMINAL_ROOT / "terminal_return.json"
            or api["original_qualify_aba_guard_passed"] is not True
            or api["pending_receipt_eligible"] is not False or api["ABA_started"] is not False
            or set(api["all_original_eight_checks"]) != set(GATES)
            or any(value != "PASS" for value in api["all_original_eight_checks"].values())
            or info["experiment_id"] != EXPERIMENT or info["classification"] != "PREPARED_NO_TRANSPORT"
            or info["cases"] != ["AAA", "ABA"] or info["budgets"] != BUDGET
            or status["classification"] != "WAITING_REFERENCE" or status["case"] != "AAA"
            or status["prepared_sha256"] != prepared_sha or status["cases"]["AAA"]["classification"] != "VALID_MET"):
        raise ValueError("actual sealed new qualification/prepared/status/original-budget identities differ")
    require(FORMAL, qualification_sha)
    require(terminal_path, terminal_sha)
    original_guard = c.qualify_aba(info, PROD, prepared_sha, FORMAL, qualification_sha)
    if original_guard != api["qualification"]:
        raise ValueError("original production ABA guard differs from actual sealed CE API")
    if build_seal_sha != BUILD_SEAL:
        raise ValueError("actual successful bounded source-factor build required")
    builder = load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), "source_factor_ABA_build_dependency")
    build = builder.production_admission(build_seal_sha)
    if info["runtime_sources"]["Dragon"] != build["corrected_runtime"]:
        raise ValueError("actual fresh production runtime does not match source-factor build")
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
    files = {str(PROD / name): sha for name, sha in info["local_files"].items()}
    files.update({str(path): digest(path) for path in (Path(__file__).resolve(), CE_FACTORY, BUILD_FACTORY, FULL_FACTORY,
        PROD / "prepared.json", PROD / "AAA/run_status.json", BUILD / "seal.json", REFERENCE / "seal.json", FORMAL, Path(terminal_path),
        Path(info["declaration"]["path"]), Path(info["case_spec"]["path"]), Path(info["rank_addendum"]["path"]))})
    files.update({str(path): digest(path) for path in SOURCE.rglob("*") if path.is_file() and not path.is_symlink()})
    verify(files)
    source_files = {str(path.relative_to(SOURCE)): digest(path) for path in SOURCE.rglob("*") if path.is_file() and not path.is_symlink()}
    admission_archive_gate()
    command = original_command(info, prepared_sha, qualification_sha, producer)
    declaration = dict(schema="AXMAT_SOURCEFACTOR_SEALED_REFERENCE_TO_ABA_DECLARATION_V1",
        classification="DECLARED_QUALIFIED_SOURCEFACTOR_ABA_HANDOFF_NOT_RUN", declared_unix=time.time(), files=files,
        declared_admission_files=source_files,
        helper=pin(Path(__file__).resolve()), CE_factory=pin(CE_FACTORY), production_controller=pin(PROD / "runtime/production_runner.py"),
        production_prepared=pin(PROD / "prepared.json"), AAA_status=pin(PROD / "AAA/run_status.json"),
        reference_seal=pin(REFERENCE / "seal.json"), formal_qualification=pin(FORMAL), actual_external_terminal_evidence=terminal,
        build_seal=pin(BUILD / "seal.json"), build_admission=build, actual_reference_API=api,
        declaration_read_only_API_receipt=receipt, original_production_qualify_aba=guard,
        producer_environment=producer, reservation=reserve, resource_roots=roots,
        explicit_resource_monitor_overlay=monitor_contract(c, roots),
        resources_before_API=before_API, resources_after_actual_guards_and_reservation=before,
        production_command=command, original_case_budgets=BUDGET, original_gate_names=list(GATES),
        artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR, read_only_API_wall_seconds=READ_ONLY_CAP,
        read_only_API_rss_cap_mib=READ_ONLY_RSS, numeric_children_at_once=1, threads=1, retries=0,
        production_prepared_monitor_roots=info["resource_roots"], frozen_production_source_and_scientific_callables_changed=False,
        explicit_resource_monitor_binding_changed=True,
        pending_receipt_eligible=False, extra_transport_calls=0, extra_linear_solves=0, ABA_started=False)
    write_new(SOURCE / "declaration.json", declaration)
    admission_archive_gate()
    print(json.dumps(dict(classification=declaration["classification"], declaration=pin(SOURCE / "declaration.json"), ABA_started=False)))


def run(expected):
    absent(PROD / "ABA")
    d = read(require(SOURCE / "declaration.json", expected))
    if (d["schema"] != "AXMAT_SOURCEFACTOR_SEALED_REFERENCE_TO_ABA_DECLARATION_V1"
            or d["classification"] != "DECLARED_QUALIFIED_SOURCEFACTOR_ABA_HANDOFF_NOT_RUN"
            or d["helper"] != pin(Path(__file__).resolve()) or d["artifact_budget_bytes"] != HISTORY_CAP
            or d["min_free_bytes"] != FREE_FLOOR or d["original_case_budgets"] != BUDGET
            or d["original_gate_names"] != list(GATES) or d["threads"] != 1 or d["numeric_children_at_once"] != 1
            or d["retries"] != 0 or d["read_only_API_wall_seconds"] != READ_ONLY_CAP
            or d["read_only_API_rss_cap_mib"] != READ_ONLY_RSS
            or d["pending_receipt_eligible"] is not False
            or d["frozen_production_source_and_scientific_callables_changed"] is not False
            or d["explicit_resource_monitor_binding_changed"] is not True):
        raise ValueError("the immutable qualified ABA handoff contract differs")
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
        raise ValueError("the actual newly repeated sealed CE qualification API changed")
    info, status, build, producer, guard = actual_candidate(c, d["production_prepared"]["sha256"], d["AAA_status"]["sha256"], api,
        d["reference_seal"]["sha256"], d["formal_qualification"]["sha256"], d["build_seal"]["sha256"], terminal["path"], terminal["sha256"])
    if (build != d["build_admission"] or producer != d["producer_environment"]
            or reservation(c, info, status) != d["reservation"] or guard != d["original_production_qualify_aba"]):
        raise ValueError("current source-factor runtime/producer/reservation/original guard changed")
    command = original_command(info, d["production_prepared"]["sha256"], d["formal_qualification"]["sha256"], producer)
    if command != d["production_command"]:
        raise ValueError("original ABA CLI handoff arguments changed")
    declared_monitor = monitor_contract(c, d["resource_roots"])
    if declared_monitor != d["explicit_resource_monitor_overlay"]:
        raise ValueError("declared original/new resource monitor or frozen scientific callable proof changed")
    active_monitor = monitor_contract(c, roots)
    # The original runtime also repeats its own qualification and immutable
    # prepared checks before its exclusive case-directory claim.
    verify(d["files"])
    absent(PROD / "ABA")
    _, snapshot = current_resources(c, roots, d["reservation"]["fresh_ABA_reserve_bytes"])
    original_monitor = c.resource_monitor
    scientific = {name: getattr(c, name) for name in ("run", "qualify_aba", "SerialExecutor")}
    c.resource_monitor = functools.partial(complete_history_resource_monitor, c, original_monitor, tuple(roots))
    try:
        binding = c.resource_monitor
        if (not isinstance(binding, functools.partial) or binding.func is not complete_history_resource_monitor
                or binding.args != (c, original_monitor, tuple(roots)) or binding.keywords != {}):
            raise ValueError("actual explicit resource-monitor binding differs from its declaration")
        if any(getattr(c, name) is not obj for name, obj in scientific.items()):
            raise ValueError("frozen scientific callables changed before ABA launch")
        write_new(SOURCE / "RUN/handoff.json", dict(schema="AXMAT_SOURCEFACTOR_ACTUAL_ABA_HANDOFF_V1",
            classification="ALL_GUARDS_PASSED_CALL_FROZEN_ABA_RUN_WITH_EXPLICIT_RESOURCE_OVERLAY", declaration_sha256=expected,
            actual_repeated_CE_API_receipt=receipt, actual_external_terminal_evidence=terminal,
            formal_qualification=d["formal_qualification"], production_prepared=d["production_prepared"], AAA_status=d["AAA_status"],
            original_guard=guard, current_resources=snapshot, fresh_ABA_reservation=d["reservation"],
            equivalent_original_CLI_arguments=command, producer_environment=producer, production_case_directory_created=False,
            explicit_resource_monitor_overlay=active_monitor, scientific_callables_and_budgets_changed=False,
            actual_resource_monitor_binding=dict(type="functools.partial", function=callable_pin(binding.func),
                original_resource_monitor=callable_pin(original_monitor), actual_controller=pin(c.__file__),
                admitted_roots=list(binding.args[2]), keywords=binding.keywords,
                func_and_all_bound_arguments_match=True, source_files_and_module_identity_changed=False),
            resource_monitor_scope_explicitly_extended=True, pending_receipt_eligible=False))
        # Repeat current storage checks after the final admission output and
        # the real binding. Only the original body can now claim PROD/ABA.
        absent(PROD / "ABA")
        admission_archive_gate()
        current_resources(c, roots, d["reservation"]["fresh_ABA_reserve_bytes"])
        result = c.run(PROD / "prepared.json", d["production_prepared"]["sha256"], "ABA",
            FORMAL, d["formal_qualification"]["sha256"])
    finally:
        c.resource_monitor = original_monitor
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
        if not all(required):
            parser.error("declare requires actual prepared/status/reference-seal/formal/terminal-evidence/CE-source/build SHA256 identities")
        declare(*required)
    elif not args.sha256:
        parser.error("run requires the actual immutable admission declaration --sha256")
    else:
        run(args.sha256)
