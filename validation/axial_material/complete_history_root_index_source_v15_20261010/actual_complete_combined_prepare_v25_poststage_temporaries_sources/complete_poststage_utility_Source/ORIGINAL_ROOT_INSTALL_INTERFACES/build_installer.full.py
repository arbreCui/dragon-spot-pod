import argparse, hashlib, json, os, shutil, stat
from pathlib import Path

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
D=B/'actual_complete_combined_build_v25_monitor_access_sources'
E=B/'actual_complete_combined_build_v25_monitor_access_receipts'
PRE=B/'actual_complete_combined_prepare_v25_monitor_access_receipts'
OLD_D=B/'actual_complete_combined_build_v22_sources'
OLD_FREEZE=B/'actual_complete_combined_build_v22_receipts/Root_prelaunch_complete_build_source_freeze.json'
BOUND=Path('/private/tmp/spot_v25_monitor_access_ACTUAL_READY_BUILD_SOURCE_ROOT_20261010')
HOST=ART/'axial-material-complete-combined-build-host-v25-monitor-access-20261010'
OUT=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py'

PREP_H=ART/'axial-material-complete-combined-prepare-host-v25-monitor-access-20261010'
PREP_D=B/'actual_complete_combined_prepare_v25_monitor_access_sources'
MOTHER=Path('/private/tmp/axmat_v25_monitor_access_complete_BUILD_UNREADY_Source_j8g_s3id')
SAVED_PREP_PEER=Path('/private/tmp/axmat_v25_monitor_access_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_ORIGINAL_STAGE_STORAGE_20261010')
MOTHER_PEER=Path('/private/tmp/spot_ROOT_independent_v25_monitor_access_BUILD_namespace_Source_review_20261010')
MOTHER_SEAL=Path('/private/tmp/spot_ROOT_independent_v25_monitor_access_BUILD_namespace_Source_review_20261010_seal_receipt.json')
BINDING_RECEIPT=B/'Root_actual_monitor_access_V25_full_BUILD_Source_binding_tool_return.json'
OLD_TERMINAL=B/'actual_complete_combined_build_v22_receipts/Root_actual_build_tool_terminal_return.json'
UTILITY=Path('/private/tmp/axmat_v25_monitor_access_complete_installer_prelaunch_UNREADY_Source_9af6cqgv')
MOTHER_SHA='8c99844e51761cbf00013f260d647b34fa34919e8db7b655a4340f11e6c6b4d7'
BOUND_SHA='1a169d0f6676deb535515b620aae9619f4451408a51e93f10c7d308b8f59f8d4'
SAVED_PREP_SHA='df76470aff57f68a81024adece0fc1411f8b6931b491272d0b5f9324c5cd839e'
MOTHER_PEER_SHA='107be533cc8c1b201409e6875ac409cc1ef7a5709b3119f2b47c7566375dbf4b'
SUMMARY_SHA='91994d892cf9f89e97ca0f51e92a50dc59444368d80a457df66c9d728474a891'
NS_SHA='4824dea24bec810e1a7d9456bd3996995d60cda3f35a79e0eaf09499fdecc641'
HOST_SHA='b47fa026c4b9317741c67c35d4a708294c1a5cb7b5a84e18911c908116f14c24'
WRITER_SHA='54d30f415a162e80fa91619489beeb4eb776d7787b66a91fd9d55ec2221baf1a'
C_SHA='643d1b5fcfada4c7ec13f8c5d4c01fb6a77529f51a109d73fac214952f849ef2'
FAMILY='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
OUTPUTS=('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','audit/binary_identity.json','audit/result.json',FAMILY+'/stages.json','runtime/Dragon')
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

def strict_terminal(record,expected):
    assert record['closed'] is True
    tr=record.get('terminal_tool_return',record.get('actual_tool_return',record.get('exec_command_result')))
    assert type(tr) is dict and type(tr['exit_code']) is int and tr['exit_code']==expected and 'session_id' not in tr
    return tr
def full_package(root,sha):
    m,v=complete_package(root,'MANIFEST.json',sha)
    assert m['source_only'] is True and m['directories']==v['directories'] and m['member_count']+1==len(v['files'])
    return m,v
def seal_pair(path,sha,manifest_pin,review_pin):
    s,sp=load(path,sha);tr=strict_terminal(s,0)
    observed=json.loads(tr['output']);assert type(observed) is dict
    assert observed['manifest_pin']==manifest_pin and observed['review_pin']==review_pin
    return sp

def full_PREP(summary):
    ns,nsp=load(PRE/'Root_actual_complete_prepare_namespace_manifest.json',NS_SHA)
    assert {k:nsp[k] for k in summary['namespace_manifest']}==summary['namespace_manifest']
    assert ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1'
    expected=[PREP_H,S,OUT,T,PREP_D]
    assert [Path(v['root']) for v in ns['namespaces']]==expected
    prepared=[]
    for saved in ns['namespaces']:
        v=snapshot(Path(saved['root']));assert saved['symlinks']=={} and set(v['files'])==set(saved['files'])
        for q in saved['files'].values():exact(q)
        assert {k:i for k,i in v['directories'].items() if k!='.'}=={q['path']:q['identity'] for q in saved['directories']}
        prepared.append(v)
    ph,php=load(Path(summary['actual_host_result']['path']),summary['actual_host_result']['sha256']);exact(summary['actual_host_result'])
    assert len(ph['input_sources'])==142
    inputs=[exact(q) for q in ph['input_sources']+[ph['original_helper'],ph['resource_factory']]]
    assert len(inputs)==144 and summary['all_original_pinned_inputs_unchanged_count']==144
    strict_terminal(load(PRE/'Root_actual_prepare_tool_terminal_return.json')[0],0)
    strict_terminal(load(PRE/'Root_actual_prepare_metadata_writer_tool_terminal_return.json')[0],0)
    return ns,nsp,ph,php,inputs,prepared

def counted_bytes(roots,canonical):
    return sum(q['size_bytes'] for root in roots if root.exists() for q in snapshot(root)['files'].values())+pin(canonical)['size_bytes']

def main():
    assert not __import__('sys').flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and __import__('sys').getprofile() is None
    ap=argparse.ArgumentParser()
    for key in ('peer-manifest','peer-manifest-sha256','peer-seal-receipt','peer-seal-receipt-sha256'):ap.add_argument('--'+key,required=True)
    a=ap.parse_args();peer_path=Path(a.peer_manifest);peer_root=peer_path.parent
    assert peer_path.name=='MANIFEST.json' and not any(os.path.lexists(p) for p in (D,E,HOST))
    assert all(os.environ.get(k)=='1' for k in THREAD_KEYS)
    assert Path(__import__('sys').executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
    oldfreeze,oldfreeze_pin=load(OLD_FREEZE);old=snapshot(OLD_D)
    assert oldfreeze['schema']=='ROOT_V22_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' and oldfreeze['source_root']==str(OLD_D)
    assert oldfreeze['symlinks']=={} and oldfreeze['no_SOURCE_append_after_freeze'] is True
    assert old['files']==oldfreeze['complete_files'] and old['directories']==oldfreeze['complete_directories']
    assert len(old['files'])==123 and len(old['directories'])==12
    oldterminal,oldterminal_pin=load(OLD_TERMINAL);strict_terminal(oldterminal,1)
    assert oldterminal['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1' and oldterminal['observed_terminal'] is True
    mother_m,mother=full_package(MOTHER,MOTHER_SHA)
    bound_m,bound=full_package(BOUND,BOUND_SHA)
    saved_m,saved=full_package(SAVED_PREP_PEER,SAVED_PREP_SHA)
    mpeer_m,mpeer=full_package(MOTHER_PEER,MOTHER_PEER_SHA)
    assert (len(mother['files']),len(bound['files']),len(saved['files']),len(mpeer['files']))==(45,5,83,7)
    mother_review,mother_review_pin=load(MOTHER_PEER/'REVIEW.json')
    assert mother_review['schema']=='INDEPENDENT_V25_MONITOR_ACCESS_COMPLETE_BUILD_NAMESPACE_SOURCE_REVIEW_V1'
    assert mother_review['all_checks_typed_true'] is True and mother_review['blockers']==[]
    assert mother_review['complete_new_Source_manifest_pin']==pin(MOTHER/'MANIFEST.json')
    mother_seal_pin=seal_pair(MOTHER_SEAL,None,pin(MOTHER_PEER/'MANIFEST.json'),mother_review_pin)
    saved_review,saved_review_pin=load(SAVED_PREP_PEER/'REVIEW.json')
    assert saved_review['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'
    assert saved_review['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY' and saved_review['all_checks_typed_true'] is True and saved_review['blockers']==[]
    peer_m,peer=full_package(peer_root,a.peer_manifest_sha256)
    review,review_pin=load(peer_root/'REVIEW.json')
    assert review['schema']=='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1'
    assert review['status']=='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY'
    assert review['source_only'] is True and review['all_checks_typed_true'] is True and review['utility_Source_checks_typed_true'] is True and review['blockers']==[]
    utility_m,utility=full_package(UTILITY,review['actual_Source_utility_manifest_pin']['sha256'])
    expected=[('actual_bound_build_host_pin',BOUND/'combined_build_host.py'),('actual_postclose_META_writer_pin',BOUND/'write_actual_build_postclose_META.py'),('actual_Root_Source_binding_tool_receipt_pin',BINDING_RECEIPT),('qualified_actual_bound_Source_manifest_pin',BOUND/'MANIFEST.json'),('actual_Source_utility_manifest_pin',UTILITY/'MANIFEST.json'),('actual_Root_source_installer_Source_pin',UTILITY/'Root_source_installer.py'),('actual_Root_prelaunch_checker_Source_pin',UTILITY/'Root_prelaunch_checker.py')]
    for field,path in expected:assert review[field]==pin(path)
    assert pin(Path(__file__))==review['actual_Root_source_installer_Source_pin']
    exact(review['original_bound_Source_review_report_pin'])
    peer_seal_pin=seal_pair(Path(a.peer_seal_receipt),a.peer_seal_receipt_sha256,pin(peer_path),review_pin)
    binding,binding_pin=load(BINDING_RECEIPT);tr=strict_terminal(binding,0)
    actual_bind=json.loads(tr['output'])
    assert binding['source_only'] is True and tr['chunk_id']=='a1380b' and actual_bind['manifest']==pin(BOUND/'MANIFEST.json')
    assert actual_bind['host']==pin(BOUND/'combined_build_host.py') and actual_bind['writer']==pin(BOUND/'write_actual_build_postclose_META.py')
    summary,summary_pin=load(PRE/'Root_actual_complete_combined_prepare_summary.json',SUMMARY_SHA)
    assert summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
    ns,nsp,ph,php,prep_inputs,prepared=full_PREP(summary)
    for key,path in [('actual_Root_PREP_summary_pin',PRE/'Root_actual_complete_combined_prepare_summary.json'),('actual_Root_PREP_terminal_pin',PRE/'Root_actual_prepare_tool_terminal_return.json'),('actual_complete_namespace_manifest_pin',PRE/'Root_actual_complete_prepare_namespace_manifest.json')]:assert saved_review[key]==pin(path)
    pre=snapshot(PRE)
    assert pin(C)['sha256']==C_SHA and bound['files']['combined_build_host.py']['sha256']==HOST_SHA and bound['files']['write_actual_build_postclose_META.py']['sha256']==WRITER_SHA
    for rel in OUTPUTS:assert not os.path.lexists(OUT/rel)
    assert shutil.disk_usage(R).free-2*2**30>=8*2**30
    D.mkdir();E.mkdir()
    copy_roles=[('original_complete_closed_failed_V22_build_sources',old),('complete_monitor_access_BUILD_mother_SOURCE',mother),('actual_bound_full_build_SOURCE',bound),('sealed_actual_complete_PREP_saved_META_review',saved),('sealed_independent_monitor_access_BUILD_mother_Source_review',mpeer),('sealed_independent_actual_bound_BUILD_and_utilities_Source_review',peer),('complete_actual_PREP_receipts_before_build',pre)]
    for prefix,v in copy_roles:copy_view(v,prefix)
    # Utilities are retained once; their INPUT_SOURCE_COPIES are author provenance, not recursively recopied into new D.
    utility_selected={k:q for k,q in utility['files'].items() if not k.startswith('INPUT_SOURCE_COPIES/')}
    utility_dirs={k:v for k,v in utility['directories'].items() if k=='.' or not k.startswith('INPUT_SOURCE_COPIES')}
    for k,q in utility_selected.items():
        dest=D/'complete_utility_SOURCE'/k;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q['path'],dest)
        assert pin(dest)['sha256']==q['sha256'] and pin(dest)['size_bytes']==q['size_bytes']
    for k in utility_dirs:(D/'complete_utility_SOURCE'/k).mkdir(parents=True,exist_ok=True)
    for src,name in [(BOUND/'combined_build_host.py','combined_build_host.py'),(BOUND/'write_actual_build_postclose_META.py','write_actual_build_postclose_META.py'),(UTILITY/'Root_source_installer.py','Root_source_installer.py'),(UTILITY/'Root_prelaunch_checker.py','Root_prelaunch_checker.py'),(OLD_FREEZE,'original_V22_complete_source_freeze.byte_exact.json'),(OLD_TERMINAL,'original_V22_closed_failed_tool_terminal.byte_exact.json'),(MOTHER_SEAL,'actual_mother_Source_peer_seal_tool_return.byte_exact.json'),(Path(a.peer_seal_receipt),'actual_bound_and_utility_Source_peer_seal_tool_return.byte_exact.json'),(BINDING_RECEIPT,'actual_Root_BUILD_Source_binding_tool_return.byte_exact.json')]:
        source=pin(src);shutil.copyfile(src,D/name);assert pin(D/name)['sha256']==source['sha256']
    save(D/'Root_complete_SOURCE_install_record.json',dict(schema='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_INSTALL_V1',status='SOURCE_INSTALLED_NO_ACTUAL_BUILD_YET',original_V22_D_freeze=oldfreeze_pin,original_V22_failed_terminal=oldterminal_pin,complete_original_V22_source=old,complete_mother_source=mother,complete_actual_bound_source=bound,complete_actual_PREP_saved_peer=saved,complete_actual_mother_Source_peer=mpeer,actual_mother_Source_peer_seal=mother_seal_pin,complete_actual_bound_and_utility_Source_peer=peer,actual_peer_report=review_pin,actual_peer_seal=peer_seal_pin,qualified_complete_utility_SOURCE=utility,utility_SOURCE_selected_files_retained_once=utility_selected,utility_author_provenance_copies_not_recopied=True,complete_actual_PREP_E_source=pre,actual_PREP_summary=summary_pin,actual_PREP_host_result=php,actual_PREP_peer=saved_review_pin,actual_PREP_namespace=nsp,all144_actual_PREP_fixed_inputs_unchanged=prep_inputs,all_complete_prepared_namespace_unchanged=True,actual_Root_Source_binding=binding_pin,no_SOURCE_append_after_freeze=True,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    frozen=snapshot(D)
    for v in (old,mother,bound,saved,mpeer,peer,utility,pre,*prepared):assert snapshot(Path(v['root']))==v
    for q in prep_inputs:exact(q)
    save(E/'Root_prelaunch_complete_build_source_freeze.json',dict(schema='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1',source_root=str(D),complete_files=frozen['files'],complete_directories=frozen['directories'],symlinks={},no_SOURCE_append_after_freeze=True,actual_complete_SOURCE_file_count=len(frozen['files'])))
    extras=[HOST,S,OUT,T,D,E,PREP_H,PREP_D,PRE]
    assert counted_bytes(extras,C)<2*2**30 and shutil.disk_usage(R).free-2*2**30>=8*2**30
    print(json.dumps(dict(status='COMPLETE_SOURCE_INSTALLED_FROZEN_NO_BUILD_YET',full_Source_files=len(frozen['files']),complete_Source_directories=len(frozen['directories']),host=pin(D/'combined_build_host.py'),writer=pin(D/'write_actual_build_postclose_META.py'),frozen=pin(E/'Root_prelaunch_complete_build_source_freeze.json'),original_V22_D_unchanged=True,actual_PREP_inputs_unchanged=len(prep_inputs),new_build_or_numeric_executed=False)))
if __name__=='__main__':main()
