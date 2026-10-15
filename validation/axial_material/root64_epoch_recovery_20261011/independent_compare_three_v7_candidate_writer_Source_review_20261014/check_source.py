from pathlib import Path
import ast,base64,collections,hashlib,json,os,stat,types
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_material_evidence_compare_three_after_GENDF_cumulative_resources_source_v7_20261014'
OLD=R/'current_material_evidence_compare_three_exact_historical_terminal_schema_source_v6_20261014'
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
def require(ok,msg):assert type(ok)is bool and ok,msg
def tool0(t,p):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 for k in ['actual_review_return','actual_postverification_return']:
  z=t[k];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==p
def union(rows):
 out=[]
 for row in rows:
  if row not in out:out.append(row)
 return out
def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
rp=pin(P/'SOURCE_REVIEW_READY.json');ready=load(rp);plan=load(ready['plan_pin']);iv=load(ready['inverse_pin']);oldready=load(OLD/'SOURCE_REVIEW_READY.json');oldplan=load(plan['predecessor_v6_plan_pin'])
assert rp['sha256'].startswith('82b9aafa')and rp['size_bytes']==6151 and ready['plan_pin']['sha256'].startswith('dc130c4d')and ready['plan_pin']['size_bytes']==11357675
assert ready['inverse_pin']['sha256'].startswith('de975477')and ready['inverse_pin']['size_bytes']==111309 and ready['writer_source_pin']['sha256'].startswith('bc4bc9ed')and ready['writer_source_pin']['size_bytes']==9961
for obj in [ready,plan,iv]:
 assert obj['source_only']is True
 for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']:assert obj[k]is False
for obj in [ready,plan]:
 for k in ['actual_compare_three_report_pin','actual_request_pin','actual_GENDF_independent_post_pin','actual_OVERV_control_report_pin']:assert obj[k]is None
for k in ['future_Source_freeze_pin','future_Host_freeze_pin','future_dynamic_interface_pin']:assert plan[k]is None
rawpin=pin(R/'ACTUAL_COMPARE_AFTER_GENDF_CUMULATIVE_RESOURCE_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261014.json');raw=load(rawpin)
assert rawpin['sha256'].startswith('93b926fa')and raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==0
for k in ['actual_Source_preparation_return','actual_Source_generation_return']:
 z=raw[k];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['ready_pin']==rp
preD=R/'independent_compare_three_v6_candidate_writer_Source_review_20261014';prepin=pin(preD/'REVIEW.json');pretpin=pin(preD/'TRUE_TOOL_RETURNS.json');pre=load(prepin);tool0(load(pretpin),prepin)
assert prepin['sha256'].startswith('35a15b81')and pre['failure']is None and pre['Source_candidate_PASS']is True
allowed={'schema','complete_source_file_pins_candidate','source_copies','complete_byte_inverse_pin','planned_cumulative_compare_three_root_count','candidate_scientific_child_pin','predecessor_v6_plan_pin','retained_actual_GENDF_and_control_joint_roots','retained_actual_GENDF_explicit_metadata_file_pins','retained_actual_GENDF_resource_authority_pins','retained_actual_GENDF_current_dependency_pins','original_compare_sixteen_root_projection','planned_complete_cumulative_compare_roots','planned_actual_output_root','planned_actual_request_root','actual_GENDF_independent_post_pin','actual_OVERV_control_report_pin'}
assert {k for k in plan if k not in oldplan or plan[k]!=oldplan[k]}==allowed and set(oldplan)<=set(plan)
source=plan['complete_source_file_pins_candidate'];assert len(source)==13
for p in source:assert pin(p['path'])==p
assert len(iv['source_copies'])==11 and sum(x['whole_bytes_unchanged']for x in iv['source_copies'])==8
for row in iv['source_copies']:
 assert pin(row['candidate_pin']['path'])==row['candidate_pin']and pin(row['predecessor_pin']['path'])==row['predecessor_pin']
 if row['whole_bytes_unchanged']:assert Path(row['candidate_pin']['path']).read_bytes()==Path(row['predecessor_pin']['path']).read_bytes()
code={role:Path(ready[key]['path']).read_text()for role,key in [('builder','builder_source_pin'),('host','host_source_pin'),('child','scientific_child_source_pin'),('writer','writer_source_pin')]}
for role,key in [('builder','builder_source_pin'),('host','host_source_pin'),('child','scientific_child_source_pin'),('writer','writer_source_pin')]:
 restored=code[role]
 for c in reversed(iv[role+'_changes']):assert restored.count(c['after'])==1;restored=restored.replace(c['after'],c['before'],1)
 assert restored.encode()==base64.b64decode(iv['original_'+role+'_whole_bytes_base64'])==Path(oldready[key]['path']).read_bytes()
childtree=ast.parse(code['child']);oldchild=Path(oldready['scientific_child_source_pin']['path']).read_text();oldct=ast.parse(oldchild)
for node in childtree.body:
 if isinstance(node,ast.FunctionDef)and node.name!='main':assert ast.get_source_segment(code['child'],node)==ast.get_source_segment(oldchild,fn(oldct,node.name))
assert ast.get_source_segment(code['child'],fn(childtree,'admit_owning_stage'))==ast.get_source_segment(oldchild,fn(oldct,'admit_owning_stage'))and plan['exact_historical_producer_terminal_contracts']==oldplan['exact_historical_producer_terminal_contracts']
assert ready['current_formal_plan_pin']==oldready['current_formal_plan_pin']and ready['current_producer_projection_pin']==oldready['current_producer_projection_pin']and plan['projection_current_live_pins']==oldplan['projection_current_live_pins']and plan['projection_metadata_authority_pins']==oldplan['projection_metadata_authority_pins']
ownkeys=['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','current_formal_plan_pin','current_producer_projection_pin','plan_pin','inverse_pin'];own=[ready[k]for k in ownkeys]+[rp,ready['writer_source_pin']]
assert any(isinstance(n,ast.List)and all(isinstance(e,ast.Constant)for e in n.elts)and ast.literal_eval(n)==ownkeys for n in ast.walk(ast.parse(code['writer'])))
assert "source=plan['complete_source_file_pins_candidate']"in code['writer']and 'complete_source_file_pins=source'in code['writer']and "plan['retained_actual_GENDF_current_dependency_pins']"in code['writer']
for p in own+[ready['Source_author_pin']]:assert pin(p['path'])==p
authority=plan['retained_actual_GENDF_resource_authority_pins'];assert len(authority)==12
for p in authority:assert pin(p['path'])==p
gfsf=load(authority[0]);gfhf=load(authority[1]);gfhost=load(authority[3]);gfchild=load(authority[4]);gftrue=load(authority[5]);gfargv=load(authority[6]);control=load(authority[7])
assert gfhost['status']=='ACTUAL_ELEVEN_SAVED_MT5_EXTRACTION_CLOSED0_ONLY'and gfhost['failure']is None and gfhost['after_check_error']is None
assert gfchild['status']=='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY'and gfhost['actual_child_receipt']['report']==authority[4]
assert gftrue['observed_closed']is True and type(gftrue['original_integer_exit_code'])is int and gftrue['original_integer_exit_code']==0 and type(gftrue['actual_terminal_return']['exit_code'])is int and gftrue['actual_terminal_return']['exit_code']==0 and gftrue['actual_terminal_return'].get('session_id')is None
gfD=R/'independent_GENDF_cumulative17_v11_actual_evidence_postverify_20261014';gfpp=pin(gfD/'REVIEW_v4.json');gftp=pin(gfD/'TRUE_TOOL_RETURNS.json');gfpost=load(gfpp);tool0(load(gftp),gfpp)
assert gfpost['failure']is None and gfpost['status']=='PASS_ACTUAL_GENDF_CUMULATIVE17_EVIDENCE_POSTVERIFICATION'and gfpost['actual_aggregate_host_pin']==authority[3]and gfpost['actual_aggregate_report_pin']==authority[4]and gfpost['actual_Root_true_tool_pin']==authority[5]
gfroots=gfsf['cumulative_artifact_root_paths'][:3]+gfsf['cumulative_Source_root_paths']+gfsf['cumulative_artifact_root_paths'][3:];assert len(gfroots)==len(set(gfroots))==17 and set(gfroots)==set(gfpost['actual_cumulative_joint_roots'])
retained=union(gfroots+control['cumulative_joint_roots']+[str(OLD)]);assert plan['retained_actual_GENDF_and_control_joint_roots']==retained and len(retained)==21
assert control['source_only']is True and control['actual_current_control_report_pin']is None and control['physics_qualified']is False and control['historical_machine_bit_replay']is False
explicit=plan['retained_actual_GENDF_explicit_metadata_file_pins'];assert explicit==gfsf['cumulative_explicit_metadata_file_pins']+[authority[6],authority[5]]and len(explicit)==len({p['path']for p in explicit})==4
for p in explicit:
 s=Path(p['path']).lstat();assert s.st_uid==os.getuid()and s.st_nlink==1 and not any(a.is_symlink()for a in(Path(p['path']),*Path(p['path']).parents));seven(p)
deps=plan['retained_actual_GENDF_current_dependency_pins'];assert deps==authority+gfhost['fixed_current_pins']+gfhost['complete_output_pins']and len(deps)==6030
current={}
for p in deps+plan['projection_current_live_pins']:
 assert p['path']not in current or current[p['path']]==p;current[p['path']]=p;seven(p)
sixteen=plan['original_compare_sixteen_root_projection'];roots=union(sixteen+retained)
assert len(sixteen)==len(set(sixteen))==16 and len(roots)==len(set(roots))==plan['planned_cumulative_compare_three_root_count']==ready['planned_cumulative_joint_root_count']==25 and roots==plan['planned_complete_cumulative_compare_roots']
assert roots[0]==plan['planned_actual_output_root']and roots[3]==str(P)and roots[4]==plan['planned_actual_request_root']
assert not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)
assert len(set(gfroots)-set(sixteen))==5 and len(set(control['cumulative_joint_roots'])-set(sixteen+gfroots))==3 and str(OLD)not in sixteen+gfroots+control['cumulative_joint_roots']
bt=ast.parse(code['builder']);addition=next(n for n in ast.walk(bt)if isinstance(n,ast.If)and "request['original_compare_sixteen_role_roots']"in ast.unparse(n)and ast.unparse(n.test)=="args.operation == 'compare-three'")
scope=dict(Path=Path,require=require,args=types.SimpleNamespace(operation='compare-three'),request=dict(joint_archive_roots=list(sixteen),complete_input_pins=[]),sf={k:plan[k]for k in ['retained_actual_GENDF_and_control_joint_roots','retained_actual_GENDF_explicit_metadata_file_pins','retained_actual_GENDF_resource_authority_pins','retained_actual_GENDF_current_dependency_pins']})
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn(bt,'unique'),addition],type_ignores=[])),'<only metadata resource append>','exec'),scope)
assert scope['request']['joint_archive_roots']==roots and scope['request']['explicit_cumulative_metadata_file_pins']==explicit
hostloop=next(n for n in ast.walk(ast.parse(code['host']))if isinstance(n,ast.For)and ast.unparse(n.target)=='expected'and ast.unparse(n.iter)=='explicit_metadata')
hostscope=dict(Path=Path,stat=stat,os=os,explicit_metadata=explicit,roots=roots,extra=0,nodes=set());exec(compile(ast.fix_missing_locations(ast.Module(body=[hostloop],type_ignores=[])),'<only actual explicit metadata stat>','exec'),hostscope)
childloop=next(n for n in ast.walk(childtree)if isinstance(n,ast.For)and ast.unparse(n.target)=='expected'and ast.unparse(n.iter)=='self.explicit_metadata')
childscope=dict(Path=Path,stat=stat,os=os,require=require,identity=ids,self=types.SimpleNamespace(explicit_metadata=explicit,roots=[Path(s)for s in roots]),total=0,nodes=set());exec(compile(ast.fix_missing_locations(ast.Module(body=[childloop],type_ignores=[])),'<only actual child explicit metadata stat>','exec'),childscope)
assert all(not any(Path(p['path']).is_relative_to(Path(root))for root in roots)for p in explicit)and hostscope['extra']==childscope['total']==sum(p['size_bytes']for p in explicit)==22676
assert "fresh['artifact_bytes']+extra>=2*2**30"in code['host']and "total+sum(unlinked.values())<2*2**30"in code['child']and "now-self.start<600 and peak<512*2**20"in code['child']
for p in current.values():seven(p)
for p in own+source+authority:seven(p)
assert not any((P/name).exists()for name in ['COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json','ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json'])
result=dict(schema='INDEPENDENT_COMPARE_THREE_V7_CANDIDATE_WRITER_SOURCE_REVIEW_V1',status='PASS_COMPARE_THREE_V7_CUMULATIVE_RESOURCE_CANDIDATE_WRITER_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,Source_candidate_PASS=True,final_selected_Source_pins=own,ready_pin=rp,plan_pin=ready['plan_pin'],inverse_pin=ready['inverse_pin'],writer_source_pin=ready['writer_source_pin'],reviewer_source_pin=pin(__file__),actual_Source_generation_true_tool_pin=rawpin,actual_Source_generation_integer_exit_code=0,predecessor_v6_exact_legacy_Source_review_pin=prepin,predecessor_v6_exact_legacy_Source_tools_pin=pretpin,actual_GENDF_independent_post_pin=gfpp,actual_GENDF_independent_post_tools_pin=gftp,actual_GENDF_host_report_pin=authority[3],actual_GENDF_child_report_pin=authority[4],actual_GENDF_Root_true_tool_pin=authority[5],four_whole_file_inverses_equal_actual_v6_bytes=True,all8_other_Source_runtime_copies_wholebytes_unchanged=True,all_child_scientific_functions_and_exact_three_historical_contract_bytes_unchanged=True,exact2383_projection_and63_outputs_unchanged=True,all13_Source_EOF_and_current7_verified=True,writer_same_round9_Source_roles_plus_READY_writer11_fullpins_verified=True,writer_direct_complete13_Source_assignment_and_cumulative_metadata_bound=True,planned_original_compare_root_count=16,actual_retained_GF_root_count=17,planned_control_root_count=len(control['cumulative_joint_roots']),actual_new_GF_roles_over_original16=5,planned_new_control_roles_over_GF_and_original16=3,exact_old_v6_projection_Source_root_retained=True,planned_complete_cumulative_joint_roots=roots,planned_complete_cumulative_joint_root_count=25,actual_builder_pure_metadata_append_equals_precise25_roots=True,explicit_external_metadata_file_pins=explicit,actual_host_and_child_pure_metadata_meter_bytes=22676,actual_retained_dependency_declaration_count=len(deps),actual_retained_distinct_dependency_count=len({p['path']for p in deps}),actual_retained_and_projection_distinct_current_pin_count=len(current),all_retained_and_projection_current7_verified_twice=True,all_original_caps_and_resource_classes_preserved=True,host_child_same_joint2GiB_includes_all25_roots_plus4_external_metadata_and_child_open_unlinked=True,actual_OVERV_control_report_pin=None,actual_request_pin=None,actual_compare_three_report_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,Source_publication_or_request_or_science_executed=False,large_scientific_payload_or_native_tree_EOF_repeated=False,physics_qualified=False,complete_reaction_authority_qualified=False,historical_machine_bit_replay=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),Source_candidate_PASS=True,planned_complete_cumulative_joint_root_count=25,actual_external_metadata_count=4,actual_external_metadata_bytes=22676,actual_retained_distinct_dependency_count=result['actual_retained_distinct_dependency_count'])),flush=True)
