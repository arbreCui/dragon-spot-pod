#!/usr/bin/env python3
import json,hashlib,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
S=R/'storage_release_literal2_old_v14_BQ_source_v2_20261014';D=R/'independent_literal2_old_v14_BQ_v2_final_MF_readonly_review_20261014'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return{k:q[k]for k in('path','sha256','size_bytes','identity')}
def read(p,q=None):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 with p.open('rb')as f:assert ids(os.fstat(f.fileno()))==ids(s);b=f.read();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);pf=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
 if q is not None:assert pf==norm(q),str(p)
 return b,pf
def load(p,q=None):
 b,pf=read(p,q);return json.loads(b),pf
def current(q):
 p=Path(q['path']);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and ids(s)==q['identity'],str(p)
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
m,mp=load(S/'EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json')
assert mp['sha256']=='2d9ea9a1c7dace6c79cbc23f360f9e020d85b488a2a0f19d4f5272fd477c435a'and mp['size_bytes']==5657320
assert mp['identity']==[16777229,50074397,33188,1,5657320,1791909596968265682,1791909596968265682]
ro,rop=load(R/'storage_release_literal2_old_v14_BQ_actual_receipts_20261014/READONLY_EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_OLD_PRIVATE_VERIFICATION_RECEIPT.json')
assert rop['sha256']=='b0a7d908d93439e35c9cec8971b04501edd18b90e477e7389363039f10ef6036'and rop['size_bytes']==182903
assert ro['status']=='READONLY_LITERAL2_ALL_CURRENT_EOF_VERIFIED'and ro['manifest_pin']==mp and ro['execute_requested']is False and ro['deletion_records']==[]and ro['next_target_intent']is None and ro['compiler_or_business_executed']is False
sf,sfp=load(m['selected_Source_freeze_pin']['path'],m['selected_Source_freeze_pin'])
assert sfp['sha256']=='b479562621c520def2825c349cb9312e93c77a2612bc55bc06f49f158fe7b58c'and m['Source_pins']==sf['Source_pins']
for q in sf['Source_pins']:read(q['path'],q)
assert m['target_count']==2 and m['target_logical_bytes']==528482632 and m['target_full_EOF_pins']==sf['literal2_fullpins']
assert m['draft_only']is False and m['action_executed']is False and m['compiler_or_business_executed']is False
targets=m['target_full_EOF_pins'];protected=m['current_protected_full_EOF_pins'];retained=m['retained_all_other_v14_files_full_EOF_pins'];dag=m['Source_DAG_provenance']
assert len(protected)==7251 and len({q['path']for q in protected})==7251 and len(retained)==297
table={q['path']:norm(q)for q in protected};paths={q['path']for q in targets};nodes={tuple(q['identity'][:2])for q in targets}
assert len(paths)==2 and len(nodes)==2
for q in protected:current(q);assert q['path']not in paths and tuple(q['identity'][:2])not in nodes
for q in targets:
 s=Path(q['path']).lstat();assert ids(s)==q['identity']and s.st_uid==os.getuid()and s.st_nlink==1 and stat.S_ISREG(s.st_mode)
old,oldp=load(sf['historical_evidence_pins']['previous7030_manifest']['path'],sf['historical_evidence_pins']['previous7030_manifest'])
oldrows=old['current_protected_full_EOF_pins'];assert len(oldrows)==7030 and [oldrows[i]for i in(4166,4167)]==targets
for ix,q in enumerate(oldrows):
 if ix not in(4166,4167):assert table[q['path']]==norm(q)
assert dag['previous_protected_count']==7030 and dag['only_two_original_indices_migrated_to_historical']==[4166,4167]
for key in ['all_original_other7028_PF_rows_data_retained','historical_original7030_and_v14_299_attestation_not_rewritten','protected_all_current_success_and_failed_public5_actual_outputs','old_nested_JSON_historical_PF_not_live_dependencies']:assert dag[key]is True
before=m['complete_before_inventory'];v14=Path(sf['literal_failed_owner_proof']['root'])
assert before==dag['current_v14_complete_inventory']==old['Source_DAG_provenance']['current_v14_complete_inventory']
assert len(before['ordinary_file_identities'])==299 and not before['symlinks']
assert inventory(v14)==before
v12=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12')
assert inventory(v12)==dag['current_v12_complete_inventory']==old['Source_DAG_provenance']['current_v12_complete_inventory']
assert {q['path']:q['identity']for q in retained}=={p:i for p,i in before['ordinary_file_identities'].items()if p not in paths}
for q in retained:assert table[q['path']]==norm(q)
roles=dag['roles']
for key,entries in roles.items():
 assert len(entries)==len(set(entries))and all(path in table for path in entries)
for sel in sf['current_actual_selections']:
 hf,hfp=load(sel['Host_freeze_pin']['path'],sel['Host_freeze_pin']);actual,ap=load(sel['actual_report_pin']['path'],sel['actual_report_pin'])
 for q in[sel['Host_freeze_pin'],sel['actual_report_pin'],sel['exact_cli_pin'],hf['host_source']]+hf['dependencies']+actual['fixed_current_pins']+actual['output_pins']:
  assert table[q['path']]==norm(q),q['path']
 if sel['role']=='public5_failed':
  assert actual['actual_seven_genuine_public_READ_controls_passed']is False
  bundles=[q for q in actual['output_pins']if q['path'].endswith('coherent_complete_context.xsm')]
  assert len(bundles)==2 and all(q['size_bytes']==100163528 and table[q['path']]==q for q in bundles)
preptool,preptoolp=load(R/'ROOT_LITERAL2_V2_ACTUAL_MANIFEST_PREPARATION_TRUE_TOOL_RETURNS_20261014.json')
rotool,rotoolp=load(R/'ROOT_LITERAL2_V2_DEFAULT_READONLY_TRUE_TOOL_RETURNS_20261014.json')
for tool,prefix,terminalchunk,session in [(preptool,'3ebc91','c40113',35689),(rotool,'70dcd6','5fe867',48609)]:
 assert tool['actual_initial_return']['chunk_id']==prefix and tool['actual_initial_return']['session_id']==session
 tr=tool['actual_terminal_return'];assert tr['chunk_id']==terminalchunk and type(tr['exit_code'])is int and tr['exit_code']==0 and tr.get('session_id')is None and tool['deletion_executed']is False
prepare_output=json.loads(preptool['actual_terminal_return']['output'].strip().splitlines()[-1]);assert prepare_output['manifest_pin']==mp and prepare_output['protected_count']==7251 and prepare_output['retained_other_count']==297 and prepare_output['deletion_executed']is False
readonly_output=json.loads(rotool['actual_terminal_return']['output'].strip().splitlines()[-1]);assert readonly_output['receipt_pin']==rop and readonly_output['deletion_executed']is False
prep_argv,prep_argvp=load(R/'ROOT_EXACT_LITERAL2_V2_MANIFEST_PREPARE_ARGV_20261014.json')
release_argv,release_argvp=load(R/'ROOT_EXACT_LITERAL2_V2_READONLY_AND_EXECUTE_ARGV_20261014.json')
assert shlex.split(preptool['exact_executed_command'])==prep_argv['argv']
readonly=shlex.split(rotool['exact_executed_command'])
assert '--execute'not in readonly
env=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B']
assert readonly[:11]==env and readonly[11]==str(S/'verify_or_execute_literal2.py')and len(readonly)==16
assert readonly[12:15]==['--manifest-sha256',mp['sha256'],'--manifest-seven-id']and json.loads(readonly[15])==mp['identity']
review_evidence=[]
for who,q,t in m['selected_literal2_Source_reviews']:
 d,dp=load(q['path'],q);tool,tp=load(t['path'],t)
 ar=tool['actual_review_return'];assert d['Source_freeze_pin']==sfp and d['failure']is None and d['business_executed']is False
 assert tool['observed_closed']is True and type(tool['original_integer_exit_code'])is int and tool['original_integer_exit_code']==0 and type(ar['exit_code'])is int and ar['exit_code']==0 and ar.get('session_id')is None
 assert norm(json.loads(ar['output'].strip().splitlines()[-1])['review_pin'])==q
 review_evidence.append(dict(role=who,review_pin=dp,true_tool_pin=tp,actual_review_return=ar))
budget=ro['original_budget_before'];mbudget=m['original_budget_before_preparation']
for b in[budget,mbudget]:
 assert b['artifact_budget_bytes']==103079215104 and b['min_free_bytes']==8589934592 and b['original_cold_reserve_bytes']==20971764748 and b['metadata_reserve_bytes']==67108864 and b['initial_fresh_reserve_bytes']==2147483648
 assert b['artifact_bytes']<=103079215104 and b['disk_free_bytes']>=8589934592
 expected=103079215104-b['artifact_bytes']-20971764748-67108864-2147483648
 assert expected==b['remaining_after_original_initial_reserves_bytes']and b['original_initial_reserve_admitted']==(expected>0)
assert budget['artifact_bytes']==mbudget['artifact_bytes']and budget['regular_files']==mbudget['regular_files']
expected_after_reserve=budget['remaining_after_original_initial_reserves_bytes']+528482632
assert expected_after_reserve>0
for q in protected:current(q)
for q in targets:current(q)
for q in[sfp,mp,rop,preptoolp,rotoolp,prep_argvp,release_argvp]:current(q)
assert inventory(v14)==before
report=dict(schema='INDEPENDENT_LITERAL2_OLD_V14_BQ_V2_FINAL_MANIFEST_READONLY_REVIEW_V1',status='PASS_LITERAL2_V2_FINAL_MANIFEST_GENUINE_READONLY_CURRENT_PF_VERIFIED',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,candidate_imported=False,candidate_files_opened=False,
 manifest_pin=mp,Source_freeze_pin=sfp,readonly_receipt_pin=rop,genuine_manifest_preparation_tool_pin=preptoolp,genuine_default_readonly_tool_pin=rotoolp,actual_manifest_preparation_return=preptool['actual_terminal_return'],actual_default_readonly_return=rotool['actual_terminal_return'],manifest_prepare_CLI_pin=prep_argvp,readonly_and_future_execute_CLI_pin=release_argvp,actual_default_readonly_argv=readonly,
 target_count=2,target_bytes=528482632,exact_target_pins=targets,targets_present_current_UID_regular_singlelink_all7=True,target_paths_and_physical_inodes_disjoint_from_all_protection=True,
 current_protected_count=7251,all7251_current7_reobserved_twice=True,original7030_only_exact4166_4167_historical_migration=True,original_other7028_full_PF_rows_retained=True,retained_other_v14_files=297,complete_v14_file_count=299,complete_v14_directory_count=len(before['directory_identities']),symlinks_count=0,retained297_exact_inventory_and_current7=True,complete_v14_inventory_reobserved_twice=True,complete_v12_inventory_unchanged=True,all4_current_HFs_fixed_outputs_Source_and_failed_public5_scene_retained=True,failed_public5_both_context_bundles_current=True,
 genuine_root_and_independent_Source0_review_evidence=review_evidence,original_caps=sf['original_caps'],original_budget_before=budget,expected_reserve_after_future_exact2_release_bytes=expected_after_reserve,expected_future_release_not_claimed_actual=True,
 default_readonly_no_delete_proven_by_command_and_receipt=True,execute_requires_one_literal_flag_remains_Root_only=True,
 independent_PS_lsof_not_repeated=True,Root_genuine_PS_lsof_fullEOF_evidence_bound_to_MF_and_readonly_tools=True,independent_science_fullEOF_repeated=False,all_file_descriptors_closed=True,
 limitation='This is pre-execution final Source/MF/read-only verification. No file has been deleted by this reviewer. Root must rerun the frozen execute safety guards, then obtain an actual exact2 release receipt and postverify the real delta.')
D.mkdir(exist_ok=True);path=D/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert os.write(fd,data)==len(data);os.fsync(fd)
finally:os.close(fd)
_,q=read(path);print(json.dumps(dict(status=report['status'],review_pin=q,manifest_pin=mp,current_protected_count=7251,retained_other_v14_count=297,target_files_opened=False,all_file_descriptors_closed=True,deletion_executed=False)))
