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
D=B/'actual_complete_combined_prepare_v25_sources'
E=B/'actual_complete_combined_prepare_v25_receipts'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py'
NAMES=('axial-material-complete-combined-prepare-host-v25-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-20261010')
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

assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
p=argparse.ArgumentParser()
for k in ('unready-root','unready-manifest-sha256','unready-seal','unready-peer-root','unready-peer-manifest-sha256','unready-peer-seal','bound-root','bound-manifest-sha256','bound-peer-root','bound-peer-manifest-sha256','bound-peer-seal','actual-binding-tool-return','prelaunch-source'):
    p.add_argument('--'+k,required=True)
args=p.parse_args();U=Path(args.unready_root);UP=Path(args.unready_peer_root);A=Path(args.bound_root);P=Path(args.bound_peer_root)
originals={};manifests={}
for label,root,wanted in [('sealed_complete_PREP_UNREADY_Source',U,args.unready_manifest_sha256),('sealed_independent_UNREADY_complete_PREP_Source_review',UP,args.unready_peer_manifest_sha256),('sealed_actual_READY_complete_PREP_Source',A,args.bound_manifest_sha256),('sealed_independent_actual_READY_complete_PREP_Source_review',P,args.bound_peer_manifest_sha256)]:
    originals[label],manifests[label]=package(root,wanted)
for peerroot,expected_schema,manifest_key,source_label,rolepaths in [
    (UP,'INDEPENDENT_V25_COMPLETE_CANONICAL_TRUE_SNAPSHOT_PREP_BUILD_SOURCE_REVIEW_V1','qualified_template_manifest_pin','sealed_complete_PREP_UNREADY_Source',{'canonical':U/'canonical.V25.UNREADY.full.py','prepare_host':U/'host_and_postclose_templates/prepare_host.V25.UNREADY.full.py','prepare_writer':U/'host_and_postclose_templates/prepare_writer.V25.UNREADY.full.py','build_host':U/'host_and_postclose_templates/build_host.V25.UNREADY.full.py','build_writer':U/'host_and_postclose_templates/build_writer.V25.UNREADY.full.py','PREP_binder':U/'bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py','BUILD_binder':U/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'}),
    (P,'INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1','qualified_bound_manifest_pin','sealed_actual_READY_complete_PREP_Source',{'canonical':A/C.name,'prepare_host':A/'combined_prepare_host.py','prepare_writer':A/'write_actual_prepare_terminal.py'})]:
    review=json.loads((peerroot/'REVIEW.json').read_bytes())
    assert review['schema']==expected_schema and review['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION'
    assert review['source_only'] is True and review['all_checks_typed_true'] is True and review['blockers']==[]
    assert type(review['check_count']) is int and len(review['checks'])==review['check_count']>0
    assert all(type(c['passed']) is bool and c['passed'] is True for c in review['checks'])
    assert review[manifest_key]==manifests[source_label]
    assert review['qualified_role_Source_pins']=={k:pin(v) for k,v in rolepaths.items()}
proofs={k:terminal(Path(v)) for k,v in [('unready_author_seal',args.unready_seal),('unready_independent_seal',args.unready_peer_seal),('bound_independent_seal',args.bound_peer_seal),('actual_Source_binding_tool_return',args.actual_binding_tool_return)]}
Q=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json';qp=pin(Q)
assert qp['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
helper=R/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
hp=pin(helper);assert hp['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
bound_inverse=json.loads((A/'Root_actual_Q_bound_complete_PREP_Source_inverse.json').read_bytes())
assert bound_inverse['source_only'] is True and bound_inverse['actual_Q']==qp and bound_inverse['candidate_guard_API_compiler_or_numeric_executed'] is False
assert all(v is None for v in bound_inverse['all_six_future_business_pins'].values())
assert all(not os.path.lexists(q) for q in (D,E,C,*(ART/n for n in NAMES)))
pre=Path(args.prelaunch_source);prepin=pin(pre)
before_oldcanonical=pin(R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py')
assert before_oldcanonical['sha256']=='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'
D.mkdir();E.mkdir();copied={}
for label,root in [('sealed_complete_PREP_UNREADY_Source',U),('sealed_independent_UNREADY_complete_PREP_Source_review',UP),('sealed_actual_READY_complete_PREP_Source',A),('sealed_independent_actual_READY_complete_PREP_Source_review',P)]:copied[label]=copy_tree(root,D/label)
for key,proof in proofs.items():copied[key]=copy_file(Path(proof['path']),D/(key+'.json'))
copied['Root_complete_SOURCE_install_writer.py']=copy_file(Path(__file__),D/'Root_complete_SOURCE_install_writer.py')
copied['Root_complete_PREP_prelaunch.py']=copy_file(pre,D/'Root_complete_PREP_prelaunch.py')
for n in ('combined_prepare_host.py','write_actual_prepare_terminal.py'):copied[n]=copy_file(A/n,D/n)
copied['canonical_factory']=copy_file(A/C.name,C)
for label,root in [('sealed_complete_PREP_UNREADY_Source',U),('sealed_independent_UNREADY_complete_PREP_Source_review',UP),('sealed_actual_READY_complete_PREP_Source',A),('sealed_independent_actual_READY_complete_PREP_Source_review',P)]:assert inventory(root)==originals[label]
assert pin(Q)==qp and pin(helper)==hp and pin(pre)==prepin and pin(Path(before_oldcanonical['path']))==before_oldcanonical
write(D/'Root_actual_complete_SOURCE_install_record.json',dict(schema='ROOT_V25_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_RECORD_V1',source_only=True,complete_enumerable_package_copies=copied,source_manifests=manifests,actual_complete_bound_Source_proofs=proofs,actual_helper_only_Q=qp,installed_helper=hp,canonical_installed=pin(C),prior_v22_canonical_unchanged=before_oldcanonical,metadata_writer_and_prelaunch_included_before_freeze=True,new_PREP_or_build_executed=False,whole_build_INPUT_native_or_science_qualified=False,cleanup_performed=False))
frozen=inventory(D)
write(E/'Root_prelaunch_complete_source_freeze.json',dict(schema='ROOT_V25_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1',source_root=str(D),source_root_identity=frozen['directories']['.'],complete_files=frozen['files'],complete_directories={k:v for k,v in frozen['directories'].items() if k!='.'},symlinks={},file_count=len(frozen['files']),directory_count=len(frozen['directories'])-1,no_SOURCE_append_after_freeze=True,all_file_SHA7ID_recorded=True,canonical_factory=pin(C),actual_PREP_not_started=True,original_whole_seconds=1800,original_stage_seconds=600,original_RSS_mib=512,original_joint_archive_bytes=2*2**30,original_history_bytes=96*2**30,original_free_floor_bytes=8*2**30,original_threads=1,original_children=1,original_retries=0))
assert inventory(D)==frozen
total=pin(C)['size_bytes']+sum(v['size_bytes'] for v in frozen['files'].values())+sum(pin(x)['size_bytes'] for x in E.rglob('*') if x.is_file())
assert total<2*2**30
print(json.dumps(dict(SOURCE_freeze=pin(E/'Root_prelaunch_complete_source_freeze.json'),canonical=pin(C),full_source_files=len(frozen['files']),full_source_directories=len(frozen['directories'])-1,complete_H_S_O_T_D_E_and_canonical_regular_bytes=total,metadata_writer_and_prelaunch_frozen=True,PREP_or_build_executed=False)))
