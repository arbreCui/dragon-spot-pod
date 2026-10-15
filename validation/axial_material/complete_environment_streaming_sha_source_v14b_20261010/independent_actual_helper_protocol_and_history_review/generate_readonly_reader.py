"""Create a pending pure-readonly auditor; never run its future-evidence body."""
from pathlib import Path
import ast, hashlib, json

D=Path(__file__).parent
D.mkdir(parents=True,exist_ok=True)
parent=Path('/private/tmp/axmat_v14_actual_helper_controls_independent_review_20261010/review_actual_controls.py')
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
old=parent.read_text();text=old;edits=[]
def replace(a,b):
    global text
    count=text.count(a);assert count==1,(a[:80],count)
    text=text.replace(a,b);edits.append({'old':a,'new':b,'count':1})
start=old.index('D=Path(');end=old.index('pins={}',start)
replace(old[start:end],'''import argparse
args=argparse.ArgumentParser()
args.add_argument('--config',required=True)
cfg=json.loads(Path(args.parse_args().config).read_text())
assert cfg['schema']=='AXMAT_V14B_ACTUAL_HELPER_REVIEW_BINDINGS_V1'
assert cfg['status']=='ROOT_TERMINAL_RECEIPTS_AND_BOUND_SOURCES_AVAILABLE'
assert cfg['fixture'] is not None and cfg['source_binding'] is not None
for value in cfg['paths'].values():
    assert value is None or (isinstance(value,str) and value.startswith('/'))
assert cfg['paths']['source_dir'] and cfg['paths']['fixture_host_root'] and cfg['paths']['fixture_controls_root']
D=Path(cfg['output_directory'])
assert D.parent==Path(__file__).parent and not D.exists()
D.mkdir()
P=Path('/Users/wen/spot'); A=P/'validation/artifacts'; V=P/'validation/axial_material'
S=Path(cfg['paths']['source_dir'])
H=Path(cfg['paths']['fixture_host_root']);C=Path(cfg['paths']['fixture_controls_root'])
HH=HC=None
if cfg['history'] is not None:
    assert cfg['paths']['history_host_root'] and cfg['paths']['history_controls_root']
    HH=Path(cfg['paths']['history_host_root']);HC=Path(cfg['paths']['history_controls_root'])
capture_roots=(S,H,C)+((HH,HC) if cfg['history'] is not None else ())
''')
replace("ns_before={str(r):namespace(r) for r in (S,H,C,HH,HC)}", "ns_before={str(r):namespace(r) for r in capture_roots}")
replace("root=read(S/'actual_helper_control_receipts/Root_actual_helper_controls_tool_terminal_return.json',\n    '5914404602b0797a8365f3781a7fc278519fca6facc7fd195ce6b70fd3e0bb94')", "root=read(cfg['fixture']['root_receipt_path'],cfg['fixture']['root_receipt_sha256'])")
replace("assert root['schema']=='AXMAT_V14_HELPER_ONLY_ROOT_ACTUAL_TERMINAL_RECEIPT_V1'", "assert root['schema']==cfg['fixture']['root_receipt_schema']")
replace("assert root['action']=='fixtures' and root['initial_session_id']==21373", "assert root['action']=='fixtures' and root['initial_session_id']==cfg['fixture']['session_id']")
replace("assert root['call_history'][0]['chunk_id']=='9fe32f' and root['terminal_result']['chunk_id']=='9c9d85'", "assert root['call_history'][0]['chunk_id']==cfg['fixture']['initial_chunk_id'] and root['terminal_result']['chunk_id']==cfg['fixture']['terminal_chunk_id']")
replace("host=read(H/'result.json','3f0515b181169da0253661f7a6ac706819b4eaa62ad89e28e592dba07c9626ec')", "host=read(H/'result.json',cfg['fixture']['host_result_sha256'])")
replace("out=read(C/'result.json','002467a8fe0fc4ae9246563c1902c02d44ba1d57ea61c7882255a01592b37440')", "out=read(C/'result.json',cfg['fixture']['controls_result_sha256'])")
replace("bound=read(S/'actual_control_sources/exact_source_binding_inverse.json')", "bound=read(cfg['source_binding']['path'],cfg['source_binding']['sha256'])")
replace("'839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'", "'7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'")
replace("assert type(watch['returncode']) is int and watch['returncode']==0 and type(watch['pid']) is int and watch['pid']==70564", "assert type(watch['returncode']) is int and watch['returncode']==0 and type(watch['pid']) is int and watch['pid']>0")
replace("assert watch['sampled_peak_rss_mib']==0.0", "assert type(watch['sampled_peak_rss_mib']) in (int,float) and 0<=watch['sampled_peak_rss_mib']<512")
replace("str(S/'actual_control_sources/helper_only_controls.py')", "bound['driver']['bound_source']['path']")
replace("{'one.link':'other/input.bin','two.link':'one.link','dir.link':'other/nested'}", "{'one.link':'other/input.bin','two.link':'one.link','dir.link':'other/nested','three.link':'two.link','self_cycle.link':'self_cycle.link','mutual_a.link':'mutual_b.link','mutual_b.link':'mutual_a.link','growing_cycle.link':'growing_cycle.link/padding'}")
replace("assert G[names[5]]['result']['oracle_sha256']==oracle(1225) and len(G[names[5]]['actual_new_helper_open_stream_events'])==4", '''aliasgroup=G[names[5]];aliasresult=aliasgroup['result'];aliasevents=aliasgroup['actual_new_helper_open_stream_events']
assert aliasresult['oracle_sha256']==oracle(1225) and len(aliasevents)==6
assert aliasresult['actual_total_complete_alias_streams']==6 and aliasresult['original_four_literal_checks_preserved'] is True
assert aliasresult['separate_full_reads']==4 and aliasresult['dotdot_OS_semantics_retained'] is True
extras=aliasresult['additional_v14b_alias_cases']
assert [x['case'] for x in extras]==['legal_three_link_chain','legal_completed_directory_link_repeat_after_dotdot','self_cycle','mutual_cycle','growing_cycle']
aliasfolder=C/names[5];first=aliasfolder/'one.link';second=aliasfolder/'two.link';third=aliasfolder/'three.link';directory=aliasfolder/'dir.link'
repeated=directory/'..'/'..'/'dir.link'/'..'/'input.bin'
expectedhops=[[str(third),str(second),str(first)],[str(directory),str(directory)]]
for i,(r,expectedliteral) in enumerate(zip(extras[:2],[str(third),str(repeated)])):
    assert r['literal']==expectedliteral and r['independent_full_SHA_oracle']==r['actual_SHA']==oracle(1225)==sha(expectedliteral)
    hops=r['alias_hops'];assert [h[0] for h in hops]==expectedhops[i]
    for literal,seven,word in hops:
        assert identity(literal)==seven and os.readlink(literal)==word
    event=aliasevents[4+i]
    assert event['literal']==expectedliteral and event['bytecount']==event['opened_fd_size']==1225
    assert event['EOF_observed'] is True and event['positive_reads']==1 and event['readinto_calls']==2
assert extras[1]['completed_link_revisited_twice'] is True
for r,path in zip(extras[2:],[aliasfolder/'self_cycle.link',aliasfolder/'mutual_a.link',aliasfolder/'growing_cycle.link']):
    assert r['literal']==str(path)
    original=r['independent_original_OS_full_open_rejection']
    assert original['type']=='OSError' and type(original['errno']) is int and original['errno']==62
    assert r['new_manual_walk_rejection']['type']=='ValueError'
    assert 'cyclic active literal alias expansion' in r['new_manual_walk_rejection']['message']
    assert r['no_partial_file_stream_or_SHA_accepted'] is True and r['context_buffer_memo_lock_reset'] is True
# No cycle aliases are opened here; independent OS failures were captured by the genuine executed driver.
''')
replace("assert set(host['resource_roots']).issubset(roots) and len(host['resource_roots'])==270", "assert set(host['resource_roots']).issubset(roots) and len(host['resource_roots'])==len(set(host['resource_roots']))")
history_start=text.index('# A separate actual whole old->new environment read')
history_end=text.index('\nfor row in list(pins.values())',history_start)
history=text[history_start:history_end]
newhistory=history
substitutions=[
("hr=read(S/'actual_historical_environment_read_receipts/Root_actual_historical_environment_read_tool_terminal_return.json','3f4ca6d6a6e6e4a657dddc73c09e916dba0fa5e765bca424df242d6e04141fad')", "hr=read(cfg['history']['root_receipt_path'],cfg['history']['root_receipt_sha256'])"),
("assert hr['initial_session_id']==46623 and hr['call_history'][0]['chunk_id']=='3b9149'", "assert hr['initial_session_id']==cfg['history']['session_id'] and hr['call_history'][0]['chunk_id']==cfg['history']['initial_chunk_id']"),
("assert hr['terminal_result']['chunk_id']=='667c7b'", "assert hr['terminal_result']['chunk_id']==cfg['history']['terminal_chunk_id']"),
("hh=read(HH/'result.json','2e70836c4dd7ead9b8b9979591c0241884fb82081076e680b6752be834f7f18f')", "hh=read(HH/'result.json',cfg['history']['host_result_sha256'])"),
("hc=read(HC/'result.json','5a1a82598476a1bd7df63e0c09eedf2ff6e2b89211cc12d4f6d16f37872a17a5')", "hc=read(HC/'result.json',cfg['history']['controls_result_sha256'])"),
("assert hw['rss_cap_mib']==512 and hw['sampled_peak_rss_mib']==135.28125", "assert hw['rss_cap_mib']==512 and type(hw['sampled_peak_rss_mib']) in (int,float) and 0<=hw['sampled_peak_rss_mib']<512"),
("assert hc['old_elapsed_seconds_including_profile']==15.705013833998237\nassert hc['new_elapsed_seconds_including_open_probe']==15.68816187500488", "assert type(hc['old_elapsed_seconds_including_profile']) is float and 0<hc['old_elapsed_seconds_including_profile']<hc['elapsed_seconds']\nassert type(hc['new_elapsed_seconds_including_open_probe']) is float and 0<hc['new_elapsed_seconds_including_open_probe']<hc['elapsed_seconds']"),
("'actual_Root_terminal_chunk':'667c7b'", "'actual_Root_terminal_chunk':hr['terminal_result']['chunk_id']"),
("'interpretation':'No material elapsed improvement demonstrated in this instrumented old->new run. This does not admit full86 or remedy the failed V13 final audit.'", "'interpretation':'Actual instrumented old->new complete reads only. Recorded timings include distinct observers; this review alone neither proves a full86 budget solution nor admits component/native/AAA/ABA.'")]
for a,b in substitutions:
    assert newhistory.count(a)==1,(a[:80],newhistory.count(a));newhistory=newhistory.replace(a,b)
replace(history,'history_summary=None\nif cfg[\'history\'] is not None:\n'+''.join('    '+line+'\n' for line in newhistory.splitlines()).rstrip())
replace("assert {str(r):namespace(r) for r in (S,H,C,HH,HC)}==ns_before", "assert {str(r):namespace(r) for r in capture_roots}==ns_before")
replace("'schema':'AXMAT_V14_ACTUAL_HELPER_ONLY_CONTROL_FULL_READONLY_EVIDENCE_V1'", "'schema':'AXMAT_V14B_ACTUAL_HELPER_ONLY_CONTROL_FULL_READONLY_EVIDENCE_V1'")
replace("'schema':'AXMAT_V14_ACTUAL_HELPER_ONLY_CONTROL_INDEPENDENT_REVIEW_V1'", "'schema':'AXMAT_V14B_ACTUAL_HELPER_ONLY_CONTROL_INDEPENDENT_REVIEW_V1'")
replace("'actual_root_terminal_chunk':'9c9d85'", "'actual_root_terminal_chunk':root['terminal_result']['chunk_id']")
replace("'sampled_peak_rss_mib_as_recorded':0.0", "'sampled_peak_rss_mib_as_recorded':watch['sampled_peak_rss_mib']")
replace("'RSS_interpretation':'The original short-child watchdog recorded no positive RSS sample. 0.0 is not a measured process peak and supplies no RSS-reduction or native-512MiB success credit.'", "'RSS_interpretation':'A zero record supplies no measured-peak credit. A positive record observes this helper-only child; neither supplies transport/native512 or improvement credit.'")
replace("'actual_positive_RSS_sample_observed':False", "'actual_positive_RSS_sample_observed':watch['sampled_peak_rss_mib']>0")
replace("'historical_environment_action_executed_by_Root':True", "'historical_environment_action_executed_by_Root':cfg['history'] is not None")
replace("(D/'REPORT.txt').write_text('独立实际控制审查：PASS_HELPER_PROTOCOL_ONLY\\n21项原始控制、完整SHA/EOF、别名/命名空间/拒绝顺序、清理记录、原监督器来源、120秒/512MiB/单子进程/零重试及全资源门均通过有限独审。\\n实际整段11.091秒；原watch采样峰0.0没有捕获短进程正RSS样本，不能解释为真实RSS峰0，也不能授予86阶段组件/native/AAA/ABA资格。\\n本审查只读现存证据，未导入helper、重跑控制或写项目。\\n')", "(D/'REPORT.txt').write_text('H14b独立实际控制只读审查：PASS_HELPER_PROTOCOL_ONLY\\n保留21组，新增别名合法三链/完成后重复与三循环拒绝，完整原始文件SHA、EOF、命名空间及真实Root/监督器证据均已审。\\n实际耗时和采样只见REPORT/EVIDENCE，零采样不等于真实RSS峰0；本范围不授予86阶段、native、AAA或ABA资格。\\n历史环境范围如已终态另见完整五输入/八命名空间event证明，本独审未重读28GB内容或重跑helper。\\n')")
restored=text
for edit in reversed(edits):
    assert restored.count(edit['new'])==1;restored=restored.replace(edit['new'],edit['old'])
assert restored==old
tree=ast.parse(text);compile(tree,str(D/'review_actual_helper_v14b.py'),'exec')
for n in ast.walk(tree):
    if isinstance(n,ast.Import):assert all(a.name in {'argparse','ast','hashlib','json','math','os','stat','struct','time'} for a in n.names)
    if isinstance(n,ast.ImportFrom):assert n.module in {'pathlib','collections'}
out=D/'review_actual_helper_v14b.py';out.write_text(text)
config={'schema':'AXMAT_V14B_ACTUAL_HELPER_REVIEW_BINDINGS_V1','status':'WAITING_TRUE_ROOT_TERMINAL_AND_BOUND_SOURCE_FACTS',
        'output_directory':str(D/'actual_review_attempt_01'),
        'paths':dict.fromkeys(['source_dir','fixture_host_root','fixture_controls_root','history_host_root','history_controls_root']),
        'fixture':None,'history':None,'source_binding':None,
        'fixture_binding_required_fields':['root_receipt_path','root_receipt_sha256','root_receipt_schema','initial_chunk_id','session_id','terminal_chunk_id','host_result_sha256','controls_result_sha256'],
        'history_binding_required_fields':['root_receipt_path','root_receipt_sha256','initial_chunk_id','session_id','terminal_chunk_id','host_result_sha256','controls_result_sha256'],
        'source_binding_required_fields':['path','sha256']}
(D/'PENDING_ACTUAL_BINDINGS.json').write_text(json.dumps(config,indent=2)+'\n')
proof={'schema':'AXMAT_V14B_READONLY_READER_SOURCE_PREPARATION_INVERSE_V1','parent':{'path':str(parent),'sha256':sha(parent)},'new_reader':{'path':str(out),'sha256':sha(out)},'edits':edits,'complete_inverse':restored==old,'AST_and_compile_only_no_execution':True}
(D/'READER_SOURCE_INVERSE.json').write_text(json.dumps(proof,indent=2)+'\n')
plan={'schema':'AXMAT_V14B_ACTUAL_HELPER_REVIEW_PENDING_SCOPE_V1','status':'READY_TO_BIND_ONLY_AFTER_TRUE_ROOT_TERMINAL','reader':proof['new_reader'],'parent_actual_scope':proof['parent'],
      'fixture_groups':21,'new_alias_subcases':['legal_three_link_chain','legal_completed_directory_link_repeat_after_dotdot','self_cycle','mutual_cycle','growing_cycle'],
      'actual_valid_alias_full_streams_required':6,'actual_cycle_file_streams_required':0,'original86_stage_increment':0,
      'caps':{'wall_seconds':120,'own_child_RSS_MiB':512,'archive_bytes':64*2**20,'threads':1,'children':1,'retries':0,'global_history_bytes':96*2**30,'min_free_bytes':8*2**30},
      'full_history_fields':['files','preserved_predecessors','build_python_executable','native_library_aliases','numerical_loader_environment'],
      'preserved_history_namespaces':8,'fixed_original_V13_decl_old_event_count':25213,'fixed_original_V13_decl_distinct_literal_new_event_count':13588,
      'all_event_literal_occurrences_derive_from_complete_declaration':True,'new_unique_literal_order_derive_from_old_first_occurrences':True,
      'original_619_source_required':'619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743',
      'new_canonical_helper_required':'7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3',
      'source_driver_unready_required':'f4beea085f5c8877cf4d77ac031cd7faad39f39a34cae3ecb559fc3bcbb35e26',
      'raw_namespace_is_exhaustive_not_bin_only':True,'literal_hardlinks_are_separate_fullSHA_members':True,'cycle_and_broken_links_preserved_nofollow':True,
      'full_Source_guard_MRO_and_actual_commands_audited':True,'all_fullSHA_and_7identity_before_after':True,'history_28GB_reread_by_review':False,
      'timing_gain_inference':None,'actual_tool_receipt':None,'actual_RESULT':None,'actual_controls_PASS':None,'actual_history_PASS':None,
      'helper_loaded_or_called':False,'fixture_or_history_executed':False,'project_written':False,'Root_polled':False,'native_AAA_ABA_credit':False,
      'small_readonly_directory_lookup_error_preserved':{'chunk_id':'5fef99','exit_code':1,'attempted_filename':'review_actual_protocol.py','reason':'Pure directory lookup guessed a nonexistent auditor filename; no helper/business action.'}}
(D/'REVIEW_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
(D/'REPORT.txt').write_text('H14b后续实际证据只读审查已准备。仅AST/编译reader源码未执行reader；未知Root收据、source绑定及host/driver产物路径全部None。收到真终态后才绑定并逐文件审查；21组与别名5子例、完整历史五输入/八namespace/event范围保留。禁止helper/fixture/benchmark重跑，不授予86/native/AAA/ABA资格。\n')
print(json.dumps({'status':plan['status'],'reader_sha256':sha(out),'plan_sha256':sha(D/'REVIEW_PLAN.json'),'inverse_sha256':sha(D/'READER_SOURCE_INVERSE.json'),'reader_executed':False,'fixture_executed':False,'future_actuals_all_None':True},indent=2))
