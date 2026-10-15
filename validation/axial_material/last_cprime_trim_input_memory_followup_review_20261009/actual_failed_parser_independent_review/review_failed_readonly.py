import ast, hashlib, json, math, os, pathlib, stat, subprocess, time

OUT=pathlib.Path('/private/tmp/spot_v9_isolated_parser_actual_failed_independent_review_20261009')
ACT=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_root_execution_20261009')
PLAN=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_20261009')
CAND=pathlib.Path('/private/tmp/axmat_v9_strict_json_local_immutable_sharing_candidate_20261009/strict_json_bytes_local_immutable_sharing_candidate.py')
OLD=pathlib.Path('/Users/wen/spot/validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py')
DECL=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/declaration.json')
SEVEN=pathlib.Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json')
EXPECTED={OLD:'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4',DECL:'3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae',SEVEN:'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa',CAND:'15383b532973a9dc68fcdaeb7251723ee3379a075472bddadfb6bdbf9b9ec8d3',PLAN/'parser_metadata_worker.py':'9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552',PLAN/'root_owned_parser_watchdog.py':'e5177791ee5c88e36aa5f161f917c8baa4106fc62556bb3e5b6e0d39eb6a9e63',PLAN/'source_plan.json':'e2f9248874a427bd76de88beafe55c7d1210ee06dea3c85c37c4038ce9a66cb7'}

def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,collect=False):
 p=pathlib.Path(p);before=p.lstat();assert stat.S_ISREG(before.st_mode)
 assert p.is_absolute() and p.parent.resolve(strict=True)==p.parent
 with p.open('rb') as f:
  assert identity(os.fstat(f.fileno()))==identity(before)
  h=hashlib.sha256();parts=[]
  while b:=f.read(1024*1024):
   h.update(b)
   if collect:parts.append(b)
  assert identity(os.fstat(f.fileno()))==identity(before)
 assert identity(p.lstat())==identity(before)
 v=dict(path=str(p),size=before.st_size,sha256=h.hexdigest(),identity=identity(before))
 if p in EXPECTED:assert v['sha256']==EXPECTED[p]
 return v,b''.join(parts) if collect else None

def readj(p):return json.loads(pin(p,True)[1])
def save(p,v):
 with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')

OUT.mkdir(exist_ok=True)
initial={str(p):pin(p)[0] for p in EXPECTED}
actual_files=sorted(p for p in ACT.rglob('*') if p.is_file())
actual_before={str(p):pin(p)[0] for p in actual_files}
assert sorted(p.name for p in ACT.iterdir())==['original_DECL','root_actual_failed_tool_return.json']
case=ACT/'original_DECL';report=readj(case/'child_report.json');start=readj(case/'owned_child_start.json');terminal=readj(ACT/'root_actual_failed_tool_return.json')
assert terminal['closed'] is True and terminal['exit_code']==terminal['completion_tool']['exit_code']==1
assert terminal['initial_tool']['chunk_id']=='c8a0a5' and terminal['initial_tool']['session_id']==66201
assert terminal['completion_tool']['chunk_id']=='24b476' and terminal['science_credit'] is False
trace=terminal['completion_tool']['output'];assert "line 125, in run_case" in trace and "NameError: name 'data_before' is not defined" in trace
watch=pin(PLAN/'root_owned_parser_watchdog.py',True)[1].decode();lines=watch.splitlines();assert 'data_before=data_before,data_after=after_data' in lines[124]
tree=ast.parse(watch);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_case')
loads={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
stores={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store)}
assert 'data_before' in loads and 'data_before' not in stores and 'before_data' in stores
assert any('cleanup=clean_owned_group(proc)' in line for line in lines[:124])
assert not (case/'watchdog_receipt.json').exists() and not (ACT/'diagnostic_summary.json').exists()
pid=start['pid'];assert pid==11722==start['process_group']==report['worker_pid']
assert start['rss_cap_mib']==512 and start['wall_cap_seconds']==120 and start['numeric_or_business_stage'] is False
assert start['command'][2:6]==['--source',str(OLD),'--source-sha',EXPECTED[OLD]]
assert report['classification']=='PARSED_METADATA_DIAGNOSTIC_ONLY' and report['business_import_or_API_or_constructor_or_PREP_RUN'] is False and report['native_or_science_credit'] is False
assert report['source_before']==report['source_after']==initial[str(OLD)] and report['data_before']==report['data_after']==initial[str(DECL)]
assert report['mutable_container_independence'] is True and report['bytecode_disabled'] is True and report['optimization_disabled'] is True
assert len(report['thread_environment'])==5 and set(report['thread_environment'].values())=={'1'}
oldtext=pin(OLD,True)[1].decode();oldtree=ast.parse(oldtext);oldfn=next(n for n in oldtree.body if isinstance(n,ast.FunctionDef) and n.name=='strict_json_bytes')
oldfnbytes=''.join(oldtext.splitlines(keepends=True)[oldfn.lineno-1:oldfn.end_lineno]).encode()
assert hashlib.sha256(oldfnbytes).hexdigest()==report['extracted_function_sha256']=='f80c0f683401e258414187dcaa3b72ab233bd597b19cdfe003215bcbd0027d59'
events=[json.loads(x) for x in pin(case/'stdout.jsonl',True)[1].splitlines()]
phases=['stdlib_and_parser_AST_loaded','raw_verified_before_parse','parse_active','parse_return_value_and_raw_retained','parsed_value_retained_raw_released','plain_type_order_and_full_output_digest','parsed_value_retained_after_validation','after_fresh_pins_value_retained','parsed_value_released_with_explicit_gc','child_report_atomically_complete']
assert len(events)==11 and [v['phase'] for v in events[:10]]==phases and [v['sequence'] for v in events[:10]]==list(range(1,11))
assert all(v['worker_pid']==pid and v['scope']=='PARSER_METADATA_DIAGNOSTIC_ONLY' for v in events[:10])
assert all(a['monotonic']<=b['monotonic'] for a,b in zip(events[:9],events[1:10]))
assert readj(case/'latest_phase.json')==events[9] and events[10]['report']==str(case/'child_report.json')
assert pin(case/'stderr.txt')[0]['size']==0
samples=[json.loads(x) for x in pin(case/'own_pid_ps_samples.jsonl',True)[1].splitlines()]
assert len(samples)==59;agg={};last=0
for s in samples:
 assert s['pid']==pid and type(s['rss_kib']) is int and s['rss_kib']>=0 and s['rss_mib']==s['rss_kib']/1024
 assert s['raw_ps'].split()==[str(pid),str(s['rss_kib'])] and s['elapsed_seconds']>=last and s['elapsed_seconds']<120
 last=s['elapsed_seconds'];assert s['stable_phase']==(s['phase_before']==s['phase_after'])
 assert s['phase']==(s['phase_after']['phase'] if s['stable_phase'] else 'phase_transition_ambiguous')
 assert s['phase_sequence']==s['phase_after']['sequence']
 a=agg.setdefault(s['phase'],dict(samples=0,min_mib=s['rss_mib'],max_mib=s['rss_mib'],last_mib=s['rss_mib']))
 a.update(samples=a['samples']+1,min_mib=min(a['min_mib'],s['rss_mib']),max_mib=max(a['max_mib'],s['rss_mib']),last_mib=s['rss_mib'])
coverage={x:agg.get(x,{}).get('samples',0)>0 for x in (phases[3],phases[4],phases[6],phases[7],phases[8])}
assert all(coverage.values()) and max(s['rss_mib'] for s in samples)==55.46875
for key in ('rusage_before_parse','rusage_immediately_after_parse','rusage_maxrss'):
 r=report[key];assert r['platform']=='darwin' and r['unit']=='bytes' and r['MiB']==r['raw']/1024**2 and r['supplement_only_not_own_PID_ps_gate'] is True
# Ordinary STDlib full-metadata parse for independent value/type/digest validation.
# No extraction execution, worker/watch invocation or measurement child.
value=json.loads(pin(DECL,True)[1]);counts={};shape=hashlib.sha256();seen=set()
def walk(item):
 kind=type(item);assert kind in (dict,list,str,int,float,bool,type(None))
 label=kind.__name__;counts[label]=counts.get(label,0)+1;shape.update(label.encode()+b':')
 if kind in (dict,list):
  assert id(item) not in seen;seen.add(id(item));shape.update(str(len(item)).encode()+b'[')
  if kind is dict:
   for key,part in item.items():
    assert type(key) is str;shape.update(json.dumps(key,ensure_ascii=True,separators=(',',':')).encode());walk(part)
  else:
   for part in item:walk(part)
  shape.update(b']')
 elif kind is float:assert math.isfinite(item)
walk(value);seen.clear();h=hashlib.sha256();length=0
for piece in json.JSONEncoder(sort_keys=False,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(value):
 b=piece.encode();h.update(b);length+=len(b)
assert counts==report['plain_builtin_type_counts'] and shape.hexdigest()==report['type_and_insertion_order_shape_sha256']
assert h.hexdigest()==report['whole_insertion_order_JSON_output_sha256'] and length==report['whole_insertion_order_JSON_output_bytes']==7933604
del value
ps_command=['/bin/ps','-o','pid=','-o','rss=','-p',str(pid)]
try:
 ps=subprocess.run(ps_command,capture_output=True,text=True)
 current_pid_observation=dict(command=ps_command,returncode=ps.returncode,stdout=ps.stdout,stderr=ps.stderr,PID_absent_observed=ps.returncode==1 and not ps.stdout.strip())
except PermissionError as error:
 current_pid_observation=dict(command=ps_command,returncode=None,stdout=None,stderr=None,PID_absent_observed=None,sandbox_denial=repr(error),no_alternate_sandbox_or_bypass_used=True)
fresh={str(p):pin(p)[0] for p in EXPECTED};assert fresh==initial
actual_after={str(p):pin(p)[0] for p in actual_files};assert actual_before==actual_after
result=dict(status='PASS_READONLY_AUDIT_OF_ACTUAL_DIAGNOSTIC_DRIVER_FAILURE',diagnostic_qualification=False,four_case_qualification=False,actual_root_terminal=dict(initial_chunk='c8a0a5',session_id=66201,completion_chunk='24b476',exit_code=1,closed=True,pin=actual_before[str(ACT/'root_actual_failed_tool_return.json')]),failure_attribution=dict(kind='watchdog receipt construction NameError',line=125,undefined_load='data_before',defined_required_name='before_data',data_after_current_expression='after_data already correct',not_parser_or_science_failure=True,prior_source_execution_PASS_missed_this_defect=True),original_case=dict(label='original_DECL',pid=pid,child_returncode=None,own_group_cleanup_receipt=None,cleanup_source_call_preceded_trace=True,current_PID_readonly_observation=current_pid_observation,raw_phases=phases,own_PID_ps_sample_count=len(samples),own_PID_ps_sampled_peak_mib=max(s['rss_mib'] for s in samples),phase_aggregates=agg,retained_stable_phase_coverage=coverage,parse_seconds_reported=report['parse_seconds'],reported_rusage={k:report[k] for k in ('rusage_before_parse','rusage_immediately_after_parse','rusage_maxrss')},plain_builtin_type_counts=counts,full_output_bytes=length,full_output_sha256=h.hexdigest(),full_type_insertion_shape_sha256=shape.hexdigest(),mutable_container_independence=True,whole_metadata_recomputed_with_plain_stdlib_JSON=True),unrun_cases=['candidate_DECL','original_FULL_SEVEN_INPUT','candidate_FULL_SEVEN_INPUT'],absent_files=['original_DECL/watchdog_receipt.json','diagnostic_summary.json'],source_and_both_full_data_pins=fresh,actual_evidence_pins=actual_after,scope=dict(isolated_metadata_evidence_only=True,business_or_constructor_or_API_PREP_RUN_or_native_executed=False,watch_or_worker_invoked_by_reviewer=False,candidate_executed_by_reviewer=False,project_formal_ART_modified=False,combined_native_AAA_ABA_or_science_credit=False,actual_V8_allocating_line_localized=False),limitations=['Completed original parser payload/phase/output evidence does not establish its actual child wait returncode.','Source shows finally cleanup returned before receipt exception; no cleanup receipt was persisted and no numerical cleanup result is fabricated.','Reviewer sandbox denied /bin/ps; current PID absence is unknown to reviewer and no alternate sandbox was used.','Stable phase RSS labels and getrusage high-water include diagnostic work and pauses, not allocation sizes or original combined footprint.','Four-case comparison and candidate memory benefit remain unmeasured here; local immutable pools can increase peak with distinct values.'],future_v2_source_review_sha256=None,future_three_case_actual_terminal=None)
save(OUT/'REPORT.json',result)
print(json.dumps(dict(status=result['status'],report=str(OUT/'REPORT.json'),sha256=pin(OUT/'REPORT.json')[0]['sha256'],sample_count=59,peak_mib=55.46875,root_exit=1,child_returncode=None,no_science_credit=True)))
