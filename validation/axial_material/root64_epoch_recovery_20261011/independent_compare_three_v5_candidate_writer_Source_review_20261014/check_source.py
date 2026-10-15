from pathlib import Path
import ast,base64,hashlib,json,os,stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_material_evidence_compare_three_exact_current_projection_source_v5_20261014'
D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and s.st_size<64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes']
def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
def tool0(t,p):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 z=t['actual_review_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==p
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
rp=pin(P/'SOURCE_REVIEW_READY.json');ready=load(rp);plan=load(ready['plan_pin']);iv=load(ready['inverse_pin']);projection=load(ready['current_producer_projection_pin']);formal=load(ready['current_formal_plan_pin'])
assert rp['sha256'].startswith('8d97b2f6')and rp['size_bytes']==5906 and ready['plan_pin']['sha256'].startswith('ae4d914f')and ready['plan_pin']['size_bytes']==8768298
assert ready['inverse_pin']['sha256'].startswith('d4ae372e')and ready['inverse_pin']['size_bytes']==93570
assert ready['current_formal_plan_pin']['sha256'].startswith('9f78b5fd')and ready['current_producer_projection_pin']['sha256'].startswith('11e65e3d')
assert ready['builder_source_pin']['sha256'].startswith('2d8c9865')and ready['writer_source_pin']['sha256'].startswith('7d2796fa')
for obj in [ready,plan,iv]:
 assert obj['source_only']is True
 for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']:assert obj[k]is False
for k in ['actual_compare_three_report_pin','actual_request_pin']:assert ready[k]is None
for k in ['future_Source_freeze_pin','future_Host_freeze_pin','future_dynamic_interface_pin','actual_compare_three_report_pin','actual_request_pin']:assert plan[k]is None
source=plan['complete_source_file_pins_candidate'];assert len(source)==13
for p in source:assert pin(p['path'])==p
for copy in iv['source_copies']:
 assert pin(copy['candidate_pin']['path'])==copy['candidate_pin']and pin(copy['predecessor_pin']['path'])==copy['predecessor_pin']
 if copy['whole_bytes_unchanged']:assert Path(copy['candidate_pin']['path']).read_bytes()==Path(copy['predecessor_pin']['path']).read_bytes()
assert len(iv['source_copies'])==11 and sum(not p['whole_bytes_unchanged']for p in iv['source_copies'])==1
builder=Path(ready['builder_source_pin']['path']).read_text();writer=Path(ready['writer_source_pin']['path']).read_text()
assert builder.encode()==base64.b64decode(iv['candidate_builder_whole_bytes_base64'])and writer.encode()==base64.b64decode(iv['candidate_writer_whole_bytes_base64'])
for code,splices,originalkey in [(builder,iv['builder_unique_splices'],'original_builder_whole_bytes_base64'),(writer,iv['writer_splices'],'original_writer_whole_bytes_base64')]:
 restored=code
 for s in reversed(splices):assert restored.count(s['candidate'])>0;restored=restored.replace(s['candidate'],s['original'])
 assert restored.encode()==base64.b64decode(iv[originalkey])
bt=ast.parse(builder);oldbuilder=base64.b64decode(iv['original_builder_whole_bytes_base64']).decode();obt=ast.parse(oldbuilder)
for name in ['unique','admit_evidence_host','base_request']:assert ast.get_source_segment(builder,fn(bt,name))==ast.get_source_segment(oldbuilder,fn(obt,name))
assert "for stage in report['records']:admit_owning_stage(row['report'],stage['label'],stage['command'],lambda:None)"in builder
assert "projected['projected_fixed_current_pins']+projected['projected_output_pins']"in builder
assert "len(set(request['joint_archive_roots']))==len(request['joint_archive_roots'])==16"in builder
assert "retained_host['fixed_current_pins']+retained_host['complete_output_pins']"in builder
assert "newsf.update(provenance,complete_source_file_pins=source"in writer and "source=plan['complete_source_file_pins_candidate']"in writer
ownkeys=['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','current_formal_plan_pin','current_producer_projection_pin','plan_pin','inverse_pin']
own=[ready[k]for k in ownkeys]+[rp,ready['writer_source_pin']];assert len(own)==11
assert any(isinstance(n,ast.List) and all(isinstance(x,ast.Constant) for x in n.elts) and ast.literal_eval(n)==ownkeys for n in ast.walk(ast.parse(writer))) and "'same-round eleven exact Source PFs'"in writer
for p in own+[ready['Source_author_pin']]:assert pin(p['path'])==p
auditpin=projection['original_metadata_audit_pin'];audit=load(auditpin);tool0(load(projection['original_metadata_audit_tools_pin']),auditpin)
suppin=projection['output_supplement_review_pin'];supp=load(suppin);tool0(load(projection['output_supplement_tools_pin']),suppin)
assert audit['failure']is None and supp['failure']is None and projection['no_generic_device_rule_or_missing_skip']is True and projection['original_reports_not_modified']is True
approved={r['historical_pin']['path']:r for r in audit['exact_rebinding_enumeration']+supp['exact_rebinding_enumeration']};assert len(approved)==2383
assert sorted(projection['explicit2383_rebinding_enumeration'],key=lambda r:r['historical_pin']['path'])==[approved[p]for p in sorted(approved)]
current={p:r['canonical_current_full_EOF_pin']for p,r in approved.items()}
for p,r in approved.items():
 old=r['historical_pin'];now=r['canonical_current_full_EOF_pin'];assert old['path']==now['path']and old['sha256']==now['sha256']and old['size_bytes']==now['size_bytes']and old['identity'][0]==16777234 and now['identity'][0]==16777229 and old['identity'][1:]==now['identity'][1:];seven(now)
def rebind(obj):
 if isinstance(obj,dict):
  if set(obj)=={'path','sha256','size_bytes','identity'}:
   assert approved[obj['path']]['historical_pin']==obj;return current[obj['path']]
  return{k:rebind(v)for k,v in obj.items()}
 if isinstance(obj,list):return[rebind(v)for v in obj]
 return obj
original_formal=load(projection['original_formal_plan_pin']);assert formal==rebind(original_formal)
assert projection['current_formal_plan_pin']==ready['current_formal_plan_pin']==plan['current_formal_plan_pin']
assert len(formal['formal_inputs'])==13 and len(formal['producers'])==3 and formal['formal_configuration']==original_formal['formal_configuration']
assert len(projection['by_original_report_path'])==3
producer_counts=[];alllive=[];legacy_failures=[];reports=[]
lineage=Path(ready['scientific_child_source_pin']['path']).read_text();lt=ast.parse(lineage);admit=fn(lt,'admit_owning_stage')
admitguard=admit.body[2].value.args[0]
builderguards=[n.args[0]for n in ast.walk(bt)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require'and "report['after_check_error']"in ast.unparse(n.args[0])]
assert len(builderguards)==1
for row in formal['producers']:
 reportpin=row['report'];raw=load(reportpin);reports.append(reportpin);pr=projection['by_original_report_path'][reportpin['path']]
 assert pr['actual_original_report_pin']==reportpin and pr['plane']==row['plane']and pr['original_report_not_modified']is True
 assert pr['projected_fixed_current_pins']==[rebind(p)for p in raw['fixed_current_pins']]
 assert pr['projected_output_pins']==[rebind(p)for p in raw['output_pins']]
 assert len(raw['records'])==4 and raw['failure']is None and raw['actual_native_terminal']==row['native_readback']and len(raw['output_pins'])==21
 assert 'after_check_error'not in raw
 failures=[]
 for label,guard,scope in [('compare_builder',builderguards[0],dict(report=raw,row=row,plane=row['plane'])),('original_admit_owning_stage',admitguard,dict(value=raw))]:
  try:eval(compile(ast.Expression(guard),'<actual Source compatibility predicate>','eval'),scope);raise AssertionError('missing legacy field was not accessed')
  except KeyError as e:assert e.args==('after_check_error',);failures.append(dict(predicate=label,actual_error=repr(e)))
 legacy_failures.append(dict(plane=row['plane'],actual_original_report_pin=reportpin,schema=raw['schema'],actual_status=raw['status'],missing_field='after_check_error',actual_failed_predicates=failures))
 alllive+=pr['projected_fixed_current_pins']+pr['projected_output_pins'];producer_counts.append(dict(plane=row['plane'],fixed=len(raw['fixed_current_pins']),outputs=len(raw['output_pins'])))
assert [p['fixed']for p in producer_counts]==[4731,9427,9427]and len(alllive)==23648 and alllive==plan['projection_current_live_pins']
retained=load(plan['retained_current_corrected_aggregation_request_pin']);assert len(retained['joint_archive_roots'])==12 and retained['joint_archive_roots']==plan['retained_corrected_aggregation_joint_archive_roots']
for p in plan['projection_metadata_authority_pins']:assert pin(p['path'])==p
for p in current.values():seven(p)
for p in own+source+reports:seven(p)
result=dict(schema='INDEPENDENT_COMPARE_THREE_V5_CANDIDATE_WRITER_SOURCE_REVIEW_V1',status='REPORTED_COMPARE_THREE_V5_EXACT_LEGACY_PRODUCER_SCHEMA_COMPATIBILITY_FAILURE',failure="Three sealed legacy producer reports lack after_check_error; actual unchanged builder and admit_owning_stage predicates raise KeyError before current projection consumption.",source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,Source_publication_or_request_or_science_executed=False,
 final_selected_Source_pins=own,ready_pin=rp,plan_pin=ready['plan_pin'],inverse_pin=ready['inverse_pin'],writer_source_pin=ready['writer_source_pin'],current_formal_plan_pin=ready['current_formal_plan_pin'],current_producer_projection_pin=ready['current_producer_projection_pin'],reviewer_source_pin=pin(__file__),
 all13_Source_EOF_and7_verified=True,builder_and_writer_wholebyte_inverses_verified=True,all10_scientific_runtime_copies_wholebytes_unchanged=True,original_owning_stage_scientific_main_and_thresholds_wholebytes_unchanged=True,writer_same_round9_Source_roles_plus_READY_writer11_fullpins_verified=True,writer_direct_complete13_Source_assignment_verified=True,
 exact2383_rebinding_enumeration_equals_original_two_genuine_audits=True,all2383_current7_verified_twice=True,all2383_path_SHA_size_other6_identity_fields_preserved=True,formal13_only_exact_catalog_device_metadata_rebound=True,three_sealed_original_reports_EOF_and_current7_verified=True,three_original_reports_not_rewritten=True,actual_projected_producer_counts=producer_counts,all63_outputs_exact_projection_and_actual_canonical_EOF_proof_preserved=True,actual_projected_live_pin_declarations=23648,
 actual_legacy_missing_field_failures=legacy_failures,Common_current_metadata_view_adds_no_missing_schema_fields=True,planned_compare8_union_retained12_count=16,original_same2GiB_resource_caps_and_math_unmodified=True,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,actual_compare_three_report_pin=None,actual_request_pin=None,
 physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,large_scientific_payload_or_native_tree_EOF_repeated=False,no_generic_missing_field_or_device_skip_added=True)
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),Source_candidate_PASS=False,actual_legacy_producer_missing_after_check_error_count=3,exact_current_projection_path_count=2383)),flush=True)
