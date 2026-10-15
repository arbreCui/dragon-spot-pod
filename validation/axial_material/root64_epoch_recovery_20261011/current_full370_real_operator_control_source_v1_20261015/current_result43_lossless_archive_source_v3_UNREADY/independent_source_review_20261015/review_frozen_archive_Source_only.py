"""Formal v3 Source-only archive review; reads no plain/native payloads."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent

def need(v,m):
 if v is not True:raise ValueError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ident(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7 '+str(q))
def pin(q):
 q=Path(q);r=q.read_bytes();t=q.lstat();return dict(path=str(q),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=ident(t))
def full(p):
 current(p);need(p['size_bytes']<8*2**20,'bounded Source/report metadata8MiB')
 with Path(p['path']).open('rb')as f:
  need(ident(os.fstat(f.fileno()))==p['identity'],'opened Source/meta7');r=f.read();need(ident(os.fstat(f.fileno()))==p['identity'],'EOF Source/meta7')
 need(len(r)==p['size_bytes']and hashlib.sha256(r).hexdigest()==p['sha256'],'whole Source/meta SHA');current(p);return r
def unique(rows):
 d={}
 for p in rows:need(p['path']not in d or d[p['path']]==p,'consistent fullPF');d[p['path']]=p
 return list(d.values())
def genuine(d,key,chunk,p,field):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and r['chunk_id']==chunk and json.loads(r['output'].strip().splitlines()[-1])[field]==p,'genuine original typed0/PF')

def main():
 pready=pin(D/'SOURCE_REVIEW_READY.json');pg=pin(D/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
 need(pready['sha256']=='d568a41eb3c42c54f35368226cb9e5fa3caf8fd08ff7c7ae709ea6950fb3ff61'and pg['sha256']=='18a901dd85cab7ec1ef844dc14b0a9a3a08fd3a69a8409049404031a86cac408','exact Root supplied ready/gen')
 ready=json.loads(full(pready));gen=json.loads(full(pg));genuine(gen,'actual_Source_preparation_return','9a6d28',pready,'ready_pin')
 selected=unique(ready['selected_Source_pins']+[pready,pg]);ready_union_count=len(selected)
 raw={p['path']:full(p)for p in selected};pb=ready['execution_binding_pin'];need(pb==ready['control_plan_pin']and pb['sha256']=='919334f526bf5521815053a96410867a2561764feb118357c0fa4256683f4eae','exact PLAN binding')
 binding=json.loads(raw[pb['path']]);authorpin=binding['Source_author_freeze_pin'];author=json.loads(raw[authorpin['path']]);need(authorpin['sha256']=='cfa15919d0cc9ca10efc4c285280f716f952026fb43333819b6965c49bb2d1f5'and author['author_STOP_WRITES']is True and len(author['source_pins'])==5,'frozen author5 Source')

 priorpin=binding['prior_frozen_v2_author_pin'];priorauthor=json.loads(full(priorpin))
 priorproofs=[priorpin,binding['prior_v2_Source_generation_true_tools_pin'],binding['prior_v2_Source_READY_pin'],binding['prior_v2_PLAN_pin'],binding['prior_v2_Source_blocker_review_pin'],binding['prior_v2_Source_blocker_true_tools_pin'],author['static_facts_pin'],author['own_metadata_preflight_failure_pin']]+priorauthor['source_pins']+[binding['original_production_resource_Source_pin']]
 selected=unique(selected+priorproofs);raw.update({p['path']:full(p)for p in priorproofs})
 priorready=json.loads(raw[binding['prior_v2_Source_READY_pin']['path']]);priorgen=json.loads(raw[binding['prior_v2_Source_generation_true_tools_pin']['path']]);priorplan=json.loads(raw[binding['prior_v2_PLAN_pin']['path']]);priorreview=json.loads(raw[binding['prior_v2_Source_blocker_review_pin']['path']]);priortools=json.loads(raw[binding['prior_v2_Source_blocker_true_tools_pin']['path']])
 genuine(priorgen,'actual_Source_preparation_return','c738e9',binding['prior_v2_Source_READY_pin'],'ready_pin');genuine(priortools,'actual_review_return','bc7d7a',binding['prior_v2_Source_blocker_review_pin'],'review_pin')
 need(priorreview['status']=='FAIL_SOURCE_ONLY'and type(priorreview['failure'])is dict and priorreview['failure']['kind']=='TWO_OWNING_HOST_METADATA_PATHS_OMIT_ORIGINAL_STAGE_PREFIX'and len(priorreview['failure']['blockers'])==2 and binding['prior_v2_Source_blocker_failure']==priorreview['failure']and binding['prior_v2_Source_blocker_status']==priorreview['status'],'real prior failed dict classification unchanged')
 need(priorreview['publisher_admission_refused']is True and priorreview['business_admission_refused']is True and binding['prior_v2_business_started']is False and binding['prior_v2_has_no_actual_business_failure']is True,'prior Source failure never admission/business failure')
 ownerror=json.loads(raw[author['own_metadata_preflight_failure_pin']['path']]);need(ownerror['actual_tool_chunk_id']=='22751b'and type(ownerror['actual_original_integer_exit_code'])is int and ownerror['actual_original_integer_exit_code']==1 and ownerror['candidate_Source_generation_executed']is False and ownerror['business_executed']is False,'author original ownmetadata1 preserved')
 unchanged=[];priorbyname={Path(p['path']).name:p for p in priorauthor['source_pins']}
 replacements=[("watchpath=out/'serial_result48_byte_archive.watchdog.json'","watchpath=out/(runner.records[0]['label']+'.watchdog.json')"),("log=out/'serial_result48_byte_archive.log'","log=out/(runner.records[0]['label']+'.log')")]
 for p in author['source_pins']:
  name=Path(p['path']).name;now=raw[p['path']];previous=raw[priorbyname[name]['path']]
  if name=='run_guarded_result43_lossless_archive.UNREADY.py':
   inverse=now
   for before,after in replacements:need(now.count(after.encode())==1 and previous.count(before.encode())==1,'exact two unique path replacements');inverse=inverse.replace(after.encode(),before.encode())
   need(inverse==previous,'entire host inverse exactv2 only two metadata paths')
  else:need(now==previous,'entire other4 Source unchanged');unchanged.append(name)
 need(len(unchanged)==4 and author['source_pins']==ready['complete_source_file_pins'],'exact frozen five Source whole inverse')
 facts=json.loads(raw[author['static_facts_pin']['path']]);need(facts['host_whole_inverse_exact_v2']is True and facts['actual_prior_Source_review_failure']==priorreview['failure'],'Source facts match actual whole inverse and failure dict')
 for key in ('all48_plain_pins','retained_native_current7_pins','complete_joint_roots','inherited_latest_complete_joint_roots','planned_actual_output_root','original_caps','bounded_total_output_bytes','bounded_archive_payload_bytes','reserved_metadata_runtime_bytes','bounded_Source_metadata_bytes','old30_intersection_paths','historical_completed_guard_role_paths','completed_A2_host_pin','completed_A2_Root_tools_pin','completed_A2_post_pin','completed_A2_post_tools_pin','early14_closure_pins'):
  need(binding[key]==priorplan[key],'unchanged role/scope/cap '+key)
 for p in ready['complete_source_file_pins']:ast.parse(raw[p['path']].decode(),filename=p['path'])
 plain=binding['all48_plain_pins'];retained=binding['retained_native_current7_pins'];need(len(plain)==48 and len(retained)==66 and sum(p['size_bytes']for p in plain)==805236925 and ready['old48_plain_and_retained66_current7_only_pins']==plain+retained,'exact48/805236925 and66 protected roles')
 for p in plain+retained:current(p)
 need(binding['complete_joint_roots']==binding['inherited_latest_complete_joint_roots']+[binding['planned_actual_output_root']]and len(binding['inherited_latest_complete_joint_roots'])==64 and len(binding['complete_joint_roots'])==65 and not os.path.lexists(binding['planned_actual_output_root']),'entire64 prefix plus fresh owning65 unexecuted')
 need(binding['bounded_total_output_bytes']==192*2**20 and binding['bounded_archive_payload_bytes']==184*2**20 and binding['reserved_metadata_runtime_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==16*2**20 and binding['compression_ratio_assumed']is False,'original complete192/184+8/Source16 no assumed compression')
 cp=binding;host=json.loads(raw[cp['completed_A2_host_pin']['path']]);post=json.loads(raw[cp['completed_A2_post_pin']['path']]);root=json.loads(raw[cp['completed_A2_Root_tools_pin']['path']]);pt=json.loads(raw[cp['completed_A2_post_tools_pin']['path']])
 genuine(root,'actual_terminal_return','da510e',cp['completed_A2_host_pin'],'report_pin');genuine(pt,'actual_review_return','4d14cc',cp['completed_A2_post_pin'],'review_pin')
 need(host['actual_child_evidence_only_integer_exit_code']==2 and post['original_FAILED_error2_record_retained']is True and post['actual_compared_source_fields']==19249 and post['actual_context_event_count']==55 and post['actual_snapshot_count']==8 and post['actual_context_or_operand_issues']==0,'actual A2 full scope/child2 preserved')
 ep=binding['early14_closure_pins'];er=json.loads(raw[ep['receipt']['path']]);et=json.loads(raw[ep['Root_tools']['path']]);ept=json.loads(raw[ep['post_tools']['path']]);earlypost=json.loads(raw[ep['post']['path']])
 genuine(et,'actual_execution_return','92150e',ep['receipt'],'receipt_pin');genuine(ept,'actual_review_return','63ede6',ep['post'],'review_pin')
 projection=binding['early14_post_actual_role_projection'];need(earlypost['schema']==projection['schema']and earlypost['status']==projection['status']and earlypost[projection['receipt_pin_field']]==ep['receipt']and earlypost[projection['Root_tools_pin_field']]==ep['Root_tools']and er['actual_released_bytes']==149659264 and er['actual_released_pins']==binding['actual_retired_early14_pins']and earlypost['original_v1_readonly_failure1_preserved']is True,'exact early14 actual0/post0 projection and failedv1 preserved')
 for p in binding['actual_retired_early14_pins']:need(not os.path.lexists(p['path']),'retired14 absent')
 intersection=json.loads(raw[binding['original_result43_old_input_intersection_pin']['path']]);need(binding['old30_intersection_paths']==[p['path']for p in intersection['exact_original_input_intersection_pins']]and len(binding['old30_intersection_paths'])==30 and len(binding['completed_A2_new5_JSONL_pins'])==5,'old30 historical input lookup and new5 separate')
 worker=raw[str(D/'archive_result43_serial.UNREADY.py')].decode();need('os.unlink'not in worker and 'streamed_decompressed_SHA'in worker and "uncompressed_sha.hexdigest()==p['sha256']"in worker and "uncompressed_length==p['size_bytes']"in worker,'streaming gzip/decoded-byte SHA-length proof without plain unlink or value decoding')
 hs=raw[ready['host_source_pin']['path']].decode();need("watchpath=out/(runner.records[0]['label']+'.watchdog.json')"in hs and "log=out/(runner.records[0]['label']+'.log')"in hs and "runner.execute(stage,'serial_result48_byte_archive'"in hs and "stage=out/'archive-stage'"in hs,'two corrected exact original stage/record path bindings')
 parentpin=binding['original_production_resource_Source_pin'];parent=full(parentpin).decode();need('"label": str(directory.relative_to(self.work) / label)'in parent and 'log = directory / f"{label}.log"'in parent,'original SerialExecutor path-prefix semantics authoritative Source')
 label=host['records'][0]['label'];need(label=='evidence-stage/complete_A_aggregate_after_OVERV_control','same original runner actual prefixed record corroboration')
 blockers=priorreview['failure']['blockers']
 for p in selected:full(p)
 for p in plain+retained:current(p)
 for p in binding['actual_retired_early14_pins']:need(not os.path.lexists(p['path']),'retired14 still absent')
 report=dict(schema='INDEPENDENT_RESULT48_LOSSLESS_ARCHIVE_FORMAL_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_TWO_METADATA_PATH_FIX_WHOLE_INVERSE',failure=None,source_only=True,
  binding_pin=pb,selected_Source_pins=selected,complete_selected_Source_union_count=len(selected),ready_selected_Source_count=len(ready['selected_Source_pins']),ready_plus_generation_union_count=ready_union_count,complete_selected_Source_metadata_fullEOF_SHA_current7_verified_twice=True,Source_review_ready_pin=pready,Root_Source_generation_true_tools_pin=pg,author_Source_freeze_pin=authorpin,
  original_SerialExecutor_Source_pin=parentpin,original_SerialExecutor_execute_lines=[687,727],original_actual_A2_prefixed_record_label=label,
  expected_archive_original_record_label='archive-stage/serial_result48_byte_archive',two_metadata_path_fixes_verified=True,host_whole_inverse_exact_v2=True,other4_Source_whole_identical_v2=True,prior_v2_FAILED_Source_review_pin=binding['prior_v2_Source_blocker_review_pin'],prior_v2_FAILED_Source_tools_pin=binding['prior_v2_Source_blocker_true_tools_pin'],prior_v2_failed_status=priorreview['status'],prior_v2_failure=priorreview['failure'],prior_v2_original_audit_integer_exit_code=0,prior_v2_business_never_started=True,author_own_metadata_preflight1_preserved=True,author_own_metadata_preflight_failure_pin=author['own_metadata_preflight_failure_pin'],
  all48_plain_count=48,all48_plain_total_bytes=805236925,all66_retained_current7_preserved=True,old_plain_and_native_roles_current7_verified_twice_only=True,
  original_A2_Root0_child2_post0_scope_preserved=True,early14_actual0_post0_fullPF_projection_preserved=True,old30_historical_input_guard_lookup_and_new5_roles_separate=True,complete_joint_roots=binding['complete_joint_roots'],original_caps=binding['original_caps'],
  bounded_total_output_bytes=192*2**20,bounded_archive_payload_bytes=184*2**20,reserved_metadata_runtime_bytes=8*2**20,bounded_Source_metadata_bytes=16*2**20,compression_ratio_assumed=False,archive_size_or_runtime_fit_claimed=False,
  reviewer_source_pin=pin(Path(__file__).absolute()),auditor_Source_freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json'),
  Source_generation_repeated=False,worker_or_helpers_imported=False,publisher_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,native_executed=False,compression_executed=False,decompression_executed=False,files_deleted=False,old_plain_or_SCI_XSM_SQL_pool_JSONL_bodies_opened=False,old_plain_or_science_body_SHA_recomputed=False,result_values_decoded=False,
  physics_qualified=False,scientific_accuracy_qualified=False,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=BASE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(q)),separators=(',',':')),flush=True)
if __name__=='__main__':main()
