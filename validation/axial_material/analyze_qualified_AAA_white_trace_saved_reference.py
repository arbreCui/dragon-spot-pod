"""Rebind the complete saved physical reference to the fresh coupled AAA.

Read-only diagnostic at the original numerical gates. The reused sample's
precision admission is retained; this cannot issue an ABA qualification.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
CE = ART / 'axial-material-ce-qualified-AAA-long-generations-20261004'
OUT = ART / 'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004'
OBS = ART / 'axial-material-qualified-AAA-white-trace-observables-20261004'
PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python')
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import (verify_prepared, verify_sealed_directory,
    require_file, sha256, SerialExecutor, DiskResources, qualify_aba, Refusal)


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=sha256(path))


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def verify(files):
    for name, wanted in files.items():
        require_file(Path(name), wanted)


def prepare():
    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
    status_path = PROD / 'AAA/run_status.json'
    status = json.loads(status_path.read_text())
    if status['classification'] != 'WAITING_REFERENCE' or status['cases']['AAA']['classification'] != 'VALID_MET':
        raise ValueError('fresh complete coupled AAA fixed point required')
    for name in ('archives', 'training', 'AAA/bootstrap'):
        verify_sealed_directory(PROD / name)
    final = Path(status['cases']['AAA']['final_directory'])
    verify_sealed_directory(final)
    native = json.loads((CE / 'AAA/native_result.json').read_text())
    if native['status'] != 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS' or native['returncode'] != 0 or native['error'] is not None:
        raise ValueError('saved reference has not completed')
    require_file(CE / 'AAA/openmc.log', native['log_sha256'])
    for name, wanted in native['outputs'].items():
        require_file(CE / 'AAA' / name, wanted)
    execution = json.loads((CE / 'AAA/execution.json').read_text())
    verify(execution['files'])
    review = json.loads((CE / 'input_sampling_review.json').read_text())
    verify(review['files'])
    if review['status'] != 'PASS' or not review['physical_and_tally_XML_identical'] or not review['all_numerical_acceptance_thresholds_unchanged']:
        raise ValueError('saved physical/sampling equivalence proof required')
    physical_path = OUT / 'input_equivalence_AAA.json'
    physical = json.loads(physical_path.read_text())
    if physical['status'] != 'PASS' or physical['production_prepared'] != pin(PROD / 'prepared.json') or physical['AAA_status'] != pin(status_path):
        raise ValueError('current physical mapping does not bind this saved AAA')
    for item in physical['CE_inputs'].values():
        require_file(Path(item['path']), item['sha256'])
    (OUT / 'runtime').mkdir()
    (OUT / 'AAA').mkdir()
    for name in ('reference_statistics.py', 'compare_balance_symmetry.py'):
        shutil.copy2(CE / 'runtime' / name, OUT / 'runtime' / name)
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    rs = module(OUT / 'runtime/reference_statistics.py', 'reference_statistics')
    sys.modules['reference_statistics'] = rs
    cb = module(OUT / 'runtime/compare_balance_symmetry.py', 'white_trace_saved_cb')
    spec_path = Path(info['case_spec']['path'])
    new_rules = rs.predeclared_rules(spec_path)
    current_rules = cb.predeclared_rules(spec_path)
    for new, old_path in ((new_rules, CE / 'statistical_rules.json'), (current_rules, CE / 'balance_symmetry_rules.json')):
        old = json.loads(old_path.read_text())
        if {k:v for k,v in new.items() if k != 'case_spec_sha256'} != {k:v for k,v in old.items() if k != 'case_spec_sha256'}:
            raise ValueError('saved-reference numerical gates changed')
    write_new(OUT / 'statistical_rules.json', new_rules)
    write_new(OUT / 'balance_symmetry_rules.json', current_rules)
    production_inputs = [OBS / f'observables.{name}' for name in ('regions.csv','faces.csv','summary.txt')]
    checks = cb.evaluate_production(cb.read_production(*production_inputs, current_rules), current_rules)
    if any(v != 'PASS' for v in checks['checks'].values()):
        raise ValueError('fresh production sign/accounting/symmetry admission failed')
    checks['input_identities'] = {str(p):sha256(p) for p in production_inputs}
    write_new(OUT / 'production_checks.json', checks)
    common = ['--case-spec',str(spec_path),'--contract',str(CE / 'AAA/reference_contract.json'),
        '--statepoints',str(CE / 'AAA'),'--production-regions',str(production_inputs[0]),
        '--production-summary',str(production_inputs[2])]
    commands = [[str(PYTHON),str(OUT / 'runtime/reference_statistics.py'),'analyze',
        '--rules',str(OUT / 'statistical_rules.json'),*common,'--output',str(OUT / 'statistics.json')],
        [str(PYTHON),str(OUT / 'runtime/compare_balance_symmetry.py'),'compare',
        '--rules',str(OUT / 'balance_symmetry_rules.json'),'--statistics-rules',str(OUT / 'statistical_rules.json'),
        *common,'--production-faces',str(production_inputs[1]),'--output',str(OUT / 'currents_balance_symmetry.json')]]
    files = [PROD / 'prepared.json',status_path,final / 'result.json',physical_path,
        CE / 'AAA/native_result.json',CE / 'AAA/execution.json',CE / 'input_sampling_review.json',
        CE / 'AAA/reference_contract.json',spec_path,PYTHON.resolve(),Path(__file__).resolve(),
        OUT / 'statistical_rules.json',OUT / 'balance_symmetry_rules.json',OUT / 'production_checks.json',
        *production_inputs,*[OUT / 'runtime' / n for n in ('reference_statistics.py','compare_balance_symmetry.py','run_bounded_dragon.py')]]
    pinned = {str(p.resolve()):sha256(p) for p in files}
    pinned.update(execution['files']);pinned.update(review['files'])
    for name,wanted in native['outputs'].items():pinned[str(CE / 'AAA' / name)]=wanted
    roots = sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    declaration = dict(schema='AXMAT_SAVED_CE_FRESH_WHITE_COUPLED_DIAGNOSTIC_V1',declared_unix=time.time(),
        files=pinned,commands=commands,total_wall_seconds=120,threads=1,retries=0,
        resource_roots=roots,artifact_budget_bytes=40*2**30,min_free_bytes=8*2**30,
        sampling='Existing complete 100 inactive + 250 active batches, 10000 particles/generation, 10 generations/batch; all raw statepoints reused by identity.',
        scope='Same physical AAA inputs; explicitly changed conditional angular approximation. Full fresh coupling compared against saved independent CE, with unchanged original numerical gates.',
        new_transport_launched=False,reference_precision_previously_qualified=False,ABA_admitted=False)
    write_new(OUT / 'declaration.json',declaration)
    print(json.dumps(pin(OUT / 'declaration.json'),indent=2))


def run(expected):
    decl_path = require_file(OUT / 'declaration.json',expected)
    d = json.loads(decl_path.read_text());verify(d['files'])
    write_new(OUT / 'run_claim.json',dict(declaration=pin(decl_path),started_unix=time.time()))
    resources = DiskResources(ART,d['resource_roots'],d['min_free_bytes'],d['artifact_budget_bytes'])
    executor = SerialExecutor(OUT,d['total_wall_seconds'],'AAA',resources)
    result = dict(status='FAILED_NO_RETRY',new_transport_launched=False,ABA_admitted=False)
    started = time.monotonic()
    try:
        for i,cmd in enumerate(d['commands'],1):executor.execute(OUT,f'analysis{i}',cmd,120)
        verify(d['files'])
        stats = json.loads((OUT / 'statistics.json').read_text())
        currents = json.loads((OUT / 'currents_balance_symmetry.json').read_text())
        mapping = {'source_convergence':'source_convergence_screen','block_stability':'block_stability',
            'statistical_resolution':'statistical_resolution','keff':'keff','scalar_flux':'scalar_flux','nu_fission':'nu_fission'}
        checks = {k:stats['checks'][v] for k,v in mapping.items()}
        checks.update(input_equivalence='PASS',currents_balance_symmetry=currents['status'])
        info = verify_prepared(PROD / 'prepared.json',PREPARED_SHA)
        assessment = dict(schema_version=1,case='AAA',method='independent_continuous_energy_openmc',
            classification='AAA_REFERENCE_NOT_QUALIFIED',experiment_id=info['experiment_id'],
            checks=checks,ABA_admitted=False,diagnostic_only=True,
            evidence={k:pin(OUT / n) for k,n in [('statistics','statistics.json'),('input_equivalence','input_equivalence_AAA.json'),('currents_balance_symmetry','currents_balance_symmetry.json')]},
            production_prepared=pin(PROD / 'prepared.json'),sampling_declaration=pin(decl_path),
            reason='Saved reference precision is still evaluated under original gates. A separate fully bound qualified-reference collector is required for ABA.')
        write_new(OUT / 'reference_assessment.json',assessment)
        try:qualify_aba(info,PROD,PREPARED_SHA,OUT / 'reference_assessment.json',sha256(OUT / 'reference_assessment.json'))
        except Refusal as error:write_new(OUT / 'aba_guard.json',dict(status='REJECTED',reason=str(error),ABA_created=(PROD / 'ABA').exists()))
        else:raise ValueError('diagnostic unexpectedly admitted ABA')
        result.update(status='COMPLETE_SAVED_REFERENCE_DIAGNOSTIC',checks=checks,assessment=pin(OUT / 'reference_assessment.json'))
    finally:
        result['elapsed_seconds']=time.monotonic()-started
        result['outputs']={p.name:sha256(p) for p in OUT.iterdir() if p.is_file() and p.name not in ('run_claim.json','result.json')}
        write_new(OUT / 'result.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--sha256')
    args=parser.parse_args()
    if args.action=='prepare':prepare()
    elif not args.sha256:parser.error('--sha256 required for run')
    else:run(args.sha256)
