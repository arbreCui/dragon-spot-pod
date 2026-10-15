from pathlib import Path
import hashlib,importlib.util,json,os,shlex,stat,sys
ROOT=Path('/Users/wen/spot');R=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';P=R/'literal2_new_compare_duplicate_physical_release_source_20261014';D=Path(__file__).parent
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
 for k in ['actual_review_return','actual_postverification_return']:
  z=t[k];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==p
def module(p,name):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
pp=pin(P/'PLAN.json');plan=load(pp);cp=pin(P/'ACTUAL_EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_RECEIPT.json');receipt=load(cp);tp=pin(P/'ROOT_V3_ACTUAL_RELEASE_TRUE_TOOL_RETURNS.json');raw=load(tp);z=raw['actual_terminal_return']
assert cp['sha256'].startswith('2207a7be')and cp['size_bytes']==11283 and raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==0
assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and z['chunk_id']=='6c25fd'and json.loads(z['output'])['receipt_pin']==cp
sourceD=R/'independent_literal2_new_compare_duplicate_physical_selected_v3_Source_review_20261014';srp=pin(sourceD/'REVIEW.json');stp=pin(sourceD/'TRUE_TOOL_RETURNS.json');sreview=load(srp);tool0(load(stp),srp)
assert sreview['failure']is None and sreview['Source_candidate_PASS']is True and sreview['selected_plan_pin']==pp and pin(sreview['selected_Source_pin']['path'])==sreview['selected_Source_pin']
args=shlex.split(raw['exact_executed_command']);assert args[:3]==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',sreview['selected_Source_pin']['path']]
assert args[3:]==['--plan-sha256',pp['sha256'],'--plan-seven-id',json.dumps(pp['identity'],separators=(',',':')),'--mode','execute']
prior=load(plan['post_review_pin']);tool0(load(plan['post_tools_pin']),plan['post_review_pin'])
assert prior['actual_Root_integer_exit_code']==1 and prior['actual_original_resource_failure_retained']is True and prior['business_pass']is False
targets=plan['target_pins'];owner=plan['retained_complete_owner_pin'];retained=plan['retained_new_output_pins'];fixed=plan['fixed_current_pins']
assert receipt['schema']=='EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_RECEIPT_V1'and receipt['status']=='ACTUAL_EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASED_ONLY'and receipt['failure']is None
assert receipt['plan_pin']==pp and receipt['post_review_pin']==plan['post_review_pin']and receipt['retained_complete_owner_pin']==owner and receipt['exact_target_pins']==receipt['actual_released_pins']==targets
assert len(targets)==2 and receipt['actual_released_bytes']==sum(p['size_bytes']for p in targets)==68743634 and receipt['retained_new_output_pins']==retained and len(retained)==16 and len(fixed)==6050
assert receipt['original_Root_exit_code_retained']==1 and receipt['original_resource_failure_retained']is True and receipt['physics_qualified']is False and receipt['goal_complete']is False
assert retained==[p for p in prior['actual_complete_new_output_pins']if p not in targets]and owner in retained and owner['sha256']=='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60'
assert prior['all18_new_outputs_full_EOF_SHA_and_current7_verified']is True
for p in targets:assert p in prior['actual_complete_new_output_pins']and p['sha256']==owner['sha256']and p['size_bytes']==owner['size_bytes']==34371817 and not os.path.lexists(p['path'])
for p in fixed+retained:seven(p)
assert load(prior['actual_aggregate_host_pin'])['status']=='ACTUAL_CURRENT_EVIDENCE_FAILED_NO_RETRY'
assert load(prior['actual_aggregate_host_pin'])['failure']==prior['actual_host_failure']and load(prior['actual_aggregate_report_pin'])['all_raw_word_mismatches']==9501687
argv=load(prior['actual_Root_argv_pin']);request=load(argv['actual_request_pin']);roots=request['joint_archive_roots'];extra=request['explicit_cumulative_metadata_file_pins'];assert roots==prior['actual_joint25_roots']and len(roots)==25 and extra==prior['actual_explicit_external_metadata_file_pins']and len(extra)==4
support=module(R/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/prepare_cli_host_v15.py','dup2_actual_post_original_support');helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'dup2_actual_post_original_helper');full,production=helper.modules()
assert Path(production.__file__).resolve()==support.PARENT
snapshot=production.DiskResources(ROOT/'validation',roots,8*2**30,2**31).check();external=0
for p in extra:
 seven(p);assert pin(p['path'])==p
 if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):external+=p['size_bytes']
assert external==prior['actual_explicit_external_metadata_bytes']==22676 and prior['actual_current_original_joint_role_bytes']-snapshot['artifact_bytes']==68743634 and prior['actual_original_DiskResources_failure_snapshot']['regular_files']-snapshot['regular_files']==2
complete=snapshot['artifact_bytes']+external;assert complete==2080966373 and prior['actual_current_complete_joint_roots_plus_metadata_bytes']-complete==68743634 and complete<2**31
package=[]
for p in sorted(P.iterdir()):assert p.is_file()and not p.is_symlink();package.append(pin(p))
assert len(package)==10 and all(not Path(p['path']).is_relative_to(Path(root))for p in package for root in roots)
packagebytes=sum(p['size_bytes']for p in package)
for p in fixed+retained:seven(p)
for p in targets:assert not os.path.lexists(p['path'])
for p in package:seven(p)
result=dict(schema='INDEPENDENT_LITERAL2_NEW_COMPARE_DUPLICATE_PHYSICAL_ACTUAL_RELEASE_POSTVERIFICATION_V1',status='PASS_ACTUAL_LITERAL2_NEW_COMPARE_DUPLICATE_PHYSICAL_RELEASE_POSTVERIFICATION',failure=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,actual_Root_release_integer_exit_code=0,actual_Root_release_true_tool_pin=tp,actual_release_receipt_pin=cp,actual_selected_Source_pin=sreview['selected_Source_pin'],actual_selected_plan_pin=pp,actual_Source_review_pin=srp,actual_Source_tools_pin=stp,actual_prior_compare_post_review_pin=plan['post_review_pin'],actual_prior_compare_post_tools_pin=plan['post_tools_pin'],retained_complete_owner_pin=owner,owner_original_full_EOF_SHA_proof_composed_with_current7_only=True,original_owner_payload_EOF_not_repeated=True,exact_released_historical_target_pins=targets,actual_two_literal_target_paths_absent=True,actual_released_file_count=2,actual_released_bytes=68743634,actual_fixed_current_pin_count=6050,actual_retained_new_output_count=16,all6050_fixed_and16_retained_current7_verified_twice=True,original_all_SQLite_pools_comparison_reports_logs_and_archives_retained=True,actual_original_compare_host_pin=prior['actual_aggregate_host_pin'],actual_original_compare_child_pin=prior['actual_aggregate_report_pin'],original_compare_Root_exit_code_retained=1,original_compare_resource_failure_retained=True,original_compare_failure=prior['actual_host_failure'],original_positional_mismatch_reports_not_rewritten=True,actual_original_joint25_resource_snapshot_after_release=snapshot,actual_joint25_role_bytes_after_release=snapshot['artifact_bytes'],actual_joint25_regular_file_count_after_release=snapshot['regular_files'],actual_external_metadata_file_pins=extra,actual_external_metadata_bytes=external,actual_complete_joint25_plus_metadata_after_release_bytes=complete,actual_original_joint25_byte_delta=68743634,actual_original_joint25_file_delta=2,original_joint2GiB_cap_unchanged=True,actual_current_joint2GiB_margin_bytes=2**31-complete,actual_release_package_root=str(P),actual_release_package_metadata_pins=package,actual_release_package_metadata_file_count=len(package),actual_release_package_metadata_bytes=packagebytes,release_package_outside_original25_requires_explicit_next_cumulative_root=True,required_following_cumulative_release_evidence_roots=[str(P),str(sourceD),str(D)],physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,no_original_scientific_payload_or_native_tree_read=True,no_business_retry_or_Source_mutation=True,reviewer_source_pin=pin(__file__))
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),actual_released_bytes=68743634,actual_joint25_plus_metadata_after_release_bytes=complete,actual_joint2GiB_margin_bytes=2**31-complete,actual_release_package_metadata_bytes=packagebytes)),flush=True)
