"""Only launch ABA after actual full AAA accuracy qualification.

The separately frozen control program changes the history-storage resource
constructor and ABA reporting only. Native inputs, inner/outer gates, common
basis, per-case wall/map bounds and the actual qualification guard stay frozen.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot')
PROD=ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-20261004'
PREPARED_SHA='88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
sys.path.insert(0,str(PROD/'runtime'))
import production_runner as base


def load(declaration,expected):
    declaration=base.require_file(Path(declaration),expected)
    d=json.loads(declaration.read_text())
    if d.get('schema')!='AXMAT_ABA_ONLY_FROZEN_STORAGE_EXECUTION_V1' or d.get('case')!='ABA':
        raise base.Refusal('explicit ABA-only storage execution declaration required')
    for name,wanted in d['files'].items():base.require_file(Path(name),wanted)
    if d['files'].get(str(Path(__file__).resolve()))!=base.sha256(Path(__file__).resolve()):
        raise base.Refusal('actual entry point is not frozen')
    info=base.verify_prepared(PROD/'prepared.json',PREPARED_SHA)
    if d['production_prepared']!={'path':str(PROD/'prepared.json'),'sha256':PREPARED_SHA}:
        raise base.Refusal('declaration does not bind the original frozen prepared study')
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    if spec['resource_caps']['new_case_artifact_budget_GiB']!=40 or d['old_sealed_history_budget_GiB']!=40 or d['ABA_history_budget_GiB']!=64:
        raise base.Refusal('storage-only 40 to 64 GiB addendum required')
    if d['per_case_wall_seconds']!=info['budgets']['total_seconds'] or d['max_maps']!=info['budgets']['max_maps']:
        raise base.Refusal('original wall/map caps must remain unchanged')
    resource=base.DiskResources(base.ARTIFACTS_ROOT,d['resource_roots'],8*2**30,64*2**30)
    snapshot=resource.check()
    path=Path(d['control_program']['path'])
    # Import its matching input generator from the copied immutable directory.
    specmod=importlib.util.spec_from_file_location('aba_storage_only_control',path)
    module=importlib.util.module_from_spec(specmod)
    sys.modules[specmod.name]=module;specmod.loader.exec_module(module)
    return d,info,module,snapshot


def reference_ready(d,info,qualification,expected):
    if qualification is None or expected is None:raise base.Refusal('explicit actual AAA qualified receipt and SHA256 required')
    if Path(qualification).resolve()!=Path(d['required_qualification']).resolve():
        raise base.Refusal('only the frozen full precision reference can qualify this ABA attempt')
    base.qualify_aba(info,PROD,PREPARED_SHA,Path(qualification),expected)
    case=Path(d['reference_case'])
    result_path=case/'native_result.json'
    if not result_path.is_file():raise base.Refusal('native reference is not terminal; ABA cannot start alongside it')
    native=json.loads(result_path.read_text())
    if native.get('status')!='NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS' or native.get('returncode')!=0 or native.get('error') is not None:
        raise base.Refusal('normal terminal independent native reference required')
    base.require_file(case/'openmc.log',native['log_sha256'])
    for name,wanted in native['outputs'].items():base.require_file(case/name,wanted)
    receipt=json.loads(Path(qualification).read_text())
    if receipt['CE_execution']!=d['reference_execution'] or receipt['CE_native_result']!={'path':str(result_path),'sha256':base.sha256(result_path)}:
        raise base.Refusal('qualified receipt does not bind the actual terminal independent run')
    analysis=json.loads((case/'analysis_result.json').read_text())
    if analysis['classification']!='COMPLETE_REFERENCE_ANALYSIS' or analysis['AAA_classification']!='AAA_REFERENCE_QUALIFIED' or analysis['ABA_admitted'] is not True:
        raise base.Refusal('complete independently collected eight-gate qualification required')
    stats=json.loads(Path(receipt['evidence']['statistics']['path']).read_text())
    identities=stats['statepoint_identities']
    expected_paths=[str(case/f'statepoint.{batch:04d}.h5') for batch in range(101,2101)]
    if [i['path'] for i in identities]!=expected_paths:
        raise base.Refusal('all 2000 consecutive full precision statepoints required')
    for item in identities:base.require_file(Path(item['path']),item['sha256'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['preflight','run']);p.add_argument('declaration',type=Path);p.add_argument('--sha256',required=True)
    p.add_argument('--reference-qualification',type=Path);p.add_argument('--reference-sha256')
    a=p.parse_args();d,info,control,snapshot=load(a.declaration,a.sha256)
    if a.action=='preflight':
        # This is resource/input readiness only. It cannot create a native claim.
        print(json.dumps(dict(status='STORAGE_INPUTS_READY_AAA_ACCURACY_PENDING',new_transport_launched=False,ABA_admitted=False,
            artifact_bytes=snapshot['artifact_bytes'],artifact_budget_bytes=snapshot['artifact_budget_bytes'],disk_free_bytes=snapshot['disk_free_bytes'])))
        return
    reference_ready(d,info,a.reference_qualification,a.reference_sha256)
    out=a.declaration.resolve().parent
    with (out/'execution_claim.json').open('x') as f:json.dump(dict(declaration_sha256=a.sha256,started_unix=time.time(),case='ABA',retries=0),f,indent=2)
    control.run(PROD/'prepared.json',PREPARED_SHA,'ABA',a.reference_qualification,a.reference_sha256)


if __name__=='__main__':main()
