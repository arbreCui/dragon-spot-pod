"""Bind the UFS diagnostic to unchanged original analyses and saved AAA inputs."""
import json
from pathlib import Path
import time

from prepare_qualified_AAA_ce_ufs import OUT, PARENT, PRODUCTION, PREPARED_SHA, digest, pin, verify, write_new


def main():
    tools = Path(__file__).resolve().parent
    formal = OUT / 'AAA'
    original_inputs = Path(json.loads((PARENT / 'AAA/reference_assessment.json').read_text())['evidence']['input_equivalence']['path'])
    original = json.loads(original_inputs.read_text())
    review = json.loads((OUT / 'input_sampling_review.json').read_text())
    if review['status'] != 'PASS' or not review['physical_and_tally_XML_identical']:
        raise ValueError('physical and weighted sampling review required')
    verify(review['files'])
    smoke = json.loads((OUT / 'smoke_activation_receipt.json').read_text())
    if smoke['status'] != 'PASS' or smoke['scientific_qualification']:
        raise ValueError('native weighted activation required')
    if original['status'] != 'PASS' or original['case'] != 'AAA':
        raise ValueError('original physical equivalence not admitted')
    new = dict(original, parent_input_equivalence=pin(original_inputs),
        CE_inputs={name: pin(formal / name) for name in ('materials.xml', 'geometry.xml', 'settings.xml', 'tallies.xml', 'reference_contract.json')},
        physical_input_review=pin(OUT / 'input_sampling_review.json'), sampling_declaration=pin(OUT / 'declaration.json'),
        weighted_UFS_activation=pin(OUT / 'smoke_activation_receipt.json'),
        scope='Identical AAA physical model and tally mapping, with only the separately declared native reciprocal-weight UFS source sampling change. No CE-fitted source or engineering-threshold change.')
    new['input_identities'] = {str(p): digest(p) for p in [original_inputs, OUT / 'input_sampling_review.json', OUT / 'declaration.json',
        OUT / 'smoke_activation_receipt.json', *[formal / name for name in ('materials.xml', 'geometry.xml', 'settings.xml', 'tallies.xml', 'reference_contract.json')]]}
    write_new(OUT / 'input_equivalence_AAA.json', new)
    collector_source = tools / 'assess_qualified_AAA_reference_compensated.py'
    collector = collector_source.read_text()
    old_ce_name = 'axial-material-ce-qualified-AB-compensated-20261004'
    if collector.count(old_ce_name) != 1:
        raise ValueError('unexpected parent collector layout')
    collector = collector.replace(old_ce_name, OUT.name)
    collector = collector.replace('49404f9db97d3908df2c279f40b620ec7b9a0db80ce9f8935a8d6de77a03701f', digest(formal / 'execution.json'))
    old_inputs = 'inputs_path = admission_dir / "input_equivalence_AAA.json"'
    if collector.count(old_inputs) != 1:
        raise ValueError('unexpected parent input evidence layout')
    collector = collector.replace(old_inputs, 'inputs_path = ce / "input_equivalence_AAA.json"')
    marker = '    status_path = PRODUCTION / "AAA/run_status.json"'
    if collector.count(marker) != 1:
        raise ValueError('unexpected parent saved state layout')
    collector = collector.replace(marker, '''    for key in ("sampling_declaration", "sampling_review", "smoke_activation", "parent_measurement_admission"):
        pin = measurement[key]
        require_file(Path(pin["path"]), pin["sha256"])
    review = json.loads(Path(measurement["sampling_review"]["path"]).read_text())
    for filename, digest in review["files"].items():
        require_file(Path(filename), digest)
    if review["status"] != "PASS" or not review["physical_and_tally_XML_identical"]:
        raise ValueError("UFS physical input review failed")
''' + marker)
    collector_path = tools / 'assess_qualified_AAA_reference_ufs.py'
    with collector_path.open('x') as stream:
        stream.write(collector)
    driver_source = tools / 'run_qualified_AAA_reference_analysis_compensated.py'
    driver = driver_source.read_text()
    if driver.count(old_ce_name) != 1 or driver.count('assess_qualified_AAA_reference_compensated.py') != 1:
        raise ValueError('unexpected parent analysis layout')
    driver = driver.replace(old_ce_name, OUT.name).replace('assess_qualified_AAA_reference_compensated.py', collector_path.name)
    driver_path = tools / 'run_qualified_AAA_reference_analysis_ufs.py'
    with driver_path.open('x') as stream:
        stream.write(driver)
    frozen = [tools / 'reference_statistics.py', tools / 'compare_balance_symmetry.py', collector_path, driver_path,
        OUT / 'statistical_rules.json', OUT / 'balance_symmetry_rules.json', OUT / 'input_equivalence_AAA.json',
        OUT / 'input_sampling_review.json', OUT / 'declaration.json', OUT / 'smoke_activation_receipt.json',
        formal / 'measurement_admission.json', collector_source, driver_source, Path(__file__).resolve()]
    write_new(OUT / 'analysis_collection_declaration.json', dict(schema='AXMAT_UFS_ORIGINAL_RULES_ANALYSIS_COLLECTION_V1',
        declared_unix=time.time(), files={str(p): digest(p) for p in frozen},
        parent_implementation=pin(collector_source), parent_driver=pin(driver_source),
        adaptations=['new diagnostic CE directory and actual manifest identity', 'input equivalence includes identical physics and declared weighted sampling', 'recheck UFS admission pins before collection'],
        statistical_and_engineering_implementations_changed=False, thresholds_changed=False,
        qualification_requires='All unchanged original AAA gates PASS. Any failed or inconclusive result prohibits ABA.',
        status='FROZEN_BEFORE_COMPLETE_REFERENCE_ANALYSIS', transport_launched_by_this_declaration=False))
    print(json.dumps(dict(classification='ORIGINAL_RULES_UFS_ANALYSIS_PREPARED',
        driver=pin(driver_path), collector=pin(collector_path), declaration=pin(OUT / 'analysis_collection_declaration.json')), indent=2))


if __name__ == '__main__':
    main()
