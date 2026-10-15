"""Freeze collection of the explicitly changed sampling protocol before CE.

Physical equivalence and all acceptance thresholds are inherited. The reader
groups exactly ten native generation values per declared batch and retains the
raw histories. No physical accuracy gate or ABA guard is relaxed.
"""
import json
from pathlib import Path
import time

from prepare_qualified_AAA_ce_long_generations import OUT, TOOLS, PARENT, PRODUCTION, digest, pin, verify, write_new, once


def main():
    case=OUT / 'AAA'
    if any((case / name).exists() for name in ('run_claim.json','native_result.json','openmc.log')):
        raise ValueError('analysis must be frozen before the formal native run')
    review=json.loads((OUT / 'input_sampling_review.json').read_text())
    if review['status']!='PASS' or not review['physical_and_tally_XML_identical'] or not review['all_numerical_acceptance_thresholds_unchanged']:
        raise ValueError('frozen physical and threshold equivalence required')
    verify(review['files'])
    smoke=json.loads((OUT / 'smoke_activation_receipt.json').read_text())
    if smoke['status']!='PASS' or smoke['scientific_qualification'] or smoke['raw_generations']!=200:
        raise ValueError('complete native multi-generation schema smoke required')
    original_inputs=Path(json.loads((PARENT / 'AAA/reference_assessment.json').read_text())['evidence']['input_equivalence']['path'])
    original=json.loads(original_inputs.read_text())
    if original['case']!='AAA' or original['status']!='PASS':
        raise ValueError('original physical input equivalence not admitted')
    evidence=[original_inputs,OUT / 'input_sampling_review.json',OUT / 'declaration.json',OUT / 'smoke_activation_receipt.json',
        *[case / name for name in ('materials.xml','geometry.xml','settings.xml','tallies.xml','reference_contract.json')]]
    inputs=dict(original,parent_input_equivalence=pin(original_inputs),
        CE_inputs={name:pin(case / name) for name in ('materials.xml','geometry.xml','settings.xml','tallies.xml','reference_contract.json')},
        physical_input_review=pin(OUT / 'input_sampling_review.json'),sampling_declaration=pin(OUT / 'declaration.json'),
        generation_schema_smoke=pin(OUT / 'smoke_activation_receipt.json'),
        input_identities={str(p):digest(p) for p in evidence},
        scope='Same AAA physical model and tallies. Explicit sampling addendum changes particles per generation, generations per batch and total histories; every original numerical acceptance threshold retained. Initial source remains independent of SPOT.')
    write_new(OUT / 'input_equivalence_AAA.json',inputs)
    parent_collector=TOOLS / 'assess_qualified_AAA_reference_compensated.py'
    collector=once(parent_collector.read_text(),'axial-material-ce-qualified-AB-compensated-20261004',OUT.name)
    collector=once(collector,'49404f9db97d3908df2c279f40b620ec7b9a0db80ce9f8935a8d6de77a03701f',digest(case / 'execution.json'))
    collector=once(collector,'inputs_path = admission_dir / "input_equivalence_AAA.json"','inputs_path = ce / "input_equivalence_AAA.json"')
    marker='    status_path = PRODUCTION / "AAA/run_status.json"'
    collector=once(collector,marker,'''    for key in ("sampling_declaration", "sampling_review", "smoke_activation", "parent_measurement_admission"):
        item = measurement[key]
        require_file(Path(item["path"]), item["sha256"])
    review = json.loads(Path(measurement["sampling_review"]["path"]).read_text())
    for filename, expected in review["files"].items():
        require_file(Path(filename), expected)
    if review["status"] != "PASS" or not review["all_numerical_acceptance_thresholds_unchanged"]:
        raise ValueError("sampling/threshold equivalence review failed")
''' + marker)
    marker='    mapping = {"source_convergence": "source_convergence_screen", "block_stability": "block_stability",'
    collector=once(collector,marker,'''    import numpy as np
    history = stats.get("source_generation_history", {})
    for label in ("k_generation", "entropy"):
        raw = np.asarray(history.get("raw_" + label, []), dtype=float)
        batched = np.asarray(history.get(label, []), dtype=float)
        if raw.shape != (3500,) or batched.shape != (350,) or not np.isfinite(raw).all():
            raise ValueError("complete native raw and batched generation histories required")
        if not np.array_equal(raw.reshape(350,10).mean(axis=1), batched):
            raise ValueError("history aggregation differs from the declared consecutive batches")
    if stats.get("generation_history_aggregation", {}).get("generations_per_batch") != 10:
        raise ValueError("actual ten-generation batch analysis required")
''' + marker)
    collector_path=OUT / 'runtime/assess_qualified_AAA_reference_long_generations.py'
    with collector_path.open('x') as stream:stream.write(collector)
    parent_driver=TOOLS / 'run_qualified_AAA_reference_analysis_compensated.py'
    driver=once(parent_driver.read_text(),'axial-material-ce-qualified-AB-compensated-20261004',OUT.name)
    driver=once(driver,'assess_qualified_AAA_reference_compensated.py',collector_path.name)
    for name in ('reference_statistics.py','compare_balance_symmetry.py',collector_path.name):
        driver=once(driver,'str(TOOLS / "'+name+'")','str(CE / "runtime/'+name+'")')
    driver=driver.replace('unchanged AAA evidence analyses','original-threshold AAA evidence analyses for declared batches')
    driver=driver.replace('unchanged original rules','unchanged original thresholds and explicitly declared sampling')
    driver_path=OUT / 'runtime/run_qualified_AAA_reference_analysis_long_generations.py'
    with driver_path.open('x') as stream:stream.write(driver)
    paths=[*evidence,OUT / 'input_equivalence_AAA.json',case / 'measurement_admission.json',OUT / 'statistical_rules.json',
        OUT / 'balance_symmetry_rules.json',OUT / 'runtime/reference_statistics.py',OUT / 'runtime/compare_balance_symmetry.py',
        collector_path,driver_path,parent_collector,parent_driver,Path(__file__).resolve(),
        Path(__import__('prepare_qualified_AAA_ce_long_generations').__file__).resolve()]
    write_new(OUT / 'analysis_collection_declaration.json',dict(schema='AXMAT_LONG_GENERATION_ORIGINAL_THRESHOLD_ANALYSIS_V1',
        declared_unix=time.time(),status='FROZEN_BEFORE_FORMAL_TRANSPORT',files={str(p):digest(p) for p in paths},
        changes=['particle/generation runtime identities','batch means of exactly ten successive generation values with retained raw histories',
            'current reader imports the declared extractor','collector rechecks complete 3500-to-350 histories and unchanged threshold admission'],
        physical_inputs_changed=False,engineering_or_statistical_numerical_thresholds_changed=False,
        qualification='All original eight AAA requirements must be PASS before the actual original ABA guard can admit the same frozen production experiment. Failed or inconclusive evidence remains unqualified.',
        analysis_wall_seconds=120,threads=1,retries=0,transport_launched=False))
    print(json.dumps(dict(driver=pin(driver_path),collector=pin(collector_path),declaration=pin(OUT / 'analysis_collection_declaration.json')),indent=2))


if __name__=='__main__':main()
