"""Predeclare 2000 active native batches for the fresh white coupled AAA.

Only history length and its bounded resource allowance change from the frozen
10-generation reference. Original physical inputs and every numerical gate
remain frozen. No imported bank, fitting, statepoint discard or transport.
"""
import copy
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
PRIOR = ART / 'axial-material-ce-qualified-AAA-long-generations-20261004'
DIAG = ART / 'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004'
OBS = ART / 'axial-material-qualified-AAA-white-trace-observables-20261004'
OUT = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-20261004'
PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
PRIOR_EXEC_SHA = 'ac11a8edc48d0a288a41a37fe0f0c7ebdbec66317d49c63203f18e37c75337c6'
ACTIVE, INACTIVE, GPB, NP, WALL = 2000, 100, 10, 10000, 64800
SOURCE = Path('/Users/wen/openmc-workspace/src')
COMMIT = 'e542b2f035e397a647cc3ad0ae39946b1ad81e7b'
sys.path.insert(0,str(PROD / 'runtime'))
from production_runner import require_file,sha256,verify_prepared,verify_sealed_directory


def pin(p):
    p=Path(p).resolve();return dict(path=str(p),sha256=sha256(p))


def write_new(p,value):
    with p.open('x') as f:json.dump(value,f,indent=2);f.write('\n')


def verify(files):
    for name,wanted in files.items():require_file(Path(name),wanted)


def once(s,old,new):
    if s.count(old)!=1:raise ValueError('nonunique source anchor: '+old)
    return s.replace(old,new)


def adapt(old,new,changes):
    original=old.read_text();s=original
    for a,b in changes:s=once(s,a,b)
    with new.open('x') as f:f.write(s)
    with new.with_suffix(new.suffix+'.patch').open('x') as f:f.write(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile=str(old),tofile=str(new))))


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


def xml_value(n):
    return n.tag,tuple(sorted(n.attrib.items())),(n.text or '').strip(),tuple(xml_value(c) for c in n)


def main():
    info=verify_prepared(PROD/'prepared.json',PREPARED_SHA)
    status_path=PROD/'AAA/run_status.json';status=json.loads(status_path.read_text())
    if status['classification']!='WAITING_REFERENCE' or status['cases']['AAA']['classification']!='VALID_MET':raise ValueError('fresh coupled fixed point required')
    final=Path(status['cases']['AAA']['final_directory'])
    for p in [PROD/'archives',PROD/'training',PROD/'AAA/bootstrap',final]:verify_sealed_directory(p)
    prior_exec=json.loads(require_file(PRIOR/'AAA/execution.json',PRIOR_EXEC_SHA).read_text());verify(prior_exec['files'])
    prior_native=json.loads((PRIOR/'AAA/native_result.json').read_text())
    if prior_native['status']!='NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS' or prior_native['returncode']!=0 or prior_native['error'] is not None:raise ValueError('prior reference not terminal')
    for n,w in prior_native['outputs'].items():require_file(PRIOR/'AAA'/n,w)
    diagnostic=json.loads((DIAG/'result.json').read_text())
    if diagnostic['status']!='COMPLETE_SAVED_REFERENCE_DIAGNOSTIC':raise ValueError('full-coupling saved-reference diagnostic required')
    for n,w in diagnostic['outputs'].items():require_file(DIAG/n,w)
    smoke=json.loads((PRIOR/'smoke_activation_receipt.json').read_text())
    if smoke['status']!='PASS' or smoke['scientific_qualification'] or smoke['raw_generations']!=200:raise ValueError('native ten-generation schema not admitted')
    require_file(Path(smoke['native_result']['path']),smoke['native_result']['sha256'])
    for item in smoke['statepoint_identities']:require_file(Path(item['path']),item['sha256'])
    code=[SOURCE/'src'/n for n in ['eigenvalue.cpp','settings.cpp','simulation.cpp','state_point.cpp','physics.cpp','mesh.cpp']]
    if subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip()!=COMMIT:raise ValueError('native source commit changed')
    if subprocess.check_output(['git','-C',str(SOURCE),'diff','HEAD','--',*[str(p.relative_to(SOURCE)) for p in code]],text=True):raise ValueError('native physical/sampling implementation changed')
    OUT.mkdir(exist_ok=False);(OUT/'runtime').mkdir();case=OUT/'AAA';case.mkdir()
    for p in (PROD/'runtime').iterdir():
        if p.is_file():shutil.copy2(p,OUT/'runtime'/p.name)
    for n in ['materials.xml','geometry.xml','tallies.xml']:shutil.copy2(PRIOR/'AAA'/n,case/n)
    tree=ET.parse(PRIOR/'AAA/settings.xml');settings=tree.getroot()
    settings.find('batches').text=str(INACTIVE+ACTIVE)
    settings.find('state_point/batches').text=' '.join(map(str,range(INACTIVE+1,INACTIVE+ACTIVE+1)))
    ET.indent(tree,space='  ');tree.write(case/'settings.xml',encoding='UTF-8',xml_declaration=True)
    previous=ET.parse(PRIOR/'AAA/settings.xml').getroot();actual=ET.parse(case/'settings.xml').getroot()
    actual.find('batches').text=previous.find('batches').text
    actual.find('state_point/batches').text=previous.find('state_point/batches').text
    if xml_value(previous)!=xml_value(actual):raise ValueError('undeclared settings change')
    contract=json.loads((PRIOR/'AAA/reference_contract.json').read_text())
    contract['config']['active']=ACTIVE;contract['statepoint_batches']=list(range(INACTIVE+1,INACTIVE+ACTIVE+1))
    contract['input_hashes']['settings.xml']=sha256(case/'settings.xml')
    contract['sampling_addendum']=str(OUT/'declaration.json')
    write_new(case/'reference_contract.json',contract)
    adapt(PRIOR/'runtime/reference_statistics.py',OUT/'runtime/reference_statistics.py',[
        ("active_batches=spec['reference']['active_batches'],",'active_batches=2000,')])
    adapt(PRIOR/'runtime/compare_balance_symmetry.py',OUT/'runtime/compare_balance_symmetry.py',[
        ("active_batches=spec['reference']['active_batches'],",'active_batches=2000,')])
    adapt(PRIOR/'runtime/ce_execution.py',OUT/'runtime/ce_execution.py',[
        ('cap not in (120, 10800)','cap != 64800'),('if cap == 10800:','if cap == 64800:'),
        ("'AXMAT_CE_LONG_GENERATIONS_RESOURCE_ADDENDUM_V1'","'AXMAT_CE_WHITE_TRACE_PRECISION_RESOURCE_ADDENDUM_V1'"),
        ("supplement.get('formal_total_histories') != 35000000","supplement.get('formal_total_histories') != 210000000"),
        ("supplement.get('formal_active_batches') != reference['active_batches']","supplement.get('formal_active_batches') != 2000"),
        ("    case_spec = json.loads(case_path.read_text())",'''    collection = json.loads((folder.parent / 'analysis_collection_declaration.json').read_text())
    if collection.get('schema') != 'AXMAT_WHITE_TRACE_PRECISION_ORIGINAL_THRESHOLD_ANALYSIS_V1' or collection.get('status') != 'FROZEN_BEFORE_FORMAL_TRANSPORT':
        raise RuntimeError('frozen original-threshold analysis collection required')
    for name, wanted in collection['files'].items():
        if digest(name) != wanted:
            raise RuntimeError('measurement/analysis input changed: ' + name)
    admission = json.loads((folder / 'measurement_admission.json').read_text())
    if admission.get('classification') != 'FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE' or admission.get('case') != 'AAA':
        raise RuntimeError('fresh same-case measurement admission required')
    if admission['CE_manifest'] != dict(path=str(manifest), sha256=expected_sha256):
        raise RuntimeError('measurement admission does not bind this native execution')
    prepared_pin = admission['prepared']
    production = Path(prepared_pin['path']).parent
    prepared = production_runner.verify_prepared(Path(prepared_pin['path']), prepared_pin['sha256'])
    if prepared['case_spec'] != protocol:
        raise RuntimeError('production/reference physical declaration differs')
    status_pin = admission['AAA_status']
    if digest(status_pin['path']) != status_pin['sha256']:
        raise RuntimeError('admitted production status changed')
    saved = json.loads(Path(status_pin['path']).read_text())
    if saved['classification'] != 'WAITING_REFERENCE' or saved['cases']['AAA']['classification'] != 'VALID_MET':
        raise RuntimeError('actual coupled fixed point required before native reference')
    for directory in (production / 'archives', production / 'training', production / 'AAA/bootstrap', Path(saved['cases']['AAA']['final_directory'])):
        production_runner.verify_sealed_directory(directory)
    case_spec = json.loads(case_path.read_text())''')])
    spec=Path(info['case_spec']['path']);rs=module(OUT/'runtime/reference_statistics.py','reference_statistics')
    sys.modules['reference_statistics']=rs;cb=module(OUT/'runtime/compare_balance_symmetry.py','precision_cb')
    stat=rs.predeclared_rules(spec);current=cb.predeclared_rules(spec)
    deltas=[]
    for new,oldpath,allowed in [(stat,PRIOR/'statistical_rules.json',{'case_spec_sha256','implementation_sha256','active_batches'}),
        (current,PRIOR/'balance_symmetry_rules.json',{'case_spec_sha256','implementation_sha256','statistics_implementation_sha256','active_batches'})]:
        old=json.loads(oldpath.read_text());delta={k:dict(previous=old.get(k),actual=v) for k,v in new.items() if old.get(k)!=v}
        if set(delta)!=allowed:raise ValueError('undeclared statistical/current rule delta')
        deltas.append(delta)
    write_new(OUT/'statistical_rules.json',stat);write_new(OUT/'balance_symmetry_rules.json',current)
    original_stats=json.loads((PRIOR/'AAA/statistics.json').read_text())
    noise=[r['reference_only_error_upper_95'] for r in original_stats['block_reports']]
    declaration=dict(schema='AXMAT_CE_WHITE_TRACE_PRECISION_SAMPLING_V1',declared_unix=time.time(),
        original_case_spec=pin(spec),production_prepared=pin(PROD/'prepared.json'),prior_complete_reference=pin(PRIOR/'AAA/native_result.json'),
        prior_statistics=pin(PRIOR/'AAA/statistics.json'),fresh_coupled_diagnostic=pin(DIAG/'result.json'),
        formal=dict(particles_per_generation=NP,generations_per_batch=GPB,particles_per_batch=NP*GPB,inactive_batches=INACTIVE,active_batches=ACTIVE,
            inactive_generations=INACTIVE*GPB,active_generations=ACTIVE*GPB,total_histories=(INACTIVE+ACTIVE)*GPB*NP,seed=310031),
        design='Eight times the previous active sample, fixed before this transport. Worst previously measured flux noise 0.011579 and fuel-fraction noise 0.026339 predict about 0.004094 and 0.009312 at inverse-square-root scaling; these are planning estimates, not accuracy or statistical admission.',
        source_policy='Original ordinary native eigenvalue sampler and seed, fresh original initial source; no imported bank, UFS, feedback, combined old statepoints, fitted coefficient or omitted batch.',
        original_numerical_acceptance_thresholds_changed=False,physical_inputs_changed=False,
        scope='Formal independent CE measurement for this fresh AAA fixed point. All original eight requirements must pass; no qualification from sample size or predictions.',
        previous_reference_only_noise=noise)
    write_new(OUT/'declaration.json',declaration)
    addendum=dict(schema='AXMAT_CE_WHITE_TRACE_PRECISION_RESOURCE_ADDENDUM_V1',status='PREDECLARED_BEFORE_FORMAL_CE_TRANSPORT',
        case_spec_sha256=info['case_spec']['sha256'],formal_ce_wall_seconds_per_case=WALL,
        formal_particles_per_generation=NP,formal_generations_per_batch=GPB,formal_particles_per_batch=NP*GPB,
        formal_inactive_batches=INACTIVE,formal_active_batches=ACTIVE,formal_total_histories=(INACTIVE+ACTIVE)*GPB*NP,
        threads=1,new_numeric_children_at_once=1,automatic_retries=0,artifact_budget_bytes=40*2**30,min_free_bytes=8*2**30,
        estimated_seconds=prior_native['elapsed_seconds']*(INACTIVE+ACTIVE)/(100+250),
        rationale='Existing 35-million-history single-thread reference took 7408 seconds. The fixed 210-million-history design forecasts about 12.35 hours and has an 18-hour cap. Prior bounded runs remain unchanged.',
        authorization='Existing user authorization for ordered autonomous work and routine approvals.')
    write_new(OUT/'resource_addendum.json',addendum)
    reviewed=[Path(__file__).resolve(),OUT/'declaration.json',OUT/'resource_addendum.json',OUT/'statistical_rules.json',OUT/'balance_symmetry_rules.json',
        PROD/'prepared.json',status_path,final/'result.json',*code,*[case/n for n in ['materials.xml','geometry.xml','settings.xml','tallies.xml','reference_contract.json']],
        *[p for p in (OUT/'runtime').iterdir() if p.is_file()]]
    write_new(OUT/'input_sampling_review.json',dict(status='PASS',case='AAA',physical_and_tally_XML_identical=True,
        formal_setting_delta=['active batches: 250 -> 2000','statepoint batches: every active batch 101 through 2100'],
        statistical_rule_delta=deltas[0],current_rule_delta=deltas[1],all_numerical_acceptance_thresholds_unchanged=True,
        initial_source_entropy_seed_temperatures_boundaries_and_nuclear_data_unchanged=True,files={str(p.resolve()):sha256(p) for p in reviewed}))
    old_inputs=json.loads((DIAG/'input_equivalence_AAA.json').read_text())
    inputs=dict(old_inputs,CE_inputs={n:pin(case/n) for n in ['materials.xml','geometry.xml','settings.xml','tallies.xml','reference_contract.json']},
        parent_input_equivalence=pin(DIAG/'input_equivalence_AAA.json'),physical_input_review=pin(OUT/'input_sampling_review.json'),
        sampling_declaration=pin(OUT/'declaration.json'),generation_schema_smoke=pin(PRIOR/'smoke_activation_receipt.json'),
        input_identities={str(p.resolve()):sha256(p) for p in [DIAG/'input_equivalence_AAA.json',OUT/'input_sampling_review.json',OUT/'declaration.json',PRIOR/'smoke_activation_receipt.json',*reviewed]})
    write_new(OUT/'input_equivalence_AAA.json',inputs)
    roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    execution=copy.deepcopy(prior_exec)
    execution.update(case_spec=info['case_spec'],wall_seconds=WALL,resource_roots=roots,resource_addendum=str(OUT/'resource_addendum.json'),sampling_addendum=str(OUT/'declaration.json'))
    files=dict(prior_exec['files']);files.update({str(p.resolve()):sha256(p) for p in OUT.rglob('*') if p.is_file()});files.update({str(p.resolve()):sha256(p) for p in reviewed})
    execution['files']=files;write_new(case/'execution.json',execution)
    write_new(case/'measurement_admission.json',dict(schema='AXMAT_AAA_CE_MEASUREMENT_ADMISSION_V1',case='AAA',classification='FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE',
        independent_accuracy_qualified=False,ABA_admitted=False,prepared=pin(PROD/'prepared.json'),AAA_status=pin(status_path),final_seal=pin(final/'result.json'),
        common_basis_sha256=status['common_basis_sha256'],input_equivalence=pin(OUT/'input_equivalence_AAA.json'),production_checks=pin(DIAG/'production_checks.json'),
        CE_manifest=pin(case/'execution.json'),implementation=pin(Path(__file__).resolve()),completed_maps=status['cases']['AAA']['completed_maps'],defects=status['cases']['AAA']['maps'][-1]['defects'],
        sampling_declaration=pin(OUT/'declaration.json'),sampling_review=pin(OUT/'input_sampling_review.json'),smoke_activation=pin(PRIOR/'smoke_activation_receipt.json'),
        parent_measurement_admission=pin(PRIOR/'AAA/measurement_admission.json'),scope='Fresh AAA and original physical reference, explicit extended sampling only; original gates remain required.'))
    collector=OUT/'runtime/assess_qualified_AAA_white_trace_precision.py'
    adapt(PRIOR/'runtime/assess_qualified_AAA_reference_long_generations_v2.py',collector,[
        ('axial-material-production-qualified-AB-compensated-20261004',PROD.name),("PREPARED_SHA = \"2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7\"",'PREPARED_SHA = "'+PREPARED_SHA+'"'),
        ('CE_SHA = "'+PRIOR_EXEC_SHA+'"','CE_SHA = "'+sha256(case/'execution.json')+'"'),
        ('axial-material-ce-qualified-AAA-long-generations-20261004',OUT.name),('axial-material-qualified-AB-compensated-admission-20261004','axial-material-qualified-AB-white-trace-admission-20261004'),
        ('range(101, 351)','range(101, 2101)'),('f"statepoint.{batch}.h5"','f"statepoint.{batch:04d}.h5"'),
        ('raw.shape != (3500,) or batched.shape != (350,)','raw.shape != (21000,) or batched.shape != (2100,)'),('raw.reshape(350,10)','raw.reshape(2100,10)')])
    driver=OUT/'runtime/run_qualified_AAA_white_trace_precision_analysis.py'
    adapt(PRIOR/'runtime/run_qualified_AAA_reference_analysis_long_generations_v2.py',driver,[
        ('axial-material-ce-qualified-AAA-long-generations-20261004',OUT.name),('axial-material-qualified-AAA-observables-20261004',OBS.name),
        ('axial-material-qualified-AB-compensated-admission-20261004','axial-material-qualified-AB-white-trace-admission-20261004'),
        ('assess_qualified_AAA_reference_long_generations_v2.py',collector.name),
        ('declaration = json.loads((CE / "analysis_collection_declaration_v2.json").read_text())','declaration = json.loads((CE / "analysis_collection_declaration.json").read_text())'),
        ('CE / "analysis_collection_declaration_v2.json", *[Path(name) for name in declaration["files"]]','CE / "analysis_collection_declaration.json", *[Path(name) for name in declaration["files"]]')])
    analysis_files=[*reviewed,OUT/'input_sampling_review.json',OUT/'input_equivalence_AAA.json',case/'execution.json',case/'measurement_admission.json',
        DIAG/'production_checks.json',PRIOR/'smoke_activation_receipt.json',collector,driver,*[OBS/f'observables.{n}' for n in ['regions.csv','faces.csv','summary.txt']]]
    write_new(OUT/'analysis_collection_declaration.json',dict(schema='AXMAT_WHITE_TRACE_PRECISION_ORIGINAL_THRESHOLD_ANALYSIS_V1',declared_unix=time.time(),status='FROZEN_BEFORE_FORMAL_TRANSPORT',
        files={str(p.resolve()):sha256(p) for p in analysis_files},analysis_wall_seconds=120,threads=1,retries=0,transport_launched=False,
        engineering_or_statistical_numerical_thresholds_changed=False,qualification='Every original AAA check must pass before the unchanged actual ABA guard admits the same prepared production.'))
    print(json.dumps(dict(classification='WHITE_TRACE_PRECISION_REFERENCE_PREDECLARED_NO_TRANSPORT',execution=pin(case/'execution.json'),analysis_declaration=pin(OUT/'analysis_collection_declaration.json'),
        native_executor=pin(OUT/'runtime/ce_execution.py'),collector=pin(collector),driver=pin(driver)),indent=2))


if __name__=='__main__':main()
