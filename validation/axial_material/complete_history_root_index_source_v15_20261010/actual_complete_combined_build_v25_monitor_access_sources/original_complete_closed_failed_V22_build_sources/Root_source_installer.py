import argparse, hashlib, json, os, shutil, stat
from pathlib import Path

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
D=B/'actual_complete_combined_build_v22_sources'
E=B/'actual_complete_combined_build_v22_receipts'
PRE=B/'actual_complete_combined_prepare_v22_receipts'
OLD_D=B/'actual_complete_combined_build_v21_sources'
OLD_FREEZE=B/'actual_complete_combined_build_v21_receipts/Root_prelaunch_complete_build_source_freeze.json'
BOUND=Path('/private/tmp/axmat_v22_actual_full_build_READY_SOURCE_root_20261010_b8ad01')
META=Path('/private/tmp/spot_v22_complete_build_postclose_META_ROOT_SOURCE_20261010_6ed606')
HOST=ART/'axial-material-complete-combined-build-host-v22-20261010'
OUT=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py'
def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p); i=identity(p)
    assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def exact(q):
    p=pin(q['path']); assert {k:p[k] for k in q}==q,q['path'];return p
def load(p,sha=None):
    q=pin(p)
    if sha is not None:assert q['sha256']==sha
    d=json.loads(Path(p).read_text());assert pin(p)==q;return d,q
def snapshot(root):
    assert root.is_dir() and not root.is_symlink()
    files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink()
        key=str(p.relative_to(root));i=identity(p)
        if stat.S_ISREG(i[2]):files[key]=pin(p)
        else:assert stat.S_ISDIR(i[2]);dirs[key]=i
    for key,q in files.items():assert pin(root/key)==q
    for key,q in dirs.items():assert identity(root/key)==q
    return dict(root=str(root),files=files,directories=dirs,symlinks={})
def complete_package(root,name,sha):
    m,mp=load(root/name,sha);members=m['members']
    if type(members) is list:
        members={(q['relative_path'] if 'relative_path' in q else str(Path(q['path']).relative_to(root))):q for q in members}
    assert type(members) is dict and len(members)==m['member_count']
    view=snapshot(root);assert set(view['files'])==set(members)|{name}
    for key,q in members.items():assert Path(q['path'])==root/key;exact(q)
    return m,view
def save(p,d):
    with p.open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def copy_view(view,prefix):
    for name,q in view['files'].items():
        target=D/prefix/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(q['path'],target)
        assert pin(target)['sha256']==q['sha256'] and pin(target)['size_bytes']==q['size_bytes']
    for name in view['directories']:
        if name!='.':(D/prefix/name).mkdir(parents=True,exist_ok=True)
    assert snapshot(Path(view['root']))==view
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--peer-manifest',required=True);ap.add_argument('--peer-manifest-sha256',required=True);ap.add_argument('--peer-seal-receipt',required=True)
    a=ap.parse_args();peer_path=Path(a.peer_manifest);peer_root=peer_path.parent
    assert not any(os.path.lexists(p) for p in (D,E,HOST))
    oldfreeze,oldfreeze_pin=load(OLD_FREEZE);old=snapshot(OLD_D)
    assert oldfreeze['schema']=='ROOT_V21_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1'
    assert old['files']==oldfreeze['complete_files'] and old['directories']==oldfreeze['complete_directories']
    assert len(old['files'])==30 and len(old['directories'])==3
    _,bound=complete_package(BOUND,'MANIFEST.json','c8514275f297ac1344dfd3dd05d3b75a550516ef22ce568e33f4c868ada5bdae')
    _,meta=complete_package(META,'MANIFEST.json','f0a11bc559fc21a04dcea470d4e4eaa321d2f7725745ed9d7c24f012e6ce2998')
    _,peer=complete_package(peer_root,peer_path.name,a.peer_manifest_sha256)
    review,review_pin=load(peer_root/'REVIEW.json')
    assert review['schema']=='INDEPENDENT_V22_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1'
    assert review['status']=='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY'
    assert review['all_checks_typed_true'] is True and type(review['blockers']) is list and not review['blockers']
    for field,path in [('actual_bound_build_host_pin',BOUND/'combined_build_host.py'),('actual_postclose_META_writer_pin',META/'write_actual_build_postclose_META.py'),('actual_Root_Source_binding_tool_receipt_pin',PRE/'Root_actual_v22c_full_build_Source_binding_tool_return.json'),('qualified_actual_bound_Source_manifest_pin',BOUND/'MANIFEST.json'),('qualified_postclose_META_Source_manifest_pin',META/'MANIFEST.json')]:
        assert review[field]==pin(path)
    seal,seal_pin=load(Path(a.peer_seal_receipt));tr=seal.get('actual_tool_return',seal.get('terminal_tool_return'))
    assert seal['closed'] is True and seal['observed_terminal'] is True
    assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    prep_summary,prep_summary_pin=load(PRE/'Root_actual_complete_combined_prepare_summary.json','0b4ef19900921de593d5979283fd65c779a8df857ee1c6204d4e7b7951f4a306')
    prep_peer,prep_peer_pin=load(PRE/'sealed_independent_actual_complete_PREP_saved_META_review/REVIEW.json','678bc8e4a9e1ec795db09e40355991730670bfcb94a72a9204af3b333822f3df')
    assert prep_peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY' and prep_peer['all_checks_typed_true'] is True and prep_peer['blockers']==[]
    ns,ns_pin=load(PRE/'Root_actual_complete_prepare_namespace_manifest.json','b1133e027897d3901aa8133cfbc8c2209ae795c50d05ea069c7db09a736c8d8f')
    prepared=[]
    for saved in ns['namespaces']:
        current=snapshot(Path(saved['root']));assert set(current['files'])==set(saved['files']) and saved['symlinks']=={}
        for q in saved['files'].values():exact(q)
        saved_dirs={q['path']:q['identity'] for q in saved['directories']}
        assert {k:v for k,v in current['directories'].items() if k!='.'}==saved_dirs
        prepared.append(current)
    ph,_=load(Path(prep_summary['actual_host_result']['path']),prep_summary['actual_host_result']['sha256'])
    actual_PREP_inputs=[exact(q) for q in ph['input_sources']+[ph['original_helper'],ph['resource_factory']]]
    assert len(actual_PREP_inputs)==313
    pre=snapshot(PRE)
    assert pin(C)['sha256']=='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'
    assert bound['files']['combined_build_host.py']['sha256']=='cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269'
    assert meta['files']['write_actual_build_postclose_META.py']['sha256']=='d246786b9f02b2b8f8024d2d4b8bf80a0de8e9eb6dff2ba801fd10c1f3d4b5b7'
    for name in ('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','audit/binary_identity.json','audit/result.json','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V22/stages.json','runtime/Dragon'):assert not os.path.lexists(OUT/name)
    assert shutil.disk_usage(R).free-2*2**30>=8*2**30
    D.mkdir();E.mkdir()
    for prefix,view in [('original_complete_V21_build_sources',old),('actual_bound_full_build_SOURCE',bound),('complete_postclose_META_SOURCE',meta),('sealed_independent_actual_bound_build_and_META_SOURCE_review',peer),('complete_actual_PREP_receipts_before_build',pre)]:copy_view(view,prefix)
    for src,name in [(BOUND/'combined_build_host.py','combined_build_host.py'),(META/'write_actual_build_postclose_META.py','write_actual_build_postclose_META.py'),(Path(__file__),'Root_source_installer.py'),(Path('/private/tmp/spot_v22_complete_build_prelaunch_ROOT.py'),'Root_prelaunch_checker.py'),(OLD_FREEZE,'original_V21_complete_source_freeze.byte_exact.json'),(Path(a.peer_seal_receipt),'actual_bound_build_and_META_Source_peer_seal_tool_return.json')]:
        source=pin(src);shutil.copyfile(src,D/name);assert pin(D/name)['sha256']==source['sha256']
    save(D/'Root_complete_SOURCE_install_record.json',dict(schema='ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_INSTALL_V1',status='SOURCE_INSTALLED_NO_ACTUAL_BUILD_YET',original_V21_D_freeze=oldfreeze_pin,complete_original_V21_source=old,complete_actual_bound_source=bound,complete_postclose_META_source=meta,complete_actual_bound_Source_peer=peer,actual_peer_report=review_pin,actual_peer_seal=seal_pin,complete_actual_PREP_E_source=pre,actual_PREP_summary=prep_summary_pin,actual_PREP_peer=prep_peer_pin,actual_PREP_namespace=ns_pin,all313_actual_PREP_fixed_inputs_unchanged=actual_PREP_inputs,all_complete_prepared_namespace_unchanged=True,no_SOURCE_append_after_freeze=True,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    frozen=snapshot(D)
    for view in (old,bound,meta,peer,pre,*prepared):assert snapshot(Path(view['root']))==view
    for q in actual_PREP_inputs:exact(q)
    save(E/'Root_prelaunch_complete_build_source_freeze.json',dict(schema='ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1',source_root=str(D),complete_files=frozen['files'],complete_directories=frozen['directories'],symlinks={},no_SOURCE_append_after_freeze=True,actual_complete_SOURCE_file_count=len(frozen['files'])))
    print(json.dumps(dict(status='COMPLETE_SOURCE_INSTALLED_FROZEN_NO_BUILD_YET',full_Source_files=len(frozen['files']),complete_Source_directories=len(frozen['directories']),host=pin(D/'combined_build_host.py'),writer=pin(D/'write_actual_build_postclose_META.py'),frozen=pin(E/'Root_prelaunch_complete_build_source_freeze.json'),original_V21_D_unchanged=True,actual_PREP_inputs_unchanged=len(actual_PREP_inputs),new_build_or_numeric_executed=False)))
if __name__=='__main__':main()
