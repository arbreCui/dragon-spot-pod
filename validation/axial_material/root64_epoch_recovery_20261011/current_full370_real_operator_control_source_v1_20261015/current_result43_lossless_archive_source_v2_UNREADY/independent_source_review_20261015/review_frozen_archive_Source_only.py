"""Formal failed Source-only archive review; reads no plain/native payloads."""
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
 need(pready['sha256']=='f2f3da1466294cf5a7180422a6c773805078c465cdc23e559d8b3735636fb59a'and pg['sha256']=='6d254336d6cfaa11582c14dad56caddefcab66280695c961aea9acc4b5f1ff71','exact Root supplied ready/gen')
 ready=json.loads(full(pready));gen=json.loads(full(pg));genuine(gen,'actual_Source_preparation_return','c738e9',pready,'ready_pin')
 selected=unique(ready['selected_Source_pins']+[pready,pg]);need(len(selected)==25,'complete selected23+READY+genuineGEN25')
 raw={p['path']:full(p)for p in selected};pb=ready['execution_binding_pin'];need(pb==ready['control_plan_pin']and pb['sha256']=='8955e2b6bb632666eb36bcd16e4fce80e5bc45a10058b177886862f06dfcbdcc','exact PLAN binding')
 binding=json.loads(raw[pb['path']]);authorpin=binding['Source_author_freeze_pin'];author=json.loads(raw[authorpin['path']]);need(authorpin['sha256']=='bc04a50126f5f7c452d5ded9f2c14c28d3f53e977ecaf17359fdca185832cb7f'and author['author_STOP_WRITES']is True and len(author['source_pins'])==5,'frozen author5 Source')
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
 hs=raw[ready['host_source_pin']['path']].decode();need("watchpath=out/'serial_result48_byte_archive.watchdog.json'"in hs and "log=out/'serial_result48_byte_archive.log'"in hs and "runner.execute(stage,'serial_result48_byte_archive'"in hs,'two exact frozen path blockers present')
 parentpin=binding['original_production_resource_Source_pin'];parent=full(parentpin).decode();need('"label": str(directory.relative_to(self.work) / label)'in parent and 'log = directory / f"{label}.log"'in parent,'original SerialExecutor path-prefix semantics authoritative Source')
 label=host['records'][0]['label'];need(label=='evidence-stage/complete_A_aggregate_after_OVERV_control','same original runner actual prefixed record corroboration')
 blockers=[dict(source_path=ready['host_source_pin']['path'],line=77,observed="out/'serial_result48_byte_archive.watchdog.json'",required="out/(runner.records[0]['label']+'.watchdog.json')",actual_stage_path='archive-stage/serial_result48_byte_archive.watchdog.json'),dict(source_path=ready['host_source_pin']['path'],line=82,observed="out/'serial_result48_byte_archive.log'",required="out/(runner.records[0]['label']+'.log')",actual_stage_path='archive-stage/serial_result48_byte_archive.log')]
 for p in selected:full(p)
 for p in plain+retained:current(p)
 for p in binding['actual_retired_early14_pins']:need(not os.path.lexists(p['path']),'retired14 still absent')
 report=dict(schema='INDEPENDENT_RESULT48_LOSSLESS_ARCHIVE_FORMAL_SOURCE_REVIEW_V1',status='FAIL_SOURCE_ONLY',failure=dict(kind='TWO_OWNING_HOST_METADATA_PATHS_OMIT_ORIGINAL_STAGE_PREFIX',blockers=blockers),source_only=True,
  binding_pin=pb,selected_Source_pins=selected,complete_selected_Source_union_count=25,complete_selected_Source_metadata_fullEOF_SHA_current7_verified_twice=True,Source_review_ready_pin=pready,Root_Source_generation_true_tools_pin=pg,author_Source_freeze_pin=authorpin,
  original_SerialExecutor_Source_pin=parentpin,original_SerialExecutor_execute_lines=[687,727],original_actual_A2_prefixed_record_label=label,
  expected_archive_original_record_label='archive-stage/serial_result48_byte_archive',publisher_admission_refused=True,business_admission_refused=True,
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
