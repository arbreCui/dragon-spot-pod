"""Generate source-only complete-graph memory candidates; execute no project API."""
import ast
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).parent
A = Path('/Users/wen/spot/validation/axial_material')
F = A/'prepare_sender_window_root_index_graph_table_combined_runtime_v15.py'
G = A/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
EXPECTED = {str(F): '0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382',
            str(G): 'e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'}

def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
    s = p.lstat()
    return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,
                size_bytes=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def pin(p):
    before=identity(p);data=p.read_bytes();after=identity(p)
    assert before==after
    return dict(path=str(p),sha256=sha(data),size_bytes=len(data),identity=before)
def write(name,data):
    with (OUT/name).open('xb') as f: f.write(data)
def document(name,obj): write(name,(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
def functions(text):
    lines=text.splitlines(keepends=True)
    return {n.name: ''.join(lines[n.lineno-1:n.end_lineno]) for n in ast.parse(text).body
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
before={str(p):pin(p) for p in (F,G)}
for p,wanted in EXPECTED.items(): assert before[p]['sha256']==wanted
f=F.read_text();g=G.read_text()

# Caller-only last-use candidate. Original guard calls and their order remain.
old_func=functions(f)['create_complete_input_graph']
edits=[]
caller=old_func
def edit(old,new):
    global caller
    assert caller.count(old)==1,old
    edits.append(dict(old=old,new=new));caller=caller.replace(old,new)
edit("    del expanded['owners'],expanded['namespace_specs'];del requirements,actual,new_pins,fresh,audit;gc.collect()",
     "    # Whole expanded JSON already passed the original byte/codec equality.\n"
     "    # These are exactly the existing current predicate/length-check fields.\n"
     "    expanded=minimal_live_specs({'metadata':expanded})\n"
     "    trim_binding=trim['binding']\n"
     "    del trim,trim_alias_paths,before\n"
     "    del failed['files']\n"
     "    del requirements,actual,new_pins,fresh,audit;gc.collect()")
edit("prior_failed_PREP_input=failed['binding'],actual_last_cprime_trim_component_INPUT=trim['binding']",
     "prior_failed_PREP_input=failed['binding'],actual_last_cprime_trim_component_INPUT=trim_binding")
rev=caller
for row in reversed(edits):
    assert rev.count(row['new'])==1
    rev=rev.replace(row['new'],row['old'])
assert rev==old_func
caller_full=f.replace(old_func,caller)
compile(caller_full,'caller_last_use.UNREADY.py','exec')
fc=functions(caller_full)
assert all(fc[k]==v for k,v in functions(f).items() if k!='create_complete_input_graph')
write('caller_last_use.UNREADY.py',caller_full.encode())
write('caller_last_use_function.py.txt',caller.encode())

# Separate new API. Every parent function, including the ordinary and consumer
# APIs, stays byte-for-byte intact. This API is for a new fresh whole producer.
sort_owned='''def _sort_new_owned_graph_json_in_place(value):
    """Sort only the new producer's private JSON containers; no caller data."""
    if type(value) is dict:
        entries = [(key, value[key]) for key in sorted(value)]
        value.clear()
        for key, part in entries:
            _sort_new_owned_graph_json_in_place(part)
            value[key] = part
    elif type(value) is list:
        for part in value:
            _sort_new_owned_graph_json_in_place(part)


'''
old_create=functions(g)['create_graph']
fresh=old_create
fresh_edits=[]
def fresh_edit(old,new):
    global fresh
    assert fresh.count(old)==1,old
    fresh_edits.append(dict(old=old,new=new));fresh=fresh.replace(old,new)
fresh_edit('def create_graph(', 'def create_fresh_complete_wire_graph(')
fresh_edit('    normalized_owners = _owners(owners)',
           '    _require(consumer_scope is None, "fresh complete producer cannot declare consumer scope")\n'
           '    normalized_owners = _owners(owners)')
fresh_edit('json_input=None if consumer is None else consumer["parent_input_graph"])',
           'json_input=None if consumer is None else consumer["parent_input_graph"],\n'
           '                                           compact_requirements=True)')
fresh_edit('coverage = (_coverage if consumer is None else _consumer_coverage)(requirements, actual, contract)',
           'coverage = (_coverage if consumer is None else _consumer_coverage)(\n'
           '        _compact_requirement_dicts(requirements), actual, contract)')
fresh_edit('trace_coverage = _trace_coverage(traces, requirements, normalized_namespaces,',
           'trace_coverage = _trace_coverage(traces, _compact_requirement_dicts(requirements), normalized_namespaces,')
fresh_edit('    requirement_table = _requirement_table(requirements)',
           '    requirement_table = _wire_requirement_table_compact(requirements)\n'
           '    _validate_wire_requirement_table(requirement_table)\n'
           '    del requirements')
fresh_edit('"schema": SCHEMA if consumer is None else CONSUMER_SCHEMA, "scope": INPUT_SCOPE,',
           '"schema": WIRE_GRAPH_SCHEMA, "scope": INPUT_SCOPE,')
fresh_edit('    graph["content_sha256"] = _content_digest(graph)\n    return graph',
           '    # Canonical key insertion order matches original encode_graph_wire,\n'
           '    # without cloning the complete new graph (all containers are owned).\n'
           '    graph["content_sha256"] = None\n'
           '    _sort_new_owned_graph_json_in_place(graph)\n'
           '    graph["wire_encoding"] = {"schema": WIRE_ENCODING_SCHEMA, "source_graph_schema": SCHEMA,\n'
           '        "source_requirement_table_schema": REQUIREMENT_TABLE_SCHEMA,\n'
           '        "decoded_content_sha256": _wire_semantic_content_digest(dict(graph, wire_encoding=None))}\n'
           '    graph["content_sha256"] = _content_digest(graph)\n'
           '    return graph')
rev=fresh
for row in reversed(fresh_edits):
    assert rev.count(row['new'])==1
    rev=rev.replace(row['new'],row['old'])
assert rev==old_create
helper=g+'\n\n'+sort_owned+fresh+'\n'
compile(helper,'fresh_complete_wire_helper.UNREADY.py','exec')
gf=functions(g);hf=functions(helper)
assert all(hf[k]==v for k,v in gf.items())
assert helper[:len(g)]==g
write('fresh_complete_wire_helper.UNREADY.py',helper.encode())
write('fresh_complete_wire_function.py.txt',(sort_owned+fresh+'\n').encode())

last_uses=[
    dict(value='before',last_original_use='assignment 2063; no later load',change='delete after original predicate call has occurred'),
    dict(value='trim_alias_paths',last_original_use='capture_aliases at 2053',change='delete before wire generation'),
    dict(value="trim['files']/trim['namespaces']/trim['support_owners']",last_original_use='2050/2060 owner/namespace normalization',change="retain exact trim['binding']; delete redundant trim dict only after original first full phase and checks",ownership_proof='_owners creates fresh expected_files dict; explicit_sealed_namespace creates files dict and graph_trim_namespaces returns fresh descriptors'),
    dict(value="failed['files']",last_original_use='2048 normalized owner creation',change="delete only files; preserve namespaces, sizes and binding for both original checks"),
    dict(value='expanded whole metadata',last_original_use='2067 whole codec.pack_specs==fresh.parsed; 2068 lengths + 2079 current predicate',change='only after all whole checks retain four existing minimal_live_specs fields; all later callees read only these',retained_fields=['reached_component_records','independent_directory_owners','remaining_source_owned_requirements','aliases']),
    dict(value='caller trace',last_original_use='create graph input; saved whole trace remains immutable',change='retained without consume in this minimal candidate',limitation='new producer still normalizes/clones trace once; this candidate does not claim zero trace duplication'),
]
inputs=[A/'combined_runtime_typed_specs_codec.py',A/'combined_runtime_historical_input_checks.py',
        A/'combined_runtime_current_predicates_final_private_last_uses_20261009.py']
support=[pin(p) for p in inputs]
after={str(p):pin(p) for p in (F,G)}
assert before==after
proof=dict(schema='AXMAT_FULL_GRAPH_FRESH_WIRE_MEMORY_SOURCE_INVERSE_V1',status='SOURCE_ONLY_UNREADY',
    parents=before,parent_before_after_equal=True,caller_edits=edits,caller_complete_inverse_equal=True,
    caller_other_definitions_exact=len(functions(f))-1,new_helper_additive_region_only=True,
    helper_all_parent_function_and_class_segments_exact=len(gf),fresh_producer_edits=fresh_edits,
    fresh_producer_inverse_to_parent_create_graph_exact=True,source_compile_only=True,
    no_project_module_import_or_call=True,no_fixture_or_business_execution=True)
document('source_inverse_proof.json',proof)
report=dict(schema='AXMAT_V15_COMPLETE_GRAPH_MEMORY_LAST_USE_SOURCE_PLAN_V1',status='SOURCE_ONLY_UNREADY',
    observed_root_failure=dict(initial_chunk='4c0c67',session_id=58797,terminal_chunk='c14020',exit_code=1,
                              rss_peak_mib=513.40625,child_returncode=-15,qualification=False),
    failure_line_localization=False,source_inputs=before,support_source_inputs=support,last_uses=last_uses,
    fresh_producer=dict(api='create_fresh_complete_wire_graph',whole_fresh_phase=True,
        full_owner_and_namespace_normalization=True,compact_requirements_private_tuples=True,
        unchanged_coverage_bodies_with_ephemeral_builtin_dicts=True,all_trace_records_retained=True,
        legacy_semantic_digest_streamed=True,wire_content_digest_streamed=True,
        private_owned_container_key_order_canonicalization=True,whole_graph_clone_removed=True,
        original_create_graph_encode_graph_wire_verify_graph_and_consumer_apis_exact=True),
    storage=dict(MAX_JSON_BYTES=64*2**20,changed=False,V12_stored_observed_bytes=66558943,
                 V12_margin_bytes=549921,V15_trace_observed_bytes=40915887,
                 V15_api_trace_observed_bytes=16870925,new_graph_stored_bytes=None,
                 new_stored_under_cap_verified=False,
                 note='Memory lifetime change alone cannot guarantee wire file below original cap. Root is independently measuring exact full metadata storage. No trace pruned or new graph claimed.'),
    required_next_controls=['ordinary create_graph vs fresh complete wire full decoded values/type/order/floatbits/digests equality in isolated pure fixture',
        'duplicates/roles/namespaces/aliases/absence/new-input edges and malformed guard priority compatibility',
        'private in-place canonicalization never mutates original caller graph/owners/ns/trace',
        'all whole actual trace and table stored size below original 67108864; if not explicit lossless trace storage codec is a separate necessary source change'],
    budgets_unchanged=True,project_written=False,fixtures_run=False,business_imported_or_called=False,
    runtime_RSS_or_build_or_INPUT_or_native_or_AAA_or_ABA_credit=False)
document('REPORT.json',report)
write('REPORT.txt',('源码定位完成；正式 V15 PREP 实际失败，未形成 graph/declaration。\n'
    '最小调用者修改只释放已完成完整 byte/codec/predicate 检查后不再使用的返回和重复映射；全部图数据、原追踪和后续谓词仍保留。\n'
    '独立 fresh complete wire SOURCE 草稿使用原 compact requirements 与原完整 coverage/trace 检查，流式旧语义摘要，再计算 wire 摘要，避免整图 clone 和整套 int rows。旧公开与 consumer 函数逐字不变。\n'
    '两份仅 UNREADY SOURCE；未运行任何项目函数/fixture/数值/资源扫描。没有实际 RSS 收益、图成功或 INPUT/native/AAA/ABA 信用。\n'
    '仍须完整纯元数据等值/异常/所有权控制与实际 storedbytes 验证；原 64MiB 门保留。当前新图尚不存在，不将内存方案等同解决 JSON cap。\n').encode())
products=['caller_last_use.UNREADY.py','caller_last_use_function.py.txt','fresh_complete_wire_helper.UNREADY.py',
          'fresh_complete_wire_function.py.txt','source_inverse_proof.json','REPORT.json','REPORT.txt']
print(json.dumps(dict(status='SOURCE_ONLY_UNREADY',files=[pin(OUT/name) for name in products]),separators=(',',':')))
