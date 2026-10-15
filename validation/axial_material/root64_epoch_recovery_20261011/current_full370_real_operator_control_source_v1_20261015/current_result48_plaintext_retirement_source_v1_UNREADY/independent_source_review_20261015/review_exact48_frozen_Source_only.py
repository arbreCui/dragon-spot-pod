"""Independent exact48 Source/metadata review; never opens target, gzip or native payloads."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent

def need(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
 r=q.read_bytes();s=q.lstat();return dict(path=str(q),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=ids(s))
def current(p):
 need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'fullPF integer schema')
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7')
 return s
def full(p):
 current(p);need(p['size_bytes']<8*2**20,'bounded Source/metadata8MiB')
 with Path(p['path']).open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened metadata7');r=f.read();need(ids(os.fstat(f.fileno()))==p['identity'],'EOF metadata7')
 need(len(r)==p['size_bytes']and hashlib.sha256(r).hexdigest()==p['sha256'],'whole Source/metadata SHA');current(p);return r
def unique(rows):
 d={}
 for p in rows:need(p['path']not in d or d[p['path']]==p,'consistent fullPF union');d[p['path']]=p
 return list(d.values())
def genuine(d,key,chunk,p,role):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and r['chunk_id']==chunk and type(r['exit_code'])is int and r['exit_code']==0 and not r.get('session_id')and json.loads(r['output'].strip().splitlines()[-1])[role]==p,'genuine typed original0 exact stdoutPF')

def main():
 pa=pin(D/'AUTHOR_SOURCE_FREEZE.json');need(pa['sha256']=='5f3636448b373608e5034477144062d75cfc9f3f3fddad8bdbd6f5fcecb492a9','exact frozen AUTHOR');author=json.loads(full(pa));pp=author['whole_plan_pin'];need(pp['sha256']=='c43eb68cc73422ed7cedcee2f679172d31b83feec85fe6141243cfa64b240725','exact frozen PLAN');plan=json.loads(full(pp))
 need(author['author_STOP_WRITES']is True and author['source_only']is True and len(author['whole_Source_file_pins'])==2,'author frozen two Source')
 cp=plan['actual_archive_closure_pins'];resourcepins=[plan[k]for k in('original_production_inputs_Source_pin','original_production_resource_Source_pin','original_history_resource_Source_pin')]
 selected=unique([pa,pp,author['reviewable_CLI_template_pin']]+author['whole_Source_file_pins']+list(cp.values())+[plan['inherited_complete65_archive_plan_pin']]+resourcepins+[plan['old_failed_archive_v2_Source_review_pin'],plan['old_failed_archive_v2_Source_tools_pin']]);raw={p['path']:full(p)for p in selected}
 for p in author['whole_Source_file_pins']+resourcepins:ast.parse(raw[p['path']].decode(),filename=p['path'])
 workerpin=next(p for p in author['whole_Source_file_pins']if Path(p['path']).name=='retire_exact48_archived_result_plaintexts.UNREADY.py');need(workerpin['sha256']=='b7d4f3493c7f557b99f755a959719c18ac8829851d3262bad6b5360c97c5dc1b','exact worker')
 template=json.loads(raw[author['reviewable_CLI_template_pin']['path']]);need(template['worker_Source_pin']==workerpin and template['plan_pin']==pp,'exact CLI template Source roles')
 host=json.loads(raw[cp['Host']['path']]);root=json.loads(raw[cp['Root_tools']['path']]);post=json.loads(raw[cp['post']['path']]);tools=json.loads(raw[cp['post_tools']['path']]);index=json.loads(raw[cp['index']['path']]);child=json.loads(raw[cp['child_report']['path']]);aplan=json.loads(raw[plan['inherited_complete65_archive_plan_pin']['path']])
 genuine(root,'actual_terminal_return','86373c',cp['Host'],'report_pin');genuine(tools,'actual_review_return','3ab8b9',cp['post'],'review_pin')
 need(root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False and host['status']=='ACTUAL_ALL48_ARCHIVED_ROUNDTRIP_CLOSED0_PLAIN_RETAINED'and host['failure']is None and host['archive_complete']is True and host['final_report_resource_check_passed']is True,'real complete archive/no retry')
 w=host['actual_watchdog'];need(len(host['records'])==1 and host['records'][0]['status']=='PASS'and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['elapsed_seconds']<w['wall_cap_seconds']<=600 and w['sampled_peak_rss_mib']<512,'original guarded child0 caps')
 projection=plan['actual_archive_post_key_projection'];need(post['schema']==projection['schema']and post['status']==projection['status']and post['failure']is None and post['metadata_only']is True and post[projection['Host_pin_field']]==cp['Host']and post[projection['Root_tools_pin_field']]==cp['Root_tools']and post[projection['index_pin_field']]==cp['index'],'actual post projection')
 targets=plan['exact_target_pins'];gz=plan['retained_all48_gzip_pins'];rows=index['entries']
 need(len(targets)==len(gz)==len(rows)==48 and len({p['path']for p in targets})==48 and sum(p['size_bytes']for p in targets)==plan['planned_released_bytes']==plan['target_total_bytes']==805236925 and sum(p['size_bytes']for p in gz)==post['gzip_bytes']==68959717,'exact48/805236925 to real gzip68959717')
 need(post[projection['ordered_original_pins_field']]==targets and post[projection['ordered_archive_pins_field']]==gz and [r['original_plain_full_pin']for r in rows]==targets and [r['compressed_archive_full_pin']for r in rows]==gz and [r['entry_pin']for r in rows]==post['ordered48_entry_pins'],'complete48 ordered proof tables')
 for row,p in zip(rows,targets):need(row['compression_input_SHA']==row['streamed_decompressed_SHA']==p['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==p['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True,'actual byteSHA length proof metadata only')
 need(child['failure']is None and child['completed_count']==48 and child['index_pin']==cp['index']and host['actual_child_receipt']['report_pin']==cp['child_report'],'actual child/index identity')
 need(len(plan['old30_historical_guard_pins'])==30 and len(plan['new5_completed_A2_result_pins'])==5 and plan['old30_historical_guard_pins']==post['old30_historical_guard_pins']and plan['new5_completed_A2_result_pins']==post['new5_completed_A2_result_pins']and all(p in targets for p in plan['old30_historical_guard_pins']+plan['new5_completed_A2_result_pins']),'old30/new5 historical roles distinct')
 roots=plan['complete_joint_roots'];need(roots==plan['actual_archive_complete65_prefix']==aplan['complete_joint_roots']==host['complete_joint_roots']and len(roots)==65 and plan['no_new_output_root']is True and plan['original_caps']==aplan['original_caps']==host['original_caps']and plan['bounded_own_Source_metadata_receipts_bytes']==16*2**20,'whole65 prefix/no reset/no newOUT/unchanged caps')
 native=plan['retained_native_current7_pins'];metadata=plan['retained_archive_metadata_current7_pins'];external=plan['explicit_cumulative_metadata_file_pins'];retained=unique(native+metadata+gz+external)
 need(len(native)==66 and native==aplan['retained_native_current7_pins']and len(metadata)==65 and not {p['path']for p in targets}&{p['path']for p in retained},'all retainer roles exclude48 targets')
 for p in targets:
  st=current(p);need(st.st_uid==501==os.getuid()and st.st_nlink==1,'target owned501/nlink1')
 for p in retained:current(p)
 failed=json.loads(raw[plan['old_failed_archive_v2_Source_review_pin']['path']]);ft=json.loads(raw[plan['old_failed_archive_v2_Source_tools_pin']['path']]);genuine(ft,'actual_review_return','bc7d7a',plan['old_failed_archive_v2_Source_review_pin'],'review_pin');need(failed['status']=='FAIL_SOURCE_ONLY'and type(failed['failure'])is dict,'original failed Source classified unchanged')
 ws=raw[workerpin['path']].decode();pubpin=next(p for p in author['whole_Source_file_pins']if p!=workerpin);ps=raw[pubpin['path']].decode()
 for text in ("receipt.open('xb')","current(p,True);full(p,budget)","r.returncode==1 and r.stdout==b''and r.stderr==b''","os.stat(q.name,dir_fd=fd,follow_symlinks=False)","os.unlink(q.name,dir_fd=fd);os.fsync(fd)","snapshot(f,d);budget()","budget(True);d['resources_after']=state['latest']","state['history'].check();j=state['joint'].check()","module(plan['original_production_inputs_Source_pin']","str(os.getpid())","not target and str(q)in SYSTEM"):
  need(text in ws,'reviewed original lifecycle guard '+text)
 need(ws.count('os.unlink(')==1 and "current(p,True)"in ws and "require(a.readonly_receipt_pin is not None"in ws and "genuine(ct,'actual_readonly_return',checkpin,'receipt_pin')"in ps and "ct['actual_readonly_permission_mode']=='require_escalated'"in ps and "not os.path.lexists(outfile)"in ps,'one exact unlink loop/readonly genuine0 before execute/nooverwrite')
 for p in resourcepins[1:]:need('checked_unix' in raw[p['path']].decode()and 'time.time()'in raw[p['path']].decode(),'original classes always fresh check timestamps')
 for p in selected:full(p)
 for p in targets+retained:current(p)
 report=dict(schema='INDEPENDENT_EXACT48_PLAINTEXT_RETIREMENT_FORMAL_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_EXACT48_ARCHIVED_PLAINTEXT_LIFECYCLE',failure=None,source_only=True,source_pin=workerpin,plan_pin=pp,author_Source_freeze_pin=pa,publisher_Source_pin=pubpin,selected_Source_pins=selected,complete_Source_metadata_union_count=len(selected),complete_Source_metadata_fullEOF_SHA_current7_verified_twice=True,exact48_target_current7_only_verified_twice=True,all48_target_owned501_nlink1=True,target_count=48,planned_released_bytes=805236925,all48_gzip_current7_only_verified_twice=True,retained_native_count=66,retained_archive_metadata_count=len(metadata),retained_explicit_metadata_count=len(external),all_retained_current7_verified_twice=True,retainer_target_intersection_count=0,actual_archive_closure_pins=cp,actual_archive_Root_integer_exit_code=0,actual_archive_child_integer_exit_code=0,actual_archive_post_integer_exit_code=0,actual_archive_post_schema=post['schema'],actual_archive_post_status=post['status'],Root_streamed_lossless_proof_metadata_matched=True,independent_decompression_or_plain_value_recomparison=False,old30_historical_guard_roles_preserved=True,new5_completed_A2_roles_preserved=True,old_failed_Source_review_status=failed['status'],original_caps=plan['original_caps'],complete_joint_roots=roots,no_new_business_output_root=True,readonly_then_genuine0_execute_gate_verified=True,original_resource_classes_fullPF_preserved_and_forced_fresh_calls_verified=True,exact_lsof_empty_and_dirfd7_unlink_journal_verified=True,reviewer_Source_pin=pin(Path(__file__).absolute()),auditor_Source_freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json'),worker_or_helpers_imported=False,Source_generation_executed=False,publisher_executed=False,readonly_check_executed=False,retirement_executed=False,business_executed=False,PS_executed=False,lsof_executed=False,compiler_executed=False,numerical_executed=False,native_executed=False,old_plain_or_gzip_or_SCI_body_opened=False,old_plain_or_gzip_or_SCI_SHA_recomputed=False,files_deleted=False,physics_qualified=False,scientific_accuracy_qualified=False,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=BASE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(q)),separators=(',',':')),flush=True)
if __name__=='__main__':main()
