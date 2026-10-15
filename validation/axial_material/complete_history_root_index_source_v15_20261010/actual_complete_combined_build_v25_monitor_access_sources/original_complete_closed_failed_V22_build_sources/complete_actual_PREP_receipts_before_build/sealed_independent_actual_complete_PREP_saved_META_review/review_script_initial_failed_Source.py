"""Independent saved-META review only. Stdlib hash/stat/JSON/AST; no reviewed code is imported or run."""
import ast, gc, hashlib, json, math, os, pathlib, stat, sys
ROOT=pathlib.Path(__file__).parent
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=pathlib.Path('/Users/wen/spot/validation/artifacts')
D=B/'actual_complete_combined_prepare_v22_sources'
E=B/'actual_complete_combined_prepare_v22_receipts'
H=ART/'axial-material-complete-combined-prepare-host-v22-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010'
F=pathlib.Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py')
EXPECTED={
 str(E/'Root_actual_prepare_tool_terminal_return.json'):'566ef1b8647709212b9e1c603d2b6559f2920053c36ee7c4520d1dd0c410549e',
 str(E/'Root_actual_complete_combined_prepare_summary.json'):'0b4ef19900921de593d5979283fd65c779a8df857ee1c6204d4e7b7951f4a306',
 str(E/'Root_actual_complete_prepare_namespace_manifest.json'):'b1133e027897d3901aa8133cfbc8c2209ae795c50d05ea069c7db09a736c8d8f',
 str(E/'Root_actual_prepare_metadata_writer_tool_return.json'):'66d4c5400fdb3503ebaf146af0dcb7d626b97358c15c2c0ef5da1323a8507be3',
 str(E/'Root_prelaunch_complete_source_freeze.json'):'c309a705e55865b2730ef0d9fd3f9bb1bad572acb8dd4ded483f298be49a3103',
 str(E/'Root_final_prelaunch_source_and_reserve_check.json'):'bc04ef1de210985433e532e632bc0b7cdaf12f077318f82e39f40b60620793a0',
 str(T/'declaration_terminal_return.json'):'96ff567a30a451af02767c153ce8f0213c9f5b6e7330eb48b1ca9c69a992b61c',
 str(O/'declaration.json'):'8ad01e54e6ed89911c56d1fe04284e5f39f81ebe0ae9aa060253b9378df346b1',
 str(O/'input_graph.json'):'0dd662ee6ede3122fe8d4af4e8c84b7e8e20ce2b75caed8ce0d3700e875985b0',
 str(O/'input_creation_python_open_trace.json'):'b8c1734611f449ec11dd3263a91570ed10d1817927d0a0a9bfd992753f4ec4aa',
 str(F):'09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e',
 str(D/'combined_prepare_host.py'):'1be8cbf79ef14d7537d099d0a08d0c5ef755530c2652c58cfbb188c7e18bf051',
 str(D/'write_actual_prepare_terminal.py'):'348ae877f7c8e4c86f07cb4a49f96de97e11839ccb0858c5a602e3982a4ccba0',
}
checks=[]; pins={}
def need(value,label):
 if value is not True: raise ValueError(label)
 checks.append({'check':label,'passed':True})
def ident(p):
 s=pathlib.Path(p).lstat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p):
 p=pathlib.Path(p); key=str(p); before=ident(p)
 need(stat.S_ISREG(before[2]) and before[3]==1,'regular single-link '+key)
 with p.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
 need(ident(p)==before,'full EOF stable '+key)
 v={'path':key,'sha256':digest,'size_bytes':before[4],'identity':before}
 if key in pins: need(pins[key]==v,'repeated complete pin unchanged '+key)
 else: pins[key]=v
 return v
def verify(q,label='pin'):
 need(type(q) is dict and type(q.get('path')) is str and type(q.get('sha256')) is str,label+' shape')
 p=pathlib.Path(q['path']); key=str(p)
 v=pins.get(key)
 if v is None: v=full(p)
 else: need(ident(p)==v['identity'],label+' current 7ID '+key)
 need(v['sha256']==q['sha256'],label+' SHA '+key)
 if 'identity' in q:
  need(type(q['identity']) is list and len(q['identity'])==7 and all(type(i) is int for i in q['identity']),label+' typed 7ID '+key)
  need(v['identity']==q['identity'],label+' 7ID '+key)
 if 'size_bytes' in q: need(type(q['size_bytes']) is int and v['size_bytes']==q['size_bytes'],label+' bytes '+key)
 return v
def pairs(items):
 out={}
 for k,v in items:
  if k in out: raise ValueError('duplicate JSON key')
  out[k]=v
 return out
def read(p):
 p=pathlib.Path(p);v=full(p) if str(p) not in pins else pins[str(p)]
 need(ident(p)==v['identity'],'JSON current pin '+str(p))
 with p.open('r',encoding='utf8') as f:
  x=json.load(f,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
 need(ident(p)==v['identity'],'JSON read stable '+str(p))
 return x
def finite(x,label):
 need(type(x) in (int,float) and math.isfinite(x),label+' typed finite')
def terminal(x,chunk,label):
 tr=x['terminal_tool_return']
 need(x['closed'] is True,label+' closed')
 need(type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr,label+' strict closed EXIT0')
 need(tr['chunk_id']==chunk,label+' actual chunk')
 finite(tr['wall_time_seconds'],label+' time')
 return tr
def walk(root):
 files={}; dirs={};syms={}
 for folder,subdirs,names in os.walk(root,followlinks=False):
  for n in subdirs+names:
   p=pathlib.Path(folder)/n;rel=str(p.relative_to(root));i=ident(p)
   if stat.S_ISLNK(i[2]): syms[rel]={'identity':i,'literal_target':os.readlink(p)}
   elif stat.S_ISDIR(i[2]): dirs[rel]=i
   elif stat.S_ISREG(i[2]): files[rel]=verify({'path':str(p),'sha256':pins[str(p)]['sha256']}) if str(p) in pins else full(p)
   else:raise ValueError('nonregular namespace member '+str(p))
 return files,dirs,syms
def same_namespace(q):
 root=pathlib.Path(q['root']); actual=walk(root)
 need(set(actual[0])==set(q['files']),'complete namespace file set '+str(root))
 for rel,v in q['files'].items():
  need(v['path']==str(root/rel),'namespace exact logical path '+str(root/rel));verify(v,'namespace')
 expected_dirs={v['path']:v['identity'] for v in q['directories']}
 need(actual[1]==expected_dirs,'complete namespace directory 7IDs '+str(root))
 need(actual[2]==q['symlinks'],'complete namespace literal symlinks '+str(root))
 return actual
for p,digest in EXPECTED.items():need(full(p)['sha256']==digest,'Root declared fixed SHA '+p)
tr=read(E/'Root_actual_prepare_tool_terminal_return.json');rt=terminal(tr,'fc5201','actual PREP')
need(tr['schema']=='ROOT_V22_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1' and tr['observed_terminal'] is True and tr['session_repolled_after_close'] is False,'actual Root receipt schema and no repoll')
need(type(tr['initial_tool_return']['session_id']) is int and tr['initial_tool_return']['session_id']==74847 and tr['initial_tool_return']['chunk_id']=='7f15ba','actual launch receipt')
wrt=read(E/'Root_actual_prepare_metadata_writer_tool_return.json');terminal(wrt,'34125a','actual metadata writer')
need(wrt['metadata_only'] is True,'actual writer metadata-only scope')
summary=read(E/'Root_actual_complete_combined_prepare_summary.json')
need(summary['schema']=='ROOT_V22_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD','summary exact PREP-only status')
freeze=read(E/'Root_prelaunch_complete_source_freeze.json')
reserve=read(E/'Root_final_prelaunch_source_and_reserve_check.json')
ns=read(E/'Root_actual_complete_prepare_namespace_manifest.json')
need(ns['schema']=='ROOT_V22_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and ns['no_build_or_native_credit'] is True,'namespace scope')
need([q['root'] for q in ns['namespaces']]==[str(p) for p in (H,S,O,T,D)],'all H/S/O/T/D namespace roots')
namespace_counts={}
for q in ns['namespaces']:
 a=same_namespace(q); namespace_counts[q['root']]={'files':len(a[0]),'directories':len(a[1]),'symlinks':len(a[2])}
need([(v['files'],v['directories'],v['symlinks']) for v in namespace_counts.values()]==[(5,3,0),(11,1,0),(4,5,0),(6,0,0),(304,36,0)],'actual complete namespace counts')
need(freeze['file_count']==304 and freeze['directory_count']==36 and freeze['symlinks']=={},'prelaunch complete D scope')
need(freeze['source_root']==str(D) and ident(D)==freeze['source_root_identity'],'frozen D root 7ID')
a=walk(D)
need(set(a[0])==set(freeze['complete_files']) and a[1]==freeze['complete_directories'] and a[2]==freeze['symlinks'],'prelaunch D complete namespace unchanged')
for rel,q in freeze['complete_files'].items():need(q['path']==str(D/rel),'frozen path '+rel);verify(q,'prelaunch source')
need(freeze['no_SOURCE_append_after_freeze'] is True and freeze['all_file_SHA7ID_recorded'] is True,'prelaunch full freeze')
verify(ns['canonical_factory']);verify(freeze['canonical_factory'])
h=read(H/'result.json');w=read(H/'run/prepare.watchdog.json');stages=read(H/'COMBINED_PREPARATION/stages.json')['stages']
need(h['schema']=='AXMAT_V22_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','actual genuine host schema')
need(h['status']=='ACTUAL_COMPLETE_COMBINED_PREPARE_EXTERNAL_ROOT_REQUIRED','actual host honest external receipt status')
all_inputs=h['input_sources']+[h['original_helper'],h['resource_factory']]
need(all_inputs==ns['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged'] and len(all_inputs)==313 and len(h['input_sources'])==311,'313 complete ordered original input pins')
need({q['path'] for q in h['input_sources'][7:]}=={q['path'] for q in freeze['complete_files'].values()} and len(h['input_sources'][7:])==304,'311 host sources contain all D304 plus seven actual inputs')
for q in all_inputs:verify(q,'all original inputs')
d=read(O/'declaration.json');cp=d['actual_external_prepare_terminal_contract'];f=read(T/'declaration_terminal_return.json')
command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(F),'prepare-build']
need(h['actual_canonical_command']==command and w['command']==command and cp['command']==command and f['command']==command,'actual no-extra-argv canonical command')
expected_cmd='env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'combined_prepare_host.py')+' > '+str(E/'parent_stdout.log')+' 2> '+str(E/'parent_stderr.log')
need(tr['actual_launch_arguments']['cmd']==expected_cmd,'actual original thread-one -B normal host launch')
need(len(stages)==1 and stages==h['stage_records'],'one actual stage complete records')
stage=stages[0]
need(stage['label']=='run/prepare' and stage['command']==command and stage['status']=='PASS' and stage['wall_cap_seconds']==600.0,'actual single PASS stage')
need(type(w['pid']) is int and w['pid']==19138,'actual own child PID from genuine watchdog (no claim invented)')
need(type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True,'genuine own-child successful cleanup')
need(h['watchdog']==w,'full host/watchdog equality')
for k in ['elapsed_seconds','sampled_peak_rss_mib','wall_cap_seconds','rss_cap_mib']:finite(w[k],'watch '+k)
finite(h['whole_seconds'],'whole elapsed')
need(w['elapsed_seconds']==192.8776912499452 and h['whole_seconds']==194.0198942499701 and w['sampled_peak_rss_mib']==474.0,'actual measured PREP metrics')
need(0<w['elapsed_seconds']<=600 and 0<h['whole_seconds']<1800 and 0<=w['sampled_peak_rss_mib']<512 and w['rss_cap_mib']==512 and 0<w['wall_cap_seconds']<=600,'actual original runtime caps')
for k,v in {'whole_wall_cap_seconds':1800,'stage_wall_cap_seconds':600,'rss_cap_mib':512,'archive_cap_bytes':2*2**30,'threads':1,'children_at_once':1,'retries':0}.items():need(type(h[k]) is int and h[k]==v,'host original cap '+k)
for k,v in {'total_wall_seconds':1800,'stage_wall_seconds':600,'rss_cap_mib':512,'archive_reserve_bytes':2*2**30,'artifact_budget_bytes':96*2**30,'min_free_bytes':8*2**30,'threads':1,'numeric_children_at_once':1,'retries':0}.items():need(type(d[k]) is int and d[k]==v,'declaration original cap '+k)
for k,v in {'whole_wall_cap_seconds':1800,'stage_wall_cap_seconds':600,'rss_mib':512,'joint_archive_cap_bytes':2*2**30,'history_cap_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children':1,'retries':0}.items():need(type(summary[k]) is int and summary[k]==v,'summary original cap '+k)
need(summary['whole_seconds']==h['whole_seconds'] and summary['child_seconds']==w['elapsed_seconds'] and summary['sampled_peak_rss_mib']==w['sampled_peak_rss_mib'],'summary true actual metrics')
need(summary['all_source_files_verified_count']==11 and summary['all_original_pinned_inputs_unchanged_count']==313,'S11 distinct from D304 and actual313')
for row in (reserve['actual_original_resource_check'],h['resources_before'],stage['resource_before'],stage['resource_after'],h['resources_after']):
 need(row['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1','genuine unchanged dynamic history scope')
 need(row['artifact_budget_bytes']==96*2**30 and row['min_free_bytes']==8*2**30,'saved genuine history96/free8 caps')
 need(len(row['resource_roots'])==344 and set(row['resource_roots'])==set(row['declared_resource_roots']) and set(row['resource_roots'])==set(d['resource_roots']),'complete 344 saved declared and dynamic history roots')
 need(all(pathlib.Path(p).is_relative_to(ART) and pathlib.Path(p)!=ART for p in row['resource_roots']),'all saved history roots strict ART descendants')
 for k in ['artifact_bytes','disk_free_bytes','regular_files','checked_unix']:finite(row[k],'saved resource '+k)
 need(row['artifact_bytes']<96*2**30 and row['disk_free_bytes']>=8*2**30,'actual saved resource PASS')
need(reserve['genuine_supervisor_MRO_unchanged'] is True and h['supervisor_class_or_MRO_modified'] is False and h['profile_used'] is False,'actual original genuine MRO and no profiling')
for k in ('genuine_supervisor_source','genuine_parent_class_source','actual_local_supervisor_helper','actual_resource_class_factory','original_factory_ancestry_descriptor'):verify(d[k],'genuine original SOURCE')
preflight=d['actual_supervisor_constructor_preflight']
need(preflight['actual_original_constructor_exercised'] is True and preflight['native_or_numeric_child_launched'] is False and preflight['class_name']=='OwnRSSSerialExecutor' and preflight['genuine_parent_class_name']=='SerialExecutor','genuine constructor PREP metadata scope')
need(d['actual_resource_class_factory']['genuine_class_not_overlay'] is True and d['original_factory_ancestry_descriptor']['genuine_class_not_overlay'] is True,'genuine resource class no overlay')
need(d['stages']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'],'all five future build stages retained')
need(not os.path.lexists(O/'seal.json') and not os.path.lexists(T/'terminal_return.json'),'no actual complete build seal or terminal')
need(f['schema']==cp['schema']=='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V22_ACTUAL_EXTERNAL_PREP_RETURN_V1' and cp['root']==str(T) and cp['receipt']==str(T/'declaration_terminal_return.json'),'formal exact PREP contract')
need(type(f['returncode']) is int and f['returncode']==0 and f['actual_tool_result']==rt and f['actual_root_host_launchargs']==tr['actual_launch_arguments'],'formal genuine actual typed tool return binding')
for k in ['successful_declaration_input_observed','actual_tool_terminal_return_observed','record_written_after_actual_terminal_return']:need(f[k] is True,'formal '+k)
need(f['observed_at_unix']>=stage['started_unix']+w['elapsed_seconds'],'formal observed after actual child completion')
for k in ['source','declaration','source_inventory','full_stdout','full_stderr','actual_child_watchdog','actual_root_host_terminal_tool_return','actual_root_host_stdout','original_executor_merged_capture_source']:verify(f[k],'formal complete saved pin')
need(f['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and f['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and f['separate_child_stderr_captured'] is False and f['independent_child_stderr_empty_verified'] is False,'honest merged child stream and separate outer stderr labels')
for src,dst in [(H/'run/prepare.log',T/'actual_child_merged_stdout_stderr.json'),(E/'parent_stderr.log',T/'actual_external_host_stderr.txt'),(E/'parent_stdout.log',T/'actual_external_host_stdout.json'),(E/'Root_actual_prepare_tool_terminal_return.json',T/'actual_external_Root_tool_terminal.json')]:
 need(full(src)['sha256']==full(dst)['sha256'] and src.read_bytes()==dst.read_bytes(),'complete byte-exact original stream '+str(dst))
need(pins[str(E/'parent_stderr.log')]['size_bytes']==0,'actual outer host stderr empty only')
need(read(H/'run/prepare.log')=={'declaration':str(O/'declaration.json'),'declaration_sha256':EXPECTED[str(O/'declaration.json')]} and stage['log_sha256']==pins[str(H/'run/prepare.log')]['sha256'],'full actual canonical merged JSON stream')
hostout=read(E/'parent_stdout.log')
need(hostout['status']==h['status'] and hostout['actual_external_Root_terminal_required'] is True,'actual host stdout requires Root terminal')
for q in [hostout['actual_host_result'],hostout['actual_prepare_stdout']]:verify(q,'complete parent stdout pointers')
for k in ['actual_declaration','actual_prepare_stdout','actual_source_admission','actual_watchdog']:verify(h[k],'host saved output')
for k in ['actual_root_terminal','actual_host_result','formal_PREP_terminal','actual_declaration','actual_input_graph','actual_complete_creation_trace','namespace_manifest']:verify(summary[k],'summary original pin')
need(summary['Root_actual_terminal']==summary['actual_root_terminal'] and summary['actual_complete_input_graph']==summary['actual_input_graph'],'summary aliases exact')
need(f['input_graph']==d['input_graph'] and f['historical_whole_component_body']==d['historical_whole_component_body'] and f['historical_PREP']==d['historical_PREP'] and f['actual_last_cprime_trim_component_INPUT']==d['actual_last_cprime_trim_component_INPUT'],'full historical/trim metadata retained in formal T')
actual_S=walk(S)
inventory={'files':{rel:v['sha256'] for rel,v in actual_S[0].items()},'directories':sorted(actual_S[1]),'symlinks':{}}
need(inventory==d['source_inventory']==read(T/'Root_actual_SOURCE_inventory.json'),'all S11 actual Source inventory exact')
sa=read(S/'source_admission.json')
need(sa['trim_component_API_executed_in_this_PREP'] is True and d['trim_component_API_executed_in_this_PREP'] is True and f['trim_component_API_executed_in_this_PREP'] is True,'actual existing trim metadata API execution honestly retained')
need(sa['inherited_mathematical_controls_not_newly_executed'] is True and sa['retained_cache_math_unchanged'] is True and sa['no_Fortran_or_observer_source_written'] is True,'inherited mathematics/source scope')
for container,keys,label in [
 (summary,['new_five_stage_build_executed','whole_combined_INPUT_admitted','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted','goal_complete','original_five_build_stages_executed','native_RSS_qualified','cleanup_performed'],'summary'),
 (h,['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'],'host'),
 (d,['original_component_APIs_executed_now','historical_failed_combined_RUN_promoted','mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'],'declaration'),
 (sa,['original_component_APIs_executed_now','historical_failed_combined_RUN_grants_success','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'],'source admission'),
 (f,cp['false_fields'],'formal')]:
 for k in keys:need(container[k] is False,'no science/build credit '+label+' '+k)
need(d['original_operator_capture_RSS_scope_not_transferred'] is True and summary['original_caps_preserved'] is True,'no transferred native RSS and original caps')
tree=ast.parse(F.read_text())
defs=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))]
need(len(defs)==70,'reviewed complete canonical all70 Source definitions')
names=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assign={t.id:x.value for x in tree.body if isinstance(x,ast.Assign) for t in x.targets if isinstance(t,ast.Name)}
for name in names:need(isinstance(assign[name],ast.Constant) and assign[name].value is None,'all six original future business pins None '+name)
qsha=ast.literal_eval(assign['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])
need(qsha=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816','true new helper metadata-only Q Source binding')
q=read(B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json')
need(pins[str(B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json')]['sha256']==qsha,'true Q whole EOF')
# Current graph and creation trace are encoded metadata only. No decoder or helper API is invoked.
stored=read(O/'input_graph.json')
need(stored['schema']=='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1' and set(stored)=={'schema','graph'},'complete encoded graph storage envelope')
g=stored['graph']
need(g['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and g['consumer_scope'] is None and g['science_qualification_created'] is False and g['external_declaration_exit0_verified'] is False and g['live_resources_verified'] is False,'complete stored graph no resource or science qualification')
need(g['content_sha256']==d['input_graph']['content_sha256']==g['wire_encoding']['decoded_content_sha256'],'stored/declaration encoded content binding only')
need(d['input_graph_source_root_inventory_is_exhaustive'] is True and d['input_graph']['scope']=='COMPLETE_HISTORICAL_INPUT_ONLY','complete historical graph scope')
rr=g['requirements']['rows']
need(rr['row_count']==238441 and rr['column_count']==5 and rr['encoding']=='CANONICAL_UNSIGNED_LEB128_BASE64','actual complete encoded 238441 five-column requirements (not five wrapper keys)')
counts={'canonical_files':len(g['canonical_files']['rows']),'owners':len(g['owners']['rows']),'namespaces':len(g['namespaces']),'aliases':len(g['aliases']),'absence_inputs':len(g['absence_inputs']),'requirements':rr['row_count'],'requirement_columns':rr['column_count'],'read_trace_records':g['read_trace']['records']['row_count'],'coverage_categories':len(g['coverage'])}
need(counts=={'canonical_files':37111,'owners':4473,'namespaces':86,'aliases':186,'absence_inputs':479,'requirements':238441,'requirement_columns':5,'read_trace_records':63543,'coverage_categories':9},'actual complete current encoded graph counts')
need(g['newly_declared_input_paths']=={} and g['newly_declared_input_pins']=={} and g['declared_new_source_roots']==[],'no new graph declarations inserted')
need(len(g['closure_categories'])==9 and set(g['coverage'])==set(g['closure_categories']) and len(g['trace_coverage'])==10,'all nine coverage and ten trace fields retained')
need(g['typed_snapshot']['original_component_APIs_executed_now'] is False and g['typed_snapshot']['failed_historical_combined_RUN_promoted'] is False,'complete typed graph historical scope')
need(g['typed_snapshot']['historical_whole_component_body']==d['historical_whole_component_body'] and g['typed_snapshot']['actual_last_cprime_trim_component_INPUT']==d['actual_last_cprime_trim_component_INPUT'],'complete typed metadata body binding')
del rr,g,stored;gc.collect()
trace=read(O/'input_creation_python_open_trace.json')
need(trace['schema']=='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' and trace['coverage']=='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' and len(trace['records'])==counts['read_trace_records'] and trace['subprocess_records']==[],'complete actual 63543 creation open trace and zero subprocess records')
del trace;gc.collect()
# Calculate actual full joint scope, preserving separately labeled historical sample before two later Root outputs.
current_joint=sum(v['size_bytes'] for root in (H,S,O,T,D,E) for v in walk(root)[0].values())+pins[str(F)]['size_bytes']
later=[E/'Root_actual_complete_combined_prepare_summary.json',E/'Root_actual_prepare_metadata_writer_tool_return.json']
historical_joint=current_joint-sum(pins[str(p)]['size_bytes'] for p in later)
need(summary['joint_archive_bytes']==152660642 and historical_joint==summary['joint_archive_bytes'],'exact historical H/S/O/T/D/E+factory joint sample restored by two honest later Root outputs')
need(current_joint<2*2**30,'current complete H/S/O/T/D/E+factory joint below original2GiB')
# Reuse already sealed bound Source qualification; do not redo its complete inverse history.
reuse=pathlib.Path('/private/tmp/axmat_v22_actual_BOUND_PREP_independent_SOURCE_review_20261010_d__3ud50')
need(full(reuse/'REVIEW.json')['sha256']=='410dec337abcf2e99ba9acaee7976ac9d55baeaa96d72a23ae4668786c65d6e2','reuse exact875 bound Source review')
need(full(reuse/'MANIFEST.json')['sha256']=='5f07f9ec2d6d77ca5d40e8e026e6d45627a782fcc1c38dfbbfa86d94e73e2d7e','reuse exact sealed bound Source manifest')
# Every unique reviewed source/META/namespace/input is re-read to full EOF, not merely stat-rechecked.
initial=dict(pins)
for p,v in initial.items():need(full(p)==v,'final complete EOF/SHA7ID unchanged '+p)
report={'schema':'INDEPENDENT_V22_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1','status':'PASS_ACTUAL_COMPLETE_PREP_ONLY','source_only_reviewer':True,'stdlib_only':True,'actual_PREP_closed_EXIT0_verified':True,'actual_metadata_writer_closed_EXIT0_verified':True,'actual_PREP_terminal_chunk':'fc5201','actual_metadata_writer_terminal_chunk':'34125a','checks':checks,'all_checks_typed_true':True,'check_count':len(checks),'complete_actual_input_entries':313,'complete_unique_reviewed_files':len(pins),'complete_full_EOF_input_pins':list(pins.values()),'namespace_counts':namespace_counts,'actual_graph_metadata_counts':counts,'metrics':{'whole_seconds':h['whole_seconds'],'child_seconds':w['elapsed_seconds'],'sampled_peak_rss_mib':w['sampled_peak_rss_mib'],'historical_joint_bytes':historical_joint,'current_joint_bytes':current_joint},'actual_genuine_guard_caps':{'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children':1,'retries':0},'all_complete_scope_verified':True,'truthful_capture':{'child_merged_full_stream':True,'outer_host_stderr_full_stream':True,'independent_child_stderr_captured':False},'existing_trim_metadata_API_was_actually_executed_by_Root_PREP':True,'reviewer_called_any_reviewed_API':False,'graph_payload_decoded_by_business_codec':False,'numeric_or_native_payload_read':False,'new_business_or_numeric_execution':False,'new_five_stage_build_qualified':False,'whole_INPUT_qualified':False,'native_transport_qualified':False,'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False,'goal_complete':False,'cleanup_performed':False,'blockers':[]}
(ROOT/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(ROOT/'REPORT.txt').write_text('PASS: actual V22 complete PREP only. Root fc5201 closed typed EXIT0 and actual metadata writer34125a verified.\nAll313 original inputs, D304/36, S11, all H/S/O/T/D namespaces and complete45,544,751B graph plus41,013,047B trace full EOF/SHA7ID unchanged.\nOne genuine own-child PASS; whole194.0198942499701s/child192.8776912499452s/peak474MiB, original1800/600/512/2GiB/96GiB/free8GiB/1/1/0 preserved.\nComplete graph:37111 canonical files,4473owners,86namespaces,186aliases,238441 five-column requirements,63543full open records. No graph decoder/helper/guard/business execution by reviewer.\nStreams are complete child merged stdout/stderr and actual outer host stderr; independent child stderr is not claimed. Existing trim metadata API execution is honestly retained.\nFive-stage build/whole INPUT/native/AAA/ABA/physical balance/cleanup/goal remain unqualified.\n')
print(json.dumps({'status':report['status'],'check_count':len(checks),'unique_reviewed_files':len(pins),'original_input_entries':313,'namespace_counts':namespace_counts,'graph_counts':counts,'historical_joint_bytes':historical_joint,'current_joint_bytes':current_joint,'review':str(ROOT/'REVIEW.json')},allow_nan=False))

