from pathlib import Path
import ast,base64,copy,hashlib,json,os,shlex,stat
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014'
D=Path(__file__).parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
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
def term0(z):assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None
def contains(obj,p):
 return obj==p or isinstance(obj,dict)and any(contains(v,p)for v in obj.values())or isinstance(obj,list)and any(contains(v,p)for v in obj)
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
rp=pin(P/'SOURCE_REVIEW_READY_v2.json');ready=load(rp);pp=ready['plan_pin'];plan=load(pp);ip=ready['complete_inverse_pin'];iv=load(ip);wp=ready['writer_source_pin']
assert rp['sha256']=='7f01ccbf207c2cf6535ef52caab9c1bf6f37073747d84ec9e434574a8d88064f'and rp['size_bytes']==5691 and pp['sha256'].startswith('5ce4b57d')and pp['size_bytes']==56671 and ip['sha256'].startswith('b7e8d307')and ip['size_bytes']==136466
assert wp['sha256']=='6fae25c8d97b05eb0735052b3b3ae1afaecb1b29b6865c4813b3d5c6a854b003'and wp['size_bytes']==11651
assert ready['schema']=='GENDF_ACTUAL_CUMULATIVE17_EXACT_MAPPING_CANDIDATE_WRITER_SOURCE_READY_V1'and ready['source_only']is True and plan['source_only']is True and plan['original_caps']==CAPS
for obj in [ready,plan,iv]:
 for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']:assert obj[k]is False
for k in ['future_Source_freeze_pin','future_Host_freeze_pin','future_recipe_pin','actual_GENDF_report_pin']:assert ready[k]is None
for k in ['future_own_Source_freeze_pin','future_own_Host_freeze_pin','future_own_recipe_pin']:assert plan[k]is None
selected=ready['selected_Source_pins']+[rp];assert len(ready['selected_Source_pins'])==6 and len(selected)==7
for p in selected+plan['complete_source_file_pins']+[plan['Source_author_pin']]:assert pin(p['path'])==p
genpin=pin(R/'ACTUAL_GENDF_V11_EXACT_SEVEN_POINTER_METADATA_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261014.json');gen=load(genpin);term0(gen['actual_Source_preparation_return'])
assert genpin['sha256']=='b2242b0de1b0f3c42a7b5cbae73a40d44c644d1bb615929a82722de4ed858fad'and gen['actual_Source_preparation_return']['chunk_id']=='45eced'and gen['observed_closed']is True and type(gen['original_integer_exit_code'])is int and gen['original_integer_exit_code']==0
assert json.loads(gen['actual_Source_preparation_return']['output'])['ready_pin']==rp
codes={};original={};trees={};oldtrees={}
for role in ['host','child','writer']:
 cp=iv[role+'_candidate_pin'];op=iv[role+'_predecessor_pin'];assert pin(cp['path'])==cp and pin(op['path'])==op
 code=Path(cp['path']).read_text();old=Path(op['path']).read_bytes();assert old==base64.b64decode(iv[role+'_original_whole_bytes_base64'])
 restored=code
 for change in reversed(iv[role+'_changes']):assert restored.count(change['after'])>0;restored=restored.replace(change['after'],change['before'])
 assert restored.encode()==old;codes[role]=code;original[role]=old.decode();trees[role]=ast.parse(code);oldtrees[role]=ast.parse(old.decode())
assert iv['all_three_whole_file_inverse_byte_equal']is True and iv['all_scientific_parser_math_threshold_functions_whole_bytes_unchanged']is True and iv['original_caps_unchanged']is True
for n in trees['child'].body:
 if isinstance(n,ast.FunctionDef)and n.name!='main':assert ast.get_source_segment(codes['child'],n)==ast.get_source_segment(original['child'],fn(oldtrees['child'],n.name))
cli=next(r for r in plan['source_copies']if Path(r['candidate_pin']['path']).name=='build_root_reviewable_actual_gendf_cli.py')
assert Path(cli['candidate_pin']['path']).read_bytes()==Path(cli['predecessor_pin']['path']).read_bytes()
oldsf=load(plan['predecessor_source_freeze_pin']);oldhf=load(plan['predecessor_host_freeze_pin']);mapping=plan['publication_source_mapping']
assert mapping==iv['publication_source_mapping']and len(mapping)==3
for row in mapping:
 assert row['predecessor_pin']in oldsf['complete_source_file_pins']and row['predecessor_pin']in oldhf['dependencies']and pin(row['predecessor_pin']['path'])==row['predecessor_pin']and pin(row['candidate_pin']['path'])==row['candidate_pin']
# Execute precisely the writer's actual loaded-SF/HF in-memory mapping block; no publisher node is selected.
main=fn(trees['writer'],'main');block=[];active=False
for n in main.body:
 if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='mapping'for t in n.targets):active=True
 if active:
  if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and isinstance(n.value.func.value,ast.Name)and n.value.func.value.id=='sf'and n.value.func.attr=='update':break
  block.append(copy.deepcopy(n))
assert block and not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='write'for node in block for n in ast.walk(node))
scope=dict(plan=plan,sf=copy.deepcopy(oldsf),hf=copy.deepcopy(oldhf),pin=pin,copy=copy)
exec(compile(ast.fix_missing_locations(ast.Module(body=block,type_ignores=[])),'<actual writer exact mapping only; no publication>','exec'),scope)
mapped_sf=scope['sf'];mapped_hf=scope['hf'];assert scope['counts']==[2,3,2]and sum(scope['counts'])==7
assert mapped_sf['complete_source_file_pins']==plan['complete_source_file_pins']
assert all(not contains(mapped_sf,row['predecessor_pin'])and not contains(mapped_hf,row['predecessor_pin'])for row in mapping)
assert all(row['candidate_pin']in mapped_sf['complete_source_file_pins']and row['candidate_pin']in mapped_hf['dependencies']for row in mapping)
assert 'basename'not in ast.get_source_segment(codes['writer'],next(n for n in main.body if isinstance(n,ast.FunctionDef)and n.name=='replace_exact'))
assert 'host_source=plan[\'candidate_host_source_pin\']'in codes['writer']and plan['candidate_host_source_pin']==iv['host_candidate_pin']
assert "recipe['argv_prefix'][:11]+[plan['candidate_host_source_pin']['path']"in codes['writer']
art=plan['cumulative_artifact_root_paths'];rec=plan['cumulative_Source_root_paths'];roots=plan['complete_cumulative_seventeen_role_roots']
assert len(art)==10 and len(rec)==7 and len(roots)==len(set(roots))==17 and set(roots)==set(art+rec)
assert not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)
v10=Path(iv['host_predecessor_pin']['path']).parent;assert str(v10)in rec and str(P)in rec
request=load(plan['actual_corrected_aggregation_request_pin']);assert set(request['joint_archive_roots'])<=set(roots)and set(plan['original_five_role_roots_preserved'])<=set(roots)
metadata=plan['cumulative_explicit_metadata_file_pins'];assert len(metadata)==2 and sum(p['size_bytes']for p in metadata)==plan['explicit_metadata_file_bytes']==15660
for p in metadata:
 assert pin(p['path'])==p;s=Path(p['path']).lstat();assert s.st_nlink==1 and s.st_uid==os.getuid()and not any(Path(p['path']).is_relative_to(Path(root))for root in roots)
for p in plan['original_v10_published_metadata_pins']:assert pin(p['path'])==p and Path(p['path']).parent==v10
phasepin=plan['retained_actual_capture_owner_authority_pin'];phase=load(phasepin);capture=plan['retained_actual_capture_owner_root']
assert capture==str(Path(phase['actual_prior_A_cwd']).parent)and Path(phase['original_failed_phase_pin']['path']).parent==Path(capture)and capture in art
host=codes['host'];child=codes['child'];writer=codes['writer']
assert "str(Path(observed['actual_prior_A_cwd']).parent)!=sf['retained_actual_capture_owner_root'] or Path(observed['original_failed_phase_pin']['path']).parent!=Path(sf['retained_actual_capture_owner_root'])"in host
assert "!=artifact_roots[3]"not in host
for token in ['len(source_root_paths)!=7 or len(set(roots))!=17','complete_seventeen_role_joint_bytes=joint',"joint=fresh['artifact_bytes']+source_bytes+unlinked",'parent.DiskResources(c.ART,artifact_roots,8*2**30,2*2**30)','if joint>=2*2**30',"total+=item.st_size;count+=1",'host_open_unlinked_bytes']:
 assert token in host
for token in ['len(roots)==17','len(set(roots))==17','len(explicit_metadata)==2',"if not any(p.is_relative_to(root)for root in self.roots):total+=s.st_size",'total+sum(unlinked.values())<2*2**30','now-self.started<600 and peak<512*2**20']:
 assert token in child
assert "cumulative_explicit_metadata_file_pins=explicit_metadata"in host and "binding['cumulative_explicit_metadata_file_pins']"in child
assert ready['original_Host_argv_count']==32 and ready['original_metadata_builder_argv_count']==18 and ready['once_writer_required_fullpin_role_count']==8
assert "peer['final_selected_Source_pins']"in writer and "pt['actual_review_return']"in writer and 'original_integer_exit_code' in writer
agg=load(plan['actual_aggregation_report_pin']);post=load(plan['actual_aggregation_post_pin']);pt=load(plan['actual_aggregation_post_tools_pin']);rt=load(plan['actual_aggregation_Root_tool_pin']);argv=load(plan['actual_aggregation_Root_argv_pin'])
term0(rt['actual_terminal_return']);assert rt['observed_closed']is True and type(rt['original_integer_exit_code'])is int and rt['original_integer_exit_code']==0 and shlex.split(rt['exact_executed_command'])==argv['argv']and len(argv['argv'])==30
assert agg['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY'and agg['failure']is None and agg['after_check_error']is None and agg['records'][0]['status']=='FAILED'
assert post['failure']is None and post['schema']==plan['actual_aggregation_POST_schema']and post['status']==plan['actual_aggregation_POST_status']
for key in ['actual_review_return','actual_postverification_return']:
 term0(pt[key]);assert json.loads(pt[key]['output'])['review_pin']==plan['actual_aggregation_post_pin']
assert pt['actual_remaining_source_context_issue']['field']=='OVERV'and pt['actual_remaining_source_context_issue']['historical_machine_bit_replay']is False
assert post['actual_child_integer_exit_code']==2 and post['actual_Root_integer_exit_code']==0
for p in plan['eleven_saved_binary_input_pins']:seven(p)
for filename in ['COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json','ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json']:assert not(P/filename).exists()
allpins=selected+plan['complete_source_file_pins']+[genpin,plan['Source_author_pin'],phasepin]+metadata+plan['original_v10_published_metadata_pins']+plan['selected_closed_current_authority_pins']
for _ in range(2):
 for p in allpins+plan['eleven_saved_binary_input_pins']:seven(p)
result=dict(schema='INDEPENDENT_GENDF_ACTUAL_CUMULATIVE17_V11_CANDIDATE_WRITER_SOURCE_REVIEW_V1',status='PASS_GENDF_ACTUAL_CUMULATIVE17_V11_CANDIDATE_WRITER_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,Source_candidate_PASS=True,final_selected_Source_pins=selected,ready_pin=rp,plan_pin=pp,inverse_pin=ip,writer_source_pin=wp,actual_Source_generation_tools_pin=genpin,reviewer_source_pin=pin(__file__),
 all_three_whole_file_inverse_bytes_verified=True,all_scientific_parser_math_threshold_functions_preserved=True,actual_loaded_v6_SF_HF_pure_writer_mapping_executed_without_publication=True,actual_mapping_counts=scope['counts'],actual_publication_source_mapping=mapping,actual_projected_SF_complete5_Source_pins=mapped_sf['complete_source_file_pins'],all5_current_SF_Source_fullpins_equal_plan_candidate5=True,all7_exact_original_current_source_pointer_occurrences_replaced=True,no_three_old_source_fullpins_remaining_in_mapped_SF_HF=True,no_basename_or_generic_path_device_mapping=True,
 actual_ART_root_count=10,actual_REC_root_count=7,actual_total_runtime_root_count=17,complete_cumulative_runtime_roots=roots,actual_v10_already_published_Source_root_preserved=True,actual_explicit_metadata_file_pins=metadata,actual_explicit_metadata_file_bytes=15660,two_top_level_metadata_files_exact_PF_metered_without_REC_whole_scan=True,all17_roots_plus_exact2_files_share_original2GiB=True,actual_retained_capture_owner_root=capture,actual_retained_capture_owner_authority_pin=phasepin,original_both_capture_owner_comparisons_preserved_with_explicit_correct_owner=True,
 original_caps=CAPS,metadata18_Root32_oncewriter60_protocol_preserved=True,actual_corrected_aggregate_Root0_child2_and_OVERV_issue_preserved=True,all_current7_verified_twice=True,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_recipe_pin=None,actual_GENDF_report_pin=None,candidate_imported_or_executed=False,once_writer_executed=False,scientific_payload_EOF_or_native_tree_repeated=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),Source_candidate_PASS=True,actual_mapping_counts=scope['counts'],ART_roots=10,REC_roots=7,runtime_roots=17,explicit_metadata_file_bytes=15660)),flush=True)
