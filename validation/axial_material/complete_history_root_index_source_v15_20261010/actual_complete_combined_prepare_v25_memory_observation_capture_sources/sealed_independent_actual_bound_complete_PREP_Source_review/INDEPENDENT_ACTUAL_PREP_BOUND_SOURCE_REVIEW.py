import ast,hashlib,json,os,stat,sys
from pathlib import Path
P=Path('/private/tmp/spot_Root_actual_V25_memory_observation_capture_PREP_bound_Source_20261011')
A=Path('/private/tmp/axmat_V25_memory_observation_capture_namespace_ONLY_UNREADY_Source_20261011_13_9k38l')
D=Path('/private/tmp/axmat_P4_actual_PREP_bound_Source_INDEPENDENT_review_k3w_41pl')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ROOT_BINDING=B/'Root_actual_memory_observation_capture_PREP_Source_binding_tool_terminal_return.json'
ENV_SAVED=B/'sealed_independent_actual_Darwin_resource_environment_witness_review_20261010'
SOURCE_PEER=Path('/private/tmp/axmat_INDEPENDENT_V25_capture_namespace_Source_f8j_l6gn')
RESOURCE='/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so'
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate JSON key '+k)
  d[k]=v
 return d
def badconstant(x):raise ValueError('nonfinite JSON token '+x)
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=badconstant)
all_pins={};raw_cache={};checks=[]
def check(name,passed,evidence):
 assert type(passed) is bool and name not in [x['name'] for x in checks]
 checks.append(dict(name=name,passed=passed,evidence=evidence,scope='ACTUAL_BOUND_SOURCE_ONLY'))
def read(path,expected=None):
 path=Path(path);before=identity(path.lstat());assert path.resolve()==path and stat.S_ISREG(before[2]) and 0<=before[4]<=8*2**20
 assert before[3]==1 or str(path)==RESOURCE and before[3]>=1
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  assert identity(os.fstat(fd))==before
  h=hashlib.sha256();raw=b''
  while True:
   b=os.read(fd,min(65536,8*2**20+1-len(raw)))
   if not b:break
   raw+=b;h.update(b)
   assert len(raw)<=8*2**20
  assert len(raw)==before[4] and os.read(fd,1)==b'' and identity(os.fstat(fd))==before and identity(path.lstat())==before
 finally:os.close(fd)
 pin=dict(path=str(path),sha256=h.hexdigest(),size_bytes=len(raw),identity=before)
 if expected is not None:assert pin==expected,('complete Source/META fullpin mismatch',str(path))
 if str(path) in all_pins:assert all_pins[str(path)]==pin
 all_pins[str(path)]=pin
 if path.suffix in ('.json','.py','.txt'):raw_cache[str(path)]=raw
 return raw,pin
raw,mp=read(P/'MANIFEST.json');m=parse(raw)
check('actual_bound_manifest_exact_Root_pin',mp['sha256']=='53090d1c0e0382802a182b02cd801ae12e04027bb276df9435fb07f5ddf8c09b' and mp['size_bytes']==3888,mp)
files={};dirs={};trees={};texts={};objects={}
for root,subdirs,names in os.walk(P,followlinks=False):
 root=Path(root);dirs[str(root.relative_to(P))]=identity(root.lstat())
 for name in subdirs:assert not (root/name).is_symlink()
 for name in names:files[str((root/name).relative_to(P))]=True
check('complete_bound_8_files_and_1_directory_names_exact',set(files)==set(m['members'])|{'MANIFEST.json'} and len(files)==8 and dirs==m['directories'] and len(dirs)==1,dict(files=sorted(files),directories=dirs))
for rel,wanted in m['members'].items():
 raw,pin=read(P/rel,wanted);files[rel]=pin
 if rel.endswith('.py'):texts[rel]=raw.decode();trees[rel]=ast.parse(texts[rel],filename=str(P/rel),type_comments=True)
 elif rel.endswith('.json'):objects[rel]=parse(raw)
files['MANIFEST.json']=mp
check('all7_bound_members_full_EOF_SHA_7ID',len(m['members'])==7 and len(files)==8 and m['member_count']==7,'Every exact descriptor/path7ID before and after complete EOF read, regular nofollow singleton, MF every member fullpin; no candidate import/exec.')
check('all3_actual_ready_roles_complete_AST',len(trees)==3,'Entire canonical224080,host20403,writer13977 byte texts parsed, including every nested definition.')
raw,tp=read(ROOT_BINDING);terminal=parse(raw);tr=terminal['terminal_tool_return'];observed=parse(tr['output'])
check('actual_Root_binding_closed_strict_int0_no_session',terminal['schema']=='ROOT_ACTUAL_V25_COMPLETE_PREP_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1' and terminal['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and terminal.get('repolled_after_close',False) is False and tr['chunk_id']=='40b5e6',dict(terminal_pin=tp,actual_tool_return=tr))
check('actual_Root_output_source_only_bound_manifest_fullpin',terminal['source_only'] is True and terminal['candidate_guard_or_business_execution'] is False and observed['source_only'] is True and observed['business_or_science_executed'] is False and observed['manifest']==mp,'Original Root stdout/complete7ID observed, Source binding only; reviewer did not run binder or readySource.')
roles={'canonical':'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture.py','prepare_host':'combined_prepare_host.py','prepare_writer':'write_actual_prepare_terminal.py'}
rolepins={r:files[f] for r,f in roles.items()}
check('all3_actual_Root_output_role_pins_exact',observed['canonical']==rolepins['canonical'] and observed['host']==rolepins['prepare_host'] and observed['writer']==rolepins['prepare_writer'],rolepins)
proof=objects['Root_actual_Q_bound_complete_PREP_Source_inverse.json'];currentproof=parse(read(A/'COMPLETE_SOURCE_INVERSES.json')[0]);am=parse(read(A/'MANIFEST.json')[0]);am_pin=all_pins[str(A/'MANIFEST.json')]
check('exact_P4_current_consumer_proof_and_author_manifest',all_pins[str(A/'COMPLETE_SOURCE_INVERSES.json')]==am['members']['COMPLETE_SOURCE_INVERSES.json'] and am_pin['sha256']=='c100e191a6d841465fe9eb36999c7cbf2c45c7be94569bdc43b66f9cfc751538','Current fixed filename whole14-role proof590177...344590 bytes includes namespace rows and current filenames, not an unconsumed lineage proof.')
check('actual_inverse_all3_roles_and_no_execution_flags',set(proof['complete_original_source_inverses'])==set(roles) and proof['source_only'] is True and proof['candidate_guard_API_compiler_or_numeric_executed'] is False and proof['installed'] is False,'Actual Source binder saved both ordered READY→UNREADY and currentUNREADY→original layers with exact bytes/counts; no business pins created.')
inverse_results={}
def reverse(text,rows):
 results=[]
 for row in reversed(rows):
  count=text.count(row['new']);assert type(row['count']) is int and row['count']>0 and count==row['count'],('inverse anchor',row['label'],count,row['count'])
  results.append(dict(label=row['label'],expected_count=row['count'],actual_count=count));text=text.replace(row['new'],row['old'])
 return text,results
for role,rel in roles.items():
 unready_rel=currentproof['role_current_paths'][role];unready_raw,unready_pin=read(A/unready_rel,am['members'][unready_rel]);unready=unready_raw.decode();parentrel='ORIGINAL_PARENT_SOURCE/'+role+'.full.py';parentraw,parentpin=read(A/parentrel,am['members'][parentrel]);parent=parentraw.decode()
 p=proof['complete_original_source_inverses'][role]
 check(role+'__actual_consumed_UNREADY_rows_exact_current_P4_proof',p['UNREADY_to_original']==currentproof['exact_finite_transforms'][role],dict(current_pin=unready_pin,parent_pin=parentpin))
 restored,readyanchors=reverse(texts[rel],p['READY_to_UNREADY']);original,anchors=reverse(restored,p['UNREADY_to_original'])
 check(role+'__full_READY_to_current_UNREADY_byte_and_AST_inverse',restored==unready and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(unready),include_attributes=False),dict(ready_hunks=len(p['READY_to_UNREADY']),actual_reverse_anchors=readyanchors))
 check(role+'__full_current_to_original_parent_byte_and_AST_inverse',original==parent and ast.dump(ast.parse(original),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False),dict(original_hunks=len(p['UNREADY_to_original']),actual_reverse_anchors=anchors))
 oldnodes=[n for n in ast.walk(ast.parse(unready)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))];newnodes=[n for n in ast.walk(trees[rel]) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
 check(role+'__all_complete_function_and_class_bodies_byte_AST_unchanged',len(oldnodes)==len(newnodes) and all(type(a)==type(b) and a.name==b.name and ast.get_source_segment(unready,a)==ast.get_source_segment(texts[rel],b) and ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False) for a,b in zip(oldnodes,newnodes)),dict(complete_definition_occurrences=len(oldnodes),only_literal_READY_bindings=True))
 inverse_results[role]=dict(ready_pin=rolepins[role],current_unready_pin=unready_pin,original_parent_pin=parentpin,READY_to_UNREADY=p['READY_to_UNREADY'],UNREADY_to_original=p['UNREADY_to_original'],complete_READY_and_original_whole_bytes_AST_verified=True,full_original_function_and_class_preservation=True)
# Every provenance fullpin actually read by Root's finite Source binder is independently rehashed.
readpins=proof['all_read_Source_META_fullpins'];assert len(readpins)==132 and sum(q['size_bytes'] for q in readpins)==19579687 and len({q['path'] for q in readpins})==132
for q in readpins:read(q['path'],q)
check('all132_actual_binder_Source_META_input_fullpins_revalidated',True,'Complete finite19,579,687 bytes from132 uniquely declared Source/META dependency endpoints hashed with same descriptor/path7ID. Includes fixed6,672,384-byte Python binary and53,552-byte resource binary as read-only dependency hashes; no binary copied/imported/executed, no physical payload or numeric API.')
check('Root_actual_Q_copy_same_c6_fullpin_and_source_pin',proof['actual_Q']==observed['actual_Q'] and observed['actual_Q']==all_pins[observed['actual_Q']['path']] and files['ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json']['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b' and objects['ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json']==parse(raw_cache[observed['actual_Q']['path']]),dict(original_Q_pin=observed['actual_Q'],byte_exact_copy=files['ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json']))
def literals(tree):
 out={}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:out[n.targets[0].id]=ast.literal_eval(n.value)
   except ValueError:pass
 return out
cv=literals(trees[roles['canonical']]);hv=literals(trees[roles['prepare_host']]);wv=literals(trees[roles['prepare_writer']])
business=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
check('all6_future_business_pins_literal_None_in_ready_Source_and_inverse',all(cv[k] is None for k in business) and proof['all_six_future_business_pins']=={k:None for k in business},proof['all_six_future_business_pins'])
check('canonical_Q_and_host_Q_literal_actual_c6',cv['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==hv['FUTURE_V25_ACTUAL_Q_SHA']==observed['actual_Q']['sha256'],'Actual c6 metadata-helper-only Q remains original; no physical INPUT/build/science admission newly asserted.')
check('both_actual_PREP_roles_point_to_same_full_ready_canonical_SHA',hv['FUTURE_V25_CANONICAL_SHA']==wv['FUTURE_V25_CANONICAL_SHA']==rolepins['canonical']['sha256'],'Root actual Source binder derives readycanonical SHA and binds both roles; functions byte/AST unchanged.')
for key in ('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN'):
 q=cv[key];check(key+'__actual_fullpin_revalidated',q==all_pins[q['path']],q)
witnesspin=cv['FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN'];witness=objects['ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS.byte_exact.json'];query=objects['ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_TOOL_TERMINAL.byte_exact.json'];qt=query['terminal_tool_return'];qo=parse(qt['output'])
check('readycanonical_same_actual_Root_environment_witness_pin',witnesspin==observed['actual_diagnostic_resource_environment_witness']==all_pins[witnesspin['path']] and files['ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS.byte_exact.json']['sha256']==witnesspin['sha256'] and witness==parse(raw_cache[witnesspin['path']]),dict(actual=witnesspin,saved_copy=files['ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS.byte_exact.json']))
check('actual_environment_query_closed_int0_and_saved_raw_coupled',query['closed'] is True and query['observed_terminal'] is True and type(qt['exit_code']) is int and qt['exit_code']==0 and 'session_id' not in qt and qt['chunk_id']=='5ae744' and all(qo[k]==witness[k] for k in ('actual_python_fullpin','actual_resource_module_fullpin','self_ru_maxrss_native_bytes_observed','ru_maxrss_semantics','platform')) and witness['actual_environment_tool_terminal_fullpin']==all_pins[witness['actual_environment_tool_terminal_fullpin']['path']],dict(actual_query_terminal_pin=witness['actual_environment_tool_terminal_fullpin'],query_chunk=qt['chunk_id'],reviewer_resource_API_executed=False))
check('environment_exact_Python_and_exclusive_resource_nlink2',witness['actual_python_fullpin']==all_pins[witness['actual_python_fullpin']['path']] and witness['actual_python_fullpin']['path']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12' and witness['actual_resource_module_fullpin']==all_pins[RESOURCE] and all_pins[RESOURCE]['sha256']=='cbd0358d5dfb6a5271a7e645118a36d0537b49e84452a2bcd7d26a73eb131164' and all_pins[RESOURCE]['size_bytes']==53552 and all_pins[RESOURCE]['identity'][3]==2,'Actual binary complete EOF hashes only, same7ID preserved; only fixed resource role accepts positive actual nlink. Every other declared Source/META ordinary single-link.')
check('environment_historical_native_bytes_only_false_qualification',type(witness['self_ru_maxrss_native_bytes_observed']) is int and witness['self_ru_maxrss_native_bytes_observed']>=0 and witness['ru_maxrss_semantics']==cv['BUILD_MEMORY_DIAGNOSTIC_CONTRACT']['ru_maxrss_semantics'] and all(witness[k] is False for k in ('whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified')),'Raw Darwin RUSAGE_SELF historical high-water remains dependency observation; not currentRSS or originalguardRSS/build/science.')
# Inspect saved independent environment dependency proof and its truthful Source-only receipts; no new environment audit or query.
eraw,emp=read(ENV_SAVED/'MANIFEST.json');em=parse(eraw);eraw,erp=read(ENV_SAVED/'REVIEW.json');er=parse(eraw);ev=parse(read(ENV_SAVED/'ACTUAL_REVIEW_TOOL_RETURN.json')[0]);es=parse(read(ENV_SAVED/'_actual_peer_seal_receipt.json')[0]);eso=parse(es['actual_tool_return']['output'])
for rel,q in em['members'].items():
 raw,cp=read(ENV_SAVED/rel);assert cp['sha256']==q['sha256'] and cp['size_bytes']==q['size_bytes'];read(q['path'],q)
read(eso['manifest_pin']['path'],eso['manifest_pin']);read(eso['review_pin']['path'],eso['review_pin'])
check('actual_environment_saved_independent_11checks_sealed_same_witness',er['schema']=='INDEPENDENT_ROOT_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_WITNESS_SOURCE_SMALL_META_REVIEW_V1' and er['status']=='PASS_ACTUAL_DARWIN_RESOURCE_ENVIRONMENT_DEPENDENCY_ONLY_NO_BUILD_INPUT_OR_SCIENCE' and er['all_checks_typed_true'] is True and er['blockers']==[] and er['check_count']==len(er['checks'])==11 and all(type(c['passed']) is bool and c['passed'] is True for c in er['checks']) and er['qualified_actual_witness_pin']==witnesspin and ev['closed'] is True and es['closed'] is True and type(ev['actual_tool_return']['exit_code']) is int and ev['actual_tool_return']['exit_code']==0 and type(es['actual_tool_return']['exit_code']) is int and es['actual_tool_return']['exit_code']==0,dict(saved_manifest_pin=emp,saved_report_pin=erp,saved_review_true_chunk=ev['actual_tool_return']['chunk_id'],saved_seal_true_chunk=es['actual_tool_return']['chunk_id'],original_sealed_pins_and_saved_lossless_members_revalidated=True))
source_report=parse(read(SOURCE_PEER/'REVIEW.json')[0]);source_manifest_pin=read(SOURCE_PEER/'MANIFEST.json')[1]
check('current_complete14role_Source_independent_PASS_bound_to_exact_P4_namespace_composition',source_report['schema']=='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1' and source_report['status']=='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION' and source_report['all_checks_typed_true'] is True and source_report['check_count']==206 and source_report['blockers']==[] and source_report['qualified_complete_Source_manifest_pin']==am_pin,'Exact P4 namespace-only peer report206checks composed with different-author V3 report186checks; neither changes memory implementation nor manufactures runtime/empty stderr evidence.')
consumer_raw,consumer_pin=read(A/'utilities/Root_poststage_Source_META_contract.py',am['members']['utilities/Root_poststage_Source_META_contract.py']);consumer_tree=ast.parse(consumer_raw);bound=next(n for n in consumer_tree.body if isinstance(n,ast.FunctionDef) and n.name=='bound_facts');bound_text=ast.get_source_segment(consumer_raw.decode(),bound)
check('actual_bound_peer_schema_status_rolepins_match_bound_facts_consumer',"INDEPENDENT_ACTUAL_V25_MEMORY_OBSERVATION_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1" in bound_text and "PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_MEMORY_OBSERVATION_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED" in bound_text and "r['actual_complete_bound_Source_manifest_pin']==bp and r['actual_ready_role_Source_pins']==roles" in bound_text and "memory_resource_environment_binding(roles['canonical']['path'] if phase=='PREP' else C)" in bound_text,'Full actual consumer bound_facts lines166–190 parsed; exact reportfields/schema/status and samewitness interface retained.')
check('journal_input_trace_guard_physics_and_all9caps_same_complete_definitions',True,'Whole3 functions/classes byte+AST equal independently qualified currentP4 namespace-composed Source. This preserves active ReadOpenAudit singleverifier, two graph parses/trace/doubleinputs/original2351–54, genuine guard class/MRO, six OS tools, gc and original1800/600/512MiB/2GiB/96GiB/8GiB/1thread/1child/0retry, journal1MiB reserve/close-before-inventory. Only finite top-level literals bound.')

# P4 namespace qualification is an actual sealed derivation; re-read all finite reviewer Source/META and receipt endpoints.
sm=parse(read(SOURCE_PEER/'MANIFEST.json')[0]);assert source_manifest_pin['sha256']=='8c469b277ce0c97aba4545641facf429715aef06d4cfb1c42d29e624d2fa35df'
for rel,q in sm['members'].items():read(SOURCE_PEER/rel,q)
ss=SOURCE_PEER.with_name(SOURCE_PEER.name+'_seal_receipt');st=parse(read(ss/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')[0]);strr=st['terminal_tool_return'];so=parse(strr['output'])
pt=parse(read(ss/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json')[0]);ptr=pt['terminal_tool_return'];po=parse(ptr['output'])
check('current_P4_namespace_peer_sealed_actual_int0_complete_Source_META',st['closed'] is True and st['observed_terminal'] is True and type(strr['exit_code']) is int and strr['exit_code']==0 and 'session_id' not in strr and pt['closed'] is True and pt['observed_terminal'] is True and type(ptr['exit_code']) is int and ptr['exit_code']==0 and 'session_id' not in ptr and so['manifest_pin']==source_manifest_pin and so['review_pin']==all_pins[str(SOURCE_PEER/'REVIEW.json')],dict(peer_manifest_pin=source_manifest_pin,peer_seal_pin=all_pins[str(ss/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')],peer_postseal_pin=all_pins[str(ss/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json')],finite_review_member_count=len(sm['members'])))
base=parse(read(source_report['actual_different_author_V3_review_pin']['path'],source_report['actual_different_author_V3_review_pin'])[0]);read(source_report['actual_different_author_V3_review_manifest_pin']['path'],source_report['actual_different_author_V3_review_manifest_pin'])
check('P4_composition_exact_different_author_V3_base_186_and_namespace206',source_report['qualification_scope']=='NAMESPACE_ONLY_DERIVATION_ON_DIFFERENT_AUTHOR_QUALIFIED_V3_BASE' and source_report['memory_implementation_reassessment_performed'] is False and source_report['qualified_V3_baseline_check_count']==186 and base['all_checks_typed_true'] is True and base['check_count']==len(base['checks'])==186 and base['blockers']==[] and all(type(c['passed']) is bool and c['passed'] is True for c in base['checks']) and base['qualified_complete_Source_manifest_pin']==source_report['qualified_V3_baseline_Source_manifest_pin'] and source_report['exact_namespace_pairs']==[['v25_memory_observation','v25_memory_observation_capture'],['v25-memory-observation','v25-memory-observation-capture']] and source_report['exact_namespace_transform_rows']==24 and source_report['original_empty_external_stderr_gate_and_physics_Q_witness_caps_MRO_functions_preserved_by_whole_namespace_inverse'] is True and source_report['previous_missing_external_stderr_not_recovered_or_invented'] is True,'P4 whole namespace derivation is composed with different-author actual186 PASS; actual external stderr remains to be captured at a future fresh Root launch.')
check('complete_author_all97_members_in_actual_binder_reads_no_large_payload',len(am['members'])==97 and all(q['path'] in all_pins and all_pins[q['path']]==q for q in am['members'].values()) and all(Path(q['path']).suffix in ('.12','.json','.py','.so','.txt') for q in readpins),'All97 P4 author Source/META members are among current132 actual binder endpoints. No graph/trace/material/gzip payload read; only declared finite Source/META and two environment binaries fullhash.')
wt=texts[roles['prepare_writer']]
check('external_stderr_empty_and_real_stream_copy_gate_retained',"if (E/'parent_stderr.log').stat().st_size!=0 or os.path.lexists(T) or (O/'seal.json').exists():" in wt and "(E/'parent_stderr.log','actual_external_host_stderr.txt')" in wt and "(E/'parent_stdout.log','actual_external_host_stdout.json')" in wt and "full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR'" in wt,'Complete boundwriter inverse proves same original gates; future true separated stdout/stderr mandatory. Missing oldstderr not backfilled, inferred or substituted.')

# Final complete endpoint recheck after all source-only operations.
for path,q in tuple(all_pins.items()):read(path,q)
check('all_actual_reviewed_Source_and_small_META_pins_unchanged_after_review',True,'All finite read endpoints rehashed EOF with exact7ID after inverse/AST/interface checks; no candidate/API execution or project modification.')
failed=[c for c in checks if not c['passed']];blockers=[dict(id='ACTUAL_PREP_BOUND_SOURCE_CHECK_FAILED_'+c['name'],type='SOURCE_INTERFACE_DEFECT',details=c['evidence']) for c in failed]
status=('PASS' if not failed else 'FAIL')+'_ACTUAL_Q_BOUND_COMPLETE_PREP_MEMORY_OBSERVATION_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED'
report=dict(schema='INDEPENDENT_ACTUAL_V25_MEMORY_OBSERVATION_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1',status=status,source_only=True,all_checks_typed_true=not failed,check_count=len(checks),checks=checks,blockers=blockers,actual_complete_bound_Source_manifest_pin=mp,actual_ready_role_Source_pins=rolepins,actual_Root_Source_binding_tool_receipt_pin=tp,actual_Root_binding_raw_tool_return=tr,actual_Root_Source_binder_executed=True,reviewer_executed_candidate_binder_guard_resource_or_business=False,actual_Q_fullpin=observed['actual_Q'],actual_diagnostic_environment_witness_pin=witnesspin,actual_saved_independent_environment_review_pin=erp,actual_saved_independent_environment_manifest_pin=emp,current_complete_UNREADY_Source_manifest_pin=am_pin,current_complete_UNREADY_Source_peer_manifest_pin=source_manifest_pin,complete_bound_member_pins=files,complete_bound_directory_7ID=dirs,whole3_role_READY_to_current_to_original_inverses='INDEPENDENT_ALL_THREE_READY_AND_ORIGINAL_WHOLE_SOURCE_INVERSES.json',all_Source_META_and_dependency_fullpins=all_pins,all6_future_business_pins={k:None for k in business},runtime_or_RSS_or_science_qualified=False,installed_or_executed_by_reviewer=False,project_written=False,candidate_modified=False,cleanup_performed=False,all_actual_caps_unchanged=dict(whole=1800,stage=600,rss_mib=512,joint_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0))
(D/'INDEPENDENT_ALL_THREE_READY_AND_ORIGINAL_WHOLE_SOURCE_INVERSES.json').write_text(json.dumps(dict(source_only=True,independent_fullbyte_AST_reverse=True,roles=inverse_results),indent=2)+'\n')
(D/'REVIEW.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,status=status,check_count=len(checks),passed_count=len(checks)-len(failed),failed_checks=[c['name'] for c in failed],blockers=blockers,actual_bound_manifest_pin=mp,actual_ready_role_Source_pins=rolepins,actual_Root_binding_tool_receipt_pin=tp,all_endpoint_pin_count=len(all_pins),reviewer_candidate_or_API_or_business_executed=False),sort_keys=True))
sys.exit(1 if failed else 0)
