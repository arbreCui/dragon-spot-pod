"""Bounded independent Source/metadata audit; no candidate import or cleanup."""
import ast,hashlib,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent.parent
OUT=Path(__file__).absolute().parent
START=time.monotonic()
SCI_BODIES_OPENED=False
FULL=[]
def need(v,m):
 if v is not True:raise RuntimeError(m)
def budget():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(peak<512*2**20 and time.monotonic()-START<600,'own original SELF512/stage600')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 need(type(p)is dict and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'exact Python integer PF')
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ident(s)==p['identity']and s.st_size==p['size_bytes']and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents)),'current7 ordinary file')
 return q

def own_pin(q):
 b=q.read_bytes();s=q.stat();return dict(path=str(q),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ident(s))
def full(p,parse=False):
 q=current(p);need(p['size_bytes']<8*2**20,'Source/metadata8MiB only')
 fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();parts=[];n=0
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b);parts.append(b);budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'Source/metadata EOF SHA')
 current(p);FULL.append(p);raw=b''.join(parts)
 return json.loads(raw)if parse else raw

def main():
 author=own_pin(BASE/'AUTHOR_SOURCE_FREEZE.json');a=full(author,True)
 need(a['schema']=='ROOT_AUTHOR_LITERAL3_COMPLETED_A_ASCII_RETIREMENT_SOURCE_FREEZE_V1'and a['AST_parse_only_no_import']is True and a['check_or_execute_invoked']is False and a['Source_frozen_before_peer_review']is True and a['Root_is_only_retirement_executor']is True,'frozen author contract')
 ps=a['whole_Source_pin'];pp=a['whole_plan_pin'];raw=full(ps);plan=full(pp,True);candidate=full(plan['candidate_audit_pin'],True);mother=full(plan['current62_plan_pin'],True)
 tree=ast.parse(raw);need(ps['path']==str(BASE/'retire_completed_A_ASCII_exports.py')and pp['path']==str(BASE/'PLAN.json'),'literal Source/plan')
 need(plan['schema']=='LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_PLAN_V1'and plan['source_only']is True,'Source-only plan')
 eligible=candidate['exact_target_pins'][14:];need(len(eligible)==3 and plan['target_pins']==eligible and sum(p['size_bytes']for p in eligible)==plan['planned_released_bytes']==346861973,'exact eligible3; HOLD14 excluded')
 owner=Path('/Users/wen/spot/validation/artifacts/axial-material-new-current-formal-material-observations-short-FIL-after-v18-saved370-20261014-v10/A')
 need([p['path']for p in eligible]==[str(owner/n)for n in ['microlib.ascii','macro.ascii','metadata.ascii']],'only literal3 export paths')
 assign=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='TARGETS'for t in n.targets))
 need(isinstance(assign.value,ast.List)and len(assign.value.elts)==3,'static3 target list')
 for node,p in zip(assign.value.elts,eligible):
  need(isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='dict'and not node.args,'literal target dict')
  kw={x.arg:x.value for x in node.keywords};need(set(kw)=={'path','sha256','size_bytes','identity'},'full target keys')
  need(ast.unparse(kw['path'])=="str(PREFIX / '"+Path(p['path']).name+"')"and ast.literal_eval(kw['sha256'])==p['sha256']and ast.literal_eval(kw['size_bytes'])==p['size_bytes']and ast.literal_eval(kw['identity'])==p['identity'],'exact Source literal PF')
 need(plan['complete_joint_roots']==mother['complete_joint_roots']and len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==62,'complete62 unchanged prefix')
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
 need(plan['original_caps']==mother['original_caps']==caps,'all original caps unchanged')
 funcs={x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)}
 def snippet(name):return ast.get_source_segment(raw.decode(),funcs[name])
 b=snippet('main');need("receipt.open('xb')"in b and "choices=['check','execute']"in b,'exclusive once receipt and exact modes')
 for text in ['peak<512*2**20','time.monotonic()-started<600',"<2*2**30",'<96*2**30','>=8*2**30','20971764748','64*2**20','DynamicHistoryResources','DiskResources']:
  need(text in b,'same resource bound '+text)
 need("for p in TARGETS:full(p,budget)"in b,'Root blindEOF exact targets')
 unlink=[x for x in ast.walk(tree)if isinstance(x,ast.Call)and isinstance(x.func,ast.Attribute)and x.func.attr=='unlink'];need(len(unlink)==1 and ast.unparse(unlink[0])=='os.unlink(q.name, dir_fd=fd)','one literal dirfd unlink call')
 for text in ["r.returncode==1 and r.stdout==b''and r.stderr==b''","os.O_DIRECTORY|os.O_NOFOLLOW","os.stat(q.name,dir_fd=fd,follow_symlinks=False)","d['actual_released_pins'].append(p)","d['actual_released_bytes']+=p['size_bytes']","snapshot(f,d);budget()","FAILED_PARTIAL_EXACT_LITERAL3_A_EXPORTS","FAILED_BEFORE_UNLINK"]:
  need(text in b,'ownership/immediate7/partial journal '+text)
 need(b.index("r.returncode==1 and r.stdout==b''and r.stderr==b''")<b.index('os.unlink(q.name,dir_fd=fd)'),'lsof closure before any unlink')
 need("['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in TARGETS]"in b and 'timeout=30'in b,'bounded exact-target lsof')
 need("a.readonly_receipt_pin is not None"in b and "READONLY_READY_EXACT_LITERAL3_A_EXPORTS"in b,'execute requires prior exact readonly receipt')
 closure={k:full(p,True)for k,p in plan['closure_pins'].items()}
 closed=closure['completion_post'];rt=closure['completion_root_tools'];pt=closure['completion_post_tools'];manifest=closure['observation_manifest'];extract=closure['complete_extraction_report']
 need(closed['status']=='PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION'and closed['failure']is None and closed['actual_Root_integer_exit_code']==0 and closed['actual_original_Root_integer_exit_code']==1 and closed['actual_material_stage_closed0']is True and closed['actual_new_material_child_launch_count']==0,'completed actual native A; old Root1 retained')
 for wrapper,key in [(rt,'actual_terminal_return'),(pt,'actual_review_return')]:
  ret=wrapper[key];need(wrapper['observed_closed']is True and type(wrapper['original_integer_exit_code'])is int and wrapper['original_integer_exit_code']==0 and type(ret['exit_code'])is int and ret['exit_code']==0 and'session_id'not in ret,'genuine original typed0')
 need(rt['actual_terminal_return']['chunk_id']=='31a677'and pt['actual_review_return']['chunk_id']=='2cb8d9','actual named closure executions')
 need(json.loads(pt['actual_review_return']['output'])['review_pin']==plan['closure_pins']['completion_post'],'post stdout exact PF')
 rr=json.loads(rt['actual_terminal_return']['output']);need(rr['completion_report_pin']==closed['actual_report_pin'],'genuine Root stdout binds Host')
 need(closed['actual_observation_manifest_pin']==plan['closure_pins']['observation_manifest'],'same manifest')
 state=manifest['states']['A'];need(manifest['state_order']==['A']and state['actual_material_child_closed_before_manifest']is True and state['all_actual_events_and_snapshots_saved']is True and len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8 and all(p in state['actual_material_product_pins']for p in eligible),'completed literal product/state scope')
 need(extract['actual_observation_manifest_pin']==plan['closure_pins']['observation_manifest']and extract['state_order']==['A']and extract['all_complete_state_scope_retained']is True and extract['all_handles_closed_between_snapshots']is True and len(extract['states']['A'])==8 and all(r['ASCII_used_or_invented']is False for r in extract['states']['A']),'all eight native snapshots; ASCII not consumed')
 retained=plan['retained_current7_pins'];identityonly=plan['retained_identity_only_roles'];metacurrent=plan['explicit_cumulative_metadata_file_pins'];need(len(retained)==80 and len(identityonly)==43,'full retained role counts')
 rmap={p['path']:p for p in retained};need(all(p['path']in rmap and rmap[p['path']]==p for p in candidate['exact_target_pins'][:14]),'HOLD14 complete saved PFs retained')
 need(all(s['input_pin']['path']in rmap and rmap[s['input_pin']['path']]==s['input_pin']for s in extract['states']['A']),'all original observer XSMs retained')
 for k in ['retained_final55_SQLite_pin','retained_final55_pool_pin','retained_original_A_material_XSM_pin','retained_final55_observer_XSM_pin']:
  p=candidate[k];need(rmap[p['path']]==p,'live retained original '+k)
 expected={p['path']:dict(path=p['path'],size_bytes=p['size_bytes'],identity=p['current7'])for p in candidate['preserved_result_JSONL_current7']};need({p['path']:p for p in identityonly}==expected,'all43 result documents identities preserved')
 targetpaths={p['path']for p in eligible};need(not targetpaths&{p['path']for p in retained+identityonly+metacurrent},'retired targets not left in live retained/meta roles')
 need(plan['original_A_aggregate_issue1_preserved']is True and plan['all14_earlier_SQL_pool_files_still_live']is True and plan['no_byte_identical_duplicate_claim']is True and plan['future_exact_retirement_receipt_admission_required']is True,'truthful lifecycle, old issue, future admission')
 for role in ['original_production_resource_Source_pin','original_history_resource_Source_pin']:full(plan[role])
 for p in retained+identityonly+metacurrent+eligible:current(p)
 need(not any((BASE/n).exists()for n in ['READONLY_RECEIPT.json','EXECUTION_RECEIPT.json']),'no check/retirement executed before review')
 unique={p['path']:p for p in FULL}
 for p in unique.values():full(p)
 for p in retained+identityonly+metacurrent+eligible:current(p)
 report=dict(schema='INDEPENDENT_LITERAL3_A_ASCII_EXPORT_RETIREMENT_SOURCE_METADATA_REVIEW_V1',status='PASS_SOURCE_METADATA_ONLY_EXACT3_EXPORT_LIFECYCLE_RETIREMENT_SCOPE',failure=None,source_pin=ps,plan_pin=pp,author_freeze_pin=author,metadata_only=True,reviewer_source_pin=own_pin(Path(__file__).absolute()),exact_target_pins=eligible,planned_released_bytes=346861973,Source_and_metadata_full_EOF_SHA_current7_twice_pins=list(unique.values()),Source_and_metadata_full_EOF_count=len(unique),retained_current7_role_count=len(retained),retained_result_identity_role_count=len(identityonly),inherited_metadata_current7_only_count=len(metacurrent),scientific_current7_only_count=len(retained)+len(identityonly)+len(eligible),all14_earlier_SQL_pool_files_retained=True,all8_observer_XSM_retained=True,all55_context_files_retained=True,all43_result_JSONL_retained=True,scientific_bodies_opened=False,scientific_body_SHA_recomputed=False,original_closed_native_A_verified_from_metadata=True,completion_Root_actual_return=rt['actual_terminal_return'],completion_post_actual_return=pt['actual_review_return'],original_A_aggregate_issue1_preserved=True,no_byte_identical_duplicate_claim=True,original_caps=caps,complete_joint_roots=plan['complete_joint_roots'],Root_only_actual_retirement_required=True,future_exact_retirement_receipt_admission_required=True,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024),wall_seconds=time.monotonic()-START,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,PS_executed=False,lsof_executed=False,check_or_execute_invoked=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 path=OUT/'REVIEW.json';need(not path.exists(),'own review once');raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20,'review8MiB')
 with path.open('xb')as stream:stream.write(raw)
 print(json.dumps(dict(status=report['status'],review_pin=own_pin(path))),flush=True)
if __name__=='__main__':main()
