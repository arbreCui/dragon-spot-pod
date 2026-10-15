from pathlib import Path
import ast, base64, hashlib, json, os, shlex, stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_eleven_saved_gendf_actual_cumulative_sixteen_roots_host_source_v10_20261014'
D=Path(__file__).parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size<64*2**20
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
    assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
    if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
    return json.loads(Path(p).read_bytes())
def seven(p):
    q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and ids(s)==p['identity'] and s.st_size==p['size_bytes']
def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
def literal(tree,name):return ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)))
def term0(z):assert type(z['exit_code']) is int and z['exit_code']==0 and z.get('session_id') is None
assert not (D/'REVIEW.json').exists() and not (D/'TRUE_TOOL_RETURNS.json').exists()
rp=pin(P/'SOURCE_REVIEW_READY.json');ready=load(rp)
assert rp['sha256'].startswith('9303248e') and rp['size_bytes']==5627
pp=ready['plan_pin'];plan=load(pp);ip=ready['complete_inverse_pin'];iv=load(ip);wp=ready['writer_source_pin']
assert pp['sha256'].startswith('8b3b56f1') and pp['size_bytes']==40749 and ip['sha256'].startswith('5f2da2e9') and ip['size_bytes']==80505
assert wp['sha256']=='98771f450c8542bba2930fdea5f676e24d034a953dd04b89d254f0a5e3a87f98' and wp['size_bytes']==10315
assert ready['schema']=='GENDF_ACTUAL_CUMULATIVE16_CANDIDATE_WRITER_SOURCE_READY_V1' and ready['source_only'] is True
assert plan['schema']=='GENDF_ACTUAL_COMPLETE_CUMULATIVE_SIXTEEN_ROOTS_SOURCE_PLAN_V1' and plan['source_only'] is True and plan['original_caps']==CAPS
for obj in [ready,plan,iv]:
    for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']:assert obj[k] is False
for k in ['candidate_imported_or_executed','parser_executed','compiler_or_native_engine_started','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete']:assert plan[k] is False
assert ready['actual_GENDF_report_pin'] is None
for k in ['future_Source_freeze_pin','future_Host_freeze_pin','future_recipe_pin']:assert ready[k] is None
for k in ['future_own_Source_freeze_pin','future_own_Host_freeze_pin','future_own_recipe_pin']:assert plan[k] is None
selected=ready['selected_Source_pins']+[rp];assert len(ready['selected_Source_pins'])==6 and len({p['path'] for p in selected})==7
for p in selected+plan['complete_source_file_pins']+[plan['Source_author_pin']]:assert pin(p['path'])==p
assert iv['host_candidate_pin']==plan['candidate_host_source_pin'] and iv['writer_candidate_pin']==wp
codes={};originals={}
for role in ['host','writer']:
    cp=iv[role+'_candidate_pin'];op=iv[role+'_predecessor_pin'];assert pin(cp['path'])==cp and pin(op['path'])==op
    code=Path(cp['path']).read_text();old=Path(op['path']).read_bytes();assert old==base64.b64decode(iv[role+'_original_whole_bytes_base64'])
    restored=code
    for change in reversed(iv[role+'_changes']):assert restored.count(change['after'])==1;restored=restored.replace(change['after'],change['before'])
    assert restored.encode()==old;codes[role]=code;originals[role]=old.decode()
assert iv['whole_host_and_writer_inverse_byte_equal'] is True
copies=iv['source_copies'];assert len(copies)==3
for row in copies:
    assert pin(row['candidate_pin']['path'])==row['candidate_pin'] and pin(row['predecessor_pin']['path'])==row['predecessor_pin']
    if row['whole_bytes_unchanged']:assert Path(row['candidate_pin']['path']).read_bytes()==Path(row['predecessor_pin']['path']).read_bytes()
childp=iv['child_candidate_source_pin'];assert childp==copies[0]['candidate_pin']
child=Path(childp['path']).read_text();oldchild=base64.b64decode(iv['child_original_whole_bytes_base64']).decode();assert oldchild==Path(copies[0]['predecessor_pin']['path']).read_text()
ct=ast.parse(child);ot=ast.parse(oldchild)
budget=next(n for n in ct.body if isinstance(n,ast.ClassDef) and n.name=='Budget');oldbudget=next(n for n in ot.body if isinstance(n,ast.ClassDef) and n.name=='Budget')
init=fn(budget,'__init__');oldinit=fn(oldbudget,'__init__');newsegment=ast.get_source_segment(child,init);oldsegment=ast.get_source_segment(oldchild,oldinit)
assert child.count(newsegment)==1 and child.replace(newsegment,oldsegment).encode()==oldchild.encode()
assert ast.get_source_segment(child,fn(budget,'check')).encode()==ast.get_source_segment(oldchild,fn(oldbudget,'check')).encode()
assert iv['child_budget_exact_original_count']==5 and iv['child_budget_exact_current_count']==16 and iv['only_child_Budget_init_resource_count_changed'] is True
assert iv['all_child_scientific_functions_and_original_parser_and_metadata_builder_whole_bytes_unchanged'] is True
assert 'len(roots)==16' in newsegment and 'len(set(roots))==16' in newsegment and 'len(roots)==5' in oldsegment
host=codes['host'];writer=codes['writer'];ht=ast.parse(host);wt=ast.parse(writer)
assert 'len(artifact_roots)!=10 or len(source_root_paths)!=6 or len(set(roots))!=16' in host
assert "source_root_paths=[str(BASE),str(Path(planpin['path']).parent)]+sf['cumulative_Source_root_paths'][2:]" in host
assert 'complete_sixteen_role_joint_bytes=joint' in host and 'complete_ten_role_joint_bytes=joint' not in host
assert "joint=fresh['artifact_bytes']+source_bytes+unlinked" in host and 'if joint>=2*2**30' in host
assert 'parent.DiskResources(c.ART,artifact_roots,8*2**30,2*2**30)' in host
assert 'peak>=512*2**20 or time.monotonic()-start>=1800' in host
assert "before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30" in host
assert "resources,checks" not in host
for token in ['os.O_DIRECTORY|os.O_NOFOLLOW','os.scandir(fd)','stat.S_ISDIR(item.st_mode)','stat.S_ISREG(item.st_mode)','stat.S_ISREG(item.st_mode)and item.st_nlink==0','/dev/fd']:
    assert token in host
assert 'total+sum(unlinked.values())<2*2**30' in child and "now-self.started<600 and peak<512*2**20" in child
art=plan['cumulative_artifact_root_paths'];rec=plan['cumulative_Source_root_paths'];roots=plan['complete_cumulative_sixteen_role_roots']
assert len(art)==len(set(art))==10 and len(rec)==len(set(rec))==6 and len(roots)==len(set(roots))==16
assert set(roots)==set(art+rec) and roots==plan['complete_cumulative_ten_role_roots'] and plan['complete_cumulative_ART_role_count']==10 and plan['complete_cumulative_Source_request_role_count']==6
assert all(Path(p).is_relative_to(R.parent.parent/'artifacts') for p in art)
assert all(Path(p).is_relative_to(R) for p in rec)
assert not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b)
request=load(plan['actual_corrected_aggregation_request_pin']);oldfive=plan['original_five_role_roots_preserved']
assert len(oldfive)==5 and len(set(oldfive)&set(request['joint_archive_roots']))==1
assert set(roots)==set(oldfive+request['joint_archive_roots']) and len(request['joint_archive_roots'])==12
guard=init.body[0].value.args[0]
assert eval(compile(ast.Expression(guard),'<actual strict16 Source predicate>','eval'),{'roots':roots}) is True
assert eval(compile(ast.Expression(guard),'<15-role negative>','eval'),{'roots':roots[:-1]}) is False
assert eval(compile(ast.Expression(guard),'<duplicate-role negative>','eval'),{'roots':roots[:-1]+[roots[0]]}) is False
assert ready['original_Host_argv_count']==32 and ready['original_metadata_builder_argv_count']==18 and ready['once_writer_required_fullpin_role_count']==8
assert "roles=('Source-review','Source-tools','Source-generation-tools','aggregate-report','aggregate-Root-tools','aggregate-Root-argv','aggregate-post-review','aggregate-post-tools')" in writer
for token in ["peer['final_selected_Source_pins']","pt['actual_review_return']","gen['actual_Source_preparation_return']","'actual_review_return','actual_postverification_return'","'actual_aggregate_host_pin'","'actual_Root_true_tool_pin'","'actual_Root_argv_pin'","'actual_aggregate_report_pin'","expected_original_DiskResources_ART_role_count=10","complete_joint_source_tree_role_count=6","complete_cumulative_joint_root_count=16","recipe['argv_prefix'][:11]","is_complete_executable_argv=False","GENDF_executed=False","os.fsync(fd)"]:
    assert token in writer
hostcaps=next(n.value for n in ht.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CAPS' for t in n.targets))
childcaps=next(n.value for n in ct.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CAPS' for t in n.targets))
assert ast.dump(hostcaps,include_attributes=False)==ast.dump(childcaps,include_attributes=False)
authoritykeys=['actual_aggregation_report_pin','actual_aggregation_post_pin','actual_aggregation_Root_tool_pin','actual_aggregation_Root_argv_pin','actual_aggregation_post_tools_pin']
agg=load(plan['actual_aggregation_report_pin']);post=load(plan['actual_aggregation_post_pin']);rt=load(plan['actual_aggregation_Root_tool_pin']);argv=load(plan['actual_aggregation_Root_argv_pin']);pt=load(plan['actual_aggregation_post_tools_pin'])
term0(rt['actual_terminal_return']);assert rt['observed_closed'] is True and type(rt['original_integer_exit_code']) is int and rt['original_integer_exit_code']==0 and shlex.split(rt['exact_executed_command'])==argv['argv'] and len(argv['argv'])==30
assert agg['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY' and agg['failure'] is None and agg['after_check_error'] is None and agg['actual_intentional_exit2_normal_closure'] is True
assert agg['records'][0]['status']=='FAILED' and agg['records'][0]['error']=='own-child stage failed; no retry'
watch=load(agg['actual_watchdog_full_pin']);assert type(watch['returncode']) is int and watch['returncode']==2 and watch['limit_failure'] is None
childreportpin=agg['actual_complete_child_receipt']['report'];math=load(childreportpin)
assert post['schema']==plan['actual_aggregation_POST_schema'] and post['status']==plan['actual_aggregation_POST_status'] and post['failure'] is None
canon=dict(actual_aggregate_host_pin=plan['actual_aggregation_report_pin'],actual_Root_true_tool_pin=plan['actual_aggregation_Root_tool_pin'],actual_Root_argv_pin=plan['actual_aggregation_Root_argv_pin'],actual_aggregate_report_pin=childreportpin)
assert all(post[k]==p for k,p in canon.items())
for key in ['actual_review_return','actual_postverification_return']:
    term0(pt[key]);assert json.loads(pt[key]['output'].strip().splitlines()[-1])['review_pin']==plan['actual_aggregation_post_pin']
assert pt['observed_closed'] is True and type(pt['original_integer_exit_code']) is int and pt['original_integer_exit_code']==0
for obj in [agg,post,math,math['states'][0]]:
    for key,value in obj.items():
        if key.endswith('_qualified') or key in ['ABA_admitted','goal_complete']:assert value is False
issue=pt['actual_remaining_source_context_issue'];assert issue==dict(category='SOURCE_CONTEXT_NOT_SAVED',field='OVERV',reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',original_all370x8_words_compared=True,historical_machine_bit_replay=False)
assert math['states'][0]['all_context_or_operand_issues']==1 and math['states'][0]['all_mismatching_elements']==0
for p in plan['eleven_saved_binary_input_pins']:seven(p)
assert len(plan['eleven_saved_binary_input_pins'])==11 and sum(p['size_bytes'] for p in plan['eleven_saved_binary_input_pins'])==plan['original_saved_binary_input_bytes']==154650680
for filename in ['COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json','ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json']:assert not (P/filename).exists()
allpins=selected+plan['complete_source_file_pins']+[plan['Source_author_pin']]+[plan[k] for k in authoritykeys]+[childreportpin,plan['actual_corrected_aggregation_request_pin']]
for _ in range(2):
    for p in allpins+plan['eleven_saved_binary_input_pins']:seven(p)
result=dict(schema='INDEPENDENT_GENDF_ACTUAL_CUMULATIVE16_V10_CANDIDATE_WRITER_SOURCE_REVIEW_V1',status='PASS_GENDF_ACTUAL_CUMULATIVE16_V10_CANDIDATE_WRITER_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,final_selected_Source_pins=selected,ready_pin=rp,plan_pin=pp,inverse_pin=ip,writer_source_pin=wp,Source_author_pin=plan['Source_author_pin'],reviewer_source_pin=pin(__file__),
    complete_host_and_writer_wholebyte_inverses_verified=True,child_only_Budget_init_5_to16_wholebyte_inverse_verified=True,all_scientific_parser_math_functions_and_original_Budget_check_wholebytes_preserved=True,all_selected_Source_EOF_SHA_and_current7_verified=True,all_required_current7_verified_twice=True,exact_ART_role_count=10,exact_REC_Source_request_role_count=6,exact_disjoint_cumulative_runtime_root_count=16,exact_original_five_plus_actual_corrected_twelve_minus_one_overlap_verified=True,complete_cumulative_root_paths=roots,original_caps=CAPS,
    actual_strict16_positive_and_missing_duplicate_negatives_verified=True,original_ART_scan_plus_all_six_REC_trees_plus_open_unlinked_metering_preserved=True,truthful_complete_sixteen_role_joint_bytes_field=True,original_metadata_builder18_and_runtimeRoot32_protocol_preserved=True,once_writer_exact8_fullpin_roles_and_same_round_review0_protocol_verified=True,once_writer_corrected_actual_aggregation_post_schema_status_and_four_canonical_keys_verified=True,actual_aggregation_authority_pins={k:plan[k] for k in authoritykeys},actual_aggregate_child_report_pin=childreportpin,actual_original_Root0_child2_FAILED_no_retry_preserved=True,actual_OVERV_remaining_issue_preserved=issue,
    eleven_saved_input_current7_count=11,eleven_saved_input_body_EOF_repeated=False,future_own_Source_freeze_pin=None,future_own_Host_freeze_pin=None,future_own_recipe_pin=None,actual_GENDF_report_pin=None,candidate_imported_or_executed=False,once_writer_executed=False,native_or_scientific_trees_decoded=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with (D/'REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),ready_pin=rp,selected_Source_count=len(selected),ART_roots=10,REC_roots=6,runtime_roots=16)),flush=True)
