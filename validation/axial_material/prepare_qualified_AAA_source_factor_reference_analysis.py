"""Bind actual new source-factor AAA to complete original-gate CE reassessment.

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
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path("/Users/wen/spot")
ART = ROOT / "validation/artifacts"
PROD = ART / "axial-material-production-qualified-AB-source-factor-20261006"
COUPLING = ART / "axial-material-qualified-AB-source-factor-admission-20261006"
SOURCE = ART / "axial-material-qualified-AAA-source-factor-reference-admission-20261006"
OUT = ART / "axial-material-qualified-AAA-source-factor-reference-20261006"
TERMINAL = ART / "axial-material-qualified-AAA-source-factor-reference-terminal-20261006"
CE = ART / "axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004"
OLD_SOURCE = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"
BUILD = ART / "axial-material-source-factor-build-20261006"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_source_factor_production.py"
FULL_FACTORY = ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py"
PHYSICAL = ROOT / "validation/axial_material/review_qualified_AAA_refined_input_identity.py"
EXPORTER = ART / "axial-material-tools-20261003/export_observables"
EXPORT_SOURCE = ROOT / "validation/axial_material/export_observables.f90"
PYTHON = Path("/Users/wen/miniforge3/envs/openmc-dev/bin/python")
BUILD_SEAL = "2a005852d49e4929e05b6835d5b8a51f9ce68afb6f15fc665fb5e7bd7547ed1e"
BUILD_SOURCE_SHA = "619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743"
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
TERMINAL_SCHEMA = "AXMAT_SOURCEFACTOR_CE_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
TAIL_FIELDS = ("full_closeout_tail_gate", "actual_elapsed_through_full_closeout_seconds",
               "actual_complete_archive_bytes", "resources_after_full_closeout")


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


def terminal_contract():
    """Root records the actual terminal return; this factory only consumes it."""
    return dict(schema=TERMINAL_SCHEMA, root=str(TERMINAL), receipt=str(TERMINAL / "terminal_return.json"),
        record_producer="root", full_stdout_is_retained=True, actual_tool_exit_zero_required=True,
        record_written_after_actual_terminal_return_required=True, tail_fields=list(TAIL_FIELDS),
        actual_run_command=[str(PYTHON), str(Path(__file__).resolve()), "run", "--sha256", "__DECLARATION_SHA256__"],
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
    return dict(schema="AXMAT_SOURCEFACTOR_SEPARATE_CE_ENVIRONMENT_V1",
        executable=str(PYTHON.resolve()), python_version=platform.python_version(), numpy_version=np.__version__,
        producer_environment_is_separate=True, files=files,
        thread_environment={key: "1" for key in THREADS}, loader_environment=loader)


def ready(prepared_sha, status_sha, build_seal_sha):
    if build_seal_sha != BUILD_SEAL:
        raise ValueError("actual successful source-factor build seal required")
    require(BUILD_FACTORY, BUILD_SOURCE_SHA)
    builder = module(BUILD_FACTORY, "source_factor_reference_build_dependency")
    build = builder.production_admission(build_seal_sha)
    c = controller()
    info = c.verify_prepared(PROD / "prepared.json", prepared_sha)
    status = read(require(PROD / "AAA/run_status.json", status_sha))
    if (info["classification"] != "PREPARED_NO_TRANSPORT"
            or info["experiment_id"] != "axial-material-qualified-AB-rank1-source-factor-20261006"
            or status["classification"] != "WAITING_REFERENCE" or status["case"] != "AAA"
            or status["prepared_sha256"] != prepared_sha
            or status["cases"].get("AAA", {}).get("classification") != "VALID_MET"
            or status["common_basis_sha256"] != digest(PROD / "training/common_basis.xsm")
            or info["runtime_sources"]["Dragon"] != build["corrected_runtime"]):
        raise ValueError("actual complete new source-factor AAA fixed point required")
    final = Path(status["cases"]["AAA"]["final_directory"])
    if final.parent != PROD / "AAA":
        raise ValueError("actual new AAA final stage must be in its own case")
    for folder in (PROD / "archives", PROD / "training", PROD / "AAA/bootstrap", final):
        c.verify_sealed_directory(folder)
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
    return c, info, status, final, recipe, native, execution, build


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
    gate_item = declaration["source_factor_equivalence"]
    gate = read(require(gate_item["path"], gate_item["sha256"]))
    source_item = gate["source_equivalence"]
    source = read(require(source_item["path"], source_item["sha256"]))
    proof = source["patches"]["production_runner.py"]
    require(proof["candidate"]["path"], proof["candidate"]["sha256"])
    if digest(c.__file__) != proof["candidate"]["sha256"] or "SerialExecutor" not in proof["unchanged_function_AST"]:
        raise ValueError("actual production supervisor differs from its exact source proof")
    revision = declaration["source_factor_revision"]
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
    return dict(schema="AXMAT_SOURCEFACTOR_CE_LIVE_GUARD_PROVENANCE_V1",
        own_RSS_source=pin(FULL_FACTORY), actual_parent_controller=pin(c.__file__),
        original_parent_controller=pin(original), coupling_gate_equivalence=gate_item,
        coupling_source_equivalence=source_item, actual_base_is_verified_current_SerialExecutor=True,
        original_parent_SerialExecutor_AST_exact=True, module_identity_reassigned=False)


ADMISSION = '''"""Bind fresh source-factor measurement to the one bounded reassessment."""
import json
from pathlib import Path
import sys
PROD = Path(__PROD__)
OUT = Path(__OUT__)
sys.path.insert(0, str(PROD / "runtime"))
from production_runner import require_file, sha256, verify_sealed_directory


def verify_measurement_admission(prepared, expected):
    d = json.loads(require_file(OUT / "declaration.json", expected).read_text())
    for name, wanted in d["files"].items():
        require_file(Path(name), wanted)
    status = json.loads(require_file(PROD / "AAA/run_status.json", d["AAA_status"]["sha256"]).read_text())
    claim = json.loads((OUT / "AAA/analysis_claim.json").read_text())
    if (d["schema"] != "AXMAT_SOURCEFACTOR_COMPLETE_ORIGINAL_GATE_REFERENCE_V1"
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


def declare(prepared_sha, status_sha, build_seal_sha):
    env = environment()
    c, info, status, final, recipe, native, execution, build = ready(prepared_sha, status_sha, build_seal_sha)
    if SOURCE.exists() or OUT.exists() or TERMINAL.exists():
        raise ValueError("independent reference roots must be absent; no retry or overwrite")
    require(EXPORTER, EXPORTER_SHA)
    require(EXPORT_SOURCE, EXPORT_SOURCE_SHA)
    require(FULL_FACTORY, FULL_SOURCE_SHA)
    full = module(FULL_FACTORY, "source_factor_reference_guard")
    builder = module(BUILD_FACTORY, "source_factor_reference_build_dependency")
    guard_files = builder.guard_admission(full)
    guard_provenance = live_guard_provenance(full, c, info)
    roots = sorted(set(info["resource_roots"]) | set(read(BUILD / "declaration.json")["resource_roots"])
        | set(read(FULL / "declaration.json")["resource_roots"])
        | set(read(CAUSAL / "declaration.json")["resource_roots"])
        | {str(path.resolve()) for path in ART.glob("axial-material-*") if path.is_dir()}
        | {str(SOURCE), str(OUT), str(TERMINAL)})
    before = c.DiskResources(ART, roots, 8 * 2**30, 96 * 2**30).check()
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
         "PREPARED_SHA = " + repr(prepared_sha), 1)], runtime / "source_factor_physical_identity.py")
    original_collector = recipe["unchanged_reference_implementations"]["assess_qualified_AAA_white_trace_precision.py"]
    require(original_collector["path"], original_collector["sha256"])
    entry = '    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)'
    changes = [
        ("axial-material-production-qualified-AB-white-trace-20261004", PROD.name, 1),
        ("88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf", prepared_sha, 1),
        (entry, entry + '\n    from source_factor_reference_admission import verify_measurement_admission\n'
         '    if len(sys.argv) != 2:\n        raise ValueError("explicit analysis declaration SHA256 required")\n'
         '    current_measurement = verify_measurement_admission(prepared, sys.argv[1])\n'
         '    analysis = Path(' + repr(str(OUT)) + ')', 1),
        ('    stats_path = case_dir / "statistics.json"', '    stats_path = analysis / "AAA/statistics.json"', 1),
        ('    currents_path = case_dir / "currents_balance_symmetry.json"', '    currents_path = analysis / "AAA/currents_balance_symmetry.json"', 1),
        ('    inputs_path = ce / "input_equivalence_AAA.json"', '    inputs_path = analysis / "input_equivalence_AAA.json"', 1),
        ('        measurement_admission=descriptor(case_dir / "measurement_admission.json"),',
         '        measurement_admission=descriptor(case_dir / "measurement_admission.json"),\n'
         '        source_factor_measurement_admission=descriptor(analysis / "measurement_admission.json"),\n'
         '        complete_fine_observation_projection=descriptor(analysis / "observation/projection_receipt.json"),', 1),
        ('    write_new(case_dir / "reference_assessment.json", receipt)', '    write_new(analysis / "AAA/reference_assessment.json", receipt)', 1),
        ('        target = case_dir / "reference_qualification.json"', '        target = analysis / "AAA/reference_qualification.pending.json"', 1),
        ('        assessment=descriptor(case_dir / "reference_assessment.json")), indent=2))',
         '        assessment=descriptor(analysis / "AAA/reference_assessment.json")), indent=2))', 1)]
    equivalence["collector"] = patch(original_collector["path"], changes,
        runtime / "source_factor_reference_collector.py", ("main",))
    host = ADMISSION
    for token, value in (("__PROD__", str(PROD)), ("__OUT__", str(OUT)), ("__PREPARED_SHA__", prepared_sha)):
        if host.count(token) != 1:
            raise ValueError("reference admission template token ambiguous")
        host = host.replace(token, repr(value), 1)
    (runtime / "source_factor_reference_admission.py").write_text(host)
    shutil.copy2(PROD / "runtime/run_bounded_dragon.py", runtime / "run_bounded_dragon.py")
    write_new(SOURCE / "source_equivalence.json", dict(
        schema="AXMAT_SOURCEFACTOR_REFERENCE_SOURCE_EQUIVALENCE_V1", implementations=equivalence,
        exporter=pin(EXPORTER), exporter_source=pin(EXPORT_SOURCE), native_export_arithmetic_byte_exact=True,
        all_original_physical_checks_AST_exact=True, scientific_statistics_currents_and_projection_byte_exact=True,
        original_collector_scientific_conditions_restored_exactly=True, frozen_module_identity_reassigned=False))
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
    files.update({str(CE / "AAA" / name): sha for name, sha in native["outputs"].items()})
    files.update({str(path): digest(path) for path in [Path(__file__).resolve(), BUILD_FACTORY, FULL_FACTORY,
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
    verify(files)
    common = ["--case-spec", str(OUT / "observation_case_spec.json"), "--contract", str(CE / "AAA/reference_contract.json"),
        "--statepoints", str(CE / "AAA"), "--production-regions", str(OUT / "observation/observables.regions.csv"),
        "--production-summary", str(OUT / "observation/observables.summary.txt")]
    commands = [[str(EXPORTER), "track.xsm", "axial.xsm", "macro.xsm", "observables"],
        [str(PYTHON), str(OUT / "runtime/source_factor_physical_identity.py")],
        [str(PYTHON), str(Path(__file__).resolve()), "project-worker", "--sha256", "__DECLARATION_SHA256__"],
        [str(PYTHON), str(OUT / "runtime/reference_statistics.py"), "analyze", "--rules", str(OUT / "statistical_rules.json"),
         *common, "--output", str(OUT / "AAA/statistics.json")],
        [str(PYTHON), str(OUT / "runtime/compare_balance_symmetry.py"), "compare", "--rules", str(OUT / "balance_symmetry_rules.json"),
         "--statistics-rules", str(OUT / "statistical_rules.json"), *common,
         "--production-faces", str(OUT / "observation/observables.faces.csv"), "--output", str(OUT / "AAA/currents_balance_symmetry.json")],
        [str(PYTHON), str(OUT / "runtime/source_factor_reference_collector.py"), "__DECLARATION_SHA256__"]]
    d = dict(schema="AXMAT_SOURCEFACTOR_COMPLETE_ORIGINAL_GATE_REFERENCE_V1", declared_unix=time.time(), files=files,
        production_prepared=pin(PROD / "prepared.json"), AAA_status=pin(PROD / "AAA/run_status.json"),
        final_stage_seal=pin(final / "result.json"), build_admission=build,
        original_recipe_dependency=pin(OLD_SOURCE / "refined_reference_analysis_recipe.json"),
        old_recipe_is_dependency_only=True, actual_new_candidate_receipt_required=True,
        source_equivalence=pin(SOURCE / "source_equivalence.json"), analysis_environment=pin(SOURCE / "analysis_environment.json"),
        live_guard_provenance=pin(SOURCE / "live_guard_provenance.json"),
        exporter=pin(EXPORTER), exporter_source=pin(EXPORT_SOURCE), source_inputs={str(path): digest(path) for path in inputs.values()},
        staged_inputs={name: pin(path) for name, path in inputs.items()}, commands=commands, labels=list(LABELS),
        total_wall_seconds=TOTAL_WALL, native_export_stage_wall_seconds=60, rss_cap_mib=RSS_CAP,
        threads=1, retries=0, numeric_children_at_once=1, resource_roots=roots, resources_before=before,
        min_free_bytes=8 * 2**30, artifact_budget_bytes=96 * 2**30, archive_reserve_bytes=RESERVE,
        actual_external_terminal_return_contract=terminal_contract(),
        original_eight_gates=list(GATES), fixed_history=recipe["fixed_history"], transport_launched=False,
        AAA_accuracy_qualified=False, ABA_admitted=False,
        scope="Actual new source-factor AAA; complete saved fine fields and original physical bins, one global normalization, all original sample history and eight original scientific gates.")
    write_new(SOURCE / "declaration.json", d)
    write_new(SOURCE / "source_inventory.json", dict(files={str(path.relative_to(SOURCE)): digest(path)
        for path in SOURCE.rglob("*") if path.is_file()}))
    print(json.dumps(dict(classification="DECLARED_NEW_SOURCEFACTOR_REFERENCE_NOT_PREPARED_OR_RUN",
        declaration=pin(SOURCE / "declaration.json"), output=str(OUT))))


def admission(expected, prepared=False):
    d = read(require(SOURCE / "declaration.json", expected))
    if (d["schema"] != "AXMAT_SOURCEFACTOR_COMPLETE_ORIGINAL_GATE_REFERENCE_V1"
            or d["total_wall_seconds"] != TOTAL_WALL or d["rss_cap_mib"] != RSS_CAP
            or d["threads"] != 1 or d["retries"] != 0 or d["numeric_children_at_once"] != 1
            or d["min_free_bytes"] != 8 * 2**30 or d["artifact_budget_bytes"] != 96 * 2**30
            or d["archive_reserve_bytes"] != RESERVE or d["native_export_stage_wall_seconds"] != 60
            or d["labels"] != list(LABELS) or d["original_eight_gates"] != list(GATES)
            or d["actual_external_terminal_return_contract"] != terminal_contract()
            or str(TERMINAL) not in d["resource_roots"]):
        raise ValueError("frozen complete original-gate reference resource protocol differs")
    inventory = read(SOURCE / "source_inventory.json")
    if {str(path.relative_to(SOURCE)) for path in SOURCE.rglob("*") if path.is_file()} != set(inventory["files"]) | {"source_inventory.json"}:
        raise ValueError("reference source namespace changed")
    verify({str(SOURCE / name): sha for name, sha in inventory["files"].items()})
    verify(d["files"])
    environment(read(d["analysis_environment"]["path"]))
    actual = ready(d["production_prepared"]["sha256"], d["AAA_status"]["sha256"], d["build_admission"]["build_seal_sha256"])
    if actual[-1] != d["build_admission"]:
        raise ValueError("actual completed source-factor build admission changed")
    if prepared:
        p = read(OUT / "prepared.json")
        if p["declaration"] != pin(SOURCE / "declaration.json"):
            raise ValueError("actual reference preparation differs")
        require(OUT / "declaration.json", expected)
        verify({str(OUT / name): sha for name, sha in p["files"].items()})
        if p["source_links"] != d["staged_inputs"]:
            raise ValueError("prepared native export input descriptors differ")
        for name, item in p["source_links"].items():
            path = OUT / "fine" / name
            if not path.is_symlink() or path.resolve(strict=True) != Path(item["path"]):
                raise ValueError("actual native export input link does not point to its bound new final state")
            require(item["path"], item["sha256"])
    return d, actual


def prepare(expected):
    d, actual = admission(expected)
    if OUT.exists():
        raise ValueError("new reference prepared root must be absent; no retry")
    c = actual[0]
    resources = c.DiskResources(ART, d["resource_roots"], d["min_free_bytes"], d["artifact_budget_bytes"])
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
    write_new(OUT / "prepared.json", dict(classification="PREPARED_SOURCEFACTOR_REFERENCE_NO_ANALYSIS",
        declaration=pin(SOURCE / "declaration.json"), files={str(path.relative_to(OUT)): digest(path)
            for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()},
        source_links=d["staged_inputs"], transport_launched=False, analysis_started=False,
        AAA_accuracy_qualified=False, ABA_admitted=False, resources_before=before))
    resources.check()
    print(json.dumps(dict(classification="PREPARED_SOURCEFACTOR_REFERENCE_NO_ANALYSIS", prepared=pin(OUT / "prepared.json"))))


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
    d, actual = admission(expected, prepared=True)
    c, info, status, final, recipe = actual[:5]
    rs = module(OUT / "runtime/reference_statistics.py", "reference_statistics")
    cb = module(OUT / "runtime/compare_balance_symmetry.py", "source_factor_current_checker")
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
    projection = module(OUT / "runtime/project_refined_observables.py", "source_factor_projection").project(
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
    result.update(classification="SOURCEFACTOR_REFERENCE_PUBLICATION_FAILED", error=repr(error),
                  AAA_accuracy_qualified=False, ABA_admitted=False)


def run(expected):
    d, actual = admission(expected, prepared=True)
    c = actual[0]
    if (OUT / "AAA/analysis_claim.json").exists():
        raise ValueError("one analysis attempt only; no retry")
    resources = c.DiskResources(ART, d["resource_roots"], d["min_free_bytes"], d["artifact_budget_bytes"])
    before = resources.check()
    if before["artifact_bytes"] + RESERVE >= d["artifact_budget_bytes"] or before["disk_free_bytes"] - RESERVE < d["min_free_bytes"]:
        raise ValueError("actual remaining complete-history reference reservation no longer fits")
    write_new(OUT / "AAA/analysis_claim.json", dict(declaration_sha256=expected, started_unix=time.time(),
        prepared=d["production_prepared"], AAA_status=d["AAA_status"], own_child_only=True, retries=0))
    full = module(require(FULL_FACTORY, FULL_SOURCE_SHA), "source_factor_reference_guard")
    if live_guard_provenance(full, c, actual[1]) != read(d["live_guard_provenance"]["path"]):
        raise ValueError("actual own-child supervisor provenance changed")
    runner = full.OwnRSSSerialExecutor(OUT, TOTAL_WALL, "AAA", resources)
    started = time.monotonic()
    result = dict(classification="SOURCEFACTOR_REFERENCE_FAILED_NO_RETRY", completed_commands=0, error=None,
        transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False, ABA_started=False,
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
        result.update(classification="COMPLETE_SOURCEFACTOR_ORIGINAL_GATE_REFERENCE_REASSESSMENT",
            AAA_classification=assessment["classification"], original_eight_checks=assessment["checks"],
            AAA_accuracy_qualified=assessment["classification"] == "AAA_REFERENCE_QUALIFIED",
            ABA_admitted=assessment["ABA_admitted"], reference_assessment=pin(OUT / "AAA/reference_assessment.json"),
            watchdogs=monitors, maximum_sampled_rss_mib=max(read(item["path"])["sampled_peak_rss_mib"] for item in monitors))
    except BaseException as error:
        failed = error
        result["error"] = repr(error)
    finally:
        try:
            admission(expected, prepared=True)
            resources.check()
            elapsed = time.monotonic() - started
            total_bytes = sum(path.stat().st_size for path in OUT.rglob("*") if path.is_file() and not path.is_symlink())
            if elapsed >= TOTAL_WALL or total_bytes >= RESERVE:
                raise ValueError("actual complete analysis exceeds original total wall or declared archive reserve")
            if (PROD / "ABA").exists():
                raise ValueError("reference reassessment must not execute or create ABA")
            result.update(elapsed_seconds=elapsed, actual_archive_bytes_before_closeout=total_bytes)
        except BaseException as error:
            failed = error
            result.update(classification="SOURCEFACTOR_REFERENCE_INPUT_OR_RESOURCE_FAILED", error=repr(error),
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
            write_new(OUT / "seal.json", dict(schema="AXMAT_SOURCEFACTOR_REFERENCE_SEAL_V1",
                files={str(path.relative_to(OUT)): digest(path) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()}))
            # These last checks include formal publication, output hashing,
            # analysis_result and seal writing. Keep the already sealed files
            # immutable; successful terminal measurements go to the return/
            # stdout record. A failure appends a new artifact and withdraws
            # the formal receipt, invalidating the prior success namespace.
            terminal_resources = resources.check()
            terminal_bytes = sum(path.stat().st_size for path in OUT.rglob("*")
                if path.is_file() and not path.is_symlink())
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
    command = [str(PYTHON), str(factory), "run", "--sha256", declared_sha]
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
    archive_bytes = tail["actual_complete_archive_bytes"]
    snapshot = tail["resources_after_full_closeout"]
    actual_bytes = sum(path.stat().st_size for path in OUT.rglob("*") if path.is_file() and not path.is_symlink())
    if (tail["full_closeout_tail_gate"] != "PASS" or type(elapsed) not in (int, float)
            or not math.isfinite(elapsed) or not sealed_result["elapsed_seconds"] <= elapsed < TOTAL_WALL
            or type(archive_bytes) is not int or not 0 <= archive_bytes < RESERVE or archive_bytes != actual_bytes
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["artifact_budget_bytes"] != 96 * 2**30 or d["artifact_budget_bytes"] != 96 * 2**30
            or snapshot["min_free_bytes"] != 8 * 2**30 or d["min_free_bytes"] != 8 * 2**30
            or snapshot["resource_roots"] != d["resource_roots"]
            or type(snapshot["artifact_bytes"]) is not int
            or not archive_bytes <= snapshot["artifact_bytes"] <= d["artifact_budget_bytes"]
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < d["min_free_bytes"]
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float)
            or not math.isfinite(snapshot["checked_unix"]) or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete closeout tail wall/archive/resource evidence failed")
    return dict(receipt=pin(receipt), full_stdout=pin(stdout), command=command,
                schema=TERMINAL_SCHEMA, **tail)


def qualification_admission(expected_seal, expected_qualification, terminal_evidence, terminal_evidence_sha256):
    """Only complete seal, formal receipt and actual terminal return admit ABA."""
    seal = read(require(OUT / "seal.json", expected_seal))
    if seal["schema"] != "AXMAT_SOURCEFACTOR_REFERENCE_SEAL_V1":
        raise ValueError("actual completed new reference seal required")
    actual = {str(path.relative_to(OUT)) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()}
    if actual != set(seal["files"]) | {"seal.json"}:
        raise ValueError("complete reference terminal seal namespace changed")
    verify({str(OUT / name): sha for name, sha in seal["files"].items()})
    result = read(OUT / "AAA/analysis_result.json")
    if (result["classification"] != "COMPLETE_SOURCEFACTOR_ORIGINAL_GATE_REFERENCE_REASSESSMENT"
            or result["completed_commands"] != len(LABELS) or result["error"] is not None
            or result["AAA_accuracy_qualified"] is not True or result["ABA_admitted"] is not True
            or result["ABA_started"] is not False or result["transport_launched"] is not False
            or result["mandatory_full_closeout_tail_gate"] is not True
            or not 0 <= result["elapsed_seconds"] < TOTAL_WALL
            or result["actual_archive_bytes_before_closeout"] >= RESERVE
            or set(result["original_eight_checks"]) != set(GATES)
            or any(value != "PASS" for value in result["original_eight_checks"].values())):
        raise ValueError("actual complete bounded eight-gate qualification is not present")
    d, ready_state = admission(read(OUT / "prepared.json")["declaration"]["sha256"], prepared=True)
    formal = require(OUT / "AAA/reference_qualification.json", expected_qualification)
    if result["reference_qualification"] != pin(formal):
        raise ValueError("only the successful formally published qualification is eligible")
    stages = read(OUT / "AAA/stages.json")["stages"]
    if len(stages) != len(LABELS) or [stage["label"] for stage in stages] != list(LABELS) or any(stage["status"] != "PASS" for stage in stages):
        raise ValueError("all actual reassessment stages must pass")
    declared_sha = read(OUT / "prepared.json")["declaration"]["sha256"]
    commands = [[declared_sha if value == "__DECLARATION_SHA256__" else value for value in command]
                for command in d["commands"]]
    for stage, command in zip(stages, commands, strict=True):
        if stage["command"] != command:
            raise ValueError("actual completed reference command differs from its declaration")
        watch(stage)
    terminal = external_terminal_admission(d, declared_sha, expected_seal, result,
                                          terminal_evidence, terminal_evidence_sha256)
    ready_state[0].qualify_aba(ready_state[1], PROD, d["production_prepared"]["sha256"], formal, expected_qualification)
    return dict(schema="AXMAT_SOURCEFACTOR_SEALED_REFERENCE_QUALIFICATION_ADMISSION_V1",
        reference_root=str(OUT), reference_seal_sha256=expected_seal, qualification=pin(formal),
        production_prepared=d["production_prepared"], AAA_status=d["AAA_status"],
        actual_external_terminal_evidence=terminal["receipt"], actual_external_terminal_validation=terminal,
        all_original_eight_checks=result["original_eight_checks"], original_qualify_aba_guard_passed=True,
        pending_receipt_eligible=False, ABA_started=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("declare", "prepare", "run", "project-worker", "admit-qualification"))
    parser.add_argument("--sha256")
    parser.add_argument("--prepared-sha256")
    parser.add_argument("--status-sha256")
    parser.add_argument("--build-seal-sha256")
    parser.add_argument("--qualification-sha256")
    parser.add_argument("--terminal-evidence", type=Path)
    parser.add_argument("--terminal-evidence-sha256")
    args = parser.parse_args()
    if args.action == "declare":
        if not all((args.prepared_sha256, args.status_sha256, args.build_seal_sha256)):
            parser.error("declare requires actual prepared, AAA status and completed build-seal SHA256 values")
        declare(args.prepared_sha256, args.status_sha256, args.build_seal_sha256)
    elif not args.sha256:
        parser.error("the frozen declaration --sha256 is required")
    elif args.action == "admit-qualification":
        if not all((args.qualification_sha256, args.terminal_evidence, args.terminal_evidence_sha256)):
            parser.error("actual formal --qualification-sha256, reference seal --sha256 and both terminal-evidence inputs required")
        print(json.dumps(qualification_admission(args.sha256, args.qualification_sha256,
                                                args.terminal_evidence, args.terminal_evidence_sha256)))
    else:
        {"prepare": prepare, "run": run, "project-worker": project_worker}[args.action](args.sha256)
