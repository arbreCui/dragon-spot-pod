"""Finite SOURCE-only V20 candidate; one completed JSON raw-byte local lifetime changes."""
import ast
import hashlib
import json
from pathlib import Path
import stat

D=Path(__file__).parent
P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')
P_SHA='34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b'
def pin(p,expected=None):
    assert '/validation/artifacts/' not in str(p) and p.resolve()==p
    s=p.lstat();b=p.read_bytes();t=p.lstat()
    fields=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and fields(s)==fields(t) and len(b)==s.st_size
    h=hashlib.sha256(b).hexdigest()
    if expected is not None:assert h==expected
    return b,dict(path=str(p),sha256=h,size_bytes=len(b),identity7=fields(t))
old_bytes,parent=pin(P,P_SHA);old=old_bytes.decode()
def definitions(t):
    return {n.name:ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
old_defs=definitions(old)
strict_old=old_defs['strict_json_bytes']
before="    value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)"
after=before+"\n    del raw"
assert strict_old.count(before)==1
strict_new=strict_old.replace(before,after)
a=ast.parse(strict_old).body[0]
loads=[n for n in ast.walk(a) if isinstance(n,ast.Name) and n.id=='raw' and isinstance(n.ctx,ast.Load)]
assert len(loads)==1 and isinstance(a.args.args[0],ast.arg) and a.args.args[0].arg=='raw'
assert old_defs['read']=="def read(path):return strict_json_bytes(require(path).read_bytes())"
def condition_nodes(s):
    return [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(s)) if isinstance(n,(ast.If,ast.Assert,ast.Raise))]
def call_nodes(s):
    return [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Call)]
assert condition_nodes(strict_old)==condition_nodes(strict_new)
assert call_nodes(strict_old)==call_nodes(strict_new)
assert [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(strict_old)) if isinstance(n,ast.Return)]==[ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(strict_new)) if isinstance(n,ast.Return)]
proposal=dict(schema='AXMAT_V20_STRICT_JSON_RAW_LAST_USE_SINGLE_SOURCE_PROPOSAL_V1',
status='SOURCE_ONLY_PROPOSAL_NO_OBSERVED_PEAK_LINE_CAUSE_OR_PREDICTED_PASS',
    parent_source=parent,source_lines=dict(strict_json_bytes_start=261,json_loads_complete=268,finite_validation_start=269,return_line=276),
old_function_source=strict_old,proposed_function_source=strict_new,
sole_change='Insert del raw immediately after the original complete json.loads returns, before original full finite-value traversal.',
raw_argument_Load_count=1,raw_last_Load_is_original_complete_json_decode=True,
normal_read_caller_has_no_named_raw_local=True,
all_original_JSON_pairs_parse_constant_finite_conditions_and_call_and_return_AST_exact=True,
no_graph_or_trace_or_descriptor_or_historical_body_change=True,
no_new_gc_malloc_cache_skip_memo_or_budget_change=True,
limitations=['The original complete decode allocations and its instantaneous peak are unchanged.','Only the completed local raw reference lifetime changes; no actual RSS consequence has been measured.','Actual V19 build peak512.1875 MiB was not observed at a specific source line.'],
Root_reported_actual_V19_build_failure=dict(initial_chunk='813c12',original_session_id=63671,terminal_chunk='128ba5',typed_exit_code=1,closed=True,child_returncode=-15,child_seconds=123.553010,sampled_peak_rss_mib=512.1875,original_rss_cap_mib=512,actual_inner_PASS=['build/link'],other_four_stages_incomplete=True,no_seal_or_driver_result_or_native=True,source='Root message only; no ART read'),
other_lifetime_findings=['run_build d remains required by all before-stage and run_finally environments and final audit field comparisons.','commands remain required by the final complete five-command comparison and audit command.','binary_audit and audit_build are reached after the four original metadata stages, so their later private views do not identify this observed only-link-PASS failure.','declaration_admission proof/link/inverse can have small last-use cleanup, but no source evidence establishes a large new retained payload there.'],
business_or_API_or_helper_executed=False,numeric_payload_read=False,resource_check_called=False,ART_read_or_written=False)
proposal_path=D/'SINGLE_POINT_PROPOSAL.json'
proposal_bytes=(json.dumps(proposal,indent=2,allow_nan=False)+'\n').encode()
if proposal_path.exists():
    assert proposal_path.read_bytes()==proposal_bytes
else:
    with proposal_path.open('xb') as f:f.write(proposal_bytes)
text=old;edits=[]
def replace(before,after,count=1,reason='finite source change'):
    global text
    assert text.count(before)==count,before[:90]
    text=text.replace(before,after)
    edits.append(dict(old=before,new=after,occurrences=count,reason=reason))
replace(old.splitlines()[0],repr('UNREADY SOURCE-only V20 complete sender/root-index strict JSON raw last-use candidate. Actual V19 complete build exceeded the unchanged512 MiB limit after only build/link passed; no successful new complete build seal, whole INPUT or native qualification exists. The sole lifetime change releases the strict reader raw-byte local only after original full JSON decoding and before its unchanged full finite-value checks. Decode-process peak remains unchanged and no future RSS PASS is predicted. All original PREP, run_build, environment, full fresh EOF phases, graph scope, trace, aliases, namespaces, nine coverage categories, historical seven-key bodies, physical inputs, guards and budgets remain complete. Qualified bcd/d490 pure helper protocol and actual V15 complete86 component remain original INPUT prerequisites. All six future combined/native success pins remain None; this fresh V20 family has executed no business or scientific validation.'),reason='truthful UNREADY complete source scope')
for before,after in [
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v20-20261010'),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010'),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v20-20261010'),
('SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V19','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V20'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V20'),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')]:
    replace(before,after,reason='fresh fixed V20 namespace only')
replace("DRAFT_STATUS = 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'",
"DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V20_STRICT_JSON_RAW_LAST_USE_REVIEW_REQUIRED'",reason='no READY claim or new business pins')
replace("if DRAFT_STATUS != 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':",
"if DRAFT_STATUS != 'READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':",reason='same original require_ready guard in fresh family')
replace(strict_old,strict_new,reason='the single completed private raw local lifetime')
reverse=text
for e in reversed(edits):
    assert reverse.count(e['new'])==e['occurrences'];reverse=reverse.replace(e['new'],e['old'])
assert reverse.encode()==old_bytes
new_defs=definitions(text)
assert len(old_defs)==len(new_defs)==70 and set(old_defs)==set(new_defs)
changed=[k for k in old_defs if old_defs[k]!=new_defs[k]]
assert changed==['require_ready','strict_json_bytes']
for name in old_defs:
    if name not in changed:assert old_defs[name]==new_defs[name]
assert old_defs['require_ready'].replace('READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')==new_defs['require_ready']
for name in old_defs:
    assert call_nodes(old_defs[name])==call_nodes(new_defs[name])
    expected=old_defs[name]
    if name=='require_ready':expected=expected.replace('READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
    assert condition_nodes(expected)==condition_nodes(new_defs[name])
def assignments(t):
    result={}
    for n in ast.parse(t).body:
        if isinstance(n,ast.Assign):
            for q in n.targets:
                if isinstance(q,ast.Name):result[q.id]=ast.dump(n.value,include_attributes=False)
    return result
og,ng=assignments(old),assignments(text)
assert set(og)==set(ng)
changed_globals=sorted(k for k in og if og[k]!=ng[k])
assert changed_globals==['DRAFT_STATUS','FAMILY','FORMAL_FACTORY','OUT','PREFIX','SOURCE','TERMINAL']
future=[k for k in ng if k.startswith('FUTURE_ACTUAL_') and k!='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']
assert len(future)==6 and all(ng[k]==ast.dump(ast.Constant(value=None),include_attributes=False) for k in future)
compile(text,str(D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.UNREADY.py'),'exec')
assert pin(P,P_SHA)[1]==parent
candidate=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.UNREADY.py'
with candidate.open('x') as f:f.write(text)
cp=pin(candidate)[1]
proof=dict(schema='AXMAT_V20_COMPLETE_STRICT_JSON_RAW_LAST_USE_SOURCE_INVERSE_V1',
status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_SOURCE_REVIEW_AND_ACTUAL_FRESH_RUNTIME',
parent=parent,candidate=cp,edits=edits,finite_change_count=len(edits),
entire_byte_inverse_to_34ef_parent_exact=True,parent_full_EOF_SHA7ID_before_after_exact=True,
original_definition_names_and_count70_exact=True,changed_definitions=changed,
other_68_definitions_byteexact=True,
prepare_build_run_build_environment_complete_input_phase_and_helpers_byteexact=True,
all_original_call_nodes_and_order_in_all_definitions_AST_exact=True,
all_original_If_Assert_Raise_AST_exact_except_literal_require_ready_version=True,
strict_reader_all_original_If_Assert_Raise_Call_Return_AST_exact=True,
only_raw_argument_single_last_Load_released_after_full_decode=True,
all_globals_except_fresh_namespace_and_UNREADY_status_AST_exact=True,
original_math_physical_inputs_scope_budgets_and_genuine_guards_unchanged=True,
actual_qualified_bcd_d490_and_original_component_bindings_unchanged=True,
all_six_future_business_success_pins_None=True,
project_or_ART_written=False,project_or_helper_API_imported_or_called=False,
numeric_payload_read=False,resource_check_called=False,
candidate_executed=False,new_RSS_or_science_credit=False)
with (D/'source_inverse_proof.json').open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
report=dict(schema='AXMAT_V20_COMPLETE_SINGLE_RAW_LAST_USE_SOURCE_REPORT_V1',
status=proof['status'],candidate=cp,original_parent=parent,
only_semantic_source_change='del raw after original strict full JSON decoding; all parsed contents and validation remain.',
original_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,stages=5,threads=1,children=1,retries=0,complete_graph_strict_JSON_bytes=64*2**20),
future_success_pins={k:None for k in future},
existing_READY_generator_to_retarget_later='/private/tmp/axmat_v19_complete_combined_READY_source_binding_20261010/source_binding_generator.py',
existing_normal_PREP_generator_to_retarget_later='/private/tmp/axmat_v19_normal_PREP_host_source_binding_20261010/generate_prepare_host.py',
future_SOURCE_binding_plan='After exact independent V20 SOURCE review, reuse the prior finite two-edit READY binding and nine-retarget normal PREP host generation. No old failed family may be rerun and no successful business pins may be inferred.',
fresh_namespaces=dict(canonical_factory='/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py',source='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v20-20261010',out='/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010',terminal='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v20-20261010',planned_prepare_host='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v20-20261010'),
source_line_failure_cause_observed=False,decode_process_peak_eliminated=False,future_RSS_PASS_predicted=False,
installed=False,business_or_helper_API_called=False,numeric_payload_read=False,
resource_check_called=False,ART_read_or_written=False,new_native_or_AAA_or_ABA_credit=False)
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,UNREADY=True,candidate=cp,
proof=pin(D/'source_inverse_proof.json')[1],report=pin(D/'REPORT.json')[1],proposal=pin(D/'SINGLE_POINT_PROPOSAL.json')[1],
entire_inverse_to_34ef=True,other_68_definitions_exact=True,all_original_calls_AST_exact=True,all_original_conditions_AST_exact_except_READY_version=True,candidate_executed=False)))
