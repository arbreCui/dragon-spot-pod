#!/usr/bin/env python3
"""Finite standard-library SOURCE-only V20 -> V21 UNREADY generation.
No Q, ART payload, project module, guard, API or business branch is read/executed.
The future actual qualification field contract is intentionally deferred.
"""
from pathlib import Path
import ast
import hashlib
import json
import os
import stat
import sys

DEST = Path(__file__).absolute().parent
PARENT = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')
PARENT_SHA = '566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3'
PROTO_DIR = Path('/private/tmp/axmat_v21_canonical_decode_last_use_SOURCE_plan_20261010_ef9qq1yd')
PROTO = PROTO_DIR/'combined_runtime_strict_JSON_decode_last_use.SOURCE_ONLY.py'
PROTO_SHA = 'f229e3116f61caad7b4c34f3ccd5705e5392f58ee2fd97066425bd64f57f5125'
PROTO_PROOF = PROTO_DIR/'source_inverse_proof.json'
PROTO_PROOF_SHA = '199efa99bb33b2a739b7ad48a6e855d22983f86d46fe51cfbd0c614954985e3c'
PROTO_REVIEW = PROTO_DIR/'REVIEW.json'
CANDIDATE_NAME = 'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.UNREADY.py'
NEW_HELPER_PATH = '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py'
NEW_HELPER_SOURCE_CONTEXT_SHA = 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
NEW_HELPER_SOURCE_CONTEXT_BYTES = 147870
NEW_DOC = (
    'UNREADY SOURCE-only V21 complete sender/root-index full graph private verifier design. '
    'The complete V20 parent remains the sole runtime source parent. Its actual complete build '
    'exceeded the unchanged 512 MiB limit after only build/link passed; the precise peak source line '
    'was not observed. The independently SOURCE-reviewed strict reader change preserves the entire '
    'UTF-8 decode, original JSON pairs/reject hooks and full finite-value checks, ending raw after '
    'successful decode and decoded after successful JSON parsing. The new private full verifier helper '
    'has independent SOURCE review only; its new graph-helper success SHA and actual qualification SHA '
    'remain None until Root completes actual original pure protocol controls, full current-graph fresh '
    'verification and saved review. The new helper path is design context, not business qualification. '
    'All original functions, PREP, complete five-stage build, whole INPUT admission, physical inputs, '
    'seven historical component bodies, full graph/trace, aliases, namespaces, nine coverage categories, '
    'both complete fresh reads, guards and budgets remain complete. The original actual V15 complete86 '
    'component pins remain unchanged. All six future combined/native success pins remain None. '
    'This fresh V21 family has executed no business, build, native or scientific validation; SOURCE-only '
    'review predicts no RSS reduction or future PASS. No actual new helper Q is read or bound here.'
)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def identity(path):
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
        raise ValueError('ordinary single-link SOURCE file required')
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def source_read(path, expected=None):
    a = identity(path)
    data = path.read_bytes()
    b = identity(path)
    if a != b or len(data) != a[4] or (expected is not None and sha(data) != expected):
        raise ValueError('fixed SOURCE pin changed: '+str(path))
    return data,dict(path=str(path),sha256=sha(data),identity7=a,whole_SOURCE_EOF_read=True)

def dump(node):
    return ast.dump(node,include_attributes=False)

def source_segment(text,node):
    return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

def topdefs(text):
    return {node.name:node for node in ast.parse(text).body
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def globals_by_name(text):
    rows={}
    for node in ast.parse(text).body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name): rows[target.id]=node
                elif isinstance(target,(ast.Tuple,ast.List)):
                    for item in target.elts:
                        if isinstance(item,ast.Name): rows[item.id]=node
        elif isinstance(node,ast.AnnAssign) and isinstance(node.target,ast.Name):
            rows[node.target.id]=node
    return rows

def write_new(name,data):
    path=DEST/name
    with path.open('xb') as f:f.write(data)
    return dict(path=str(path),sha256=sha(data),size_bytes=len(data),identity7=identity(path))

def write_json(name,value):
    return write_new(name,(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())

def main():
    if sys.argv[1:] != ['--generate-unready-source-only']:
        raise SystemExit('Only --generate-unready-source-only is accepted. Future actual helper Q binding is deferred; no READY branch exists.')
    inputs=[]
    oldraw,p = source_read(PARENT,PARENT_SHA); inputs.append(p)
    protraw,p = source_read(PROTO,PROTO_SHA); inputs.append(p)
    proofraw,p = source_read(PROTO_PROOF,PROTO_PROOF_SHA); inputs.append(p)
    reviewraw,p = source_read(PROTO_REVIEW); inputs.append(p)
    old=oldraw.decode('utf-8'); proto=protraw.decode('utf-8')
    pp=json.loads(proofraw); review=json.loads(reviewraw)
    if (pp['parent']['sha256'] != PARENT_SHA or pp['candidate']['sha256'] != PROTO_SHA
        or pp['inverse_whole_bytes_exact'] is not True or pp['definitions'] != 70
        or pp['changed_definitions'] != ['strict_json_bytes']
        or review['candidate']['sha256'] != PROTO_SHA
        or review['execution_scope']['project_source_executed'] is not False):
        raise ValueError('fixed independently reviewed SOURCE prototype differs')
    forward=old
    for e in pp['changes']:
        if e['count'] != 1 or forward.count(e['old']) != 1:
            raise ValueError('prototype finite region not unique')
        forward=forward.replace(e['old'],e['new'],1)
    if forward != proto or sha(forward.encode()) != PROTO_SHA:
        raise ValueError('entire prototype is not exact two-hunk derivation')
    edits=[]
    def edit(name,oldpart,newpart):
        nonlocal forward
        if forward.count(oldpart) != 1:
            raise ValueError('nonunique counted SOURCE edit: '+name)
        forward=forward.replace(oldpart,newpart,1)
        edits.append(dict(name=name,old=oldpart,new=newpart,count=1))
    # Include exact reviewed decoder edits first, then finite path/UNREADY binding only.
    forward=old
    for i,e in enumerate(pp['changes']):
        edit('reviewed_strict_reader_lifetime_'+str(i+1),e['old'],e['new'])
    olddoc=source_segment(old,ast.parse(old).body[0])
    edit('truthful_UNREADY_design_doc',olddoc,repr(NEW_DOC)+'\n')
    for name in ('SOURCE','OUT','TERMINAL','FAMILY','PREFIX','FORMAL_FACTORY'):
        node=globals_by_name(old)[name]
        segment=source_segment(old,node)
        replacement=segment.replace('v20','v21').replace('V20','V21')
        if replacement == segment: raise ValueError('missing fixed version binding')
        edit('fixed_fresh_V21_'+name,segment,replacement)
    edit('UNREADY_status',
         "DRAFT_STATUS = 'READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'\n",
         "DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_PRIVATE_VERIFIER_FORMAL_FACTORY'\n")
    edit('require_ready_version_only',
         "    if DRAFT_STATUS != 'READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':\n",
         "    if DRAFT_STATUS != 'READY_REVIEWED_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':\n")
    edit('future_private_helper_path_and_unbound_SHA',
         " 'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py','bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),\n",
         " 'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',None),\n")
    edit('new_helper_actual_qualification_unbound',
         "FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = 'd49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'\n",
         "FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None\n")
    candidate=forward
    # Complete inverse, not a hash-only or selected-fields comparison.
    inverse=candidate
    for e in reversed(edits):
        if inverse.count(e['new']) != 1: raise ValueError('nonunique full inverse region')
        inverse=inverse.replace(e['new'],e['old'],1)
    if inverse != old or sha(inverse.encode()) != PARENT_SHA:
        raise ValueError('full V21 -> complete V20 whole-byte inverse differs')
    olddefs=topdefs(old); newdefs=topdefs(candidate)
    if list(olddefs) != list(newdefs) or len(olddefs) != 70:
        raise ValueError('entire original top-level definition inventory differs')
    definition_rows=[]
    for name,node in olddefs.items():
        before=source_segment(old,node)
        after=source_segment(candidate,newdefs[name])
        if name=='strict_json_bytes':
            if after != source_segment(proto,topdefs(proto)[name]):
                raise ValueError('strict reader must equal independently reviewed complete prototype function')
            normalization='reviewed two lifetime edits only'
        else:
            normalized=after.replace('READY_REVIEWED_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY',
                                     'READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
            if normalized != before:
                raise ValueError('original definition bytes changed outside approved decoder/version: '+name)
            normalization='require_ready version-only' if after != before else 'byteexact'
        # Decoder original checks, raises, assertions and returns remain AST exact.
        for typ,label in ((ast.If,'if_tests'),(ast.Raise,'raises'),(ast.Assert,'asserts'),(ast.Return,'returns')):
            def controls(n):
                return [dump(x.test) if typ is ast.If else dump(x) for x in ast.walk(n) if isinstance(x,typ)]
            oc,nc=controls(node),controls(newdefs[name])
            if name=='require_ready':
                nc=[x.replace('READY_REVIEWED_V21_','READY_REVIEWED_V20_') for x in nc]
            if oc != nc: raise ValueError('original '+label+' differs: '+name)
        definition_rows.append(dict(name=name,original_sha256=sha(before.encode()),candidate_sha256=sha(after.encode()),
                                    proof=normalization,original_control_sequence_unchanged=True))
    oldg=globals_by_name(old); newg=globals_by_name(candidate)
    allowed={'SOURCE','OUT','TERMINAL','FAMILY','DRAFT_STATUS','PREFIX','FORMAL_FACTORY',
             'INPUT_HELPERS','FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'}
    if list(oldg) != list(newg): raise ValueError('original global inventory changed')
    global_rows=[]
    for name,node in oldg.items():
        changed=dump(node) != dump(newg[name])
        if changed and name not in allowed:
            raise ValueError('unapproved original physics/input/budget global changed: '+name)
        if name in allowed and not changed:raise ValueError('expected fixed binding missing: '+name)
        global_rows.append(dict(name=name,original_AST_sha256=sha(dump(node).encode()),
                                candidate_AST_sha256=sha(dump(newg[name]).encode()),changed=changed,
                                role='finite UNREADY/fresh namespace only' if changed else 'entire original global AST exact'))
    future_names=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA',
        'FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA',
        'FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
    for name in future_names+('FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA',):
        if not isinstance(newg[name].value,ast.Constant) or newg[name].value.value is not None:
            raise ValueError('unknown future success pin must remain None')
    ih=newg['INPUT_HELPERS'].value
    graph=[v for k,v in zip(ih.keys,ih.values) if isinstance(k,ast.Constant) and k.value=='graph']
    if len(graph)!=1 or not isinstance(graph[0].elts[1],ast.Constant) or graph[0].elts[1].value is not None:
        raise ValueError('new graph helper SHA must remain None')
    # All nondefinition nodes differ only by the explicit doc/globals listed above.
    def nondefs(text):
        return [n for n in ast.parse(text).body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    aa=nondefs(old); bb=nondefs(candidate)
    if len(aa)!=len(bb):raise ValueError('original nondefinition inventory changed')
    for i,(a,b) in enumerate(zip(aa,bb)):
        if dump(a)==dump(b):continue
        if i==0 and isinstance(a,ast.Expr) and isinstance(b,ast.Expr):continue
        names=[k for k,v in oldg.items() if v is a]
        # Nodes above came from a distinct AST; use original source line matching.
        names=[k for k,v in oldg.items() if v.lineno==a.lineno]
        if not names or not set(names)<=allowed:raise ValueError('original module executable SOURCE changed')
    compile(candidate,str(DEST/CANDIDATE_NAME),'exec',dont_inherit=True,optimize=0)
    # AST Call order is unchanged outside the identical original JSON-load argument handoff.
    for name,node in olddefs.items():
        before=[dump(x) for x in ast.walk(node) if isinstance(x,ast.Call)]
        after=[dump(x) for x in ast.walk(newdefs[name]) if isinstance(x,ast.Call)]
        if name=='strict_json_bytes':
            # AST walk changes only order of the original raw.decode call when lifted.
            before_loads=[dump(x) for x in ast.walk(node) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and dump(x.func)==dump(ast.parse('json.loads').body[0].value)]
            after_loads=[dump(x) for x in ast.walk(newdefs[name]) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and dump(x.func)==dump(ast.parse('json.loads').body[0].value)]
            if len(before_loads)!=1 or len(after_loads)!=1:raise ValueError('one original full loads call required')
            if len(before)!=len(after):raise ValueError('decoder original call count differs')
        elif before!=after:raise ValueError('original call AST sequence changed: '+name)
    # Repeat each complete fixed SOURCE read after all static checks.
    for p in inputs:
        _,fresh=source_read(Path(p['path']),p['sha256'])
        if fresh!=p:raise ValueError('full SOURCE before/after identity differs')
    parentpin=write_new('frozen_complete_parent_V20_566939.SOURCE.py',oldraw)
    protopin=write_new('frozen_reviewed_strict_decode_prototype_f229.SOURCE.py',protraw)
    candidatepin=write_new(CANDIDATE_NAME,candidate.encode())
    proof=dict(schema='AXMAT_V21_COMPLETE_RUNTIME_UNREADY_FINITE_SOURCE_INVERSE_V1',
        status='SOURCE_ONLY_UNREADY_NO_NEW_HELPER_QUALIFICATION',parent=inputs[0],candidate=candidatepin,
        complete_parent_snapshot=parentpin,reviewed_complete_decode_prototype=protopin,
        edits=edits,finite_edit_count=len(edits),full_inverse_whole_bytes_exact=True,inverse_sha256=PARENT_SHA,
        original_top_level_definitions=70,all_definition_names_and_order_exact=True,
        non_decoder_definition_count=69,non_decoder_68_bytes_exact=True,
        require_ready_only_original_Ready_version_string_retarget=True,
        strict_json_bytes_identical_reviewed_prototype_function=True,
        definition_inventory=definition_rows,global_inventory=global_rows,
        all_original_imports_and_other_module_executable_AST_exact=True,
        all_original_if_tests_raises_asserts_returns_preserved_except_Ready_version=True,
        original_call_sequences_preserved_except_reviewed_decode_argument_handoff=True,
        full_SOURCE_inputs_before_after=inputs,
        business_project_helper_guard_executed=False,helper_Q_read=False,ART_or_numeric_payload_read=False,
        canonical_or_frozen_or_results_changed=False)
    proofpin=write_json('full_finite_source_inverse_proof.json',proof)
    plan=dict(schema='AXMAT_V21_FUTURE_ACTUAL_HELPER_SOURCE_BINDING_PLAN_V1',
        status='UNREADY_FUTURE_ACTUAL_CONTRACT_DEFERRED',candidate=candidatepin,
        future_binding_parameters=['Root actual helper qualification summary path','Root actual helper qualification summary SHA256'],
        accepted_actual_qualification_schema=None,accepted_actual_qualification_status=None,
        new_helper_path_context=NEW_HELPER_PATH,new_helper_SOURCE_context_sha256=NEW_HELPER_SOURCE_CONTEXT_SHA,
        new_helper_SOURCE_context_bytes=NEW_HELPER_SOURCE_CONTEXT_BYTES,
        new_helper_qualification_sha256=None,new_helper_qualification_identity7=None,
        future_actual_helper_source_path=None,future_actual_helper_source_sha256=None,
        future_actual_helper_source_bytes=None,future_actual_helper_source_identity7=None,
        mandatory_future_evidence=['Root actual original pure protocol controls typed integer EXIT0 CLOSED',
            'Root actual complete current graph fresh verifier typed integer EXIT0 CLOSED',
            'saved independent review of both full metadata results',
            'actual installed canonical helper SOURCE exact SHA/bytes/7ID and unchanged EOF reread',
            'actual Q exact full EOF SHA/7ID plus genuine Q schema/status/fields supplied by Root',
            'all science/native/combined claims false until their own actual qualification'],
        ready_binding_not_implemented_or_executed=True,no_Q_read=True,
        minimal_future_runtime_changes_after_actual_evidence=['graph helper SHA None -> actual helper SHA',
            'helper controls admission SHA None -> actual Q SHA',
            'UNREADY doc/status -> truthful independently reviewed SOURCE_READY doc/status'],
        retain_unmodified=['all original 70 definitions except the approved strict decode lifetime source',
            'full PREP and complete five build stages and whole INPUT logic',
            'all original physics/component actual pins and all historical seven-key bodies',
            'full graph trace namespaces aliases roots coverage and both complete fresh EOF reads',
            'all original guards MRO and resource archive checks'],
        original_limits=dict(whole_wall_seconds=1800,single_stage_wall_seconds=600,rss_mib=512,
            runtime_aggregate_archive_gib=2,whole_INPUT_stdout_metadata_mib=64,history_gib=96,free_floor_gib=8,
            thread_keys=5,threads_each=1,children=1,retries=0),
        future_business_pins={name:None for name in future_names},
        original_bcd_d490_not_reused_as_new_helper_qualification=True,
        source_review_grants_no_business_RSS_build_native_or_scientific_success=True)
    planpin=write_json('future_actual_helper_binding_contract.UNREADY.json',plan)
    report=dict(schema='AXMAT_V21_COMPLETE_RUNTIME_SOURCE_ONLY_REPORT_V1',
        status='COMPLETE_SOURCE_GENERATED_UNREADY_FOR_ANY_BUSINESS',candidate=candidatepin,
        full_inverse=proofpin,future_binding_contract=planpin,
        scope='Only fixed SOURCE bytes, standard-library AST/compile/hash; no project import/execution, Q or ART data read.',
        changes=[e['name'] for e in edits],top_level_definitions=70,non_decoder_definitions=69,
        source_only_original70_definitions_complete=True,
        last_use_rationale='UTF8 text is complete before raw ends; decoded ends only after original full JSON parse. Full finite checks/return remain identical. New helper lifetime design awaits actual qualification.',
        limits='No actual RSS peak line, measured savings or future PASS is established; no business or scientific credit.',
        future_actual_helper_Q_sha=None,all_six_future_business_pins=None,
        original_all_physics_global_AST_preserved=True,original_caps_and_full_scope_unchanged=True,
        all_input_SOURCE_pins_before_after=inputs)
    reportpin=write_json('SOURCE_REPORT.json',report)
    text=('已生成完整 V21 UNREADY SOURCE，完整 inverse 逐字节回 V20 566939。\n'
          '仅 13 个有限修改：已审两处 strict decode lifetime、fresh V21 family/path/schema、doc/status/Ready 版本、'
          '新 helper 设计路径及两个未知资格 SHA 的 None。\n'
          '全部 70 个原定义保留：68 个逐字节不变，require_ready 仅版本字串，strict_json_bytes 等于已审 prototype。'
          '全部原物理/component pins、五阶段/whole INPUT/完整 trace/两次完整 fresh EOF/原 guard 与 caps 保留。\n'
          '当前生成器只接受 --generate-unready-source-only，没有 READY 绑定分支。'
          '新 Q 字段与真实两项成功/独审尚未提供，因此未知 schema/Q SHA/7ID 都为空；不读取新 Q。\n'
          '仅 SOURCE 标准库静态工作；无项目/helper/guard/API 执行、无 ART/数值/历史读取、无 canonical/results 修改，'
          '没有实际 RSS/构建/native/AAA/ABA 成功信用。\n')
    write_new('REPORT.txt',text.encode())
    print(json.dumps(dict(status=report['status'],candidate=candidatepin,proof=proofpin,plan=planpin,report=reportpin,
        finite_edits=len(edits),top_level_definitions=70,actual_Q_read=False,business_executed=False),ensure_ascii=False))

if __name__ == '__main__':
    main()
