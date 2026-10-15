import ast,hashlib,json,math,os,pathlib,stat
O=pathlib.Path('/private/tmp/spot_v9_remaining_three_parser_actual_independent_review_20261009')
A=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_remaining_v2_root_execution_20261009')
P=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_v2_20261009')
PRIOR=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_root_execution_20261009')
FORMAL=pathlib.Path('/Users/wen/spot/validation/axial_material/last_cprime_trim_input_memory_followup_review_20261009/actual_remaining_three_parser_diagnostic_v2')
def pin(p,collect=False):
 p=pathlib.Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and p.parent.resolve(strict=True)==p.parent
 h=hashlib.sha256();parts=[]
 with p.open('rb') as f:
  while b:=f.read(1024**2):
   h.update(b)
   if collect:parts.append(b)
 assert s==p.lstat()
 return dict(path=str(p),identity=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink],size=s.st_size,sha256=h.hexdigest()),b''.join(parts) if collect else None
def j(p):return json.loads(pin(p,True)[1])
O.mkdir(exist_ok=True)
initial={str(p):pin(p)[0] for p in A.rglob('*') if p.is_file()}
summarypin,raw=pin(A/'diagnostic_summary.json',True);summary=json.loads(raw);assert summarypin['sha256']=='01d050946534a3649d522e487ee3277277f26f5c5989c0a3c6f23b490b07d053'
terminalpin,_=pin(A/'root_actual_tool_return.json');terminal=j(A/'root_actual_tool_return.json')
assert terminal['closed'] is True and terminal['exit_code']==terminal['completion_tool']['exit_code']==0
assert terminal['initial_tool']['chunk_id']=='eb41ca' and terminal['initial_tool']['session_id']==3948 and terminal['completion_tool']['chunk_id']=='0e3832'
assert terminal['old_parent_actual_exit_code']==1 and terminal['old_original_child_exact_wait_returncode'] is None and terminal['overall_four_case_watchdog_qualification'] is False and terminal['science_credit'] is False
pointer=json.loads(terminal['completion_tool']['output']);assert pointer['sha256']==summarypin['sha256'] and pointer['report']==str(A/'diagnostic_summary.json') and pointer['completed_cases']==3 and pointer['overall_four_case_watchdog_qualification'] is False and pointer['no_science'] is True
assert summary['status']=='PASS_REMAINING_THREE_ISOLATED_PARSER_METADATA_DIAGNOSTICS_ONLY' and summary['completed_cases']==summary['expected_cases']==3 and summary['remaining_three_case_diagnostic_success'] is True
assert summary['prior_original_DECL_child_wait_returncode'] is None and summary['prior_parent_actual_exit_code']==1 and summary['overall_four_case_watchdog_qualification'] is False and summary['original_DECL_rerun'] is False
assert summary['one_worker_at_once'] is True and summary['retries']==0 and summary['Root_tool_terminal_observation'] is None and summary['actual_V8_allocating_line_localized'] is False
assert summary['no_business_factory_import_or_API_constructor_PREP_RUN'] is True and summary['no_combined_runtime_native_AAA_ABA_or_science_credit'] is True
expected=['candidate_DECL','original_FULL_SEVEN_INPUT','candidate_FULL_SEVEN_INPUT'];assert summary['planned_cases']==expected
assert sorted(p.name for p in A.iterdir() if p.is_dir())==sorted(expected) and not (A/'original_DECL').exists()
baseline=summary['prior_original_DECL_baseline'];assert baseline['prior_parent_actual_exit_code']==1 and baseline['original_child_wait_returncode'] is None and baseline['original_child_success_qualification'] is False and baseline['overall_four_case_watchdog_qualification'] is False and baseline['original_parent_watchdog_receipt_present'] is False
for rel,wanted in baseline['prior_file_pins'].items():assert pin(PRIOR/rel)[0]==wanted
oldterm=j(PRIOR/'root_actual_failed_tool_return.json');assert oldterm['exit_code']==1 and oldterm['closed'] is True
assert not (PRIOR/'original_DECL/watchdog_receipt.json').exists() and not (PRIOR/'diagnostic_summary.json').exists()
for k in ('worker_source_pin','watchdog_source_pin','ps_executable_pin'):assert pin(summary[k]['path'])[0]==summary[k]
assert summary['worker_source_pin']['sha256']=='9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552'
assert summary['watchdog_source_pin']['sha256']=='5983010d03389ac3a6170d349c09761c88381d1bce3894fd9545faeff98c5271'
phasenames=['stdlib_and_parser_AST_loaded','raw_verified_before_parse','parse_active','parse_return_value_and_raw_retained','parsed_value_retained_raw_released','plain_type_order_and_full_output_digest','parsed_value_retained_after_validation','after_fresh_pins_value_retained','parsed_value_released_with_explicit_gc','child_report_atomically_complete']
retained=phasenames[3:5]+phasenames[6:9];cases=[];children={('DECL','original'):j(PRIOR/'original_DECL/child_report.json')};stable={('DECL','original'):baseline['stable_phase_RSS_samples']};all_source_data={};previous_end=None
def aggregate(samples):
 agg={};last=-1
 for s in samples:
  assert type(s['pid']) is int and type(s['rss_kib']) is int and s['rss_kib']>=0 and s['rss_mib']==s['rss_kib']/1024
  assert s['raw_ps'].split()==[str(s['pid']),str(s['rss_kib'])] and last<=s['elapsed_seconds']<120;last=s['elapsed_seconds']
  assert s['stable_phase']==(s['phase_before']==s['phase_after']) and s['phase_sequence']==s['phase_after']['sequence']
  assert s['phase']==(s['phase_after']['phase'] if s['stable_phase'] else 'phase_transition_ambiguous')
  a=agg.setdefault(s['phase'],dict(samples=0,min_mib=s['rss_mib'],max_mib=s['rss_mib'],last_mib=s['rss_mib']))
  a.update(samples=a['samples']+1,min_mib=min(a['min_mib'],s['rss_mib']),max_mib=max(a['max_mib'],s['rss_mib']),last_mib=s['rss_mib'])
 return agg
oldsamples=[json.loads(x) for x in pin(PRIOR/'original_DECL/own_pid_ps_samples.jsonl',True)[1].splitlines()];oldagg=aggregate(oldsamples)
assert len(oldsamples)==59 and sum(x['stable_phase'] for x in oldsamples)==57
assert {k:v for k,v in oldagg.items() if k!='phase_transition_ambiguous'}==baseline['stable_phase_RSS_samples']
for label,receipt in zip(expected,summary['receipts']):
 d=A/label;assert j(d/'watchdog_receipt.json')==receipt;child=j(d/'child_report.json');start=j(d/'owned_child_start.json');events=[json.loads(x) for x in pin(d/'stdout.jsonl',True)[1].splitlines()]
 pid=receipt['child_pid'];assert type(pid) is int and pid==child['worker_pid']==start['pid']==start['process_group'] and pid!=11722
 assert receipt['child_returncode']==0 and receipt['status']=='PASS_ISOLATED_PARSER_DIAGNOSTIC_ONLY' and receipt['limit_or_observation_failure'] is None
 assert receipt['rss_cap_mib']==512 and receipt['wall_cap_seconds']==120 and 0<receipt['elapsed_seconds']<120
 assert receipt['ROOT_business_RUNNING_stage_faked'] is False and receipt['business_or_native_or_combined_RSS_or_science_credit'] is False
 clean=receipt['own_group_cleanup'];assert clean['owned_pid']==clean['owned_session_and_group']==pid and clean['wait_returncode']==0 and clean['direct_child_reaped'] is True and clean['signals']==clean['exit_races']==[]
 assert start['command']==receipt['command'] and start['numeric_or_business_stage'] is False
 assert len(events)==11 and [x['phase'] for x in events[:10]]==phasenames and [x['sequence'] for x in events[:10]]==list(range(1,11))
 assert all(x['worker_pid']==pid and x['scope']=='PARSER_METADATA_DIAGNOSTIC_ONLY' for x in events[:10]) and j(d/'latest_phase.json')==events[9]
 assert events[10]['report']==str(d/'child_report.json') and events[10]['classification']=='PARSER_METADATA_DIAGNOSTIC_ONLY'
 assert all(a['monotonic']<=b['monotonic'] for a,b in zip(events[:9],events[1:10]))
 if previous_end is not None:assert start['monotonic']>previous_end
 previous_end=events[9]['monotonic']
 assert pin(d/'stderr.txt')[0]['size']==0
 samples=[json.loads(x) for x in pin(d/'own_pid_ps_samples.jsonl',True)[1].splitlines()];assert samples and all(x['pid']==pid for x in samples)
 agg=aggregate(samples);peak=max(x['rss_mib'] for x in samples)
 assert agg==receipt['phase_RSS_samples'] and peak==receipt['own_PID_ps_sampled_peak_mib']<512 and len(samples)==receipt['own_PID_ps_sample_count']
 assert receipt['stable_retained_phase_coverage']=={x:agg.get(x,{}).get('samples',0)>0 for x in retained} and all(receipt['stable_retained_phase_coverage'].values())
 for key in ('stdout_pin','stderr_pin','samples_pin','child_report_pin','worker_source_pin'):assert pin(receipt[key]['path'])[0]==receipt[key]
 for kind in ('source','data'):
  before=receipt[kind+'_before'];assert before==receipt[kind+'_after']==child[kind+'_before']==child[kind+'_after']==pin(before['path'])[0];all_source_data[before['path']]=before
 text=pin(child['source_before']['path'],True)[1].decode();tree=ast.parse(text);fn=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strict_json_bytes'];assert len(fn)==1
 fnbytes=''.join(text.splitlines(keepends=True)[fn[0].lineno-1:fn[0].end_lineno]).encode();assert hashlib.sha256(fnbytes).hexdigest()==child['extracted_function_sha256']
 assert child['classification']=='PARSED_METADATA_DIAGNOSTIC_ONLY' and child['business_import_or_API_or_constructor_or_PREP_RUN'] is False and child['native_or_science_credit'] is False
 assert child['bytecode_disabled'] is True and child['optimization_disabled'] is True and child['mutable_container_independence'] is True
 assert len(child['thread_environment'])==5 and set(child['thread_environment'].values())=={'1'} and child['python_executable']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
 for k in ('rusage_before_parse','rusage_immediately_after_parse','rusage_maxrss'):
  x=child[k];assert x['platform']=='darwin' and x['unit']=='bytes' and x['MiB']==x['raw']/1024**2<512 and x['supplement_only_not_own_PID_ps_gate'] is True
 assert receipt['rusage_maxrss']==child['rusage_maxrss']
 source,data=('candidate','DECL') if label=='candidate_DECL' else ('original','FULL_SEVEN_INPUT') if label=='original_FULL_SEVEN_INPUT' else ('candidate','FULL_SEVEN_INPUT')
 children[(data,source)]=child;stable[(data,source)]={k:v for k,v in agg.items() if k!='phase_transition_ambiguous'}
 cases.append(dict(label=label,pid=pid,actual_wait_returncode=0,cleanup=clean,own_PID_ps_sample_count=len(samples),sampled_peak_mib=peak,reported_rusage={k:child[k] for k in ('rusage_before_parse','rusage_immediately_after_parse','rusage_maxrss')},phases=agg,elapsed_seconds=receipt['elapsed_seconds'],source_size=child['source_before']['size'],source_whole_SHA=child['source_before']['sha256'],data_size=child['data_before']['size'],data_whole_SHA=child['data_before']['sha256'],parse_seconds_reported=child['parse_seconds']))
assert len({x['pid'] for x in cases})==3
# Independent ordinary-STDlib full metadata verification. No target strict_json
# function, factory/module, parser worker/watch or new memory measurement runs.
recomputed={}
for label in ('DECL','FULL_SEVEN_INPUT'):
 child=children[(label,'candidate')];value=json.loads(pin(child['data_before']['path'],True)[1]);counts={};shape=hashlib.sha256();mutable=set()
 def walk(x):
  kind=type(x);assert kind in (dict,list,str,int,float,bool,type(None));name=kind.__name__;counts[name]=counts.get(name,0)+1;shape.update(name.encode()+b':')
  if kind in (dict,list):
   assert id(x) not in mutable;mutable.add(id(x));shape.update(str(len(x)).encode()+b'[')
   if kind is dict:
    for key,y in x.items():assert type(key) is str;shape.update(json.dumps(key,ensure_ascii=True,separators=(',',':')).encode());walk(y)
   else:
    for y in x:walk(y)
   shape.update(b']')
  elif kind is float:assert math.isfinite(x)
 walk(value);mutable.clear();h=hashlib.sha256();length=0
 for piece in json.JSONEncoder(sort_keys=False,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(value):
  b=piece.encode();h.update(b);length+=len(b)
 for source in ('original','candidate'):
  c=children[(label,source)];assert c['plain_builtin_type_counts']==counts and c['type_and_insertion_order_shape_sha256']==shape.hexdigest() and c['whole_insertion_order_JSON_output_sha256']==h.hexdigest() and c['whole_insertion_order_JSON_output_bytes']==length and c['mutable_container_independence'] is True
 recomputed[label]=dict(plain_builtin_type_counts=counts,type_and_insertion_order_shape_sha256=shape.hexdigest(),whole_insertion_order_JSON_output_sha256=h.hexdigest(),whole_insertion_order_JSON_output_bytes=length,mutable_container_independence=True);del value
for label,fields in summary['whole_builtin_insertion_order_JSON_output_comparisons'].items():assert all(fields.values())
comparisons={}
for label,phases in summary['actual_stable_phase_RSS_comparisons'].items():
 comparisons[label]={}
 for name,x in phases.items():
  old=stable[(label,'original')][name];new=stable[(label,'candidate')][name]
  assert old==x['original_actual_stable_phase_samples'] and new==x['candidate_actual_stable_phase_samples'] and new['max_mib']-old['max_mib']==x['candidate_minus_original_max_mib']
  comparisons[label][name]=x['candidate_minus_original_max_mib']
loader='stdlib_and_parser_AST_loaded';old_loader=stable[('FULL_SEVEN_INPUT','original')][loader]['max_mib'];new_loader=stable[('FULL_SEVEN_INPUT','candidate')][loader]['max_mib']
assert old_loader==28.046875 and new_loader==16.765625 and old_loader-new_loader==11.28125
assert children[('FULL_SEVEN_INPUT','original')]['source_before']['size']==102551 and children[('FULL_SEVEN_INPUT','candidate')]['source_before']['size']==1174
copy_pins={}
for path,p in initial.items():
 original=pathlib.Path(path);f=FORMAL/original.relative_to(A);q=pin(f)[0];assert q['size']==p['size'] and q['sha256']==p['sha256'];copy_pins[str(f)]=q
final={str(p):pin(p)[0] for p in A.rglob('*') if p.is_file()};assert initial==final
for path,p in all_source_data.items():assert pin(path)[0]==p
for rel,p in baseline['prior_file_pins'].items():assert pin(PRIOR/rel)[0]==p
result=dict(status='PASS_INDEPENDENT_ACTUAL_REMAINING_THREE_ISOLATED_DIAGNOSTIC_REVIEW',root_actual_exit_code=0,root_terminal_pin=terminalpin,summary_sha256=summarypin['sha256'],actual_tool=dict(initial_chunk='eb41ca',session_id=3948,completion_chunk='0e3832',exit_code=0,closed=True),remaining_three_actual_success=True,overall_four_case_watchdog_qualification=False,prior_original_parent_actual_exit_code=1,prior_original_child_exact_wait_returncode=None,original_DECL_rerun=False,cases=cases,whole_metadata_independent_plain_STDlib_recomputations=recomputed,actual_stable_phase_candidate_minus_original_max_mib=comparisons,loader_confound=dict(original_fullfactory_source_bytes=102551,candidate_single_function_source_bytes=1174,original_full_SEVEN_phase1_max_mib=old_loader,candidate_full_SEVEN_phase1_max_mib=new_loader,loader_phase_difference_mib=old_loader-new_loader,original_input_rows_retained_phase_differences_range_mib=[-3.265625,-0.578125],claim='Inputs to AST source extraction have unequal full source sizes; source loading/whole AST construction and allocator history differ before JSON parsing. Observed smaller candidate RSS cannot be causally credited to immutable sharing.',candidate_pool_may_increase_peak=True,source_loader_AST_tree_still_retained_not_proved=True,GC_phase_difference_FULL_SEVEN_candidate_minus_original_mib=1.6875,do_not_subtract_loader_delta_as_causal_adjustment=True),parser_candidate_adopted_for_V9=False,V9_original_parser_retained=True,actual_TMP_evidence_pins=final,formal_exact_copy_pins=copy_pins,source_and_both_whole_data_fresh_pins=all_source_data,prior_frozen_evidence_pins=baseline['prior_file_pins'],scope=dict(no_worker_or_watch_invoked_by_reviewer=True,no_target_parser_or_business_factory_module_loaded=True,no_API_constructor_PREP_RUN_native_or_solver_by_reviewer=True,no_project_ART_formal_write=True,no_combined_RSS_native_AAA_ABA_or_science_credit=True,no_actual_V8_allocation_line_localized=True),limitations=['Only the three previously unrun isolated metadata cases have real successful parent/child receipts. Earlier original_DECL parent remains failed with missing exact child waitcode.','Source loading differs (102551 vs1174 bytes), leaving an approximately11.28MiB loader-phase RSS difference; no parser improvement attribution is valid.','Stable phases are approximate sampled whole-process RSS with diagnostic pauses/type/hash/fresh-file work. ru_maxrss is supplemental historical high-water, not object-size or original combined caller footprint.','Original DECL baseline report/59samples/57stable rows preserved. No repeat case or fabricated old success.','Outputs/type/order/hash equality cover full DECL and whole seven-input payload; mutable sharing is prohibited. Candidate pools per-call only, with separate processes for all actual new cases.'])
with (O/'REPORT.json').open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps(dict(status=result['status'],report=str(O/'REPORT.json'),sha256=pin(O/'REPORT.json')[0]['sha256'],root_exit=0,three_child_waitcodes=[0,0,0],old_four_case_qualification=False,parser_adopted=False,no_science=True)))
