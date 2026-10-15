from pathlib import Path
import ast,base64,copy,hashlib,json,os,stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_material_evidence_compare_three_exact_historical_terminal_schema_source_v6_20261014'
OLD=R/'current_material_evidence_compare_three_exact_current_projection_source_v5_20261014'
PRE=R/'independent_compare_three_v5_candidate_writer_Source_review_20261014'
D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and s.st_size<=64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes']
def tool0(t,p):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 z=t['actual_review_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==p
def require(ok,msg):assert type(ok)is bool and ok,msg
def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
rp=pin(P/'SOURCE_REVIEW_READY.json');ready=load(rp);plan=load(ready['plan_pin']);iv=load(ready['inverse_pin']);projection=load(ready['current_producer_projection_pin']);formal=load(ready['current_formal_plan_pin'])
assert rp['sha256']=='ec5d7f995d22b0e69348aced3b2f3eb1dc0dbf908721aa086999eff779cf0a70'and rp['size_bytes']==5986
assert ready['plan_pin']['sha256']=='f574005d5b3bb55ec3abcd2509953724142d1815c657369989dc3f31dee4df81'and ready['plan_pin']['size_bytes']==8771696
assert ready['inverse_pin']['sha256']=='d27a716a49076ff62a534a653d702a08eae7560af67642be311631b2c2c01583'and ready['inverse_pin']['size_bytes']==94292
assert ready['writer_source_pin']['sha256']=='b5c1bb3c06ef536a86389fccb00f2a88aaf75f46e78729f2a4200e2fbb8f43dc'and ready['writer_source_pin']['size_bytes']==9499
rawpin=pin(R/'ACTUAL_COMPARE_V6_EXACT_HISTORICAL_TERMINAL_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261014.json');raw=load(rawpin)
assert rawpin['sha256'].startswith('b44642bb')and raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==0
for k in ['actual_Source_preparation_return','actual_Source_generation_return']:
 z=raw[k];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['ready_pin']==rp
prepin=pin(PRE/'REVIEW.json');pre=load(prepin);pretpin=pin(PRE/'TRUE_TOOL_RETURNS.json');tool0(load(pretpin),prepin)
assert prepin['sha256'].startswith('1809d060')and pre['failure']is not None and pre['status']=='REPORTED_COMPARE_THREE_V5_EXACT_LEGACY_PRODUCER_SCHEMA_COMPATIBILITY_FAILURE'
assert len(pre['actual_legacy_missing_field_failures'])==3
for obj in [ready,plan,iv]:
 assert obj['source_only']is True
 for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']:assert obj[k]is False
for k in ['actual_compare_three_report_pin','actual_request_pin']:assert ready[k]is None
for k in ['future_Source_freeze_pin','future_Host_freeze_pin','future_dynamic_interface_pin','actual_compare_three_report_pin','actual_request_pin']:assert plan[k]is None
oldplan=load(plan['predecessor_v5_plan_pin']);oldready=load(OLD/'SOURCE_REVIEW_READY.json')
allowed={'schema','complete_source_file_pins_candidate','source_copies','complete_byte_inverse_pin','all_runtime_source_bytes_unchanged','projection_metadata_authority_pins','current_formal_plan_pin','current_producer_projection_pin','predecessor_v5_plan_pin','candidate_scientific_child_pin','exact_historical_producer_terminal_contracts','only_builder_and_owning_stage_exact_historical_metadata_admission_changed'}
assert {k for k in plan if k not in oldplan or plan[k]!=oldplan[k]}==allowed and set(oldplan)<=set(plan)
source=plan['complete_source_file_pins_candidate'];assert len(source)==13
for p in source:assert pin(p['path'])==p
assert len(iv['source_copies'])==11 and sum(x['whole_bytes_unchanged']for x in iv['source_copies'])==9
for row in iv['source_copies']:
 assert pin(row['candidate_pin']['path'])==row['candidate_pin']and pin(row['predecessor_pin']['path'])==row['predecessor_pin']
 if row['whole_bytes_unchanged']:assert Path(row['candidate_pin']['path']).read_bytes()==Path(row['predecessor_pin']['path']).read_bytes()
builder=Path(ready['builder_source_pin']['path']).read_text();child=Path(ready['scientific_child_source_pin']['path']).read_text();writer=Path(ready['writer_source_pin']['path']).read_text()
for label,code,oldp in [('builder',builder,oldready['builder_source_pin']),('child',child,oldready['scientific_child_source_pin']),('writer',writer,oldready['writer_source_pin'])]:
 restored=code;changes=iv[label+'_changes'];assert len(changes)==1
 for c in reversed(changes):assert restored.count(c['after'])==1;restored=restored.replace(c['after'],c['before'])
 original=base64.b64decode(iv['original_'+label+'_whole_bytes_base64']);assert original==Path(oldp['path']).read_bytes()==restored.encode()
bt=ast.parse(builder);ct=ast.parse(child);oldchild=Path(oldready['scientific_child_source_pin']['path']).read_text();oct=ast.parse(oldchild)
for n in ct.body:
 if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name!='admit_owning_stage':assert ast.get_source_segment(child,n)==ast.get_source_segment(oldchild,next(o for o in oct.body if type(o)is type(n)and o.name==n.name))
assert plan['candidate_scientific_child_pin']==ready['scientific_child_source_pin']and plan['exact_historical_producer_terminal_contracts']==iv['exact_historical_producer_terminal_contracts']
assert plan['only_builder_and_owning_stage_exact_historical_metadata_admission_changed']is True
oldprojection=load(oldready['current_producer_projection_pin']);oldformal=load(oldready['current_formal_plan_pin'])
assert formal==oldformal and ready['current_formal_plan_pin']['sha256']==oldready['current_formal_plan_pin']['sha256']
assert {k for k in projection if projection[k]!=oldprojection[k]}=={'current_formal_plan_pin'}and projection['current_formal_plan_pin']==ready['current_formal_plan_pin']==plan['current_formal_plan_pin']
auditpin=projection['original_metadata_audit_pin'];audit=load(auditpin);tool0(load(projection['original_metadata_audit_tools_pin']),auditpin)
suppin=projection['output_supplement_review_pin'];supp=load(suppin);tool0(load(projection['output_supplement_tools_pin']),suppin)
assert audit['failure']is None and supp['failure']is None
approved={r['historical_pin']['path']:r for r in audit['exact_rebinding_enumeration']+supp['exact_rebinding_enumeration']};assert len(approved)==2383
assert sorted(projection['explicit2383_rebinding_enumeration'],key=lambda r:r['historical_pin']['path'])==[approved[p]for p in sorted(approved)]
for x in approved.values():
 old=x['historical_pin'];now=x['canonical_current_full_EOF_pin'];assert old['path']==now['path']and old['sha256']==now['sha256']and old['size_bytes']==now['size_bytes']and old['identity'][1:]==now['identity'][1:];seven(now)
ownkeys=['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','current_formal_plan_pin','current_producer_projection_pin','plan_pin','inverse_pin']
own=[ready[k]for k in ownkeys]+[rp,ready['writer_source_pin']];assert len(own)==11
assert any(isinstance(n,ast.List)and all(isinstance(e,ast.Constant)for e in n.elts)and ast.literal_eval(n)==ownkeys for n in ast.walk(ast.parse(writer)))
assert "source=plan['complete_source_file_pins_candidate']"in writer and 'complete_source_file_pins=source'in writer and "==plan['candidate_scientific_child_pin']"in writer
for p in own+[ready['Source_author_pin']]:assert pin(p['path'])==p
guards=[n for n in ast.walk(bt)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require']
exactguard=next(n.args[0]for n in guards if n.args[1].value=='exact original producer fullPF/schema retains historically absent after_check_error')
fourguard=next(n.args[0]for n in guards if n.args[1].value=='own true four-stage current single-plane solve/full readback')
admit=fn(ct,'admit_owning_stage');prefix=admit.body[2:5];assert isinstance(prefix[0],ast.Assign)and prefix[0].targets[0].id=='historical_terminal'and isinstance(prefix[1],ast.If)
terminalcode=compile(ast.fix_missing_locations(ast.Module(body=prefix,type_ignores=[])),'<only exact historical terminal metadata>','exec')
def evaluate(expr,scope):return eval(compile(ast.Expression(expr),'<actual metadata guard>','eval'),scope)
counts=[];contracts=[];outputs=0
for row,contract in zip(formal['producers'],iv['exact_historical_producer_terminal_contracts']):
 reportpin=row['report'];value=load(reportpin)
 assert contract==dict(actual_original_report_pin=reportpin,actual_original_schema=value['schema'],after_check_error_field_present=False)
 assert 'after_check_error'not in value and value['failure']is None and len(value['records'])==4 and all(x['status']=='PASS'for x in value['records'])
 assert evaluate(exactguard,dict(row=row,report=value))is True and evaluate(fourguard,dict(row=row,report=value,plane=row['plane']))is True
 scope=dict(report_pin=reportpin,value=value,require=require);exec(terminalcode,scope);assert scope['historical_terminal']is True
 for which in ['pin','schema','presentNone']:
  badpin=copy.deepcopy(reportpin);badvalue=copy.deepcopy(value)
  if which=='pin':badpin['identity'][1]+=1
  if which=='schema':badvalue['schema']+='UNBOUND'
  if which=='presentNone':badvalue['after_check_error']=None
  assert evaluate(exactguard,dict(row=dict(row,report=badpin),report=badvalue))is False
  try:exec(terminalcode,dict(report_pin=badpin,value=badvalue,require=require));raise RuntimeError('unbound or modified legacy report passed')
  except (AssertionError,KeyError):pass
 pr=projection['by_original_report_path'][reportpin['path']];assert pr==oldprojection['by_original_report_path'][reportpin['path']]and pr['actual_original_report_pin']==reportpin
 outputs+=len(pr['projected_output_pins']);counts.append(dict(plane=row['plane'],fixed=len(pr['projected_fixed_current_pins']),outputs=len(pr['projected_output_pins'])))
 contracts.append(contract)
assert outputs==63 and [x['fixed']for x in counts]==[4731,9427,9427]
assert plan['projection_current_live_pins']==oldplan['projection_current_live_pins']and len(plan['projection_current_live_pins'])==23648
assert plan['planned_cumulative_compare_three_root_count']==16
for p in plan['projection_metadata_authority_pins']:assert pin(p['path'])==p
for x in approved.values():seven(x['canonical_current_full_EOF_pin'])
for p in own+source:seven(p)
assert not any((P/name).exists()for name in ['COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json','ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json'])
result=dict(schema='INDEPENDENT_COMPARE_THREE_V6_CANDIDATE_WRITER_SOURCE_REVIEW_V1',status='PASS_COMPARE_THREE_V6_EXACT_HISTORICAL_TERMINAL_CANDIDATE_WRITER_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,Source_candidate_PASS=True,Source_publication_or_request_or_science_executed=False,final_selected_Source_pins=own,ready_pin=rp,plan_pin=ready['plan_pin'],inverse_pin=ready['inverse_pin'],writer_source_pin=ready['writer_source_pin'],reviewer_source_pin=pin(__file__),actual_Source_generation_true_tool_pin=rawpin,actual_Source_generation_integer_exit_code=0,original_v5_specific_compatibility_failure_review_pin=prepin,original_v5_specific_compatibility_failure_tools_pin=pretpin,original_v5_failure_preserved=pre['failure'],all13_Source_EOF_and_current7_verified_twice=True,whole_builder_child_writer_byte_inverses_equal_actual_v5=True,all9_other_Source_runtime_copies_wholebytes_unchanged=True,all_other_child_functions_and_scientific_math_thresholds_wholebytes_unchanged=True,only_original_owning_stage_terminal_metadata_exact3_legacy_contracts_changed=True,exact_historical_terminal_contracts=contracts,actual_three_original_report_fullPF_schema_field_absence_guards_pass=True,unbound_fullPF_or_schema_and_invented_None_explicitly_rejected=True,original_owning_stage_records_watch_log_caps_and_native_terminal_checks_preserved=True,three_original_reports_EOF_verified_and_not_rewritten=True,formal13_original_configuration_unchanged=True,exact2383_rebinding_enumeration_equals_original_two_genuine_audits=True,all2383_current7_verified_twice=True,all2383_path_SHA_size_other6_identity_fields_preserved=True,all63_outputs_exact_projection_and_original_canonical_EOF_proof_preserved=True,actual_projected_producer_counts=counts,actual_projected_live_pin_declarations=23648,writer_same_round9_Source_roles_plus_READY_writer11_fullpins_verified=True,writer_direct_complete13_Source_assignment_verified=True,planned_compare8_union_retained12_count=16,original_same2GiB_resource_caps_and_math_unmodified=True,projection_current_formal_pin_only_path_rebound=True,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,actual_compare_three_report_pin=None,actual_request_pin=None,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,large_scientific_payload_or_native_tree_EOF_repeated=False,no_generic_missing_field_or_device_skip_added=True)
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),Source_candidate_PASS=True,exact_historical_producer_contract_count=3,exact_current_projection_path_count=2383,actual_projected_output_count=63)),flush=True)
