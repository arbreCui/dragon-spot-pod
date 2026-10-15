"""Independent finite AST review of all108 strict require arguments; no candidate execution."""
import ast,hashlib,json
from pathlib import Path
P=Path(__file__).parent
source=P/'actual_failed_native_checker_SOURCE.py'
raw=source.read_bytes();s=raw.decode();tree=ast.parse(s)
assert hashlib.sha256(raw).hexdigest()=='403feaa916159c901f7b4f44c6a7c70798afac7ce5035cdbded90a14a5c96517'
def callname(x):
 if isinstance(x,ast.Name):return x.id
 if isinstance(x,ast.Attribute):return callname(x.value)+'.'+x.attr
 return '?'
def boolean_leaves(x):
 if isinstance(x,ast.Compare):return []
 if isinstance(x,ast.UnaryOp)and isinstance(x.op,ast.Not):return []
 if isinstance(x,ast.Constant)and type(x.value)is bool:return []
 if isinstance(x,ast.BoolOp):
  return [y for v in x.values for y in boolean_leaves(v)]
 if isinstance(x,ast.Call)and (callname(x.func)in ('all','any','isinstance','math.isfinite','bool','stat.S_ISREG','stat.S_ISDIR','stat.S_ISLNK')or isinstance(x.func,ast.Attribute)and x.func.attr in ('is_dir','is_file','is_symlink','exists','is_relative_to','is_integer','is_absolute')):
  return []
 return [ast.get_source_segment(s,x)]
rows=[]
for n in sorted((n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require'),key=lambda n:n.lineno):
 rows.append(dict(line=n.lineno,condition=ast.get_source_segment(s,n.args[0]),condition_AST=ast.dump(n.args[0],include_attributes=False),argument_kind=type(n.args[0]).__name__,non_obvious_boolean_leaves=boolean_leaves(n.args[0])))
assert len(rows)==108
unresolved=[r for r in rows if r['non_obvious_boolean_leaves']]
assert [(r['line'],r['non_obvious_boolean_leaves'])for r in unresolved]==[(245,['name']),(556,['ended']),(755,['inputs']),(819,['full'])]
assignments={}
for n in ast.walk(tree):
 if isinstance(n,ast.Assign):
  for target in n.targets:
   if isinstance(target,ast.Name)and target.id in ('ended','full','name'):
    assignments.setdefault(target.id,[]).append(dict(line=n.lineno,Source=ast.get_source_segment(s,n),value_AST=ast.dump(n.value,include_attributes=False)))
ended=[n for n in ast.walk(tree)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ended'for t in n.targets)]
assert len(ended)==2 and {n.value.value for n in ended if isinstance(n.value,ast.Constant)}=={False,True}
full=[n for n in ast.walk(tree)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='full'for t in n.targets)]
assert len(full)==1 and isinstance(full[0].value,ast.Call)and callname(full[0].value.func)=='all'
name_proof=next(r for r in rows if r['line']==245)
assert name_proof['condition']=='name and name not in names'
bad=next(r for r in rows if r['line']==755)
assert bad['condition']=='type(inputs) is list and inputs'
report=dict(schema='INDEPENDENT_ALL108_NATIVE_CHECKER_STRICT_REQUIRE_SOURCE_ARGUMENT_REVIEW_V1',
 status='SOURCE_ONLY_ONE_DETERMINATE_VALID_INPUT_NONBOOL_REJECTION_AT755',
 source_sha256=hashlib.sha256(raw).hexdigest(),source_bytes=len(raw),
 strict_require_call_count=108,all108_calls_preserved=rows,
 relevant_local_assignment_Source=assignments,
 special_condition_analysis=[
 dict(line=245,valid_name_nonempty_returns_builtin_membership_bool=True,invalid_blank_string_shortcircuit_returns_empty_str_and_is_correctly_rejected=True,no_valid_input_bug_identified=True),
 dict(line=556,ended_only_builtin_boolean_assignments=[False,True],valid_last_comparison_returns_bool=True,no_valid_input_bug_identified=True),
 dict(line=755,actual_complete_input_type='builtin list',actual_list_count=129,nonempty_valid_list_returns_list=True,strict_require_rejects_that_nonbool=True,minimum_fix='type(inputs) is list and len(inputs)>0',strict_require_function_unchanged_required=True,full129_scope_unchanged_required=True),
 dict(line=819,full_from_builtin_all_returns_bool=True,no_valid_input_bug_identified=True)],
 no_other_determinate_valid_input_nonbool_rejection_identified=True,
 no_dynamic_candidate_or_protocol_test_executed=True,
 no_call_condition_dropped_or_coerced=True,
 all_existing_comparisons_membership_all_any_type_bool_guard_semantics_preserved=True,
 original_require_rejects_nonbool_unchanged_required=True,
 new_Source_mother_author_is_other_agent=True,
 new_family23_must_be_fresh_bound_and_independently_Source_reviewed_before_actual_Run=True,
 actual_native_byte_qualification_sha256=None,
 native_RSS_verified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (P/'STRICT_REQUIRE_ALL108_SOURCE_REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=report['status'],strict_require_call_count=108,only_determinate_valid_input_bug_line=755,no_candidate_executed=True)))
