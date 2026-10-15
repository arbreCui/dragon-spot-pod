"""Stage independently defined ABA XML while actual AAA accuracy is pending.

Copies the already audited physical model exactly, with an explicit sampling
addendum. Packed initial material/geometry records are independently checked.
No native child, measurement admission, qualification or ABA track is created.
"""
import copy
import json
from pathlib import Path
import shutil
import sys
import time
import xml.etree.ElementTree as ET

sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
PROD=ART/'axial-material-production-qualified-AB-white-trace-20261004'
PARENT=ART/'axial-material-ce-qualified-AB-compensated-20261004/ABA'
OUT=ART/'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004/aba_reference_inputs'
PREPARED_SHA='88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
sys.path.insert(0,str(PROD/'runtime'))
from production_runner import verify_prepared,verify_sealed_directory,require_file,sha256,DiskResources
from qualified_snapshot_ingestion import list_handles
from snapshot_control_preflight import _open_xsm


def pin(p):p=Path(p).resolve();return dict(path=str(p),sha256=sha256(p))


def write_new(p,d):
    with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')


def xml_value(n):
    return n.tag,tuple(sorted(n.attrib.items())),(n.text or '').strip(),tuple(xml_value(c) for c in n)


def main():
    info=verify_prepared(PROD/'prepared.json',PREPARED_SHA)
    if (PROD/'ABA').exists():raise ValueError('ABA already claimed; this is initial-input preparation only')
    verify_sealed_directory(PROD/'archives')
    prior_path=ART/'axial-material-tools-20261003/input_equivalence.json'
    prior=json.loads(prior_path.read_text())
    if prior['status']!='PHYSICAL_INPUT_DEFINITION_AND_CE_MAPPING_CHECKED_PENDING_SPOT_AXIAL_RECORDS':
        raise ValueError('original physical-input-only proof scope differs')
    for name,wanted in prior['input_sha256'].items():require_file(Path(name),wanted)
    physical=prior['cases']['ABA']
    if physical['composition_by_physical_zone']!=list('ABA') or physical['white_side_surfaces']!=6 or physical['axial_end_vacuum_planes']!=[0,150]:
        raise ValueError('original physical ABA boundary/material mapping differs')
    archive=PROD/'archives/aba_snapshots.xsm';records=[]
    sources=[]
    with _open_xsm(archive) as new:
        for owner,keys in [('MICROLIB2',('ISOTOPERNAME','ISOTOPESMIX','ISOTOPESDENS','ISOTOPESTEMP','ISOTOPESUSED','ISOTOPESVOL','MIXTURESVOL','ENERGY')),
            ('TRACK',('MATCOD','KEYFLX','VOLUME','NZON$MCCG','V$MCCG','ZMU$MCCG','WZMU$MCCG','XMU$MCCG'))]:
            handles=list_handles(new,new.root,owner,3)
            for slot,state in enumerate('ABA',1):
                if handles[slot-1][1:]!=(-1,0):raise ValueError('packed source archive directory required')
                actual=new.directory(handles[slot-1][0]);path=ART/'axial-material-inputs-20261003'/state/f'snapshot_{state}.xsm';sources.append(path)
                with _open_xsm(path) as old:
                    previous=old.object(owner)
                    for name in keys:
                        a,b=actual[name],previous[name]
                        if a[1:]!=b[1:] or new.read(a[0],a[1])!=old.read(b[0],b[1]):raise ValueError(f'initial {owner}/{slot}/{state}/{name} differs')
                        records.append(dict(owner=owner,slot=slot,composition=state,record=name,record_words=a[1],record_type=a[2],exact=True))
    for name in ('materials.xml','geometry.xml','tallies.xml'):
        original=ART/'axial-material-ce-v2-20261003/ABA'/name
        if sha256(PARENT/name)!=sha256(original):raise ValueError('audited physical XML identity differs: '+name)
    original_contract=json.loads((PARENT/'reference_contract.json').read_text())
    if original_contract['case']!='ABA' or original_contract['schema']!='AXMAT_CE_INPUT_V2':raise ValueError('signed polar ABA contract required')
    if any(row['composition']!='ABA'[row['physical_zone']-1] for row in original_contract['region_layer_bins']):raise ValueError('region/layer composition mapping differs')
    settings=ET.parse(PARENT/'settings.xml');node=settings.getroot()
    if int(node.findtext('seed'))!=310033 or int(node.findtext('inactive'))!=100:raise ValueError('original ABA sampling seed/inactive differs')
    OUT.mkdir(exist_ok=False)
    for name in ('materials.xml','geometry.xml','tallies.xml'):shutil.copy2(PARENT/name,OUT/name)
    node.find('particles').text='10000';node.find('generations_per_batch').text='10';node.find('batches').text='2100'
    node.find('state_point/batches').text=' '.join(map(str,range(101,2101)))
    ET.indent(settings,space='  ');settings.write(OUT/'settings.xml',encoding='UTF-8',xml_declaration=True)
    previous=ET.parse(PARENT/'settings.xml').getroot();actual=ET.parse(OUT/'settings.xml').getroot()
    for name in ('particles','generations_per_batch','batches'):actual.find(name).text=previous.findtext(name)
    actual.find('state_point/batches').text=previous.findtext('state_point/batches')
    if xml_value(previous)!=xml_value(actual):raise ValueError('undeclared settings/source change')
    contract=copy.deepcopy(original_contract)
    contract['config'].update(particles=10000,generations_per_batch=10,particles_per_batch=100000,active=2000)
    contract['statepoint_batches']=list(range(101,2101))
    contract['input_hashes']={name:sha256(OUT/name) for name in ('materials.xml','geometry.xml','tallies.xml','settings.xml')}
    contract['sampling_addendum']=str(OUT/'declaration.json')
    contract['source_history_policy']='Original independently defined initial source and seed 310033; no imported bank or SPOT feedback. All 21000 native generations retained, with ten successive generations per declared batch.'
    write_new(OUT/'reference_contract.json',contract)
    write_new(OUT/'initial_archive_review.json',dict(status='PASS_48_INITIAL_ABA_MATERIAL_AND_GEOMETRY_RECORDS_EXACT',case='ABA',archive=pin(archive),records=records,
        original_physical_definition=pin(prior_path),actual_coupled_ABA_track_produced=False,native_transport_started=False,independent_accuracy_qualified=False))
    paths=[Path(__file__).resolve(),PROD/'prepared.json',PROD/'archives/result.json',archive,prior_path,Path(info['case_spec']['path']),PARENT/'reference_contract.json',
        *[PARENT/name for name in ('materials.xml','geometry.xml','tallies.xml','settings.xml')],*sources,
        PROD/'runtime/snapshot_control_preflight.py',PROD/'runtime/qualified_snapshot_ingestion.py',
        *[OUT/name for name in ('materials.xml','geometry.xml','tallies.xml','settings.xml','reference_contract.json','initial_archive_review.json')]]
    roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    resources=DiskResources(ART,roots,8*2**30,40*2**30).check()
    write_new(OUT/'declaration.json',dict(schema='AXMAT_ABA_INDEPENDENT_REFERENCE_INPUT_STAGING_V1',declared_unix=time.time(),case='ABA',
        status='PHYSICAL_INPUTS_STAGED_PENDING_ACTUAL_AAA_ACCURACY_AND_ABA_FIXED_POINT',files={str(p.resolve()):sha256(p) for p in paths},
        inherited_physical_source_pins=prior['input_sha256'],case_spec=info['case_spec'],production_prepared=pin(PROD/'prepared.json'),
        original_density_formula_and_XML_proof_reused_by_exact_identity=True,physical_tally_XML_bytes_unchanged=True,all_other_settings_source_seed_entropy_and_temperature_unchanged=True,
        sampling=dict(particles_per_generation=10000,generations_per_batch=10,inactive_batches=100,active_batches=2000,total_histories=210000000,seed=310033),
        planning_wall_seconds=64800,planning_history_budget_GiB=64,old_sealed_caps_changed=False,
        engineering_and_statistical_numerical_thresholds_changed=False,native_transport_started=False,ABA_admitted=False,
        required_next_evidence=['actual full eight-gate AAA reference qualification','fresh actual coupled ABA tracking/input equivalence','actual ABA fixed point and original saved-state checks','fully bound original-threshold native CE execution and analysis declarations'],
        resource_snapshot_before_staging_seal=resources))
    print(json.dumps(dict(status='ABA_PHYSICAL_INPUTS_STAGED_NO_TRANSPORT',declaration=pin(OUT/'declaration.json'),initial_archive_review=pin(OUT/'initial_archive_review.json')),indent=2))


if __name__=='__main__':main()
