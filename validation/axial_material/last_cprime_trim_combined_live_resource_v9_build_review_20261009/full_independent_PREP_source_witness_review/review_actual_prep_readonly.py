from pathlib import Path
import os,stat,hashlib,json,ast,math,datetime,collections
ROOT=Path('/Users/wen/spot'); A=ROOT/'validation/axial_material'; B=ROOT/'validation/artifacts'
R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'; T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
S=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
O=B/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
TERM=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
DST=Path('/private/tmp/spot_v9_actual_PREP_source_witness_independent_review_20261009')
F=A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
F8=A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'
TRIM=B/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008'; TS=B/'axial-material-qualified-AB-rank1-factor-cache-last-cprime-trim-build-admission-20261008'; TT=B/'axial-material-qualified-AB-rank1-factor-cache-last-cprime-trim-build-terminal-20261008'
F_SHA='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'; D_SHA='7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0'; P_SHA='0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb'; OBS_SHA='c5f622740e5a7e554993ec51dd12b7ae4b7fb5bfd0cf5b0c3834cb023d4ec7a7'
PINS={}; checks=[]
def check(v,label):
 if not v:raise AssertionError(label)
 checks.append(label)
def identity(p):
 s=p.lstat();check(stat.S_ISREG(s.st_mode) and not p.is_symlink(),'regular nonlink '+str(p));return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,expected=None):
 p=Path(p);before=identity(p);v=p.read_bytes();after=identity(p);check(before==after,'stable read '+str(p));h=hashlib.sha256(v).hexdigest()
 if expected:check(h==expected,'full SHA '+str(p))
 PINS[str(p)]=dict(path=str(p),size=len(v),sha256=h,identity=before);return v

def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d

def finite(v):
 if type(v) is float:check(math.isfinite(v),'finite JSON value')
 elif type(v) is dict:
  for k,x in v.items():check(type(k)is str,'builtin str key');finite(x)
 elif type(v)is list:
  for x in v:finite(x)
 else:check(type(v)in (str,int,bool,type(None)),'plain builtin scalar')

def obj(p,expected=None):
 v=json.loads(raw(p,expected),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)));finite(v);return v

def typed_equal(x,y):
 if type(x)is not type(y):return False
 if type(x)is dict:return x.keys()==y.keys() and all(typed_equal(x[k],y[k])for k in x)
 if type(x)is list:return len(x)==len(y)and all(typed_equal(a,b)for a,b in zip(x,y))
 if type(x)is float:return x.hex()==y.hex()
 return x==y

def cd(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()
source=raw(F,F_SHA).decode();f8=raw(F8,'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4').decode()
def definitions(text):
 tree=ast.parse(text);return {n.name:(n,ast.get_source_segment(text,n))for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
n9=definitions(source);n8=definitions(f8);check(len(n9)==len(n8)==65 and n9.keys()==n8.keys(),'65 complete top definitions remain')
defs=[]
for name,(n,text)in n9.items():
 m,old=n8[name];check(text==old and ast.dump(n,include_attributes=False)==ast.dump(m,include_attributes=False),'byte/AST unchanged '+name);defs.append(dict(name=name,line=n.lineno,source_sha256=hashlib.sha256(text.encode()).hexdigest()))
check(n9['strict_json_bytes'][1]==n8['strict_json_bytes'][1],'original strict parser retained; sharing parser not adopted')
for text in ["TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512","RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30","THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')"]:check(text in source,'original cap/thread source '+text)
d=obj(O/'declaration.json',D_SHA);p=obj(TERM/'declaration_terminal_return.json',P_SHA);obs=obj(R/'prepare_terminal_tool_return.json',OBS_SHA);check(obj(R/'prepare_terminal_return.json',P_SHA)==p,'formal R PREP byte copy')
check(type(obs['exit_code'])is int and obs['exit_code']==0 and obs['closed'] is True,'Root true builtin integer0 closed PREP');check((obs['initial_chunk_id'],obs['session_id'],obs['terminal_chunk_id'])==('ef22f4',60763,'f4b055'),'genuine Root PREP tool handle')
check(p['actual_tool_result']==obs and type(p['returncode'])is int and p['returncode']==0,'receipt embeds exact Root observation/int0')
check(obs['Root_tool_return_observed_before_receipt']is True and obs['business_RUN_started']is False and obs['native_RSS_or_science_credit']is False,'Root PREP-only scope')
check(p['record_producer']=='root' and p['actual_tool_terminal_return_observed']is True and p['record_written_after_actual_terminal_return']is True,'external Root producer observed before written receipt')
py='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12';cmd=[py,str(F),'prepare-build'];check(p['command']==obs['command']==cmd,'standard PREP CLI')
check(p['source']==dict(path=str(F),sha256=F_SHA) and p['declaration']==dict(path=str(O/'declaration.json'),sha256=D_SHA),'actual source/declaration bindings')
expected_files={'input_specs.json','historical_input_combined_runtime_factory.py','source_admission.json','trim_component_admission_INPUT.json','trim_component_API_python_open_trace.json','trim_component_API_absence_INPUT.json',*(f'runtime/{x}.py'for x in ('graph','codec','current','checks','ordinary'))}
inv=d['source_inventory'];check(set(inv['files'])==expected_files and inv['symlinks']=={} and inv['directories']==['runtime'],'complete SOURCE inventory11/one dir/nolinks')
actual_files=set();actual_dirs=set()
for folder,dirs,names in os.walk(S,followlinks=False):
 for n in dirs:check(not (Path(folder)/n).is_symlink(),'SOURCE directory not link');actual_dirs.add(str((Path(folder)/n).relative_to(S)))
 for n in names:actual_files.add(str((Path(folder)/n).relative_to(S)))
check(actual_files==expected_files and actual_dirs=={'runtime'},'fresh SOURCE complete member names')
for name,wanted in inv['files'].items():raw(S/name,wanted)
check(obj(TERM/'declaration_source_inventory.json',p['source_inventory']['sha256'])==inv,'fresh four PREP inventory witness equals declaration')
check(p['source_inventory']['path']==str(TERM/'declaration_source_inventory.json'),'inventory witness exact TERMpath')
term_members={x.name for x in TERM.iterdir()};check(term_members=={'declaration_full_stderr.txt','declaration_full_stdout.json','declaration_source_inventory.json','declaration_terminal_return.json'},'exact4 PREP witness members no future run receipt')
out=raw(TERM/'declaration_full_stdout.json',p['full_stdout']['sha256']);err=raw(TERM/'declaration_full_stderr.txt',p['full_stderr']['sha256']);check(out==raw(T/'prepare.stdout') and err==raw(T/'prepare.stderr') and err==b'','full raw stdout/stderr exact TERM/T and emptystderr')
check(json.loads(out)==dict(declaration=str(O/'declaration.json'),declaration_sha256=D_SHA),'complete stdout pointer');check(p['full_stdout']['path']==str(TERM/'declaration_full_stdout.json')and p['full_stderr']['path']==str(TERM/'declaration_full_stderr.txt'),'stdoutstderr exact paths')
check(obs['actual_stdout_sha256']==p['full_stdout']['sha256'] and obs['actual_stderr_sha256']==p['full_stderr']['sha256'],'Root raw full SHA matcheswitness')
for k in ('build_seal','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'):check(p[k]is None,'PREP future '+k+' None')
for k in ('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','scientific_qualification','successful_new_runtime_build_observed','original_component_APIs_executed_now','successful_combined_link_completion_observed','production_admission_observed'):check(p[k]is False,'PREP no credit '+k)
check(p['successful_declaration_input_observed']is True and p['trim_component_API_executed_in_this_PREP']is True and p['planned_total_stages']==5 and type(p['compiled_or_numeric_stages_started'])is int and p['compiled_or_numeric_stages_started']==0,'PREP inputsuccess only zero compiled/numeric stages')
check(p['input_file_pins']==len(d['files'])==35647 and p['archive_reserve_bytes']==2*2**30,'full inputcount/reserve receipt')
for name in ('seal.json','driver_result.json','binary_identity.json','audit/audit_result.json', 'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V9/stages.json'):
 check(not os.path.lexists(O/name),'no RUN outcome '+name)
for name in ('build','audit','metadata','HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V9'):check(list((O/name).iterdir())==[],'PREP createdempty '+name)
check({x.name for x in (O/'runtime').iterdir()}=={'run_bounded_dragon.py'},'no newly linked runtime')
config=obj(T/'config.json');check(config['factorySha']==F_SHA and config['declarationSha']==D_SHA and config['prepSha']==P_SHA,'actual liveconfig three pinnedobservations')
for k in ('sealSha','terminalPath','terminalSha','failed_terminal_sha'):check(config[k]is None,'config future '+k+' None')
raw(T/'record_root_terminal.py','b534c49f046d3869dba07e4101e907bd08de8c61599bc3a05a688a0733de5d9e')
helpers={'graph':('combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py','1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'),'codec':('combined_runtime_typed_specs_codec.py','758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69'),'current':('combined_runtime_current_predicates_final_private_last_uses_20261009.py','fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19'),'checks':('combined_runtime_historical_input_checks.py','86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e'),'ordinary':('combined_runtime_current_ordinary_path_checks.py','47e7f9eb2e7ff89e96c30b91f98a25d37d66d82a029dcfbf4845c8f5968482d5')}
check(raw(S/'historical_input_combined_runtime_factory.py',F_SHA)==source.encode(),'copied fullfactory byteexact')
for role,(name,wanted)in helpers.items():check(raw(A/name,wanted)==raw(S/f'runtime/{role}.py',wanted),'formal/copy byteexact helper '+role)
specsha='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa';specpath=A/'combined_runtime_complete_historical_input_specs_20261007.json'
encoded=obj(specpath,specsha);saved=obj(S/'input_specs.json',specsha);check(typed_equal(encoded,saved),'whole19356767 typed metadata exact copy')
original=obj(B/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json','aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
body=encoded['metadata']['historical_actual_components'];seven={'original92','physical','dedup','capture','mathematical_controls_inherited_not_newly_executed','capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved'};check(set(body)==seven and typed_equal(body,original['actual_components']),'whole original seven keys/full typed deep equality')
check(cd(body)=='a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130','full original seven canonical value SHA')
check(body['mathematical_controls_inherited_not_newly_executed']is True and body['capture_scope_is_original_operator_only']is True and body['combined_runtime_RSS_not_proved']is True,'originalseven INPUT only false native transfer')
for k in ('historical_whole_component_body','historical_PREP','input_graph','actual_last_cprime_trim_component_INPUT'):check(p[k]==d[k],'PREP/declaration binding '+k)
check(d['historical_whole_component_body']==dict(path=str(specpath),sha256=specsha,encoding_schema='AXMAT_COMBINED_RUNTIME_LOSSLESS_TYPED_INPUT_METADATA_ENCODING_V1',pointer='/metadata/historical_actual_components',whole_seven_key_body_retained=True,original_component_API_execution_claimed=False,historical_FAILED_RUN_promoted=False),'full body pointer/scope binding')
trim=obj(S/'trim_component_admission_INPUT.json','a4662b853831357c299de0c28d1d19e2a869f81c6308081f6fa1d7833fd797bb');trimoriginal=obj(A/'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
check(typed_equal(trim,trimoriginal),'full74keys actual original fed209 trim typed deep equality no field filtering')
check(trim['inherited_rank1_factor_cache_admission']==body['original92'] and trim['inherited_rank1_factor_cache_memory_admission']==body['dedup']['inherited_rank1_factor_cache_memory_admission'],'fulltrim inherited original andmemory bodies exact')
check(trim['resource_scope_contract']==body['original92']['resource_scope_contract'],'fulltrim originalresourcecontract')
td=obj(TRIM/'declaration.json','e6dd804a473ae25888ecf5e070af708a024618772c0f753d836127af6074dc00');ta=obj(TS/'source_admission.json','559b25aa80ff165ce6edc756de9c9309929288c5e601ef2ce71a1e9805c11677')
obj(TRIM/'seal.json','38f44fe55187199e467f8445015e505814cf0df911d9a51d1b35c8e264bb0e0e');obj(TT/'terminal_return.json','076565db2dc0048db70166d37bd6e81107d30acb9a72b14945b436a473094a88')
check(ta['control_contract']==td['control_contract'] and ta['last_cprime_trim']==td['control_contract']['last_cprime_trim'],'wholetrim actualsource controlcontract exact')
check(td['production_link_command']==td['build_commands'][1]==trim['production_link_command'],'full literal trimlinkcommand')
for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed','production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted'):check(trim[k]is False,'actualtrim no science/newRSS '+k)
check(trim['actual_control_rows']==112 and trim['actual_selector_invocations']==224 and trim['actual_source_unit_invocations']==192 and trim['newly_executed_original_interface_receiver_calls']==0 and trim['newly_executed_native_receiver_calls']==2710,'full original trim control counts retained')
check(ta['source_patch_proof']['last_cprime_trim']['complete_inverse_to_dedup_byteexact']is True and ta['source_patch_proof']['last_cprime_trim']['full_33_rhs_solve_unchanged']is True,'trim original inverse/mathproof retained')
trace=obj(S/'trim_component_API_python_open_trace.json','160186407ddc6dcc219a359b3c69e03075e45c459032780f2f043755a18a4d50');check(trace['schema']=='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' and trace['coverage']=='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' and trace['subprocess_records']==[],'actual trace attempt-only/nosubprocess')
check(trace['record_storage']=='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS' and trace['success_of_open_attempt_is_not_observed']is True and trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced']is True,'honest trace coverage limitations retained')
rows=trace['records'];keys=[]
for row in rows:
 check(type(row['attempt_count'])is int and row['attempt_count']>0 and row['event']=='open' and row['observation']=='OPEN_ATTEMPT','positive genuine open-attempt record');keys.append(cd({k:v for k,v in row.items()if k!='attempt_count'}))
check(len(rows)==trace['unique_records']==23935 and len(set(keys))==len(rows) and sum(x['attempt_count']for x in rows)==trace['actual_read_open_attempts']==139942,'complete raw normalized trace actualcounts/unique allretained')
check(any(x.get('path')==str(A/'prepare_qualified_AB_rank1_factor_cache_last_cprime_trim_production.py')for x in rows),'trace binds original trimfactory read')
negative=obj(S/'trim_component_API_absence_INPUT.json','e0313410478a31c38055f700dbc02cc8ca300de7198cfb30ea900de453fa59d8');check(len(negative['absence_inputs'])==len(negative['observations'])==445 and negative['aliases']==[] and negative['absence_inputs'].keys()==negative['observations'].keys(),'all445 exactsource cache absences retained')
for path,v in negative['absence_inputs'].items():
 obs0=negative['observations'][path];owner=v['owner'].removesuffix('#OPTIONAL_CURRENT_INTERPRETER_CACHE');check(owner in td['files'] or owner==str(A/'prepare_qualified_AB_rank1_factor_cache_last_cprime_trim_production.py'),'absence source explicitly trim-pinned');check(Path(owner).suffix=='.py' and path==str(Path(owner).parent/'__pycache__'/(Path(owner).stem+'.cpython-312.pyc')) and not os.path.lexists(path),'currentexact .12optionalcache absent');check(obs0['path']==path and obs0['missing_errno']==2 and obs0['regular_input_bytes']==0 and obs0['observation']=='EXACT_DECLARED_ENOENT_ONLY','original absence observation honest')
admission=obj(S/'source_admission.json',inv['files']['source_admission.json']);check(len(admission)==17,'full17 sourceadmission fields')
for k in ('link_inverse','historical_whole_component_body','historical_PREP','prior_failed_PREP_input','actual_last_cprime_trim_component_INPUT'):check(admission[k]==d[k],'source/declaration actual binding '+k)
check(admission['trim_component_API_executed_in_this_PREP']is True and admission['original_component_APIs_executed_now']is False and admission['historical_failed_combined_RUN_grants_success']is False and admission['combined_runtime_native_RSS_not_proved']is True,'source INPUT-only physical/historical control scope')
caps=dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,threads=1,numeric_children_at_once=1,retries=0,archive_reserve_bytes=2*2**30,artifact_budget_bytes=96*2**30,min_free_bytes=8*2**30)
for k,v in caps.items():check(type(d[k])is int and d[k]==v and td[k]==v,'original unchanged literal caps '+k)
check(d['stages']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'],'all5 originalstage labels')
check(d['python_command']==py and d['build_python_executable']==str(Path(py).resolve())==original['build_python_executable'],'same genuine Python3.12 interpreter')
mro=d['actual_supervisor_constructor_preflight'];check(mro['actual_original_constructor_exercised']is True and mro['native_or_numeric_child_launched']is False and mro['class_name']=='OwnRSSSerialExecutor' and mro['genuine_parent_class_name']=='SerialExecutor','genuine original MRO constructor PREP witness nochild')
for k in ('local_bounded_helper','genuine_supervisor_source','genuine_parent_class_source'):
 v=mro[k];raw(v['path'],v['sha256']); dk={'local_bounded_helper':'actual_local_supervisor_helper'}.get(k,k);check(d[dk]==v,'declaration full real MROsource bind '+k)
check(mro['local_bounded_helper']==dict(path=str(O/'runtime/run_bounded_dragon.py'),sha256='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),'actual local boundedhelper bc4 unchanged')
check(mro['genuine_supervisor_source']['sha256']=='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'and mro['genuine_parent_class_source']['sha256']=='38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128','genuine frozen supervisor705/parent38de')
for path in d['actual_production_objects']:raw(path,d['files'][path])
check(d['original_sender']==dict(path=d['actual_production_objects'][2],sha256=d['files'][d['actual_production_objects'][2]]) and d['original_selector']==dict(path=d['actual_production_objects'][3],sha256=d['files'][d['actual_production_objects'][3]]),'original sender/selector exactbinary bindings')
old=obj(B/'axial-material-rank1-factor-cache-build-20261007/declaration.json');link=list(d['production_link_command']);check(link.count(d['actual_production_objects'][0])==1 and link.count(d['actual_production_objects'][1])==1,'one trim+physical soleoverride tokens');link.remove(d['actual_production_objects'][1]);link[link.index(d['actual_production_objects'][0])]=str(B/'axial-material-rank1-factor-cache-build-20261007/build/SPOT1P64.o');link[-1]=str(B/'axial-material-rank1-factor-cache-build-20261007/runtime/Dragon');check(link==old['build_commands'][2]==d['link_inverse']['original_link_command'],'wholelink original92 inverse exact flags allotherobjects/libraries')
forecast=d['complete_archive_forecast'];check(forecast['total_bound']<2*2**30 and forecast['original_cold_reservation_bytes']==20971764748 and forecast['cold_reservation_reduced']is False and forecast['measured_native_RSS']is False and forecast['roots']==[str(S),str(O)],'fullSOURCE+OUTforecast unchanged2GiB noRSS/nativecredit')
for k in ('original_component_APIs_executed_now','historical_failed_combined_RUN_promoted','mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'):check(d[k]is False,'newDECL scopefalse '+k)
check(d['original_operator_capture_RSS_scope_not_transferred']is True,'originalcaptureRSS nottransferred')
check(d['actual_external_terminal_return_contract']['tail_fields']==['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'] and d['actual_external_terminal_return_contract']['actual_tool_exit_zero_required']is True,'all4 future actualtails and trueRoot0 gate unchanged')
for path,v in PINS.items():check(identity(Path(path))==v['identity'],'allreviewed metadata/source identity stable atclose')
report=dict(schema='AXMAT_V9_ACTUAL_PREP_SOURCE_WITNESS_INDEPENDENT_REVIEW_V1',status='PASS',scope='ACTUAL_PREP_SOURCE11_WITNESS4_WHOLE_HISTORICAL_AND_TRIM_JSON_NO_BUSINESS_EXECUTION',manifest_source_sha256=F_SHA,declaration_sha256=D_SHA,preflight_prepare_terminal_sha256=P_SHA,Root_actual_prepare_tool_observation_sha256=OBS_SHA,Root_actual_prepare_handle=dict(initial_chunk_id='ef22f4',session_id=60763,terminal_chunk_id='f4b055',exit_code=0,closed=True),actual_review_tool_terminal=None,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),SOURCE_all11_fresh_full_SHA_and_complete_names=True,PREP_all4_witnesses_fresh_full_SHA=True,fullraw_stdout_stderr_exact=True,original65_factory_definitions_byte_AST_exact=True,original_parser_retained=True,local_immutable_pool_candidate_adopted=False,whole_original_seven_BODY_full_typed_equal=True,historical_whole_19356767_bytes_copied_SHA=specsha,whole_seven_canonical_value_sha256=cd(body),whole_original_trim_fed209_full74key_typed_equal=True,trim_current_canonical_value_sha256=cd(trim),actual_trim_input_3arg_call_preserved_source_AST=True,trim_open_trace=dict(full_RAW_SHA=PINS[str(S/'trim_component_API_python_open_trace.json')]['sha256'],unique_records=len(rows),actual_read_open_attempts=trace['actual_read_open_attempts'],allrecords_complete_unique_positivecounts=True,subprocess_records=0,coverage=trace['coverage'],successful_open_and_native_libc_HDF5_loader_stat_not_observed=True,V8trace_bytes_not_assumed_equal='This is a fresh PREP attempt trace; source inventory and exact attempt counts are not inherited.'),all445_exact_declaredcache_absence_paths_current_absent=True,all_source_formal_helpers_and_copy_exact=True,genuine705_38de_bc4_MROsource_pins=True,original_sender_selector_physical_trim_production_objects_full_SHA=True,whole_original92_link_token_inverse=True,caps=caps,singlethread_fivekeys_and_true_ctor_MRO_guards_source_unchanged=True,no_new_numeric_or_compiled_stage_started=True,no_seal_driver_binary_tails_RUN_rootreceipt=True,all_RUN_outcomes_None=True,scientific_or_combined_native_RSS_credit=False,reviewer_business_factory_helper_recorder_import_or_execution=False,reviewer_API_constructor_PREP_RUN_watch_worker_called=False,reviewer_formal_ART_written=False,source_ast_definitions=defs,full_fresh_reviewed_pins=list(PINS.values()),checks_passed=len(checks),limitations=['Only readonly STDlib AST/hash/strict whole JSON metadata comparisons were performed. Existing Root PREP actual receipts are verified; this reviewer did not invoke business code or repeat PREP.','Complete 35GB canonical inputs, all graph wire rows, namespace/aliases, path closure, coverage and dynamic231resource roots are being independently audited by graph_serialization_space_review; this report alone is not whole PREP admission until that true audit also passes.','PREP metadata establishes an actual INPUT-return and original constructor witness, not a new runtime build, actual 512MiB combined fit, native full FLU or AAA/ABA qualification.','Live numerical loader/threads are represented by pinned unchanged actual PREP source guards and Root receipts, not reconstructed by importing or calling original constructors in this independent audit.','New V9 RUN is not started/observed in this report. Old V7/V8 nonzero failures remain separate frozen evidence; no allocation line or memory benefit cause is claimed.'])
with (DST/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
with (DST/'REPORT.txt').open('x')as f:f.write('PASS：V9真实PREP成功及SOURCE11/TERM4独立只读复核。Root ef22f4/session60763→f4b055 int0 CLOSED；whole2cad七项BODY与原aa3e全深/类型相等，actual fed209 trim完整74项与a466全深相等。五原阶段/四未来tails、1800/600/512/thread1/onechild/0retry/2GiB/96GiB/free8不变。尚无新RUN/seal/driver/API成功收据；不授予RSS或科学信用。35GB全图和231资源根由另一独立审查者核对，此报告只覆盖源码/收据/完整元数据。未import业务或执行业务。\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',scope=report['scope'],SOURCE_files=11,TERM_PREP_witnesses=4,pins=len(PINS),checks=len(checks),report_sha256=hashlib.sha256((DST/'REPORT.json').read_bytes()).hexdigest(),no_business=True)))
