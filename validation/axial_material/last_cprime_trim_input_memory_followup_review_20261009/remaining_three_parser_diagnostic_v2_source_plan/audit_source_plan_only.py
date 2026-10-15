"""Source-only static and tiny synthetic fixture audit; never loads watch or worker."""
import ast
import copy
import hashlib
import json
from pathlib import Path

O=Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_v2_20261009')
P=Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_20261009')
mother=(P/'root_owned_parser_watchdog.py').read_text()
candidate=(O/'root_owned_parser_watchdog.py').read_text()
assert hashlib.sha256(mother.encode()).hexdigest()=='e5177791ee5c88e36aa5f161f917c8baa4106fc62556bb3e5b6e0d39eb6a9e63'
assert hashlib.sha256(candidate.encode()).hexdigest()=='5983010d03389ac3a6170d349c09761c88381d1bce3894fd9545faeff98c5271'
compile(candidate,str(O/'root_owned_parser_watchdog.py'),'exec')
A={n.name:n for n in ast.parse(mother).body if isinstance(n,ast.FunctionDef)}
B={n.name:n for n in ast.parse(candidate).body if isinstance(n,ast.FunctionDef)}
def segment(source,node):
 return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
for name in A:
 if name not in ('run_case','main'):
  assert segment(mother,A[name])==segment(candidate,B[name])
  assert ast.dump(A[name],include_attributes=False)==ast.dump(B[name],include_attributes=False)
assert segment(candidate,B['run_case'])==segment(mother,A['run_case']).replace('data_before=data_before,data_after=after_data','data_before=before_data,data_after=after_data')
assert (P/'parser_metadata_worker.py').read_bytes()==(O/'parser_metadata_worker.py').read_bytes()
assert hashlib.sha256((O/'parser_metadata_worker.py').read_bytes()).hexdigest()=='9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552'
inverse=json.loads((O/'complete_source_positional_inverse.json').read_text())
restored=candidate
for op in reversed(inverse['operations']):
 assert restored[op['candidate_start']:op['candidate_end']]==op['candidate_text']
 restored=restored[:op['candidate_start']]+op['mother_text']+restored[op['candidate_end']:]
assert restored==mother
constants={}
for node in ast.parse(candidate).body:
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('REMAINING_CASES','RETAINED_PHASES'):
  constants[node.targets[0].id]=ast.literal_eval(node.value)
assert constants['REMAINING_CASES']==(('candidate','DECL'),('original','FULL_SEVEN_INPUT'),('candidate','FULL_SEVEN_INPUT'))
def receipt_expression(node):
 return next(n.value for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='value' for t in n.targets))
class FixtureProc:
 pid=900001
 returncode=0
fixture=dict(dict=dict,pin=lambda p:{'fixture_only_pin':str(p)},proc=FixtureProc(),passed=True,command=['SYNTHETIC_NO_PROCESS'],CAP_SECONDS=120,CAP_MIB=512,elapsed=1.,count=2,peak=5.,phases={},retained_phase_coverage={},failure=None,cleanup={'fixture':True},before_source={'fixture':'source-before'},after_source={'fixture':'source-after'},before_data={'fixture':'data-before'},after_data={'fixture':'data-after'},worker_pin={'fixture':'worker'},stdout=Path('fixture-stdout'),stderr=Path('fixture-stderr'),case=Path('fixture-case'),child={'rusage_maxrss':{'fixture':True}},report_path=Path('fixture-report'))
try:
 eval(compile(ast.Expression(receipt_expression(A['run_case'])),'mother_tiny_receipt','eval'),fixture)
 raise AssertionError('Expected mother NameError')
except NameError as error:
 assert 'data_before' in str(error)
receipt=eval(compile(ast.Expression(receipt_expression(B['run_case'])),'v2_tiny_receipt','eval'),fixture)
assert receipt['data_before']==fixture['before_data'] and receipt['data_after']==fixture['after_data']
assert 'before_data' not in receipt and 'after_data' not in receipt
namespace={'RETAINED_PHASES':constants['RETAINED_PHASES']}
exec(compile(ast.Module(body=[B['compare_output_and_stable_phase_RSS']],type_ignores=[]),'pure_AST_comparison_tiny_fixture','exec'),namespace)
compare=namespace['compare_output_and_stable_phase_RSS']
original=dict(plain_builtin_type_counts={'dict':1},type_and_insertion_order_shape_sha256='fixture-shape',whole_insertion_order_JSON_output_sha256='fixture-output',whole_insertion_order_JSON_output_bytes=42,mutable_container_independence=True)
changed=copy.deepcopy(original)
phases={name:dict(samples=1,min_mib=10.,max_mib=20.,last_mib=15.) for name in constants['RETAINED_PHASES']}
other=copy.deepcopy(phases)
before=json.dumps([original,changed,phases,other],sort_keys=True)
outputs,rss=compare(original,changed,phases,other)
assert all(outputs.values()) and all(x['candidate_minus_original_max_mib']==0 for x in rss.values())
assert json.dumps([original,changed,phases,other],sort_keys=True)==before
changed['whole_insertion_order_JSON_output_bytes']=43
assert compare(original,changed,phases,other)[0]['whole_insertion_order_JSON_output_bytes'] is False
other[constants['RETAINED_PHASES'][0]]['max_mib']=17.
assert compare(original,original,phases,other)[1][constants['RETAINED_PHASES'][0]]['candidate_minus_original_max_mib']==-3.
other[constants['RETAINED_PHASES'][0]]['samples']=0
try:
 compare(original,original,phases,other)
 raise RuntimeError('Missing stable phase was not rejected')
except AssertionError:
 pass
plan=json.loads((O/'source_plan.json').read_text())
assert plan['overall_four_case_watchdog_qualification'] is False and plan['original_DECL_rerun'] is False
assert plan['known_prior_parent_failed_baseline']['original_child_wait_returncode'] is None
assert plan['known_prior_parent_failed_baseline']['prior_parent_actual_tool_exit_code']==1
for key in ('actual_business_RUNNING_stage','actual_child_PID','actual_measurements','actual_output','actual_tool_terminal','future_remaining_three_actual_child_pids','future_remaining_three_actual_child_returncodes','future_remaining_three_actual_receipts','future_remaining_three_actual_diagnostic_success','future_comparisons_and_RSS_deltas'):
 assert plan[key] is None
for name in ('load_prior_original_decl','main'):
 text=segment(candidate,B[name])
 assert 'overall_four_case_watchdog_qualification=False' in text
 assert 'original_child_wait_returncode=None' in text or 'prior_original_DECL_child_wait_returncode=None' in text
print(json.dumps(dict(status='PASS_SOURCE_ONLY_STATIC_AND_8_SYNTHETIC_TINY_FIXTURES',watch_worker_or_business_executed=False,complete_inverse=True,unchanged_original_helpers=6,worker_byte_exact=True,remaining_cases=3,original_DECL_rerun=False,overall_four_case_watchdog_qualification=False)))
