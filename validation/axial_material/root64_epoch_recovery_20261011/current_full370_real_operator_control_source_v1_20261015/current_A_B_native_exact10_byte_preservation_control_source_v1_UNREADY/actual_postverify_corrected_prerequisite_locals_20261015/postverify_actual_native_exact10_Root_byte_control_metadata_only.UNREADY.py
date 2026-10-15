"""UNREADY independent metadata post for the actual Root-only native exact10 byte-preservation control.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source and saved metadata are read. Original products and gzip files get current7 only; no repeated decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A_B_native_exact10_byte_preservation_control_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '38b11861b0d97e92303959aff09defa03c10280c4816bd74c63b426aabf2a555', 'size_bytes': 4565, 'identity': [16777229, 50931763, 33188, 1, 4565, 1792078968966356702, 1792078968966356702]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(compiler_executed=False,native_executed=False,children_started_by_post=False,worker_or_guard_helpers_imported=False,original_plain_payload_body_opened=False,original_plain_payload_SHA_recomputed=False,gzip_payload_body_opened_by_post=False,compression_repeated=False,decompression_repeated=False,restored_product_file_written=False,scientific_values_decoded=False,files_deleted=False,retirement_authorized=False,paired_SQL_pool_archive_complete=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
def member0_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['original_elapsed_seconds']<600 and v['complete_joint_root_count']==len(roots)and v['non_scalar_resource_inventories_omitted']is True,'actual original Root-only SELF512/stage600 and scalar snapshots for entire bound root topology')
 h=v['original_history'];j=v['complete_joint']
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual saved original cumulative/history/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
EXPECTED_FROZEN_CLI_TEMPLATE_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A_B_native_exact10_byte_preservation_control_source_v1_UNREADY/ROOT_REVIEWABLE_BYTE_CONTROL_CLI_NULL_PEER_TEMPLATE.json', 'sha256': '9fcdd310b4ade2f66470423df03a6797302b9ffc55110237295badb77414a624', 'size_bytes': 4823, 'identity': [16777229, 50931761, 33188, 1, 4823, 1792078968965509532, 1792078968965509532]}
def current_failed_v1(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q

def current_failed_pool(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool metadata/runtime rows, never fullPF/SHA or deletion targets')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-pool retained row stable current7 only')
 return q

def unique(rows):
 out={}
 for p in rows:need(p['path']not in out or out[p['path']]==p,'same path same fullPF');out[p['path']]=p
 return list(out.values())

def genuine_code(d,key,code):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and r.get('session_id')is None,'genuine original closed typed integer tool return; no live session')
 return r

def genuine_post(tools,p):
 r=genuine_code(tools,'actual_review_return',0);need(json.loads(r['output'].strip().splitlines()[-1])['review_pin']==p,'genuine independent metadata post0 exact stdout review PF')

def historical_absence(plan):
 rows=plan['exact49_historical_absent_pins'];need(len(rows)==len({p['path']for p in rows})==49 and rows[-4:]==plan['exact4_retired_completed_spool_pins'],'only exact inherited45 plus just-completed4 historical paths')
 for p in rows:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'precise closed historical absence only; no generic missing skip')

def native_compact_resource_facts(v,roots):
 need(v['complete_joint_root_count']==len(roots)==83 and v['non_scalar_resource_inventories_omitted']is True and type(v['SELF_peak_bytes'])is int and 0<=v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600,'actual compact original Root resource facts: full83/SELF512/stage600')
 h=v['original_history'];j=v['complete_joint'];sample=v['actual_PS_return']
 need(type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and type(sample['stdout'])is str and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'actual saved original same-PID PS return; never repeat PS')
 need(j['artifact_bytes']+v['external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'saved original joint/history/cold64metadata/free8 caps include all external/open-unlinked')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','report-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent once-only immutable metadata post, never author self-run')
 pRoot=json.loads(a.Root_tools_pin);pReport=json.loads(a.report_pin);raw=meta(pRoot);report=None if pReport is None else meta(pReport);terminal=raw['actual_terminal_return']
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_retried']is False,'original genuine observed closed typed Root integer/no retry; no child invented')
 core=meta(EXPECTED_CORE_AUTHOR_FREEZE);ps=core['source_pin'];pp=core['plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];full(ps);full(ps)
 need(core['schema']=='AUTHOR_NATIVE_EXACT10_ROOT_ONLY_BYTE_CONTROL_SOURCE_FREEZE_V1'and core['core_Source_and_PLAN_frozen']is True and core['Root_unique_byte_IO_executor']is True and core['no_GEN_required_for_this_Root_only_byte_control']is True and plan['schema']=='ROOT_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['actual_prerequisites_closed']is True and plan['only_Root_native_byte_preservation_control']is True and plan['actual_exact4_execute0_independent_post0_complete']is True and source_limit==8*2**20 and plan['Root_stage_seconds']==600 and plan['Root_whole_seconds']==1800 and plan['resource_full_scan_interval_seconds']==5.0 and plan['resource_scan_last_recorded_after_completion']is True and plan['new_data_owning_root_created']is False and plan['original_caps']==CAPS,'same author-frozen exact10 byte-only control Source/PLAN and original caps with localSource8')
 need(ps['path']==str(PACKAGE/'verify_exact10_native_bytes_and_Bfinal_archived_stream_Root_only.UNREADY.py')and pp['path']==str(PACKAGE/'PLAN.json'),'exact actual algorithm and PLAN paths')
 if pReport is not None:need(pReport['path']==str(PACKAGE/'ROOT_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_REPORT.json')and report['schema']=='ROOT_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_REPORT_V1','actual emitted native10 Root report exact role')
 code=raw['original_integer_exit_code']
 if code!=0:
  result=dict(schema='NATIVE_EXACT10_BYTE_CONTROL_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_native10_Root_report_pin=pReport,actual_Root_integer_exit_code=code,actual_report_status=None if report is None else report['status'],actual_report_failure=None if report is None else report['failure'],source_pin=ps,plan_pin=pp,no_child_code_inferred=True,native10_control_success_or_retirement_authorization_inferred=False)
  save(result,source_limit);return
 need(report is not None,'Root0 requires exact actual emitted report PF');genuine(raw,'actual_terminal_return',pReport,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(report['status']=='PASS_ROOT_NATIVE_EXACT10_COMPLETE_BYTE_PRESERVATION_CONTROL_NO_RETIREMENT'and report['failure']is None and report['source_pin']==ps and report['plan_pin']==pp and report['role_projection_pin']==plan['role_projection_pin']==core['native_role_projection_pin']and report['final_report_resource_check_passed']is True and raw['actual_execution_permission_mode']=='require_escalated'and type(stdout['children_started'])is int and stdout['children_started']==0 and stdout['native_candidate_count']==10 and stdout['canonical_native_count']==7 and stdout['files_deleted']is False and stdout['retirement_authorized']is False,'actual same-source Root0 native10 byte control only, no retirement')
 pr=report['actual_Source_review_pin'];pt=report['actual_Source_review_tools_pin'];review=meta(pr);tools=meta(pt);genuine_post(tools,pr)
 need(review['status']=='PASS_SOURCE_ONLY_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL'and review['failure']is None and review['source_only']is True and review['source_pin']==ps and review['plan_pin']==pp,'genuine independent Source0 of same exact control')
 cli=meta(EXPECTED_FROZEN_CLI_TEMPLATE_PIN);actualargv=shlex.split(raw['exact_executed_command']);templateargv=cli['argv']
 need(cli['schema']=='ROOT_EXACT10_BYTE_CONTROL_CLI_TEMPLATE_PENDING_TRUE_SOURCE_PEER0_V1'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['required_Source_review_status']==review['status']and cli['only_two_exact_future_Source_peer_roles_may_be_filled']is True and cli['pending_actual_Source_review_pin']is None and cli['pending_actual_Source_review_tools_pin']is None and len(actualargv)==len(templateargv),'frozen pending-review template is historical Source metadata, actual peer roles come from genuine report')
 for expected,actual in zip(templateargv,actualargv):
  if expected=='__GENUINE_INDEPENDENT_SOURCE_REVIEW_FULL_PIN_JSON__':need(json.loads(actual)==pr,'actual exact genuine Source review argument')
  elif expected=='__GENUINE_INDEPENDENT_SOURCE_REVIEW_TOOLS_FULL_PIN_JSON__':need(json.loads(actual)==pt,'actual exact genuine Source review tools argument')
  else:need(expected==actual,'all other original frozen argv strings exact; no reconstructed command alias')
 roots=plan['complete_joint_roots'];need(roots==report['complete_joint_roots']and len(roots)==len(set(roots))==83 and any(PACKAGE.is_relative_to(Path(r))for r in roots)and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'entire real83 unchanged roots/no new data ownroot')
 projection = meta(plan['role_projection_pin'])
 need(projection['schema'] == 'NATIVE_EXACT10_CANDIDATE_TO_EXACT_CANONICAL_BYTE_SOURCE_METADATA_PROJECTION_V1' and projection['source_only'] is True and (projection['metadata_only'] is True) and (projection['formal_byte_control_admission'] is False) and (projection['actual_prerequisite_closure_pins'] == plan['actual_prerequisite_closure_pins']) and (plan['exact4_prerequisite_closure_pins'] == plan['actual_prerequisite_closure_pins']['exact4_completed_spools_Root0_post0']), 'projection is Source role metadata, not claimed prior byte proof')
 targets = plan['exact_ordered10_candidate_full_pins']
 canonical = plan['retained_ordered7_canonical_native_full_pins']
 all17 = plan['all17_native_full_pins']
 maps = plan['exact_ordered10_recovery_mappings']
 need(targets == projection['exact_ordered10_candidate_full_pins'] and canonical == projection['retained_ordered7_canonical_native_full_pins'] and (all17 == projection['all17_native_full_pins'] == unique(targets + canonical)) and (maps == projection['exact_ordered10_recovery_mappings']) and (len(targets) == 10) and (len(canonical) == 7) and (len(all17) == 17) and (len(maps) == 10) and ([m['target_pin'] for m in maps] == targets) and (len({p['path'] for p in all17}) == 17) and (sum((p['size_bytes'] for p in targets)) == plan['candidate_total_bytes'] == 232289584) and (sum((p['size_bytes'] for p in all17)) == plan['all17_native_total_bytes'] == 368221520), 'exact17 native roles and10 ordered candidate-to-recovery maps, no generic dedup')
 for p in all17:
     current(p)
 cp = plan['exact4_prerequisite_closure_pins']
 receipt4 = meta(cp['receipt'])
 root4 = meta(cp['Root_tools'])
 post4 = meta(cp['post'])
 post4tools = meta(cp['post_tools'])
 e4plan = meta(cp['plan'])
 genuine_code(root4, 'actual_terminal_return', 0)
 genuine_post(post4tools, cp['post'])
 need(json.loads(root4['actual_terminal_return']['output'].strip().splitlines()[-1])['receipt_pin'] == cp['receipt'], 'genuine exact4 Root0 stdout receipt')
 need(receipt4['mode'] == 'execute' and receipt4['failure'] is None and (receipt4['status'] == 'RETIRED_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_DERIVED_TEMPORARIES_ONLY') and (receipt4['plan_pin'] == cp['plan']) and (receipt4['actual_released_pins'] == receipt4['exact_target_pins'] == plan['exact4_retired_completed_spool_pins']) and (receipt4['actual_released_bytes'] == 183292696) and (receipt4['resources_after_original_classes_forced_fresh'] is True) and (receipt4['files_deleted'] is True), 'genuine exact4 completed-spool cleanup, unrelated native remains live')
 need(post4['schema'] == 'CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_EXECUTION_METADATA_POSTVERIFY_V1' and post4['status'] == 'PASS_ACTUAL_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_TEMPORARIES_RETIRED_NATIVE_AND_RESULTS_PRESERVED_METADATA_ONLY' and (post4['failure'] is None) and (post4['metadata_only'] is True) and (type(post4['actual_Root_integer_exit_code']) is int) and (post4['actual_Root_integer_exit_code'] == 0) and (post4['actual_execution_receipt_pin'] == cp['receipt']) and (post4['actual_Root_tools_pin'] == cp['Root_tools']) and (post4['plan_pin'] == cp['plan']) and (post4['exact_four_targets_absent_verified_twice'] is True) and (post4['all_retained_roles_current7_verified_twice'] is True) and (post4['retained_all_current7_pins'] == plan['retained_current7_pins']) and (post4['complete_joint_roots'] == e4plan['complete_joint_roots'] == roots), 'actual independent exact4 metadata0 and exact latest live-retainer roles')
 proof = plan['actual_prerequisite_closure_pins']
 posts = {}
 reports = {}
 specs = (('A_original_stage0_Root1', 'actual_report_pin', 'actual_Root_true_tool_return_pin', 1), ('A_continuation_Root0_no_new_child', 'actual_report_pin', 'actual_Root_true_tool_return_pin', 0), ('A_full_extract_Root0_child2', 'actual_report_pin', 'actual_Root_true_tool_return_pin', 0), ('B_full_capture_Root0_child0', 'actual_Host_report_pin', 'actual_Root_tools_pin', 0), ('B4_member0_old_Root0_no_child', 'actual_member0_Root_report_pin', 'actual_Root_tools_pin', 0), ('B4_all4_Root0_child0', 'actual_Host_report_pin', 'actual_Root_tools_pin', 0))
 for name, reportkey, rootkey, code in specs:
     c = proof[name]
     post = meta(c['post'])
     prior_report = meta(c['Root_report'])
     prior_raw = meta(c['Root_tools'])
     ptools = meta(c['post_tools'])
     genuine_code(prior_raw, 'actual_terminal_return', code)
     genuine_post(ptools, c['post'])
     need(post['schema'] == c['post_schema'] and post['status'] == c['post_status'] and (post['failure'] is None) and (type(post['actual_Root_integer_exit_code']) is int) and (post['actual_Root_integer_exit_code'] == code) and (post[reportkey] == c['Root_report']) and (post[rootkey] == c['Root_tools']), 'real exact producer/extract/archive original Root state and independent post0 roles')
     posts[name] = post
     reports[name] = prior_report
 ao = posts['A_original_stage0_Root1']
 ac = posts['A_continuation_Root0_no_new_child']
 ax = posts['A_full_extract_Root0_child2']
 bc = posts['B_full_capture_Root0_child0']
 mp = posts['B4_member0_old_Root0_no_child']
 b4 = posts['B4_all4_Root0_child0']
 am = projection['A_material_saved_full_pin']
 af = projection['A_final55_saved_full_pin']
 ae = projection['A_early7_saved_full_pins']
 bf = projection['B_final55_saved_full_pin']
 be = projection['B_early7_saved_full_pins']
 need(ao['actual_material_stage_closed0'] is True and ao['all_new_scene_files_full_EOF_read_once_with_pin_cache'] is True and all((p in ao['actual_scene_full_EOF_pins'] for p in [am, af] + ae)) and (reports['A_original_stage0_Root1']['status'] == 'FAILED_CURRENT_OBSERVATION_NO_RETRY') and (reports['A_original_stage0_Root1']['failure'] is not None), 'A original Root1 release-blocked remains failed with true stage0 exact fullEOF native9')
 need(ac['actual_original_Root_integer_exit_code'] == 1 and ac['actual_new_material_child_launch_count'] == 0 and (ac['original_capture_collector_reexecuted'] is False) and (ac['actual_complete_state_snapshot_pin_count'] == 8) and (ac['actual_complete_context_pin_count'] == 55), 'separate A continuation0 exact8/55 without new material child or Root1 relabel')
 achild = meta(proof['A_full_extract_Root0_child2']['child_report'])
 need(ax['actual_child_report_pin'] == proof['A_full_extract_Root0_child2']['child_report'] and ax['actual_child_integer_exit_code'] == 2 and (ax['actual_complete_snapshot_count'] == 8) and (ax['actual_complete_context_count'] == 55) and ([r['input_pin'] for r in achild['states']['A']] == ae + [af]), 'real A full8 extraction original input PFs in exact order')
 need(bc['actual_child_integer_exit_code'] == 0 and all((p in bc['new_output_blind_fullEOF_SHA_current7_twice_pins'] for p in be + [bf])), 'real B capture native8 complete original blind2 saved PFs')
 gz = plan['existing_complete_B4_gzip_pin']
 ep = plan['existing_B4_member0_entry_pin']
 ip = plan['existing_B4_all4_lookup_index_pin']
 oldm = plan['historical_B4_original_m_full_pin']
 entry = meta(ep)
 index = meta(ip)
 need(mp['actual_child_integer_exit_code'] is None and mp['Root_actual_complete_member0_stream_verified'] is True and (mp['original_member0_saved_full_pin'] == oldm) and (mp['complete_member0_gzip_pin'] == gz) and (mp['retained_member0_entry_pin'] == ep) and (mp['actual_streamed_decompressed_SHA'] == oldm['sha256']) and (mp['actual_streamed_decompressed_length'] == oldm['size_bytes']), 'old m Root0 stream proof retained as old-path evidence only, not new Bfinal control')
 need(b4['actual_child_integer_exit_code'] == 0 and b4['Root_recorded_stream_decompression_proofs_matched_original_fullPF'] is True and (b4['actual_archive_index_pin'] == ip) and (b4['ordered4_original_product_full_pins'][0] == oldm) and (b4['ordered4_compressed_archive_full_pins'][0] == gz) and (b4['ordered4_entry_pins'][0] == ep) and (len(index['entries']) == 4) and (index['entries'][0]['entry_pin'] == ep) and (index['entries'][0]['original_plain_full_pin'] == oldm) and (index['entries'][0]['compressed_archive_full_pin'] == gz) and (entry['original_plain_full_pin'] == oldm) and (entry['compressed_archive_full_pin'] == gz) and (entry['original_plain_preserved'] is True) and (entry['exact_original_plain_bytes_recoverable'] is True), 'precise permanent B4 m gzip/entry/all4 index and old creation-history preserved')
 need(entry['compression_input_SHA'] == entry['streamed_decompressed_SHA'] == oldm['sha256'] == bf['sha256'] and entry['compression_input_length'] == entry['streamed_decompressed_length'] == oldm['size_bytes'] == bf['size_bytes'] == 76594248 and (gz['size_bytes'] == 33559716), 'saved Bfinal and oldm exact SHA/length equality; fresh control still pending')
 for m in maps:
     if m['mode'] == 'retained_native_copy':
         c = m['canonical_pin']
         need(c in canonical and (c['sha256'], c['size_bytes']) == (m['target_pin']['sha256'], m['target_pin']['size_bytes']), 'each explicit native-copy role saved fullSHA/length equality')
     else:
         need(m['mode'] == 'existing_complete_gzip_member' and m['target_pin'] == bf and (m['canonical_gzip_pin'] == gz) and (m['canonical_entry_pin'] == ep) and (m['canonical_B4_lookup_index_pin'] == ip) and (m['historical_original_member0_full_pin'] == oldm), 'only exact Bfinal mapped to complete archived oldm bytes')
 retained = unique(plan['retained_current7_pins'] + plan['retained_archive_metadata_current7_pins'] + plan['explicit_cumulative_metadata_file_pins'] + plan['retained_B2_current_epoch_readonly_pins'] + [gz, ep, ip])
 historical_absence(plan)
 need(report['exact_ordered10_candidate_full_pins']==targets and report['retained_ordered7_canonical_native_full_pins']==canonical and report['all17_native_full_pins']==all17 and report['exact_ordered10_recovery_mappings']==maps and report['candidate_total_bytes']==232289584 and report['all17_native_total_bytes']==368221520,'same exact ordered candidate10/canonical7/maps17 as actual Source plan')
 proofs=report['all17_native_blind_fullEOF_SHA_length_proofs'];need(type(proofs)is list and len(proofs)==17 and [x['original_full_pin']for x in proofs]==all17,'all17 complete proof rows in exact original order')
 for p,row in zip(all17,proofs):need(row['blind_fullEOF_SHA_length']==dict(sha256=p['sha256'],size_bytes=p['size_bytes'],full_EOF=True,stable_opened_and_EOF_identity=p['identity']),'Root recorded each complete native blind SHA/length and before/opened/EOF stable7 matches exact fullPF; post never rereads native body')
 expectedgzip=dict(sha256=gz['sha256'],size_bytes=gz['size_bytes'],full_EOF=True,stable_opened_and_EOF_identity=gz['identity'])
 need(report['all17_native_fullEOF_SHA_and_stable7_verified']is True and report['all17_native_current7_verified_before_and_after']is True and report['existing_complete_B4_gzip_pin']==gz and report['existing_B4_member0_entry_pin']==ep and report['existing_B4_all4_lookup_index_pin']==ip and report['historical_B4_original_m_full_pin']==oldm and report['new_B_final55_full_pin']==bf and report['new_B_final55_streamed_decompressed_SHA']==bf['sha256']and type(report['new_B_final55_streamed_decompressed_length'])is int and report['new_B_final55_streamed_decompressed_length']==bf['size_bytes']and report['new_B_final55_independent_complete_stream_verified']is True and report['gzip_blind_fullEOF_before']==report['gzip_blind_fullEOF_after']==expectedgzip,'new same-Bfinal actual complete gzip stream SHA/length, not old B4 member0 proof substituted')
 need(report['actual_prerequisite_closure_pins']==proof and report['exact4_prerequisite_closure_pins']==cp and type(report['old_A_Root_integer_exit_code'])is int and report['old_A_Root_integer_exit_code']==1 and type(report['A_continuation_Root_integer_exit_code'])is int and report['A_continuation_Root_integer_exit_code']==0 and type(report['A_continuation_new_material_children_started'])is int and report['A_continuation_new_material_children_started']==0 and report['old_B4_member0_proof_relabelled_as_new_B_final55_control']is False,'original A Root1 and separate continuation0/no new child preserved; old B4m is historical original role')
 need(type(report['children_started'])is int and report['children_started']==0 and report['actual_child_integer_exit_code']is None and report['all_retained_roles_current7_verified']is True and report['new_data_owning_root_created']is False and report['bounded_own_Source_metadata_receipts_bytes']==source_limit and report['original_caps']==CAPS,'actual Root-only no child or new root; no child0 inferred')
 for k in('retained_current7_pins','retained_archive_metadata_current7_pins','retained_B2_current_epoch_readonly_pins','retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins','exact49_historical_absent_pins'):need(report[k]==plan[k],'same exact saved current and narrowly historical role tables')
 build=meta(plan['original_guard_build_plan_pin'])
 for _ in range(2):
  for p in all17+[gz]:current(p)
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
  for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
  historical_absence(plan)
 need(type(report['Root_SELF_peak_bytes'])is int and report['Root_SELF_peak_bytes']<512*2**20 and 0<report['Root_elapsed_seconds']<600,'actual Root original SELF512/stage600')
 for k in('resources_before','resources_after','resources_after_including_summary_bytes'):native_compact_resource_facts(report[k],roots)
 need(bool(report['original_resource_scalar_snapshots']),'actual compact resource observations retained')
 for v in report['original_resource_scalar_snapshots']:native_compact_resource_facts(v,roots)
 for k in('restored_large_file_written','native_or_scientific_values_decoded','compiler_executed','native_executed','compression_executed','files_deleted','retirement_authorized','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(report[k]is False,'byte preservation control never grants retirement or numerical/physics qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full83/external/open-unlinked/cold/free original caps include post bytes')
 for p in[pRoot,pReport,ps,pp,pr,pt,EXPECTED_CORE_AUTHOR_FREEZE,EXPECTED_FROZEN_CLI_TEMPLATE_PIN,core['report_field_projection_pin'],plan['role_projection_pin'],ep,ip]:full(p)
 result=dict(schema='RECORDED_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_ROOT_NATIVE_EXACT10_COMPLETE_BYTE_PRESERVATION_CONTROL_ROOT0_METADATA_ONLY_NO_RETIREMENT',failure=None,actual_Root_tools_pin=pRoot,actual_native10_Root_report_pin=pReport,actual_Root_integer_exit_code=0,actual_children_started=0,actual_child_integer_exit_code=None,no_child0_invented_for_Root_only_control=True,source_pin=ps,plan_pin=pp,core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,actual_Source_review_pin=pr,actual_Source_review_tools_pin=pt,exact_frozen_CLI_template_pin=EXPECTED_FROZEN_CLI_TEMPLATE_PIN,actual_Root_argv_matches_frozen_template_except_two_genuine_peer_roles=True,role_projection_pin=plan['role_projection_pin'],exact_ordered10_candidate_full_pins=targets,retained_ordered7_canonical_native_full_pins=canonical,exact_ordered10_recovery_mappings=maps,all17_native_full_pins=all17,candidate_total_bytes=232289584,all17_native_total_bytes=368221520,Root_recorded_all17_native_blind_fullEOF_SHA_length_proofs=proofs,Root_recorded_all17_native_fullEOF_SHA_and_stable7_verified=True,all17_native_current7_only_verified_twice_by_post=True,existing_complete_B4_gzip_pin=gz,existing_B4_member0_entry_pin=ep,existing_B4_all4_lookup_index_pin=ip,historical_B4_original_m_full_pin=oldm,new_B_final55_full_pin=bf,new_B_final55_streamed_decompressed_SHA=report['new_B_final55_streamed_decompressed_SHA'],new_B_final55_streamed_decompressed_length=report['new_B_final55_streamed_decompressed_length'],Root_new_B_final55_independent_complete_stream_verified=True,actual_gzip_blind_fullEOF_before=report['gzip_blind_fullEOF_before'],actual_gzip_blind_fullEOF_after=report['gzip_blind_fullEOF_after'],gzip_current7_only_by_post=True,native_or_gzip_body_opened_or_hashed_by_post=False,decompression_repeated_by_post=False,actual_prerequisite_closure_pins=proof,exact4_prerequisite_closure_pins=cp,old_A_Root_integer_exit_code=1,A_continuation_Root_integer_exit_code=0,A_continuation_new_material_children_started=0,old_B4_member0_proof_relabelled_as_new_B_final55_control=False,retained_all_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],exact49_historical_absent_pins=plan['exact49_historical_absent_pins'],all_retained_roles_current7_verified_twice=True,exact49_historical_absence_only_verified_twice=True,complete_joint_roots=roots,new_data_owning_root_created=False,original_caps=CAPS,local_Source_bound_bytes=source_limit,actual_Root_SELF_peak_bytes=report['Root_SELF_peak_bytes'],actual_Root_elapsed_seconds=report['Root_elapsed_seconds'],actual_original_resources_before=report['resources_before'],actual_original_resources_after=report['resources_after'],actual_original_resources_after_including_summary=report['resources_after_including_summary_bytes'],actual_original_resource_scalar_snapshots=report['original_resource_scalar_snapshots'],actual_final_report_resource_check_passed=True,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)

if __name__=='__main__':main()
