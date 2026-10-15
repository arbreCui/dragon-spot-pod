"""Draft Root-only blind current-epoch binding of exact A1/A3 eighteen and formal thirteen roles.
No old producer rerun, no native/decoder, no transitive or context/physics admission.
Historical missing independent successful tool objects stay NULL and are not promoted.
"""
import argparse,hashlib,importlib.util,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
CHUNK=2**20
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and ids(s)==p['identity']and s.st_size==p['size_bytes'],'literal owned metadata/Source exact current7');return q
def small(p):
 q=current(p);need(p['size_bytes']<8*2**20,'metadata/Source below8MiB');raw=q.read_bytes();need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole small metadata/Source SHA');current(p);return raw
def meta(p):return json.loads(small(p))
def true0(p,key,field,want):
 d=meta(p);r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[field]==want,'actual typed closed0 exact metadata PF');return d

def pointer(d,parts):
 for part in parts:d=d[int(part)]if isinstance(d,list)else d[part]
 return d
def historical_metadata_preserved(old,new):
 need(new['path']==old['path']and new['sha256']==old['sha256']and new['size_bytes']==old['size_bytes']and new['identity'][1:]==old['identity'][1:],'old historical metadata bytes and six nondevice fields preserved')
def admit_old_producers(b):
 hosts={}
 for p in b['historical_producers']:
  old=meta(p['current_Host_metadata_pin']);historical_metadata_preserved(p['historical_Host_full_pin'],p['current_Host_metadata_pin'])
  raw=meta(p['current_Root_raw_metadata_pin']);terminal=pointer(raw,p['genuine_terminal_JSON_pointer'])
  need(type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and terminal['chunk_id']==p['genuine_terminal_chunk'],'same genuine old Root terminal typed0; exact A1/A3 raw keys, no invented B_v3 aliases')
  out=json.loads(terminal['output'].strip().splitlines()[-1]);need(out==dict(status=p['expected_Host_status'],failure=None,records=4)and old['status']==out['status']and old['failure']is None and len(old['records'])==4 and all(r['status']=='PASS'for r in old['records']),'old four-stage single-plane producer actual closure remains historical')
  nt=old['actual_native_terminal'];need(nt['schema']==p['expected_terminal_schema']and nt['status']=='PASS'and(nt['plane'],nt['epoch'],nt['groups'],nt['unknowns'],nt['full_native_read_status'])==(p['plane'],0,370,14,3),'old own-plane/e0/whole370 terminal metadata only')
  for k in('all370_ROOT_FLUX64_FLUX64_REF_bits_equal','full_source64_type4_finite_and_exact_mirror','archive_read_only','strict_terminal_gate_passed'):need(nt[k]is True,'old terminal original gate fact')
  for record in old['records']:
   wp=next(x for x in p['current_watchdog_metadata_pins']if x['path']==str(Path(p['current_Host_metadata_pin']['path']).parent/(record['label']+'.watchdog.json')));w=meta(wp)
   need(w['command']==record['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'exact old per-label watchdog genuine recorded child closure')
  for x in p['current_log_metadata_pins']:small(x)
  meta(p['current_terminal_binding_metadata_pin']);meta(p['current_owning_binding_metadata_pin'])
  need(p['historical_independent_actual_review_raw_pin']is None and p['historical_independent_actual_review_genuine_typed0_asserted']is False,'missing historical independent success raw is explicitly NULL; no synthesized old post0')
  if p['plane']==1:
   sr=meta(p['current_historical_Source_review_metadata_pin']);need(sr['schema']=='INDEPENDENT_FINAL_CURRENT_WARM_A_V3_EXACT_SCHEMA_SOURCE_REVIEW'and p['current_historical_independent_actual_review_metadata_pin']is None,'A1 saved Source review is only Source review, not actual producer post')
  else:
   ir=meta(p['current_historical_independent_actual_review_metadata_pin']);handoff=meta(p['current_historical_independent_review_handoff_metadata_pin']);provenance=meta(p['current_historical_independent_review_copy_provenance_metadata_pin']);small(p['current_historical_independent_review_Source_metadata_pin'])
   need(ir['schema']=='INDEPENDENT_CLOSED_ACTUAL_A23_SINGLE_PLANE_SAVED_REPORT_REVIEW_V1'and ir['status']=='PASS_ACTUAL_A3_FOUR_STAGE_SAVED_PRODUCER_ONLY'and ir['actual_summary_pin']==p['historical_Host_full_pin']and ir['actual_Root_terminal_chunk']==p['genuine_terminal_chunk']and ir['actual_native_terminal']==nt,'actual saved A3 independent report exact old Host/terminal; not a new raw tool return')
   historical_metadata_preserved(ir['actual_Root_terminal_receipt_pin'],p['current_Root_raw_metadata_pin'])
   copyrow=next(x for x in provenance['files']if x['durable_copy']['path']==p['current_historical_independent_actual_review_metadata_pin']['path']);need(copyrow['original']['path']==handoff['A3_review_pin']['path']and copyrow['original']['sha256']==handoff['A3_review_pin']['sha256']==p['current_historical_independent_actual_review_metadata_pin']['sha256']and handoff['A3_actual_terminal_chunk']==p['genuine_terminal_chunk'],'A3 original-to-durable exact byte provenance, no original path/PF relabel')
  hosts[p['tag']]=old
 need(set(hosts)=={'A1','A3'},'exact two old producers only');return hosts
def admit_recovery(b):
 rp=b['actual_SQL_partial_recovery_execution_receipt_pin'];tp=b['actual_SQL_partial_recovery_Root_tools_pin'];pp=b['actual_SQL_partial_recovery_execute_post_pin'];pt=b['actual_SQL_partial_recovery_execute_post_tools_pin']
 need(all(isinstance(p,dict)for p in(rp,tp,pp,pt))and b['actual_current_stage_resource_admission']is not None,'future recovery Root/post and real current budget cannot be NULL at admission')
 r=meta(rp);p=meta(pp);plan=meta(b['recovery_plan_pin']);true0(tp,'actual_terminal_return','receipt_pin',rp);true0(pt,'actual_review_return','review_pin',pp)
 need(r['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_RECEIPT_V1'and r['mode']=='execute'and r['status']=='RECOVERED_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED'and r['failure']is None and r['plan_pin']==b['recovery_plan_pin']and r['actual_released_pins']==plan['exact_target_pins']and r['actual_released_bytes']==70080456 and r['files_deleted']is True and r['resources_after_original_classes_forced_fresh']is True,'true exact SQL+partial recovery Root0 original resource closure')
 contract=plan['execute_post_report_contract'];need(p['schema']==contract['schema']and p['status']==contract['status']and p['failure']is None and p['metadata_only']is True and p['actual_execution_receipt_pin']==rp and p['actual_Root_tools_pin']==tp and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==0 and p['actual_released_pins']==plan['exact_target_pins']and p['actual_released_bytes']==70080456 and p['files_deleted']is True and p['files_deleted_by_post']is False and p['whole_pair_archive_complete']is False and p['complete_joint_roots']==b['complete_joint_roots'],'actual independent metadata post0; pair failure is not upgraded')
 for target in plan['exact_target_pins']:need(not os.path.lexists(target['path']),'only explicit SQL+partial retired paths absent; no historical original body probe')
 return[rp,tp,pp,pt]
def main():
 started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('binding','source','review','review-tools'):ap.add_argument('--'+role+'-pin',required=True)
 a=ap.parse_args();pb=json.loads(a.binding_pin);ps=json.loads(a.source_pin);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin)
 need(ps['path']==str(Path(__file__).absolute()),'same frozen executing Source');small(ps);b=meta(pb)
 need(b['schema']=='SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BRIDGE_BINDING_V1'and b['Source_admission_ready']is True and b['draft_unready']is False and b['new_owning_data_root_created']is False and b['future_Root_report_pin']is None,'exact finalized independent-reviewed binding, no future actual report minted')
 def selfcheck():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-started<600,'unchanged Root SELF512/stage600/whole1800 from original start');n=0
  for q in BASE.rglob('*'):
   s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'whole Source no alias');n+=s.st_size if stat.S_ISREG(s.st_mode)else 0
  need(n<16*2**20,'entire bridge Source and metadata16MiB');return peak
 selfcheck();fd=os.open(BASE/'ROOT_CURRENT_EPOCH_BINDING_ONCE_CLAIM.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'w')as f:json.dump(dict(schema='ROOT_A1_A3_FORMAL13_EPOCH_BRIDGE_ONCE_CLAIM_V1',PID=os.getpid(),started=started,claim_before_helpers_or_payload_IO=True,argv=sys.argv),f);f.write('\n');f.flush();os.fsync(f.fileno())
 peer=meta(pr);true0(pt,'actual_review_return','review_pin',pr);need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_A1_A3_FORMAL13_EPOCH_BRIDGE_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BLIND_BINDING_V1'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==ps and peer['binding_pin']==pb,'new bridge independent Source0 is distinct from historical producer review evidence')
 need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'original unoptimized thread1')
 recovery_pins=admit_recovery(b);hosts=admit_old_producers(b);formal=meta(b['historical_formal_plan_current_metadata_pin']);need(formal['formal_configuration']==b['historical_formal_configuration']and len(formal['formal_inputs'])==13,'exact original formal13 declaration, no B-bearing compatibility inferred')
 rows=b['ordered_role_specs'];need(len(rows)==31 and len({x['role']for x in rows})==31 and len({x['historical_full_pin']['path']for x in rows})==31 and sum(x['family']=='FORMAL13'for x in rows)==13 and sum(x['family']=='A1'for x in rows)==sum(x['family']=='A3'for x in rows)==9,'complete explicit selected18 plus formal13, no truncation')
 for row in rows:
  source=formal if row['family']=='FORMAL13'else hosts[row['family']];parts=row['historical_source_JSON_pointer'].strip('/').split('/');need(pointer(source,parts)==row['historical_full_pin'],'each selected historical role exactly derives from original Host/formal table')
 common=b['frozen_original_resource_common_Source_pin'];small(common);spec=importlib.util.spec_from_file_location('A13_epoch_original_resource_support',common['path']);c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
 rb=dict(b['original_resource_binding']);need(rb['complete_joint_roots']==b['complete_joint_roots']and len(rb['complete_joint_roots'])==81 and b['original_caps']==c.CAPS,'entire actual recovery81 roots, original classes/caps unchanged')
 table={}
 for p in rb['explicit_cumulative_metadata_file_pins']+[pb,ps,pr,pt]+recovery_pins:need(p['path']not in table or table[p['path']]==p,'samepath explicit metadata cannot conflict');table[p['path']]=p
 rb['explicit_cumulative_metadata_file_pins']=list(table.values());resources=c.Resources(rb,started,600);last=0.0;snapshots=[]
 def checkpoint(force=False):
  nonlocal last
  selfcheck();resources.light()
  if force or time.monotonic()-last>=5:
   state=resources.check();history=state['original_history']['resource_roots'];need(all(any(Path(row['historical_full_pin']['path']).is_relative_to(Path(r))for r in history)for row in rows),'all selected historical roles remain original history/cold, never ordinary external metadata or new fresh inputs')
   snapshots.append(dict(history_artifact_bytes=state['original_history']['artifact_bytes'],history_root_count=len(history),complete_joint_bytes=state['complete_joint']['artifact_bytes'],explicit_external_metadata_bytes=state['explicit_external_metadata_bytes'],own_open_unlinked_bytes=state['own_open_unlinked_bytes'],disk_free_bytes=state['complete_joint']['disk_free_bytes'],SELF_peak_bytes=state['SELF_peak_bytes'],elapsed_seconds=state['original_elapsed_seconds'],all_selected_old_roles_covered_in_history=True));last=time.monotonic()
 checkpoint(True);pairs=[]
 for row in rows:
  oldpin=row['historical_full_pin'];q=Path(oldpin['path']);s=q.lstat();before=ids(s);need(before==row['expected_start_current7']and before[1:]==oldpin['identity'][1:]and oldpin['identity'][0]==16777234 and before[0]==16777229 and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and not any(x.is_symlink()for x in(q,*q.parents))and s.st_size==oldpin['size_bytes'],'only explicit device epoch changed; original six fields/SHA/length retained')
  h=hashlib.sha256();n=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   need(ids(os.fstat(fd))==before,'opened exact current7')
   while block:=os.read(fd,CHUNK):checkpoint();h.update(block);n+=len(block)
   need(ids(os.fstat(fd))==before,'complete EOF stable current7')
  finally:os.close(fd)
  need(ids(q.lstat())==before and n==oldpin['size_bytes']and h.hexdigest()==oldpin['sha256'],'blind complete SHA and length equal saved original')
  pairs.append(dict(role=row['role'],family=row['family'],historical_full_pin=oldpin,current_epoch_full_pin=dict(path=oldpin['path'],sha256=h.hexdigest(),size_bytes=n,identity=before),blind_complete_SHA_and_length_equal=True,before_open_EOF_after_current7_stable=True))
 checkpoint(True)
 report=dict(schema='ROOT_NATIVE_WARM_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BLIND_BINDING_REPORT_V1',status='PASS_A1_A3_SELECTED18_FORMAL13_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY',failure=None,binding_pin=pb,source_pin=ps,independent_Source_review_pin=pr,ordered_role_pairs=pairs,selected_A1_A3_role_count=18,selected_formal_role_count=13,explicit_cumulative_metadata_file_pins=rb['explicit_cumulative_metadata_file_pins'],historical_producer_closure_metadata=b['historical_producers'],historical_independent_success_raw_not_available_and_not_fabricated=True,actual_SQL_partial_recovery_closure_pins=recovery_pins,complete_joint_roots=b['complete_joint_roots'],original_caps=c.CAPS,resources=snapshots,all_transitive_historical_fixed_inputs_recertified=False,new_B_bearing_context_compatibility_or_lineage_proved=False,children_started=0,decoder_executed=False,native_executed=False,files_deleted=False,physics_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,Root_SELF_peak_bytes=selfcheck(),Root_elapsed_seconds=time.monotonic()-started,final_report_resource_check_passed=False)
 for row in pairs:current(row['current_epoch_full_pin'])
 q=BASE/'ROOT_CURRENT_EPOCH_A1_A3_FORMAL13_BLIND_BINDING_REPORT.json';need(not os.path.lexists(q),'report once');owned=None
 def write_report(first):
  nonlocal owned
  raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<2*2**20,'small bridge report2MiB');oldsize=0 if first else q.lstat().st_size;need(sum(p.lstat().st_size for p in BASE.rglob('*')if p.is_file())-oldsize+len(raw)<16*2**20,'whole Source16 before report')
  if not first:need(ids(q.lstat())==owned,'same just-created own report7')
  fd=os.open(q,os.O_WRONLY|os.O_NOFOLLOW|(os.O_CREAT|os.O_EXCL if first else 0),0o600)
  with os.fdopen(fd,'wb')as f:
   if not first:need(ids(os.fstat(f.fileno()))==owned,'same open own report7');f.truncate(0)
   f.write(raw);f.flush();os.fsync(f.fileno())
  owned=ids(q.lstat())
 write_report(True);checkpoint(True);report['resources']=snapshots;report['final_report_resource_check_passed']=True;write_report(False);checkpoint(True)
 for row in pairs:current(row['current_epoch_full_pin'])
 small(ps);small(pb);raw=q.read_bytes();s=q.lstat();p=dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s));selfcheck();print(json.dumps(dict(status=report['status'],report_pin=p,selected31_only=True,all_transitive_recertified=False,lineage_qualified=False,online_BOOT_qualified=False)),flush=True)
if __name__=='__main__':main()
