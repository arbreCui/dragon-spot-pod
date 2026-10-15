import argparse, hashlib, json, os, shutil, stat
from pathlib import Path

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
D=B/'actual_complete_combined_build_v25_poststage_temporaries_sources'
E=B/'actual_complete_combined_build_v25_poststage_temporaries_receipts'
PRE=B/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'
OLD_D=B/'actual_complete_combined_build_v22_sources'
OLD_FREEZE=B/'actual_complete_combined_build_v22_receipts/Root_prelaunch_complete_build_source_freeze.json'
BOUND=None  # UNREADY until actual finite request
HOST=ART/'axial-material-complete-combined-build-host-v25-poststage-temporaries-20261010'
OUT=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'

PREP_H=ART/'axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010'
PREP_D=B/'actual_complete_combined_prepare_v25_poststage_temporaries_sources'
MOTHER=None  # UNREADY until actual finite request
SAVED_PREP_PEER=None  # UNREADY until actual finite request
MOTHER_PEER=None  # UNREADY until actual finite request
MOTHER_SEAL=None  # UNREADY until actual finite request
BINDING_RECEIPT=None  # UNREADY until actual finite request
OLD_TERMINAL=B/'actual_complete_combined_build_v22_receipts/Root_actual_build_tool_terminal_return.json'
UTILITY=None  # UNREADY until actual finite request
MOTHER_SHA=None  # UNREADY until actual finite request
BOUND_SHA=None  # UNREADY until actual finite request
SAVED_PREP_SHA=None  # UNREADY until actual finite request
MOTHER_PEER_SHA=None  # UNREADY until actual finite request
SUMMARY_SHA=None  # UNREADY until actual finite request
NS_SHA=None  # UNREADY until actual finite request
HOST_SHA=None  # UNREADY until actual finite request
WRITER_SHA=None  # UNREADY until actual finite request
C_SHA=None  # UNREADY until actual finite request
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
    scope.prepare_input_scope(ph,summary)
    inputs=[exact(q) for q in ph['input_sources']+[ph['original_helper'],ph['resource_factory']]]
    assert len(inputs)==len(ph['input_sources'])+2 and summary['all_original_pinned_inputs_unchanged_count']==len(inputs)
    strict_terminal(load(PRE/'Root_actual_prepare_tool_terminal_return.json')[0],0)
    strict_terminal(load(PRE/'Root_actual_prepare_metadata_writer_tool_terminal_return.json')[0],0)
    return ns,nsp,ph,php,inputs,prepared

def counted_bytes(roots,canonical):
    return sum(q['size_bytes'] for root in roots if root.exists() for q in snapshot(root)['files'].values())+pin(canonical)['size_bytes']

import Root_poststage_Source_META_contract as scope
def main():
    global SUMMARY_SHA,NS_SHA,HOST_SHA,WRITER_SHA,C_SHA
    assert Path(scope.__file__).resolve()==Path(__file__).resolve().parent/'Root_poststage_Source_META_contract.py'
    sys=__import__('sys');assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
    assert all(os.environ.get(k)=='1' for k in THREAD_KEYS) and Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
    ap=argparse.ArgumentParser();ap.add_argument('--request',required=True);ap.add_argument('--request-sha256',required=True);a=ap.parse_args()
    request,request_pin=scope.load_request(a.request,a.request_sha256,'BUILD')
    assert pin(Path(__file__))==request['utility']['roles']['Root_source_installer.py']
    prep=request['actual_new_PREP'];roles=request['bound']['roles']
    SUMMARY_SHA=prep['summary']['sha256'];NS_SHA=prep['namespace']['sha256'];HOST_SHA=roles['build_host']['sha256'];WRITER_SHA=roles['build_writer']['sha256'];C_SHA=pin(C)['sha256']
    summary,summary_pin=load(PRE/'Root_actual_complete_combined_prepare_summary.json',SUMMARY_SHA)
    ns,nsp,ph,php,prep_inputs,prepared=full_PREP(summary)
    assert all(not os.path.lexists(p) for p in (D,E,HOST)) and all(not os.path.lexists(OUT/rel) for rel in OUTPUTS)
    assert shutil.disk_usage(R).free-2*2**30>=8*2**30
    D.mkdir();E.mkdir();owners=[]
    copy_roles=[('original_closed_monitor_access_complete_BUILD_Source',request['parent']['view']),('complete_actual_poststage_PREP_Source',prep['complete_new_PREP_Source']),('actual_bound_full_build_SOURCE',request['bound']['view']),('sealed_actual_complete_PREP_saved_META_review',prep['peer']['view']),('sealed_independent_actual_bound_BUILD_Source_review',request['bound']['peer']['view']),('complete_actual_PREP_receipts_before_build',prep['current_complete_PREP_E'])]
    for prefix,v in copy_roles:copy_view(v,prefix);owners.append(dict(original=v,destination_prefix=prefix))
    # PREP's whole Source owner tree already retains this exact utility, author and independent utility peer packages once.
    assert prep['complete_new_PREP_Source']['files']['Root_poststage_Source_META_contract.py']['sha256']==request['utility']['roles']['Root_poststage_Source_META_contract.py']['sha256']
    for role,q in request['utility']['roles'].items():
        target=D/role;shutil.copyfile(q['path'],target);assert pin(target)['sha256']==q['sha256'] and pin(target)['size_bytes']==q['size_bytes']
    for src,name in [(Path(scope.__file__).parent/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json','FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json'),(Path(roles['build_host']['path']),'combined_build_host.py'),(Path(roles['build_writer']['path']),'write_actual_build_postclose_META.py'),(Path(a.request),'Root_actual_Source_META_install_request.byte_exact.json'),(Path(request['bound']['binding_terminal']['path']),'actual_Root_BUILD_Source_binding_tool_return.byte_exact.json'),(Path(request['bound']['peer']['seal']['path']),'actual_bound_BUILD_Source_peer_seal.byte_exact.json'),(Path(prep['peer']['seal']['path']),'actual_saved_PREP_META_peer_seal.byte_exact.json'),(Path(request['parent']['freeze']['path']),'original_complete_BUILD_Source_freeze.byte_exact.json')]:
        q=pin(src);shutil.copyfile(src,D/name);assert pin(D/name)['sha256']==q['sha256'] and pin(D/name)['size_bytes']==q['size_bytes']
    save(D/'Root_complete_SOURCE_install_record.json',dict(schema='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_INSTALL_V1',status='SOURCE_INSTALLED_NO_ACTUAL_BUILD_YET',source_only=True,actual_request=request_pin,installed_request=pin(D/'Root_actual_Source_META_install_request.byte_exact.json'),complete_Source_owner_copies=owners,complete_actual_PREP_E_source=prep['current_complete_PREP_E'],actual_PREP_summary=summary_pin,actual_PREP_host_result=php,actual_PREP_namespace=nsp,all_actual_PREP_fixed_inputs_unchanged=prep_inputs,actual_PREP_fixed_input_count=len(prep_inputs),old144_count_is_provenance_only=True,all_complete_prepared_namespace_unchanged=True,actual_Root_Source_binding=request['bound']['binding_terminal'],old_parent_complete_Source_count=328,no_SOURCE_append_after_freeze=True,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    frozen=snapshot(D)
    for _,v in copy_roles:assert snapshot(Path(v['root']))==v
    for q in prep_inputs:exact(q)
    save(E/'Root_prelaunch_complete_build_source_freeze.json',dict(schema='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1',source_root=str(D),complete_files=frozen['files'],complete_directories=frozen['directories'],symlinks={},no_SOURCE_append_after_freeze=True,actual_complete_SOURCE_file_count=len(frozen['files'])))
    scope.installed_request(D,'BUILD');assert snapshot(D)==frozen
    extras=[HOST,S,OUT,T,D,E,PREP_H,PREP_D,PRE]
    assert counted_bytes(extras,C)<2*2**30 and shutil.disk_usage(R).free-2*2**30>=8*2**30
    print(json.dumps(dict(status='COMPLETE_SOURCE_INSTALLED_FROZEN_NO_BUILD_YET',full_Source_files=len(frozen['files']),complete_Source_directories=len(frozen['directories']),host=pin(D/'combined_build_host.py'),writer=pin(D/'write_actual_build_postclose_META.py'),frozen=pin(E/'Root_prelaunch_complete_build_source_freeze.json'),old_parent_Source_count=328,actual_PREP_inputs_unchanged=len(prep_inputs),new_build_or_numeric_executed=False)))
if __name__=='__main__':main()
