"""UNREADY independent metadata post for an actual B2 current-epoch blind binding.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Only the frozen Root bridge records and current7 are verified; no payload SHA is repeated.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(target_payload_body_opened_or_hashed=False,gzip_payload_body_opened_or_hashed=False,worker_or_guard_helpers_imported=False,worker_executed=False,lsof_executed=False,PS_executed=False,native_executed=False,compiler_executed=False,compression_repeated=False,decompression_repeated=False,numerical_executed=False,JSONL_or_array_values_decoded=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
START=time.monotonic()
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def budget():
 need(time.monotonic()-START<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post stage600/SELF512')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary owned current7')
 return q
def full(p):
 q=current(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind whole-file SHA/length');current(p);return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==ids(s),'opened new file7')
  while b:=f.read(2**20):h.update(b);budget()
  need(ids(os.fstat(f.fileno()))==ids(s),'new file EOF7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def meta(p):
 need(p['size_bytes']<8*2**20,'only bounded control metadata8MiB is decoded')
 q=full(p);v=json.loads(q.read_bytes());full(p);return v
def genuine(v,key,p,field):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and json.loads(t['output'].strip().splitlines()[-1])[field]==p,'genuine closed typed0 and exact output artifact PF')
def current_role(p,build):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'same exact inherited current7 without old payload read')
 if p in build['readonly_system_SDK_header_pins']:
  root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
  need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and ids(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only frozen selected readonly SDK headers current7')
 elif p in build['readonly_system_tool_metadata_pins']:
  need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly PS/lsof roles')
 elif p==build['C_compiler_pin']:
  need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen current readonly clang role')
 elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
  need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only original frozen gfortran link exception')
 else:need(s.st_uid==os.getuid()and s.st_nlink==1,'same owned ordinary inherited role')
def all_output_pins(out):
 rows=[]
 if not os.path.lexists(out):return rows
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh current B55 control output')
 for q in sorted(out.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no new output alias')
  if stat.S_ISREG(s.st_mode):p=pin(q);full(p);rows.append(p)
  else:need(stat.S_ISDIR(s.st_mode),'ordinary new output files/directories only')
 return rows
def counted_bytes(roots):
 total=0
 for value in roots:
  root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'literal counted root')
  if not os.path.lexists(root):continue
  need(root.is_dir(),'counted root directory')
  for q in root.rglob('*'):
   budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in full counted scope')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
def unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
def readonly_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600 and v['joint']['resource_roots']==roots,'actual same original SELF512/stage600 and complete joint root topology')
 h=v['history'];j=v['joint'];sample=v['actual_PS_return']
 need(type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and type(sample['stdout'])is str and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'actual saved original same-PID PS return/RSS facts, PS not repeated by post')
 need(j['artifact_bytes']+v['external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original joint/history/cold/metadata/free caps including external/open-unlinked')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmA1_A3_formal13_epoch_bridge_source_v2_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '89bd98483f6a6c291a0f31d7bf6f3afc9c118fc126ec2af5108cff988b7e8f28', 'size_bytes': 5785, 'identity': [16777229, 50951231, 33188, 1, 5785, 1792080228085500048, 1792080228085500048]}
EXPECTED_CORE_SOURCE_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmA1_A3_formal13_epoch_bridge_source_v2_UNREADY/rebind_selected_A1_A3_and_formal13_readonly_roles_Root_only.UNREADY.py', 'sha256': '6f82e834f07839aeadd53dc752f8c5487974cbb506cadcec302f37c75a03bb8a', 'size_bytes': 21503, 'identity': [16777229, 50950138, 33188, 1, 21503, 1792079991536036186, 1792079991536036186]}
EXPECTED_CORE_BINDING_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmA1_A3_formal13_epoch_bridge_source_v2_UNREADY/BINDING.json', 'sha256': '2ed5ab061157290a2304189ba69a79521756172996c571d22f1825c3b51455df', 'size_bytes': 958418, 'identity': [16777229, 50951228, 33188, 1, 958418, 1792080228059290178, 1792080228059290178]}
def small(p):
 q=current(p);need(p['size_bytes']<8*2**20,'metadata/Source below8MiB');raw=q.read_bytes();need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole small metadata/Source SHA');current(p);return raw

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

def admit_latest_native_retirement(b):
 cp=b['latest_native10_retirement_closure_pins'];need(type(cp)is dict and all(type(cp[k])is dict for k in('receipt','Root_tools','post','post_tools'))and b['latest_native10_execute0_and_independent_post0_complete']is True,'latest native10 Root0/post0 future NULL hard reject')
 rp=cp['receipt'];tp=cp['Root_tools'];pp=cp['post'];pt=cp['post_tools'];r=meta(rp);p=meta(pp);plan=meta(b['latest_native10_retirement_plan_pin']);true0(tp,'actual_terminal_return','receipt_pin',rp);true0(pt,'actual_review_return','review_pin',pp)
 need(r['schema']=='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_RECEIPT_V1'and r['mode']=='execute'and r['status']=='RETIRED_CURRENT_A_B_NATIVE_EXACT10_ORIGINAL_BYTES_PRESERVED_IN_EXACT_RECOVERY_MAPS'and r['failure']is None and r['plan_pin']==b['latest_native10_retirement_plan_pin']and r['actual_released_pins']==r['exact_target_pins']==plan['exact_target_pins']and r['actual_released_bytes']==232289584 and r['files_deleted']is True and r['resources_after_original_classes_forced_fresh']is True,'genuine native10 redundant-original byte-preserved retirement Root0, never spool or old C10-only proof')
 contract=plan['execute_post_report_contract'];need(p['schema']==contract['schema']and p['status']==contract['status']and p['failure']is None and p['metadata_only']is True and p['actual_execution_receipt_pin']==rp and p['actual_Root_tools_pin']==tp and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==0 and p['actual_released_pins']==plan['exact_target_pins']and p['actual_released_bytes']==232289584 and p['files_deleted']is True and p['files_deleted_by_post']is False and p['exact_ten_targets_absent_verified_twice']is True and p['native_original_complete_bytes_preserved_by_exact_recovery_maps']is True and p['all_canonical7_gzip_entry_index_current7_verified_twice']is True and p['all_retained_roles_current7_verified_twice']is True and p['complete_joint_roots']==b['complete_joint_roots'],'actual independent R10 metadata post0 and full native byte recovery maps, no old producer qualification promoted')
 need(b['retained_current7_pins']==p['retained_all_current7_pins']and b['retained_archive_metadata_current7_pins']==p['retained_archive_metadata_current7_pins']and b['retained_B2_current_epoch_readonly_pins']==p['retained_B2_current_epoch_readonly_pins']and b['retained_failed_v1_current7_only_pins']==p['retained_failed_v1_current7_only_pins']and b['retained_failed_pool_archive_current7_only_pins']==p['retained_failed_pool_archive_current7_only_pins']and b['exact59_historical_absent_pins']==plan['exact49_historical_absent_pins']+plan['exact_target_pins'],'latest complete live roles and only exact previous49 plus newly closed10 historical paths')
 for target in b['exact59_historical_absent_pins']:need(not os.path.lexists(target['path'])and not any(x.is_symlink()for x in Path(target['path']).parents),'only specifically closed59 historical paths absent, no current relabel or generic skip')
 return[rp,tp,pp,pt]

def bridge_resources(v):
 need(type(v['history_artifact_bytes'])is int and type(v['complete_joint_bytes'])is int and type(v['explicit_external_metadata_bytes'])is int and type(v['own_open_unlinked_bytes'])is int and v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600 and v['all_selected_old_roles_covered_in_history']is True and type(v['history_root_count'])is int and v['history_root_count']>0,'actual scalar original history/complete83/SELF512/stage600 with selected31 cold roles remaining history')
 need(v['history_artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and v['complete_joint_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and v['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged global history96/joint2/cold/meta64/free8 include every actual external/openunlinked byte')
 sample=v['actual_PS_return'];need(type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and type(sample['stdout'])is str and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'saved original same-PID PS/RSS evidence only; no repeated PS')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','bridge-report-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent immutable once-only post, never author self-run')
 need(all(type(p)is dict for p in(EXPECTED_CORE_AUTHOR_FREEZE,EXPECTED_CORE_SOURCE_PIN,EXPECTED_CORE_BINDING_PIN)),'draft Source cannot run before actual author/core freeze PFs are filled')
 pTools=json.loads(a.Root_tools_pin);pReport=json.loads(a.bridge_report_pin);tools=meta(pTools);terminal=tools['actual_terminal_return'];report=None if pReport is None else meta(pReport)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None and tools['actual_execution_permission_mode']=='require_escalated'and tools['actual_retried']is False,'genuine original closed typed Root integer/no retry/permission, no child0 inference')
 author=meta(EXPECTED_CORE_AUTHOR_FREEZE);ps=EXPECTED_CORE_SOURCE_PIN;pb=EXPECTED_CORE_BINDING_PIN;b=meta(pb);source_limit=b['bounded_own_Source_metadata_receipts_bytes'];full(ps);full(ps)
 need(author['schema']=='AUTHOR_A1_A3_SELECTED18_FORMAL13_LATEST83_EPOCH_BRIDGE_SOURCE_FREEZE_V2'and author['source_pin']==ps and author['binding_pin']==pb and author['Source_and_binding_frozen']is True and author['Source_author_stopped_editing']is True and author['all_transitive_historical_fixed_inputs_recertified']is False and author['new_B_bearing_context_compatibility_or_lineage_proved']is False,'exact immutable final Source-author freeze and no expanded scope')
 need(b['schema']=='SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BRIDGE_BINDING_V1'and b['Source_admission_ready']is True and b['draft_unready']is False and b['new_owning_data_root_created']is False and b['future_Root_report_pin']is None and source_limit==8*2**20 and b['original_caps']==CAPS,'same frozen latest83 actual retirement0/post0 binding, future actual bridge remains NULL in source-era binding')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='A1_A3_FORMAL31_EPOCH_BRIDGE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pTools,actual_bridge_report_pin=pReport,actual_Root_integer_exit_code=code,actual_report_status=None if report is None else report['status'],actual_report_failure=None if report is None else report['failure'],actual_child_integer_exit_code=None,actual_children_started=None,closed0_bridge_or_scope_qualification_inferred=False,source_pin=ps,binding_pin=pb)
  save(result,source_limit);return
 need(report is not None,'genuine Root0 requires emitted actual bridge report');genuine(tools,'actual_terminal_return',pReport,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(pReport['path']==str(PACKAGE/'ROOT_CURRENT_EPOCH_A1_A3_FORMAL13_BLIND_BINDING_REPORT.json')and report['schema']=='ROOT_NATIVE_WARM_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BLIND_BINDING_REPORT_V1'and report['status']=='PASS_A1_A3_SELECTED18_FORMAL13_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and report['failure']is None and report['source_pin']==ps and report['binding_pin']==pb and report['original_caps']==CAPS and type(report['children_started'])is int and report['children_started']==0 and report['final_report_resource_check_passed']is True and report['bounded_own_Source_metadata_receipts_bytes']==source_limit,'actual same-source selected31 bridge Root0/current epoch only, no data child or qualification')
 need(stdout['selected31_only']is True and all(stdout[k]is False for k in('all_transitive_recertified','lineage_qualified','online_BOOT_qualified')),'actual stdout selected roles only, no transitive/lineage/online promotion')
 argv=shlex.split(tools['exact_executed_command']);prefix=b['original_complete_ENV_Python_B_prefix'];need(argv[:len(prefix)]==prefix and argv[len(prefix)]==ps['path']and len(argv)==len(prefix)+9,'complete original ENV/Python-B prefix and same exact executing bridge Source')
 tail=argv[len(prefix)+1:];need(len(tail)==8 and set(tail[::2])=={'--binding-pin','--source-pin','--review-pin','--review-tools-pin'},'four exact explicit Source-owned parameters, no aliases or extra arguments')
 args={k:json.loads(v)for k,v in zip(tail[::2],tail[1::2])};peerpin=args['--review-pin'];peertoolspin=args['--review-tools-pin'];need(args['--binding-pin']==pb and args['--source-pin']==ps and peerpin==report['independent_Source_review_pin'],'actual genuine command consumed exact Source/binding and report peer')
 peer=meta(peerpin);peertools=meta(peertoolspin);genuine(peertools,'actual_review_return',peerpin,'review_pin');need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_A1_A3_FORMAL13_EPOCH_BRIDGE_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BLIND_BINDING_V1'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==ps and peer['binding_pin']==pb,'new independent Source review0 separate from unavailable historical producer review raw')
 claimpin=pin(PACKAGE/'ROOT_CURRENT_EPOCH_BINDING_ONCE_CLAIM.json');claim=meta(claimpin);need(claim['schema']=='ROOT_A1_A3_FORMAL13_EPOCH_BRIDGE_ONCE_CLAIM_V1'and claim['claim_before_helpers_or_payload_IO']is True and claim['argv']==argv[len(prefix):]and type(claim['PID'])is int and claim['PID']>0,'real once claim before all helper/payload IO, exact actual sys.argv')
 latest=admit_latest_native_retirement(b);hosts=admit_old_producers(b);formal=meta(b['historical_formal_plan_current_metadata_pin']);need(formal['formal_configuration']==b['historical_formal_configuration']and len(formal['formal_inputs'])==13,'exact original formal13 metadata declaration, no B-bearing compatibility')
 specs=b['ordered_role_specs'];pairs=report['ordered_role_pairs'];need(len(specs)==len(pairs)==31 and len({r['role']for r in pairs})==31 and len({r['current_epoch_full_pin']['path']for r in pairs})==31 and report['selected_A1_A3_role_count']==18 and report['selected_formal_role_count']==13,'complete explicit selected A1/A3 eighteen and formal thirteen, no scope truncation')
 total=0
 for row,spec in zip(pairs,specs):
  prior=row['historical_full_pin'];currentpin=row['current_epoch_full_pin'];origin=formal if spec['family']=='FORMAL13'else hosts[spec['family']]
  need(pointer(origin,spec['historical_source_JSON_pointer'].strip('/').split('/'))==prior==spec['historical_full_pin']and row['role']==spec['role']and row['family']==spec['family']and row['blind_complete_SHA_and_length_equal']is True and row['before_open_EOF_after_current7_stable']is True and currentpin['path']==prior['path']and currentpin['sha256']==prior['sha256']and currentpin['size_bytes']==prior['size_bytes']and prior['identity'][0]==16777234 and currentpin['identity'][0]==16777229 and prior['identity'][1:]==currentpin['identity'][1:]and currentpin['identity']==spec['expected_start_current7'],'each exact historical role derives from its actual old Host/formal pointer; new complete SHA/length and all six nondevice identity fields preserved')
  current(currentpin);total+=currentpin['size_bytes']
 need(sum(r['family']=='FORMAL13'for r in pairs)==13 and sum(r['family']=='A1'for r in pairs)==sum(r['family']=='A3'for r in pairs)==9 and total==b['selected_total_recorded_bytes'],'full31 exact byte count/family counts; no transitive recertification')
 need(report['historical_producer_closure_metadata']==b['historical_producers']and report['historical_independent_success_raw_not_available_and_not_fabricated']is True and all(p['historical_independent_actual_review_raw_pin']is None and p['historical_independent_actual_review_genuine_typed0_asserted']is False for p in b['historical_producers'])and report['actual_latest_native10_retirement_closure_pins']==latest,'old independent successful tool raw remains unavailable NULL, exact actual latest R10 closure distinct')
 roots=b['complete_joint_roots'];need(report['complete_joint_roots']==roots and len(roots)==len(set(roots))==83 and any(PACKAGE.is_relative_to(Path(r))for r in roots)and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'whole existing latest83 including prior roots, no fresh output root')
 table={}
 for p in b['explicit_cumulative_metadata_file_pins']+[pb,ps,peerpin,peertoolspin]+latest:need(p['path']not in table or table[p['path']]==p,'same metadata path same complete PF');table[p['path']]=p
 explicit=list(table.values());need(report['explicit_cumulative_metadata_file_pins']==explicit and not{r['current_epoch_full_pin']['path']for r in pairs}&set(table),'whole actual cumulative metadata union, selected old readonly bodies remain history/cold')
 for k in('retained_current7_pins','retained_archive_metadata_current7_pins','retained_B2_current_epoch_readonly_pins','retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins','exact59_historical_absent_pins'):need(report[k]==b[k],'exact latest complete current/historical role arrays')
 build=meta(b['original_guard_build_plan_pin'])
 for _ in range(2):
  for p in explicit+b['retained_current7_pins']+b['retained_archive_metadata_current7_pins']+b['retained_B2_current_epoch_readonly_pins']:current_role(p,build)
  for row in pairs:current(row['current_epoch_full_pin'])
  for p in b['retained_failed_v1_current7_only_pins']+b['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'strict failed stat3 only, never payload SHA');current(p)
  need(len(b['exact59_historical_absent_pins'])==len({p['path']for p in b['exact59_historical_absent_pins']})==59,'only precise original49+retired10 historical paths')
  for p in b['exact59_historical_absent_pins']:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'no generic missing path skip; only actual closed exact59 absence')
 need(report['Root_SELF_peak_bytes']<512*2**20 and 0<=report['Root_elapsed_seconds']<600 and len(report['resources'])>=2,'actual Root original SELF512/stage600 and real saved checkpoints')
 last=-1
 for snap in report['resources']:bridge_resources(snap);need(snap['elapsed_seconds']>=last,'actual resource checkpoints follow original start order');last=snap['elapsed_seconds']
 for k in('all_transitive_historical_fixed_inputs_recertified','new_B_bearing_context_compatibility_or_lineage_proved','decoder_executed','native_executed','files_deleted','physics_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(report[k]is False,'selected31 blind binding grants no producer rerun/transitive/B-context/lineage/online/physics qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in explicit if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full83/external/openunlinked/free original caps include Source and new metadata post')
 for p in(pTools,pReport,ps,pb,peerpin,peertoolspin,claimpin,EXPECTED_CORE_AUTHOR_FREEZE):full(p)
 result=dict(schema='A1_A3_FORMAL31_CURRENT_EPOCH_BRIDGE_ACTUAL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_ROOT0_CURRENT7_METADATA_ONLY_NO_COMPATIBILITY_QUALIFICATION',failure=None,actual_Root_tools_pin=pTools,actual_bridge_report_pin=pReport,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=None,actual_children_started=0,source_pin=ps,binding_pin=pb,actual_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,actual_Source_review_pin=peerpin,actual_Source_review_tools_pin=peertoolspin,actual_Root_claim_pin=claimpin,exact_actual_Root_command=tools['exact_executed_command'],ordered_role_pairs=pairs,actual_selected_role_count=31,actual_selected_blind_verified_bytes=total,all31_current_epoch_roles_current7_verified_twice=True,Root_recorded_blind_fullEOF_SHA_length_and_stable7_verified_without_payload_replay=True,historical_producer_closure_metadata=b['historical_producers'],historical_independent_success_raw_not_available_and_not_fabricated=True,historical_independent_genuine_typed0_asserted=False,actual_latest_native10_retirement_closure_pins=latest,exact59_historical_absent_pins=b['exact59_historical_absent_pins'],exact59_historical_absence_only_verified_twice=True,retained_all_current7_pins=b['retained_current7_pins'],retained_archive_metadata_current7_pins=b['retained_archive_metadata_current7_pins'],retained_B2_current_epoch_readonly_pins=b['retained_B2_current_epoch_readonly_pins'],retained_failed_v1_current7_only_pins=b['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=b['retained_failed_pool_archive_current7_only_pins'],all_retained_roles_current7_verified_twice=True,explicit_cumulative_metadata_file_pins=explicit,complete_joint_roots=roots,original_caps=CAPS,local_Source_bound_bytes=source_limit,actual_Root_resource_snapshots=report['resources'],actual_final_report_resource_check_passed=True,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,all_transitive_historical_fixed_inputs_recertified=False,new_B_bearing_context_compatibility_or_lineage_proved=False,online_BOOT_qualified=False,physics_qualified=False,payload_SHA_repeated_by_post=False,decoder_executed=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()
