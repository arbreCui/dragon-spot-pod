"""Read-only audit using the unchanged original current-accounting rules.

The original cold controller's exact-zero rejection remains FAILED. No native
solve is repeated, no frozen record is edited, and no AAA/ABA accuracy or
coupled-map qualification follows from this saved-state audit.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode=True
import prepare_AAA_white_trace_cold_control_paths as control
base=control.base
ROOT,ART,PROD=control.ROOT,control.ART,control.PROD
CE=control.CE.parent
OUT=ART / 'axial-material-AAA-white-trace-saved-accounting-20261004'
sys.path.insert(0,str(CE / 'runtime'))
import compare_balance_symmetry as balance
import reference_statistics as statistics


def verified_control():
    declaration=json.loads((control.OUT / 'declaration.json').read_text())
    result=json.loads((control.OUT / 'result.json').read_text())
    if result['classification']!='FAILED_CONDITIONAL_WHITE_TRACE_NATIVE_NO_RETRY' or result['error']!="ValueError('saved scalar/current admission failed')":
        raise ValueError('expected preserved exact-zero controller rejection required')
    for name,sha in declaration['files'].items():base.require_file(Path(name),sha)
    for name,sha in result['outputs'].items():base.require_file(control.OUT / name,sha)
    for case in ('off','on'):
        base.check_terminal((control.OUT / case / 'solve.log').read_text())
        if 'AXMAT-FROZEN-AXIAL-COMPLETE' not in (control.OUT / case / 'solve.log').read_text():
            raise ValueError('actual native completion marker missing')
    stages=json.loads((control.OUT / 'AAA/stages.json').read_text())['stages']
    wanted={'off/solve','off/export','on/solve','on/export'}
    actual={r['label'] for r in stages if r['status']=='PASS'}
    if not wanted<=actual:raise ValueError('native solves or exports incomplete')
    return declaration,result


def prepare():
    declaration,result=verified_control()
    rules=json.loads((CE / 'balance_symmetry_rules.json').read_text())
    info,_=base.prepared();spec=Path(info['case_spec']['path'])
    if rules!=balance.predeclared_rules(spec) or rules['telescoping_epsilon_multiplier']!=64:
        raise ValueError('original frozen rules/code identity changed')
    OUT.mkdir(exist_ok=False)
    for name in ('runtime','AAA'):(OUT / name).mkdir()
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py',OUT / 'runtime/run_bounded_dragon.py')
    files=[Path(__file__).resolve(),Path(control.__file__),Path(base.__file__),Path(balance.__file__),Path(statistics.__file__),
        Path(sys.executable).resolve(),OUT / 'runtime/run_bounded_dragon.py',CE / 'balance_symmetry_rules.json',
        CE / 'AAA/statistics.json',CE / 'AAA/reference_contract.json',CE / 'AAA/reference_assessment.json',spec,
        control.OUT / 'declaration.json',control.OUT / 'result.json',control.OUT / 'build_identity.json',
        PROD / 'prepared.json',PROD / 'AAA/run_status.json',*[Path(p) for p in declaration['files']],
        *[control.OUT / name for name in result['outputs']]]
    base.write_new(OUT / 'declaration.json',dict(schema='AXMAT_WHITE_TRACE_SAVED_ORIGINAL_ACCOUNTING_AUDIT_V1',declared_unix=time.time(),
        files={str(p.resolve()):base.digest(p) for p in files},original_controller_result=base.pin(control.OUT / 'result.json'),
        original_rules=base.pin(CE / 'balance_symmetry_rules.json'),wall_seconds=90,threads=1,retries=0,
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()),
        min_free_bytes=8*2**30,artifact_budget_bytes=24*2**30,
        preserved_rejection='The original controller imposed exact zero on an exported floating-point telescoping residual. That controller result and every native output remain unchanged. This new audit invokes the already-frozen original 64*eps64*sum(abs(group-summed region-face currents)) rule and its unchanged parser directly.',
        comparisons='Both actual completed cold states: original native terminals, complete saved REAL64 authority/positivity, unchanged current sign/accounting/mirror rules. Report ON vs OFF and reference sample-mean discrepancies; the current reference resolution remains unqualified.',
        scope='Saved-state numerical/accounting audit only. No new native solve, training, radial update, coupled map, coefficient fitting, physical-accuracy admission, or shared-runtime promotion.',
        original_controller_classification_changed=False,original_scientific_thresholds_changed=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    print(json.dumps(dict(declaration=base.pin(OUT / 'declaration.json'),status='PREDECLARED_READ_ONLY_AUDIT_NO_NATIVE_RETRY'),indent=2))


def check(expected):
    base.require_file(OUT / 'declaration.json',expected)
    declaration=json.loads((OUT / 'declaration.json').read_text())
    for name,sha in declaration['files'].items():base.require_file(Path(name),sha)
    verified_control()
    return declaration


def saved_group_scalars(folder,production):
    import numpy as np
    with base._open_xsm(folder / 'track.xsm') as tr:
        keys=base.field(tr,tr.root,'KEYFLX','<i4')
        state=base.field(tr,tr.root,'STATE-VECTOR','<i4')
        if len(keys)!=96 or len(set(keys.tolist()))!=96 or state[1]!=456 or np.any(keys<1) or np.any(keys>state[10]):
            raise ValueError('complete declared scalar-key mapping required')
    with base._open_xsm(folder / 'axial.xsm') as a:
        k=base.field(a,a.root,'SPOT-KEFF64','<f8');tag=base.field(a,a.root,'SPOT-X-KEFF','<f8')
        if k.shape!=(1,) or not np.array_equal(k,tag) or k[0]!=float(production['summary']['k64']) or k[0]<=0:
            raise ValueError('saved REAL64 eigenvalue authority differs')
        values=[]
        for item in base.list_handles(a,a.root,'FLUX64',370):
            if item[1:]!=(912,4):raise ValueError('incomplete authoritative REAL64 group field')
            values.append(np.frombuffer(a.read(item[0],item[1]),'<f8')[keys-1])
    array=np.asarray(values,float)
    if array.shape!=(370,96) or not np.isfinite(array).all() or np.any(array<=0):
        raise ValueError('nonpositive/nonfinite/incomplete group scalars')
    return float(k[0]),array/production['exporter_denominator'],float(array.min())


def child(expected):
    declaration=check(expected)
    import numpy as np
    rules=json.loads((CE / 'balance_symmetry_rules.json').read_text())
    info,_=base.prepared()
    if rules!=balance.predeclared_rules(Path(info['case_spec']['path'])):raise ValueError('unchanged original rules required')
    prior=json.loads((control.OUT / 'result.json').read_text())
    stats=json.loads((CE / 'AAA/statistics.json').read_text())
    contract=json.loads((CE / 'AAA/reference_contract.json').read_text())
    keys=[(r,z) for r in range(1,9) for z in range(1,13)]
    mapped={key:[] for key in keys}
    for row in contract['region_layer_bins']:mapped[(row['region'],row['production_axial_cell'])].append(row)
    if any(len(rows)!=1 for rows in mapped.values()):raise ValueError('nonunique original reference bins')
    volumes=np.array([mapped[key][0]['volume_cm3'] for key in keys])
    fuel=np.array([key[0] in (4,5,6,7) for key in keys])
    references=(np.asarray(stats['reference_flux']),np.asarray(stats['reference_nufission_fraction']))
    states={};arrays={}
    for case in ('off','on'):
        folder=control.OUT / case
        p=balance.read_production(folder / 'observables.regions.csv',folder / 'observables.faces.csv',folder / 'observables.summary.txt',rules)
        result=balance.evaluate_production(p,rules)
        if any(value!='PASS' for value in result['checks'].values()):raise ValueError('saved state fails unchanged original current rules: '+case)
        k,array,minimum=saved_group_scalars(folder,p)
        arrays[case]=array
        production=statistics.normalized_observables(p['rates'].reshape(96,2),p['volumes'].reshape(96))[:2]
        point=statistics.discrepancy(references,production,volumes,fuel)
        states[case]=dict(k64=k,saved_group_scalar_entries=int(array.size),minimum_group_scalar_flux=minimum,
            current_checks=result['checks'],accounting=result['accounting'],symmetry=result['symmetry'],
            escape_per_nufission=result['total_escape_per_nufission'],
            sample_mean_reference_discrepancies=point.tolist(),
            sample_mean_reactivity_difference_pcm=1e5*(1/stats['k']['reference']-1/k),
            reference_statistical_classification=stats['classification'],reference_accuracy_qualified=False)
    old_off=json.loads((control.OUT / 'off_compatibility.json').read_text())
    if old_off['status']!='PASS_ORIGINAL_INNER_PRECISION' or old_off['max_relative_scalar_group_flux']!=0 or old_off['relative_k']!=0:
        raise ValueError('exact OFF compatibility receipt required')
    if prior['native_application']['groups']!=370 or prior['tracking_copy']['new_records']!=2 or prior['compiled_kernel']['negative_controls_rejected']!=7:
        raise ValueError('all native integration controls required')
    result=dict(classification='PASS_SAVED_COLD_STATES_AT_ORIGINAL_ACCOUNTING_RULES_ONLY',
        original_controller_classification=prior['classification'],original_controller_error=prior['error'],
        original_controller_rejection_preserved=True,original_scientific_thresholds_changed=False,
        unchanged_rules_implementation=base.pin(Path(balance.__file__)),original_rules=base.pin(CE / 'balance_symmetry_rules.json'),
        states=states,on_vs_off=dict(reactivity_difference_pcm=1e5*(1/states['off']['k64']-1/states['on']['k64']),
            max_relative_global_normalized_group_scalar_change=float(np.max(abs(arrays['on']/arrays['off']-1)))),
        saved_states_audited=['off','on'],native_run_repeated=False,new_coupled_map=False,
        AAA_accuracy_qualified=False,ABA_admitted=False,shared_solver_promoted=False,
        scope=declaration['scope'])
    base.write_new(OUT / 'result.json',result)
    print('AXMAT-WHITE-SAVED-ACCOUNTING-AUDIT-COMPLETE')


def run(expected):
    declaration=check(expected)
    if (OUT / 'run_claim.json').exists():raise ValueError('no repeat or retry')
    base.write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    resources=base.DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    runner=base.SerialExecutor(OUT,90,'AAA',resources)
    runner.execute(OUT / 'AAA','accounting',[sys.executable,str(Path(__file__).resolve()),'child','--sha256',expected],90,'AXMAT-WHITE-SAVED-ACCOUNTING-AUDIT-COMPLETE')
    for name,sha in declaration['files'].items():base.require_file(Path(name),sha)
    base.write_new(OUT / 'driver_result.json',dict(status='COMPLETE_BOUNDED_READ_ONLY_ORIGINAL_ACCOUNTING_AUDIT',
        declaration_sha256=expected,result=base.pin(OUT / 'result.json'),resources=resources.check(),native_solve_repeated=False,
        original_controller_rejection_preserved=True,AAA_accuracy_qualified=False))
    print(json.dumps(dict(result=base.pin(OUT / 'result.json'),status='COMPLETE_READ_ONLY_AUDIT_NO_NATIVE_RETRY'),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run','child'));parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else (run(args.sha256) if args.action=='run' else child(args.sha256))
