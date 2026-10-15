import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
D=B/'actual_complete_combined_prepare_v22_sources'
E=B/'actual_complete_combined_prepare_v22_receipts'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py'
U=Path('/private/tmp/axmat_v22_complete_canonical_genuine_PREP_UNREADY_SOURCE_wngfraff')
A=Path('/private/tmp/axmat_v22_actual_Q_bound_complete_PREP_SOURCE_root_20261010_b89d2')

def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read_pin(p):
    i=identity(p)
    assert stat.S_ISREG(i[2]) and not p.is_symlink(),str(p)
    b=p.read_bytes()
    assert identity(p)==i and len(b)==i[4]
    return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
def pin(p):return read_pin(p)[1]
def inventory(root):
    files={};dirs={}
    for folder,dnames,names in os.walk(root,followlinks=False):
        p=Path(folder)
        assert not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode)
        dirs[str(p.relative_to(root))]=identity(p)
        for n in names:
            f=p/n;files[str(f.relative_to(root))]=pin(f)
    return dict(root=str(root),files=files,directories=dirs,symlinks={})
def package(root,wanted_sha):
    mpath=root/'MANIFEST.json';m=json.loads(read_pin(mpath)[0])
    assert pin(mpath)['sha256']==wanted_sha
    members=m['members']
    if isinstance(members,list):members={v['relative_path']:v for v in members}
    assert isinstance(members,dict)
    actual=inventory(root)
    assert set(actual['files'])==set(members)|{'MANIFEST.json'}
    for n,w in members.items():
        p=actual['files'][n]
        assert p=={k:w[k] for k in p},n
    return actual
def terminal(p):
    d=json.loads(read_pin(p)[0]);assert d['closed'] is True
    a=d.get('actual_tool_return',d.get('terminal_tool_return',d.get('exec_command_result')))
    assert type(a['exit_code']) is int and a['exit_code']==0 and not a.get('session_id')
    return pin(p)
def write(p,v):
    with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def copy_tree(root,dest):
    before=inventory(root);assert not dest.exists()
    dest.mkdir(parents=True)
    for n in sorted(before['directories'],key=lambda s:(s.count('/'),s)):
        if n!='.':(dest/n).mkdir(exist_ok=True)
    copies={}
    for n,w in before['files'].items():
        b,p=read_pin(root/n);assert p==w
        with (dest/n).open('xb') as f:f.write(b)
        q=pin(dest/n);assert (q['sha256'],q['size_bytes'])==(w['sha256'],w['size_bytes'])
        copies[n]=dict(original=w,saved=q)
    assert inventory(root)==before
    return dict(original_inventory=before,complete_file_copies=copies,saved_inventory=inventory(dest))

p=argparse.ArgumentParser()
p.add_argument('--bound-peer-root',required=True)
p.add_argument('--bound-peer-manifest-sha256',required=True)
p.add_argument('--bound-peer-seal-receipt',required=True)
args=p.parse_args()
P=Path(args.bound_peer_root);seal=Path(args.bound_peer_seal_receipt)
peer_inventory=package(P,args.bound_peer_manifest_sha256)
peer=json.loads(read_pin(P/'REVIEW.json')[0]);assert peer['PASS'] is True and not peer['hard_blockers']
peer_terminal=terminal(seal)
actual_binding_terminal=terminal(B/'actual_joint_helper_admission_v22b_receipts/Root_actual_Q_to_complete_PREP_Source_binding_tool_return.json')
package(U,'0000b8505b6ea35a149099fe9d0494532f26521bfa13b7de6c8236b297beb9c4')
package(A,'7e2711c180b11ed4d9181f944c8ccd948aebc463227c8ba22b5f7117a6a5c894')
Q=B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
assert pin(Q)['sha256']=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816'
canonical_pin=pin(A/'complete_combined_runtime.V22.READY_SOURCE.py')
assert canonical_pin['sha256']=='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'
for n,h in [('combined_prepare_host.py','1be8cbf79ef14d7537d099d0a08d0c5ef755530c2652c58cfbb188c7e18bf051'),('write_actual_prepare_terminal.py','348ae877f7c8e4c86f07cb4a49f96de97e11839ccb0858c5a602e3982a4ccba0')]:
    assert pin(A/n)['sha256']==h
oldD=B/'actual_complete_combined_prepare_v21_sources'
oldfreeze=json.loads(read_pin(B/'actual_complete_combined_prepare_v21_receipts/Root_prelaunch_complete_source_freeze.json')[0])
original=inventory(oldD)
assert original['files']==oldfreeze['complete_files']
assert sorted(set(original['directories'])-{'.'})==oldfreeze['complete_directories']
assert original['directories']['.']==oldfreeze['source_root_identity']
assert len(original['files'])==58 and len(original['directories'])==10
for n in ['axial-material-complete-combined-prepare-host-v22-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010']:
    assert not os.path.lexists(ART/n)
assert not os.path.lexists(D) and not os.path.lexists(E) and not os.path.lexists(C)
E.mkdir();D.mkdir()
roots=[
    (oldD,'sealed_original_complete_PREP_v21_source'),
    (U,'sealed_complete_PREP_UNREADY_Source'),
    (A,'sealed_actual_READY_complete_PREP_Source'),
    (P,'sealed_independent_actual_READY_complete_PREP_Source_review'),
]
for n in ['actual_complete_graph_helper_controls_v22_sources','actual_complete_graph_fresh_verifier_v22_sources','actual_joint_helper_admission_v22_sources','actual_joint_helper_admission_v22b_sources','actual_complete_graph_helper_controls_v22_receipts','actual_complete_graph_fresh_verifier_v22_receipts','actual_joint_helper_admission_v22_receipts','actual_joint_helper_admission_v22b_receipts']:
    roots.append((B/n,'complete_qualified_helper_evidence/'+n))
copied={}
for root,relative in roots:copied[relative]=copy_tree(root,D/relative)
for src,name in [(seal,'actual_BOUND_Source_peer_seal_tool_return.json'),(U.with_name(U.name+'_seal_receipt')/'ACTUAL_SOURCE_PACKAGE_SEAL_TOOL_TERMINAL_RETURN.json','actual_complete_PREP_UNREADY_author_seal_tool_return.json'),(Path(__file__),'Root_complete_SOURCE_install_writer.py')]:
    b,w=read_pin(src)
    with (D/name).open('xb') as f:f.write(b)
    q=pin(D/name);assert q['sha256']==w['sha256']
    copied[name]=dict(original=w,saved=q)
for n in ['combined_prepare_host.py','write_actual_prepare_terminal.py']:
    b,w=read_pin(A/n)
    with (D/n).open('xb') as f:f.write(b)
    assert pin(D/n)['sha256']==w['sha256']
with C.open('xb') as f:f.write(read_pin(A/'complete_combined_runtime.V22.READY_SOURCE.py')[0])
assert pin(C)['sha256']==canonical_pin['sha256']
assert inventory(oldD)==original and inventory(P)==peer_inventory
write(D/'Root_actual_complete_SOURCE_install_record.json',dict(schema='ROOT_V22_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_RECORD_V1',complete_enumerable_package_copies=copied,actual_binding_terminal=actual_binding_terminal,actual_bound_Source_peer_seal=peer_terminal,canonical_original=canonical_pin,canonical_installed=pin(C),metadata_writer_included_before_freeze=True,original_complete_v21_frozen_Source_unchanged=True,new_PREP_or_build_executed=False,native_or_science_qualified=False,cleanup_performed=False))
frozen=inventory(D)
write(E/'Root_prelaunch_complete_source_freeze.json',dict(schema='ROOT_V22_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1',source_root=str(D),source_root_identity=frozen['directories']['.'],complete_files=frozen['files'],complete_directories={k:v for k,v in frozen['directories'].items() if k!='.'},symlinks={},file_count=len(frozen['files']),directory_count=len(frozen['directories'])-1,no_SOURCE_append_after_freeze=True,all_file_SHA7ID_recorded=True,canonical_factory=pin(C),actual_PREP_not_started=True,original_whole_seconds=1800,original_stage_seconds=600,original_RSS_mib=512,original_joint_archive_bytes=2*2**30,original_history_bytes=96*2**30,original_free_floor_bytes=8*2**30,original_threads=1,original_children=1,original_retries=0))
assert inventory(D)==frozen and inventory(oldD)==original
print(json.dumps({'SOURCE_freeze':pin(E/'Root_prelaunch_complete_source_freeze.json'),'canonical':pin(C),'full_source_files':len(frozen['files']),'full_source_directories':len(frozen['directories'])-1,'metadata_writer_frozen':True,'original_v21_Source_unchanged':True,'PREP_or_build_executed':False}))
