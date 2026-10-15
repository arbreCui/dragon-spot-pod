"""Independent actual literal3 retirement facts; Source/metadata/stat only."""
import hashlib,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent.parent
OUT=Path(__file__).absolute().parent
START=time.monotonic();EOF=[]
def need(v,m):
 if v is not True:raise RuntimeError(m)
def budget():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(peak<512*2**20 and time.monotonic()-START<600,'own original SELF512/stage600')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 need(type(p)is dict and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'Python integer current7')
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ident(s)==p['identity']and s.st_size==p['size_bytes']and not any(z.is_symlink()for z in(q,*q.parents)),'ordinary current exact7; original tool nlinks preserved')
 return q
def ownpin(p):
 b=p.read_bytes();s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ident(s))
def full(p,parse=False):
 q=current(p);need(p['size_bytes']<8*2**20,'Source/report metadata8MiB only');fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0;parts=[]
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b);parts.append(b);budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'Source/report metadata EOF SHA');current(p);EOF.append(p)
 return json.loads(b''.join(parts))if parse else b''.join(parts)
def typed(wrapper,key,code):
 r=wrapper[key];need(wrapper['observed_closed']is True and type(wrapper['original_integer_exit_code'])is int and wrapper['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and'session_id'not in r,'genuine closed typed return');return r

def main():
 a=full(ownpin(BASE/'AUTHOR_SOURCE_FREEZE.json'),True);ps=a['whole_Source_pin'];pp=a['whole_plan_pin'];full(ps);plan=full(pp,True)
 need(a['schema']=='ROOT_AUTHOR_LITERAL3_COMPLETED_A_ASCII_RETIREMENT_SOURCE_FREEZE_V2'and a['prior_readonly_original_integer_exit_code']==1 and a['prior_failure_preserved']is True,'v2 immutable author')
 execution_tools=full(ownpin(BASE/'ROOT_EXECUTION_TRUE_TOOL_RETURNS.json'),True);ret=typed(execution_tools,'actual_execution_return',0)
 need(ret['chunk_id']=='ef0657'and execution_tools['actual_execution_permission_mode']=='require_escalated'and execution_tools['execute_invoked']is True and execution_tools['files_deleted']is True and execution_tools['original_readonly_failure_preserved']is True,'actual authorized retirement0')
 er=json.loads(ret['output']);receipt_pin=er['receipt_pin'];need(receipt_pin['path']==str(BASE/'EXECUTION_RECEIPT.json'),'literal execution receipt');receipt=full(receipt_pin,True)
 need(receipt['schema']=='LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']==er['status']=='RETIRED_EXACT_LITERAL3_COMPLETED_A_ASCII_EXPORTS_ONLY'and receipt['failure']is None,'actual success receipt')
 targets=plan['target_pins'];need(len(targets)==3 and receipt['exact_target_pins']==receipt['actual_released_pins']==targets and receipt['actual_released_bytes']==er['actual_released_bytes']==sum(p['size_bytes']for p in targets)==346861973,'only exact3 actual bytes')
 prefix=Path('/Users/wen/spot/validation/artifacts/axial-material-new-current-formal-material-observations-short-FIL-after-v18-saved370-20261014-v10/A')
 need([p['path']for p in targets]==[str(prefix/n)for n in ['microlib.ascii','macro.ascii','metadata.ascii']]and all(not os.path.lexists(p['path'])for p in targets),'all literal3 paths absent')
 need(receipt['source_pin']==ps and receipt['plan_pin']==pp and receipt['retained_current7_pins']==plan['retained_current7_pins']and receipt['closure_pins']==plan['closure_pins']and receipt['complete_joint_roots']==plan['complete_joint_roots'],'receipt exact frozen inputs')
 owner=receipt['actual_lsof_owner_check'];need(owner['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]and type(owner['returncode'])is int and owner['returncode']==1 and owner['stdout']==''and owner['stderr']=='','actual immediate no-open-owner evidence')
 peer=full(receipt['peer_review_pin'],True);pt=full(ownpin(BASE/'independent_source_review_20261015/TRUE_TOOL_RETURNS.json'),True);pr=typed(pt,'actual_review_return',0)
 need(peer['status'].startswith('PASS')and peer['failure']is None and peer['source_pin']==ps and peer['plan_pin']==pp and json.loads(pr['output'])['review_pin']==receipt['peer_review_pin'],'original independent Source peer0')
 readonly_tools=full(ownpin(BASE/'ROOT_READONLY_TRUE_TOOL_RETURNS.json'),True);rr=typed(readonly_tools,'actual_readonly_return',0);rv=json.loads(rr['output']);check=full(rv['receipt_pin'],True)
 need(rr['chunk_id']=='b8cd2f'and readonly_tools['execute_invoked']is False and readonly_tools['files_deleted']is False and check['mode']=='check'and check['status']=='READONLY_READY_EXACT_LITERAL3_A_EXPORTS'and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['peer_review_pin']==receipt['peer_review_pin']and check['exact_target_pins']==targets and check['actual_released_pins']==[]and check['actual_released_bytes']==0,'true prior readonly0 no execute')
 first=full(plan['prior_readonly_failure_true_tools_pin'],True);fr=typed(first,'actual_readonly_return',1);failed=full(plan['prior_failed_readonly_receipt_pin'],True)
 need(fr['chunk_id']=='b3f004'and first['execute_invoked']is False and first['files_deleted']is False and failed['status']=='FAILED_BEFORE_UNLINK'and failed['actual_released_pins']==[]and failed['actual_released_bytes']==0,'original failure1 preserved no deletion')
 need(failed['source_pin']==plan['prior_failed_Source_pin']and failed['plan_pin']==plan['prior_failed_plan_pin'],'original v1 provenance')
 full(plan['prior_failed_Source_pin']);full(plan['prior_failed_plan_pin']);full(plan['prior_Source_peer_pin']);full(plan['prior_Source_peer_tools_pin']);full(plan['original_production_inputs_Source_pin']);full(plan['original_production_resource_Source_pin']);full(plan['original_history_resource_Source_pin'])
 mother=full(plan['current62_plan_pin'],True);candidate=full(plan['candidate_audit_pin'],True)
 need(plan['complete_joint_roots']==mother['complete_joint_roots']and len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==62,'complete62 unchanged no reset')
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
 need(plan['original_caps']==mother['original_caps']==caps,'original caps unchanged')
 retained=plan['retained_current7_pins'];docs=plan['retained_identity_only_roles'];meta=plan['explicit_cumulative_metadata_file_pins'];need(len(retained)==80 and len(docs)==43,'full preserved roles')
 rmap={p['path']:p for p in retained};need(all(rmap[p['path']]==p for p in candidate['exact_target_pins'][:14]),'all HOLD14 pairs still live')
 for k in ['retained_final55_SQLite_pin','retained_final55_pool_pin','retained_final55_observer_XSM_pin','retained_original_A_material_XSM_pin']:
  p=candidate[k];need(rmap[p['path']]==p,'final55/original material role retained')
 for p in candidate['retained_seven_original_XSM_pins']:need(rmap[p['full_pin']['path']]==p['full_pin'],'seven original observer XSMs retained')
 expect={p['path']:dict(path=p['path'],size_bytes=p['size_bytes'],identity=p['current7'])for p in candidate['preserved_result_JSONL_current7']};need({p['path']:p for p in docs}==expect,'all43 results identity preserved')
 need(sum('.context.bin'in p['path']for p in retained)==55 and sum(p['path'].endswith('.xsm')for p in retained)==9,'55contexts plus9XSM fullPF roles')
 need(receipt['raw_export_lifecycle_only']is True and receipt['duplicate_byte_identity_claim']is False and receipt['all14_earlier_SQL_pool_files_retained']is True and receipt['original_A_aggregate_issue1_preserved']is True,'honest export lifecycle and issue history')
 for k in ['business_executed','numerical_executed','compiler_executed','physics_qualified','AAA_qualified','ABA_admitted','goal_complete']:need(receipt[k]is False,'all qualification/execution flags remainfalse '+k)
 for p in retained+docs+meta:current(p)
 for name,snap in [('before',receipt['resources_before']),('after',receipt['resources_after'])]:
  need(snap['SELF_peak_bytes']<512*2**20 and 0<=snap['elapsed_seconds']<600 and snap['joint_bytes']+snap['external_metadata_bytes']+snap['open_unlinked_bytes']<2*2**30,'original actual execution budget '+name)
  need(snap['history_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and snap['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original actual reservation '+name)
 total=0
 for root in plan['complete_joint_roots']:
  for dp,ds,fs in os.walk(root,followlinks=False):
   for n in fs:
    p=Path(dp)/n;s=p.lstat();need(stat.S_ISREG(s.st_mode),'regular counted namespace');total+=s.st_size;budget()
 external=sum(p['size_bytes']for p in meta if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']))
 need(total+external<2*2**30,'fresh stat current62 + existing external metadata within2GiB')
 unique={p['path']:p for p in EOF}
 for p in unique.values():full(p)
 for p in retained+docs+meta:current(p)
 need(all(not os.path.lexists(p['path'])for p in targets),'target absence verified twice')
 report=dict(schema='INDEPENDENT_ACTUAL_LITERAL3_A_ASCII_EXPORT_RETIREMENT_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_EXACT_LITERAL3_A_ASCII_EXPORT_RETIREMENT_346861973B_METADATA_ONLY',failure=None,metadata_only=True,reviewer_source_pin=ownpin(Path(__file__).absolute()),actual_retirement_receipt_pin=receipt_pin,actual_Root_execution_tools_pin=ownpin(BASE/'ROOT_EXECUTION_TRUE_TOOL_RETURNS.json'),actual_Root_return=ret,actual_Root_integer_exit_code=0,actual_Root_execution_permission='require_escalated',actual_readonly_return=rr,actual_readonly_integer_exit_code=0,original_prior_readonly_return=fr,original_prior_readonly_integer_exit_code=1,prior_failed_readonly_receipt_pin=plan['prior_failed_readonly_receipt_pin'],Source_peer_actual_return=pr,exact_target_pins=targets,actual_released_pins=targets,actual_released_bytes=346861973,all3_target_paths_absent_verified_twice=True,actual_lsof_owner_check=owner,Source_and_metadata_full_EOF_SHA_current7_twice_pins=list(unique.values()),Source_and_metadata_full_EOF_count=len(unique),retained_scientific_fullPF_current7_pins=retained,retained_scientific_role_count=80,preserved_result_document_current7_roles=docs,preserved_result_document_count=43,inherited_metadata_current7_only_count=len(meta),all14_earlier_SQL_pool_files_still_live=True,all55_contexts_and9_XSMs_still_live=True,all43_result_JSONL_preserved=True,original_A_aggregate_issue1_preserved=True,complete_joint_roots=plan['complete_joint_roots'],original_caps=caps,actual_receipt_resources_before=receipt['resources_before'],actual_receipt_resources_after=receipt['resources_after'],receipt_resource_snapshots_are_original_sampled_values_not_relabelled_as_post_unlink_current_bytes=True,fresh_stat_current62_joint_bytes=total,external_metadata_bytes=external,resource_scope='Current namespace stat only; no helper/resource factory import or fresh history/body replay',scientific_bodies_opened=False,scientific_body_SHA_recomputed=False,XSM_SQL_pool_or_JSONL_body_opened=False,check_or_execute_repeated=False,PS_executed=False,lsof_executed_by_peer=False,native_or_compiler_executed=False,files_deleted_by_peer=False,actual_Root_files_deleted=True,no_byte_identical_duplicate_claim=True,future_exact_retirement_receipt_admission_required=True,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024),wall_seconds=time.monotonic()-START,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 path=OUT/'REVIEW.json';need(not path.exists(),'own post once');raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20,'post8MiB')
 with path.open('xb')as stream:stream.write(raw)
 print(json.dumps(dict(status=report['status'],review_pin=ownpin(path))),flush=True)
if __name__=='__main__':main()
