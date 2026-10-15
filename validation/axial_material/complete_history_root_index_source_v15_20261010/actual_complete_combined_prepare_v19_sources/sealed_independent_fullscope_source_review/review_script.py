"""Bounded SOURCE/AST/text-only V19 review; never import/call any project/helper/business API."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import time

START=time.monotonic();OUT=Path(__file__).parent
ROOT=Path('/Users/wen/spot/validation/axial_material')
AUTHOR=Path('/private/tmp/axmat_v19_complete_prepare_caller_last_use_source_only_20261010')
PARENT=ROOT/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'
CANDIDATE=AUTHOR/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py'
checks={};pins={};texts={}
def check(k,v):
    checks[k]=bool(v)
    if not v:raise ValueError(k)
def read(path,want=None):
    path=Path(path);before=path.stat();raw=path.read_bytes();after=path.stat();keys=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
    check('full_SOURCE_EOF_and7ID:'+str(path),len(raw)==before.st_size and all(getattr(before,k)==getattr(after,k) for k in keys))
    sha=hashlib.sha256(raw).hexdigest()
    if want:check('fixed_SOURCE_SHA:'+str(path),sha==want)
    pins[str(path)]={'sha256':sha,'size_bytes':len(raw),'before7ID':{k:getattr(before,k) for k in keys},'after7ID':{k:getattr(after,k) for k in keys}}
    texts[str(path)]=raw.decode();return texts[str(path)]
def parse_json(path,want=None):return json.loads(read(path,want))
def defs(tree):return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def names(tree):return {t.id:n for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
def dump(n):return ast.dump(n,include_attributes=False)
def order_nodes(node,types):return sorted((n for n in ast.walk(node) if isinstance(n,types)),key=lambda n:(n.lineno,n.col_offset))
def calls(node,exclude=()):return [dump(n) for n in order_nodes(node,ast.Call) if ast.unparse(n.func) not in exclude]
def uses(function,name):return [{'line':n.lineno,'column':n.col_offset,'ctx':type(n.ctx).__name__} for n in order_nodes(function,ast.Name) if n.id==name]
def helper_fields(function,param):
    return sorted({n.slice.value for n in ast.walk(function) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id==param and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str)})
def protect(node,normalize_ready=False):
    n=copy.deepcopy(node)
    if normalize_ready:
        for x in ast.walk(n):
            if isinstance(x,ast.Constant) and x.value=='READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':x.value='READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
    return dump(n)

review={'schema':'AXMAT_V19_INDEPENDENT_FINITE_COMPLETE_SOURCE_REVIEW_V1','scope':'COMPLETE_SOURCE_AST_TEXT_INVERSE_AND_LAST_USE_PROOF_ONLY','project_helper_imported_or_called':False,'business_API_called':False,'business_executed':False,'numeric_payload_read':False,'ART_read_or_written':False,'canonical_or_project_written':False,'resource_helper_called':False,'source_line_RSS_cause_observed':False,'actual_RSS_pass_proved':False,'future_PASS_predicted':False,'blocking_findings':[]}
try:
    parent=read(PARENT,'5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240')
    new=read(CANDIDATE,'585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50')
    check('parent180102_candidate180475_bytes',len(parent.encode())==180102 and len(new.encode())==180475)
    proof=parse_json(AUTHOR/'source_inverse_proof.json','c3927b04791aa00115f1ad661f6113de6992d5a93f165a3c8ea58586dccd6595')
    manifest=parse_json(AUTHOR/'sealed_manifest.json')
    check('sealed_author_five_member_SOURCE_package',manifest['member_count']==len(manifest['members'])==5)
    for member in manifest['members']:
        text=read(member['path'],member['sha256']);check('author_member_bytes:'+member['path'],len(text.encode())==member['size_bytes'])
    for item in proof['inputs']:
        source=read(item['path'],item['sha256']);check('pinned_finite_SOURCE_input_bytes:'+item['path'],len(source.encode())==item['size_bytes'])
    restored=new
    for i,edit in reversed(list(enumerate(proof['edits']))):
        check('unique_whole_inverse_region:'+str(i),restored.count(edit['new'])==edit['occurrences'])
        restored=restored.replace(edit['new'],edit['old'],edit['occurrences'])
    check('full_byte_inverse_to_actual_V18_5c4b',restored==parent)
    pt=ast.parse(parent);nt=ast.parse(new);pd=defs(pt);nd=defs(nt)
    check('same70_original_top_definitions',list(pd)==list(nd) and len(pd)==70)
    changed=[name for name in pd if ast.get_source_segment(parent,pd[name])!=ast.get_source_segment(new,nd[name])]
    check('only_require_ready_and_create_changed68_exact',changed==['require_ready','create_complete_input_graph'] and len(pd)-len(changed)==68)
    check('prepare_build_and_full_V18_complete_input_phase_byteexact',all(ast.get_source_segment(parent,pd[n])==ast.get_source_segment(new,nd[n]) for n in ('prepare_build','complete_input_phase')))
    pa=names(pt);na=names(nt);modified_global=[k for k in pa if dump(pa[k])!=dump(na[k])]
    check('only_fresh_family_globals_changed',set(pa)==set(na) and set(modified_global)=={'SOURCE','OUT','TERMINAL','FAMILY','PREFIX','FORMAL_FACTORY','DRAFT_STATUS'})
    check('six_future_success_pins_None',all(ast.literal_eval(na[k].value) is None for k in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')))
    check('truthful_UNREADY_not_constructor_admitted',ast.literal_eval(na['DRAFT_STATUS'].value)=='UNREADY_SOURCE_ONLY_V19_PREP_CALLER_LAST_USE_REVIEW_REQUIRED' and "if DRAFT_STATUS != 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':" in ast.get_source_segment(new,nd['require_ready']))
    check('graph_bcd_and_admission_d490_bindings_unmodified',dump(pa['INPUT_HELPERS'])==dump(na['INPUT_HELPERS']) and dump(pa['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])==dump(na['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']))
    protections={}
    for name in pd:
        old=order_nodes(pd[name],(ast.If,ast.Assert,ast.Raise));now=order_nodes(nd[name],(ast.If,ast.Assert,ast.Raise))
        check('all_original_If_Assert_Raise_order:'+name,[protect(n) for n in old]==[protect(n,name=='require_ready') for n in now])
        protections[name]={'If':sum(isinstance(n,ast.If) for n in old),'Assert':sum(isinstance(n,ast.Assert) for n in old),'Raise':sum(isinstance(n,ast.Raise) for n in old)}
    oldc=pd['create_complete_input_graph'];newc=nd['create_complete_input_graph']
    check('all_create_nonlifetime_call_AST_order_exact',calls(oldc,('minimal_live_specs',))==calls(newc,('minimal_live_specs',)))
    check('three_original_gc_calls_no_added_collectors',sum(ast.unparse(n.func)=='gc.collect' for n in ast.walk(oldc) if isinstance(n,ast.Call))==sum(ast.unparse(n.func)=='gc.collect' for n in ast.walk(newc) if isinstance(n,ast.Call))==3)
    # Collector boundaries expressed by all non-minimal call AST indices are exact,
    # not by shifted line numbers: the above whole sequence includes gc.collect.
    check('whole_codec_If_AST_exact_before_minimal',dump(next(n for n in order_nodes(oldc,ast.If) if 'codec.pack_specs' in ast.unparse(n.test)))==dump(next(n for n in order_nodes(newc,ast.If) if 'codec.pack_specs' in ast.unparse(n.test))))
    use_witness={n:{'parent':uses(oldc,n),'candidate':uses(newc,n)} for n in ('requirements','new_pins','fresh','actual','audit','expanded','trim','trim_alias_paths','before','owners','namespaces','aliases','trace','failed')}
    for name in ('requirements','new_pins','fresh','actual','audit','trim','trim_alias_paths','before'):
        rows=use_witness[name]['candidate'];drops=[r['line'] for r in rows if r['ctx']=='Del'];loads=[r['line'] for r in rows if r['ctx']=='Load']
        check('true_last_use_before_delete:'+name,len(drops)==1 and (not loads or max(loads)<drops[0]))
    check('requirements_no_parent_or_candidate_caller_consumer',not any(r['ctx']=='Load' for r in use_witness['requirements']['parent']+use_witness['requirements']['candidate']))
    minimalcall=next(n for n in order_nodes(newc,ast.Call) if ast.unparse(n.func)=='minimal_live_specs')
    codeceq=next(n for n in order_nodes(newc,ast.If) if 'codec.pack_specs' in ast.unparse(n.test))
    check('full_specs_codec_equality_finishes_before_fourfield_selection',codeceq.end_lineno<minimalcall.lineno)
    minimal=pd['minimal_live_specs'];literal_tuple=next(n for n in ast.walk(minimal) if isinstance(n,ast.Tuple) and all(isinstance(x,ast.Constant) for x in n.elts));selected=tuple(x.value for x in literal_tuple.elts)
    check('all_original_four_minimal_fields_exact',selected==('reached_component_records','independent_directory_owners','remaining_source_owned_requirements','aliases') and dump(minimal)==dump(nd['minimal_live_specs']))
    helper_pins={'graph':('combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py','bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),'codec':('combined_runtime_typed_specs_codec.py','758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69'),'current':('combined_runtime_current_predicates_final_private_last_uses_20261009.py','fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19'),'checks':('combined_runtime_historical_input_checks.py','86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e'),'ordinary':('combined_runtime_current_ordinary_path_checks.py','47e7f9eb2e7ff89e96c30b91f98a25d37d66d82a029dcfbf4845c8f5968482d5')}
    hs={k:read(ROOT/path,sha) for k,(path,sha) in helper_pins.items()};hd={k:defs(ast.parse(s)) for k,s in hs.items()}
    dependencies={'check_current_predicate_subset':helper_fields(hd['current']['check_current_predicate_subset'],'specs'),'check_member_and_directory_predicates':helper_fields(hd['checks']['check_member_and_directory_predicates'],'specs'),'check_failed_lengths_and_owned_negative_bytes':helper_fields(hd['checks']['check_failed_lengths_and_owned_negative_bytes'],'specs')}
    check('every_later_predicate_field_preserved',set().union(*(set(v) for v in dependencies.values()))=={'reached_component_records','independent_directory_owners','remaining_source_owned_requirements'} and all(set(v)<=set(selected) for v in dependencies.values()))
    for name in ('check_current_predicate_subset','check_member_and_directory_predicates','check_failed_lengths_and_owned_negative_bytes'):
        fn=hd['current'].get(name) or hd['checks'].get(name);parents={child:node for node in ast.walk(fn) for child in ast.iter_child_nodes(node)}
        check('callee_only_literal_specs_field_access:'+name,all(isinstance(parents[n],ast.Subscript) and parents[n].value is n and isinstance(parents[n].slice,ast.Constant) for n in ast.walk(fn) if isinstance(n,ast.Name) and n.id=='specs' and isinstance(n.ctx,ast.Load)))
    failed_fields=helper_fields(pd['check_failed_prepare_phase'],'failed');check('failed_checker_never_reads_deleted_flat_files',failed_fields==['namespaces'])
    ownersource=ast.get_source_segment(hs['graph'],hd['graph']['_owners']);nssource=ast.get_source_segment(hs['graph'],hd['graph']['explicit_sealed_namespace']);clonesource=ast.get_source_segment(hs['graph'],hd['graph']['_json_clone']);auditsource=ast.get_source_segment(hs['graph'],hd['graph']['ReadOpenAudit'])
    check('normalized_owners_independent_complete_expected_map', '"expected_files": {_path(path): _sha(digest) for path, digest in mapping.items()}' in ownersource)
    check('normalized_namespaces_copy_complete_regular_and_symlink_maps','regular = {_relative(name): _sha(digest) for name, digest in files.items()}' in nssource and '"directories": sorted(expected_dirs)' in nssource)
    check('snapshot_independent_complete_records_subprocess_clone','"records": _json_clone(records)' in auditsource and '"subprocess_records": _json_clone(self._subprocess_records)' in auditsource and '_ACTIVE_TRACES.remove(self)' in auditsource and 'def __del__' not in auditsource)
    check('snapshot_clone_builtin_lists_dicts_finite_values','return {key: clone(item[key]) for key in sorted(item)}' in clonesource and 'return [clone(part) for part in item]' in clonesource)
    check('trim_binding_scalar_dictionary_retained_unmodified',"binding=dict(path=str(SOURCE/TRIM_INPUT_NAME),sha256=digest(SOURCE/TRIM_INPUT_NAME)," in ast.get_source_segment(parent,pd['trim_component_input']) and "trim_binding=trim['binding']" in ast.get_source_segment(new,newc))
    check('no_original_helper_function_or_API_replaced_or_monkeypatched',not any(isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.Lambda)) for n in ast.walk(newc) if n is not newc) and not any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Attribute) and isinstance(t.value,ast.Name) and t.value.id in ('g','codec','checks','helpers') for t in n.targets) for n in ast.walk(newc)))
    helpers_evidence={'_owners':ownersource,'explicit_sealed_namespace':nssource,'_json_clone':clonesource,'ReadOpenAudit':auditsource,'codec_pack_specs':ast.get_source_segment(hs['codec'],hd['codec']['pack_specs']),'codec_unpack_specs':ast.get_source_segment(hs['codec'],hd['codec']['unpack_specs']),'later_current_subset':ast.get_source_segment(hs['current'],hd['current']['check_current_predicate_subset']),'later_member_directory':ast.get_source_segment(hs['checks'],hd['checks']['check_member_and_directory_predicates']),'later_failed_lengths_negative_bytes':ast.get_source_segment(hs['checks'],hd['checks']['check_failed_lengths_and_owned_negative_bytes']),'failed_prepare_phase':ast.get_source_segment(parent,pd['check_failed_prepare_phase']),'trim_component_input':ast.get_source_segment(parent,pd['trim_component_input'])}
    with (OUT/'SOURCE_LAST_USE_AND_ALIAS_WITNESSES.json').open('x') as f:json.dump({'parent_and_candidate_use_sites':use_witness,'original_AST_protection_counts':protections,'complete_field_dependencies':dependencies,'minimal_original_four_fields':selected,'source_segments':helpers_evidence,'parent_create_complete_source':ast.get_source_segment(parent,oldc),'candidate_create_complete_source':ast.get_source_segment(new,newc)},f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    for path,pin in list(pins.items()):read(path,pin['sha256'])
    review.update(status='SOURCE_PASS_COMPLETE_V19_UNREADY_LAST_USE_ONLY_NO_RUNTIME_CREDIT',checks=checks,source_pins=pins,candidate_sha256='585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50',candidate_bytes=180475,parent_sha256='5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240',source_inverse_proof_sha256='c3927b04791aa00115f1ad661f6113de6992d5a93f165a3c8ea58586dccd6595',whole_inverse_byteexact=True,changed_definitions=changed,other68_original_definitions_byteexact=True,all_original_If_Assert_Raise_order_exact_except_new_ready_family_literal=True,all_create_nonminimal_call_AST_sequence_exact=True,original_gc_call_count_and_semantic_boundaries_exact=True,full_specs_codec_equality_before_minimal=True,V18_full_complete_input_phase_byteexact=True,prepare_build_byteexact=True,all_original_two_full_creation_phases_full_EOF_nine_closure_trace_namespaces_aliases_predicates_and_failed_lengths_retained=True,last_use_findings=['First-phase requirements has no caller Load and is released only after phase return; helper already used it to produce full canonical union and complete EOF checks.','new_pins/fresh end after original complete pack_specs equality. actual ends after both original first-phase length checks.','Expanded top dictionary is rebound to a new minimal dictionary containing the unchanged original four referenced values. Every subsequent predicate consumes only preserved literal fields; no source spec or public return is mutated.','Original _owners copies complete expected maps and original namespace descriptors copy full regular/link maps; trim and failed flat-map caller duplicates end after all complete construction. Independent scalar trim binding and complete failed namespace/size obligations remain.','Audit has exited active tracing before snapshot, whose complete records and subprocess records are independently JSON-cloned. Releasing inactive audit preserves full trace.','No added collector or changed source/helper/MRO/physics/cap branch. Future memory peak is unmeasured; source-level object liveness is not source-line RSS attribution.'],qualified_bcd_d490_and_original_component_bindings_unchanged=True,six_future_combined_native_success_pins_None=True,qualification={'complete_PREP_pass_obtained':False,'complete_build_pass_obtained':False,'whole_INPUT_admitted':False,'native_RSS_verified':False,'new_native_transport_executed':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False,'goal_complete':False},remaining_requirements=['Separate truthful Root READY binding and fresh bounded execution required.','Original actual V18 failure remains failed/closed; no rerun or success credit.','A source-line cause for V18 RSS excess was not observed; V19 RSS success must be measured under original512MiB and original1800/600/2GiB/history96GiB/free8GiB limits.'])
except BaseException as error:review.update(status='SOURCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE',error=repr(error),blocking_findings=[repr(error)],checks=checks,source_pins=pins)
review['source_only_seconds']=time.monotonic()-START
with (OUT/'REVIEW.json').open('x') as f:json.dump(review,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
report='V19完整SOURCE独立有限复核：'+review['status']+'\n完整候选585e /180475B与proof c392固定。整文件逆变换逐字恢复实际V18 5c4b；只有require_ready的V19门牌和create_complete_input_graph的真实caller last-use更改，其余68定义、prepare_build和已有V18完整INPUT阶段修正逐字不变。所有原If/Assert/Raise与非minimal调用序列、3个原gc边界、完整两阶段fullEOF、codec相等、全owner/namespace/alias/trace/9closure、原长度/current控制均保留。\n释放依据见源码现场：requirements无caller读取；完整codec相等后fresh/new_pins结束；actual在两长度检查后结束；audit snapshot完整独立clone且退出_ACTIVE_TRACES；trim/failed flat-map只在全normalize owner/namespace创建后结束，所需binding和完整failed namespace义务保留。minimal四字段保持原值引用，所有后续helper只读保留的三个字段。\n只SOURCE_PASS；候选仍UNREADY，未安装/调用helper/API/业务/数值载荷/资源检查，未读写ART或写规范源码。未观测V18 RSS具体源行原因，未证明或预测V19内存通过。原512MiB及1800/600/2GiB/history96/free8上限、6futureNone、bcd/d490均未改变；AAA/ABA/native/物理平衡及目标完成flag仍false。\n'
if review['blocking_findings']:report+='明确阻碍：'+repr(review['blocking_findings'])+'\n'
with (OUT/'REPORT.txt').open('x') as f:f.write(report)
raw=(OUT/'REVIEW.json').read_bytes();print(json.dumps({'status':review['status'],'directory':str(OUT),'review_sha256':hashlib.sha256(raw).hexdigest(),'review_bytes':len(raw),'source_checks':len(checks),'candidate_sha256':'585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50','business_helper_API_called':False,'numeric_payload_read':False,'ART_read_or_written':False,'RSS_pass_claimed':False},indent=2))
if review['blocking_findings']:raise SystemExit(1)
