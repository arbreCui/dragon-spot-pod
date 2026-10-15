"""Read exact SOURCE anchors only; never write or execute business candidates."""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).absolute().parent
R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
C = R / 'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py'
H = B / 'actual_complete_combined_prepare_v21_sources/sealed_READY_runtime_and_PREP_binding/BOUND_READY_SOURCE/combined_prepare_host.py'

def pin(p):
    s = p.lstat(); before = [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    b = p.read_bytes(); t = p.lstat(); after = [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    assert before == after and len(b) == before[4]
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'identity':before}

cb = pin(C); hb = pin(H); c = C.read_text(); h = H.read_text(); tree = ast.parse(c); hosttree = ast.parse(h)
assert cb['sha256'] == '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'
assert hb['sha256'] == '776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405'
cglobals = {n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
hglobals = {n.targets[0].id:n for n in hosttree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}

def anchor(source,node,purpose):
    exact = ast.get_source_segment(source,node)
    return {'line':node.lineno,'whole_exact_source_anchor':exact,'whole_source_occurrences':source.count(exact),'purpose':purpose}

ca = [anchor(c, tree.body[0], 'Truthful new V22 UNREADY doc; after actual new Q only helper metadata qualified, new business six pins remain None')]
for name in ('SOURCE','OUT','TERMINAL','FAMILY','DRAFT_STATUS','PREFIX','FORMAL_FACTORY'):
    ca.append(dict(global_name=name,**anchor(c,cglobals[name], 'Retarget only own fresh V22 family; original historical namespaces remain unchanged')))
graph = cglobals['INPUT_HELPERS'].value
assert isinstance(graph, ast.Dict)
gi = next(i for i,k in enumerate(graph.keys) if ast.literal_eval(k)=='graph')
ca.append(dict(global_name="INPUT_HELPERS['graph']", **anchor(c,graph.values[gi], 'Fresh cf0 helper exact path; new SHA stays None in UNREADY, then cf0 only after actual new Q metadata Source binding')))
ca.append(dict(global_name='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA', **anchor(c,cglobals['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'], 'None until actual new V22 Q exists and saved actual joint-admission META is independently reviewed; old29ac gives no cf0 credit')))
ready = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='require_ready')
condition = next(n for n in ast.walk(ready) if isinstance(n,ast.Compare) and isinstance(n.left,ast.Name) and n.left.id=='DRAFT_STATUS')
ca.append(dict(global_name='require_ready original status predicate', **anchor(c,condition, 'Own V22 READY status literal only; entire original If/Raise/Call order retained')))
ha = []
for name in ('HOST','TARGET','TARGET_SHA','SOURCE','OUT','TERMINAL','SOURCE_ARCHIVE'):
    ha.append(dict(global_name=name, **anchor(h,hglobals[name], 'Fresh V22 host/path; TARGET_SHA unknown until full READY source exists; Source archive complete dynamic inventory')))
for node in ast.walk(hosttree):
    if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value in ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_DECLARATION_V1','AXMAT_V21_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1'):
        ha.append(anchor(h,node, 'Only new V22 own schema; original guard and resource caps unchanged'))
for node in ast.walk(hosttree):
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='pin' and len(node.args)==2 and isinstance(node.args[1],ast.Constant) and node.args[1].value in ('dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7','29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'):
        ha.append(anchor(h,node, 'Bind actual installed cf0 helper or actual new V22 Q path/SHA, never old helper/Q credit'))
assert len(ca)==11 and len(ha)==11 and all(x['whole_source_occurrences']==1 for x in ca+ha)
six={name:ast.literal_eval(node.value) for name,node in cglobals.items() if name.startswith('FUTURE_ACTUAL_') and name!='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'}
assert len(six)==6 and all(x is None for x in six.values())
result={'schema':'V22_EXACT_FUTURE_CANONICAL_GENUINE_PREP_SOURCE_LOCATIONS_ONLY_V1','source_only':True,'canonical_parent':cb,'genuine_PREP_host_parent':hb,'canonical_exact_anchors':ca,'canonical_own_global_qualifications_and_doc_only':True,'original70definitions_bytes_and_math_to_remain_unchanged_except_require_ready_own_status_literal':True,'host_exact_11_atomic_anchors':ha,'six_future_business_pins':six,'future_runtime_READY_source_sha256':None,'future_new_joint_helper_Q_sha256':None,'future_build_seal_Root_terminal_whole_INPUT_native_AAA_ABA_physics_pins':None,'genuine_PREP_caps':{'whole_seconds':1800,'phase_seconds':600,'rss_mib':512,'archive_bytes':2*2**30,'history_bytes':96*2**30,'free_bytes':8*2**30,'threads':1,'children':1,'retries':0},'complete_original_input_and_Source_inventory_policy':'Original historical seven-body physics/input/categories/pins retained; new Source complete dynamic inventory, no fixed-count crop; full metadata writer retarget/copy before D freeze; no D append after freeze','canonical_or_host_candidate_written':False,'project_API_or_business_executed':False,'old_helper_dc01_and_Q29ac_unchanged':True}
with (HERE/'EXACT_FUTURE_CANONICAL_GENUINE_PREP_SOURCE_LOCATIONS.json').open('x') as f: json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
assert pin(C)==cb and pin(H)==hb
print(json.dumps({'source_only':True,'canonical_anchors':len(ca),'host_atomic_anchors':len(ha),'all_anchors_unique':True,'all6_future_None':True,'business_candidates_written':False}))
