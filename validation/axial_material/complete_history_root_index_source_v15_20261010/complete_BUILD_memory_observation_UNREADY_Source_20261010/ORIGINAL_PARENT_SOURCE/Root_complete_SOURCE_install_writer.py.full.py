"""Root-only finite SOURCE installation; no project/helper/API import or run."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
D=B/'actual_complete_combined_prepare_v25_poststage_temporaries_sources'
E=B/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'
NAMES=('axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010')
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);i=identity(p)
    assert stat.S_ISREG(i[2]) and i[3]==1 and p.is_absolute() and '..' not in p.parts
    for q in (p,*p.parents):assert not q.is_symlink()
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def inventory(root):
    files={};dirs={}
    for folder,dnames,names in os.walk(root,followlinks=False):
        p=Path(folder);assert not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode)
        dirs[str(p.relative_to(root))]=identity(p)
        for n in names:files[str((p/n).relative_to(root))]=pin(p/n)
    return dict(root=str(root),files=files,directories=dirs,symlinks={})
def package(root,wanted):
    mp=pin(root/'MANIFEST.json');assert mp['sha256']==wanted and len(wanted)==64 and wanted!='0'*64
    m=json.loads((root/'MANIFEST.json').read_bytes());members=m.get('members',m.get('complete_members'))
    assert type(members) in (list,dict)
    if type(members) is list:members={v['relative_path']:v for v in members}
    actual=inventory(root);assert set(actual['files'])==set(members)|{'MANIFEST.json'}
    for n,w in members.items():assert actual['files'][n]=={k:w[k] for k in ('path','sha256','size_bytes','identity')}
    declared=m['directories']
    if type(declared) is list:declared={v['relative_path']:v['identity'] for v in declared}
    assert actual['directories']==declared
    return actual,mp
def terminal(p):
    pp=pin(p);v=json.loads(p.read_bytes());assert v['closed'] is True
    t=v.get('terminal_tool_return',v.get('actual_tool_return',v.get('exec_command_result')))
    assert type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t
    return pp
def write(p,value):
    with p.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def copy_file(source,dest):
    before=pin(source)
    with source.open('rb') as src,dest.open('xb') as dst:
        while True:
            raw=src.read(1024*1024)
            if not raw:break
            dst.write(raw)
    saved=pin(dest);assert pin(source)==before and (saved['sha256'],saved['size_bytes'])==(before['sha256'],before['size_bytes'])
    return dict(original=before,saved=saved)
def copy_tree(root,dest):
    before=inventory(root);assert not os.path.lexists(dest);dest.mkdir(parents=True)
    for name in sorted(before['directories'],key=lambda x:(x.count('/'),x)):
        if name!='.':(dest/name).mkdir(exist_ok=False)
    pairs={n:copy_file(root/n,dest/n) for n in before['files']}
    assert inventory(root)==before
    return dict(original_inventory=before,complete_file_copies=pairs,saved_inventory=inventory(dest))


import Root_poststage_Source_META_contract as scope
assert Path(scope.__file__).resolve()==Path(__file__).resolve().parent/'Root_poststage_Source_META_contract.py'
assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
assert Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
assert all(os.environ.get(k)=='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))
parser=argparse.ArgumentParser();parser.add_argument('--request',required=True);parser.add_argument('--request-sha256',required=True);args=parser.parse_args()
request,request_pin=scope.load_request(args.request,args.request_sha256,'PREP')
assert pin(Path(__file__))==request['utility']['roles']['Root_complete_SOURCE_install_writer.py']
assert all(not os.path.lexists(p) for p in (D,E,C,*(ART/n for n in NAMES)))
assert __import__('shutil').disk_usage(R).free-2*2**30>=8*2**30
D.mkdir();E.mkdir();copied={};owners=[]
source_views=[('original_closed_monitor_access_complete_PREP_Source',request['parent']['view']),('complete_poststage_seven_role_author_Source',request['author']['view']),('sealed_independent_poststage_seven_role_Source_review',request['author']['peer']['view']),('actual_bound_complete_PREP_Source',request['bound']['view']),('sealed_independent_actual_bound_complete_PREP_Source_review',request['bound']['peer']['view']),('complete_poststage_utility_Source',request['utility']['view']),('sealed_independent_complete_poststage_utility_Source_review',request['utility']['peer']['view'])]
for prefix,v in source_views:
    copied[prefix]=copy_tree(Path(v['root']),D/prefix);owners.append(dict(original=v,destination_prefix=prefix))
for role,q in request['utility']['roles'].items():copied[role]=copy_file(Path(q['path']),D/role)
copied['fixed_contract']=copy_file(Path(scope.__file__).parent/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json',D/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json')
roles=request['bound']['roles']
for role,name in [('prepare_host','combined_prepare_host.py'),('prepare_writer','write_actual_prepare_terminal.py')]:copied[name]=copy_file(Path(roles[role]['path']),D/name)
copied['canonical']=copy_file(Path(roles['canonical']['path']),C)
copied['request']=copy_file(Path(args.request),D/'Root_actual_Source_META_install_request.byte_exact.json')
for name,q in [('actual_Root_PREP_Source_binding_terminal.byte_exact.json',request['bound']['binding_terminal']),('actual_bound_PREP_Source_peer_seal.byte_exact.json',request['bound']['peer']['seal']),('actual_complete_utility_Source_peer_seal.byte_exact.json',request['utility']['peer']['seal']),('actual_seven_role_Source_peer_seal.byte_exact.json',request['author']['peer']['seal']),('original_complete_PREP_Source_freeze.byte_exact.json',request['parent']['freeze'])]:copied[name]=copy_file(Path(q['path']),D/name)
prefix=scope.original_prefix_seven(roles)
write(D/'Root_actual_complete_SOURCE_install_record.json',dict(schema='ROOT_V25_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_RECORD_V1',source_only=True,status='COMPLETE_SOURCE_INSTALLED_NO_NEW_PREP_EXECUTED',actual_request=request_pin,installed_request=pin(D/'Root_actual_Source_META_install_request.byte_exact.json'),complete_Source_owner_copies=owners,complete_enumerable_package_copies=copied,exact_original_host_prefix_seven_input_pins=prefix,original_parent_Source_file_count=135,actual_helper_only_Q=request['actual_helper_Q'],canonical_installed=pin(C),metadata_writer_and_prelaunch_included_before_freeze=True,no_SOURCE_append_after_freeze=True,new_PREP_or_build_executed=False,whole_build_INPUT_native_or_science_qualified=False,cleanup_performed=False))
frozen=inventory(D)
write(E/'Root_prelaunch_complete_source_freeze.json',dict(schema='ROOT_V25_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1',source_root=str(D),source_root_identity=frozen['directories']['.'],complete_files=frozen['files'],complete_directories={k:v for k,v in frozen['directories'].items() if k!='.'},symlinks={},file_count=len(frozen['files']),directory_count=len(frozen['directories'])-1,no_SOURCE_append_after_freeze=True,all_file_SHA7ID_recorded=True,canonical_factory=pin(C),actual_PREP_not_started=True,original_whole_seconds=1800,original_stage_seconds=600,original_RSS_mib=512,original_joint_archive_bytes=2*2**30,original_history_bytes=96*2**30,original_free_floor_bytes=8*2**30,original_threads=1,original_children=1,original_retries=0))
assert inventory(D)==frozen
scope.installed_request(D,'PREP');assert inventory(D)==frozen
total=pin(C)['size_bytes']+sum(q['size_bytes'] for q in frozen['files'].values())+sum(pin(p)['size_bytes'] for p in E.iterdir() if p.is_file())
assert total<2*2**30 and __import__('shutil').disk_usage(R).free-2*2**30>=8*2**30
print(json.dumps(dict(SOURCE_freeze=pin(E/'Root_prelaunch_complete_source_freeze.json'),canonical=pin(C),full_source_files=len(frozen['files']),full_source_directories=len(frozen['directories'])-1,old_parent_Source_count=135,new_original_host_ordered_input_count=7+len(frozen['files']),new_all_protected_input_count=9+len(frozen['files']),complete_H_S_O_T_D_E_and_canonical_regular_bytes=total,original_closed_parent_unchanged=True,PREP_or_build_executed=False)))
