"""Bind actual admitted INPUT facts to TMP B/F. Never imports any business source."""
import ast,copy,difflib,hashlib,json,os,stat,time
from pathlib import Path
D=Path('/private/tmp/axmat_v12_actual_INPUT_bound_cold_B_F_UNREADY_source_binder_20261009')
M=Path('/private/tmp/axmat_v12_cold_binding_authoritative_sources_and_callback_schema_fix_source_only_20261009')
CAN=Path('/private/tmp/axmat_v12_final_cold_input_candidates_20261009')
ROOT=Path('/Users/wen/spot');AM=ROOT/'validation/axial_material';ART=ROOT/'validation/artifacts'
R=AM/'identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
A=ART/'axial-material-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-evidence-20261009'
V11=ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'
S11=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009'
T11=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-v11-20261009'
FN='prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
CN='cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
BN='cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json'
FSHA='1941375f15d61b44c17ec11e2466048f646112c6c5939ce568c9fdffc84a93a6'
BSHA='563b3f7fa28c93427b9a4613bb7b958d998e56a66a2fe85d959c3ec88440abc0'
CSHA='6688e1fe2967bc63ff12900631e86ae18e30a0ee1bd0b98bb9fbcc4f0ac27823'
PINS={}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def ident(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def read(p,wanted=None,parse=False):
 p=Path(p);before=ident(p);assert stat.S_ISREG(before[2]) and p.parent.resolve()==p.parent
 raw=p.read_bytes();assert ident(p)==before and len(raw)==before[3]
 h=sha(raw)
 if wanted is not None:assert h==wanted,str(p)
 PINS[str(p)]=dict(path=str(p),sha256=h,bytes=len(raw),seven_identity=before)
 if not parse:return raw
 def pairs(items):
  d={}
  for k,v in items:assert k not in d;d[k]=v
  return d
 def bad(v):raise ValueError(v)
 return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)
def write(p,raw):
 with p.open('xb') as stream:stream.write(raw)
 return dict(path=str(p),sha256=sha(raw),bytes=len(raw))
def write_json(p,v):return write(p,(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def tops(tree):return {n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def text_span(text,node):
 lines=text.splitlines(keepends=True);base=sum(len(x.encode()) for x in lines[:node.lineno-1]);endbase=sum(len(x.encode()) for x in lines[:node.end_lineno-1]);return base+node.col_offset,endbase+node.end_col_offset
def funcs(text):
 tree=ast.parse(text);return [(n.name,ast.get_source_segment(text,n),ast.dump(n,include_attributes=False)) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
def nested_diff(a,b,path=''):
 if type(a) is dict and type(b) is dict:
  assert list(a)==list(b)
  result=[]
  for k in a:result+=nested_diff(a[k],b[k],path+'/'+k)
  return result
 if a==b and type(a) is type(b):return []
 return [dict(path=path,old=a,new=b)]
start=time.monotonic()
admission=read(R/'Root_actual_bounded_whole_input_independent_admission.json','c47dfa70b1bf610f3ef88049d1f33491815aed4284c182baa2650b0647c5963f',True)
assert admission['complete_scope_preserved'] is True and admission['descriptor_files']==36804 and admission['canonical_files']==36776
assert admission['original_caps_unchanged'] is True
for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','cold_prepared'):assert admission[k] is False
plan=read(M/'BINDING_PLAN_AND_REPORT.json','77bab26cf4f399104a5f45c9723f5c1b3e88297f233fcca8ca5de1fa3810df1b',True)
parentproof=read(M/'source_inverse_proof.json','99a4405448cd305be7e5c9eda2589ca12f529d588b8a0ae1ad70aeb0bf3834be',True)
oldF=read(M/FN,FSHA).decode();oldB=read(M/BN,BSHA,True);C=read(CAN/CN,CSHA)
root=read(A/'Root_terminal_return.json','449d08d08cdfe7cb19eaf3a882312f8d6c21725011650289608e4bae601178bf',True)
assert type(root['actual_exit_code']) is int and root['actual_exit_code']==0 and root['record_written_after_actual_tool_return'] is True
assert root['actual_tool']==dict(initial_chunk_id='3900c7',session_id=49432,terminal_chunk_id='bbe76b',exit_code=0) and type(root['actual_tool']['exit_code']) is int
body=read(A/'intake/admit.log','65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536',True)
assert len(body)==65 and body['admission']=='COMBINED_RUNTIME_INPUT_ONLY'
trim=body['actual_last_cprime_trim_admission'];counts=trim['cache_unit_control_counts'];assert type(counts) is dict and len(counts)==30 and all(type(x) is int and x>=0 for x in counts.values())
controls=read(V11/'audit/controls.json',parse=True);audit=read(V11/'audit/result.json',parse=True);driver=read(V11/'driver_result.json',parse=True)
assert controls['counts']==audit['control_counts']==driver['control_counts']==counts
assert counts['total_declared_stages']==68 and counts['original_factor_diagonal_45_stages_retained']==45 and counts['additional_keycodec_driver_build_stages']==2 and counts['additional_keycodec_execute_stages']==21
assert audit['cross_group_identity_controls_passed'] is True and driver['cross_group_identity_controls_passed'] is True and controls['keycodec_controls']['status']=='PASS'
V11seal=read(V11/'seal.json',trim['build_seal_sha256'],True)
for name in ('audit/controls.json','audit/result.json','driver_result.json'):
 assert V11seal['files'][name]==PINS[str(V11/name)]['sha256']
v11pins=dict(TRIM_DECL_SHA=sha(read(V11/'declaration.json')),TRIM_SEAL_SHA=trim['build_seal_sha256'],
 TRIM_TERMINAL_SHA=trim['actual_external_terminal_evidence']['sha256'],TRIM_OBJECT_SHA=trim['compiled_kernel']['sha256'],
 TRIM_RUNTIME_SHA=trim['corrected_runtime']['sha256'],TRIM_SOURCE_ADMISSION_SHA=trim['source_admission']['sha256'])
assert v11pins==dict(TRIM_DECL_SHA='2e5c1cda328ee1be5484e756e01337d134a956ae9e6d8623215f49f75e9b42ee',TRIM_SEAL_SHA='5517c1ada26e43ba55683092baf8f63f8676eeff58ee907cd03560047c7a0b19',TRIM_TERMINAL_SHA='26ef721c5b76af13036e6a486468f40d7362b584485c20a8713da82a23a9f430',TRIM_OBJECT_SHA='271bd5f7d768b3380b8d976c177a468cd038faee81ba156f49969bfb8c061131',TRIM_RUNTIME_SHA='05765aeb40f494e9502c0278bfc652c243f8970c31256d11abec5789de7df79b',TRIM_SOURCE_ADMISSION_SHA='a065b026e1e03b2523c945e8b7a6fd508debbea7489fc2707606c3954bb0c1e8')
for d in (trim['actual_external_terminal_evidence'],trim['compiled_kernel'],trim['corrected_runtime'],trim['source_admission']):read(d['path'],d['sha256'])
assert len(root['payload_inventory']['files'])==9 and root['payload_inventory']['symlinks']=={}
payload=dict(root['payload_inventory']['files']);payload['Root_terminal_return.json']=PINS[str(A/'Root_terminal_return.json')]['sha256']
proof={str(A/name):h for name,h in payload.items()}
for name,h in payload.items():read(A/name,h)
actual_files=set();actual_dirs=[]
for cur,ds,ns in os.walk(A,followlinks=False):
 if Path(cur)!=A:actual_dirs.append(str(Path(cur).relative_to(A)))
 for n in ds+ns:assert not (Path(cur)/n).is_symlink()
 for n in ns:actual_files.add(str((Path(cur)/n).relative_to(A)))
assert actual_files==set(payload) and sorted(actual_dirs)==sorted(root['payload_inventory']['directories'])
assert root['source_payload_pins'].keys()==root['payload_inventory']['files'].keys()
for name,d in root['source_payload_pins'].items():assert d['sha256']==payload[name]
B=copy.deepcopy(oldB)
B['draft_status']='READY_ACTUAL_V12_COMPLETE_BOUNDED_RUNTIME_INPUT_BINDING_ONLY_NO_COLD_NATIVE_QUALIFICATION'
B['actual_bounded_api_terminal_evidence']['sha256']=PINS[str(A/'Root_terminal_return.json')]['sha256']
B['api_return']['sha256']=PINS[str(A/'intake/admit.log')]['sha256']
B['intake_proof_files']=proof
B['intake_namespaces']=[dict(root=str(A),inventory=dict(files=payload,symlinks={},directories=root['payload_inventory']['directories']))]
assert B['complete_historical_input_graph']['path']==body['historical_input_graph']['path'] and B['complete_historical_input_graph']['scope']==body['historical_input_graph']['scope']
B['complete_historical_input_graph']=copy.deepcopy(body['historical_input_graph'])
B['binding_source']['sha256']=CSHA
assert B['binding_source']['path']==str(AM/CN)
B['expected_complete_alias_count']=len(body['input_aliases']);B['expected_complete_descriptor_count']=len(body['descriptor_files']);B['expected_intake_payload_count']=len(root['payload_inventory']['files'])
B['actual_V11_component_control_counts']=copy.deepcopy(counts)
assert (B['expected_complete_alias_count'],B['expected_complete_descriptor_count'],B['expected_intake_payload_count'])==(186,36804,9)
assert 'binding_descriptor' not in B and str(AM/BN) not in proof and B['science_qualification'] is False
for d in B['helper_sources'].values():read(d['path'],d['sha256'])
cp=write(D/CN,C);bp=write_json(D/BN,B)
facts=dict(COMBINED_BUILD_SEAL=body['build_seal_sha256'],COMBINED_TERMINAL_SHA=body['actual_external_terminal_evidence']['sha256'],COMBINED_RUNTIME_SHA=body['corrected_runtime']['sha256'],
 PRIVATE_INPUT_CONSUMER_SHA=CSHA,COMPONENT_INTAKE_DESCRIPTOR_SHA=bp['sha256'],**v11pins,TRIM_CONTROL_COUNTS=counts,
 EXPECTED_API_DESCRIPTOR_COUNT=len(body['descriptor_files']),EXPECTED_API_ALIAS_COUNT=len(body['input_aliases']),EXPECTED_INTAKE_PAYLOAD_COUNT=len(root['payload_inventory']['files']),
 FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA=body['actual_prepare_terminal_evidence']['sha256'])
assert len(facts)==16
oldtree=ast.parse(oldF);assign=tops(oldtree);regions=[];raw=oldF.encode()
for name,value in facts.items():
 node=assign[name].value;assert isinstance(node,ast.Constant) and node.value is None
 startpos,endpos=text_span(oldF,node);assert raw[startpos:endpos]==b'None'
 regions.append(dict(name=name,old_start=startpos,old_end=endpos,old='None',new=repr(value)))
for edit in sorted(regions,key=lambda r:r['old_start'],reverse=True):raw=raw[:edit['old_start']]+edit['new'].encode()+raw[edit['old_end']:]
newF=raw.decode();newtree=ast.parse(newF);newassign=tops(newtree);inverse=raw
inverse_regions=[]
for edit in regions:
 node=newassign[edit['name']].value;assert ast.literal_eval(node)==facts[edit['name']]
 lo,hi=text_span(newF,node);assert inverse[lo:hi].decode()==edit['new'];inverse_regions.append(dict(edit,new_start=lo,new_end=hi))
for edit in sorted(inverse_regions,key=lambda r:r['new_start'],reverse=True):inverse=inverse[:edit['new_start']]+edit['old'].encode()+inverse[edit['new_end']:]
assert inverse==oldF.encode() and sha(inverse)==FSHA
assert funcs(oldF)==funcs(newF) and len(funcs(newF))==55
unchanged_tops=set(assign)-set(facts)
assert all(ast.get_source_segment(oldF,assign[k])==ast.get_source_segment(newF,newassign[k]) for k in unchanged_tops)
assert ast.literal_eval(newassign['DRAFT_STATUS'].value)=='UNREADY' and ast.literal_eval(newassign['FORMAL_FACTORY_SHA'].value) is None and ast.literal_eval(newassign['BINDING_CONTROLS_ACTUAL'].value) is None
cold_future=[k for k in newassign if k.startswith('FUTURE_ACTUAL_COLD_')];assert len(cold_future)==7 and all(ast.literal_eval(newassign[k].value) is None for k in cold_future)
for k in ('CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER','DECK_HOOK','ADMISSION_HOST','BUDGETS','CACHE_OBSERVER_CONTRACT','TRIM_FACTOR_STORAGE_CONTRACT'):
 assert ast.get_source_segment(oldF,assign[k])==ast.get_source_segment(newF,newassign[k])
assert 'AXMAT_COLD_FACTORY_SHA256' in newF
callback=ast.literal_eval(newassign['CALLBACK_METADATA_SCHEMA'].value);hosttemplate=ast.literal_eval(newassign['ADMISSION_HOST'].value)
assert callback=='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_INPUT_ADMISSION_V12' and callback in hosttemplate
fp=write(D/FN,raw)
inverseproof=dict(schema='AXMAT_V12_ACTUAL_INPUT_FACTS_ONLY_B_F_COMPLETE_SOURCE_INVERSE_V1',factory_parent=plan['new_factory'],factory_candidate=fp,
 regions=inverse_regions,region_count=16,complete_byte_inverse_sha256=sha(inverse),parent_byteexact=True,
 all_AST_function_definitions=55,all_55_function_bodies_byteexact=True,all_55_function_AST_exact=True,all_other_top_assignments_byteexact=True,
 all_templates_MRO_math_and_caps_byteexact=True,consumer_candidate=cp,consumer_copy_byteexact=True,binding_parent=dict(path=str(M/BN),sha256=BSHA),
 binding_candidate=bp,binding_JSON_differences=nested_diff(oldB,B),binding_all_fields_retained=True,binding_self_descriptor_absent=True,
 preserved_parent_callback_fix_inverse_proof=dict(path=str(M/'source_inverse_proof.json'),sha256=PINS[str(M/'source_inverse_proof.json')]['sha256']),
 future_cold_fields_still_None=cold_future,DRAFT_STATUS='UNREADY',FORMAL_FACTORY_SHA=None,BINDING_CONTROLS_ACTUAL=None,
 original_genuine_V10_chain_preserved_by_exact_parent_and_55_bodies=True)
proofpin=write_json(D/'source_inverse_proof.json',inverseproof)
write(D/'actual_facts_only_F.diff',''.join(difflib.unified_diff(oldF.splitlines(True),newF.splitlines(True),fromfile=str(M/FN),tofile=str(D/FN))).encode())
for p,v in PINS.items():assert ident(p)==v['seven_identity'],p
report=dict(schema='AXMAT_V12_ACTUAL_ADMITTED_INPUT_B_F_SOURCE_ONLY_BINDER_V1',status='PASS_SOURCE_ONLY_ACTUAL_INPUT_BINDING_FACTORY_UNREADY',
 factory=fp,consumer=cp,binding=bp,source_inverse_proof=proofpin,actual_Root_whole_INPUT_admission=PINS[str(R/'Root_actual_bounded_whole_input_independent_admission.json')],
 actual_durable_Root_receipt=PINS[str(A/'Root_terminal_return.json')],actual_whole_API_return=PINS[str(A/'intake/admit.log')],
 actual_counts=dict(descriptor_files=36804,aliases=186,payload_files=9,durable_files=10,intake_namespaces=1,directories=3),actual_V11_control_counts=counts,
 exact_16_top_None_fact_assignments_only=True,all55_definitions_byteexact=True,all_unknown_cold_bindings_None=True,
 declared_graph_descriptor=B['complete_historical_input_graph'],new_callback_metadata_schema_kept=callback,
 actual_intake_namespace_before_and_after=True,all_full_byte_pins=PINS,consumer_final_source_review_separately_required=True,
 new_factory_READY_transition_and_final_full_source_review_reserved_for_Root=True,
 business_imports_or_calls=False,fixture_or_numerical_executed=False,Root_handles_polled=False,project_written=False,
 native_RSS_verified=False,cold_prepared=False,AAA_accuracy_qualified=False,ABA_admitted=False,elapsed_seconds=time.monotonic()-start)
rp=write_json(D/'REPORT.json',report)
print(json.dumps(dict(status=report['status'],factory=fp,binding=bp,consumer=cp,report=rp,proof=proofpin)))
