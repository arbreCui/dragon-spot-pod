"""Run the unchanged AAA evidence analyses serially, once, after CE completes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
CE = ART / "axial-material-ce-qualified-AB-compensated-20261004"
CASE = CE / "AAA"
TOOLS = ROOT / "validation/axial_material"
OBS = ART / "axial-material-qualified-AAA-observables-20261004"
SPEC = ART / "axial-material-qualified-AB-compensated-admission-20261004/case_spec.json"
REFERENCE_PYTHON = Path("/Users/wen/miniforge3/envs/openmc-dev/bin/python")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_new(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    if any((CASE / name).exists() for name in ("analysis_claim.json", "analysis_result.json", "statistics.json", "currents_balance_symmetry.json", "reference_assessment.json")):
        raise ValueError("existing analysis evidence: no overwrite or retry")
    native = json.loads((CASE / "native_result.json").read_text())
    if native["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS" or native["returncode"] != 0:
        raise ValueError("complete bounded native reference required before analysis")
    declaration = json.loads((CE / "analysis_collection_declaration.json").read_text())
    for filename, expected in declaration["files"].items():
        if digest(Path(filename)) != expected:
            raise ValueError("frozen statistical/collection implementation changed: " + filename)
    common = ["--case-spec", str(SPEC), "--contract", str(CASE / "reference_contract.json"),
        "--statepoints", str(CASE), "--production-regions", str(OBS / "observables.regions.csv"),
        "--production-summary", str(OBS / "observables.summary.txt")]
    commands = [
        [str(REFERENCE_PYTHON), str(TOOLS / "reference_statistics.py"), "analyze", "--rules", str(CE / "statistical_rules.json"),
            *common, "--output", str(CASE / "statistics.json")],
        [str(REFERENCE_PYTHON), str(TOOLS / "compare_balance_symmetry.py"), "compare", "--rules", str(CE / "balance_symmetry_rules.json"),
            "--statistics-rules", str(CE / "statistical_rules.json"), *common,
            "--production-faces", str(OBS / "observables.faces.csv"), "--output", str(CASE / "currents_balance_symmetry.json")],
        [sys.executable, str(TOOLS / "assess_qualified_AAA_reference_compensated.py")],
    ]
    paths = [SPEC, CASE / "native_result.json", CASE / "reference_contract.json", CASE / "measurement_admission.json",
        CE / "analysis_collection_declaration.json", *[Path(name) for name in declaration["files"]],
        *[OBS / f"observables.{name}" for name in ("regions.csv", "faces.csv", "summary.txt")],
        REFERENCE_PYTHON.resolve(), Path(sys.executable).resolve(), Path(__file__).resolve()]
    execution = dict(schema="AXMAT_SERIAL_ORIGINAL_AAA_REFERENCE_ANALYSIS_V1", threads=1, retries=0,
        total_wall_seconds=120, transport_launched=False, commands=commands,
        files={str(path): digest(path) for path in paths},
        scope="Read-only source, statistics, accuracy and signed-current/accounting/symmetry analyses at unchanged original rules, followed by strict AAA qualification collection.")
    write_new(CASE / "analysis_execution.json", execution)
    write_new(CASE / "analysis_claim.json", dict(execution_sha256=digest(CASE / "analysis_execution.json"), started_unix=time.time()))
    result = dict(classification="ANALYSIS_FAILED_NO_RETRY", completed_commands=0, error=None, transport_launched=False)
    started = time.monotonic()
    environment = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    try:
        for index, command in enumerate(commands, 1):
            remaining = 120 - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError("declared total analysis wall limit exceeded")
            with (CASE / f"analysis_{index:02d}.log").open("xb") as log:
                subprocess.run(command, cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=remaining)
            result["completed_commands"] = index
        assessment = json.loads((CASE / "reference_assessment.json").read_text())
        result.update(classification="COMPLETE_REFERENCE_ANALYSIS", AAA_classification=assessment["classification"],
            ABA_admitted=assessment["ABA_admitted"], reference_assessment_sha256=digest(CASE / "reference_assessment.json"))
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        for filename, expected in execution["files"].items():
            if digest(Path(filename)) != expected:
                result.update(classification="ANALYSIS_INPUT_CHANGED", error="frozen input changed: " + filename)
        result["elapsed_seconds"] = time.monotonic() - started
        result["outputs"] = {path.name: digest(path) for path in CASE.iterdir()
            if path.is_file() and (path.name.startswith("analysis_") and path.suffix == ".log"
                or path.name in ("statistics.json", "currents_balance_symmetry.json", "reference_assessment.json", "reference_qualification.json"))}
        write_new(CASE / "analysis_result.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
