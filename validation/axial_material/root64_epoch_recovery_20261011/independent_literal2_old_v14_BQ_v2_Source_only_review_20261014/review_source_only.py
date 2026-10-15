#!/usr/bin/env python3
"""Read only frozen Sources and metadata; never import candidates or open target data."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
D=R/'storage_release_literal2_old_v14_BQ_source_v2_20261014'
OUT=R/'independent_literal2_old_v14_BQ_v2_Source_only_review_20261014'
def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return{k:q[k]for k in('path','sha256','size_bytes','identity')}
def read(p,expected=None):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 with p.open('rb')as f:
  assert seven(os.fstat(f.fileno()))==seven(s);b=f.read();assert seven(os.fstat(f.fileno()))==seven(s)
 assert seven(p.lstat())==seven(s)
 q=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=seven(s))
 if expected is not None:assert q==norm(expected),(str(p),'PF')
 return b,q
def load(p,expected=None):
 b,q=read(p,expected);return json.loads(b),q
sf,sfp=load(D/'COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json')
assert sfp['sha256']=='b479562621c520def2825c349cb9312e93c77a2612bc55bc06f49f158fe7b58c'
assert sf['source_only']is True and sf['manifest_prepared']is False and sf['deletion_executed']is False and sf['compiler_or_business_executed']is False
assert all(sf[k]is None for k in('future_manifest_pin','future_readonly_receipt_pin','future_actual_release_receipt_pin'))
original,originalp=load(sf['predecessor_Source_v1_freeze_pin']['path'],sf['predecessor_Source_v1_freeze_pin'])
texts={};sourcepins=[]
for q in sf['Source_pins']:
 b,p=read(q['path'],q);ast.parse(b);texts[Path(q['path']).name]=b;sourcepins.append(p)
oldtexts={}
for q in sf['predecessor_Source_v1_pins']:
 b,p=read(q['path'],q);oldtexts[Path(q['path']).name]=b
assert texts['literal2_release_common.py']==oldtexts['literal2_release_common.py']
assert texts['prepare_literal2_manifest.py']==oldtexts['prepare_literal2_manifest.py']
inverse,inversep=load(sf['whole_Source_v1_to_v2_two_block_byte_inverse_pin']['path'],sf['whole_Source_v1_to_v2_two_block_byte_inverse_pin'])
assert len(inverse['exact_changed_blocks'])==2 and inverse['current_Source_pins']==sf['Source_pins']
restored=texts['verify_or_execute_literal2.py'].decode()
for block in reversed(inverse['exact_changed_blocks']):
 assert restored.count(block['after'])==1;restored=restored.replace(block['after'],block['before'],1)
assert restored.encode()==oldtexts['verify_or_execute_literal2.py']
common=texts['literal2_release_common.py'].decode();tree=ast.parse(common);constants={}
for node in tree.body:
 if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
  try:constants[node.targets[0].id]=ast.literal_eval(node.value)
  except(ValueError,TypeError):pass
for key,field in [('TARGET_SELECTED_PINS','literal2_fullpins'),('HISTORICAL_PINS','historical_evidence_pins'),('CURRENT_SELECTIONS','current_actual_selections'),('OWNER','literal_failed_owner_proof'),('CAPS','original_caps')]:assert constants[key]==sf[field],key
prov,provenancep=load(sf['strict_low_level_Source_provenance_pin']['path'],sf['strict_low_level_Source_provenance_pin'])
ob,op=read(prov['original_common_source_pin']['path'],prov['original_common_source_pin'])
blocks=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=blocks(common);b=blocks(ob.decode())
for name in prov['mechanically_cloned_method_names']:
 assert a[name]==b[name]and hashlib.sha256(a[name].encode()).hexdigest()==prov['method_source_SHA256'][name],name
role,rolep=load(sf['exact_role_plan_pin']['path'],sf['exact_role_plan_pin'])
assert role['literal2_target_pins']==sf['literal2_fullpins']and role['original_protected_indices']==[4166,4167]and role['new_original_protected_count']==7028
m,mp=load(sf['historical_evidence_pins']['previous7030_manifest']['path'],sf['historical_evidence_pins']['previous7030_manifest'])
oldrows=m['current_protected_full_EOF_pins'];targets=sf['literal2_fullpins']
assert len(oldrows)==7030 and [oldrows[k]for k in(4166,4167)]==targets
paths={q['path']for q in targets};nodes={tuple(q['identity'][:2])for q in targets}
assert len(paths)==2 and len(nodes)==2 and sum(q['size_bytes']for q in targets)==528482632
assert [Path(q['path']).name for q in targets]==['BQ64-MAC-ST','BQ64-SRC-ST']
for q in targets:
 s=Path(q['path']).lstat();assert seven(s)==q['identity']and s.st_uid==os.getuid()and s.st_nlink==1 and stat.S_ISREG(s.st_mode)
active={};selected=[]
for ix,q in enumerate(oldrows):
 if ix not in(4166,4167):
  assert q['path']not in paths and tuple(q['identity'][:2])not in nodes and seven(Path(q['path']).lstat())==q['identity']
  active[q['path']]=norm(q)
for selection in sf['current_actual_selections']:
 hf,hfp=load(selection['Host_freeze_pin']['path'],selection['Host_freeze_pin'])
 report,rp=load(selection['actual_report_pin']['path'],selection['actual_report_pin'])
 _,cp=load(selection['exact_cli_pin']['path'],selection['exact_cli_pin'])
 assert len(hf['dependencies'])==selection['expected_dependency_count']and len(report['fixed_current_pins'])==selection['actual_fixed_count']and len(report['output_pins'])==selection['actual_output_count']
 assert report['status']==selection['actual_status']and report['failure']==selection['actual_failure']and report['actual_host_Source_freeze_pin']==selection['Host_freeze_pin']
 rows=[selection['Host_freeze_pin'],selection['actual_report_pin'],selection['exact_cli_pin'],hf['host_source']]+hf['dependencies']+report['fixed_current_pins']+report['output_pins']
 for q in rows:
  assert q['path']not in paths and tuple(q['identity'][:2])not in nodes and seven(Path(q['path']).lstat())==q['identity']
  assert q['path']not in active or active[q['path']]==norm(q)
  active[q['path']]=norm(q)
 selected.append(dict(role=selection['role'],host_freeze_pin=hfp,actual_report_pin=rp,dependency_count=len(hf['dependencies']),fixed_count=len(report['fixed_current_pins']),output_count=len(report['output_pins'])))
for q in role['failed_public5_both_bundles_remain_current_pins']:assert active[q['path']]==q
preparation,prepp=load(R/'ACTUAL_LITERAL2_OLD_V14_BQ_V2_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json')
assert preparation['observed_closed']is True and type(preparation['original_integer_exit_code'])is int and preparation['original_integer_exit_code']==0
actual=preparation['actual_source_preparation_return'];assert type(actual['exit_code'])is int and actual['exit_code']==0 and actual.get('session_id')is None
v=texts['verify_or_execute_literal2.py'].decode()
ordered=["value['next_target_intent']=dict(fullpin=row,fsynced_before_unlink=True,unlink_return_not_yet_observed=True);rp=s.update_owned(rp_path,value,rp)","fd=os.open(target.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)","actual=os.stat(target.name,dir_fd=fd,follow_symlinks=False)","os.unlink(target.name,dir_fd=fd)","value['deletion_records'].append(dict(original_fullpin=row,actual_unlink_returned=True));value['next_target_intent']=None;rp=s.update_owned(rp_path,value,rp)","value['deletion_records'][-1]['target_directory_fsync_attempted']=True;rp=s.update_owned(rp_path,value,rp)","os.fsync(fd)","value['deletion_records'][-1]['target_directory_fsync_returned']=True;rp=s.update_owned(rp_path,value,rp)","now=s.identity(os.fstat(fd))"]
positions=[v.index(piece)for piece in ordered];assert positions==sorted(positions)
for piece in ["p.add_argument('--execute',action='store_true')","sys.argv[1:].count('--execute')!=(1 if a.execute else 0)","if not a.execute:print(","s.writer_gate(protected)","actual.st_uid!=os.getuid()or actual.st_nlink!=1","first_fd_error=error;first_fd_tb=error.__traceback__;raise","raise first_fd_error.with_traceback(first_fd_tb)","before['regular_files']-after['regular_files']!=2","before['artifact_bytes']-after['artifact_bytes']!=s.BYTES","now[3]!=previous[3]-1","now[4]!=previous[4]-32","STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY"]:assert piece in v,piece
assert v.count('os.unlink(')==1 and 'unlink_not_yet_attempted'not in v
for piece in ["oldrows[i]for i in (4166,4167)","if i not in(4166,4167):add(p","len(before['ordinary_file_identities'])!=299","all_other297_v14","old_nested_JSON_historical_PF_not_live_dependencies=True","actual_seven_genuine_public_READ_controls_passed","['/bin/ps'","['/usr/sbin/lsof'","st_uid!=os.getuid()","current_'+selected['role']+'_entire_HF_ownHost_actual_fixed_output_summary_retained"]:assert piece in common,piece
caps=dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864)
assert sf['original_caps']==caps and sf['default_readonly']is True and sf['execute_requires_one_literal_flag']is True and sf['no_retry_or_overwrite']is True and sf['qualification_promoted']is False
report=dict(schema='INDEPENDENT_LITERAL2_OLD_FAILED_V14_BQ_V2_SOURCE_ONLY_REVIEW_V1',status='PASS_LITERAL2_OLD_V14_BQ_V2_SOURCE_ONLY_READY_FOR_ROOT_MANIFEST',failure=None,Source_freeze_pin=sfp,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,candidate_imported=False,manifest_prepared=False,readonly_verifier_executed=False,
 Source_pins=sourcepins,predecessor_Source_v1_freeze_pin=originalp,whole_inverse_pin=inversep,whole_inverse_matches_v1_entire_execute_bytes=True,common_and_prepare_wholebytes_unchanged=True,original_curated66_common_pin=op,six_low_level_original_method_sourcebytes_unchanged=True,low_level_provenance_pin=provenancep,role_plan_pin=rolep,
 actual_v2_Source_preparation_true_tools_pin=prepp,genuine_Source_preparation_integer_exit_code=actual['exit_code'],literal2_target_pins=targets,target_count=2,target_bytes=528482632,only_exact_old_failed_v14_owned_targets=True,original_previous7030_manifest_pin=mp,only_migrated_original_indices=[4166,4167],retained_original7028_current7_verified=True,
 retained_v14_complete_inventory_count=299,future_retained_v14_file_count=297,current_selection_metadata=selected,current_source_scope_protection_union_count=len(active),all_current_direct_HF_fixed_outputs_target_path_and_inode_disjoint=True,all_selected_current7_and_original7028_reobserved=True,failed_public5_two_physical_bundles_retained=True,whole_v12_and_other_v14_inventory_retained_by_current_protection=True,nested_historical_PF_never_promoted_to_business_DAG=True,
 default_readonly_and_exact_single_execute_token=True,only_one_literal_leaf_unlink_call_in_two_target_loop=True,source_review_tool_strict_integer0_and_observed_closed_gate=True,real_PS_lsof_rechecked_by_Root_before_MF_readonly_and_unlink=True,independent_live_writer_tools_not_run=True,
 fsynced_preunlink_intent_truthfully_claims_unlink_return_not_observed=True,actual_unlink_return_immediately_same_owned_fsynced_receipt_before_dirfsync=True,dirfsync_attempt_durably_recorded_before_syscall=True,dirfsync_return_durably_recorded_before_parent_postcheck_and_close=True,same_dirfd_NOFOLLOW_UID_nlink_all7_literal_leaf=True,first_dirfd_exception_object_traceback_preserved_against_close_exception=True,partial_failure_has_no_automatic_retry=True,APFS_exact_single_leaf_nlink_minus1_size_minus32_guard=True,two_leaves_same_parent_aggregate_nlink_minus2_size_minus64=True,all_unaffected_files_directories_and_symlinks_exact_inventory_guard=True,
 original_caps=caps,exact_family_byte_file_delta_and_original_full_fresh_reserve_guard=True,future_manifest_and_actual_receipts_None=True,qualification_promoted=False,all_file_descriptors_closed=True,
 limitations=['Only Source/metadata and current7 reviewed; no candidate data opened, no repeated science EOF and no PS/lsof run. Root must genuinely prepare MF/fullEOF, defaultreadonly, then separately authorized exact execute and actual postverification.','Retiring the two old private BQ paths loses their exact-path failed-run replay; all remaining results, science, raw logs and completed historical attestations remain protected.'])
OUT.mkdir(exist_ok=True);path=OUT/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert os.write(fd,data)==len(data);os.fsync(fd)
finally:os.close(fd)
_,q=read(path);print(json.dumps(dict(status=report['status'],review_pin=q,Source_freeze_pin=sfp,source_only=True,business_executed=False,candidate_files_opened=False,all_file_descriptors_closed=True)))
