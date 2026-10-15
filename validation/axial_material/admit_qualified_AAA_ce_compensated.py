"""Bind saved AAA numerical and physical checks to the frozen CE run.

This is permission to measure accuracy, never an accuracy qualification.
No transport is launched and no prior sealed artifact is modified.
"""
import json
from pathlib import Path
import sys

# Verify with the actual frozen candidate runtime, including its declared
# arithmetic variant and resource addendum, rather than the legacy receiver.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation/artifacts/axial-material-production-qualified-AB-compensated-20261004/runtime"))
import compare_balance_symmetry as cb
from production_runner import ROOT, require_file, sha256, verify_prepared, verify_sealed_directory
from qualified_snapshot_ingestion import descriptor


PREPARED_SHA = "2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7"
CE_SHA = "49404f9db97d3908df2c279f40b620ec7b9a0db80ce9f8935a8d6de77a03701f"


def main():
    art = ROOT / "validation/artifacts"
    production = art / "axial-material-production-qualified-AB-compensated-20261004"
    admission = art / "axial-material-qualified-AB-compensated-admission-20261004"
    ce = art / "axial-material-ce-qualified-AB-compensated-20261004"
    obs = art / "axial-material-qualified-AAA-observables-20261004"
    prepared = verify_prepared(production / "prepared.json", PREPARED_SHA)
    status_path = production / "AAA/run_status.json"
    status = json.loads(status_path.read_text())
    case = status["cases"]["AAA"]
    if (status["classification"] != "WAITING_REFERENCE"
            or case["classification"] != "VALID_MET"
            or status["prepared_sha256"] != PREPARED_SHA):
        raise ValueError("saved independently checked AAA fixed point required")
    if case["completed_maps"] != len(case["maps"]) or not case["maps"]:
        raise ValueError("incomplete fixed-point map history")
    for row in case["maps"]:
        verify_sealed_directory(production / "AAA" / f"map{row['epoch']:03d}")
    final = Path(case["final_directory"])
    verify_sealed_directory(production / "AAA/bootstrap")
    verify_sealed_directory(production / "archives")
    verify_sealed_directory(production / "training")
    defects = case["maps"][-1]["defects"]
    if any(defects[key] > status["outer_gate"] for key in ("RRHO", "RLEAK", "RA")):
        raise ValueError("original three-defect gate not met")
    equivalence_path = admission / "input_equivalence_AAA.json"
    equivalence = json.loads(equivalence_path.read_text())
    if (equivalence["status"] != "PASS" or equivalence["case"] != "AAA"
            or equivalence["case_spec_sha256"] != prepared["case_spec"]["sha256"]):
        raise ValueError("current physical-input mapping not admitted")
    for key in ("actual_axial_track", "actual_archive", "previous_physical_audit"):
        pin = equivalence[key]
        require_file(Path(pin["path"]), pin["sha256"])
    for name, pin in equivalence["CE_inputs"].items():
        require_file(Path(pin["path"]), pin["sha256"])
        require_file(ce / "AAA" / name, pin["sha256"])
    rules_path = ce / "balance_symmetry_rules.json"
    rules = json.loads(rules_path.read_text())
    if rules != cb.predeclared_rules(Path(prepared["case_spec"]["path"])):
        raise ValueError("saved production observation rules differ")
    inputs = [obs / f"observables.{name}" for name in ("regions.csv", "faces.csv", "summary.txt")]
    result = cb.evaluate_production(cb.read_production(*inputs, rules), rules)
    if any(value != "PASS" for value in result["checks"].values()):
        raise ValueError("saved production sign, accounting or symmetry check failed")
    saved_checks = json.loads((obs / "production_checks.json").read_text())
    if any(saved_checks[key] != value for key, value in result.items()):
        raise ValueError("saved production checks differ from fresh replay")
    for path, digest in saved_checks["input_identities"].items():
        require_file(Path(path), digest)
    manifest = require_file(ce / "AAA/execution.json", CE_SHA)
    if any((ce / "AAA" / name).exists() for name in ("run_claim.json", "openmc.log", "native_result.json")):
        raise ValueError("fresh single-shot CE execution required")
    receipt = dict(schema="AXMAT_AAA_CE_MEASUREMENT_ADMISSION_V1", case="AAA",
        classification="FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE",
        independent_accuracy_qualified=False, ABA_admitted=False,
        prepared=descriptor(production / "prepared.json"), AAA_status=descriptor(status_path),
        final_seal=descriptor(final / "result.json"), common_basis_sha256=status["common_basis_sha256"],
        input_equivalence=descriptor(equivalence_path), production_checks=descriptor(obs / "production_checks.json"),
        CE_manifest=descriptor(manifest), implementation=descriptor(Path(__file__).resolve()),
        completed_maps=case["completed_maps"], defects=defects,
        scope="Admission to the unchanged independent accuracy measurement only. Full AAA CE qualification is required before ABA.")
    target = ce / "AAA/measurement_admission.json"
    with target.open("x") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(json.dumps(descriptor(target), indent=2))


if __name__ == "__main__":
    main()
