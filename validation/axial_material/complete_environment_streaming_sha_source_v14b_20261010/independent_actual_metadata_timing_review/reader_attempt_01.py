"""Pure STDlib existing-evidence reader. No factory/helper import or API call."""
from pathlib import Path
from collections import Counter
import ast,hashlib,json,math,os,stat,struct,time,types
D=Path(__file__).parent
S=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010')
A=Path('/Users/wen/spot/validation/artifacts')
H=A/'axial-material-complete-environment-metadata-timing-host-v14b-20261010'
C=A/'axial-material-complete-environment-metadata-timing-v14b-20261010'
F=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py')
FUNCTIONS=['sender_source_admission','sender_control_contract','stream_environment_helper_source_admission','source_inputs']
SUPPORT=['require','read','pin','digest']
pins={}
def identity(path):
    x=Path(path).lstat();return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def pin(path,want=None,wanted_id=None):
    path=Path(path);before=identity(path);assert stat.S_ISREG(before[2]),str(path)
    value=sha(path);assert identity(path)==before,str(path)
    if want is not None:assert value==want,(str(path),value,want)
    if wanted_id is not None:assert before==wanted_id,str(path)
    rec=dict(path=str(path),sha256=value,size_bytes=before[4],identity=before);pins[str(path)]=rec;return rec
def unique(items):
    result={}
    for key,value in items:
        if key in result:raise ValueError('duplicate JSON key')
        result[key]=value
    return result
def read(path,want=None):
    pin(path,want);return json.loads(Path(path).read_text(),object_pairs_hook=unique,
        parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))
def exact(a,b):
    assert type(a) is type(b),(type(a),type(b))
    if isinstance(a,dict):
        assert list(a)==list(b),(list(a),list(b))
        for k in a:exact(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):exact(x,y)
    elif isinstance(a,float):assert struct.pack('>d',a)==struct.pack('>d',b)
    else:assert a==b,(a,b)
def namespace(root):
    result={}
    for parent,dirs,files in os.walk(root,followlinks=False):
        for name in sorted(dirs+files):
            path=Path(parent)/name;i=identity(path)
            kind='file' if stat.S_ISREG(i[2]) else 'dir' if stat.S_ISDIR(i[2]) else 'link' if stat.S_ISLNK(i[2]) else 'other'
            assert kind!='other';result[str(path.relative_to(root))]=dict(kind=kind,identity=i)
            if kind=='link':result[str(path.relative_to(root))]['readlink']=os.readlink(path)
    return result
def defs(text):
    return [ast.get_source_segment(text,n) for n in ast.walk(ast.parse(text)) if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
started=time.monotonic();ns_before={str(p):namespace(p) for p in [H,C]}
root=read(S/'actual_metadata_timing_receipts/Root_actual_metadata_timing_tool_terminal_return.json')
assert root['schema']=='AXMAT_V14B_READONLY_METADATA_ROOT_ACTUAL_TERMINAL_RECEIPT_V1'
assert root['initial_session_id']==2168 and root['session_closed'] is True
assert root['call_history'][0]['chunk_id']=='44597f' and root['terminal_result']['chunk_id']=='fd9c12'
assert type(root['terminal_result']['exit_code']) is int and root['terminal_result']['exit_code']==0
exact(root['call_history'][-1],root['terminal_result'])
for key in ['stdout','stderr','host_result','driver_result']:
    row=root[key];assert pin(row['path'],row['sha256'])['size_bytes']==row['size_bytes']
assert root['stderr']['size_bytes']==0
host=read(root['host_result']['path']);result=read(root['driver_result']['path'])
stdout=read(root['stdout']['path']);raw=read(C/'raw_preservation_manifest.json')
assert host['status']=='ACTUAL_BOUNDED_METADATA_DIAGNOSTIC_CLOSED_EXTERNAL_ROOT_REQUIRED'
assert result['status']=='READONLY_METADATA_PROFILE_COMPLETE_DIAGNOSTIC_ONLY'
assert stdout['status']==host['status'] and stdout['actual_external_Root_terminal_still_required'] is True
pin(stdout['host_result']['path'],stdout['host_result']['sha256'],stdout['host_result']['identity'])
assert stdout['host_result']['path']==str(H/'result.json')
for key in ['host_source','driver_source','target_factory']:pin(root[key]['path'],root[key]['sha256'])
pin(F,'4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c')
binding=read(S/'actual_metadata_control_sources/Root_complete_metadata_source_binding_inverse.json','ab08873f61f57ce6569b50ff4173ab245a1c347f38ec9b76a2eb808e61e59ab4')
for key,row in binding['bindings'].items():
    new=Path(row['candidate']['path']);old=Path(row['parent']['path'])
    pin(new,row['candidate']['sha256']);pin(old,row['parent']['sha256'])
    text=new.read_text()
    for edit in reversed(row['edits']):
        assert text.count(edit['new'])==edit['count'];text=text.replace(edit['new'],edit['old'])
    assert text==old.read_text() and defs(new.read_text())==defs(old.read_text())
assert {r['candidate']['path'] for r in binding['bindings'].values()}=={root['host_source']['path'],root['driver_source']['path']}
peer=read(S/'independent_metadata_diagnostic_source_review/REPORT.json')
assert peer['status']=='PASS_FINAL_BOUND_METADATA_DIAGNOSTIC_SOURCE_ONLY_REVIEW'
peerreceipt=read(S/'independent_metadata_diagnostic_source_review/READONLY_TOOL0_RECEIPT.json')
assert type(peerreceipt['exit_code']) is int and peerreceipt['exit_code']==0
assert json.loads(peerreceipt['output'])==peer
for row in host['input_sources']+[host['original_helper'],host['resource_factory'],host['actual_full_merged_stdout_stderr'],host['actual_child_result'],host['actual_watchdog']]:
    pin(row['path'],row['sha256'],row['identity'])
watch=read(H/'run/metadata.watchdog.json');exact(watch,host['watchdog'])
cmd=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',root['driver_source']['path'],'--out',str(C)]
exact(watch['command'],cmd);exact(host['actual_command'],cmd)
assert type(watch['returncode']) is int and watch['returncode']==0 and type(watch['pid']) is int and watch['pid']==73783
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['limit_failure'] is None
assert watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=120
assert watch['sampled_peak_rss_mib']==73.875
journal=read(H/'METADATA_TIMING/stages.json');exact(journal['stages'],host['stage_records']);assert len(journal['stages'])==1
stage=journal['stages'][0];assert stage['status']=='PASS' and stage['label']=='run/metadata'
exact(stage['command'],cmd);assert stage['log_sha256']==sha(H/'run/metadata.log')
assert watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=120
childstdout=read(H/'run/metadata.log')
assert childstdout['status']==result['status'] and childstdout['result_sha256']==sha(C/'result.json')
assert childstdout['Root_actual_child_terminal_required_before_admission'] is True
for key,value in dict(whole_wall_cap_seconds=120,rss_cap_mib=512,archive_cap_bytes=64*2**20,threads=1,children_at_once=1,retries=0).items():exact(host[key],value)
assert 0<result['elapsed_seconds']<watch['elapsed_seconds'] and 0<host['whole_elapsed_seconds']<120
assert host['whole_archive_bytes']<64*2**20
for snap in [host['resources_before'],stage['resource_before'],stage['resource_after'],host['resources_after']]:
    assert snap['min_free_bytes']==8*2**30 and snap['artifact_budget_bytes']==96*2**30
    assert snap['artifact_bytes']<96*2**30 and snap['disk_free_bytes']>=8*2**30
    assert snap['resource_roots']==snap['declared_resource_roots']==host['resource_roots']
    assert snap['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
assert host['resources_before']['artifact_bytes']+64*2**20<96*2**30
assert host['resources_before']['disk_free_bytes']-64*2**20>=8*2**30
for obj in [root,host,result]:
    for key in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:assert obj[key] is False
assert host['supervisor_class_or_MRO_modified'] is False and host['old_failed_V13_factory_imported_or_called'] is False
assert host['failed_V13_audit_reexecuted'] is False and host['numerical_component_or_transport_executed'] is False
assert result['prepare_build_run_build_audit_or_admit_called'] is False and result['numerical_controls_compiler_or_transport_executed'] is False
assert host['original86_stage_count_increment']==result['original86_stage_count_increment']==raw['original86_stage_count_increment']==0
assert raw['component_native_AAA_ABA_credit'] is False
inputs=result['all_metadata_input_pins_before_after'];assert len(inputs)==183
assert len({r['path'] for r in inputs})==183
for row in inputs:
    assert pin(row['path'],row['sha256'],row['identity'])['size_bytes']==row['size_bytes']
profile=result['profile'];exact(profile['direct_invocations'],dict.fromkeys(FUNCTIONS,1))
assert profile['no_module_function_replacements'] is True and profile['profiler_cleared'] is True and profile['forbidden_canonical_calls']==[]
source=F.read_text();tree=ast.parse(source);top={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
assignments={}
for node in tree.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name):assignments[target.id]=node.value
def literal(node):
    if isinstance(node,ast.Name):return literal(assignments[node.id])
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):return literal(node.left)/literal(node.right)
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='Path':return Path(literal(node.args[0]))
    return ast.literal_eval(node)
compiled=compile(tree,str(F),'exec');code_map={}
def code_walk(code):
    code_map[code.co_qualname+'@'+str(code.co_firstlineno)]=code
    for item in code.co_consts:
        if isinstance(item,types.CodeType):code_walk(item)
selected=[]
for code in compiled.co_consts:
    if isinstance(code,types.CodeType) and code.co_name in FUNCTIONS+SUPPORT:
        selected.append(code);code_walk(code)
assert set(profile['profiled_functions'])==set(code_map)
for name in FUNCTIONS+SUPPORT:
    desc=profile['selected_definition_sources'][name];node=top[name]
    exact(desc,dict(name=name,line=node.lineno,end_line=node.end_lineno,
        source_sha256=hashlib.sha256(ast.get_source_segment(source,node).encode()).hexdigest(),canonical_file=str(F)))
edge_counts=Counter()
for edge in profile['call_edges']:
    assert edge['action'] in FUNCTIONS and edge['callee'] in code_map
    assert edge['caller']=='DIRECT_DRIVER' or edge['caller'] in code_map
    assert type(edge['calls']) is int and edge['calls']>0;edge_counts[edge['callee']]+=edge['calls']
for name,row in profile['profiled_functions'].items():
    assert all(type(x) is int and x>=0 for x in row.values())
    assert row['calls']==row['returns']==edge_counts[name]
    assert row['exclusive_selected_canonical_ns']<=row['inclusive_ns']
expectedtops={'sender_source_admission':3,'sender_control_contract':1,'stream_environment_helper_source_admission':2,'source_inputs':1}
for name,count in expectedtops.items():assert profile['profiled_functions'][name+'@'+str(top[name].lineno)]['calls']==count
ret={};expectedfiles={'result.json','raw_preservation_manifest.json'}
assert [r['function'] for r in profile['complete_function_returns']]==FUNCTIONS
for row in profile['complete_function_returns']:
    name=row['function'];desc=row['complete_return'];pin(desc['path'],desc['sha256'],desc['identity'])
    assert desc['size_bytes']==identity(desc['path'])[4] and desc['path']==str(C/(name+'.return.json'))
    document=read(desc['path']);assert document['function']==name
    assert document['python_return_type']==('tuple' if name=='source_inputs' else 'dict')
    assert row['direct_invocations']==1 and 0<row['elapsed_seconds_including_passive_profile']<result['elapsed_seconds']
    ret[name]=document['return_value'];expectedfiles.add(name+'.return.json')
exact(ret['sender_control_contract'],read(literal(assignments['SENDER_CONTROL_CONTRACT'])))
sender=ret['sender_source_admission'];sp=read(literal(assignments['SENDER_SOURCE_PROOF']))
exact(sender['proof'],sp)
assert sender['sender_text']==Path(literal(assignments['CANDIDATE_SENDER_SOURCE'])).read_bytes().decode()
assert sender['candidate_wrapper_text']==(Path(literal(assignments['CANDIDATE_SENDER_SOURCE'])).parent/'FLUSP64.candidate_unit.f').read_bytes().decode()
assert sender['reference_wrapper_text']==(Path(literal(assignments['CANDIDATE_SENDER_SOURCE'])).parent/'FLUSP64.original_reference_unit.f').read_bytes().decode()
stream=ret['stream_environment_helper_source_admission']
exact(stream['proof'],read(literal(assignments['STREAM_ENVIRONMENT_SOURCE_PROOF'])))
exact(stream['actual_helper_controls'],read(literal(assignments['STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS'])))
for name in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:assert stream[name] is False
owner={}
assignment=next(n for n in top['source_inputs'].body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='expected' for t in n.targets))
for key,value in zip(assignment.value.keys,assignment.value.values):owner[literal(key)]=literal(value)
owner.update(sender['source_inputs'])
for p,s in [('SENDER_FACTORY_SOURCE_PARENT','SENDER_FACTORY_SOURCE_PARENT_SHA'),('SENDER_CONTROL_SOURCE','SENDER_CONTROL_SOURCE_SHA'),('SENDER_CONTROL_CONTRACT','SENDER_CONTROL_CONTRACT_SHA'),('SENDER_CONTROLS_AUDITOR','SENDER_CONTROLS_AUDITOR_SHA')]:owner[literal(assignments[p])]=literal(assignments[s])
for path,wanted in stream['source_inputs'].items():
    assert owner.get(path,owner.get(Path(path),wanted))==wanted;owner[path]=wanted
exact(ret['source_inputs'][0],read(literal(assignments['PARENT'])/'declaration.json'))
exact(ret['source_inputs'][1],{str(path):wanted for path,wanted in owner.items()})
assert set(ns_before[str(C)])==expectedfiles and all(r['kind']=='file' for r in ns_before[str(C)].values())
assert set(raw['files'])==expectedfiles-{'raw_preservation_manifest.json'}
for path,wanted in raw['files'].items():pin(C/path,wanted)
assert set(ns_before[str(H)])=={'runtime','run','METADATA_TIMING','runtime/run_bounded_dragon.py','run/metadata.log','run/metadata.watchdog.json','METADATA_TIMING/stages.json','result.json'}
assert all(r['kind']!='link' for records in ns_before.values() for r in records.values())
actualarchive=sum(r['identity'][4] for records in ns_before.values() for r in records.values() if r['kind']=='file')
assert actualarchive==host['whole_archive_bytes']+identity(H/'result.json')[4]
assert {str(p):namespace(p) for p in [H,C]}==ns_before
for row in list(pins.values()):assert identity(row['path'])==row['identity']
timing={r['function']:r['elapsed_seconds_including_passive_profile'] for r in profile['complete_function_returns']}
report=dict(schema='AXMAT_V14B_ACTUAL_METADATA_TIMING_INDEPENDENT_REVIEW_V1',status='PASS_READONLY_METADATA_DIAGNOSTIC_ONLY',
    Root_true_terminal=dict(initial_chunk='44597f',session_id=2168,terminal_chunk='fd9c12',exit_code=0,closed=True),
    four_complete_returns_and_profile_preserved=True,direct_calls_each_once=True,actual_nested_top_counts=expectedtops,
    actual_metadata_input_fullSHA_7identity_before_after=183,genuine_normal_canonical_source_binding=True,
    actual_command_watch_stage_and_full_stdoutstderr_closed=True,original_genuine_MRO_and_120_512_64MiB_96_free8_caps=True,
    whole_host_seconds=host['whole_elapsed_seconds'],watch_elapsed_seconds=watch['elapsed_seconds'],watch_sample_peak_MiB=watch['sampled_peak_rss_mib'],
    archive_at_host_tail_bytes=host['whole_archive_bytes'],archive_current_after_host_result_bytes=actualarchive,
    function_seconds_including_passive_profile=timing,total_four_direct_call_seconds=sum(timing.values()),
    conclusion='The observed four metadata calls together are subsecond. This limited diagnostic does not establish an optimization sufficient to solve the whole86/1800-second final audit failure, and Root has declined the duplicate-small-admission optimization.',
    profiler_interpretation='Generator call/return values count resume/yield intervals. Exclusive subtracts selected canonical Python children only; stdlib/C and passive observer costs remain.',
    old_failed_V13_audit_reexecuted=False,old_failed_V13_factory_imported_or_called=False,
    old28GB_history_rehashed=False,numerical_or_factory_API_called_by_review=False,Root_polled=False,project_written=False,
    full86_component_qualified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    full_evidence_pin_count=len(pins),review_elapsed_seconds=time.monotonic()-started,
    Root_reported_prestart_freshness_chunk='afa17e',prestart_freshness_not_reexecuted_by_this_review=True)
evidence=dict(schema='AXMAT_V14B_ACTUAL_METADATA_DIAGNOSTIC_EXISTING_EVIDENCE_V1',full_fresh_file_pins=list(pins.values()),
    complete_namespace_before_after=ns_before,actual_root=root,actual_watch=watch,actual_stage=stage,
    actual_profile_and_four_return_pointers=profile,source_peer_report=peer,complete_binding_inverse_checked=True,
    metadata_return_types_order_floatbits_complete=True,complete_source_inputs_owner_map_count=len(ret['source_inputs'][1]))
(D/'EVIDENCE.json').write_text(json.dumps(evidence,indent=2,allow_nan=False)+'\n')
report['evidence']=dict(path=str(D/'EVIDENCE.json'),sha256=sha(D/'EVIDENCE.json'))
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('实际V14b纯元数据诊断独审通过，仅诊断资格。Root44597f/session2168→fd9c12严格int0 CLOSED；4完整return/profile、183输入全SHA/7ID前后、完整raw/源逆向及原监督器预算均核对。\n四直接调用各一次；内部sender3次、stream2次，均有真实code/profile链。四次所记录耗时总%.9f秒，亚秒小门不足以证明能解决整个86阶段1800秒失败；Root已决定不实施这个小函数去重复方案。观测器开销未去除、generator计数为resume/yield区间，不能泛化为实际全阶段时间或原生数值通过。\n未导入/调用业务或metadata API，未重读28GB，未改canonical；无full86/native/AAA/ABA资格。\n'%sum(timing.values()))
print(json.dumps(dict(status=report['status'],REPORT_sha256=sha(D/'REPORT.json'),EVIDENCE_sha256=sha(D/'EVIDENCE.json'),fullpins=len(pins),four_direct_seconds=sum(timing.values())),indent=2))
