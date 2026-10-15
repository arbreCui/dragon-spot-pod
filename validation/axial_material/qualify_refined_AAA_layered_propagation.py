"""Separately bounded mathematical controls and finite-height comparisons.

Preparation requires the completed, sealed current-data full native family.
Successful execution qualifies only program checks and the comparison archive;
it does not choose a propagation law, converge a continuous BVP, or admit ABA.
"""

import argparse
import os
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation/axial_material"))

import qualify_refined_AAA_layered_full as full
from probe_refined_AAA_white_odd_response import (
    ART, DiskResources, digest, read, require_file, verify, write_new,
)

OUT = ART / "axial-material-AAA-white-trace-refined-layered-propagation-20261005"
FULL = full.OUT
ANGULAR = ART / "axial-material-AAA-white-trace-refined-native-angular-response-20261005"
FULL_DECLARATION_SHA = "f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b"
ANGULAR_SEAL_SHA = "8862154f1fb3458676460f8a4074a1a52070322332dd08e66c2773b0e4345540"
COMPARE = ROOT / "validation/axial_material/compare_refined_AAA_layered_propagation.py"
CONTROLS = ROOT / "validation/axial_material/verify_angular_collision_slab_candidate.py"
AUDITOR = ROOT / "validation/axial_material/audit_refined_AAA_layered_propagation.py"
GROUPS = [51, 61, 98]
MODELS = ["trace", "reduced"]
LEVELS = [1, 2, 4, 8, 16, 32]
EXPECTED_LABELS = (["runs/mathematical_controls"]
    + [f"runs/reference_g{g}" for g in GROUPS]
    + [f"runs/model_g{g}_{model}" for g in GROUPS for model in MODELS]
    + ["verification"])


def _sealed(root, expected):
    if not isinstance(expected, str) or re.fullmatch(r"[a-f0-9]{64}", expected) is None:
        raise ValueError("explicit immutable SHA256 identity required")
    require_file(root / "seal.json", expected)
    manifest = read(root / "seal.json")["files"]
    observed = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"seal.json"}
    if observed != set(manifest):
        raise ValueError("complete sealed namespace changed: " + str(root))
    verify({str(root / name): sha for name, sha in manifest.items()})
    verify(read(root / "declaration.json")["files"])


def verify_full(expected_seal):
    """Reject an early result file without actual parent completion."""
    require_file(FULL / "declaration.json", FULL_DECLARATION_SHA)
    _sealed(FULL, expected_seal)
    result = read(FULL / "result.json")
    driver = read(FULL / "driver_result.json")
    stages = read(FULL / "AAA/stages.json")["stages"]
    if (driver["classification"] != "COMPLETE_BOUNDED_CURRENT_FULL_FIXED_SOURCE_WHITE_ONLY"
            or driver["error"] is not None
            or result["classification"] != "COMPLETE_CURRENT_DATA_H20_N4_FULL_FIXED_SOURCE_WHITE_ONLY"
            or len(stages) != 368 or any(s["status"] != "PASS" for s in stages)
            or result["groups"] != GROUPS or result["original_tracks"] != 11364
            or result["primary_batches"] != 180 or result["exact_replay_batches"] != 180
            or result["physical_states_per_phase"] != 1090944
            or result["coordinate_evaluations_per_phase"] != 72002304
            or not result["complete_coverage"] or not result["complete_scientific_replay"]
            or not result["full_current_discrete_fixed_source_qualified"]
            or not result["full_current_geometric_white_qualified"]):
        raise ValueError("complete actual native execution and qualification required")
    for stage in stages:
        watch = read((FULL / (stage["label"] + ".log")).with_suffix(".watchdog.json"))
        _watchdog(watch)
    for name in ("AAA_accuracy_qualified", "scattering_fission_iteration_qualified",
                 "local_inverse_propagation_qualified", "ABA_admitted"):
        if result[name] is not False:
            raise ValueError("native fixed-source scope must remain distinct")


def _watchdog(watch):
    import math
    rss, elapsed = watch["sampled_peak_rss_mib"], watch["elapsed_seconds"]
    if (watch["returncode"] != 0 or watch["limit_failure"] is not None
            or not math.isfinite(rss) or not 0 <= rss < 512
            or not math.isfinite(elapsed) or not 0 <= elapsed < 600
            or watch["own_child_only"] is not True or watch["liveness_group_cleanup"] is not True
            or watch["rss_cap_mib"] != 512):
        raise ValueError("successful bounded own-child watchdog required")


def _environment():
    import numpy as np
    import scipy
    actual = dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__)
    expected = read(FULL / "declaration.json")["numeric_environment"]
    if actual != expected:
        raise ValueError("unchanged existing numerical environment required")
    return actual


def _native_libraries(np, scipy):
    """Pin this conda host's actual BLAS/LAPACK dependency chain and aliases."""
    prefix = Path(sys.executable).resolve().parents[1]
    names = ("libblas.3.dylib", "liblapack.3.dylib", "libopenblas.0.dylib",
        "libgfortran.5.dylib", "libquadmath.0.dylib", "libgcc_s.1.1.dylib", "libomp.dylib")
    aliases = {str(prefix / "lib" / name): str((prefix / "lib" / name).resolve()) for name in names}
    paths = [require_file(Path(p)) for p in sorted(set(aliases.values()))]
    paths.append(require_file(Path("/usr/bin/otool")))
    modules = list(Path(np.__file__).parent.rglob("*_umath_linalg*.so"))
    modules += list(Path(scipy.__file__).parent.rglob("*_superlu*.so"))
    if len(modules) != 2:
        raise ValueError("actual NumPy dense and SciPy sparse solver modules required")
    linkage = {}
    for path in [*modules, *paths[:-1]]:
        response = subprocess.run(["/usr/bin/otool", "-L", str(path)],
            capture_output=True, text=True, timeout=30, check=True)
        linkage[str(path.resolve())] = response.stdout
        for line in response.stdout.splitlines()[1:]:
            dependency = line.strip().split(" (", 1)[0]
            if dependency.startswith("@rpath/"):
                expected = prefix / "lib" / dependency.removeprefix("@rpath/")
                if str(expected) not in aliases:
                    raise ValueError("unrecorded non-system numerical dependency: " + dependency)
            elif not dependency.startswith(("/usr/lib/", "/System/Library/")):
                raise ValueError("unsupported numerical loader dependency: " + dependency)
    return paths, aliases, linkage


def prepare(expected_full_seal):
    import numpy as np
    import scipy
    import decimal
    import _decimal
    import angular_collision_slab_candidate
    import angular_collision_slab_expanded_reference
    import verify_angular_collision_slab_candidate
    import compare_refined_AAA_layered_propagation
    verify_full(expected_full_seal)
    _sealed(ANGULAR, ANGULAR_SEAL_SHA)
    environment = _environment()
    native_paths, native_aliases, native_linkage = _native_libraries(np, scipy)
    if read(ANGULAR / "result.json")["classification"] != "COMPLETE_CURRENT_DATA_FULL_ANGULAR_COLLISION_RESPONSE_ONLY":
        raise ValueError("complete current-data angular response required")
    require_file(AUDITOR)
    # A conservative uncompressed bound: three dense candidate matrices plus
    # the directional sweep matrices, complete dual fields/systems, headers,
    # controls/references and reporting reserve.  Never assume compression.
    dimensions = [32 * m for m in LEVELS]
    dense_bound = 6 * sum(32 * n * n for n in dimensions)
    dual_fields_bound = 6 * sum(64 * n * 38 * 8 + 512 * n for n in dimensions)
    overhead_bound = 36 * 2**20 + 128 * 2**20 + 512 * 2**20
    uncompressed_bound = dense_bound + dual_fields_bound + overhead_bound
    if uncompressed_bound >= 2 * 2**30:
        raise ValueError("declared complete uncompressed family bound exceeded")
    OUT.mkdir(exist_ok=False)
    for name in ("runtime", "AAA", "runs", "references", "models"):
        (OUT / name).mkdir()
    shutil.copy2(FULL / "runtime/run_bounded_dragon.py", OUT / "runtime/run_bounded_dragon.py")
    paths = [Path(__file__).resolve(), COMPARE, CONTROLS, AUDITOR,
        ROOT / "validation/axial_material/angular_collision_slab_candidate.py",
        ROOT / "validation/axial_material/angular_collision_slab_expanded_reference.py",
        Path(sys.executable).resolve(), Path("/bin/ps"), FULL / "seal.json", ANGULAR / "seal.json",
        OUT / "runtime/run_bounded_dragon.py", Path(decimal.__file__).resolve(),
        Path(_decimal.__file__).resolve(), *native_paths]
    files = dict(read(FULL / "declaration.json")["files"])
    files.update(read(ANGULAR / "declaration.json")["files"])
    paths += [Path(m.__file__).resolve() for m in (
        full, angular_collision_slab_candidate, angular_collision_slab_expanded_reference,
        verify_angular_collision_slab_candidate, compare_refined_AAA_layered_propagation)]
    # Both dependency packages and their actual shared objects are pinned,
    # along with already sealed native input namespaces through their seals.
    for package in (np, scipy):
        package_root = Path(package.__file__).parent
        paths += [p for p in package_root.rglob("*")
            if p.is_file() and p.suffix in (".py", ".so", ".dylib")]
        libs = package_root.parent / (package_root.name + ".libs")
        if libs.is_dir():
            paths += [p for p in libs.rglob("*") if p.is_file()]
    files.update({str(p.resolve()): digest(require_file(p.resolve())) for p in paths})
    verify(files)
    roots = sorted(set(read(FULL / "declaration.json")["resource_roots"])
        | {str(p.resolve()) for p in ART.glob("axial-material-*") if p.is_dir()} | {str(OUT)})
    resource = DiskResources(ART, roots, 8 * 2**30, 96 * 2**30)
    before = resource.check()
    admitted = (before["artifact_bytes"] + uncompressed_bound < 96 * 2**30
        and before["disk_free_bytes"] - uncompressed_bound >= 8 * 2**30)
    if not admitted:
        raise ValueError("complete conservative family storage admission failed; no numerical child")
    write_new(OUT / "declaration.json", dict(schema="AXMAT_CURRENT_LAYERED_COMPARISON_DECLARATION_V1",
        files=files, full_root=str(FULL), full_seal_sha256=expected_full_seal,
        full_declaration_sha256=FULL_DECLARATION_SHA, angular_root=str(ANGULAR),
        angular_seal_sha256=ANGULAR_SEAL_SHA, groups=GROUPS, models=MODELS, levels=LEVELS,
        expected_stage_labels=EXPECTED_LABELS, total_wall_seconds=7200, stage_wall_seconds=600,
        rss_cap_mib=512, rss_poll_seconds=.2, numeric_children_at_once=1, threads=1, retries=0,
        requires_host_process_metadata_access=True,
        resource_roots=roots, artifact_budget_bytes=96 * 2**30, min_free_bytes=8 * 2**30,
        resources_before=before, complete_uncompressed_bound_bytes=uncompressed_bound,
        complete_storage_admitted=admitted, numeric_environment=environment,
        native_library_aliases=native_aliases, native_library_linkage=native_linkage,
        numerical_loader_environment={k: v for k, v in os.environ.items()
            if k.startswith("DYLD_") or k in ("OPENBLAS_CORETYPE", "OPENBLAS_NUM_THREADS",
                "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")},
        expected_math_case_pairs=20, expected_math_solves=40, expected_negative_controls=11,
        expected_model_case_pairs=36, expected_model_solves=72,
        expected_total_case_pairs=56, expected_total_linear_solves=112,
        expected_total_source_column_solves=3800, reference_source_columns=38,
        field_action_relative_limit=5e-12, cell_global_algebraic_relative_limit=1e-10,
        native_reference='Completed current three-group H20/Nz4 full exact-exponential discrete source response. '
            'Geometric white incoming measure; angular means retain stored native volume.',
        hypotheses='Htrace=(tau I+bNa^2 K)/G and Hreduced=prior projected zero-gradient inverse, '
            'with explicit identical mu/omega/source/height/vacuum. No unique propagation inference.',
        independent_program='Decimal80 expanded mean/shared-face equations of the same constant-subcell '
            'coupling discretization; mathematical controls include independent Decimal1024 diagonal/void fields.',
        reports_only='All six refinement changes and all model discrepancies. No convergence, '
            'physical accuracy, model-selection or CE-derived passing criterion.',
        original_accuracy_thresholds_changed=False, production_solver_changed=False, CE_data_used=False,
        continuous_BVP_qualified=False, native_propagation_qualified=False,
        physical_collision_balance_assessed=False, scattering_fission_iteration_qualified=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    print(json.dumps(dict(declaration_sha256=digest(OUT / "declaration.json"),
        native_seal_sha256=expected_full_seal, uncompressed_bound_bytes=uncompressed_bound)))


def _verify_inputs(declaration):
    verify(declaration["files"])
    verify_full(declaration["full_seal_sha256"])
    _sealed(ANGULAR, declaration["angular_seal_sha256"])
    _environment()
    for name, expected in declaration["native_library_aliases"].items():
        if str(Path(name).resolve()) != expected:
            raise ValueError("numerical library alias changed")
    # Serial children explicitly use one thread.  Loader overrides and CPU
    # dispatch selection remain bound to the same preparing environment.
    for name, value in declaration["numerical_loader_environment"].items():
        if (name.startswith("DYLD_") or name == "OPENBLAS_CORETYPE") and os.environ.get(name) != value:
            raise ValueError("numerical loader environment changed")
    extra_loader = {k for k in os.environ if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}
    if extra_loader != {k for k in declaration["numerical_loader_environment"]
                        if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}:
        raise ValueError("new numerical loader override appeared")


def _receipt(name, folder):
    """Bind downstream stages to the actual completed output namespace."""
    files = {str(p.relative_to(folder)): digest(p) for p in folder.rglob("*") if p.is_file()}
    path = OUT / "runs" / (name + ".receipt.json")
    write_new(path, dict(root=str(folder), files=files))
    return path, digest(path)


def _check_receipt(path, expected):
    if not isinstance(expected, str) or re.fullmatch(r"[a-f0-9]{64}", expected) is None:
        raise ValueError("explicit completed-stage receipt SHA256 required")
    receipt = read(require_file(path, expected))
    folder = Path(receipt["root"])
    observed = {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file()}
    if observed != set(receipt["files"]):
        raise ValueError("actual completed stage namespace changed")
    verify({str(folder / name): sha for name, sha in receipt["files"].items()})


def _worker_declaration(label):
    claim = read(OUT / "run_claim.json")
    declaration = read(require_file(OUT / "declaration.json", claim["declaration_sha256"]))
    stages = read(OUT / "AAA/stages.json")["stages"]
    if (os.getppid() != claim["parent_pid"] or not stages
            or stages[-1]["label"] != label or stages[-1]["status"] != "RUNNING"
            or stages[-1]["command"] != [sys.executable, *sys.argv]):
        raise ValueError("actual parent-admitted serial stage required")
    return declaration


def mathematical_controls():
    import verify_angular_collision_slab_candidate as controls
    declaration = _worker_declaration("runs/mathematical_controls")
    _verify_inputs(declaration)
    controls.verify_controls(OUT / "math_controls")
    print("ANGULAR-COLLISION-SLAB-MATHEMATICAL-CONTROLS-PASSED")


def reference(group):
    import compare_refined_AAA_layered_propagation as compare
    declaration = _worker_declaration(f"runs/reference_g{group}")
    _verify_inputs(declaration)
    compare.prepare_reference(FULL, ANGULAR, group, OUT / "references" / f"g{group}",
        native_seal_sha256=declaration["full_seal_sha256"], angular_seal_sha256=ANGULAR_SEAL_SHA)
    print("AXMAT-LAYERED-REFERENCE-RETAINED")


def model(group, hypothesis, receipt_sha):
    import compare_refined_AAA_layered_propagation as compare
    declaration = _worker_declaration(f"runs/model_g{group}_{hypothesis}")
    _verify_inputs(declaration)
    _check_receipt(OUT / "runs" / f"reference_g{group}.receipt.json", receipt_sha)
    compare.compare_model(OUT / "references" / f"g{group}", hypothesis,
        OUT / "models" / f"g{group}_{hypothesis}")
    print("AXMAT-LAYERED-CANDIDATE-COMPARED")


def run(expected):
    if not isinstance(expected, str) or re.fullmatch(r"[a-f0-9]{64}", expected) is None:
        raise ValueError("explicit frozen declaration SHA256 required")
    declaration = read(require_file(OUT / "declaration.json", expected))
    _verify_inputs(declaration)
    if declaration["expected_stage_labels"] != EXPECTED_LABELS or not declaration["complete_storage_admitted"]:
        raise ValueError("complete fixed stage plan and conservative storage admission required")
    resource = DiskResources(ART, declaration["resource_roots"], declaration["min_free_bytes"],
        declaration["artifact_budget_bytes"])
    started = time.monotonic()
    write_new(OUT / "run_claim.json", dict(declaration_sha256=expected, started_unix=time.time(),
        started_monotonic=started, parent_pid=os.getpid()))
    runner = full.OwnRSSSerialExecutor(OUT, 7200, "AAA", resource)
    result = dict(classification="FAILED_CURRENT_LAYERED_COMPARISON_NO_RETRY", error=None)
    receipts = {}
    def execute(label, command, marker=None):
        _verify_inputs(declaration)
        runner.execute(OUT / "runs", label, command, 600, marker)
        _verify_inputs(declaration)
    try:
        execute("mathematical_controls", [sys.executable, str(Path(__file__).resolve()), "math"],
            "ANGULAR-COLLISION-SLAB-MATHEMATICAL-CONTROLS-PASSED")
        math_result = read(OUT / "math_controls/result.json")
        if (not math_result["all_controls_passed"] or math_result["actual_numerical_solves"] != 40
                or math_result["actual_case_pairs"] != 20 or math_result["negative_controls"] != 11):
            raise ValueError("all actual mathematical controls required before comparisons")
        receipts["mathematical_controls"] = _receipt("mathematical_controls", OUT / "math_controls")
        for g in GROUPS:
            execute(f"reference_g{g}", [sys.executable, str(Path(__file__).resolve()), "reference",
                "--group", str(g)], "AXMAT-LAYERED-REFERENCE-RETAINED")
            receipts[f"reference_g{g}"] = _receipt(f"reference_g{g}", OUT / "references" / f"g{g}")
        for g in GROUPS:
            for hypothesis in MODELS:
                _check_receipt(*receipts["mathematical_controls"])
                execute(f"model_g{g}_{hypothesis}", [sys.executable, str(Path(__file__).resolve()), "model",
                    "--group", str(g), "--model", hypothesis,
                    "--receipt-sha256", receipts[f"reference_g{g}"][1]], "AXMAT-LAYERED-CANDIDATE-COMPARED")
                receipts[f"model_g{g}_{hypothesis}"] = _receipt(f"model_g{g}_{hypothesis}",
                    OUT / "models" / f"g{g}_{hypothesis}")
        write_new(OUT / "stage_receipts.json", {name: dict(path=str(path), sha256=sha)
            for name, (path, sha) in receipts.items()})
        _verify_inputs(declaration)
        runner.execute(OUT, "verification", [sys.executable, str(AUDITOR), str(OUT)], 600,
            "AXMAT-LAYERED-COMPARISON-ARCHIVE-VERIFIED")
        stages = read(OUT / "AAA/stages.json")["stages"]
        if [s["label"] for s in stages] != EXPECTED_LABELS or any(s["status"] != "PASS" for s in stages):
            raise ValueError("all eleven actual parent-observed stages required")
        _watchdog(read(OUT / "verification.watchdog.json"))
        scientific = read(OUT / "result.json")
        if (scientific["classification"] != "COMPLETE_CURRENT_FINITE_HEIGHT_COMPARISON_ONLY"
                or scientific["actual_total_linear_solves"] != 112
                or scientific["actual_total_source_column_solves"] != 3800
                or scientific["AAA_accuracy_qualified"] is not False or scientific["ABA_admitted"] is not False):
            raise ValueError("complete comparison-only scientific closeout required")
        for name in ("continuous_BVP_qualified", "native_propagation_qualified",
                     "physical_collision_balance_assessed", "scattering_fission_iteration_qualified"):
            if scientific[name] is not False:
                raise ValueError("comparison-only scope required before parent seal")
        result.update(classification="COMPLETE_BOUNDED_CURRENT_LAYERED_COMPARISON_ONLY", ABA_admitted=False)
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        _verify_inputs(declaration)
        result.update(elapsed_seconds=time.monotonic() - started, resources=resource.check())
        if result["elapsed_seconds"] >= declaration["total_wall_seconds"]:
            result.update(classification="FAILED_CURRENT_LAYERED_COMPARISON_NO_RETRY",
                error="complete family wall budget exceeded")
        write_new(OUT / "driver_result.json", result)
    if result["classification"] != "COMPLETE_BOUNDED_CURRENT_LAYERED_COMPARISON_ONLY":
        raise ValueError("complete bounded comparison execution required before seal")
    write_new(OUT / "seal.json", dict(schema="AXMAT_CURRENT_LAYERED_COMPARISON_SEAL_V1",
        files={str(p.relative_to(OUT)): digest(p) for p in OUT.rglob("*") if p.is_file()}))
    print(json.dumps(dict(classification=result["classification"], elapsed_seconds=result["elapsed_seconds"])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "run", "math", "reference", "model"])
    parser.add_argument("--full-seal-sha256")
    parser.add_argument("--sha256")
    parser.add_argument("--group", type=int, choices=GROUPS)
    parser.add_argument("--model", choices=MODELS)
    parser.add_argument("--receipt-sha256")
    args = parser.parse_args()
    if args.action == "prepare":
        prepare(args.full_seal_sha256)
    elif args.action == "run":
        run(args.sha256)
    elif args.action == "reference":
        reference(args.group)
    elif args.action == "math":
        mathematical_controls()
    else:
        model(args.group, args.model, args.receipt_sha256)
