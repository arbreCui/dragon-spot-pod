"""Collect complete frozen AAA reference evidence without relaxing any gate.

Only unanimous original checks produce an ABA admission receipt. Failed or
inconclusive evidence remains recorded, with no qualified receipt emitted.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT / "validation/artifacts/axial-material-production-qualified-AB-compensated-20261004"
sys.path.insert(0, str(PRODUCTION / "runtime"))
from production_runner import require_file, sha256, verify_prepared, verify_sealed_directory, qualify_aba
from qualified_snapshot_ingestion import descriptor

PREPARED_SHA = "2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7"
CE_SHA = "9c90b56cb1e7ab1610b4b1c92ec1784c600c1b46f1e402275425f91bc8a9a0f9"


def verified_report(path):
    report = json.loads(path.read_text())
    if report.get("case") != "AAA":
        raise ValueError("reference evidence must be for AAA")
    for filename, digest in report.get("input_identities", {}).items():
        require_file(Path(filename), digest)
    for pin in report.get("statepoint_identities", []):
        require_file(Path(pin["path"]), pin["sha256"])
    return report


def write_new(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    art = ROOT / "validation/artifacts"
    ce = art / "axial-material-ce-qualified-AAA-ufs-20261004"
    case_dir = ce / "AAA"
    admission_dir = art / "axial-material-qualified-AB-compensated-admission-20261004"
    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)
    execution = json.loads(require_file(case_dir / "execution.json", CE_SHA).read_text())
    for filename, digest in execution["files"].items():
        require_file(Path(filename), digest)
    claim = json.loads((case_dir / "run_claim.json").read_text())
    if claim["manifest_sha256"] != CE_SHA:
        raise ValueError("CE claim differs from frozen execution manifest")
    native = json.loads((case_dir / "native_result.json").read_text())
    if (native["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS"
            or native["returncode"] != 0 or native["error"] is not None):
        raise ValueError("complete original-sample native reference required")
    require_file(case_dir / "openmc.log", native["log_sha256"])
    for filename, digest in native["outputs"].items():
        require_file(case_dir / filename, digest)
    measurement = json.loads((case_dir / "measurement_admission.json").read_text())
    if measurement["classification"] != "FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE":
        raise ValueError("numerical/input admission to the CE measurement required")
    for key in ("prepared", "AAA_status", "final_seal", "input_equivalence", "production_checks", "CE_manifest", "implementation"):
        pin = measurement[key]
        require_file(Path(pin["path"]), pin["sha256"])
    for key in ("sampling_declaration", "sampling_review", "smoke_activation", "parent_measurement_admission"):
        pin = measurement[key]
        require_file(Path(pin["path"]), pin["sha256"])
    review = json.loads(Path(measurement["sampling_review"]["path"]).read_text())
    for filename, digest in review["files"].items():
        require_file(Path(filename), digest)
    if review["status"] != "PASS" or not review["physical_and_tally_XML_identical"]:
        raise ValueError("UFS physical input review failed")
    status_path = PRODUCTION / "AAA/run_status.json"
    status = json.loads(status_path.read_text())
    if (status["classification"] != "WAITING_REFERENCE"
            or status["cases"]["AAA"]["classification"] != "VALID_MET"):
        raise ValueError("AAA saved fixed point changed")
    for directory in (PRODUCTION / "archives", PRODUCTION / "training", PRODUCTION / "AAA/bootstrap", Path(status["cases"]["AAA"]["final_directory"])):
        verify_sealed_directory(directory)
    stats_path = case_dir / "statistics.json"
    currents_path = case_dir / "currents_balance_symmetry.json"
    inputs_path = ce / "input_equivalence_AAA.json"
    stats = verified_report(stats_path)
    currents = verified_report(currents_path)
    inputs = verified_report(inputs_path)
    if stats.get("method") != "independent_continuous_energy_openmc":
        raise ValueError("independent CE statistics required")
    expected_statepoints = [case_dir / f"statepoint.{batch}.h5" for batch in range(101, 351)]
    expected_identities = [dict(path=str(path), sha256=sha256(path)) for path in expected_statepoints]
    if (stats.get("statepoint_identities") != expected_identities
            or currents.get("statepoint_identities") != expected_identities):
        raise ValueError("both analyses must bind every original active-batch statepoint")
    mapping = {"source_convergence": "source_convergence_screen", "block_stability": "block_stability",
        "statistical_resolution": "statistical_resolution", "keff": "keff", "scalar_flux": "scalar_flux", "nu_fission": "nu_fission"}
    checks = {key: stats["checks"][name] for key, name in mapping.items()}
    checks.update(input_equivalence=inputs["status"], currents_balance_symmetry=currents["status"])
    qualified = (stats["classification"] == "STATISTICAL_COMPARISON_PASS"
                 and stats["status"] == "PASS" and all(value == "PASS" for value in checks.values()))
    evidence = {"statistics": descriptor(stats_path), "input_equivalence": descriptor(inputs_path),
        "currents_balance_symmetry": descriptor(currents_path)}
    receipt = dict(schema_version=1, case="AAA", method="independent_continuous_energy_openmc",
        classification="AAA_REFERENCE_QUALIFIED" if qualified else "AAA_REFERENCE_NOT_QUALIFIED",
        experiment_id=prepared["experiment_id"], prepared_sha256=PREPARED_SHA,
        case_spec_sha256=prepared["case_spec"]["sha256"], rank_addendum_sha256=prepared["rank_addendum"]["sha256"],
        common_basis_sha256=sha256(PRODUCTION / "training/common_basis.xsm"),
        aaa_run_status_sha256=sha256(status_path), checks=checks, evidence=evidence,
        CE_execution=descriptor(case_dir / "execution.json"), CE_native_result=descriptor(case_dir / "native_result.json"),
        measurement_admission=descriptor(case_dir / "measurement_admission.json"),
        implementation=descriptor(Path(__file__).resolve()), ABA_admitted=qualified,
        original_scientific_thresholds_changed=False,
        full_neutron_balance="NOT_ASSESSED: current telescoping is an accounting identity; no independent absorption/source tally.")
    write_new(case_dir / "reference_assessment.json", receipt)
    if qualified:
        target = case_dir / "reference_qualification.json"
        write_new(target, receipt)
        qualify_aba(prepared, PRODUCTION, PREPARED_SHA, target, sha256(target))
    print(json.dumps(dict(classification=receipt["classification"], checks=checks, ABA_admitted=qualified,
        assessment=descriptor(case_dir / "reference_assessment.json")), indent=2))


if __name__ == "__main__":
    main()
