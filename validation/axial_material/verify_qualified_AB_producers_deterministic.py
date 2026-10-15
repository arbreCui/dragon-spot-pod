"""Read-only replay of the A/B offline producer and explicit BOOT admission."""
import argparse
import copy
import json
from pathlib import Path

from qualified_snapshot_ingestion_deterministic import admit_snapshots,descriptor,digest

ROOT=Path('/Users/wen/spot')


def verify():
    work=ROOT/'validation/artifacts/axial-material-qualified-AB-admission-v2-20261004'
    declaration=json.loads((work/'declaration.json').read_text())
    for item in declaration['inputs'].values():
        if digest(item['path'])!=item['sha256']:raise ValueError('declared input changed')
    spec=json.loads((work/'case_spec.json').read_text())
    receipts=json.loads((work/'producer_ingestion_receipt.json').read_text())
    positive=admit_snapshots(receipts,declaration['inputs'],spec)
    negatives={}
    for name,changes in (
        ('wrong_producer',{'producer_runtime':dict(receipts['producer_runtime'],sha256='0'*64)}),
        ('false_direct_r64_ingress',{'offline_r64_directly_consumed_by_boot':True}),
        ('wrong_receiver',{'online_receiver_sha256':'0'*64}),
        ('unbound_manifest',{'inputs_manifest_sha256':'0'*64})):
        candidate=copy.deepcopy(receipts);candidate.update(changes)
        try:admit_snapshots(candidate,declaration['inputs'],spec)
        except (ValueError,OSError) as error:negatives[name]=dict(rejected=True,error=str(error))
        else:raise ValueError('bad provenance admitted: '+name)
    from qualified_snapshot_ingestion_deterministic import audit_payload
    try:audit_payload(work/'negative_archive_mirror.xsm')
    except ValueError as error:negatives['inexact_legacy_mirror']=dict(rejected=True,error=str(error))
    else:raise ValueError('inexact BOOT mirror admitted')
    if negatives!=json.loads((work/'ingestion_negative_controls.json').read_text())['controls']:
        raise ValueError('receipt rejection evidence differs')
    prior=ROOT/'validation/artifacts/axial-material-r64-A-qualified-20261003/result.sha256'
    if digest(prior)!='74fbca143d0a4909e21e40a4ec9227990e6c6f13956f595e17bc94ed010868bf':
        raise ValueError('A qualification seal changed')
    for line in prior.read_text().splitlines():
        wanted,name=line.split('  ',1)
        if digest(prior.parent/name)!=wanted:raise ValueError('A sealed closeout changed')
    return dict(classification='QUALIFIED_OFFLINE_AB_EXPLICIT_LEGACY_BOOT_ADMISSION_VERIFIED',
        snapshot_A_binary64_qualified=True,snapshot_B_binary64_qualified=True,
        producer_admission=positive,ingestion_negative_controls=negatives,
        producer_receipt=descriptor(work/'producer_ingestion_receipt.json'),
        B_audit_status=receipts['states']['B']['audit_status'],
        B_snapshot=receipts['states']['B']['archive'],
        production_qualified=False,aaa_qualified=False,aba_started=False,new_ce_accuracy_accepted=False,
        scope='Offline A/B state and producer eligibility only. Explicit receiver BOOT promotes REAL32 mirrors once; coupled solver must establish its own REAL64 authorities and all original gates.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    result=verify()
    if args.output:
        with args.output.open('x') as stream:json.dump(result,stream,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('producer_admission','ingestion_negative_controls')},indent=2))
