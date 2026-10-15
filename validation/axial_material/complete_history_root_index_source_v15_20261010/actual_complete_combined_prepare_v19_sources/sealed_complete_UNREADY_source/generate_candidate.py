"""Finite standard-library SOURCE-only V19 PREP caller lifetime candidate; no business imports."""
import ast
import hashlib
import json
from pathlib import Path
import stat

D = Path(__file__).parent
P = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py')
P_SHA = '5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240'
READY18 = Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')
U18 = Path('/private/tmp/axmat_v18_complete_combined_full_phase_last_use_source_only_20261010/source_inverse_proof.json')
READY17 = Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')
U17 = Path('/private/tmp/axmat_v17_complete_combined_fresh_wire_trace_table_source_only_FINAL_20261010/source_inverse_proof.json')
ORIGINAL = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py')
GRAPH = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
CHECKS = Path('/Users/wen/spot/validation/axial_material/combined_runtime_historical_input_checks.py')
CURRENT = Path('/Users/wen/spot/validation/axial_material/combined_runtime_current_predicates_final_private_last_uses_20261009.py')
FIXED_INPUTS = [(P,P_SHA),(READY18,'36bac8dcf1a640be03fe2e851d231cedfef0f7b06dc65afb8a0fb1bc6a4ae0ad'),
(U18,'920d4cef7d96e8f0737a82f9e5cad8feb7b7c3387324dc128b66f1c45908f0e4'),
(READY17,'6dda26bbf54de6437b185263b12692f9e4b2d83d6745718dfe8c977ba49204f0'),
(U17,'1813f631c996c89a90c0181a5c481c8f07b9a304c65e78d211083d4c98f13155'),
(ORIGINAL,'0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382'),
(GRAPH,'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),
(CHECKS,'86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e'),
(CURRENT,'fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19')]

def pin(p,expected):
    assert '/validation/artifacts/' not in str(p)
    assert p.resolve()==p
    s=p.lstat();b=p.read_bytes();t=p.lstat()
    fields=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and fields(s)==fields(t)
    assert hashlib.sha256(b).hexdigest()==expected and len(b)==s.st_size
    return b,dict(path=str(p),sha256=expected,size_bytes=len(b),identity7=fields(t))

inputs=[];data={}
for p,expected in FIXED_INPUTS:
    b,q=pin(p,expected);data[p]=b;inputs.append(q)
old=data[P].decode()
text=old
edits=[]
def replace(before,after,count=1,reason='finite SOURCE change'):
    global text
    assert text.count(before)==count,before[:100]
    text=text.replace(before,after)
    edits.append(dict(old=before,new=after,occurrences=count,reason=reason))
tree=ast.parse(old)
doc=tree.body[0]
assert isinstance(doc,ast.Expr) and isinstance(doc.value,ast.Constant)
new_doc = 'UNREADY SOURCE-only V19 complete sender/root-index PREP caller last-use candidate. Actual V18 PREP exceeded the unchanged512 MiB limit; no successful new declaration, graph, build, INPUT or native pins exist. This source changes only finished private caller lifetimes after original full checks, preserving full original graph scope, trace, nine coverage categories, whole historical seven-key body, aliases, namespaces, fresh EOF reads and all original guards and conditions. Original V18 full INPUT phase lifetime corrections remain byteexact. Qualified bcd/d490 pure graph protocol and actual V15 complete86 component remain original INPUT prerequisites. All six future combined/native success pins remain None; this new family has not executed any business or scientific validation.'
replace(ast.get_source_segment(old,doc),repr(new_doc),reason='truthful SOURCE-only scope')
for before,after in [
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010'),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010'),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010'),
('SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V18','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V19'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V18','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19'),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')]:
    replace(before,after,reason='fresh V19 namespace only')
replace("DRAFT_STATUS = 'READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'",
        "DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V19_PREP_CALLER_LAST_USE_REVIEW_REQUIRED'",reason='no READY or business credit')
replace("if DRAFT_STATUS != 'READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':",
        "if DRAFT_STATUS != 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':",reason='original ready guard on fresh family')
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='create_complete_input_graph')
old_fn=ast.get_source_segment(old,node)
new_fn=old_fn
local_edits=[]
def local(before,after,reason):
    global new_fn
    assert new_fn.count(before)==1,before[:100]
    new_fn=new_fn.replace(before,after,1)
    local_edits.append(dict(old=before,new=after,occurrences=1,reason=reason))
local("    before=current_input_predicates(helpers,expanded,True)",
"""    # All original complete owner/alias/namespace construction above has finished.
    # Normalized full owners/namespaces keep every original edge; only caller duplicates end.
    trim_binding=trim['binding']
    del trim,trim_alias_paths
    del failed['files']
    before=current_input_predicates(helpers,expanded,True)
    del before""",
'trim private fields last read after complete namespace creation; failed files copied into complete owners; original first current check finishes before releasing its unused result')
local("    if new_pins or codec.pack_specs(expanded)!=fresh['parsed']:raise ValueError('whole INPUT codec/byte identity differs')",
"""    # The first original full fresh EOF phase has returned; its requirement list
    # has no caller consumers. The full codec equality still runs immediately below.
    del requirements
    if new_pins or codec.pack_specs(expanded)!=fresh['parsed']:raise ValueError('whole INPUT codec/byte identity differs')
    del new_pins,fresh
    # Original whole expanded specs passed their full codec/byte comparison.
    # The following unchanged length/current predicates read exactly these four fields.
    expanded=minimal_live_specs({'metadata':expanded})""",
'discard unused full requirement list before full codec equality; release fresh parsed metadata after equality; retain all four original later-check fields')
local("    failed_lengths=check_failed_prepare_phase(failed,namespaces,actual)\n    trace=audit.snapshot()",
"""    failed_lengths=check_failed_prepare_phase(failed,namespaces,actual)
    del actual
    trace=audit.snapshot()
    del audit""",
'actual pins end only after both original first-phase length checks; completed audit ends only after complete trace snapshot')
local("""    # Release all expanded duplicate owner/ns maps, while normalized full owners,
    # full namespaces and complete actual trace remain. No edge is dropped.
    # Whole expanded JSON already passed the original byte/codec equality.
    # These are exactly the existing current predicate/length-check fields.
    expanded=minimal_live_specs({'metadata':expanded})
    trim_binding=trim['binding']
    del trim,trim_alias_paths,before
    del failed['files']
    del requirements,actual,new_pins,fresh,audit;gc.collect()""",
"""    # Private duplicates ended after their real last uses above. The original
    # collector remains at this original boundary; no new collector is introduced.
    gc.collect()""",
'remove only duplicate later release statements; preserve original collector boundary')
replace(old_fn,new_fn,reason='complete PREP graph caller last uses only')
inverse=text
for e in reversed(edits):
    assert inverse.count(e['new'])==e['occurrences']
    inverse=inverse.replace(e['new'],e['old'])
assert inverse.encode()==data[P]
chain=inverse
chain_sha=[]
for proof_path,wanted in [(READY18,'ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'),
(U18,'feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c'),
(READY17,'82b17014f36520dadc77c387d8e53f7cdd9b5ea92f31b3ee9659ac5464c6239e'),
(U17,'0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382')]:
    j=json.loads(data[proof_path])
    for e in reversed(j['edits']):
        assert chain.count(e['new'])==e['occurrences']
        chain=chain.replace(e['new'],e['old'])
    actual=hashlib.sha256(chain.encode()).hexdigest()
    assert actual==wanted
    chain_sha.append(dict(proof=str(proof_path),sha256=actual))
assert chain.encode()==data[ORIGINAL]

def defs(t):
    return {n.name:ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
old_defs,new_defs=defs(old),defs(text)
assert set(old_defs)==set(new_defs) and len(old_defs)==70
changed=[k for k in old_defs if old_defs[k]!=new_defs[k]]
assert changed==['require_ready','create_complete_input_graph']
assert old_defs['complete_input_phase']==new_defs['complete_input_phase']
assert old_defs['prepare_build']==new_defs['prepare_build']
def condition_nodes(s):
    return [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(s)) if isinstance(n,(ast.If,ast.Assert,ast.Raise))]
assert condition_nodes(old_fn)==condition_nodes(new_fn)
def calls(s,names):
    return [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Call) and ast.unparse(n.func) in names]
critical={'g.strict_json','codec.unpack_specs','g._owners','checks.bind_aliases','g.capture_aliases','g._alias_map','g._absence_phase','checks.bind_namespaces','graph_trim_namespaces','g.explicit_sealed_namespace','current_input_predicates','g._phase','codec.pack_specs','checks.check_failed_lengths_and_owned_negative_bytes','check_failed_prepare_phase','audit.snapshot','write_new','g.create_fresh_complete_wire_graph','g.encode_complete_graph_table_storage','graph_input_bindings'}
assert calls(old_fn,critical)==calls(new_fn,critical)
assert calls(old_fn,{'gc.collect'})==calls(new_fn,{'gc.collect'})
def spec_fields(source,name):
    n=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name==name)
    return sorted({x.slice.value for x in ast.walk(n) if isinstance(x,ast.Subscript) and isinstance(x.value,ast.Name) and x.value.id=='specs' and isinstance(x.slice,ast.Constant) and isinstance(x.slice.value,str)})
fields=set()
for name in ('check_member_and_directory_predicates','check_failed_lengths_and_owned_negative_bytes'):
    fields.update(spec_fields(data[CHECKS].decode(),name))
fields.update(spec_fields(data[CURRENT].decode(),'check_current_predicate_subset'))
assert fields <= {'reached_component_records','independent_directory_owners','remaining_source_owned_requirements','aliases'}
for name in ('failed_prepare_phase',):
    pass
n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check_failed_prepare_phase')
failed_fields={x.slice.value for x in ast.walk(n) if isinstance(x,ast.Subscript) and isinstance(x.value,ast.Name) and x.value.id=='failed' and isinstance(x.slice,ast.Constant)}
assert failed_fields=={'namespaces'}
assert "descriptor = {\"owner\": owner" in data[GRAPH].decode()
assert "\"expected_files\": {_path(path): _sha(digest) for path, digest in mapping.items()}" in data[GRAPH].decode()
globals_old={};globals_new={}
for t,dst in [(old,globals_old),(text,globals_new)]:
    for n in ast.parse(t).body:
        if isinstance(n,ast.Assign):
            for target in n.targets:
                if isinstance(target,ast.Name):dst[target.id]=ast.dump(n.value,include_attributes=False)
changed_globals=sorted(k for k in globals_old if globals_old[k]!=globals_new[k])
assert changed_globals==['DRAFT_STATUS','FAMILY','FORMAL_FACTORY','OUT','PREFIX','SOURCE','TERMINAL']
future=[k for k in globals_new if k.startswith('FUTURE_ACTUAL_') and k!='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']
assert len(future)==6 and all(globals_new[k]==ast.dump(ast.Constant(value=None),include_attributes=False) for k in future)
compile(text,str(D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py'),'exec')
for q,(p,expected) in zip(inputs,FIXED_INPUTS):
    assert pin(p,expected)[1]==q
candidate=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py'
with candidate.open('xb') as f:f.write(text.encode())
candidate_pin=pin(candidate,hashlib.sha256(text.encode()).hexdigest())[1]
proof=dict(schema='AXMAT_V19_COMPLETE_PREP_CALLER_LAST_USE_SOURCE_INVERSE_V1',
status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_SOURCE_AND_ACTUAL_FRESH_RUNTIME',
inputs=inputs,candidate=candidate_pin,edits=edits,local_create_edits=local_edits,
source_inputs_fresh_full_EOF_before_after_exact=True,full_inverse_to_actual_V18_5c4b_exact=True,
full_ancestry_inverse_5c4b_ecfd_feeb_82_0ea=chain_sha,
changed_definitions=changed,unchanged_definitions_count=68,
V18_complete_input_phase_byteexact=True,prepare_build_byteexact=True,
all_original_create_If_Assert_Raise_nodes_exact=True,
all_original_full_phase_and_check_calls_sequence_exact=True,
original_create_gc_calls_exact_no_extra_collectors=True,
four_later_check_fields_SOURCE_verified=sorted(fields),
failed_length_checker_complete_namespaces_only_SOURCE_verified=True,
normalized_owners_complete_SHA_maps_copied_by_original_qualified_helper_SOURCE_verified=True,
globals_except_fresh_namespace_and_UNREADY_status_byteexact=True,all_six_future_business_success_pins_None=True,
qualified_bcd_helper_d490_and_real_component_source_bindings_unchanged=True,
no_memo_or_graph_trace_scope_pruning_or_cross_phase_SHA_shortcut=True,
no_mathematical_or_physical_input_or_budget_change=True,
new_business_executed=False,project_written=False,ART_read_or_written=False,
project_module_or_helper_imported_or_called=False,numeric_payload_read=False,
resource_check_called=False,new_native_or_AAA_or_ABA_credit=False)
with (D/'source_inverse_proof.json').open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
report=dict(schema='AXMAT_V19_COMPLETE_PREP_CALLER_LAST_USE_SOURCE_REPORT_V1',
status=proof['status'],candidate=candidate_pin,
finding='The first-phase returned requirement list has no caller use; fresh parsed specs end after the original complete codec comparison; actual pins end after both original first-phase length checks; the inactive audit ends after its complete snapshot; normalized full owners and namespace descriptors retain all trim/failed edges.',
limitations=['No source-line cause of the actual V18 RSS excess was observed.','No predicted or actual future PASS or peak RSS claim.','No runtime, helper, component API or numerical payload was read or executed.'],
Root_reported_actual_V18_PREP_failure=dict(initial_chunk='026dfe',original_session_id=47917,terminal_chunk='d1800c',exit_code=1,closed=True,child_returncode=-15,child_seconds=160.698918,sampled_peak_rss_mib=514.421875,source='Root message; no direct ART read'),
original_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,stages=5,threads=1,children=1,retries=0,strict_JSON_bytes=64*2**20),
next_step='Independent complete SOURCE review, then a separate truthful READY binding and fresh V19 bounded PREP if Root authorizes installation. Failed V18 namespaces must never be rerun.',
fresh_namespaces=dict(canonical_factory='/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py',source='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010',out='/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010',terminal='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010',planned_prepare_host='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v19-20261010'),
future_success_pins={k:None for k in future},qualified_helper_retained_only_as_INPUT=True,
installed=False,business_executed=False,science_credit=False)
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(source_only=True,UNREADY=True,candidate=candidate_pin,
proof=pin(D/'source_inverse_proof.json',hashlib.sha256((D/'source_inverse_proof.json').read_bytes()).hexdigest())[1],
report=pin(D/'REPORT.json',hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest())[1],
changed_definitions=changed,unchanged_definitions_count=68,full_inverse_5c4b_ecfd_feeb_82_0ea=True,business_executed=False)))
