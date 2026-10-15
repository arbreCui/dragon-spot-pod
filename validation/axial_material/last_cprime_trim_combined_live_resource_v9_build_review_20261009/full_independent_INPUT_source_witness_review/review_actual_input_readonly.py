from pathlib import Path
import ast, datetime, hashlib, json, math, os, stat, struct

H=Path(__file__).resolve().parent
ROOT=Path('/Users/wen/spot'); A=ROOT/'validation/axial_material'; B=ROOT/'validation/artifacts'
R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
NAME='prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
F=A/NAME; F8=A/NAME.replace('_v9.py','_v8.py')
S=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
O=B/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
T=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
D=B/'axial-material-owned-specs-trim-v9-standalone-bounded-runtime-api-intake-evidence-20261009'
FS='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'; DS='7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0'
PS='0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb'; SS='ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed'; RS='709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27'
HS='180053eb92dbe4ff05ee87db75056ee2debca057aecd1b314e6ed648a9096aae'; CS='5bd181e59b3229398ec7725e8513da5cf055791400522935f5ebfc2b9bd0d03e'
AS='0e5727aee267c24c3a74c387c628b3633a23826e38c41eda1bfe14ecd02872f5'; IS='23acbccb31befbba6ae52ffaf80ae119fd3b7341faa263c18a45c0cd239062ba'
P12='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
PINS={}; CHECKS=0
def check(v,label):
 global CHECKS
 if not v: raise AssertionError(label)
 CHECKS+=1
def identity(p):
 s=p.lstat(); check(stat.S_ISREG(s.st_mode) and p.resolve(strict=True)==p,'ordinary canonical file '+str(p))
 return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,sha=None):
 p=Path(p); before=identity(p); value=p.read_bytes(); h=hashlib.sha256(value).hexdigest()
 check(before==identity(p),'stable read '+str(p)); check(sha is None or h==sha,'SHA '+str(p))
 if str(p) in PINS:check(PINS[str(p)]['sha256']==h and PINS[str(p)]['identity']==before,'repeat pin stable '+str(p))
 PINS[str(p)]=dict(path=str(p),sha256=h,bytes=len(value),identity=before); return value
def pairs(items):
 result={}
 for k,v in items:
  if k in result:raise ValueError('duplicate JSON key '+k)
  result[k]=v
 return result
def reject(v):raise ValueError(v)
def floating(v):
 x=float(v)
 if not math.isfinite(x):raise ValueError('nonfinite JSON float')
 return x
def finite(v):
 if type(v) is dict:
  for k,x in v.items():check(type(k)is str,'builtin JSON strkey');finite(x)
 elif type(v)is list:
  for x in v:finite(x)
 elif type(v)is float:check(math.isfinite(v),'finite JSON')
 else:check(type(v)in(str,int,bool,type(None)),'builtin JSON scalar')
def obj(p,sha=None):
 v=json.loads(raw(p,sha),object_pairs_hook=pairs,parse_float=floating,parse_constant=reject);finite(v);return v
def typed(x,y,ordered=True):
 if type(x)is not type(y):return False
 if type(x)is dict:return (list(x)==list(y) if ordered else x.keys()==y.keys()) and all(typed(x[k],y[k],ordered)for k in x)
 if type(x)is list:return len(x)==len(y)and all(typed(a,b,ordered)for a,b in zip(x,y))
 if type(x)is float:return math.isfinite(x)and math.isfinite(y)and struct.pack('!d',x)==struct.pack('!d',y)
 return x==y
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def inventory(root):
 files={};dirs=[];links={}
 for folder,sub,names in os.walk(root,followlinks=False):
  for name in list(sub):
   p=Path(folder)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p);sub.remove(name)
   else:dirs.append(str(p.relative_to(root)))
  for name in names:
   p=Path(folder)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p)
   else:files[str(p.relative_to(root))]=hashlib.sha256(raw(p)).hexdigest()
 return dict(files=files,symlinks=links,directories=sorted(dirs))

receipt=obj(D/'Root_terminal_return.json',IS)
root=obj(R/'Root_actual_bound_INPUT_host_tool_return.json','ed535093a16ab98a897bc3b895189a99a9eff4cb07165ea69d7f720b374a7434')
record=obj(R/'Root_actual_INPUT_payload_recording_tool_return.json')
actual=dict(initial_chunk_id='0a5d42',session_id=11005,terminal_chunk_id='cbbfbe',exit_code=0,closed=True)
check(typed(root['actual_tool'],actual)and root['actual_tool_terminal_return_observed']is True and root['written_after_actual_tool_return']is True,'true external Root host0 CLOSED')
check(type(receipt['actual_exit_code'])is int and receipt['actual_exit_code']==0 and typed(receipt['actual_tool'],{k:v for k,v in actual.items()if k!='closed'})and receipt['record_written_after_actual_tool_return']is True,'durable independent tenth genuine builtin0 facts')
check(typed(record['actual_host_tool'],actual)and record['actual_recorder_tool']==dict(chunk_id='727fd7',exit_code=0,closed=True)and type(record['actual_recorder_tool']['exit_code'])is int and record['observed_after_actual_recorder_tool_return']is True,'Root true recorder0 observed after terminal')
check(record['durable_Root_receipt']==dict(path=str(D/'Root_terminal_return.json'),sha256=IS,size=7234),'Root actual recorder durable receipt pin')
payload=receipt['source_payload_pins']; names=['host.py','postterminal_recorder.py','host.stdout','host.stderr','result.json','runtime/run_bounded_dragon.py','intake/admit.log','intake/admit.watchdog.json','STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json']
check(list(payload)==names,'exact original9 ordered source copy table')
inv=inventory(D); check(set(inv['files'])==set(names)|{'Root_terminal_return.json'}and inv['symlinks']=={}and inv['directories']==['STANDALONE_BOUNDED_RUNTIME_API_INTAKE','intake','runtime'],'ordinary exact9+1 full namespace')
for name,p in payload.items():
 check(inv['files'][name]==p['sha256'],'durable fullSHA copy '+name); value=raw(p['path'],p['sha256']);check(len(value)==PINS[str(D/name)]['bytes'],'whole source-copy byte length '+name)
inventory9=dict(files={k:v for k,v in inv['files'].items()if k!='Root_terminal_return.json'},symlinks={},directories=inv['directories'])
check(typed(inventory9,receipt['payload_inventory'],False),'receipt exact nine original inventory')
check(sum(PINS[str(D/n)]['bytes']for n in names)==receipt['payload_bytes']==record['payload_bytes']==25886733 and record['payload_count']==9,'nine payload byte total excludes independent receipt')
for row in record['payload_files']:check(PINS[row['path']]['sha256']==row['sha256']and PINS[row['path']]['bytes']==row['size'],'Root all actual copy pins')
host=raw(D/'host.py',HS).decode(); rec=raw(D/'postterminal_recorder.py',CS).decode();ht=ast.parse(host);ct=ast.parse(rec)
check(host.count('runner.execute(')==1 and 'full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)'in host,'source genuine MRO and exactlyone supervisor child')
check("if sys.flags.optimize!=0 or os.environ.get('PYTHONOPTIMIZE')"in host and "sys.dont_write_bytecode=True"in host and "if any(os.environ.get(k)!='1'for k in THREAD_KEYS)"in host,'nonoptimized byteoff five threadkeys1 source guards')
src=raw(F,FS).decode(); mother=raw(F8,'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4').decode();tree=ast.parse(src)
def defs(text):return {n.name:(n,ast.get_source_segment(text,n))for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
fd,md=defs(src),defs(mother);check(len(fd)==len(md)==65 and list(fd)==list(md),'whole65 producer definitions inventory')
fn_pins=[]
for name,(node,seg)in fd.items():
 check(seg==md[name][1]and ast.dump(node,include_attributes=False)==ast.dump(md[name][0],include_attributes=False),'whole definition byte/AST unchanged '+name)
 fn_pins.append(dict(name=name,start=node.lineno,end=node.end_lineno,sha256=hashlib.sha256(seg.encode()).hexdigest()))
d=obj(O/'declaration.json',DS); prep=obj(T/'declaration_terminal_return.json',PS); run=obj(T/'terminal_return.json',RS); seal=obj(O/'seal.json',SS)
check(inventory(S)==d['source_inventory']and len(d['source_inventory']['files'])==11,'whole SOURCE11 fullSHA namespace')
outinv=inventory(O);check(outinv['directories']==seal['directories']and outinv['symlinks']==seal['symlinks']=={}and set(outinv['files'])==set(seal['files'])|{'seal.json'} and all(outinv['files'][k]==v for k,v in seal['files'].items()),'complete21 sealedOUT+seal22 whole bytes')
for field in ('source_inventory','full_stdout','full_stderr'):raw(prep[field]['path'],prep[field]['sha256'])
check(obj(prep['source_inventory']['path'])==d['source_inventory'],'frozen actual PREP4 witnesses whole SOURCE11')
for field in ('full_stdout','full_stderr'):raw(run[field]['path'],run[field]['sha256'])
check(type(prep['returncode'])is int and prep['returncode']==0 and type(run['returncode'])is int and run['returncode']==0 and all(prep[k]is None for k in('build_seal','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')),'PREP remains int0 no promotion; successful actual RUN int0')
x=obj(D/'result.json',root['actual_host_result_sha256']);w=obj(D/'intake/admit.watchdog.json');st=obj(D/'STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json')
check(typed(obj(D/'host.stdout',root['actual_host_stdout_sha256']),x) and raw(D/'host.stderr',root['actual_host_stderr_sha256'])==b'','full hoststdout vs result order/types/floatbits and real empty stderr')
command=[P12,str(F),'admit','--sha256',SS,'--terminal-evidence',str(T/'terminal_return.json'),'--terminal-evidence-sha256',RS]
check(len(command)==9 and x['actual_command']==receipt['actual_API_command']==st['stages'][0]['command']==w['command']==command,'original exact nine-token standard3argument CLI')
check(receipt['actual_host_command']==[P12,payload['host.py']['path']]and d['python_command']==P12,'original interpreter and host command')
check(list(st)==['stages']and len(st['stages'])==1 and typed(x['stage_records'],st['stages'],False)and typed(x['watchdog'],w),'whole one stage and watch values/type/floatbits identical; stage file sorted keys')
stage=st['stages'][0];check(stage['label']=='intake/admit'and stage['status']=='PASS'and stage['log_sha256']==AS and stage['elapsed_seconds']==45.897095958993305,'single original PASS stage true whole merged stream')
check(type(w['pid'])is int and w['pid']==20473 and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True,'actual ownPID20473 int0/cleanup/limitNone')
check(w['sampled_peak_rss_mib']==497.84375 and 0<w['sampled_peak_rss_mib']<w['rss_cap_mib']==512 and w['elapsed_seconds']==43.68955924996408 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=stage['wall_cap_seconds']==600,'actual sampled RSS/time under original strict caps')
check(x['whole_elapsed_seconds']==receipt['whole_elapsed_seconds']==49.04454591701506 and stage['elapsed_seconds']<x['whole_elapsed_seconds']<1800,'true host whole elapsed49.0445459')
capkeys=dict(total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512,threads=1,children_at_once=1,retries=0)
for k,v in capkeys.items():check(type(x[k])is int and type(receipt[k])is int and x[k]==receipt[k]==v,'whole host original cap '+k)
for k,v in dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,threads=1,numeric_children_at_once=1,retries=0,archive_reserve_bytes=2*2**30,artifact_budget_bytes=96*2**30,min_free_bytes=8*2**30).items():check(type(d[k])is int and d[k]==v,'declaration original cap '+k)
false=('cold_controller_imported','cold_controller_bound','cold_prepared','physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')
for doc in (x,receipt):
 for k in false:check(doc[k]is False,'actual INPUT scopefalse '+k)
check(x['canonical_old_modules_only_in_isolated_process']is True and x['child_stderr_combined_into_actual_log']is receipt['child_stderr_combined_into_actual_log']is True and x['separate_child_stderr_observation_claimed']is receipt['separate_child_stderr_observation_claimed']is False,'original old modules only and merged child stderr no fictitious separate stream')
for key in ('producer','declaration','build_seal','actual_run','actual_PREP','actual_API_whole_merged_stream','actual_API_whole_return','supervisor_source','parent_source','bounded_helper'):raw(x[key]['path'],x[key]['sha256'])
check([x[k]['sha256']for k in('producer','declaration','build_seal','actual_run','actual_PREP')]==[FS,DS,SS,RS,PS],'all actual factory and four independent build witnesses exact')
check(x['supervisor_source']['sha256']=='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'and x['parent_source']['sha256']=='38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'and x['bounded_helper']['sha256']=='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09','whole original genuine MRO three source pins')
for snapshot in (x['resources_before'],x['resources_after'],stage['resource_before'],stage['resource_after']):
 check(snapshot['declared_resource_roots']==d['resource_roots']and set(d['resource_roots']).issubset(snapshot['resource_roots'])and snapshot['resource_scope_contract']==d['resource_scope_contract']and snapshot['resource_scope_policy']==d['resource_scope_policy'],'all actual host historical declared roots and resource contract retained')
 check(snapshot['artifact_budget_bytes']==96*2**30 and snapshot['min_free_bytes']==8*2**30 and snapshot['artifact_bytes']+2*2**30<96*2**30 and snapshot['disk_free_bytes']-2*2**30>=8*2**30,'actual resources original96/free8/reserve2 budgets')
api=obj(D/'intake/admit.log',AS); check(PINS[str(D/'intake/admit.log')]['bytes']==25266286,'whole25266286B actual API stream')
spec=obj(S/'input_specs.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'); original=obj(A/'combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
check(typed(spec,original),'whole19.356767MB original2cad ordering/type/floatbits unchanged'); bodies=spec['metadata']['historical_actual_components']; historical=obj(B/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json','aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
check(len(bodies)==7 and typed(bodies,historical['actual_components'],False)and digest(bodies)=='a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130','whole original seven historical declaration value/type/floatbits equality across its sorted serialized2cad clone')
trim=obj(S/'trim_component_admission_INPUT.json','a4662b853831357c299de0c28d1d19e2a869f81c6308081f6fa1d7833fd797bb'); oldtrim=obj(A/'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
check(len(trim)==73 and typed(trim,oldtrim),'full original fed209 trim73 no filtering or scalar/type/order/floatbits changes')
terminal=dict(receipt=dict(path=str(T/'terminal_return.json'),sha256=RS),full_stdout=run['full_stdout'],full_stderr=run['full_stderr'],command=run['command'],schema=run['schema'],**{k:run[k]for k in('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')})
descriptor=dict(d['files'])
def own(path,h):
 path=str(path);check(path not in descriptor or descriptor[path]==h,'descriptor pin conflict');descriptor[path]=h
for name,h in seal['files'].items():own(O/name,h)
own(O/'seal.json',SS)
for k in('receipt','full_stdout','full_stderr'):own(terminal[k]['path'],terminal[k]['sha256'])
own(d['input_graph']['path'],d['input_graph']['sha256'])
for p in(dict(path=str(T/'declaration_terminal_return.json'),sha256=PS),prep['source_inventory'],prep['full_stdout'],prep['full_stderr']):own(p['path'],p['sha256'])
def pin(path):return dict(path=str(path),sha256=descriptor[str(path)])
prefix=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='PREFIX'for t in n.targets))
expected=dict(schema=prefix+'_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1',admission='COMBINED_RUNTIME_INPUT_ONLY',build_root=str(O),source_root=str(S),build_seal_sha256=SS,
 corrected_runtime=pin(O/'runtime/Dragon'),compiled_trim_kernel=pin(B/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008/build/SPOT1P64.o'),inherited_compiled_dedup_kernel=pin(B/'axial-material-rank1-factor-cache-memory-dedup-build-20261007/build/SPOT1P64.o'),compiled_physical_assembly=pin(B/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007/build/SPOASM.o'),
 actual_local_supervisor_helper=d['actual_local_supervisor_helper'],actual_supervisor_constructor_preflight=d['actual_supervisor_constructor_preflight'],source_admission=pin(S/'source_admission.json'),compiled_link_identity=pin(O/'audit/binary_identity.json'),production_link_command=d['production_link_command'],actual_components=bodies,actual_last_cprime_trim_admission=trim,actual_last_cprime_trim_component_INPUT=d['actual_last_cprime_trim_component_INPUT'],trim_component_INPUT_semantics='ACTUAL_TRIM_3ARG_RETURN_IN_THIS_PREP_THEN_COMPLETE_FRESH_INPUT_REUSE_NO_API_REEXECUTION',trim_API_executed_in_this_consumer=False,component_INPUT_semantics='HISTORICAL_PREP_REUSE_WITH_COMPLETE_FRESH_PHASES_NOT_API_REEXECUTION',original_component_APIs_executed_now=False,historical_whole_component_body=d['historical_whole_component_body'],actual_prepare_terminal_evidence=dict(path=str(T/'declaration_terminal_return.json'),sha256=PS),
 descriptor_files=descriptor,input_aliases=d['complete_input_aliases'],historical_input_graph=d['input_graph'],original_two_literal_aliases=d['aliases'],complete_literal_owner_edges_preserved_by_graph=True,inherited_rank1_cache_admission=bodies['original92'],inherited_physical_admission=bodies['physical'],inherited_dedup_admission=bodies['dedup'],inherited_rank1_factor_cache_memory_admission=bodies['dedup']['inherited_rank1_factor_cache_memory_admission'],original_operator_capture_dependency=bodies['capture'],future_contract=bodies['original92']['future_contract'],actual_external_terminal_evidence=terminal['receipt'],actual_external_terminal_validation=terminal,resource_scope_policy='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1',resource_scope_contract=d['resource_scope_contract'],actual_resource_class_factory=bodies['dedup']['actual_resource_class_factory'],sole_object_changes=['SPOT1P64.o','SPOASM.o'],
 all_other_original92_tokens_unchanged=True,mathematical_controls_inherited_not_newly_executed=True,physical_self_operator_changed=True,retained_cache_mathematics_and_rhs_order_unchanged=True,observer_objects_linked=False,future_actual_FLU_observer_required=trim['future_actual_FLU_observer_required'],future_actual_factor_cache_observer_required=trim['future_actual_factor_cache_observer_required'],white_closure_unchanged=True,angle_grid_unchanged=True,radial_arithmetic_unchanged=True,physical_data_unchanged=True,collision_self_operator_unchanged=False,original_accuracy_thresholds_changed=False,no_CE_fitting=True,original_operator_capture_RSS_scope_not_transferred=True,trim_native_RSS_proof_obtained=False,fresh_trim_native_capture_required=trim['fresh_512MiB_native_capture_required'],fresh_combined_runtime_cold_AAA_required=True,original_cold_storage_reservation_still_required=True,production_pipeline_prepared=False,native_transport_executed=False,combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
ret=next(n.value for n in fd['production_admission'][0].body if isinstance(n,ast.Return));keys=[k.arg for k in ret.keywords]
check(len(api)==len(expected)==len(keys)==65 and list(api)==list(expected)==keys,'all65 field source order complete')
check(typed(api,expected),'all65 full immutable expectedbody types/order/floatbits complete equality')
for kw in ret.keywords:
 try:v=ast.literal_eval(kw.value)
 except (ValueError,TypeError):continue
 check(typed(expected[kw.arg],v),'source literal math/scope field '+kw.arg)
for k in('corrected_runtime','compiled_trim_kernel','inherited_compiled_dedup_kernel','compiled_physical_assembly','source_admission','compiled_link_identity'):raw(api[k]['path'],api[k]['sha256'])
math_fields=['sole_object_changes','all_other_original92_tokens_unchanged','mathematical_controls_inherited_not_newly_executed','physical_self_operator_changed','retained_cache_mathematics_and_rhs_order_unchanged','observer_objects_linked','white_closure_unchanged','angle_grid_unchanged','radial_arithmetic_unchanged','physical_data_unchanged','collision_self_operator_unchanged','original_accuracy_thresholds_changed','no_CE_fitting','original_operator_capture_RSS_scope_not_transferred','trim_native_RSS_proof_obtained','fresh_trim_native_capture_required','fresh_combined_runtime_cold_AAA_required']
math_paths=[]
def collect(v,path):
 if type(v)is dict:
  for k,x in v.items():
   p=path+'/'+k
   if any(t in k.lower()for t in('dtype','layout','invariant','bitexact','bitwise','shape','rhs_order','threshold','accuracy_threshold','collision_self','physical_data','white_closure','angle_grid','radial_arithmetic')):math_paths.append(dict(path=p,whole_value_digest=digest(x),type=type(x).__name__))
   collect(x,p)
 elif type(v)is list:
  for i,x in enumerate(v):collect(x,path+'/'+str(i))
collect(bodies,'actual_components');collect(trim,'actual_last_cprime_trim_admission')
check(bodies['mathematical_controls_inherited_not_newly_executed']is True and bodies['capture_scope_is_original_operator_only']is True and bodies['combined_runtime_RSS_not_proved']is True,'inherited mathematical controls not newly executed')
peer=Path('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009')
pg=obj(peer/'complete_graph_and_whole_returned_INPUT_review.json','defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8')
pr=obj(peer/'actual_readonly_full_INPUT_review_tool_return.json','7031ba726192399afedb53cd4d58b4a70ae92cbd7e28e19d8358c379e179e41e')
check(pg['status']=='PASS'and pg['actual_whole_return_semantic_sha256']==digest(api)and pg['returned_whole_65_field_builtin_type_floatbits_insertion_order_and_values_equal']is True,'complementary peer65 and graph report actual freshPASS samewhole digest')
check(pr['actual_tool_result']['exit_code']==0 and type(pr['actual_tool_result']['exit_code'])is int and pr['actual_tool_result']['closed']is True and pr['record_written_after_actual_terminal_return']is True,'peer genuine completed metadata read0')
check(pg['original_graph_canonical_count']==35647 and pg['returned_descriptor_files_count']==len(descriptor)==35675 and pg['graph_declared_roots_count']==231 and pg['current_dynamic_roots_count']==232 and pg['all_declared_history_roots_retained']is True,'peer fullgraph descriptor/current232 dynamicroots not frozen oldcount')
prior=obj(Path('/private/tmp/spot_v9_actual_successful_RUN_source_witness_independent_review_20261009/REPORT.json'),'7d8cf7e73725a033eff1e5419b870e69fa7c121b2f8fdf285440e604d46b6c48')
check(prior['status']=='PASS','previous actual build source witness scope realPASS frozen')
source_review=obj(Path('/private/tmp/spot_v9_true_host_bound_recorder_source_independent_review_20261009/source_review.json'),'c6379b701adac8239454ad0f61fd63b4260e8706af890178a18ad0914b00e9a9')
check(source_review['status']=='PASS'and source_review['complete_eight_assignment_inverse_wholebyte_exact']is True and source_review['recorder_sha256']==CS,'actual recorder source review complete8assignmentinverse already truePASS/fresh pin')
for p,row in PINS.items():check(identity(Path(p))==row['identity'],'all fullread source/doc/payload pinned identities stable until review end')
report=dict(schema='AXMAT_V9_ACTUAL_BOUND_INPUT_SOURCE_WITNESS_WHOLE_MATH_INDEPENDENT_REVIEW_V1',status='PASS',scope='ACTUAL_HOST_ROOT0_9PAYLOAD_PLUS_RECEIPT_SOURCE11_PREP4_SEALEDOUT22_ORIGINAL65DEFS_WATCH_STREAM_ALL65RETURN_FULL7_TRIM73_TYPE_ORDER_FLOATBITS; graph canonical numeric files verified by separately pinned complementary reviewer',observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),Root_host_tool=actual,Root_recorder_tool=record['actual_recorder_tool'],durable_Root_receipt_sha256=IS,host_sha256=HS,postterminal_recorder_sha256=CS,factory_sha256=FS,declaration_sha256=DS,PREP_sha256=PS,RUN_sha256=RS,build_seal_sha256=SS,whole_API_log_sha256=AS,whole_API_log_bytes=25266286,payload_count=9,independent_tenth_receipt=True,payload_bytes=25886733,payload_namespace_and_all_original_copy_fullSHA=True,SOURCE11_fresh_fullSHA=True,PREP4_frozen_true0_no_RUN_claim=True,OUT22_whole_seal_and_raw_bytes=True,producer_all65defs_byte_and_AST_exact_to_F8=True,producer_definition_pins=fn_pins,original_parser_unchanged=True,parser_pooling_not_adopted=True,one_original_9token_3argument_API_once=True,actual_API_command=command,complete_65key_body_equal_to_all_immutable_original_sources=True,whole65_semantic_sha256=digest(api),whole7_semantic_sha256=digest(bodies),original_trim_key_count=73,whole_trim_semantic_sha256=digest(trim),builtin_scalar_container_type_dict_insertion_list_order_and_finite_float64bits_all_preserved=True,all_redundant_inherited_component_bodies_preserved=True,math_FULL_SCOPE_all_fields_retained=True,math_scope_values={k:api[k]for k in math_fields},math_dtype_layout_shape_invariant_control_entirevalue_pins=math_paths,original_MRO_source_identity_705_38de_bc4_fullSHA=True,actual_watch={k:w[k]for k in('pid','returncode','elapsed_seconds','sampled_peak_rss_mib','limit_failure','wall_cap_seconds','rss_cap_mib','own_child_only','liveness_group_cleanup')},single_stage_PASS_seconds=stage['elapsed_seconds'],actual_host_whole_seconds=x['whole_elapsed_seconds'],caps=capkeys,history_budget_bytes=96*2**30,minimum_free_bytes=8*2**30,reserve_bytes=2*2**30,host_retained_resource_snapshots_declared231_root_complete=True,postrecorder_current_dynamic_roots232_handled_by_peer=True,current_resource_file_count_not_held_to_old_run_or_host_snapshot=True,full_hoststdout_result_deeporder_equal=True,hoststderr_truly_empty=True,wholechild_merged_stdoutstderr_log=True,separate_child_stderr_observation_claimed=False,complementary_complete_graph_review=dict(report_path=str(peer/'complete_graph_and_whole_returned_INPUT_review.json'),report_sha256='defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8',actual_receipt_path=str(peer/'actual_readonly_full_INPUT_review_tool_return.json'),actual_receipt_sha256='7031ba726192399afedb53cd4d58b4a70ae92cbd7e28e19d8358c379e179e41e',actual_tool=pr['actual_tool_result'],canonical_files=35647,descriptor_files=35675,current_dynamic_roots=232),all_fullread_pins=list(PINS.values()),readonly_checks=CHECKS,business_module_import_API_constructor_worker_watch_PREP_RUN_or_native_execution=False,formal_ART_writes=False,files_deleted=False,cold_prepared=False,new_native_transport_or_fullFLU_or_AAA_or_ABA_qualification=False,new_combined_native_RSS_credit=False,allocation_line_or_parser_or_fd3_causal_RSS_claim=False,limits=['This is actual INPUT admission and source/math/metadata preservation evidence; historical mathematical tests are inherited, not rerun.','The sampled497.84375MiB belongs to one true INPUT Python child, not native transport/FLU or a continuous exact peak.','Host resource snapshots predate durable INPUT evidence creation; independently fresh232-root current graph/resource review supplies later dynamic closure.','The35GB canonical numeric content is not reread by this source/witness reviewer: bound complementary true0 reviewer read it completely once.','No target source or business helper is imported/executed; only STDlib bytes/JSON/AST.'])
report['historical_old_DECL_dictionary_order_not_same_as_sorted_original2cad_clone']=True
report['current_API_whole_order_exact_original2cad_and_trim73']=True
report['crossfile_stage_dictionary_sorting_is_retained_original_serialization']=True
report['pure_TMP_reader_first_two_order_assertion_failures_transparently_retained_no_business_replay']=True
with (H/'REPORT.json').open('x')as f:json.dump(report,f,ensure_ascii=False,allow_nan=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
with (H/'REPORT.txt').open('x')as f:f.write('PASS：唯一V9实际INPUT Root0/CLOSED与真正recorder0、全部9payload+独立第10收据、SOURCE11/PREP4/完整OUT22封存、65函数和65返回字段、原2cad全7历史BODY及fed209全73trim逐类型/字典插入顺序/列表顺序/有限浮点64位深等。原MRO705/38de/bc4及512/600/1800/线程1/子1/零重试/历史96GiB/free8/保留2GiB完整。ownPID20473采样497.84375MiB，43.68956s；实际host49.04455s。当前232动态根/完整35GB图由已鲜pin的另一真0独审覆盖，未复读数值。只取得INPUT准入；原数学控制完整继承但未新执行，不取得冷AAA/ABA/native/FLU、combined native RSS或allocation/优化因果信用。未执行业务或修改项目。\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',report=str(H/'REPORT.json'),report_sha256=hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),pins=len(PINS),checks=CHECKS,whole65=True,whole7=True,trim73=True,child_sampled_peak_RSS_mib=497.84375,only_readonly_metadata=True)),flush=True)
