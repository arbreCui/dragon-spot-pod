"""Compose the sealed physical-input audit with actual new archive/track records."""
import json
from pathlib import Path
import struct

from qualified_snapshot_ingestion import descriptor, digest, list_handles
from snapshot_control_preflight import _open_xsm

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'


def scalar(a,d,name):
    e=d[name]
    if e[2] not in (1,2,3,4) or e[1] <= 0:
        raise ValueError('invalid scalar data record '+name)
    return e[1:],a.read(e[0],e[1])


def archived_objects(a,name,count):
    handles=list_handles(a,a.root,name,count)
    if any(h[1:] != (-1,0) for h in handles):
        raise ValueError('archive object directory required')
    return [a.directory(h[0]) for h in handles]


def review():
    tools=ART/'axial-material-tools-20261003'
    previous=tools/'input_equivalence_rank1_AAA.json'
    receipt=json.loads((tools/'input_equivalence_rank1_AAA_receipt.json').read_text())
    for path,wanted in receipt['files'].items():
        if digest(path)!=wanted:raise ValueError('sealed physical-input review changed')
    old=json.loads(previous.read_text())
    if old['status']!='PASS':raise ValueError('prior physical input review is not PASS')
    for path,wanted in old['input_sha256'].items():
        if digest(path)!=wanted:raise ValueError('original physical proof input changed: '+path)
    prod=ART/'axial-material-production-qualified-AB-20261004'
    info=json.loads((prod/'prepared.json').read_text())
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    oldspec=json.loads((ROOT/'validation/axial_material/case_spec_rank1_sensitivity.json').read_text())
    for key in ('geometry','materials','cases','reference'):
        if spec[key]!=oldspec[key]:raise ValueError('physical/reference definitions changed: '+key)
    tracked=descriptor(prod/'AAA/bootstrap/initial_axial_track.xsm')
    original=ART/'axial-material-production-rank1-20261003/AAA/bootstrap/initial_axial_track.xsm'
    records={}
    with _open_xsm(tracked['path']) as new,_open_xsm(original) as prior:
        for name in ('STATE-VECTOR','MAT1D','MATCOD','KEYFLX','AREA2D','VOL1D','VOLUME',
                     'NCODE','ICODE','ZCODE','U','W','PL','KEYFLX$ANIS'):
            value=scalar(new,new.root,name)
            if value!=scalar(prior,prior.root,name):raise ValueError('actual new axial input differs: '+name)
            records[name]=dict(length_words=value[0][0],type=value[0][1],
                sha256=__import__('hashlib').sha256(value[1]).hexdigest())
    archive=prod/'archives/aaa_snapshots.xsm'
    original_snapshot=ART/'axial-material-inputs-20261003/A/snapshot_A.xsm'
    checked_material=('ISOTOPERNAME','ISOTOPESMIX','ISOTOPESDENS','ISOTOPESTEMP','ISOTOPESUSED','ISOTOPESVOL','MIXTURESVOL','ENERGY')
    with _open_xsm(archive) as new,_open_xsm(original_snapshot) as prior:
        for obj,names in (('MICROLIB2',checked_material),('TRACK',('MATCOD','KEYFLX','VOLUME','NZON$MCCG','V$MCCG','ZMU$MCCG','WZMU$MCCG','XMU$MCCG'))):
            original_object=prior.object(obj)
            for slot,item in enumerate(archived_objects(new,obj,3),1):
                for name in names:
                    if scalar(new,item,name)!=scalar(prior,original_object,name):
                        raise ValueError(f'actual AAA archive input differs: {obj}/{slot}/{name}')
    ce=ART/'axial-material-ce-rank1-20261003/AAA'
    return dict(schema_version=1,status='PASS',experiment_id=info['experiment_id'],case='AAA',
        case_spec_sha256=info['case_spec']['sha256'],previous_physical_audit=descriptor(previous),
        previous_sealed_audit_inputs_reverified=len(old['input_sha256']),
        actual_axial_track=tracked,actual_track_record_identity=records,
        actual_archive=descriptor(archive),material_records_exact_to_original_in_all_AAA_slots=list(checked_material),
        CE_inputs={p.name:descriptor(p) for p in ce.iterdir() if p.is_file()},
        original_density_formula_and_XML_audit_reused_by_identity=True,
        limits=['Physical input mapping only; no coupled terminal, source-history, CE accuracy or neutron-balance claim.',
                'AAA actual records checked. ABA actual native input remains pending.'])


if __name__=='__main__':
    out=ART/'axial-material-qualified-AB-admission-v2-20261004/input_equivalence_AAA.json'
    result=review()
    with out.open('x') as stream:json.dump(result,stream,indent=2)
    print(result['status'])
