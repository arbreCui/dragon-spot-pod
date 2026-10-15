"""Independent finite read-only postcheck. Never enters the active v5 output.
Reuse original strict full-EOF pin and SELF guards; independently derive branch
entry deltas and terminal-receipt consistency. No current history scan.
"""
import hashlib,importlib.util,json,os,stat,time
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');P=R/'storage_release_v3_seven_and_optional_maps_20261012';OWN=P/'independent_postverify'
ACTIVE=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v5')
spec=importlib.util.spec_from_file_location('original_readonly_storage_pin_and_SELF_guard',R/'storage_release_20261012/storage_release_common.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
start=time.monotonic()
def allowed(path):
 p=Path(path)
 if p==ACTIVE or ACTIVE in p.parents:raise RuntimeError('active v5 output must not be read')
 return p
checks={}
def same(row):
 allowed(row['path']);c.same(row)
 previous=checks.get(row['path'])
 if previous is not None and previous!=row:raise RuntimeError('conflicting supposedly retained current pin')
 checks[row['path']]=row

def read(path,sha=None):
 allowed(path);p=c.pin(path)
 if sha is not None and p['sha256']!=sha:raise RuntimeError('selected original exact metadata hash')
 checks[p['path']]=p
 return c.read_pinned_json(p),p

def inventory(branch):
 allowed(branch);files={};links={};dirs={};todo=[branch]
 while todo:
  root=todo.pop();allowed(root);c.ancestors(root);before=root.lstat()
  if not stat.S_ISDIR(before.st_mode):raise RuntimeError('closed branch ordinary dir expected')
  dirs[str(root)]=c.identity(before)
  fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   if c.identity(os.fstat(fd))!=dirs[str(root)]:raise RuntimeError('directory changed at safe open')
   with os.scandir(fd) as iterator:
    for entry in iterator:
     p=root/entry.name;allowed(p);st=entry.stat(follow_symlinks=False)
     if stat.S_ISDIR(st.st_mode):todo.append(p)
     elif stat.S_ISREG(st.st_mode):files[str(p)]=c.identity(st)
     elif stat.S_ISLNK(st.st_mode):links[str(p)]={'identity':c.identity(st),'target':os.readlink(p)}
     else:raise RuntimeError('unexpected special file in closed branch')
  finally:os.close(fd)
  if c.identity(root.lstat())!=dirs[str(root)]:raise RuntimeError('closed directory changed during independent inventory')
  c.guard()
 return {'ordinary_file_identities':files,'symlinks':links,'directory_identities':dirs}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
terminal,tp=read(P/'ROOT_ACTUAL_TWO_BATCH_TRUE_CLOSED_TOOL_RETURNS.json')
addon,ap=read(P/'ADDITIONAL_CURRENT_V5_SOURCE_DAG_DISJOINT_PROOF.json','e987f9029d93aebcf96d44f194df14acdca40a2fbed38815c4b4972f382bed9a')
assert len(addon['additional_v5_current_full_EOF_pins'])==38
for p in addon['additional_v5_current_full_EOF_pins']+addon['guard_wrapper_and_unchanged_original_Source_pins']:same(p)
rows=[('failed-v3-seven','EXACT_7_FAILED_V3_INPUT_COPY_MANIFEST.json','6d7613ef455feb1bcaea53e43a5d92bfa42231f41da6527c24e3e0b9b349aa85','failed_v3_seven',7,499457228,63,0),('optional-map003004-six','EXACT_6_OPTIONAL_MAP003004_RAW_MANIFEST.json','707a960fab2e5114e2baf0851b03c65c974de7f9870408cedc3db02fc1097b9c','optional_map003004_six',6,1427734232,347,89)]
reports=[];closed=[];protected=None
for batch,filename,sha,key,count,size,retained_count,linkcount in rows:
 m,mp=read(P/filename,sha);e=terminal[key]
 assert e['terminal']['exit_code']==0 and 'session_id'in e['initial']
 # Only saved closed terminal stdout is parsed; no process or active output read.
 stdout=[json.loads(line)for line in e['terminal']['output'].splitlines()if line.strip()];assert len(stdout)==2
 saved=stdout[0]['receipt_pin'];same(saved);actual=c.read_pinned_json(saved)
 guardpin=stdout[1]['v5_guard_receipt_pin'];same(guardpin);guard=c.read_pinned_json(guardpin)
 assert actual['manifest_pin']==mp and actual['batch']==batch and actual['execute_requested']is True
 assert actual['status']=='EXACT_SELECTED_BATCH_RELEASE_AND_RETENTION_VERIFIED'
 assert actual['deleted_files']==count and actual['logical_bytes_released']==size
 assert len(actual['deletion_records'])==count
 assert [r['original_full_pin']for r in actual['deletion_records']]==m['target_full_EOF_pins']
 assert all(r['confirmed_absent']is True for r in actual['deletion_records'])
 assert guard['proof_pin']==ap and guard['selected_manifest_pin']==mp and guard['batch']==batch
 assert guard['status']=='V5_GUARD_BEFORE_AND_AFTER_COMPLETE_ORIGINAL_EXACT_EXECUTOR_COMPLETED'
 assert guard['before_full_EOF_verified']is True and guard['after_full_EOF_verified']is True and guard['original_executor_completed']is True
 assert guard['before_full_EOF_count']==43 and guard['after_full_EOF_count']==43
 assert guard['numerical_or_compiler_child_started']is False
 assert actual['all_other_raw_results_logs_Source_producers_retained']is True
 assert actual['parent_APFS_nlink_size_natural_entry_changes_verified']is True
 before=m['complete_before_inventory'];targets=m['target_full_EOF_pins'];targetpaths={r['path']for r in targets}
 assert len(targetpaths)==count and sum(p['size_bytes']for p in targets)==size
 assert all(not os.path.lexists(allowed(path))for path in targetpaths)
 branch=Path(next(iter(targetpaths))).parent
 if batch=='failed-v3-seven':branch=branch.parent
 else:branch=branch.parent.parent
 observed=inventory(branch)
 assert observed['ordinary_file_identities']=={path:identity for path,identity in before['ordinary_file_identities'].items()if path not in targetpaths}
 assert observed['symlinks']==before['symlinks'] and len(observed['symlinks'])==linkcount
 assert set(observed['directory_identities'])==set(before['directory_identities'])
 parentcounts={}
 for path in targetpaths:
  parent=str(Path(path).parent);parentcounts[parent]=parentcounts.get(parent,0)+1
 parentproof=[]
 for path,old in before['directory_identities'].items():
  new=observed['directory_identities'][path]
  if path in parentcounts:
   n=parentcounts[path];assert new[:3]==old[:3] and new[3]==old[3]-n and new[4]==old[4]-32*n
   assert new[5]>=old[5] and new[6]>=old[6]
   parentproof.append({'path':path,'before_identity':old,'after_identity':new,'ordinary_entries_removed':n,'nlink_delta':new[3]-old[3],'directory_size_byte_delta':new[4]-old[4]})
  else:assert new==old
 assert len(m['retained_ordinary_full_EOF_pins'])==retained_count
 assert {r['path']for r in m['retained_ordinary_full_EOF_pins']}==set(observed['ordinary_file_identities'])
 for pin in m['retained_ordinary_full_EOF_pins']+m['Source_pins']:same(pin)
 if protected is None:protected=m['current_protected_full_EOF_pins']
 else:assert protected==m['current_protected_full_EOF_pins']
 assert len(protected)==3783
 b,a=actual['original_budget_before'],actual['original_budget_after']
 assert b['artifact_bytes']-a['artifact_bytes']==size and b['regular_files']-a['regular_files']==count
 assert b['artifact_budget_bytes']==a['artifact_budget_bytes']==96*2**30
 assert b['min_free_bytes']==a['min_free_bytes']==8*2**30
 assert a['disk_free_bytes']>a['min_free_bytes'] and a['artifact_bytes']<a['artifact_budget_bytes']
 assert a['original_cold_reserve_bytes']==20971764748 and a['metadata_reserve_bytes']==64*2**20 and a['initial_fresh_reserve_bytes']==2*2**30
 assert a['remaining_after_original_initial_reserves_bytes']==96*2**30-a['artifact_bytes']-20971764748-64*2**20-2*2**30
 closed.append((b,a))
 reports.append({'batch':batch,'manifest_pin':mp,'actual_release_receipt_pin':saved,'v5_guard_receipt_pin':guardpin,'true_terminal_initial_and_final_chunk_ids':[e['initial']['chunk_id'],e['terminal']['chunk_id']],'actual_deleted_count':count,'actual_deleted_logical_bytes':size,'exact_after_branch_inventory_SHA256':digest(observed),'all_retained_ordinary_full_EOF_verified_count':retained_count,'all_symlinks_identity_and_target_unchanged_count':linkcount,'all_other_directories_exactly_unchanged':True,'exact_APFS_parent_nlink_and_entry_size_deltas':parentproof,'actual_saved_closed_history_delta_only':{'before_bytes':b['artifact_bytes'],'after_bytes':a['artifact_bytes'],'before_files':b['regular_files'],'after_files':a['regular_files']}})
for p in protected:same(p)
assert closed[0][1]['artifact_bytes']==closed[1][0]['artifact_bytes'] and closed[0][1]['regular_files']==closed[1][0]['regular_files']
last=closed[-1][1];assert last['artifact_bytes']==78269060170 and last['regular_files']==94837 and last['remaining_after_original_initial_reserves_bytes']==1623797674 and last['disk_free_bytes']==210944000000
bad=reports[0];first=json.loads(Path(bad['manifest_pin']['path']).read_bytes());bp=first['Source_DAG_provenance']['invalid_v3_PACK_explicit_full_pin_retained'];same(bp)
assert bp in first['retained_ordinary_full_EOF_pins']
# A second finite stable closed inventory; immutable pins checked again to EOF.
for batch,filename,sha,key,count,size,retained_count,linkcount in rows:
 m=json.loads((P/filename).read_bytes());sample=Path(next(iter(m['target_full_EOF_pins']))['path']).parent
 branch=sample.parent if batch=='failed-v3-seven' else sample.parent.parent
 assert digest(inventory(branch))==next(r['exact_after_branch_inventory_SHA256']for r in reports if r['batch']==batch)
for pin in list(checks.values()):c.same(pin)
source=c.pin(Path(__file__));total=sum(r['actual_deleted_logical_bytes']for r in reports)
report={'schema':'INDEPENDENT_TWO_CLOSED_EXACT_STORAGE_BATCH_POSTVERIFY_V1','status':'INDEPENDENT_FULL_EOF_RETENTION_AND_EXACT13_DELETION_VERIFIED','own_readonly_Source_pin':source,'closed_true_tool_returns_pin':tp,'current_v5_additional_protection_proof_pin':ap,'batches':reports,'actual_deleted_total_files':13,'actual_deleted_total_logical_bytes':total,'common_current_protected_full_EOF_count':3783,'additional_v5_current_full_EOF_count':38,'unique_retained_current_metadata_and_Source_full_EOF_count':len(checks),'unique_full_EOF_bytes_verified':sum(p['size_bytes']for p in checks.values()),'unique_checked_pin_table_SHA256':digest(sorted(checks.values(),key=lambda p:p['path'])),'retained_invalid_v3_PACK_exact_full_pin':bp,'saved_closed_after_budget_only':{k:last[k]for k in ['checked_unix','artifact_bytes','regular_files','disk_free_bytes','artifact_budget_bytes','min_free_bytes','original_cold_reserve_bytes','metadata_reserve_bytes','initial_fresh_reserve_bytes','remaining_after_original_initial_reserves_bytes','original_initial_reserve_admitted']},'current_global_history_not_scanned_while_pipeline5_running':True,'active_pipeline5_output_not_read':True,'no_file_deleted_or_execution_retried':True,'no_numerical_or_compiler_business_executed':True,'all_original_SELF_RSS_elapsed_guards_preserved':True,'physics_or_pipeline_qualification_created':False,'goal_complete':False,'elapsed_seconds':time.monotonic()-start}
out=OWN/'INDEPENDENT_TRUE_CLOSED_TWO_BATCH_POSTVERIFY.json';c.write_new(out,report);print(json.dumps({'status':report['status'],'report_pin':c.pin(out),'unique_fullpin_count':len(checks),'unique_fullpin_bytes':report['unique_full_EOF_bytes_verified'],'deleted_count':13,'deleted_bytes':total,'closed_remaining_after_original_initial_reserves_bytes':last['remaining_after_original_initial_reserves_bytes'],'elapsed_seconds':report['elapsed_seconds']}))
