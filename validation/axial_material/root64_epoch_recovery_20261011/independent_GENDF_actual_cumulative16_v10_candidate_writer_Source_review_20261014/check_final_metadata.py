from pathlib import Path
import hashlib,importlib.util,json,os,shlex,stat,sys
sys.dont_write_bytecode=True
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_eleven_saved_gendf_actual_cumulative_sixteen_roots_host_source_v10_20261014'
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
def genuine0(t):
 assert t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
 z=t['actual_terminal_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None
 return json.loads(z['output'])
assert not(D/'FINAL_METADATA_REVIEW.json').exists()and not(D/'FINAL_METADATA_TRUE_TOOL_RETURNS.json').exists()
reviewpin=pin(D/'REVIEW.json');review=load(reviewpin);reviewtoolspin=pin(D/'TRUE_TOOL_RETURNS.json');rt=load(reviewtoolspin)
assert review['source_only']is True and review['failure']is None
z=rt['actual_review_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==reviewpin
ready=load(review['ready_pin']);plan=load(review['plan_pin'])
pubpin=pin(R/'ROOT_ACTUAL_GENDF_CUMULATIVE16_SOURCE_ONCE_PUBLICATION_TRUE_TOOL_RETURNS_20261014.json');pub=load(pubpin);published=genuine0(pub)
assert pub['actual_terminal_return']['chunk_id']=='6b32f9'and published['status']=='GENDF_SIXTEEN_ROOTS_SOURCE_METADATA_PUBLISHED_ONLY'
sp=published['source_freeze_pin'];hp=published['host_freeze_pin'];rp=published['recipe_pin'];sf=load(sp);hf=load(hp);recipe=load(rp)
assert sp['sha256']=='23f1f7ccea3fba958630fc63bd5be7a1a93009998b5e04f485d1455ba877aadb'and sp['size_bytes']==32393
assert hp['sha256']=='5636d942fa55e68f8e2e5a8c3edfff3489306c13ba9d94952fa6723daa209ad3'and hp['size_bytes']==2559772
assert rp['sha256']=='5ddc052b5ed5d379214805909a1ee49f32dcf59d550e547e6394a998036c8a0b'and rp['size_bytes']==3653
assert hf['selected_source_freeze_pin']==sp==recipe['selected_source_freeze_pin']and recipe['selected_host_freeze_pin']==hp
assert hf['host_source']==recipe['host_source_pin']==plan['candidate_host_source_pin']
assert sf['same_round_Source_review_pin']==hf['same_round_Source_review_pin']==reviewpin
assert sf['same_round_Source_tools_pin']==hf['same_round_Source_tools_pin']==reviewtoolspin
assert sf['current_plan_pin']==ready['plan_pin']and sf['original_caps']==hf['original_caps']==plan['original_caps']
assert len(sf['complete_source_file_pins'])==5
for p in sf['complete_source_file_pins']:assert pin(p['path'])==p
assert {p['path']:p for p in sf['complete_source_file_pins']}=={p['path']:p for p in plan['complete_source_file_pins']}
for p in ready['selected_Source_pins']+[review['ready_pin']]:
 assert p in review['final_selected_Source_pins']and pin(p['path'])==p
deps=hf['dependencies'];table={p['path']:p for p in deps};assert len(deps)==len(table)==5994
for p in deps:seven(p)
for p in ready['selected_Source_pins']+[review['ready_pin'],reviewpin,reviewtoolspin,sp]:assert table[p['path']]==p
bp=pin(R/'ROOT_ACTUAL_GENDF_CUMULATIVE16_METADATA18_BINDER_TRUE_TOOL_RETURNS_20261014.json');binder=load(bp);bound=genuine0(binder)
ap=pin(R/'ROOT_EXACT_GENDF_CUMULATIVE16_ACTUAL32_ARGV_20261014.json');a=load(ap)
assert a==bound and a['host_or_parser_launched']is False and len(a['argv'])==32 and shlex.split(a['shell_safe_command'])==a['argv']
observedpin=a['actual_material_observation_report_pin'];observed=load(observedpin)
assert observedpin['sha256']=='57bf99b1627fb24ce9e72b1cc1783562a62e588a70446f7dc1d62f9bd874a697'
assert observed['status']=='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'and observed['failure']is None and observed['after_check_error']is None
assert observed['actual_full_A_observation_executed']is True and observed['actual_B_observation_executed']is False
assert len(recipe['argv_prefix'])==24 and len(recipe['final_output_option'])==2
assert a['argv']==recipe['argv_prefix']+['--material-observation-report-summary',observedpin['path'],'--material-observation-report-sha256',observedpin['sha256'],'--material-observation-report-seven-id',json.dumps(observedpin['identity'],separators=(',',':'))]+recipe['final_output_option']
assert recipe['argv_prefix'][11]==hf['host_source']['path']
assert recipe['argv_prefix'][12:]==['--source-freeze-summary',sp['path'],'--source-freeze-sha256',sp['sha256'],'--source-freeze-seven-id',json.dumps(sp['identity'],separators=(',',':')),'--host-freeze-summary',hp['path'],'--host-freeze-sha256',hp['sha256'],'--host-freeze-seven-id',json.dumps(hp['identity'],separators=(',',':'))]
bcmd=shlex.split(binder['exact_executed_command']);assert len(bcmd)==18 and bcmd[11]==str(P/'build_root_reviewable_actual_gendf_cli.py')
assert bcmd[12:]==a['argv'][24:30]
art=sf['cumulative_artifact_root_paths'];rec=sf['cumulative_Source_root_paths'];roots=art[:3]+rec+art[3:]
assert art==plan['cumulative_artifact_root_paths']and rec==plan['cumulative_Source_root_paths']and len(art)==10 and len(rec)==6 and len(roots)==len(set(roots))==16
assert set(roots)==set(plan['complete_cumulative_sixteen_role_roots'])and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)
assert sf['expected_original_DiskResources_ART_role_count']==10 and sf['complete_joint_source_tree_role_count']==6 and sf['complete_cumulative_joint_root_count']==hf['complete_cumulative_joint_root_count']==16
assert recipe['final_output_option']==['--output-dir',plan['planned_actual_output_root']]
assert not os.path.lexists(plan['planned_actual_output_root'])and not os.path.lexists(plan['planned_actual_evidence_root'])
for obj in [published,sf,hf,recipe]:
 for k,v in obj.items():
  if k.endswith('_qualified')or k in ['AAA_qualified','ABA_admitted','goal_complete','GENDF_executed','parser_executed','candidate_executed']:assert v is False
spec=importlib.util.spec_from_file_location('GENDF_final_original_resource_metadata_only',R/'storage_release_literal5_closed_old_map007011_source_v1_20261014/literal11_release_common.py');original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
current=original.budget();assert current['original_initial_reserve_admitted']is True and current['remaining_after_original_initial_reserves_bytes']>0
caps=plan['original_caps'];assert current['original_cold_reserve_bytes']==caps['cold_reserve_bytes']and current['metadata_reserve_bytes']==caps['metadata_reserve_bytes']and current['initial_fresh_reserve_bytes']==caps['fresh_bytes']and current['artifact_budget_bytes']==caps['history_bytes']and current['min_free_bytes']==caps['free_floor_bytes']
for p in deps+[sp,hp,rp,pubpin,bp,ap,observedpin,reviewpin,reviewtoolspin]+review['final_selected_Source_pins']:seven(p)
assert not os.path.lexists(plan['planned_actual_output_root'])and not os.path.lexists(plan['planned_actual_evidence_root'])
result=dict(schema='INDEPENDENT_GENDF_ACTUAL_CUMULATIVE16_V10_FINAL_METADATA_REVIEW_V1',status='PASS_GENDF_ACTUAL_CUMULATIVE16_V10_FINAL_METADATA_READY_FOR_UNIQUE_ROOT32',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,
 actual_Source_freeze_pin=sp,actual_Host_freeze_pin=hp,actual_recipe_pin=rp,actual_Source_candidate_writer_review_pin=reviewpin,actual_Source_candidate_writer_review_tools_pin=reviewtoolspin,actual_Source_publication_true_tool_pin=pubpin,actual_metadata18_binder_true_tool_pin=bp,actual_Root32_argv_pin=ap,actual_material_observation_report_pin=observedpin,reviewer_source_pin=pin(__file__),
 all5_original_Source_whole_EOF_SHA_and7_verified=True,all6_selected_Source_plus_READY_exact_verified=True,current_HF_dependency_count=5994,all5994_HF_current7_verified_twice=True,recipe_prefix24_actual_phase6_output2_exact_Root32=True,actual_metadata18_and_publication_returns_genuine_closed_integer0=True,original_caps=caps,complete_disjoint_cumulative_runtime_roots=roots,actual_ART_root_count=10,actual_REC_root_count=6,actual_total_root_count=16,
 actual_current_original_factory=current,actual_current_original_fullfresh2_reserve_admitted=True,new_host_and_evidence_outputs_absent=True,actual_future_GENDF_report_pin=None,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,large_scientific_payload_EOF_or_native_tree_repeated=False,no_new_approval_layer=True)
p=D/'FINAL_METADATA_REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),actual_HF_dependency_count=5994,actual_current_original_fullfresh2_reserve_admitted=current['original_initial_reserve_admitted'],actual_current_original_fullfresh2_margin_bytes=current['remaining_after_original_initial_reserves_bytes'],actual_Root32_argv_pin=ap)),flush=True)
