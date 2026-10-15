"""Freeze a longer native source history, keeping all physical accuracy gates.

Sampling changes are explicit: 10,000 particles per generation, ten generations
per batch, 100 inactive and 250 active batches. No UFS or feedback acceleration.
Original frozen runs and source files are never changed.
"""
import argparse
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

from prepare_qualified_AAA_ce_ufs import ART, ROOT, PARENT, PRODUCTION, PREPARED_SHA, PARENT_EXEC_SHA, COMMIT, SOURCE, digest, pin, verify, write_new

OUT = ART / 'axial-material-ce-qualified-AAA-long-generations-20261004'
TOOLS = ROOT / 'validation/axial_material'
OBS = ART / 'axial-material-qualified-AAA-observables-20261004'
NP = 10000
GPB = 10


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('source adaptation anchor is not unique: '+old[:90])
    return text.replace(old, new)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    item = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(item)
    return item


def xml_value(node):
    return node.tag, tuple(sorted(node.attrib.items())), (node.text or '').strip(), tuple(xml_value(child) for child in node)


def stage(folder, smoke, template):
    folder.mkdir()
    for name in ('materials.xml', 'geometry.xml', 'tallies.xml'):
        shutil.copy2(PARENT / 'AAA' / name, folder / name)
    tree = ET.parse(PARENT / 'AAA/settings.xml')
    settings = tree.getroot()
    settings.find('particles').text = '1000' if smoke else str(NP)
    settings.find('generations_per_batch').text = str(GPB)
    if smoke:
        settings.find('inactive').text = '10'
        settings.find('batches').text = '20'
        settings.find('state_point/batches').text = ' '.join(map(str, range(11,21)))
    ET.indent(tree, space='  ')
    tree.write(folder / 'settings.xml', encoding='UTF-8', xml_declaration=True)
    replay = ET.parse(folder / 'settings.xml').getroot()
    parent = ET.parse(PARENT / 'AAA/settings.xml').getroot()
    for name in ('particles','generations_per_batch') + (('inactive','batches','state_point') if smoke else ()):
        replay.remove(replay.find(name)); parent.remove(parent.find(name))
    if xml_value(replay) != xml_value(parent):
        raise ValueError('undeclared input setting changed')
    contract = json.loads((PARENT / 'AAA/reference_contract.json').read_text())
    contract['config'].update(particles=1000 if smoke else NP, generations_per_batch=GPB,
        particles_per_batch=(1000 if smoke else NP)*GPB)
    if smoke:
        contract['config'].update(inactive=10, active=10)
        contract['statepoint_batches'] = list(range(11,21))
    contract['input_hashes']['settings.xml'] = digest(folder / 'settings.xml')
    contract['sampling_addendum'] = str(OUT / 'declaration.json')
    contract['source_history_policy'] = 'Native consecutive generations, no imported bank or feedback. All generations retained; batch means of k-generation and entropy are the declared history units. Raw histories are also saved in the analysis.'
    write_new(folder / 'reference_contract.json', contract)
    execution = copy.deepcopy(template)
    execution.update(wall_seconds=120 if smoke else 10800, threads=1,
        resource_addendum=str(OUT / 'resource_addendum.json'),
        sampling_addendum=str(OUT / 'declaration.json'))
    return execution


def prepare():
    if digest(PRODUCTION / 'prepared.json') != PREPARED_SHA or digest(PARENT / 'AAA/execution.json') != PARENT_EXEC_SHA:
        raise ValueError('original frozen experiment changed')
    template = json.loads((PARENT / 'AAA/execution.json').read_text())
    verify(template['files'])
    latest = ART / 'axial-material-ce-qualified-AAA-ufs-20261004/AAA/native_result.json'
    if json.loads(latest.read_text())['returncode'] is None:
        raise ValueError('earlier CE is still running')
    code = [SOURCE / 'src' / name for name in ('eigenvalue.cpp','settings.cpp','simulation.cpp','state_point.cpp','physics.cpp','mesh.cpp')]
    if subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'], text=True).strip() != COMMIT:
        raise ValueError('native source commit changed')
    if subprocess.check_output(['git','-C',str(SOURCE),'diff','HEAD','--',*[str(p.relative_to(SOURCE)) for p in code]], text=True):
        raise ValueError('native sampling source modified')
    OUT.mkdir(exist_ok=False)
    (OUT / 'runtime').mkdir()
    for name in ('production_runner.py','production_inputs.py'):
        shutil.copy2(PARENT / 'runtime' / name, OUT / 'runtime' / name)
    original_executor = (PARENT / 'runtime/ce_execution.py').read_text()
    executor = once(original_executor, 'cap not in (120, 1800, 5400)', 'cap not in (120, 10800)')
    executor = once(executor, 'if cap == 5400:', 'if cap == 10800:')
    executor = once(executor, "'AXMAT_CE_RESOURCE_ADDENDUM_V1'", "'AXMAT_CE_LONG_GENERATIONS_RESOURCE_ADDENDUM_V1'")
    executor = once(executor, "supplement.get('formal_particles_per_batch') != reference['particles_per_batch']",
        "supplement.get('formal_particles_per_generation') != 10000\n                or supplement.get('formal_generations_per_batch') != 10\n                or supplement.get('formal_total_histories') != 35000000")
    (OUT / 'runtime/ce_execution.py').write_text(executor)
    (OUT / 'runtime/ce_execution.patch').write_text(''.join(difflib.unified_diff(original_executor.splitlines(True), executor.splitlines(True), fromfile='frozen_parent', tofile='long_generation_executor')))
    old_stats = (TOOLS / 'reference_statistics.py').read_text()
    stats = once(old_stats, "particles=spec['reference']['particles_per_batch'], generations_per_batch=1,", 'particles=10000, generations_per_batch=10,')
    stats = once(stats, 'one generation per batch; no missing batch, truncation, or post-result block choice.',
        'ten consecutive generations per batch; no missing batch, truncation, or post-result block choice. Batch means are the k/entropy history units, and all raw generation histories remain recorded.')
    stats = once(stats, 'sp.generations_per_batch!=1', "sp.generations_per_batch!=rules['generations_per_batch']")
    stats = once(stats, 'def extract_statepoints(directory, contract, rules):', '''def aggregate_generation_history(raw, batches, gpb, label):
    values=np.asarray(raw,dtype=float)
    if values.shape!=(batches*gpb,) or not np.isfinite(values).all():
        raise EvidenceError('incomplete/nonfinite raw generation history: '+label)
    return values.reshape(batches,gpb).mean(axis=1).tolist()


def extract_statepoints(directory, contract, rules):''')
    stats = once(stats, "history['k_generation']=np.asarray(sp.k_generation).tolist()", "history['raw_k_generation']=np.asarray(sp.k_generation).tolist()\n                history['k_generation']=aggregate_generation_history(history['raw_k_generation'],inactive+active,rules['generations_per_batch'],'k')")
    stats = once(stats, "try:history['entropy']=np.asarray(sp.entropy).tolist()", "try:\n                    history['raw_entropy']=np.asarray(sp.entropy).tolist()\n                    history['entropy']=aggregate_generation_history(history['raw_entropy'],inactive+active,rules['generations_per_batch'],'entropy')")
    stats = once(stats, "result['statepoint_identities']=identities", "result['statepoint_identities']=identities\n        result['source_generation_history']=history\n        result['generation_history_aggregation']=dict(generations_per_batch=rules['generations_per_batch'],total_generations=(rules['inactive_batches']+rules['active_batches'])*rules['generations_per_batch'],method='arithmetic mean of each consecutive batch; no omitted or overlapping generation')")
    stats_path = OUT / 'runtime/reference_statistics.py'
    stats_path.write_text(stats)
    (OUT / 'runtime/reference_statistics.patch').write_text(''.join(difflib.unified_diff(old_stats.splitlines(True),stats.splitlines(True),fromfile='frozen_parent',tofile='long_generation_history_reader')))
    shutil.copy2(TOOLS / 'compare_balance_symmetry.py', OUT / 'runtime/compare_balance_symmetry.py')
    current_sources = [Path(__file__).resolve(), Path(sys.modules['prepare_qualified_AAA_ce_ufs'].__file__).resolve(),
        TOOLS / 'reference_statistics.py', TOOLS / 'compare_balance_symmetry.py',
        PARENT / 'runtime/ce_execution.py', SOURCE / 'build/include/openmc/version.h', *code]
    addendum = dict(schema='AXMAT_CE_LONG_GENERATIONS_RESOURCE_ADDENDUM_V1',status='PREDECLARED_BEFORE_FORMAL_CE_TRANSPORT',
        case_spec_sha256=template['case_spec']['sha256'],formal_ce_wall_seconds_per_case=10800,
        formal_particles_per_generation=NP,formal_generations_per_batch=GPB,formal_particles_per_batch=NP*GPB,
        formal_inactive_batches=100,formal_active_batches=250,formal_total_histories=35000000,
        threads=1,new_numeric_children_at_once=1,automatic_retries=0,
        authorization='Existing user authorization for ordered autonomous work and routine approvals; physical inputs and accuracy gates unchanged.',
        rationale='Prior complete 17.5-million-history references took 3641.5 and 3577.6 seconds. This trial doubles total histories, retains >=10000 particles per generation, gives ten times as many generations before/after activation, and has a fixed three-hour ceiling. No adaptive budget extension or repeat.',
        artifact_budget_bytes=24*2**30,min_free_bytes=8*2**30)
    write_new(OUT / 'resource_addendum.json', addendum)
    write_new(OUT / 'declaration.json', dict(schema='AXMAT_CE_LONG_GENERATIONS_SAMPLING_V1',declared_unix=time.time(),
        original_case_spec=template['case_spec'],original_production=pin(PRODUCTION / 'prepared.json'),
        previous_reference=pin(ART / 'axial-material-ce-qualified-AAA-ufs-20261004/AAA/reference_assessment.json'),
        formal=dict(particles_per_generation=NP,generations_per_batch=GPB,particles_per_batch=NP*GPB,inactive_batches=100,active_batches=250,
            inactive_generations=1000,active_generations=2500,inactive_histories=10000000,active_histories=25000000,seed=310031),
        smoke=dict(particles_per_generation=1000,generations_per_batch=GPB,inactive_batches=10,active_batches=10,total_histories=200000,wall_seconds=120),
        source_policy='Exactly the original independently declared initial source. Native ordinary eigenvalue sampling only; no UFS, CMFD, feedback, imported bank or fit to SPOT.',
        analysis_policy='Original engineering and statistical numerical thresholds, 5/10-batch blocks, 50-batch bridge, all 250 consecutive active statepoints, 4000 joint bootstrap replicates and original seeds retained. The declared 10-generation batch is the history unit; raw generation histories are retained and checked before averaging.',
        changed='Sampling population, generations per batch, total simulated histories and bounded wall budget. No claim that the original one-generation sampling protocol or reader is unchanged.',
        admission='Smoke must natively complete, return exactly 200 k/entropy generation values, ten consecutive active statepoints, exactly ten tally realizations, and original physical/tally mapping. Formal evidence requires actual 3500 histories and all original gates; no automatic retry.',
        physical_inputs_changed=False,engineering_and_statistical_thresholds_changed=False,
        source_files={str(p):digest(p) for p in current_sources},
        links=['https://docs.openmc.org/en/stable/usersguide/settings.html','https://docs.openmc.org/en/stable/methods/eigenvalue.html']))
    roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    template['resource_roots']=roots
    smoke = stage(OUT / 'AAA-smoke',True,template)
    formal = stage(OUT / 'AAA',False,template)
    spec=Path(template['case_spec']['path'])
    # Load the readers from this execution's directory, so the current reader
    # imports the explicitly adapted statistical extractor, never a stale one.
    statmodule=module(stats_path,'long_generation_statistics')
    oldmodule=module(TOOLS / 'reference_statistics.py','parent_reference_statistics')
    new_rules=statmodule.predeclared_rules(spec);old_rules=oldmodule.predeclared_rules(spec)
    delta={key:dict(previous=old_rules.get(key),actual=value) for key,value in new_rules.items() if value!=old_rules.get(key)}
    if set(delta)!={'implementation_sha256','particles','generations_per_batch','adequacy_rules'}:
        raise ValueError('an acceptance rule changed unexpectedly')
    write_new(OUT / 'statistical_rules.json',new_rules)
    import reference_statistics as original_module
    sys.modules['reference_statistics']=statmodule
    try:currentmodule=module(OUT / 'runtime/compare_balance_symmetry.py','long_generation_currents')
    finally:sys.modules['reference_statistics']=original_module
    new_current=currentmodule.predeclared_rules(spec)
    prior_current=json.loads((PARENT / 'balance_symmetry_rules.json').read_text())
    current_delta={key:dict(previous=prior_current.get(key),actual=value) for key,value in new_current.items() if value!=prior_current.get(key)}
    if set(current_delta)!={'statistics_implementation_sha256'}:
        raise ValueError('a current/symmetry acceptance threshold changed')
    write_new(OUT / 'balance_symmetry_rules.json',new_current)
    reviewed=[OUT / 'declaration.json',OUT / 'resource_addendum.json',OUT / 'statistical_rules.json',OUT / 'balance_symmetry_rules.json',
        *[OUT / 'AAA' / name for name in ('materials.xml','geometry.xml','settings.xml','tallies.xml','reference_contract.json')],
        *[p for p in (OUT / 'runtime').iterdir() if p.is_file()],*current_sources]
    write_new(OUT / 'input_sampling_review.json',dict(status='PASS',case='AAA',physical_and_tally_XML_identical=True,
        formal_setting_delta=['particles: 50000 -> 10000 per generation','generations_per_batch: 1 -> 10'],
        statistical_rule_delta=delta,current_rule_delta=current_delta,all_numerical_acceptance_thresholds_unchanged=True,
        initial_source_entropy_seed_temperatures_boundaries_and_nuclear_data_unchanged=True,
        files={str(p.resolve()):digest(p) for p in reviewed}))
    files=dict(template['files'])
    files.update({str(p.resolve()):digest(p) for p in OUT.rglob('*') if p.is_file()})
    files.update({str(p.resolve()):digest(p) for p in current_sources})
    for folder,execution in ((OUT / 'AAA-smoke',smoke),(OUT / 'AAA',formal)):
        execution['files']=files
        write_new(folder / 'execution.json',execution)
    print(json.dumps(dict(classification='LONG_GENERATION_REFERENCE_PREDECLARED_NO_TRANSPORT',
        smoke=pin(OUT / 'AAA-smoke/execution.json'),formal=pin(OUT / 'AAA/execution.json'),review=pin(OUT / 'input_sampling_review.json')),indent=2))


def admit():
    import numpy as np
    review=json.loads((OUT / 'input_sampling_review.json').read_text());verify(review['files'])
    native=json.loads((OUT / 'AAA-smoke/native_result.json').read_text())
    if native['returncode']!=0 or native['error'] is not None or native['status']!='NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS':
        raise ValueError('smoke did not complete; no formal admission')
    verify({str(OUT / 'AAA-smoke' / name):sha for name,sha in native['outputs'].items()})
    rs=module(OUT / 'runtime/reference_statistics.py','long_generation_smoke_reader')
    rules=json.loads((OUT / 'statistical_rules.json').read_text())
    rules.update(particles=1000,inactive_batches=10,active_batches=10)
    contract=json.loads((OUT / 'AAA-smoke/reference_contract.json').read_text())
    batches,k,sigma,history,identities=rs.extract_statepoints(OUT / 'AAA-smoke',contract,rules)
    if len(identities)!=10 or len(history['raw_k_generation'])!=200 or len(history['raw_entropy'])!=200:
        raise ValueError('native generation/realization accounting incomplete')
    if np.asarray(batches['rates']).shape!=(10,96,2) or not np.isfinite(batches['rates']).all():
        raise ValueError('actual tally increments/mapping failed')
    smoke=dict(status='PASS',scientific_qualification=False,native_result=pin(OUT / 'AAA-smoke/native_result.json'),
        statepoint_identities=identities,raw_generations=200,declared_generations_per_batch=10,active_realizations=10,
        initial_source_and_all_physical_inputs_unchanged=True,actual_reader_checked_all_smoke_tallies=True,
        k_smoke=k,sigma_smoke=sigma,scope='Native schema, consecutive generations, all original signed-current/tally mappings only; no source convergence or scientific accuracy acceptance.')
    write_new(OUT / 'smoke_activation_receipt.json',smoke)
    parent=json.loads((PARENT / 'AAA/measurement_admission.json').read_text())
    for key in ('prepared','AAA_status','final_seal','input_equivalence','production_checks','implementation'):
        item=parent[key]
        if digest(item['path'])!=item['sha256']:raise ValueError('saved physical/fixed-point admission changed')
    admission=dict(parent,CE_manifest=pin(OUT / 'AAA/execution.json'),implementation=pin(__file__),
        sampling_declaration=pin(OUT / 'declaration.json'),sampling_review=pin(OUT / 'input_sampling_review.json'),
        smoke_activation=pin(OUT / 'smoke_activation_receipt.json'),parent_measurement_admission=pin(PARENT / 'AAA/measurement_admission.json'),
        scope='Same saved AAA physical fixed point admitted to independently sampled, explicitly longer native history; scientific accuracy and every original threshold remain required.')
    write_new(OUT / 'AAA/measurement_admission.json',admission)
    print(json.dumps(dict(classification='LONG_GENERATION_SMOKE_SCHEMA_PASS_FORMAL_ADMITTED',admission=pin(OUT / 'AAA/measurement_admission.json'),raw_generations=200),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','admit'))
    args=parser.parse_args()
    prepare() if args.action=='prepare' else admit()
