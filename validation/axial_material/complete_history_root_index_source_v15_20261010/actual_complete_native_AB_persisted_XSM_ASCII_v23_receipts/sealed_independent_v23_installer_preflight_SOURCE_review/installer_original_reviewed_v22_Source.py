import argparse,hashlib,importlib.util,json,os,shutil,sys
from pathlib import Path
ROOT=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SOURCE=Path('/private/tmp/axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf')
WRITER=Path('/private/tmp/spot_v22_native_postclose_META_ROOT_v2.py')
WRITER_SHA='dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--peer-manifest',required=True);ap.add_argument('--peer-manifest-sha256',required=True);ap.add_argument('--peer-seal-receipt',required=True);ap.add_argument('--metadata-source-peer-report',required=True);ap.add_argument('--metadata-source-peer-report-sha256',required=True)
    a=ap.parse_args();assert hashlib.sha256(WRITER.read_bytes()).hexdigest()==WRITER_SHA
    spec=importlib.util.spec_from_file_location('Root_native_metadata_functions_only',WRITER);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    assert not any(os.path.lexists(p) for p in (m.D,m.H,m.O,m.C)) and m.E.is_dir()
    manifest,mp=m.read(SOURCE/'Root_actual_complete_bound_native_SOURCE_manifest.json','bce973287d8776ddcfca502494f9f9dff0113d653aa316666ebfa962a4ea74d9')
    original=m.snapshot(SOURCE);assert set(original['files'])==set(manifest['members'])|{'Root_actual_complete_bound_native_SOURCE_manifest.json'} and len(original['files'])==89
    for k,q in manifest['members'].items():assert original['files'][k]==q
    peer_path=Path(a.peer_manifest);sealed,sp=m.read(peer_path,a.peer_manifest_sha256);peer=m.snapshot(peer_path.parent)
    members=sealed['members']
    if type(members) is list:members={(q['relative_path'] if 'relative_path' in q else str(Path(q['path']).relative_to(peer_path.parent))):q for q in members}
    assert set(peer['files'])==set(members)|{peer_path.name}
    for k,q in members.items():assert {key:peer['files'][k][key] for key in ('path','sha256','size_bytes','identity')}=={key:q[key] for key in ('path','sha256','size_bytes','identity')}
    review,rp=m.read(peer_path.parent/'REVIEW.json');assert review['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY' and review['all_checks_typed_true'] is True and review['blockers']==[]
    for field,path in [('actual_bound_Source_manifest_pin',SOURCE/'Root_actual_complete_bound_native_SOURCE_manifest.json'),('actual_binding_pin',SOURCE/'Root_actual_native_SOURCE_binding.json'),('actual_host_pin',SOURCE/'Root_bound_complete_native_genuine_host.py'),('actual_checker_pin',SOURCE/'Root_bound_complete_native_checker.py'),('actual_Root_binding_tool_receipt_pin',m.E/'Root_actual_complete_native_Source_binding_tool_return.json')]:assert review[field]==m.pin(path)
    seal,sealpin=m.read(Path(a.peer_seal_receipt));tr=seal.get('actual_tool_return',seal.get('terminal_tool_return'));assert seal['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    meta_review,mrp=m.read(Path(a.metadata_source_peer_report),a.metadata_source_peer_report_sha256)
    assert meta_review['status']=='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY' and meta_review['all_checks_typed_true'] is True and meta_review['blockers']==[] and meta_review['writer_pin']==m.pin(WRITER)
    meta_peer=m.snapshot(Path(a.metadata_source_peer_report).parent)
    before_E=m.snapshot(m.E);m.D.mkdir()
    def copy_view(view,prefix):
        for k,q in view['files'].items():
            p=m.D/prefix/k;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q['path'],p)
            assert m.pin(p)['sha256']==q['sha256'] and m.pin(p)['size_bytes']==q['size_bytes']
        assert m.snapshot(Path(view['root']))==view
    copy_view(original,Path('.'));copy_view(peer,Path('sealed_independent_actual_bound_native_SOURCE_review'));copy_view(meta_peer,Path('sealed_independent_postclose_META_SOURCE_review'));copy_view(before_E,Path('complete_original_E_receipts_before_install'))
    for path,name in [(WRITER,'Root_native_postclose_META_writer.py'),(Path(__file__),'Root_native_Source_installer.py'),(Path(a.peer_seal_receipt),'actual_bound_native_Source_peer_seal_tool_return.json')]:
        p=m.pin(path);shutil.copyfile(path,m.D/name);assert m.pin(m.D/name)['sha256']==p['sha256']
    m.write(m.D/'Root_actual_complete_native_Source_install_record.json',dict(schema='ROOT_V22_COMPLETE_NATIVE_SOURCE_INSTALL_RECORD_V1',source_only=True,actual_bound_Source=mp,actual_bound_Source_peer=rp,actual_Source_peer_seal=sealpin,postclose_META_Source_peer=mrp,original_complete_bound_Source=original,complete_original_E_before_install=before_E,all_original_input_pins_preserved_129=True,no_native_or_guard_or_numeric_executed=True,actual_native_byte_qualification_sha256=None,scientific_accuracy_qualified=False))
    frozen=m.snapshot(m.D);assert m.snapshot(m.E)==before_E
    f=m.E/'Root_complete_native_D_source_freeze.json';m.write(f,dict(schema='ROOT_V22_COMPLETE_NATIVE_D_SOURCE_FREEZE_V1',complete_D=frozen,no_D_append_after_freeze=True,actual_native_not_executed=True))
    print(json.dumps(dict(status='COMPLETE_NATIVE_SOURCE_INSTALLED_FROZEN_NOT_RUN',D_files=len(frozen['files']),D_directories=len(frozen['directories']),D_freeze=m.pin(f),host=m.pin(m.D/'Root_bound_complete_native_genuine_host.py'),writer=m.pin(m.D/'Root_native_postclose_META_writer.py'),E_original_unchanged=True,native_executed=False)))
if __name__=='__main__':main()
