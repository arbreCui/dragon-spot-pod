import ast,builtins,hashlib,json,os,pathlib,stat,symtable,types
OUT=pathlib.Path('/private/tmp/spot_v9_remaining_three_watch_v2_source_independent_review_20261009')
P=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_v2_20261009')
M=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_20261009')
ACT=pathlib.Path('/private/tmp/axmat_v9_isolated_parser_metadata_root_execution_20261009')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p):
 p=pathlib.Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and p.parent.resolve(strict=True)==p.parent
 b=p.read_bytes();assert ident(s)==ident(p.lstat())
 return dict(path=str(p),identity=ident(s),size=len(b),sha256=hashlib.sha256(b).hexdigest()),b
def j(p):return json.loads(pin(p)[1])
def defs(text):
 tree=ast.parse(text);lines=text.splitlines(keepends=True)
 return tree,{n.name:(n,''.join(lines[n.lineno-1:n.end_lineno])) for n in tree.body if isinstance(n,ast.FunctionDef)}
OUT.mkdir(exist_ok=True)
source_initial={str(f):pin(f)[0] for f in P.iterdir() if f.is_file()}
mother_pin,mb=pin(M/'root_owned_parser_watchdog.py');watch_pin,cb=pin(P/'root_owned_parser_watchdog.py');worker_pin,wb=pin(P/'parser_metadata_worker.py')
assert mother_pin['sha256']=='e5177791ee5c88e36aa5f161f917c8baa4106fc62556bb3e5b6e0d39eb6a9e63'
assert watch_pin['sha256']=='5983010d03389ac3a6170d349c09761c88381d1bce3894fd9545faeff98c5271'
assert worker_pin['sha256']=='9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552' and wb==pin(M/'parser_metadata_worker.py')[1]
mt=mb.decode();ct=cb.decode();mother_tree,md=defs(mt);tree,cd=defs(ct);compile(tree,str(P/'root_owned_parser_watchdog.py'),'exec');compile(ast.parse(wb),str(P/'parser_metadata_worker.py'),'exec')
unchanged=['identity','pin','atomic','clean_owned_group','read_phase','own_rss']
assert all(md[n][1]==cd[n][1] for n in unchanged)
assert md['run_case'][1].replace('data_before=data_before,data_after=after_data','data_before=before_data,data_after=after_data')==cd['run_case'][1]
assert md['run_case'][1].count('data_before=data_before,data_after=after_data')==1
inverse=j(P/'complete_source_positional_inverse.json');operations=inverse['operations']
assert inverse['mother_sha256']==mother_pin['sha256'] and inverse['candidate_sha256']==watch_pin['sha256']
restored=ct
for o in reversed(operations):
 assert ct[o['candidate_start']:o['candidate_end']]==o['candidate_text']
 assert mt[o['mother_start']:o['mother_end']]==o['mother_text']
 restored=restored[:o['candidate_start']]+o['mother_text']+restored[o['candidate_end']:]
assert restored==mt
forward=mt
for o in reversed(operations):forward=forward[:o['mother_start']]+o['candidate_text']+forward[o['mother_end']:]
assert forward==ct
# Independent complete symbolic name binding review; target code is not loaded/executed.
symbols=symtable.symtable(ct,str(P/'root_owned_parser_watchdog.py'),'exec')
module_names=set(symbols.get_identifiers())|{'__file__'};builtin_names=set(dir(builtins));unbound=[]
def visit(table):
 for s in table.get_symbols():
  if s.is_referenced() and s.is_global() and s.get_name() not in module_names|builtin_names:unbound.append((table.get_name(),s.get_name()))
 for child in table.get_children():visit(child)
visit(symbols);assert not unbound,unbound
assert set(md)==set(cd)-{'load_prior_original_decl','compare_output_and_stable_phase_RSS'}
assignments={t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
cases=ast.literal_eval(assignments['REMAINING_CASES']);assert cases==(('candidate','DECL'),('original','FULL_SEVEN_INPUT'),('candidate','FULL_SEVEN_INPUT'))
assert ('original','DECL') not in cases and len(set(cases))==3
for k in ('CAP_SECONDS','CAP_MIB','SAMPLE_SECONDS','THREAD_KEYS','DATA','ORIGINAL','ORIGINAL_SHA','CANDIDATE','CANDIDATE_SHA','PYTHON','PS','ROOT'):
 old={t.id:n.value for n in mother_tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
 assert ast.dump(assignments[k],include_attributes=False)==ast.dump(old[k],include_attributes=False)
plan=j(P/'source_plan.json');assert plan['planned_cases']==[a+'_'+b for a,b in cases]
assert plan['original_DECL_rerun'] is False and plan['overall_four_case_watchdog_qualification'] is False
assert plan['caps']==dict(PYTHONOPTIMIZE_absent=True,PYTHONPATH_absent=True,bytecode_disabled=True,numeric_workers_at_once=1,own_PID_ps_RSS_MiB=512,per_child_seconds=120,retries=0,threads=1)
assert plan['actual_watch_started'] is False and plan['no_API_ctor_PREP_RUN_or_business_factory_import'] is True and plan['no_combined_RSS_native_AAA_ABA_science_credit'] is True
future_keys=[k for k in plan if k.startswith('actual_') and k!='actual_watch_started']+[k for k in plan if k.startswith('future_') and k not in ('future_Root_command','future_output_directory_proposal')]
assert all(plan[k] is None for k in future_keys)
assert not pathlib.Path(plan['future_output_directory_proposal']).exists()
all_claimed=[plan[k] for k in ('frozen_original_source','known_candidate_source','watchdog_source','worker_source','mother_watchdog_source','mother_worker_source')]+plan['data_pins']+plan['known_prior_parent_failed_baseline']['prior_file_pins']+j(P/'source_and_prior_evidence_pins.json')
fresh_claimed={}
for p in all_claimed:
 actual=pin(p['path'])[0];assert actual==p,(actual,p);fresh_claimed[p['path']]=actual
prior=j(ACT/'root_actual_failed_tool_return.json');assert prior['closed'] is True and prior['exit_code']==prior['completion_tool']['exit_code']==1 and prior['science_credit'] is False
priorbaseline=plan['known_prior_parent_failed_baseline'];assert priorbaseline['original_child_wait_returncode'] is None and priorbaseline['overall_four_case_watchdog_qualification'] is False and priorbaseline['original_parent_watchdog_receipt_present'] is False
assert not (ACT/'diagnostic_summary.json').exists() and not (ACT/'original_DECL/watchdog_receipt.json').exists()
prior_shas=ast.literal_eval(assignments['PRIOR_SHAS']);assert len(prior_shas)==7
for rel,sha in prior_shas.items():assert pin(ACT/rel)[0]['sha256']==sha
samples=[json.loads(x) for x in pin(ACT/'original_DECL/own_pid_ps_samples.jsonl')[1].splitlines()]
assert len(samples)==59 and sum(s['stable_phase'] for s in samples)==57 and max(s['rss_mib'] for s in samples)==55.46875
prior_fn=cd['load_prior_original_decl'][1];main=cd['main'][1]
for marker in ("failed['exit_code']==1","original_child_wait_returncode=None","original_child_success_qualification=False","overall_four_case_watchdog_qualification=False","before==after"):
 assert marker in prior_fn
for marker in ("assert (source_label,data_label)!=('original','DECL')","for source_label,data_label in REMAINING_CASES:","original_DECL_rerun=False","overall_four_case_watchdog_qualification=False","prior_original_DECL_child_wait_returncode=None","prior_parent_actual_exit_code=1","Root_tool_terminal_observation=None","out.mkdir(exist_ok=False)","assert out!=PRIOR_OUT and not out.is_relative_to(PRIOR_OUT)","if receipt['status']!='PASS_ISOLATED_PARSER_DIAGNOSTIC_ONLY':failure=True;break"):
 assert marker in main
# Pure synthetic evaluation of just the receipt dict AST expression, never a
# watchdog/worker function, parser, process launcher or target module.
def receipt_value(defnode):return next(n.value for n in ast.walk(defnode) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='value' for t in n.targets) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='dict')
oe=receipt_value(md['run_case'][0]);ne=receipt_value(cd['run_case'][0])
names={n.id for n in ast.walk(ne) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
fake={n:None for n in names};fake.update(dict=dict,pin=lambda p:{'synthetic_path':str(p)},passed=True,proc=types.SimpleNamespace(pid=999,returncode=0),child={'rusage_maxrss':{'MiB':1}},case=pathlib.Path('/private/tmp/never-created-synthetic-fixture'),before_data={'marker':'before_data'},after_data={'marker':'after_data'},before_source={'marker':'before_source'},after_source={'marker':'after_source'})
try:eval(compile(ast.Expression(oe),'<synthetic old receipt AST>','eval'),{'__builtins__':{}},fake)
except NameError as e:assert "data_before" in str(e)
else:raise AssertionError('original typo not reproduced by isolated dict AST')
new=eval(compile(ast.Expression(ne),'<synthetic fixed receipt AST>','eval'),{'__builtins__':{}},fake)
expected=eval(compile(ast.Expression(oe),'<synthetic intended original receipt AST>','eval'),{'__builtins__':{}},{**fake,'data_before':fake['before_data']})
assert new==expected and new['data_before'] is fake['before_data'] and new['data_after'] is fake['after_data']
assert new['ROOT_business_RUNNING_stage_faked'] is False and new['business_or_native_or_combined_RSS_or_science_credit'] is False
assert new['child_returncode']==0 # synthetic fixture value only, never a prior real child claim
author=j(P/'source_self_audit.json');assert author['watch_or_worker_executed'] is False and author['business_module_or_input_parser_executed'] is False and len(author['synthetic_fixture_passes'])==8
assert author['actual_remaining_child_PID'] is None and author['actual_remaining_child_returncode'] is None and author['overall_four_case_watchdog_qualification'] is False
final={str(f):pin(f)[0] for f in P.iterdir() if f.is_file() and str(f) in source_initial};assert final==source_initial
for p,v in fresh_claimed.items():assert pin(p)[0]==v
report=dict(status='PASS_SOURCE_CONTRACT_REMAINING_THREE_ISOLATED_METADATA_ONLY',watch_sha256=watch_pin['sha256'],worker_sha256=worker_pin['sha256'],candidate_sha256=plan['known_candidate_source']['sha256'],mother_sha256=mother_pin['sha256'],source_plan_sha256=pin(P/'source_plan.json')[0]['sha256'],whole_source_inverse_exact=True,inverse_operations=len(operations),unchanged_function_bodies=unchanged,run_case_diff='Exactly one RHS name data_before -> before_data; serialized receipt field names and after_data remain unchanged',all_symbolic_global_names_bound=True,unbound_symbolic_names=unbound,remaining_cases=[a+'_'+b for a,b in cases],original_DECL_rerun=False,prior_parent_real_exit_code=1,prior_child_exact_wait_returncode=None,overall_four_case_watchdog_qualification=False,source_and_data_and_prior_complete_fresh_pins=fresh_claimed,source_plan_file_pins=final,caps=plan['caps'],future_fields_null=future_keys,proposed_output_absent=True,synthetic_AST_only_fixture_checks=['original receipt NameError independently reproduced','fixed receipt reads correct before/after dicts','serialized field names and whole intended dict identical','negative old read not silently supplied','remaining 3 literal excludes original_DECL','no unbound global name across all functions','source unchanged monitoring/caps/cleanup/serial/0retry','prior root failure and child None preserved'],author_eight_synthetic_fixture_report_pin=pin(P/'source_self_audit.json')[0],scope=dict(no_worker_or_watch_function_or_main_invoked=True,no_parser_executed=True,no_F8_business_module_loaded=True,no_constructor_API_PREP_RUN_or_native=True,no_project_or_formal_ART_modified=True,no_combined_native_AAA_ABA_science_credit=True,no_actual_V8_allocation_line_localized=True,remaining_actual_terminal=None,remaining_actual_pids=None,remaining_actual_receipts=None),limits=['PASS approves source contract for exactly three previously unrun isolated cases; not business success or old four-case qualification.','Prior original_DECL report/phase RSS may provide output/stable phase baseline only; its missing real child waitcode remains None.','RSS instrumentation phase labels are approximate; no original combined footprint or allocating-line claim.','Source-only checks and synthetic AST values are not parser measurement results; pooling may increase peak with distinct values.'])
with (OUT/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps(dict(status=report['status'],report=str(OUT/'REPORT.json'),sha256=pin(OUT/'REPORT.json')[0]['sha256'],watch_sha256=watch_pin['sha256'],no_execution=True)))
