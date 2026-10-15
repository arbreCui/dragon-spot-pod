from pathlib import Path
import ast, copy, hashlib, json, math, os, stat, struct
H=Path(__file__).resolve().parent;ROOT=Path('/Users/wen/spot');A=ROOT/'validation/axial_material';B=ROOT/'validation/artifacts'
M=Path('/private/tmp/axmat-last-cprime-trim-cold-v9-input-v5-draft-20261009');C=Path('/private/tmp/axmat-last-cprime-trim-cold-v9-qualified-input-bound-candidate-20261009');R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
FNAME='prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py';CNAME='cold_component_input_consumer_last_cprime_trim_own_pid_peak.py';BNAME='cold_owned_specs_last_cprime_trim_component_input_intake_binding_20261009.json'
FS='59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8';CS='2fa0cb00ec458e9bbbbdf2f15db703a1c0547b08d35f585b6c7e6e6274d06d59';BS='b37b9d5adda1fb4a5ffe0f4a4914d513f38f6f68d480be6145f8d4af041572dc'
PINS={}
def ident(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and p.resolve(strict=True)==p
 return[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,wanted=None):
 p=Path(p);before=ident(p);v=p.read_bytes();sha=hashlib.sha256(v).hexdigest();assert ident(p)==before
 if wanted:assert sha==wanted,(str(p),sha,wanted)
 PINS[str(p)]=dict(path=str(p),sha256=sha,bytes=len(v),identity=before);return v
def obj(p,wanted=None):return json.loads(raw(p,wanted))
def typed(x,y):
 if type(x)is not type(y):return False
 if type(x)is dict:return list(x)==list(y)and all(typed(x[k],y[k])for k in x)
 if type(x)is list:return len(x)==len(y)and all(typed(a,b)for a,b in zip(x,y))
 if type(x)is float:return math.isfinite(x)and math.isfinite(y)and struct.pack('!d',x)==struct.pack('!d',y)
 return x==y
admission=obj(R/'Root_actual_whole_INPUT_independent_admission.json','26b6bd4f61e40ba6ecff162360c31c6a14321a1ad7de36b2d82efce8e0b63c65')
assert admission['status']=='QUALIFIED_COMPLETE_INPUT_ONLY_NO_COLD_OR_SCIENCE_CREDIT'and admission['qualified_whole65_whole7_trim73_and_complete_graph_scope']is True
assert all(admission[k]is False for k in('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
for row in admission['preserved_review_files']:assert len(raw(row['path'],row['sha256']))==row['size']
joint=obj(admission['joint_independent_report']['path'],admission['joint_independent_report']['sha256']);assert joint['status']=='PASS'
jrec=obj(R/'full_independent_INPUT_joint_scope_review/actual_readonly_tool_return.json','8be8a730b272ff6853f43678a6e42c36506ea8eed4bb1232333aee4cd97b9e4a')
assert jrec['actual_tool_result']==dict(initial_chunk_id='6bf114',session_id=None,terminal_chunk_id='6bf114',exit_code=0,closed=True)and type(jrec['actual_tool_result']['exit_code'])is int
api=obj(admission['whole_API_return']['path'],admission['whole_API_return']['sha256']);receipt=obj(admission['durable_ROOT_receipt']['path'],admission['durable_ROOT_receipt']['sha256']);D=Path(admission['durable_ROOT_receipt']['path']).parent
assert receipt['actual_tool']==admission['actual_host_tool']and type(receipt['actual_exit_code'])is int and receipt['actual_exit_code']==0
consumer_values=dict(STATUS='REVIEWED_TRIM_COMPLETE_INPUT_CONSUMER_WITH_ACTUAL_BOUNDED_INTAKE',INTAKE_ROOT_SHA=admission['durable_ROOT_receipt']['sha256'],INTAKE_RETURN_SHA=admission['whole_API_return']['sha256'],API_SEAL_SHA=api['build_seal_sha256'],API_TERMINAL_SHA=api['actual_external_terminal_evidence']['sha256'],API_PREP_SHA=api['actual_prepare_terminal_evidence']['sha256'])
factory_values=dict(DRAFT_STATUS='REVIEWED_TRIM_COLD_INPUT_REUSE_FACTORY_WITH_ACTUAL_BOUNDED_INTAKE',COMBINED_BUILD_SEAL=consumer_values['API_SEAL_SHA'],COMBINED_TERMINAL_SHA=consumer_values['API_TERMINAL_SHA'],COMBINED_RUNTIME=api['corrected_runtime']['path'],COMBINED_RUNTIME_SHA=api['corrected_runtime']['sha256'],PRIVATE_INPUT_CONSUMER_SHA=CS,COMPONENT_INTAKE_DESCRIPTOR_SHA=BS)
texts={};trees={};assignments={};definitions=[];inverse_records=[]
for label,name,csha,msha,allowed in(('factory',FNAME,FS,'76ac45bd9fc22d7a23abea6f46f182207fbea4f34d6be421cd68afbe6fc71a9e',factory_values),('consumer',CNAME,CS,'040f3ec2b201eeeba850c5dff72d66604784d99d97bf9f2c6c991e9ceb48d588',consumer_values)):
 text=raw(C/name,csha).decode();mother=raw(M/name,msha).decode();tree=ast.parse(text);mt=ast.parse(mother);compile(tree,str(C/name),'exec')
 def assignments_of(t):return {n.targets[0].id:n for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
 ca=assignments_of(tree);ma=assignments_of(mt);assert list(ca)==list(ma)
 changed=[k for k in ma if ast.dump(ma[k],include_attributes=False)!=ast.dump(ca[k],include_attributes=False)];assert set(changed)==set(allowed)and len(changed)==len(allowed)
 restored=text;normalized=copy.deepcopy(tree);replacements=[]
 for key,value in allowed.items():
  assert ast.literal_eval(ca[key].value)==value and type(ast.literal_eval(ca[key].value))is type(value)
  replacements.append((ast.get_source_segment(text,ca[key]),ast.get_source_segment(mother,ma[key])))
 assert type(tree.body[0])is ast.Expr and type(tree.body[0].value)is ast.Constant and type(tree.body[0].value.value)is str
 doc=tree.body[0].value.value;assert 'INPUT'in doc and ('not qualified'in doc or 'no native'in doc)
 replacements.append((ast.get_source_segment(text,tree.body[0]),ast.get_source_segment(mother,mt.body[0])))
 for new,old in replacements:assert restored.count(new)==1;restored=restored.replace(new,old,1)
 assert restored==mother
 normalized.body[0]=copy.deepcopy(mt.body[0])
 for node in normalized.body:
  if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id in allowed:node.value=copy.deepcopy(ma[node.targets[0].id].value)
 assert ast.dump(normalized,include_attributes=False)==ast.dump(mt,include_attributes=False)
 nodes=[n for n in ast.walk(tree)if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))];old=[n for n in ast.walk(mt)if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
 assert len(nodes)==len(old)==(55 if label=='factory' else 25)
 for n,p in zip(nodes,old):
  segment=ast.get_source_segment(text,n);assert segment==ast.get_source_segment(mother,p)and ast.dump(n,include_attributes=False)==ast.dump(p,include_attributes=False)
  definitions.append(dict(source=label,name=n.name,start=n.lineno,end=n.end_lineno,sha256=hashlib.sha256(segment.encode()).hexdigest()))
 inverse_records.append(dict(source=label,changed_assignments=changed,module_doc_only_documentary=True,wholebyte_inverse_exact=True,whole_AST_inverse_exact=True,definition_count=len(nodes)))
 texts[label]=text;trees[label]=tree;assignments[label]={k:n.value for k,n in ca.items()}
assert len(definitions)==80
binding=obj(C/BNAME,BS);oldbinding=obj(M/BNAME,'dc1ced8370d9ae6e6e98d5301f570274094a7a09212ecb6f44c40b6bd4012999');expected=copy.deepcopy(oldbinding)
v=receipt['payload_inventory'];assert len(v['files'])==9 and v['symlinks']=={}
proof={str(D/name):sha for name,sha in v['files'].items()};proof[str(D/'Root_terminal_return.json')]=consumer_values['INTAKE_ROOT_SHA']
ns=[dict(root=str(D),files={**v['files'],'Root_terminal_return.json':consumer_values['INTAKE_ROOT_SHA']},directories=v['directories'],symlinks=v['symlinks'])]
assert len(proof)==10 and len(ns)==1 and len(ns[0]['files'])==10
expected.update(draft_status='REVIEWED_COMPLETE_COMPONENT_INPUT_REUSE_NO_COLD_CREDIT',actual_bounded_api_terminal_evidence=admission['durable_ROOT_receipt'],api_return=admission['whole_API_return'],intake_proof_files=proof,intake_namespaces=ns,complete_historical_input_graph=api['historical_input_graph'],expected_complete_alias_count=len(api['input_aliases']))
expected['binding_source']['sha256']=CS
assert typed(binding,expected)
assert list(binding['complete_historical_input_graph'])==['path','sha256','content_sha256','scope']and typed(binding['complete_historical_input_graph'],api['historical_input_graph'])
assert type(binding['expected_complete_alias_count'])is int and binding['expected_complete_alias_count']==len(api['input_aliases'])>0
assert 'binding_descriptor'not in binding and 'sha256'not in binding and 'self_sha256'not in binding
for path,sha in proof.items():raw(path,sha)
for p in binding['helper_sources'].values():raw(p['path'],p['sha256'])
for key in('FORMAL_FACTORY_SHA','BINDING_CONTROLS_ACTUAL'):assert ast.literal_eval(assignments['factory'][key])is None
ftext=texts['factory'];ctext=texts['consumer']
assert "Path(__file__).resolve()!=Path(FORMAL_FACTORY)"in ftext and "digest(__file__)!=nonzero_sha(os.environ.get('AXMAT_COLD_FACTORY_SHA256'))"in ftext
assert "if nonzero_sha(a.factory_sha256)!=os.environ.get('AXMAT_COLD_FACTORY_SHA256')"in ftext
assert "value['historical_input_graph']!=binding['complete_historical_input_graph']"in ctext
assert "phase='cold_INPUT/'+phase"in ctext and 'every canonical endpoint once'in ctext
assert 'actual_project_sources!=expected_project_sources'in ftext
assert all(n in ftext for n in('4456','3716','740','37000','57744','26640','storage_unknowns=1800','active_batches"] != 2000','96*2**30','8*2**30'))
def path_value(node,values):
 if isinstance(node,ast.Constant):return node.value
 if isinstance(node,ast.Name):return values[node.id]
 if isinstance(node,ast.BinOp)and isinstance(node.op,ast.Div):return path_value(node.left,values)/path_value(node.right,values)
 if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='Path'and len(node.args)==1:return Path(path_value(node.args[0],values))
 raise ValueError('only plain literal path identities evaluated')
values=dict(ROOT=ROOT,ART=B)
for name,node in assignments['factory'].items():
 try:values[name]=path_value(node,values)
 except (ValueError,KeyError):pass
formal={k:str(values[k])for k in('SOURCE','OUTPUT','COLD_TERMINAL','CONTROL_TERMINAL','FORMAL_FACTORY','PRIVATE_INPUT_CONSUMER','COMPONENT_INTAKE_DESCRIPTOR')}
assert all(not os.path.lexists(p)for p in formal.values())
source_helper_names=('COMBINED_FACTORY','HOST','CONTROLS','DECK_HELPER','PHYSICAL_BASIS_HELPER','OWN_PID_SUPERVISOR','SCIPY_HELPER','BUILD_FACTORY','PARENT_FACTORY','BASE_FACTORY','BASE_CONTROLLER','PHYSICAL_FACTORY','DEDUP_FACTORY','CURRENT_CAPTURE_FACTORY','TRIM_FACTORY','FROZEN_FAILED_PREP_FACTORY')
for name in source_helper_names:
 sha_name=name+'_SHA';wanted=values[sha_name];assert type(wanted)is str and len(wanted)==64;raw(values[name],wanted)
guard=next(n for n in trees['factory'].body if isinstance(n,ast.FunctionDef)and n.name=='guard_owner_files')
projects=next(ast.literal_eval(n.value)for n in guard.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='expected_project_sources'for t in n.targets));assert len(projects)==26
for path,sha in projects.items():raw(path,sha)
source_decl=obj(values['FULL']/'declaration.json','f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b')
assert {p:sha for p,sha in source_decl['files'].items()if Path(p).is_relative_to(ROOT/'validation')and Path(p).suffix=='.py'}==projects
guard_path=values['FULL']/'preflight/live_guard/guard_controls.json';oldguard=obj(guard_path,'ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454')
raw(guard_path.parent/'tested_driver_source.py',oldguard['source_sha256'])
for name,sha in oldguard['control_files'].items():assert not Path(name).is_absolute()and '..'not in Path(name).parts;raw(guard_path.parent/name,sha)
for pin in(api['corrected_runtime'],api['actual_external_terminal_evidence'],api['actual_prepare_terminal_evidence']):raw(pin['path'],pin['sha256'])
raw(Path(api['build_root'])/'seal.json',api['build_seal_sha256'])
assert ast.literal_eval(assignments['factory']['ORIGINAL_COLD_RESERVE_BYTES'])==20971764748 and ast.literal_eval(assignments['factory']['ORIGINAL_COMPLETE_12_MAP_CASE_BYTES'])==13265348616 and ast.literal_eval(assignments['factory']['ORIGINAL_COMPLETE_SNAPSHOT_BYTES'])==237955708
budget_call=assignments['factory']['BUDGETS'];budgets={x.arg:ast.literal_eval(x.value)for x in budget_call.keywords};assert budgets==dict(setup_seconds=120,bootstrap_axial_seconds=4200,bootstrap_radial_seconds=600,radial_seconds=300,axial_seconds=4200,host_seconds=120,max_maps=100,total_seconds=43200)
generation=obj(C/'Root_source_binding_generation_and_inverse.json');assert generation['bound_source_pins']=={FNAME:FS,CNAME:CS,BNAME:BS}and generation['admission']['sha256']=='26b6bd4f61e40ba6ecff162360c31c6a14321a1ad7de36b2d82efce8e0b63c65'
for path,pin in PINS.items():assert ident(Path(path))==pin['identity']
report=dict(status='PASS',schema='AXMAT_V9_QUALIFIED_COMPLETE_INPUT_BOUND_COLD_FINAL_SOURCE_INDEPENDENT_REVIEW_V1',factory_sha256=FS,consumer_sha256=CS,binding_sha256=BS,actual_whole_INPUT_admission_sha256='26b6bd4f61e40ba6ecff162360c31c6a14321a1ad7de36b2d82efce8e0b63c65',actual_joint_report_sha256=admission['joint_independent_report']['sha256'],actual_joint_tool=jrec['actual_tool_result'],exact7_factory_and6_consumer_top_bindings_only=True,module_doc_only_qualified_INPUT_and_pending_cold_facts=True,complete_source_wholebyte_and_AST_inverse_exact_to_frozen_mothers=True,inverse_evidence=inverse_records,all80_recursive_whole_definition_bytes_AST_unchanged=True,definition_pins=definitions,whole_binding_JSON_exact_to_mother_except_actual_allowlisted_fields=True,whole_actual_graph_all4keys_equal=True,alias_count_derived_from_actual_whole_return=binding['expected_complete_alias_count'],intake_exact_durable10absolute_map=proof,intake_whole_namespace10=ns,full_whole65_7_73_descriptor_math_dtype_layout_owners_ns_alias_trace_absence_scope_unchanged=True,physics_4456_3716_740_37000_57744_26640_1800_guards_wholebyte_retained=True,original_budgets=budgets,original_complete_cold_reservation_bytes=20971764748,original_complete12map_case_bytes=13265348616,original_complete_snapshot_bytes=237955708,history_cap96GiB_free_floor8GiB_unmodified=True,genuine_ownPID_wait4_peak512_MRO_original_helpers_pinned=True,no_api_reexecution_or_module_class_identity_overlay_added=True,FORMAL_FACTORY_SHA=None,BINDING_CONTROLS_ACTUAL=None,external_selfSHA_from_original_env_and_canonical_formal_path_required=True,formal_paths_all_absent=formal,fresh_source_helper_names=list(source_helper_names),old_original_project_source_owners26_freshSHA_and_fullset_preserved=True,old_original_guard_metadata_source_and_control_bytes_freshSHA_no_new_fixture_credit=True,source_pin_count_derived_not_frozen_to_68=len(PINS),all_fresh_pins=list(PINS.values()),actual_declaration_tool=None,actual_declaration_terminal_sha256=None,actual_preparation_tool=None,actual_prepared_sha256=None,actual_binding_tool=None,actual_ownPID_controls_seal=None,actual_controls_terminal=None,actual_cold_native_tool=None,actual_cold_native_RSS_peak=None,actual_AAA_eight_gate_result=None,actual_ABA_admission=None,source_AST_compiled_not_executed=True,source_variant_created_by_reviewer=False,target_factory_consumer_API_constructor_DECLARE_PREP_RUN_watch_fixture_or_native_executed=False,formal_ART_written=False,full35GB_numerical_files_reread=False,new_native_RSS_FLU_AAA_ABA_or_combined_RSS_credit=False,limits=['PASS permits exact source/formal binding admission only; declaration/preparation/controls/native and independent AAA/ABA remain future facts, not inherited qualification.','All executable definitions, global literals except allowed binding pins and generated physics/controller source strings are fullbyte unchanged by independently rebuilt complete inverse.','Metadata SOURCE/helper owners are independently fullSHA read; complete35GB numerical INPUT freshness is covered by genuine qualified wholeINPUT peer scope and must be freshly rechecked in each original future cold phase.','FORMAL_FACTORY_SHA and BINDING_CONTROLS_ACTUAL stay None; the final external source SHA and true control descriptors must be supplied at their original actual phase boundaries.'])
with(H/'independent_final_source_review.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',factory_sha256=FS,consumer_sha256=CS,binding_sha256=BS,report_sha256=hashlib.sha256((H/'independent_final_source_review.json').read_bytes()).hexdigest(),whole_defs80=True,fresh_pins=len(PINS),cold_outcomes_None=True,only_source=True)),flush=True)
