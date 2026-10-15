"""Pure standard-library review of sealed failure terminal. Never import business."""
import hashlib,json,struct
from pathlib import Path
D=Path('/private/tmp/axmat_v12_actual_native_AAA_failure_readonly_review_20261009')
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
W=ART/'axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009'
T=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-terminal-v12-20261009'
R=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
P=Path('/private/tmp/axmat_v12_failed_cold_native_independent_raw_review_20261009')
inventory={}
def pin(path,sha=None):
 p=Path(path);assert p.is_file() and not p.is_symlink() and p.is_absolute()
 if str(p) not in inventory:
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  inventory[str(p)]={'sha256':h,'size_bytes':p.stat().st_size}
 if sha is not None:assert inventory[str(p)]['sha256']==sha
 return dict(path=str(p),sha256=inventory[str(p)]['sha256'])
def read(path,sha=None):
 pin(path,sha)
 def pairs(rows):
  value={}
  for k,v in rows:assert k not in value;value[k]=v
  return value
 return json.loads(Path(path).read_text(),object_pairs_hook=pairs)
def exact(a,b):
 assert type(a)is type(b)
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:exact(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):exact(x,y)
 elif isinstance(a,float):assert struct.pack('!d',a)==struct.pack('!d',b)
 else:assert a==b,(a,b)
def descriptor(d):
 assert set(d)=={'path','sha256','bytes'}
 pin(d['path'],d['sha256']);assert type(d['bytes'])is int and d['bytes']==Path(d['path']).stat().st_size
 return d

body=read(D/'REPORT_FAILURE_BODY.json','81cece3995be37378cccda99960f29a37b5560457654472782212b9bcea14ba1')
bodyreceipt=read(D/'actual_failure_body_readonly_tool_return.json','243b0d85f4e9af242ff3600114a5babb876d8e5b88a68a90ddeecf2bebb43b35')
assert bodyreceipt['result']['chunk_id']=='289336' and type(bodyreceipt['result']['exit_code'])is int and bodyreceipt['result']['exit_code']==0
assert bodyreceipt['session_closed'] is True
raw=read(P/'REPORT.json','dd2e06f8850086d58984856bd8d6def474ed14d9607ca8ede3319fd8862e661c')
rawreceipt=read(P/'actual_readonly_tool_return.json','36a2fb5d49b545087db28fd2c43f9561f4f84bd16daaf034e79c3642ce64519a')
assert rawreceipt['chunk_id']=='0f08fb' and type(rawreceipt['exit_code'])is int and rawreceipt['exit_code']==0
term=read(T/'cold_failed_terminal_return.json','c4309539d589e43ce56af798cccf74984148b947e062e56391e8002984b576bc')
receipt=read(R/'Root_actual_cold_AAA_tool_terminal_return.json','27bc485a16605d0180acb46da008459ca42d16bd7be6275fef599d7ec3307ed3')
closed=read(R/'Root_current_actual_cold_AAA_job.json','d95e6c3d91ab07656ed825d836021ef26da85e2f74659778695b2ba1fc1224e0')
tool=dict(initial_chunk_id='04a9cc',session_id=69320,terminal_chunk_id='1bacfa',exit_code=1)
assert term['schema']=='AXMAT_ROOT_ACTUAL_V12_COLD_FAILED_TERMINAL_V1' and term['record_producer']=='root'
assert term['classification']==receipt['classification']==closed['classification']=='FAILED_COMBINED_COLD_NO_RETRY'
assert term['phase']==closed['phase']=='run-AAA' and term['returncode']==closed['actual_exit_code']==1
exact(term['actual_tool_result'],tool);exact(receipt['actual_tool'],tool);exact(closed['actual_tool'],tool)
for k in ('actual_initial_tool_result','actual_terminal_tool_result'):
 exact(term[k],receipt[k]);exact(term[k],closed[k])
assert term['actual_initial_tool_result']['session_id']==69320
assert type(term['actual_terminal_tool_result']['exit_code'])is int and term['actual_terminal_tool_result']['exit_code']==1
assert 'session_id' not in term['actual_terminal_tool_result']
assert term['session_closed'] is True and receipt['session_closed'] is True
assert term['record_written_after_actual_terminal_return'] is True and receipt['record_written_after_actual_terminal_return'] is True
assert receipt['actual_tool_terminal_return_observed'] is True
assert closed['actual_live_session_id'] is None and closed['terminal_return_observed'] is True and closed['actual_closed_session_id']==69320
for d in term.values():
 if isinstance(d,dict) and set(d)=={'path','sha256','bytes'}:descriptor(d)
for d in receipt.values():
 if isinstance(d,dict) and set(d)=={'path','sha256','bytes'}:descriptor(d)
for k in ('failed_terminal','Root_terminal'):descriptor(closed[k])
exact(closed['failed_terminal'],receipt['failed_cold_terminal'])
assert receipt['failed_cold_terminal']['path']==str(T/'cold_failed_terminal_return.json')
assert closed['Root_terminal']['path']==str(R/'Root_actual_cold_AAA_tool_terminal_return.json')
assert term['source']['sha256']==closed['source_sha256']==body['source_factory']['sha256']=='7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71'
exact(term['prepared_cold'],receipt['prepared_cold'])
assert term['prepared_cold']['sha256']==closed['prepared_cold_sha256']==body['prepared_cold']['sha256']=='a0bef1fdec73993e084876db89f5ea41fe8dc10304a3e38d6be17a5b68590368'
assert term['input_declaration_terminal_evidence']['sha256']==closed['declaration_terminal_sha256']=='66c0647d69ba276460a84a09cee6502b272ded07c5b24b5f3509a64ae47d0b2c'
for k in ('full_stdout','full_stderr'):
 assert Path(term[k]['path']).read_bytes()==Path(receipt[k]['path']).read_bytes()
 assert term[k]['sha256']==receipt[k]['sha256'] and term[k]['bytes']==receipt[k]['bytes']
assert term['full_stdout']['bytes']==0 and term['full_stderr']['bytes']==3084
stderr=Path(term['full_stderr']['path']).read_text()
assert stderr.rstrip().endswith('RuntimeError: own-child 512 MiB RSS cap reached')
assert 'cold_launch_in_clean_process' in stderr and 'bootstrap_axial.x2m' in stderr and 'enforce_observed_peak' in stderr
failure=read(term['actual_source_failure']['path']);status=read(term['actual_run_status']['path'])
stages=read(term['actual_stages']['path'])['stages'];watch=read(term['actual_native_watchdog']['path'])
exact(term['stage_summary'],[{k:s[k]for k in ('label','status','elapsed_seconds')}for s in stages])
assert [s['status']for s in stages]==['PASS']*6+['FAILED'] and len(stages)==7
assert term['failed_stage']==stages[-1]['label']=='AAA/bootstrap/bootstrap_axial'
assert term['completed_maps']==receipt['completed_maps']==closed['completed_maps']==status['completed_maps']==0
assert status['classification']=='FAILED_NO_RETRY' and failure['classification']=='FAILED_COMBINED_COLD_NO_RETRY'
assert term['sampled_own_child_peak_rss_mib']==receipt['sampled_own_child_peak_rss_mib']==watch['sampled_peak_rss_mib']==watch['observed_peak_rss_mib']==512.890625
assert term['original_rss_cap_mib']==watch['rss_cap_mib']==512 and term['native_child_returncode']==watch['returncode']==-15
assert watch['pid']==62748 and watch['own_child_only'] is True and watch['live_rss_sample_count']==460
assert term['own_child_group_cleanup_observed']==watch['liveness_group_cleanup'] is True
assert term['own_pid_wait4_observed']==watch['own_pid_wait4_observed'] is False
assert term['own_pid_wait4_peak_rss_mib'] is None and term['kernel_peak_not_observed'] is True
for k in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'):assert watch[k] is None
assert term['full_closeout_tail_gate'] is None and term['cold_closeout_seal_present'] is False
assert not (W/'cold_source_complete_result.json').exists() and not (W/'cold_closeout_seal.json').exists()
assert not any(k in term for k in ('actual_tail_check','actual_archive_bytes','actual_resources'))
for x in (term,receipt,closed):
 assert x['retry_count']==0
 for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert x[k] is False
assert term['scientific_qualification'] is False
assert term['original_budgets_unchanged'] is True and closed['original_512_43200_stage_limits_unchanged'] is True
exact(read(W/'prepared_cold.json')['budgets'],body['original_production_budgets'])
for path,v in body['current_small_evidence_inventory'].items():pin(path,v['sha256'])
report={'status':'PASS_READONLY_CLOSED_ACTUAL_FAILURE_SCOPE_ONLY',
 'actual_business_terminal_state':'FAILED_COMBINED_COLD_NO_RETRY_EXIT1_CLOSED',
 'root_failed_terminal':pin(T/'cold_failed_terminal_return.json'),'Root_actual_AAA_receipt':pin(R/'Root_actual_cold_AAA_tool_terminal_return.json'),
 'Root_closed_job':pin(R/'Root_current_actual_cold_AAA_job.json'),
 'actual_AAA_tool':tool,'integer_exit_one_verified':True,'live_session_is_None':True,
 'failure_body_review':pin(D/'REPORT_FAILURE_BODY.json'),'failure_body_actual_readonly_tool':pin(D/'actual_failure_body_readonly_tool_return.json'),
 'independent_raw_review':pin(P/'REPORT.json'),'independent_raw_actual_readonly_tool':pin(P/'actual_readonly_tool_return.json'),
 'prior_actual_business_tool_exits':{k:v['exit_code']for k,v in body['prior_actual_zero_exits'].items()},
 'six_stages_PASS_one_FAILED':True,'zero_completed_maps':True,'source_and_PREP_current_pins_unchanged':True,
 'full_source_failure_run_status_stages_watch_log_stream_descriptors_current_hashes_verified':True,
 'full_stdout_and_stderr_equal_to_Root_complete_original_streams':True,
 'true_failure_is_own_PID_monitor_SIGTERM_not_solver_native_ABORT':True,
 'original_RSS_cap_MiB':512,'actual_live_sample_peak_MiB':512.890625,'actual_native_child_returncode':-15,
 'actual_watch_seconds':watch['elapsed_seconds'],'actual_stage_seconds':stages[-1]['elapsed_seconds'],
 'all_four_unknown_kernel_wait4_fields_None':True,'no_kernel_peak_synthesized':True,
 'no_success_closeout_tail_or_seal_claimed':True,'no_success_admission_credit':True,
 'original_math_inputs_and_budgets_unchanged':True,'permanent_no_retry_namespace':str(W),
 'precision_assessment_not_started':True,'not_an_INCONCLUSIVE_precision_result':True,
 'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,
 'business_import_call_execution':False,'Root_session_poll':False,'project_write':False,'35GB_union_rehash':False,
 'checked_small_current_file_inventory':inventory}
q=D/'REPORT_FINAL_CLOSED_FAILURE.json';q.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'report':pin(q),'actual_AAA_tool':tool,
 'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False},sort_keys=True))
