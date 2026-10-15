#!/usr/bin/env python3
"""Independent actual release postverification, streaming full EOF of all retained pins."""
import hashlib,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
S=R/'storage_release_literal2_old_v14_BQ_source_v2_20261014';D=R/'independent_literal2_old_v14_BQ_v2_actual_postverify_20261014'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return{k:q[k]for k in('path','sha256','size_bytes','identity')}
def read(p,q=None,capture=True):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 h=hashlib.sha256();parts=[];fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert ids(os.fstat(fd))==ids(s)
  while True:
   b=os.read(fd,1048576)
   if not b:break
   h.update(b)
   if capture:parts.append(b)
  assert ids(os.fstat(fd))==ids(s)
 finally:os.close(fd)
 assert ids(p.lstat())==ids(s);pf=dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
 if q is not None:assert pf==norm(q),(str(p),'fullEOF PF')
 return b''.join(parts)if capture else None,pf
def load(p,q=None):
 b,pf=read(p,q);return json.loads(b),pf
def inventory(root):
 files={};dirs={};links={};todo=[Path(root)]
 while todo:
  p=todo.pop();s=p.lstat();assert stat.S_ISDIR(s.st_mode)and not p.is_symlink();dirs[str(p)]=ids(s)
  fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   assert ids(os.fstat(fd))==ids(s)
   with os.scandir(fd)as entries:
    for e in entries:
     q=p/e.name;t=e.stat(follow_symlinks=False)
     if stat.S_ISDIR(t.st_mode):todo.append(q)
     elif stat.S_ISREG(t.st_mode):files[str(q)]=ids(t)
     elif stat.S_ISLNK(t.st_mode):links[str(q)]=dict(identity=ids(t),target=os.readlink(q))
     else:raise AssertionError('special file')
   assert ids(os.fstat(fd))==ids(s)
  finally:os.close(fd)
 return dict(ordinary_file_identities=files,directory_identities=dirs,symlinks=links)
m,mp=load(S/'EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json');assert mp['sha256']=='2d9ea9a1c7dace6c79cbc23f360f9e020d85b488a2a0f19d4f5272fd477c435a'
receipt,rp=load(R/'storage_release_literal2_old_v14_BQ_actual_receipts_20261014/ACTUAL_EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_OLD_PRIVATE_RELEASE_RECEIPT.json')
assert rp['sha256']=='ec2c754aa82d3fa2f78a4f507a1de2edf2d33451e39e160bd39b83242c8ab863'and rp['size_bytes']==367916
assert rp['identity']==[16777229,50075010,33188,1,367916,1791910358694881907,1791910358694881907]
tool,tp=load(R/'ROOT_LITERAL2_V2_ACTUAL_EXECUTE_TRUE_TOOL_RETURNS_20261014.json')
assert tool['actual_initial_return']['chunk_id']=='3cd71d'and tool['actual_initial_return']['session_id']==80090
terminal=tool['actual_terminal_return'];assert terminal['chunk_id']=='655ec6'and type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None
observed=json.loads(terminal['output'].strip().splitlines()[-1]);assert observed['receipt_pin']==rp and observed['deleted_files']==2 and observed['logical_bytes_released']==528482632 and observed['original_initial_reserve_admitted']is True
argv,argvp=load(R/'ROOT_EXACT_LITERAL2_V2_READONLY_AND_EXECUTE_ARGV_20261014.json')
assert shlex.split(tool['exact_executed_command'])==argv['execute_argv']and argv['execute_argv']==argv['readonly_argv']+['--execute']and argv['execute_argv'].count('--execute')==1
assert receipt['manifest_pin']==mp and receipt['status']=='EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'
assert receipt['execute_requested']is True and receipt['deleted_files']==2 and receipt['logical_bytes_released']==528482632 and receipt['next_target_intent']is None and receipt['compiler_or_business_executed']is False
sf,sfp=load(m['selected_Source_freeze_pin']['path'],m['selected_Source_freeze_pin']);assert sfp['sha256']=='b479562621c520def2825c349cb9312e93c77a2612bc55bc06f49f158fe7b58c'
targets=m['target_full_EOF_pins'];assert targets==sf['literal2_fullpins']and len(targets)==2
assert all(not os.path.lexists(q['path'])for q in targets)
assert [x['original_fullpin']for x in receipt['deletion_records']]==targets
for rec in receipt['deletion_records']:
 for key in ['actual_unlink_returned','target_directory_fsync_attempted','target_directory_fsync_returned','confirmed_absent']:assert rec[key]is True,key
 before=rec['parent_before_seven_id'];after=rec['parent_after_seven_id']
 assert before[:3]==after[:3]and after[3]==before[3]-1 and after[4]==before[4]-32 and after[5]>=before[5]and after[6]>=before[6]
assert receipt['deletion_records'][0]['parent_after_seven_id']==receipt['deletion_records'][1]['parent_before_seven_id']
protected=m['current_protected_full_EOF_pins'];assert len(protected)==7251
for q in protected:read(q['path'],q,False)
retained=m['retained_all_other_v14_files_full_EOF_pins'];assert len(retained)==297
ptable={q['path']:norm(q)for q in protected}
for q in retained:assert ptable[q['path']]==norm(q)
before=m['complete_before_inventory'];root=sf['literal_failed_owner_proof']['root'];now=inventory(root)
paths={q['path']for q in targets}
assert now['ordinary_file_identities']=={p:i for p,i in before['ordinary_file_identities'].items()if p not in paths}
assert not now['symlinks']and now['symlinks']==before['symlinks']and set(now['directory_identities'])==set(before['directory_identities'])
changes=receipt['affected_parent_changes'];assert len(changes)==1
changed=changes[0];parent=str(Path(targets[0]['path']).parent);assert changed['path']==parent==str(Path(targets[1]['path']).parent)
assert changed['removed_children']==2 and changed['nlink_delta']==-2 and changed['size_delta']==-64
assert changed['before']==before['directory_identities'][parent]and changed['after']==now['directory_identities'][parent]
for p,old in before['directory_identities'].items():
 cur=now['directory_identities'][p]
 if p!=parent:assert cur==old,p
 else:assert cur[:3]==old[:3]and cur[3]==old[3]-2 and cur[4]==old[4]-64 and cur[5]>=old[5]and cur[6]>=old[6]
v12='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12'
assert inventory(v12)==m['Source_DAG_provenance']['current_v12_complete_inventory']
bundles=[q for q in protected if q['path'].endswith('coherent_complete_context.xsm')and '/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/'in q['path']]
assert len(bundles)==2 and all(q['size_bytes']==100163528 and q['sha256']=='2ba7398987f21ce747691ca5d635a374e5793ce7f2dbad2a30b1bb827d4c9061'for q in bundles)
b=receipt['original_budget_before'];a=receipt['original_budget_after']
assert b['artifact_bytes']==80070766376 and a['artifact_bytes']==79542283744 and b['artifact_bytes']-a['artifact_bytes']==528482632
assert b['regular_files']==97461 and a['regular_files']==97459 and b['regular_files']-a['regular_files']==2
for v in[b,a]:
 assert v['artifact_budget_bytes']==103079215104 and v['min_free_bytes']==8589934592 and v['disk_free_bytes']>=8589934592 and v['original_cold_reserve_bytes']==20971764748 and v['metadata_reserve_bytes']==67108864 and v['initial_fresh_reserve_bytes']==2147483648
 assert v['remaining_after_original_initial_reserves_bytes']==103079215104-v['artifact_bytes']-20971764748-67108864-2147483648
assert a['remaining_after_original_initial_reserves_bytes']==350574100 and a['original_initial_reserve_admitted']is True
assert b['resource_scope_policy']==a['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
assert b['resource_scope_contract']==a['resource_scope_contract']and b['resource_roots']==a['resource_roots']and b['declared_resource_roots']==a['declared_resource_roots']
pub_review,pub_reviewp=load(R/'independent_public7_final_HF_ROOT_CLI_Source_integration_review_20261014/REVIEW.json')
for q in[pub_review['host_freeze_pin'],pub_review['CLI_pin'],pub_review['host_source_pin'],pub_review['plan_pin'],pub_review['lifetime_Source_plan_pin']]:read(q['path'],q)
assert not Path(pub_review['planned_output_root']).exists()
for q in protected:
 assert ids(Path(q['path']).lstat())==q['identity'],q['path']
for q in[sfp,mp,rp,tp,argvp]:assert ids(Path(q['path']).lstat())==q['identity']
report=dict(schema='INDEPENDENT_ACTUAL_LITERAL2_OLD_V14_BQ_V2_RELEASE_POSTVERIFICATION_V1',status='PASS_ACTUAL_LITERAL2_V2_EXACT_RELEASE_ALL_RETAINED_FULL_EOF_POSTVERIFIED',failure=None,
 actual_release_receipt_pin=rp,actual_Root_true_tool_pin=tp,actual_Root_initial_return=tool['actual_initial_return'],actual_Root_terminal_return=terminal,manifest_pin=mp,Source_freeze_pin=sfp,exact_execute_argv_pin=argvp,
 actual_deleted_files=2,actual_logical_bytes_released=528482632,actual_deleted_original_fullpins=targets,both_targets_absent=True,actual_unlink_and_target_directory_fsync_returned_both=True,actual_deletion_records=receipt['deletion_records'],
 current_protected_count=7251,independent_all7251_full_EOF_SHA_all7_reverified=True,streamed_scientific_files_no_wholefile_memory_buffer=True,all297_retained_v14_fullEOF_PFs_preserved=True,all7251_postEOF_current7_reobserved=True,
 actual_v14_remaining_file_count=len(now['ordinary_file_identities']),actual_v14_directory_count=len(now['directory_identities']),actual_v14_symlink_count=len(now['symlinks']),only_one_parent_nlink_minus2_size_minus64=True,actual_affected_parent_changes=changes,all_other35_directories_unchanged=True,current_v12_inventory_unchanged=True,
 current_failed_public5_context_bundle_pins_preserved_fullEOF=bundles,current_public7_Source_HF_CLI_PLAN_lifetime_unchanged=True,current_public7_OUT_still_absent=True,public7_final_Source_review_pin=pub_reviewp,
 actual_family_budget_before=b,actual_family_budget_after=a,actual_unique_family_delta_bytes=528482632,actual_unique_family_file_delta=2,original_full_fresh_cold_metadata_reserve_admitted=True,remaining_after_original_initial_reserves_bytes=350574100,
 original_guarded_Root_fullEOF_PS_lsof_before_after_evidence_preserved=True,independent_PS_lsof_not_repeated=True,
 independent_deletion_executed=False,independent_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,all_file_descriptors_closed=True,
 only_old_private_exact_path_replay_lost=True,production_reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,
 limitation='This verifies the exact cleanup and preserved results. The new public7 controls and complete pipeline still require their own genuine executions.')
D.mkdir(exist_ok=True);p=D/'REVIEW.json';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert os.write(fd,raw)==len(raw);os.fsync(fd)
finally:os.close(fd)
_,qp=read(p);print(json.dumps(dict(status=report['status'],review_pin=qp,all7251_independent_fullEOF_verified=True,actual_deleted_files=2,actual_logical_bytes_released=528482632,all297_retained=True,remaining_after_original_initial_reserves_bytes=350574100,current_public7_OUT_absent=True,all_file_descriptors_closed=True)))
